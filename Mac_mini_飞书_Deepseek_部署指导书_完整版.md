Mac mini + 飞书 + Deepseek Chat 大模型部署对接详细指导书

版本: v1.0
更新日期: 2026年3月5日
适用平台: macOS Sonoma 14.0+
目标硬件: Mac mini M2/M3/M4

目录

1. 项目概述
2. 系统架构
3. 硬件与系统要求
4. 环境准备
5. Ollama与Deepseek部署
6. 飞书机器人配置
7. 系统集成开发
8. 部署与运维
9. 故障排除
10. 附录

一、项目概述

1.1 项目目标
构建一个基于Mac mini的私有化AI助手系统，实现：
- 本地部署Deepseek大语言模型
- 通过飞书机器人提供对话服务
- 数据完全本地化，保障隐私安全
- 支持多端访问（手机、电脑、平板）

1.2 技术方案
- 硬件平台: Mac mini (Apple Silicon)
- 模型运行: Ollama
- AI模型: Deepseek-R1系列
- 消息平台: 飞书开放平台
- 开发框架: Python + FastAPI
- 部署方式: Docker容器化

1.3 应用场景
- 企业私有化AI助手
- 个人知识管理助手
- 团队协作智能工具
- 敏感数据处理场景

二、系统架构

2.1 整体架构

用户层（飞书APP/网页端/桌面端）
    ↓
飞书开放平台（消息网关/事件订阅/身份认证）
    ↓ Webhook
AI服务层（FastAPI服务/消息处理器/会话管理）
    ↓ API调用
Ollama服务层（Deepseek模型/模型管理/API网关）

2.2 核心组件

组件              技术选型           作用
消息网关          飞书Webhook        接收用户消息
API服务           FastAPI            HTTP接口服务
模型推理          Ollama             本地模型运行
AI模型            Deepseek-R1        大语言模型
数据存储          SQLite/Redis       会话和缓存

三、硬件与系统要求

3.1 推荐配置

基础版（个人使用）:
- 设备: Mac mini M2
- 内存: 16GB 统一内存
- 存储: 512GB SSD
- 网络: 千兆以太网
- 模型: Deepseek-R1 7B
- 并发: 支持1-2人同时使用

标准版（小型团队）:
- 设备: Mac mini M3 Pro
- 内存: 32GB 统一内存
- 存储: 1TB SSD
- 网络: 2.5Gb以太网
- 模型: Deepseek-R1 14B
- 并发: 支持3-5人同时使用

专业版（企业级）:
- 设备: Mac Studio M2 Ultra
- 内存: 64GB 统一内存
- 存储: 2TB SSD
- 网络: 10Gb以太网
- 模型: Deepseek-R1 32B/70B
- 并发: 支持10+人同时使用

3.2 性能参考

模型    内存占用    推理速度        适用场景
1.5B    2GB         50 tokens/s     简单问答
7B      6GB         25 tokens/s     日常对话
14B     12GB        15 tokens/s     复杂推理
32B     24GB        8 tokens/s      专业任务

四、环境准备

4.1 安装Homebrew

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

4.2 安装Docker Desktop

brew install --cask docker

或从官网下载：https://www.docker.com/products/docker-desktop/

4.3 安装Python 3.11

brew install python@3.11
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

4.4 创建项目目录

mkdir -p ~/AI-Assistant/{config,data,logs,models,scripts}
cd ~/AI-Assistant
python3 -m venv venv
source venv/bin/activate

五、Ollama与Deepseek部署

5.1 安装Ollama

curl -fsSL https://ollama.com/install.sh | sh
ollama --version

5.2 配置Ollama

export OLLAMA_HOST=0.0.0.0:11434
export OLLAMA_MODELS=~/AI-Assistant/models
export OLLAMA_NUM_PARALLEL=4

5.3 下载Deepseek模型

# 下载7B模型（推荐）
ollama pull deepseek-r1:7b

# 下载14B模型（性能更好）
ollama pull deepseek-r1:14b

# 查看已下载模型
ollama list

5.4 启动Ollama服务

# 前台启动
ollama serve

# 后台启动
nohup ollama serve > ~/AI-Assistant/logs/ollama.log 2>&1 &

5.5 测试模型

# 交互式对话
ollama run deepseek-r1:7b

# API测试
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-r1:7b",
  "prompt": "你好",
  "stream": false
}'

六、飞书机器人配置

6.1 创建应用

1. 访问 https://open.feishu.cn/
2. 登录并进入开发者后台
3. 创建企业自建应用
4. 填写应用信息：
   - 应用名称: AI智能助手
   - 应用描述: 基于Deepseek的私有化AI助手

6.2 记录应用凭证

