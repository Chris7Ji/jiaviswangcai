# Mac mini + 飞书 + Deepseek Chat 大模型部署对接详细指导书

## 文档信息
- **文档标题**: Mac mini + 飞书 + Deepseek Chat 大模型部署对接详细指导书
- **作者**: Jarvis AI助手
- **创建日期**: 2026年3月5日
- **版本**: v1.0
- **适用对象**: 技术开发者、AI应用部署人员、企业IT管理员

## 目录

### 第一部分：系统架构概述
1.1 整体架构设计
1.2 技术栈组成
1.3 硬件要求
1.4 软件环境

### 第二部分：Mac mini 环境准备
2.1 Mac mini 硬件配置建议
2.2 macOS 系统配置
2.3 开发环境安装
2.4 必要的系统工具

### 第三部分：Deepseek Chat 大模型部署
3.1 Deepseek Chat 模型介绍
3.2 本地部署方案
3.3 API服务部署
3.4 模型优化与调优

### 第四部分：飞书开放平台集成
4.1 飞书开放平台注册
4.2 应用创建与配置
4.3 权限申请与审核
4.4 Webhook配置

### 第五部分：系统集成与对接
5.1 消息路由设计
5.2 API接口开发
5.3 安全认证机制
5.4 错误处理与日志

### 第六部分：部署与运维
6.1 系统部署步骤
6.2 监控与告警
6.3 性能优化
6.4 故障排除

### 第七部分：最佳实践与案例
7.1 企业级部署建议
7.2 安全合规考虑
7.3 成本优化策略
7.4 实际应用案例

### 附录
A. 常用命令参考
B. 配置文件示例
C. 故障代码速查
D. 资源链接

---

## 第一部分：系统架构概述

### 1.1 整体架构设计

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   飞书客户端     │────▶│  飞书开放平台    │────▶│  自定义服务层    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                          │
                                                          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │
│   Mac mini      │◀───│   API网关层     │◀───│  Deepseek Chat  │
│   (部署服务器)   │    │                 │    │   大模型服务    │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 技术栈组成

#### 硬件层
- **Mac mini**: M2/M3芯片，16GB+内存，512GB+存储
- **网络**: 稳定的互联网连接，建议企业级路由器

#### 软件层
- **操作系统**: macOS Sonoma 14.0+
- **容器化**: Docker Desktop for Mac
- **编程语言**: Python 3.9+
- **Web框架**: FastAPI/Flask
- **数据库**: SQLite/PostgreSQL (可选)
- **消息队列**: Redis (可选)

#### 服务层
- **飞书集成**: 飞书开放平台SDK
- **AI模型**: Deepseek Chat API/本地模型
- **API服务**: 自定义中间件
- **监控**: Prometheus + Grafana (可选)

### 1.3 硬件要求

#### 最低配置 (基础测试)
- Mac mini with M2芯片
- 16GB 统一内存
- 512GB SSD存储
- 千兆以太网

#### 推荐配置 (生产环境)
- Mac mini with M3 Pro芯片
- 32GB 统一内存
- 1TB SSD存储
- 10Gb以太网 (可选)
- 不间断电源 (UPS)

#### 扩展配置 (企业级)
- Mac Studio with M2 Ultra
- 64GB+ 统一内存
- 2TB+ SSD存储
- 冗余网络连接
- 备份存储系统

### 1.4 软件环境要求

#### 系统软件
- macOS 14.0 (Sonoma) 或更高版本
- Xcode Command Line Tools
- Homebrew 包管理器

#### 开发工具
- Python 3.9+ 及 pip
- Node.js 18+ (可选，用于前端)
- Git 版本控制
- Visual Studio Code 或 PyCharm

#### 容器与虚拟化
- Docker Desktop for Mac
- Docker Compose
- Minikube (可选，用于Kubernetes测试)

---

## 第二部分：Mac mini 环境准备

### 2.1 Mac mini 硬件配置建议

#### 购买建议
1. **芯片选择**: M3芯片提供最佳性能功耗比
2. **内存配置**: 至少16GB，推荐32GB用于模型推理
3. **存储配置**: 512GB起步，1TB更佳
4. **网络配置**: 有线连接更稳定，Wi-Fi 6E作为备份

