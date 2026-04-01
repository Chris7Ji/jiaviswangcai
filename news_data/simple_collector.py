#!/usr/bin/env python3
"""
Simple AI News Collector - 简化版
只收集近3天的真实新闻
"""
import json
import requests
from datetime import datetime, timedelta

SERPAPI_KEY = "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f"
NEWS_DB_PATH = "/Users/jiyingguo/.openclaw/workspace/news_data/news_db.json"

def search_news(query, num=10):
    """使用SerpAPI搜索新闻"""
    print(f"Searching: {query[:50]}...")
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "tbm": "nws",
            "num": num,
            "days": "3"  # 近3天
        }
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("news_results", [])
            print(f"  Found {len(results)} results")
            return results
        else:
            print(f"  Error: {resp.status_code}")
            return []
    except Exception as e:
        print(f"  Exception: {e}")
        return []

def main():
    queries = [
        "OpenAI AI news March 2026",
        "Google Gemini AI March 2026",
        "Anthropic Claude March 2026",
        "NVIDIA AI chip March 2026"
    ]
    
    all_news = []
    seen_titles = set()
    
    for q in queries:
        results = search_news(q)
        for r in results:
            title = r.get('title', '')
            if title and title not in seen_titles:
                seen_titles.add(title)
                all_news.append({
                    'title': title,
                    'summary': r.get('snippet', ''),
                    'url': r.get('link', ''),
                    'source': r.get('source', ''),
                    'date': r.get('date', ''),
                })
    
    print(f"\nTotal unique news: {len(all_news)}")
    
    # 保存
    today = datetime.now().strftime('%Y-%m-%d')
    db = {
        'last_updated': datetime.now().isoformat(),
        'news_by_date': {
            today: all_news[:10]  # 最多10条
        }
    }
    
    with open(NEWS_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"Saved to {NEWS_DB_PATH}")

if __name__ == '__main__':
    main()
