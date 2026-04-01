# DuckDuckGo 搜索技能配置

## 概述
使用DuckDuckGo进行网页搜索，无需API Key，立即可用。

## 使用方法

### 直接搜索
```
搜索 "OpenClaw 最新版本"
查找 "Python 教程"
搜索今天的AI新闻
```

### 高级搜索
```
搜索 site:github.com OpenClaw
搜索 filetype:pdf Python指南
```

## 技术实现

### 使用 ddgr 命令行工具
```bash
# 安装 ddgr
brew install ddgr

# 基本搜索
ddgr "搜索关键词"

# 限制结果数量
ddgr -n 5 "搜索关键词"

# JSON输出
ddgr -j "搜索关键词"
```

### 使用 Python 脚本
```python
from duckduckgo_search import DDGS

with DDGS() as ddgs:
    results = ddgs.text("搜索关键词", max_results=5)
    for r in results:
        print(f"{r['title']}\n{r['href']}\n{r['body']}\n")
```

## 配置说明

### 环境要求
- Python 3.8+
- 网络连接（无需代理）

### 安装依赖
```bash
pip install duckduckgo-search
```

## 使用示例

### 示例1: 搜索新闻
```
用户: 搜索今天的科技新闻
助手: 使用DuckDuckGo搜索"today tech news"...
```

### 示例2: 查找教程
```
用户: 找Docker入门教程
助手: 使用DuckDuckGo搜索"Docker tutorial beginner"...
```

### 示例3: 竞品分析
```
用户: 搜索OpenClaw的竞品
助手: 使用DuckDuckGo搜索"OpenClaw alternatives AI agent"...
```

## 限制说明

1. **速率限制**: DuckDuckGo有隐含的速率限制，频繁请求可能需要等待
2. **结果数量**: 每次搜索最多返回约30条结果
3. **地区限制**: 某些地区可能需要使用代理

## 替代方案

如果需要更稳定的搜索，可以考虑：
1. **Brave Search API** - 需要API Key，但结果更稳定
2. **SerpAPI** - 支持Google搜索，需要付费
3. **Bing Search API** - 微软提供，每月有免费额度

## 更新日志

- 2026-03-07: 初始配置，使用DuckDuckGo作为默认搜索引擎
