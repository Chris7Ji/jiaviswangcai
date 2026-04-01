# 🌐 OpenClaw 网络搜索功能设置指南

## 📋 当前状态分析

### ✅ 已配置的功能
1. **模型配置**: DeepSeek、MiniMax、Moonshot/Kimi
2. **飞书集成**: 已配置并启用
3. **网关服务**: 本地运行 (ws://127.0.0.1:18789)
4. **技能系统**: 52个技能已安装

### ❌ 缺失的功能
1. **网络搜索API密钥**: Brave Search API 未配置
2. **网页抓取配置**: 可能需要额外设置

## 🎯 网络搜索功能概述

OpenClaw 提供两种网络搜索工具：

### 1. **web_search** - Brave搜索API
- 使用Brave Search API进行网络搜索
- 返回标题、URL和摘要
- 支持区域和语言过滤
- 需要API密钥

### 2. **web_fetch** - 网页内容抓取
- 抓取网页内容并转换为Markdown/文本
- 无需API密钥（但有安全限制）
- 适合获取特定网页内容

## 🔑 获取API密钥

### 步骤1: 获取Brave Search API密钥

#### 方法A: 注册Brave Search API
1. 访问: https://brave.com/search/api/
2. 点击 "Get Started" 或 "Sign Up"
3. 创建账户（可能需要验证邮箱）
4. 在控制台获取API密钥

#### 方法B: 使用现有服务（如果已有）
- Perplexity API
- SerpAPI
- Google Custom Search API

### 步骤2: 备用方案
如果无法获取Brave API密钥，可以考虑：
1. **使用web_fetch工具**: 直接抓取特定网页
2. **配置其他搜索提供商**: 如DuckDuckGo、Google等
3. **使用本地搜索技能**: 如已有的summarize技能

## ⚙️ 配置方法

### 方法1: 使用命令行配置（推荐）

```bash
# 启动web配置向导
openclaw configure --section web

# 或者直接设置环境变量
export BRAVE_API_KEY="your_api_key_here"

# 永久保存到配置文件
openclaw configure --section web << EOF
your_api_key_here
EOF
```

### 方法2: 手动编辑配置文件

编辑 `/Users/jiyingguo/.openclaw/openclaw.json`，添加web配置：

```json
{
  "web": {
    "brave": {
      "apiKey": "your_brave_api_key_here"
    },
    "fetch": {
      "timeout": 30000,
      "maxRedirects": 5,
      "userAgent": "OpenClaw/2026.2.26"
    }
  }
}
```

### 方法3: 环境变量配置

在shell配置文件中添加（如 `~/.zshrc` 或 `~/.bashrc`）：

```bash
# Brave Search API
export BRAVE_API_KEY="your_api_key_here"

# 其他可选配置
export WEB_SEARCH_COUNTRY="CN"
export WEB_SEARCH_LANGUAGE="zh"
export WEB_FETCH_TIMEOUT="30000"
```

## 🔧 测试配置

### 测试1: 检查当前配置
```bash
# 检查环境变量
echo $BRAVE_API_KEY

# 检查OpenClaw配置
openclaw status | grep -i web
```

### 测试2: 简单搜索测试
```bash
# 如果配置成功，可以测试搜索
# 注意：需要在OpenClaw会话中执行
```

### 测试3: 验证工具可用性
```bash
# 检查web_search工具状态
# 在OpenClaw会话中尝试：
# web_search query="test search"
```

## 🛠️ 故障排除

### 常见问题1: "missing_brave_api_key"
**症状**:
```
Error: missing_brave_api_key
web_search needs a Brave Search API key.
```

**解决方案**:
1. 确认已设置API密钥
2. 重启OpenClaw网关服务
3. 检查密钥格式是否正确

```bash
# 重启网关
openclaw gateway restart

# 验证配置
openclaw configure --section web
```

### 常见问题2: 网络连接失败
**症状**:
- 搜索超时
- 无法连接到API

**解决方案**:
1. 检查网络连接
2. 增加超时时间
3. 使用代理（如果需要）

```bash
# 测试网络连接
curl -I https://api.search.brave.com

# 配置代理（如果需要）
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### 常见问题3: 速率限制
**症状**:
- "Rate limit exceeded"
- 搜索次数受限

**解决方案**:
1. 等待限制解除
2. 升级API套餐
3. 减少搜索频率

## 🌐 替代搜索方案

### 方案A: 使用web_fetch工具
```bash
# 直接抓取网页内容
web_fetch url="https://example.com"

# 转换为Markdown
web_fetch url="https://example.com" extractMode="markdown"
```

### 方案B: 使用已有技能
```bash
# 使用summarize技能（如果已安装）
summarize https://example.com

# 使用其他信息获取技能
# 如天气、新闻等专用技能
```

### 方案C: 浏览器自动化
```bash
# 使用browser工具（需要Chrome扩展）
browser action="open" targetUrl="https://google.com"
browser action="snapshot"
```

## 📊 配置验证脚本

创建测试脚本 `/Users/jiyingguo/.openclaw/workspace/test_web_config.sh`:

```bash
#!/bin/bash
echo "=== OpenClaw Web配置测试 ==="

# 检查环境变量
echo "1. 检查环境变量:"
echo "   BRAVE_API_KEY: ${BRAVE_API_KEY:0:10}..."  # 显示前10个字符

# 检查OpenClaw状态
echo "2. 检查OpenClaw状态:"
openclaw gateway status

# 测试网络连接
echo "3. 测试网络连接:"
curl -s --max-time 5 https://api.search.brave.com/health | head -1

echo "=== 测试完成 ==="
```

## 🔄 配置更新流程

### 日常维护
1. **定期检查API密钥有效期**
2. **监控使用量和费用**
3. **备份配置文件**

### 密钥轮换
```bash
# 1. 获取新密钥
# 2. 更新配置
openclaw configure --section web

# 3. 重启服务
openclaw gateway restart

# 4. 验证新密钥
# （执行测试搜索）
```

## 🎯 最佳实践

### 安全实践
1. **不要硬编码API密钥**在脚本中
2. **使用环境变量**或配置文件
3. **定期轮换密钥**
4. **限制密钥权限**

### 性能优化
1. **缓存搜索结果**（如果支持）
2. **批量处理搜索请求**
3. **使用合适的超时设置**
4. **监控API使用情况**

### 成本控制
1. **设置使用限制**
2. **监控API调用次数**
3. **使用免费套餐（如果可用）**
4. **考虑替代方案**

## 📞 支持资源

### 官方文档
- OpenClaw Web工具文档: https://docs.openclaw.ai/tools/web
- Brave Search API文档: https://brave.com/search/api/

### 社区支持
- OpenClaw Discord: https://discord.com/invite/clawd
- GitHub Issues: https://github.com/openclaw/openclaw/issues

### 故障诊断
```bash
# 查看详细日志
openclaw gateway logs

# 重置配置
openclaw configure --reset web

# 寻求帮助（提供以下信息）:
# 1. OpenClaw版本: openclaw --version
# 2. 错误信息
# 3. 配置摘要
```

## 🚀 快速开始清单

### 今日任务
- [ ] 获取Brave Search API密钥
- [ ] 配置API密钥到OpenClaw
- [ ] 测试web_search功能
- [ ] 创建备份配置

### 本周任务
- [ ] 探索web_fetch工具
- [ ] 设置搜索缓存（如果支持）
- [ ] 创建常用搜索模板
- [ ] 集成到工作流中

### 长期目标
- [ ] 建立完整的网络研究流程
- [ ] 开发自定义搜索技能
- [ ] 优化搜索性能和成本
- [ ] 创建搜索知识库

---

**下一步行动**: 
1. 访问 https://brave.com/search/api/ 获取API密钥
2. 运行 `openclaw configure --section web` 进行配置
3. 测试搜索功能: `web_search query="OpenClaw skills"`

需要我帮你执行任何配置步骤，或者有其他问题吗？