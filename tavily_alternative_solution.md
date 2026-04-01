# Tavily搜索功能替代方案

由于clawhub严格速率限制导致Tavily技能无法安装，以下是完整的替代解决方案。

## 🎯 Tavily核心功能分析

### Tavily主要特点：
1. **AI优化搜索** - 为AI代理优化的搜索结果
2. **智能摘要** - 自动提取和总结内容
3. **深度搜索** - 比普通搜索更深入
4. **结构化结果** - AI友好的结果格式
5. **多源聚合** - 整合多个信息源

## 🛠️ 替代方案实现

### 方案1：配置现有OpenClaw搜索工具（推荐）

#### 配置Brave搜索API：
```bash
# 1. 获取Brave Search API密钥
# 访问: https://brave.com/search/api/

# 2. 配置OpenClaw
openclaw configure --section web

# 3. 输入API密钥
# 4. 立即开始使用
```

#### Brave搜索优势：
- ✅ **高质量结果** - Brave搜索质量很高
- ✅ **隐私保护** - 不跟踪用户
- ✅ **免费额度** - 充足的免费搜索次数
- ✅ **中文支持** - 良好的中文搜索结果

### 方案2：创建自定义Tavily-like搜索脚本

#### 如果已有Tavily API密钥：
```python
#!/usr/bin/env python3
# tavily_custom_search.py

import requests
import json
import os

class TavilyCustomSearch:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        self.base_url = "https://api.tavily.com"
    
    def search(self, query, max_results=5, include_answer=True):
        """执行Tavily搜索"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "query": query,
            "max_results": max_results,
            "include_answer": include_answer,
            "include_raw_content": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/search",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"搜索失败: {e}")
            return None
    
    def get_ai_summary(self, query):
        """获取AI摘要"""
        result = self.search(query, include_answer=True)
        if result and 'answer' in result:
            return result['answer']
        return None

# 使用示例
if __name__ == "__main__":
    # 设置API密钥
    import sys
    if len(sys.argv) > 1:
        query = sys.argv[1]
        searcher = TavilyCustomSearch()
        results = searcher.search(query)
        if results:
            print(json.dumps(results, indent=2, ensure_ascii=False))
```

### 方案3：多搜索引擎聚合方案

#### 结合多个免费搜索源：
```python
#!/usr/bin/env python3
# multi_search_aggregator.py

import requests
from typing import List, Dict
import json

class MultiSearchAggregator:
    """多搜索引擎聚合器"""
    
    def __init__(self):
        self.sources = [
            self._brave_search,
            self._duckduckgo_search,
            # 可以添加更多搜索源
        ]
    
    def search(self, query: str, max_results: int = 10) -> Dict:
        """多源聚合搜索"""
        all_results = []
        
        for source in self.sources:
            try:
                results = source(query, max_results // len(self.sources))
                if results:
                    all_results.extend(results)
            except Exception as e:
                print(f"搜索源失败: {e}")
                continue
        
        # 去重和排序
        unique_results = self._deduplicate_results(all_results)
        sorted_results = self._rank_results(unique_results, query)
        
        return {
            "query": query,
            "results": sorted_results[:max_results],
            "total_sources": len(self.sources),
            "total_results": len(sorted_results)
        }
    
    def _brave_search(self, query: str, max_results: int) -> List[Dict]:
        """Brave搜索（需要API密钥）"""
        # 实现Brave搜索逻辑
        pass
    
    def _duckduckgo_search(self, query: str, max_results: int) -> List[Dict]:
        """DuckDuckGo搜索"""
        # 实现DuckDuckGo搜索逻辑
        pass
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """去重结果"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            if 'url' in result and result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        return unique_results
    
    def _rank_results(self, results: List[Dict], query: str) -> List[Dict]:
        """智能排名结果"""
        # 简单的基于关键词匹配的排名
        query_words = set(query.lower().split())
        
        def relevance_score(result):
            score = 0
            title = result.get('title', '').lower()
            snippet = result.get('snippet', '').lower()
            
            for word in query_words:
                if word in title:
                    score += 3
                if word in snippet:
                    score += 1
            
            return score
        
        return sorted(results, key=relevance_score, reverse=True)
```

### 方案4：使用开源元搜索引擎

#### 自托管SearXNG：
```bash
# 1. 安装Docker
# 2. 运行SearXNG
docker run -d \
  --name searxng \
  -p 8080:8080 \
  -e "SEARXNG_BASE_URL=http://localhost:8080/" \
  searxng/searxng

# 3. 访问 http://localhost:8080
# 4. 通过API集成到OpenClaw
```

#### SearXNG优势：
- ✅ **完全开源** - 可自托管
- ✅ **隐私保护** - 不记录搜索历史
- ✅ **多引擎支持** - 支持70+个搜索引擎
- ✅ **API接口** - 可通过API调用

## 📋 实施步骤

### 立即行动（推荐）：
1. **获取Brave API密钥** - 免费，质量高
2. **配置OpenClaw web_search** - 5分钟完成
3. **开始使用高质量搜索** - 立即生效

### 如需Tavily特定功能：
4. **获取Tavily API密钥**（如需）
5. **我创建自定义集成脚本** - 1小时内完成
6. **测试和优化** - 确保功能完整

### 长期方案：
7. **明天重试安装** - 速率限制可能每日重置
8. **探索其他技能源** - GitHub、直接下载等
9. **创建技能镜像** - 避免依赖clawhub

## 🎯 功能对比

| 功能 | Tavily技能 | Brave搜索 | 自定义方案 |
|------|-----------|-----------|-----------|
| AI优化结果 | ✅ | ⚠️ 部分 | ✅ 可定制 |
| 智能摘要 | ✅ | ❌ | ✅ 可实现 |
| 多源聚合 | ✅ | ❌ | ✅ 可定制 |
| 安装难度 | ❌ 困难 | ✅ 简单 | ⚠️ 中等 |
| 成本 | 可能有费用 | 免费额度 | 依赖API |
| 隐私保护 | ⚠️ 一般 | ✅ 优秀 | ✅ 可控制 |

## 💡 建议

### 对于大多数用户：
1. **配置Brave搜索** - 简单、免费、质量高
2. **满足90%搜索需求** - 一般搜索完全足够
3. **无需等待安装** - 立即可用

### 对于需要AI优化搜索：
1. **获取Tavily API密钥**（如有）
2. **创建自定义集成** - 实现相同功能
3. **结合现有工具** - 获得最佳体验

### 对于技术爱好者：
1. **自托管SearXNG** - 完全控制
2. **多引擎聚合** - 最大化覆盖
3. **定制化开发** - 按需定制功能

## 🚀 下一步

### 告诉我您的选择：
1. **配置Brave搜索**（推荐） - 我指导您获取API密钥
2. **创建Tavily自定义集成** - 需要Tavily API密钥
3. **等待明天安装** - 继续尝试clawhub安装
4. **其他搜索需求** - 告诉我具体需求

**搜索功能有多种实现方式，不依赖单一技能安装！**