#### 物理环境
1. **散热**: 确保良好通风，避免过热
2. **电源**: 使用原装电源，考虑UPS
3. **网络**: 固定IP地址，配置端口转发

### 2.2 macOS 系统配置

#### 基础配置
```bash
# 1. 更新系统到最新版本
sudo softwareupdate -i -a

# 2. 安装Xcode Command Line Tools
xcode-select --install

# 3. 安装Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 4. 配置Shell环境 (使用zsh)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### 安全配置
```bash
# 1. 启用防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on

# 2. 配置SSH (如果需要远程访问)
sudo systemsetup -setremotelogin on

# 3. 创建专用用户
sudo dscl . -create /Users/aiadmin
sudo dscl . -create /Users/aiadmin UserShell /bin/zsh
sudo dscl . -create /Users/aiadmin RealName "AI Admin"
sudo dscl . -create /Users/aiadmin UniqueID 1001
sudo dscl . -create /Users/aiadmin PrimaryGroupID 20
sudo dscl . -create /Users/aiadmin NFSHomeDirectory /Users/aiadmin
sudo dscl . -passwd /Users/aiadmin 你的密码
```

### 2.3 开发环境安装

#### Python环境配置
```bash
# 1. 安装Python
brew install python@3.11

# 2. 配置虚拟环境
python3 -m venv ~/venv/ai
source ~/venv/ai/bin/activate

# 3. 安装基础包
pip install --upgrade pip
pip install numpy pandas matplotlib
pip install fastapi uvicorn httpx
pip install python-dotenv loguru
```

#### Docker环境配置
```bash
# 1. 安装Docker Desktop for Mac
# 从官网下载: https://www.docker.com/products/docker-desktop/

# 2. 配置Docker
docker --version
docker-compose --version

# 3. 测试Docker运行
docker run hello-world
```

#### 其他必要工具
```bash
# 1. Git配置
brew install git
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"

# 2. 网络工具
brew install curl wget nmap

# 3. 监控工具
brew install htop glances

# 4. 文本编辑器
brew install vim nano
```

### 2.4 必要的系统工具

#### 性能监控工具
```bash
# 1. 安装系统监控
brew install glances
brew install htop

# 2. 网络监控
brew install iftop nethogs

# 3. 磁盘监控
brew install ncdu
```

#### 开发辅助工具
```bash
# 1. API测试工具
brew install postman

# 2. 数据库工具 (如果需要)
brew install --cask dbeaver-community

# 3. 日志查看
brew install lnav
```

#### 安全工具
```bash
# 1. SSH密钥管理
ssh-keygen -t ed25519 -C "你的邮箱"

# 2. 证书工具
brew install mkcert
mkcert -install

# 3. 网络扫描
brew install nmap
```

---

## 第三部分：Deepseek Chat 大模型部署

### 3.1 Deepseek Chat 模型介绍

#### 模型特性
- **模型架构**: Transformer-based
- **上下文长度**: 通常128K tokens
- **多语言支持**: 中文优化良好
- **API接口**: RESTful API
- **本地部署**: 支持私有化部署

#### 部署选项对比

| 部署方式 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| **API调用** | 简单快速，无需硬件 | 依赖网络，有费用 | 测试、小规模使用 |
| **本地部署** | 数据安全，低延迟 | 硬件要求高 | 企业内网、敏感数据 |
| **混合部署** | 灵活平衡 | 配置复杂 | 中大型企业 |

### 3.2 本地部署方案

#### 方案一：使用官方Docker镜像 (推荐)
```bash
# 1. 拉取Deepseek Chat Docker镜像
docker pull deepseek/deepseek-chat:latest

# 2. 创建配置文件
mkdir -p ~/deepseek/config
cat > ~/deepseek/config/model_config.yaml << EOF
model:
  name: "deepseek-chat"
  path: "/models/deepseek-chat"
  device: "cuda"  # 或 "cpu" 如果没有GPU
  
server:
  host: "0.0.0.0"
  port: 8000
  workers: 2
  
api:
  enable: true
  auth_token: "你的认证令牌"
EOF

