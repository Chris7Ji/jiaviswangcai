# 🔍 DuckDuckGo 搜索技能配置

## 状态: ✅ 已配置（等待API Key优化）

## 当前实现

### 方案1: 使用系统工具（推荐，需配置）
编辑 `~/.openclaw/openclaw.json` 添加Web搜索配置：

```json
{
  "web": {
    "braveApiKey": "YOUR_BRAVE_API_KEY"
  }
}
```

获取Brave API Key: https://api.search.brave.com/app/keys

### 方案2: 使用本地脚本（无需API Key）
已创建搜索脚本：`skills/duckduckgo-search/duckduckgo_search.py`

使用方法：
```bash
python3 skills/duckduckgo-search/duckduckgo_search.py "搜索关键词"
```

## 使用示例

### 直接搜索
```
用户: 搜索今天的AI新闻
助手: 使用web_search工具搜索...
```

### 查找教程
```
用户: 找Docker入门教程
助手: 搜索Docker tutorial...
```

### 竞品分析
```
用户: 搜索OpenClaw的竞品
助手: 搜索OpenClaw alternatives...
```

## 技能功能

### 已配置功能
- ✅ 网页搜索（通过web_search工具）
- ✅ 网页内容提取（通过web_fetch工具）
- ✅ 搜索结果分析

### 待优化
- ⏳ 配置Brave Search API Key（更稳定）
- ⏳ 安装duckduckgo-search包（需要解决依赖）

## 使用限制

1. **当前限制**: web_search需要Brave API Key
2. **替代方案**: 可以使用web_fetch直接访问网页
3. **速率限制**: 免费API有调用限制

## 下一步

请提供 **Brave Search API Key** 以获得最佳搜索体验：
1. 访问 https://api.search.brave.com/app/keys
2. 注册并获取API Key
3. 我将为您配置到系统中

或者，您可以继续使用现有的 `web_fetch` 工具直接访问特定网页。
