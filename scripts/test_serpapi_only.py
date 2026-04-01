#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""单独测试SerpAPI（移除hl/gl参数后）"""

import sys
import os
import json
import urllib.parse
import requests

SERPAPI_KEY = "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f"

def search_serpapi(query: str, max_results: int = 5):
    """使用SerpAPI搜索新闻"""
    # 不带 hl=zh-CN&gl=cn 参数
    url = f"https://serpapi.com/search?q={urllib.parse.quote(query)}&api_key={SERPAPI_KEY}&num={max_results}&tbm=nws"
    
    print(f"URL: {url[:100]}...")
    
    response = requests.get(url, timeout=60)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        results = data.get("news_results", []) or data.get("organic_results", [])
        print(f"news_results: {len(data.get('news_results', []))} 条")
        print(f"organic_results: {len(data.get('organic_results', []))} 条")
        print(f"\n前3条结果:")
        for i, item in enumerate(results[:3], 1):
            print(f"  {i}. {item.get('title', '')[:60]}")
        return results
    return []

if __name__ == "__main__":
    query = "AI人工智能 最新新闻"
    print(f"测试查询: {query}")
    print("=" * 50)
    results = search_serpapi(query, max_results=5)
    print(f"\n总计: {len(results)} 条结果")
