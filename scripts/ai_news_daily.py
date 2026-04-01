#!/usr/bin/env python3
"""
AI新闻摘要任务（已存在）
每天早上6:30生成AI新闻摘要
"""
import os
import sys
import json
import urllib.request
from datetime import datetime

def generate_ai_news_summary():
    """生成AI新闻摘要"""
    
    api_key = os.environ.get("TAVILY_API_KEY", "")
    if not api_key:
        print("错误：未设置TAVILY_API_KEY")
        return None
    
    # 搜索AI新闻
    queries = [
        "AI人工智能 最新新闻 2025",
        "OpenAI Google Gemini 新功能 发布",
        "AI大模型 技术突破 进展"
    ]
    
    all_results = []
    
    for query in queries:
        try:
            url = "https://api.tavily.com/search"
            payload = {
                "api_key": api_key,
                "query": query,
                "max_results": 5,
                "search_depth": "advanced",
                "include_answer": True
            }
            
            headers = {"Content-Type": "application/json"}
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                all_results.append(result)
        except Exception as e:
            print(f"搜索失败: {e}")
    
    # 生成报告
    today = datetime.now().strftime("%Y年%m月%d日")
    
    report = f"""# 🤖 AI新闻摘要日报

> **日期**：{today}  
> **生成时间**：06:30  
> **生成者**：旺财Jarvis

---

## 📰 今日AI要闻

### 🔥 热点新闻
"""
    
    # 添加搜索结果
    news_count = 0
    for result in all_results:
        if "results" in result:
            for news in result["results"][:3]:
                news_count += 1
                title = news.get("title", "无标题")
                content = news.get("content", "")[:200]
                url = news.get("url", "")
                
                report += f"""
**{news_count}. {title}**

{content}...

[查看原文]({url})

---
"""
    
    report += f"""
## 📊 数据统计

- 搜索查询：{len(queries)} 个
- 获取新闻：{news_count} 条
- 数据来源：Tavily AI搜索

---

*本报告由OpenClaw大龙虾智能助手自动生成*  
*数据来源：Tavily AI搜索*
"""
    
    # 保存文件
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today_str}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ AI新闻摘要已生成: {filename}")
    return filename

if __name__ == "__main__":
    generate_ai_news_summary()