                "create_time": message.get("create_time")
            }
            
        except Exception as e:
            logger.error(f"解析消息失败: {e}")
            return {}
    
    async def close(self):
        """关闭连接"""
        await self.http_client.aclose()


# 全局机器人实例
feishu_bot = None

def get_feishu_bot() -> FeishuBot:
    """获取飞书机器人实例（单例模式）"""
    global feishu_bot
    if feishu_bot is None:
        from config import Config
        feishu_bot = FeishuBot(
            app_id=Config.FEISHU_APP_ID,
            app_secret=Config.FEISHU_APP_SECRET,
            verification_token=Config.FEISHU_VERIFICATION_TOKEN
        )
    return feishu_bot
```

**保存文件**。

---

### 5.5 编写配置模块

**创建 config.py**：

```python
"""
配置模块 - 管理所有配置项
"""

import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

class Config:
    """配置类"""
    
    # 飞书配置
    FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
    FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
    FEISHU_VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    FEISHU_ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY", "")
    
    # AI模型配置
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
    
    # 服务器配置
    SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "8080"))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # 日志配置
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    @classmethod
    def validate(cls) -> bool:
        """验证配置是否完整"""
        required = [
            cls.FEISHU_APP_ID,
            cls.FEISHU_APP_SECRET,
            cls.FEISHU_VERIFICATION_TOKEN
        ]
        
        missing = [i for i, v in enumerate(required) if not v]
        
        if missing:
            print("❌ 配置错误：以下必填项未设置")
            fields = ["FEISHU_APP_ID", "FEISHU_APP_SECRET", "FEISHU_VERIFICATION_TOKEN"]
            for i in missing:
                print(f"   - {fields[i]}")
            return False
        
        return True
```

**保存文件**。

---

### 5.6 编写主程序

**创建 main.py**：

```python
"""
主程序 - 启动Web服务器，处理飞书Webhook
"""

import os
import sys
import json
import logging
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# 确保可以导入本地模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from feishu_bot import get_feishu_bot
from ai_service import get_ai_service

# 配置日志
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("=" * 50)
    logger.info("AI助手服务启动中...")
    logger.info("=" * 50)
    
    # 验证配置
    if not Config.validate():
        logger.error("配置验证失败，请检查.env文件")
        sys.exit(1)
    
    # 检查AI服务
    ai = get_ai_service()
    if await ai.health_check():
        logger.info("✅ AI服务连接正常")
    else:
        logger.warning("⚠️ AI服务未启动，请确保Ollama正在运行")
    
    yield
    
    # 关闭时
    logger.info("正在关闭服务...")
    await get_feishu_bot().close()
    await get_ai_service().close()