创建完成后记录：
- App ID: cli_xxxxxxxxxxxxxxxx
- App Secret: xxxxxxxxxxxxxxxxxxxxxxxx
- Verification Token: xxxxxxxxxxxxxxxxxx

6.3 配置权限

申请以下权限：
- contact:user.id:readonly - 获取用户ID
- im:message - 发送消息
- im:message.group_at_msg - 接收群@消息
- im:message.p2p_msg - 接收私聊消息

6.4 配置Webhook

1. 进入事件订阅页面
2. 配置请求地址：http://你的IP:8080/webhook
3. 添加订阅事件：im.message.receive_v1

6.5 发布应用

1. 进入版本管理与发布
2. 创建版本（如1.0.0）
3. 申请发布

6.6 添加机器人到群组

1. 进入飞书群组
2. 设置 -> 群机器人
3. 添加机器人
4. 选择创建的AI助手

七、系统集成开发

7.1 安装Python依赖

pip install fastapi uvicorn httpx python-dotenv lark-oapi

7.2 核心代码 (main.py)

#!/usr/bin/env python3
import os
import json
import hmac
import hashlib
import logging
from fastapi import FastAPI, Request, HTTPException
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")

class OllamaClient:
    def __init__(self, host, model):
        self.host = host
        self.model = model
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def chat(self, message):
        response = await self.client.post(
            f"{self.host}/api/generate",
            json={
                "model": self.model,
                "prompt": message,
                "stream": False
            }
        )
        result = response.json()
        return result.get("response", "抱歉，我无法回答")

ollama = OllamaClient(OLLAMA_HOST, OLLAMA_MODEL)

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.body()
    event_data = json.loads(body)
    
    # URL验证
    if event_data.get("type") == "url_verification":
        return {"challenge": event_data.get("challenge")}
    
    # 处理消息
    event = event_data.get("event", {})
    message = event.get("message", {})
    content = json.loads(message.get("content", "{}"))
    text = content.get("text", "").strip()
    chat_id = message.get("chat_id", "")
    
    # 调用AI
    ai_response = await ollama.chat(text)
    
    # 发送回复（简化版，实际需要调用飞书API）
    logger.info(f"回复: {ai_response}")
    
    return {"code": 0, "msg": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

7.3 环境变量配置 (.env)

FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_VERIFICATION_TOKEN=xxxxxxxxxxxxxxxx
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:7b

7.4 启动服务

source venv/bin/activate
python main.py

八、部署与运维

8.1 Docker部署

docker-compose.yml:

version: '3.8'
services:
  ai-assistant:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
    depends_on:
      - ollama
    restart: unless-stopped
  
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ./models:/root/.ollama/models
    restart: unless-stopped

启动：docker-compose up -d

8.2 配置开机自启动

创建启动脚本 scripts/start.sh:

#!/bin/bash
cd ~/AI-Assistant
source venv/bin/activate
nohup python src/main.py > logs/app.log 2>&1 &
echo $! > logs/app.pid

创建launchd配置 ~/Library/LaunchAgents/com.ai-assistant.plist:

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-assistant</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>/Users/yourname/AI-Assistant/scripts/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>

加载配置：
launchctl load ~/Library/LaunchAgents/com.ai-assistant.plist

8.3 监控与日志

查看日志：
tail -f ~/AI-Assistant/logs/app.log

健康检查：
curl http://localhost:8080/health

九、故障排除

9.1 Ollama连接失败

症状：Connection refused
解决：
- 检查Ollama是否运行：ps aux | grep ollama
- 启动Ollama：ollama serve
- 检查端口：lsof -i :11434

9.2 飞书签名验证失败

症状：签名验证失败
解决：
- 检查FEISHU_APP_SECRET是否正确
- 确保系统时间准确

9.3 模型回复慢

解决：
- 使用更小的模型（如7B代替14B）
- 减少num_predict参数
- 关闭其他占用资源的应用

9.4 端口被占用

症状：Address already in use
解决：
lsof -i :8080
kill -9 <PID>

十、附录

10.1 常用命令

命令                              用途
ollama list                       列出模型
ollama pull <model>               下载模型
ollama run <model>                运行模型
curl http://localhost:8080/health 健康检查
tail -f logs/app.log              查看日志

10.2 资源链接

- 飞书开放平台：https://open.feishu.cn/
- Ollama官网：https://ollama.com/
- Deepseek官网：https://www.deepseek.com/
- Docker Desktop：https://www.docker.com/products/docker-desktop/

10.3 升级维护

升级模型：
ollama pull deepseek-r1:7b

备份配置：
tar -czf backup-$(date +%Y%m%d).tar.gz AI-Assistant/

查看日志：
grep ERROR logs/app.log

---

文档结束

作者：Jarvis AI助手
创建日期：2026年3月5日
版本：v1.0