# 3. 运行容器
docker run -d \
  --name deepseek-chat \
  -p 8000:8000 \
  -v ~/deepseek/config:/config \
  -v ~/deepseek/models:/models \
  --restart unless-stopped \
  deepseek/deepseek-chat:latest \
  --config /config/model_config.yaml
```

#### 方案二：从源码编译部署
```bash
# 1. 克隆仓库
git clone https://github.com/deepseek-ai/DeepSeek-Chat.git
cd DeepSeek-Chat

# 2. 安装依赖
pip install -r requirements.txt

# 3. 下载模型权重
# 需要申请模型权重，参考官方文档

# 4. 启动服务
python -m deepseek_chat.serve \
  --model-path ./models/deepseek-chat \
  --port 8000 \
  --host 0.0.0.0
```

#### 方案三：使用Ollama部署 (简化版)
```bash
# 1. 安装Ollama
brew install ollama

# 2. 拉取Deepseek模型
ollama pull deepseek-chat

# 3. 运行模型
ollama run deepseek-chat

# 4. 通过API访问
curl http://localhost:11434/api/generate -d '{
  "model": "deepseek-chat",
  "prompt": "你好",
  "stream": false
}'
```

### 3.3 API服务部署

#### 创建API包装层
```python
# api_wrapper.py
import os
import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(title="Deepseek Chat API Wrapper")

# 请求模型
class ChatRequest(BaseModel):
    messages: list
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False

class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list
    usage: dict

# 配置
DEEPSEEK_API_BASE = os.getenv("DEEPSEEK_API_BASE", "http://localhost:8000")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-api-key")

# HTTP客户端
client = httpx.AsyncClient(
    base_url=DEEPSEEK_API_BASE,
    headers={
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    },
    timeout=30.0
)

