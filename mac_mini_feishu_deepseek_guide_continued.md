Chat的智能对话助手"
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