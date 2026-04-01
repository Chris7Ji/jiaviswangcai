# 🔍 Tavily AI搜索技能

## 概述
高质量AI搜索引擎，支持深度搜索和智能摘要。比传统搜索更智能，能生成AI摘要和相关度评分。

## 状态
✅ **已配置并正常工作**

## 功能特性

### ✅ 已实现功能
- AI智能搜索
- 自动生成答案摘要
- 相关度评分
- 支持中英文搜索
- 深度搜索模式（advanced）
- 结果保存为JSON

### 📝 使用方法

#### 基础搜索
```bash
bash skills/tavily-search/search.sh "搜索关键词"
```

#### 深度搜索
```bash
bash skills/tavily-search/search.sh "搜索关键词" advanced 10
```

#### 参数说明
- 参数1: 搜索关键词（必需）
- 参数2: 搜索深度（可选，basic/advanced，默认basic）
- 参数3: 结果数量（可选，默认10）

### 💬 自然语言指令

可以直接对我说：
- "搜索今天的AI新闻"
- "查找OpenClaw的最新信息"
- "深度搜索量子计算进展"

## 配置说明

### API配置（已配置）
- **API Key**: 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
- **虚拟环境**: venv_tavily
- **Python包**: tavily-python

### 虚拟环境位置
```
/Users/jiyingguo/.openclaw/workspace/venv_tavily
```

## 使用示例

### 示例1: 搜索AI新闻
```bash
bash skills/tavily-search/search.sh "AI人工智能最新新闻" basic 5
```

输出：
```
🤖 AI摘要:
AI advancements include new models like GPT-5.4 and Gemini 3 Deep Think...

📊 找到 5 条结果:
1. AI人工智能-每日最新AI新闻&文章聚合 (相关度: 0.86)
   URL: https://www.ainav.cn/news/
   ...
```

### 示例2: 深度搜索
```bash
bash skills/tavily-search/search.sh "OpenClaw AI agent" advanced 10
```

## 与其他搜索对比

| 特性 | Tavily | DuckDuckGo | Brave Search |
|------|--------|------------|--------------|
| AI摘要 | ✅ | ❌ | ❌ |
| 相关度评分 | ✅ | ❌ | ❌ |
| 深度搜索 | ✅ | ❌ | ❌ |
| 需要API Key | ✅ | ❌ | ✅ |
| 中文支持 | ✅ | ✅ | ✅ |

## 使用建议

1. **日常搜索**: 使用Tavily获得AI摘要和相关度评分
2. **快速搜索**: 使用DuckDuckGo（无需API Key）
3. **备用方案**: 配置Brave Search API Key作为备用

## 更新日志

- 2026-03-07: 确认Tavily搜索功能正常工作，创建便捷脚本