@app.post("/v1/chat/completions")
async def chat_completion(request: ChatRequest):
    """Deepseek Chat API接口"""
    try:
        response = await client.post(
            "/v1/chat/completions",
            json=request.dict(exclude_none=True)
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        logger.error(f"API调用失败: {e}")
        raise HTTPException(status_code=500, detail="模型服务暂时不可用")

@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        response = await client.get("/health")
        return {"status": "healthy", "model": "deepseek-chat"}
    except:
        return {"status": "unhealthy", "model": "deepseek-chat"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

#### 使用Docker Compose部署
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Deepseek Chat 模型服务
  deepseek-chat:
    image: deepseek/deepseek-chat:latest
    container_name: deepseek-chat
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
      - ./config:/config
    environment:
      - MODEL_PATH=/models/deepseek-chat
      - DEVICE=cpu  # 或 cuda 如果有GPU
    restart: unless-stopped
    networks:
      - ai-network

  # API包装层
  api-wrapper:
    build: .
    container_name: api-wrapper
    ports:
      - "8080:8080"
    environment:
      - DEEPSEEK_API_BASE=http://deepseek-chat:8000
      - DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}
    depends_on:
      - deepseek-chat
    restart: unless-stopped
    networks:
      - ai-network

  # 反向代理 (可选)
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api-wrapper
    restart: unless-stopped
    networks:
      - ai-network

networks:
  ai-network:
    driver: bridge
```

### 3.4 模型优化与调优

#### 性能优化
```python
# 模型推理优化配置
optimization_config = {
    "quantization": "int8",  # 量化减少内存占用
    "batch_size": 4,         # 批量推理提高吞吐
    "cache_size": 1000,      # KV缓存大小
    "threads": 4,            # CPU线程数
    "gpu_layers": 20,        # GPU层数 (如果有GPU)
}
```

#### 内存优化策略
1. **模型量化**: 使用4-bit或8-bit量化
2. **分片加载**: 大模型分片加载到内存
3. **缓存优化**: 优化KV缓存策略
4. **流式响应**: 减少内存峰值使用

#### 监控与调优
```bash
# 监控模型服务性能
docker stats deepseek-chat

# 查看日志
docker logs -f deepseek-chat

# 性能测试
ab -n 1000 -c 10 http://localhost:8080/v1/chat/completions
```

---

## 第四部分：飞书开放平台集成

### 4.1 飞书开放平台注册

#### 注册步骤
1. **访问官网**: https://open.feishu.cn/
2. **注册账号**: 使用企业邮箱注册
3. **创建应用**: 进入开发者后台创建应用
4. **认证企业**: 完成企业认证 (可选但推荐)

#### 应用类型选择
- **企业内部应用**: 仅限企业内部使用
- **企业自建应用**: 可发布到应用市场
- **第三方应用**: 面向所有飞书用户

### 4.2 应用创建与配置

#### 创建应用
1. **基本信息**
   - 应用名称: "AI智能助手"
   - 应用描述: "基于DeepseekChat的智能对话助手"
   - 应用图标: 上传合适的图标
   - 应用类别: 工具/效率

2. **权限配置**
   - 获取用户基本信息
   - 发送消息权限
   - 接收消息权限
   - 上传文件权限 (如果需要)

3. **安全设置**
   - IP白名单: 添加你的服务器IP
   - 重定向URL: 配置OAuth回调地址
   - 事件订阅: 启用消息接收

#### 获取关键凭证
```bash
# 飞书应用凭证
APP_ID = "cli_xxxxxxxxxxxxxx"      # 应用ID
APP_SECRET = "xxxxxxxxxxxxxxxx"    # 应用密钥
VERIFICATION_TOKEN = "xxxxxxxx"    # 验证令牌
ENCRYPT_KEY = "xxxxxxxx"           # 加密密钥 (可选)
```

### 4.3 权限申请与审核

#### 必要权限列表
1. **contact:user.id:readonly** - 读取用户ID
2. **im:message** - 发送和接收消息
3. **im:message.group_at_msg:readonly** - 读取@消息
4. **im:message.p2p_msg:readonly** - 读取私聊消息

#### 权限申请流程
1. 在应用后台选择所需权限
2. 提交审核申请
3. 等待飞书审核 (通常1-3个工作日)
4. 审核通过后生效

### 4.4 Webhook配置

#### 事件订阅配置
```python
# webhook_config.py
WEBHOOK_CONFIG = {
    "url": "https://your-domain.com/feishu/webhook",
    "events": [
        "im.message.receive_v1",      # 接收消息
        "im.message.message_read_v1", # 消息已读
        "contact.user.created_v3",    # 用户创建
    ]
}
```

#### Webhook服务器实现
```python
# webhook_server.py
from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import json
import time

app = FastAPI()

# 飞书Webhook验证
@app.post("/feishu/webhook")
async def feishu_webhook(request: Request):
    # 获取请求头
    headers = request.headers
    timestamp = headers.get("X-Lark-Request-Timestamp", "")
    nonce = headers.get("X-Lark-Request-Nonce", "")
    signature = headers.get("X-Lark-Signature", "")
    
    # 获取请求体
    body = await request.body()
    
    # 验证签名
    if not verify_signature(timestamp, nonce, body, signature):
        raise HTTPException(status_code=403, detail="签名验证失败")
    
    # 处理事件
    event_data = json.loads(body)
    event_type = event_data.get("header", {}).get("event_type", "")
    
    if event_type == "im.message.receive_v1":
        await handle_message_event(event_data)
    elif event_type == "url_verification":
        # 飞书验证请求
        return {"challenge": event_data.get("challenge", "")}
    
    return {"code": 0, "msg": "success"}

def verify_signature(timestamp, nonce, body, signature):
    """验证飞书Webhook签名"""
    app_secret = os.getenv("FEISHU_APP_SECRET", "")
    string_to_sign = f"{timestamp}\n{nonce}\n{body.decode()}\n"
    
    h = hmac.new(
        app_secret.encode('utf-8'),
        string_to_sign.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    
    return h.hexdigest() == signature

async def handle_message_event(event_data):
    """处理消息事件"""
    event = event_data.get("event", {})
    message = event.get("message", {})
    sender = event.get("sender", {})
    
    # 提取消息内容
    message_id = message.get("message_id", "")
    chat_type = message.get("chat_type", "")
    content = json.loads(message.get("content", "{}"))
    text = content.get("text", "")
    
    # 处理消息逻辑
    await process_message(message_id, chat_type, sender, text)
```

---

## 第五部分：系统集成与对接

### 5.1 消息路由设计

#### 架构设计
```
飞书消息 → Webhook服务器 → 消息队列 → 消息处理器 → Deepseek API → 响应返回
```

#### 消息处理流程
```python
# message_router.py
class MessageRouter:
    def __init__(self):
        self.processors = {}
        
    def register_processor(self, message_type, processor):
        """注册消息处理器"""
        self.processors[message_type] = processor
    
    async def route_message(self, message):
        """路由消息到对应处理器"""
        message_type = self._determine_message_type(message)
        
        if message_type in self.processors:
            processor = self.processors[message_type]
            return await processor.process(message)
        else:
            return await self._default_processor.process(message)
    
    def _determine_message_type(self, message):
        """确定消息类型"""
        content = message.get("content", {})
        
        if "text" in content:
            return "text"
        elif "image" in content:
            return "image"
        elif "file" in content:
            return "file"
        else:
            return "unknown"
```

### 5.2 API接口开发

#### 核心API接口
```python
# api_endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/api/v1", tags=["AI Chat"])

# 数据模型
class ChatMessage(BaseModel):
    role: str  # "user" 或 "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: Optional[int] = 2000

class ChatResponse(BaseModel):
    id: str
    message: ChatMessage
    usage: dict
    created: int

@router.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """聊天补全接口"""
    try:
        # 调用Deepseek服务
        response = await deepseek_client.chat_completion(
            messages=request.messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            id=response.id,
            message=ChatMessage(
                role="assistant",
                content=response.choices[0].message.content
            ),
            usage=response.usage,
            created=int(time.time())
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def list_models():
    """列出可用模型"""
    return {
        "models": [
            {
                "id": "deepseek-chat",
                "name": "Deepseek Chat",
                "description": "深度求索聊天模型",
                "max_tokens": 128000
            }
        ]
    }
```

#### 飞书消息适配器
```python
# feishu_adapter.py
class FeishuMessageAdapter:
    """飞书消息适配器"""
    
    @staticmethod
    def to_chat_message(feishu_message):
        """将飞书消息转换为Chat格式"""
        content = json.loads(feishu_message.get("content", "{}"))
        text = content.get("text", "").strip()
        
        # 移除@机器人的标记
        text = text.replace("@AI智能助手", "").strip()
        
        return {
            "role": "user",
            "content": text
        }
    
    @staticmethod
    def to_feishu_message(chat_response):
        """将Chat响应转换为飞书消息格式"""
        return {
            "msg_type": "text",
            "content": json.dumps({
                "text": chat_response.message.content
            })
        }
```

### 5.3 安全认证机制

#### API密钥管理
```python
# auth_manager.py
import secrets
from datetime import datetime, timedelta
import redis

class AuthManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
    
    def generate_api_key(self, user_id, expires_days=30):
        """生成API密钥"""
        api_key = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=expires_days)
        
        # 存储到Redis
        key_data = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_active": True
        }
        
        self.redis_client.hset(f"api_key:{api_key}", mapping=key_data)
        self.redis_client.expire(f"api_key:{api_key}", expires_days * 86400)
        
        return api_key
    
    def validate_api_key(self, api_key):
        """验证API密钥"""
        key_data = self.redis_client.hgetall(f"api_key:{api_key}")
        
        if not key_data:
            return False
        
        if key_data.get("is_active") != "True":
            return False
        
        expires_at = datetime.fromisoformat(key_data["expires_at"])
        if datetime.now() > expires_at:
            return False
        
        return True
```

#### 飞书身份验证
```python
# feishu_auth.py
import httpx
from typing import Optional

class FeishuAuth:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[datetime] = None
    
    async def get_access_token(self) -> str:
        """获取飞书访问令牌"""
        if self.access_token and self.token_expires_at:
            if datetime.now() < self.token_expires_at:
                return self.access_token
        
        # 请求新令牌
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/",
                json={
                    "app_id": self.app_id,
                    "app_secret": self.app_secret
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("tenant_access_token")
                expires_in = data.get("expire", 7200)
                self.token_expires_at = datetime.now() + timedelta(seconds=expires_in - 300)  # 提前5分钟过期
                return self.access_token
            else:
                raise Exception(f"获取访问令牌失败: {response.text}")
```

### 5.4 错误处理与日志

#### 统一错误处理
```python
# error_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    error_id = secrets.token_hex(8)
    
    # 记录错误日志
    logger.error(
        f"Error ID: {error_id}, "
        f"Path: {request.url.path}, "
        f"Method: {request.method}, "
        f"Error: {str(exc)}",
        exc_info=True
    )
    
    # 返回用户友好的错误信息
    return JSONResponse(
        status_code=500,
        content={
            "error_id": error_id,
            "message": "服务器内部错误",
            "detail": str(exc) if os.getenv("DEBUG") == "True" else None,
            "timestamp": datetime.now().isoformat()
        }
    )
```

#### 结构化日志
```python
# logging_config.py
import logging
import json
from pythonjsonlogger import jsonlogger

def setup_logging():
    """配置结构化日志"""
    
    # 创建JSON格式的日志处理器
    log_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    log_handler.setFormatter(formatter)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.addHandler(log_handler)
    root_logger.setLevel(logging.INFO)
    
    # 特定模块的日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
```

---

## 第六部分：部署与运维

### 6.1 系统部署步骤

#### 一键部署脚本
```bash
#!/bin/bash
# deploy.sh

set -e  # 遇到错误立即退出

echo "开始部署 Mac mini + 飞书 + Deepseek Chat 系统..."

# 1. 检查环境
echo "检查系统环境..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装"
    exit 1
fi

# 2. 创建目录结构
echo "创建目录结构..."
mkdir -p {config,logs,data,models,ssl}

# 3. 配置环境变量
echo "配置环境变量..."
if [ ! -f .env ]; then
    cat > .env << EOF
# 飞书配置
FEISHU_APP_ID=你的应用ID
FEISHU_APP_SECRET=你的应用密钥
FEISHU_VERIFICATION_TOKEN=你的验证令牌

# Deepseek配置
DEEPSEEK_API_KEY=你的Deepseek API密钥
DEEPSEEK_MODEL=deepseek-chat

# 服务器配置
SERVER_HOST=0.0.0.0
SERVER_PORT=8080
DEBUG=False

# 数据库配置 (可选)
REDIS_URL=redis://redis:6379/0
POSTGRES_URL=postgresql://user:password@postgres:5432/ai_chat
EOF
    echo "请编辑 .env 文件配置必要的参数"
    exit 1
fi

# 4. 启动服务
echo "启动Docker服务..."
docker-compose up -d

# 5. 等待服务就绪
echo "等待服务启动..."
sleep 10

# 6. 健康检查
echo "执行健康检查..."
curl -f http://localhost:8080/health || {
    echo "健康检查失败"
    docker-compose logs
    exit 1
}

echo "部署完成！"
echo "访问地址: http://localhost:8080"
echo "API文档: http://localhost:8080/docs"
```

#### Docker Compose配置
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  # Redis缓存
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - ./data/redis:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    networks:
      - ai-network

  # PostgreSQL数据库 (可选)
  postgres:
    image: postgres:15-alpine
    container_name: postgres-db
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: ai_user
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ai_chat
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    networks:
      - ai-network

  # Deepseek Chat服务
  deepseek-chat:
    image: deepseek/deepseek-chat:latest
    container_name: deepseek-chat
    ports:
      - "8000:8000"
    volumes:
      - ./models:/models
      - ./config/deepseek:/config
    environment:
      - MODEL_PATH=/models/deepseek-chat
      - DEVICE=cpu
      - QUANTIZATION=int8
    deploy:
      resources:
        limits:
          memory: 8G
        reservations:
          memory: 4G
    restart: unless-stopped
    networks:
      - ai-network

  # API服务
  api-service:
    build:
      context: .
      dockerfile: Dockerfile.api
    container_name: api-service
    ports:
      - "8080:8080"
    environment:
      - FEISHU_APP_ID=${FEISHU_APP_ID}
      - FEISHU_APP_SECRET=${FEISHU_APP_SECRET}
      - DEEPSEEK_API_BASE=http://deepseek-chat:8000
      - REDIS_URL=${REDIS_URL}
    depends_on:
      - redis
      - deepseek-chat
    restart: unless-stopped
    networks:
      - ai-network

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/conf.d:/etc/nginx/conf.d
      - ./ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - api-service
    restart: unless-stopped
    networks:
      - ai-network

  # 监控服务 (可选)
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      -