# 搜索技能启用配置
# 创建时间: 2026-03-14 03:26
# 状态: 已启用

## 启用的搜索技能（3个）

### 1. Tavily Search (AI搜索)
- **状态**: ✅ 已启用并配置
- **版本**: 已安装
- **API Key**: 已配置 (tvly-dev-...)
- **优势**: AI摘要、相关度评分、深度搜索
- **使用**: `bash skills/tavily-search/search.sh "关键词"`
- **推荐场景**: 深度研究、新闻监控、高质量结果

### 2. Multi Search Engine (多搜索引擎)
- **状态**: ✅ 已启用
- **版本**: 2.0.1
- **引擎数量**: 17个（8个国内 + 9个国际）
- **优势**: 无需API Key、多引擎对比、隐私保护
- **使用**: 通过web_fetch访问各搜索引擎URL
- **推荐场景**: 快速查询、多源对比、隐私搜索

### 3. DuckDuckGo Search (隐私搜索)
- **状态**: ✅ 已启用
- **版本**: 已安装
- **优势**: 无需API Key、隐私保护、快速
- **使用**: `python3 skills/duckduckgo-search/duckduckgo_search.py "关键词"`
- **推荐场景**: 简单查询、隐私保护、快速搜索

---

## 使用策略

| 场景 | 推荐技能 | 原因 |
|------|---------|------|
| 深度研究 | Tavily | AI摘要、相关度评分 |
| 新闻监控 | Tavily | 高质量、实时 |
| 快速查询 | DuckDuckGo | 无需API、快速 |
| 多源对比 | Multi Search | 17个引擎 |
| 隐私保护 | DuckDuckGo/Multi | 不追踪 |
| 国内搜索 | Multi Search | 百度、搜狗等 |
| 国际搜索 | Multi Search | Google、Bing等 |

---

## 快速使用示例

### Tavily 搜索
```bash
# 基础搜索
bash skills/tavily-search/search.sh "AI最新进展"

# 深度搜索
bash skills/tavily-search/search.sh "量子计算" advanced 10
```

### Multi Search Engine
```bash
# 通过web_fetch使用各引擎
web_fetch "https://www.google.com/search?q=python+tutorial"
web_fetch "https://duckduckgo.com/html/?q=privacy+tools"
web_fetch "https://www.baidu.com/s?wd=人工智能"
```

### DuckDuckGo
```bash
# 使用本地脚本
python3 skills/duckduckgo-search/duckduckgo_search.py "Docker教程"
```

---

## 配置状态

- ✅ Tavily: API Key 已配置
- ✅ Multi Search: 无需配置
- ✅ DuckDuckGo: 脚本可用
- ⏳ Brave API Key: 可选配置（更稳定）

---

*启用时间: 2026-03-14*
*Proactive Agent 自动启用*
