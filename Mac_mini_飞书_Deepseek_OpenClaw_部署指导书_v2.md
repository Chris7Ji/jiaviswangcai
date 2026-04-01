# Mac mini + 飞书 + Deepseek + OpenClaw 部署指导书（简化版）

**版本**: v2.0  
**更新日期**: 2026年3月5日  
**部署方式**: Deepseek API + OpenClaw官方命令行  

---

## 目录

1. [方案概述](#一方案概述)
2. [系统架构](#二系统架构)
3. [环境准备](#三环境准备)
4. [OpenClaw一键安装](#四openclaw一键安装)
5. [Deepseek API配置](#五deepseek-api配置)
6. [飞书机器人配置（图文）](#六飞书机器人配置图文)
7. [系统对接](#七系统对接)
8. [启动与测试](#八启动与测试)
9. [故障排除](#九故障排除)

---

## 一、方案概述

### 1.1 新方案特点

| 特性 | 原方案 | 新方案 |
|------|--------|--------|
| AI模型 | Ollama本地部署 | Deepseek官方API |
| 安装方式 | 多步骤手动安装 | OpenClaw一键命令行 |
| 开发框架 | Python + FastAPI | OpenClaw内置 |
| 部署方式 | Docker容器化 | 直接机器部署 |
| 适用系统 | 仅Mac | Mac/Windows/Linux |

### 1.2 优势
- **更简单**: 一条命令完成安装
- **更快速**: 无需下载大模型，直接调用API
- **更轻量**: 无需Docker，直接运行
- **跨平台**: 支持Mac/Windows/Linux

---

## 二、系统架构

```
┌─────────────────┐
│   用户（飞书）   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  飞书开放平台    │
│  （Webhook）    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    OpenClaw     │
│  （消息处理）   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deepseek API   │
│ （官方云服务）  │
└─────────────────┘
```

---

## 三、环境准备

### 3.1 硬件要求

**最低配置**:
- 设备: Mac mini / Windows PC / Linux服务器
- 内存: 8GB+
- 存储: 10GB可用空间
- 网络: 稳定的互联网连接

**推荐配置**:
- 内存: 16GB+
- 网络: 100Mbps宽带

### 3.2 系统要求

| 操作系统 | 版本要求 |
|---------|---------|
| macOS | 12.0 (Monterey) 或更高 |
| Windows | Windows 10/11 |
| Linux | Ubuntu 20.04+ / CentOS 8+ |

---

## 四、OpenClaw一键安装

### 4.1 Mac系统安装

**步骤1**: 打开终端（Terminal）
- 按 `Command + 空格`，输入"终端"，回车

**步骤2**: 运行安装命令

```bash
# 安装OpenClaw（官方推荐方式）
curl -fsSL https://openclaw.ai/install.sh | bash

# 或使用Homebrew
brew install openclaw
```

**步骤3**: 验证安装

```bash
openclaw --version
```

预期输出：
```
OpenClaw 2026.3.2
```

**步骤4**: 初始化配置

```bash
openclaw init
```

按照提示完成初始化设置。

---

### 4.2 Windows系统安装

**步骤1**: 打开PowerShell（管理员权限）
- 按 `Win + X`，选择"Windows PowerShell（管理员）"

**步骤2**: 运行安装命令

```powershell
# 安装OpenClaw
irm https://openclaw.ai/install.ps1 | iex

# 或使用winget
winget install OpenClaw.OpenClaw
```

**步骤3**: 验证安装

```powershell
openclaw --version
```

**步骤4**: 初始化配置

```powershell
openclaw init
```

---

### 4.3 Linux系统安装

**Ubuntu/Debian**:

```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y curl

# 安装OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 验证
openclaw --version

# 初始化
openclaw init
```

**CentOS/RHEL**:

```bash
# 安装依赖
sudo yum install -y curl

# 安装OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 验证
openclaw --version

# 初始化
openclaw init
```

---

## 五、Deepseek API配置

### 5.1 获取API Key

**步骤1**: 访问Deepseek官网
- 打开 https://www.deepseek.com/

**步骤2**: 注册/登录账号
- 点击"注册"，使用邮箱或手机号注册
- 或使用已有账号登录

**步骤3**: 获取API Key
1. 登录后进入"开发者中心"
2. 点击"API Keys"
3. 点击"创建新Key"
4. 复制生成的API Key（格式：sk-xxxxxxxx）

⚠️ **重要**: API Key只显示一次，请妥善保存！

### 5.2 配置OpenClaw使用Deepseek

**步骤1**: 配置API Key

```bash
# Mac/Linux
export DEEPSEEK_API_KEY="sk-你的API-Key"

# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-你的API-Key"

# 永久配置（推荐）
# Mac/Linux: 添加到 ~/.bashrc 或 ~/.zshrc
echo 'export DEEPSEEK_API_KEY="sk-你的API-Key"' >> ~/.zshrc
source ~/.zshrc

# Windows: 添加到系统环境变量
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-你的API-Key", "User")
```

**步骤2**: 验证API连接

```bash
openclaw configure --provider deepseek --api-key $DEEPSEEK_API_KEY
```

---

## 六、飞书机器人配置（图文）

### 6.1 创建飞书应用

**步骤1**: 访问飞书开放平台
- 打开 https://open.feishu.cn/

**步骤2**: 登录并进入开发者后台
- 使用企业账号或个人账号登录
- 点击"开发者后台"

【配图1：飞书开放平台首页截图，标注"开发者后台"入口】

**步骤3**: 创建企业自建应用
- 点击"创建企业自建应用"
- 填写应用信息：
  - **应用名称**: AI智能助手
  - **应用描述**: 基于Deepseek的AI助手
  - **应用图标**: 上传图标（可选）

【配图2：创建应用页面截图，标注填写位置】

### 6.2 获取应用凭证

创建完成后，记录以下信息：

```
App ID: cli_xxxxxxxxxxxxxxxx
App Secret: xxxxxxxxxxxxxxxxxxxxxxxx
Verification Token: xxxxxxxxxxxxxxxxxx
```

【配图3：应用凭证页面截图，标注三个关键信息位置】

⚠️ **重要**: App Secret只显示一次，点击"查看"后复制保存！

### 6.3 启用机器人能力

**步骤1**: 进入机器人设置
- 点击左侧菜单"机器人"
- 打开"启用机器人"开关

【配图4：机器人设置页面截图，标注开关位置】

**步骤2**: 配置机器人信息
- 机器人名称：AI助手
- 机器人介绍：智能对话助手
- 上传机器人头像（可选）

### 6.4 配置权限

**步骤1**: 进入权限管理
- 点击左侧"权限管理"
- 点击"申请权限"

【配图5：权限管理页面截图】

**步骤2**: 添加必要权限
搜索并添加以下权限：
- ✅ `im:chat:readonly` - 获取群组信息
- ✅ `im:message` - 发送消息
- ✅ `im:message.group_at_msg` - 接收群@消息
- ✅ `im:message.p2p_msg` - 接收私聊消息
- ✅ `contact:user.id:readonly` - 获取用户ID

【配图6：权限列表截图，标注已勾选的权限】

**步骤3**: 申请权限
- 点击"批量申请"
- 等待审核通过（通常即时通过）

### 6.5 配置事件订阅（Webhook）

**步骤1**: 进入事件订阅
- 点击左侧"事件订阅"

【配图7：事件订阅页面截图】

**步骤2**: 配置请求地址
- 在"请求地址"栏输入：
  ```
  http://你的服务器IP:8080/webhook
  ```
  例如：`http://192.168.1.100:8080/webhook`

【配图8：请求地址配置截图，标注输入框位置】

**步骤3**: 配置订阅事件
- 点击"添加事件"
- 选择：`im.message.receive_v1`（接收消息）

【配图9：事件选择截图，标注选择的事件】

**步骤4**: 保存配置
- 点击"保存"
- 飞书会发送验证请求，确保服务已启动

### 6.6 发布应用

**步骤1**: 创建版本
- 点击左侧"版本管理与发布"
- 点击"创建版本"

【配图10：版本管理页面截图】

**步骤2**: 填写版本信息
- 版本号：1.0.0
- 更新说明：初始版本
- 可用性状态：已启用

【配图11：版本信息填写截图】

**步骤3**: 申请发布
- 点击"申请发布"
- 等待审核（企业应用通常即时通过）

### 6.7 添加机器人到群组

**步骤1**: 进入群组
- 打开飞书，进入目标群组

**步骤2**: 添加机器人
- 点击右上角"设置"（齿轮图标）
- 选择"群机器人"
- 点击"添加机器人"

【配图12：群机器人设置截图】

**步骤3**: 选择机器人
- 找到"AI智能助手"
- 点击"添加"

【配图13：机器人列表截图，标注选择位置】

---

## 七、系统对接

### 7.1 配置OpenClaw连接飞书

**步骤1**: 配置飞书凭证

```bash
# 配置App ID
openclaw configure --key feishu.app_id --value "cli_xxxxxxxxxxxxxxxx"

# 配置App Secret
openclaw configure --key feishu.app_secret --value "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 配置Verification Token
openclaw configure --key feishu.verification_token --value "xxxxxxxxxxxxxxxx"
```

**步骤2**: 验证配置

```bash
openclaw feishu verify
```

### 7.2 配置AI服务

**步骤1**: 配置Deepseek

```bash
# 配置API Key
openclaw configure --key deepseek.api_key --value "sk-xxxxxxxxxxxxxxxx"

# 配置模型（可选，默认deepseek-chat）
openclaw configure --key deepseek.model --value "deepseek-chat"
```

**步骤2**: 测试AI连接

```bash
openclaw ai test --message "你好"
```

预期输出：
```
AI回复: 你好！有什么我可以帮助你的吗？
```

---

## 八、启动与测试

### 8.1 启动服务

**步骤1**: 启动OpenClaw服务

```bash
# 前台启动（调试用）
openclaw start

# 后台启动（生产环境）
openclaw start --daemon

# 指定端口
openclaw start --port 8080
```

**步骤2**: 检查服务状态

```bash
openclaw status
```

预期输出：
```
Service: running
Port: 8080
Uptime: 00:05:32
```

### 8.2 测试完整流程

**步骤1**: 测试Webhook

```bash
curl http://localhost:8080/health
```

预期输出：
```json
{"status": "healthy", "service": "openclaw"}
```

**步骤2**: 在飞书中测试
1. 打开飞书，进入配置了机器人的群组
2. @机器人并发送消息：
   ```
   @AI助手 你好
   ```
3. 等待机器人回复

【配图14：飞书对话截图，展示@机器人和回复】

### 8.3 查看日志

```bash
# 实时查看日志
openclaw logs --follow

# 查看最近100行
openclaw logs --tail 100

# 查看错误日志
openclaw logs --level error
```

---

## 九、故障排除

### 9.1 安装问题

**问题**: OpenClaw安装失败

**解决**:
```bash
# 检查网络连接
ping openclaw.ai

# 使用代理
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://openclaw.ai/install.sh | bash

# 手动下载安装
wget https://openclaw.ai/download/openclaw-latest.tar.gz
tar -xzf openclaw-latest.tar.gz
sudo mv openclaw /usr/local/bin/
```

### 9.2 API连接问题

**问题**: Deepseek API连接失败

**解决**:
```bash
# 检查API Key
openclaw configure --key deepseek.api_key

# 测试网络连接
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer sk-你的API-Key"

# 检查API Key是否有效
openclaw ai test --verbose
```

### 9.3 飞书Webhook问题

**问题**: 飞书无法连接到服务

**解决**:
```bash
# 检查服务是否运行
openclaw status

# 检查端口是否开放
netstat -an | grep 8080

# 检查防火墙
sudo ufw allow 8080  # Ubuntu
sudo firewall-cmd --add-port=8080/tcp  # CentOS

# 查看Webhook日志
openclaw logs --filter webhook
```

### 9.4 机器人无响应

**检查清单**:
- [ ] OpenClaw服务是否运行？`openclaw status`
- [ ] 飞书Webhook地址是否正确？
- [ ] 机器人在群组中吗？
- [ ] API Key是否有效？
- [ ] 查看错误日志：`openclaw logs --level error`

---

## 附录

### A. 常用命令速查

| 命令 | 用途 |
|------|------|
| `openclaw --version` | 查看版本 |
| `openclaw init` | 初始化配置 |
| `openclaw start` | 启动服务 |
| `openclaw stop` | 停止服务 |
| `openclaw status` | 查看状态 |
| `openclaw logs` | 查看日志 |
| `openclaw configure` | 配置参数 |
| `openclaw feishu verify` | 验证飞书配置 |
| `openclaw ai test` | 测试AI连接 |

### B. 配置文件位置

| 系统 | 配置文件路径 |
|------|-------------|
| Mac | `~/.openclaw/config.yaml` |
| Windows | `%USERPROFILE%\.openclaw\config.yaml` |
| Linux | `~/.openclaw/config.yaml` |

### C. 资源链接

- **OpenClaw官网**: https://openclaw.ai
- **OpenClaw文档**: https://docs.openclaw.ai
- **Deepseek官网**: https://www.deepseek.com
- **Deepseek API文档**: https://platform.deepseek.com/docs
- **飞书开放平台**: https://open.feishu.cn

---

**文档结束**

*版本: v2.0*  
*更新日期: 2026年3月5日*  
*作者: Jarvis AI助手*