app = FastAPI(
    title="AI助手服务",
    description="飞书 + Deepseek AI助手",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """根路径 - 服务状态"""
    return {
        "status": "running",
        "service": "AI助手",
        "version": "1.0.0",
        "time": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    ai = get_ai_service()
    ai_healthy = await ai.health_check()
    
    return {
        "status": "healthy" if ai_healthy else "degraded",
        "ai_service": "up" if ai_healthy else "down",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook")
async def feishu_webhook(request: Request):
    """
    飞书Webhook接收端点
    
    这是飞书发送消息通知的入口
    """
    try:
        # 获取请求头
        headers = request.headers
        timestamp = headers.get("X-Lark-Request-Timestamp", "")
        nonce = headers.get("X-Lark-Request-Nonce", "")
        signature = headers.get("X-Lark-Signature", "")
        
        # 获取请求体
        body = await request.body()
        
        logger.info(f"收到飞书请求: {timestamp}")
        
        # 解析JSON
        event_data = json.loads(body)
        
        # 处理URL验证（首次配置时使用）
        if event_data.get("type") == "url_verification":
            challenge = event_data.get("challenge", "")
            logger.info("处理URL验证请求")
            return {"challenge": challenge}
        
        # 验证签名（确保请求来自飞书）
        bot = get_feishu_bot()
        if not bot.verify_signature(timestamp, nonce, body, signature):
            logger.warning("签名验证失败，可能是伪造请求")
            raise HTTPException(status_code=403, detail="签名验证失败")
        
        # 处理消息事件
        event_type = event_data.get("header", {}).get("event_type", "")
        
        if event_type == "im.message.receive_v1":
            # 解析消息
            message = bot.parse_message(event_data)
            
            if not message:
                logger.warning("无法解析消息")
                return {"code": 0, "msg": "success"}
            
            user_text = message.get("text", "")
            chat_id = message.get("chat_id", "")
            sender_name = message.get("sender_name", "用户")
            
            logger.info(f"收到消息 from {sender_name}: {user_text[:50]}...")
            
            # 调用AI服务
            ai = get_ai_service()
            ai_response = await ai.chat(user_text)
            
            logger.info(f"AI回复: {ai_response[:50]}...")
            
            # 发送回复
            await bot.send_message(chat_id, ai_response)
            
            logger.info("消息处理完成")
        
        return {"code": 0, "msg": "success"}
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
        raise HTTPException(status_code=400, detail="无效的JSON格式")
    except Exception as e:
        logger.error(f"处理Webhook时出错: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="服务器内部错误")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 启动AI助手服务...")
    print(f"📡 监听地址: {Config.SERVER_HOST}:{Config.SERVER_PORT}")
    print(f"🤖 AI模型: {Config.OLLAMA_MODEL}")
    print(f"📱 飞书应用: {Config.FEISHU_APP_ID}")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        reload=Config.DEBUG,
        log_level=Config.LOG_LEVEL.lower()
    )
```

**保存文件**。

---

### 5.7 安装依赖并测试

**步骤1：安装Python依赖**

```bash
# 确保在虚拟环境中
source ~/AI-Assistant/venv/bin/activate

# 安装依赖
pip install fastapi uvicorn httpx python-dotenv
```

**步骤2：创建日志目录**

```bash
mkdir -p ~/AI-Assistant/logs
```

**步骤3：测试运行**

```bash
# 进入项目目录
cd ~/AI-Assistant

# 运行主程序
python main.py
```

**预期输出**：
```
🚀 启动AI助手服务...
📡 监听地址: 0.0.0.0:8080
🤖 AI模型: deepseek-r1:7b
📱 飞书应用: cli_xxxxxxxx
--------------------------------------------------
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
==================================================
AI助手服务启动中...
==================================================
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080
```

**步骤4：测试Webhook**

打开另一个终端窗口：

```bash
# 测试根路径
curl http://localhost:8080/

# 测试健康检查
curl http://localhost:8080/health
```

如果返回JSON数据，说明服务运行正常！

---

### 5.8 配置飞书Webhook（重要！）

**步骤1：获取Mac的IP地址**

在终端输入：
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

找到类似 `192.168.1.xxx` 的地址。

**步骤2：更新飞书开放平台配置**

1. 打开 https://open.feishu.cn/
2. 进入你的应用
3. 点击"事件订阅"
4. 在"请求地址"栏填写：
   ```
   http://你的IP:8080/webhook
   ```
   例如：`http://192.168.1.100:8080/webhook`

5. 点击"保存"

**步骤3：在群里测试**

1. 打开飞书，进入测试群组
2. @机器人，发送消息：
   ```
   @AI助手 你好
   ```

3. 等待几秒钟，机器人应该回复！

---

## 第六部分：部署上线（预计30分钟）

### 6.1 配置开机自启动

**为什么要配置自启动？**
这样Mac mini开机后，AI服务会自动运行，不需要手动启动。

**方法一：使用launchd（推荐）**

**步骤1：创建启动脚本**

```bash
# 创建启动脚本
cat > ~/AI-Assistant/start.sh << 'EOF'
#!/bin/bash
# AI助手启动脚本

cd ~/AI-Assistant
source venv/bin/activate
python main.py
EOF

# 添加执行权限
chmod +x ~/AI-Assistant/start.sh
```

**步骤2：创建launchd配置文件**

```bash
# 创建plist文件
cat > ~/Library/LaunchAgents/com.ai-assistant.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-assistant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$(echo $HOME)/AI-Assistant/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$(echo $HOME)/AI-Assistant/logs/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$(echo $HOME)/AI-Assistant/logs/launchd.error.log</string>
</dict>
</plist>
EOF
```

**步骤3：加载配置**

```bash
# 加载plist文件
launchctl load ~/Library/LaunchAgents/com.ai-assistant.plist

# 启动服务
launchctl start com.ai-assistant

# 检查状态
launchctl list | grep com.ai-assistant
```

**步骤4：测试开机自启动**

1. 重启Mac mini
2. 等待系统启动完成
3. 打开终端，检查服务是否运行：
   ```bash
   curl http://localhost:8080/health
   ```

---

### 6.2 设置监控告警

**创建简单的监控脚本**：

```bash
cat > ~/AI-Assistant/monitor.sh << 'EOF'
#!/bin/bash
# 监控脚本

LOG_FILE="$HOME/AI-Assistant/logs/monitor.log"

# 检查服务是否运行
check_service() {
    if curl -s http://localhost:8080/health > /dev/null; then
        echo "$(date): ✅ 服务运行正常" >> $LOG_FILE
        return 0
    else
        echo "$(date): ❌ 服务异常，尝试重启..." >> $LOG_FILE
        return 1
    fi
}

# 检查Ollama是否运行
check_ollama() {
    if pgrep -x "ollama" > /dev/null; then
        return 0
    else
        echo "$(date): ⚠️ Ollama未运行，尝试启动..." >> $LOG_FILE
        nohup ollama serve > $HOME/AI-Assistant/logs/ollama.log 2>&1 &
        return 1
    fi
}

# 主检查逻辑
main() {
    check_ollama
    check_service
    
    if [ $? -ne 0 ]; then
        # 重启服务
        launchctl stop com.ai-assistant
        sleep 2
        launchctl start com.ai-assistant
        echo "$(date): 🔄 服务已重启" >> $LOG_FILE
    fi
}

main
EOF

chmod +x ~/AI-Assistant/monitor.sh
```

**添加定时监控**：

```bash
# 添加到crontab，每5分钟检查一次
echo "*/5 * * * * $HOME/AI-Assistant/monitor.sh" | crontab -
```

---

### 6.3 性能优化建议

#### 1. 模型优化

**使用量化模型**（减少内存占用）：
```bash
# 下载量化版本（如果可用）
ollama pull deepseek-r1:7b-q4_0
```

**调整模型参数**：
在 `ai_service.py` 中修改：
```python
"options": {
    "temperature": 0.7,      # 创造性程度
    "num_predict": 1024,     # 最大生成token数
    "num_ctx": 4096,         # 上下文窗口大小
    "num_thread": 4          # CPU线程数
}
```

#### 2. 系统优化

**关闭不必要的动画**：
```bash
# 减少视觉效果
defaults write com.apple.dock expose-animation-duration -float 0
```

**调整内存压力**：
```bash
# 查看内存使用情况
vm_stat

# 清理内存缓存
sudo purge
```

#### 3. 网络优化

**使用有线网络**：
- 比WiFi更稳定
- 延迟更低

**配置DNS**：
```bash
# 使用更快的DNS
networksetup -setdnsservers Wi-Fi 8.8.8.8 114.114.114.114
```

---

## 第七部分：常见问题解决

### 7.1 安装问题

#### Q1: Homebrew安装失败

**症状**：
```
Failed to connect to raw.githubusercontent.com
```

**解决方案**：
1. 检查网络连接
2. 尝试使用镜像源：
   ```bash
   export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
   export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

---

#### Q2: Ollama下载模型很慢

**症状**：下载速度只有几十KB/s

**解决方案**：
1. 使用代理或VPN
2. 手动下载模型文件：
   - 从 https://ollama.com/library/deepseek-r1 下载
   - 放到 `~/.ollama/models/` 目录

---

#### Q3: Python包安装失败

**症状**：
```
ERROR: Could not find a version that satisfies the requirement xxx
```

**解决方案**：
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxx
```

---

### 7.2 运行问题

#### Q1: 服务启动失败，端口被占用

**症状**：
```
Address already in use
```

**解决方案**：
```bash
# 查找占用8080端口的进程
lsof -i :8080

# 杀死进程
kill -9 <PID>

# 或修改端口
# 在.env文件中修改 SERVER_PORT=8081
```

---

#### Q2: AI回复很慢或超时

**可能原因**：
1. 模型太大，内存不足
2. CPU负载过高
3. 生成内容太长

**解决方案**：
1. 使用更小的模型（如1.5B或7B）
2. 减少 `num_predict` 参数
3. 关闭其他占用资源的应用
4. 升级Mac mini内存

---

#### Q3: 飞书收不到消息

**检查清单**：
- [ ] 服务是否运行？`curl http://localhost:8080/health`
- [ ] IP地址是否正确？
- [ ] 飞书Webhook配置是否正确？
- [ ] 防火墙是否放行8080端口？
- [ ] 机器人在群组中吗？

---

### 7.3 连接问题

#### Q1: 飞书签名验证失败

**症状**：日志显示"签名验证失败"

**解决方案**：
1. 检查 `.env` 文件中的 `FEISHU_APP_SECRET` 是否正确
2. 确保系统时间准确（时间不同步会导致签名失败）

---

#### Q2: 无法连接到Ollama

**症状**：
```
Connection refused
```

**解决方案**：
```bash
# 检查Ollama是否运行
ps aux | grep ollama

# 如果没有运行，启动它
ollama serve

# 检查端口
lsof -i :11434
```

---

## 附录

### A. 常用命令速查表

| 命令 | 用途 |
|------|------|
| `ollama list` | 列出已安装的模型 |
| `ollama pull <model>` | 下载模型 |
| `ollama run <model>` | 运行模型 |
| `ollama rm <model>` | 删除模型 |
| `python main.py` | 启动AI助手服务 |
| `curl http://localhost:8080/health` | 检查服务健康 |
| `tail -f logs/app.log` | 查看实时日志 |
| `launchctl start com.ai-assistant` | 启动服务 |
| `launchctl stop com.ai-assistant` | 停止服务 |

---

### B. 完整配置文件模板

#### .env 文件模板

```env
# ==========================================
# 飞书机器人配置
# ==========================================
FEISHU_APP_ID=cli_xxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxx
FEISHU_ENCRYPT_KEY=

# ==========================================
# AI模型配置
# ==========================================
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b

# ==========================================
# 服务器配置
# ==========================================
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG=False

# ==========================================
# 日志配置
# ==========================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

---

### C. 资源下载链接

#### 官方资源
- **飞书开放平台**: https://open.feishu.cn/
- **Ollama官网**: https://ollama.com/
- **Deepseek官网**: https://www.deepseek.com/
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/

#### 教程资源
- **Ollama GitHub**: https://github.com/ollama/ollama
- **FastAPI文档**: https://fastapi.tiangolo.com/
- **Python官方**: https://www.python.org/

#### 社区资源
- **Homebrew**: https://brew.sh/
- **VS Code**: https://code.visualstudio.com/

---

### D. 升级和维护

#### 如何升级模型？

```bash
# 拉取最新版本
ollama pull deepseek-r1:7b

# 查看模型更新日志
ollama show deepseek-r1:7b
```

#### 如何备份配置？

```bash
# 备份整个项目
cd ~
tar -czf ai-assistant-backup-$(date +%Y%m%d).tar.gz AI-Assistant/

# 备份到云存储（如有）
# cp ai-assistant-backup-*.tar.gz /path/to/backup/
```

#### 如何查看日志？

```bash
# 查看应用日志
tail -f ~/AI-Assistant/logs/app.log

# 查看Ollama日志
tail -f ~/AI-Assistant/logs/ollama.log

# 搜索错误
grep ERROR ~/AI-Assistant/logs/app.log
```

---

## 🎉 恭喜你！

如果你按照本指导书一步步操作到这里，你应该已经：

✅ 在Mac mini上成功部署了Deepseek AI模型  
✅ 创建了飞书机器人  
✅ 实现了飞书和AI的对接  
✅ 可以通过手机飞书随时随地和AI聊天  

### 接下来可以做什么？

1. **训练专属模型**：用你自己的数据微调模型
2. **添加更多功能**：如图片识别、语音对话
3. **接入其他平台**：如钉钉、企业微信
4. **优化性能**：让响应更快、更稳定

### 需要帮助？

如果遇到问题：
1. 查看本指导书的"常见问题"部分
2. 检查日志文件
3. 搜索相关错误信息
4. 联系技术支持

---

**祝使用愉快！** 🚀

*本指导书由 Jarvis AI助手 编写*  
*最后更新: 2026年3月5日*
