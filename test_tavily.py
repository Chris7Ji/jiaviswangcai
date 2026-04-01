#!/usr/bin/env python3
"""
测试Tavily API
"""

import requests
import json

api_key = "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"

url = "https://api.tavily.com/search"

headers = {
    "Content-Type": "application/json"
}

payload = {
    "api_key": api_key,
    "query": "AI人工智能最新新闻",
    "search_depth": "basic",
    "max_results": 3
}

print("测试Tavily API...")
print(f"API密钥: {api_key[:10]}...")
print(f"请求URL: {url}")
print(f"请求负载: {json.dumps(payload, indent=2, ensure_ascii=False)}")

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"状态码: {response.status_code}")
    print(f"响应头: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    else:
        print(f"响应内容: {response.text}")
        
except Exception as e:
    print(f"请求异常: {type(e).__name__}: {e}")