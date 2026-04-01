#!/usr/bin/env python3
"""
简化版Tavily测试
"""

import requests
import json
from datetime import datetime

api_key = "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"

# 简化参数
payload = {
    "api_key": api_key,
    "query": "AI news 2026",
    "max_results": 3
}

print("测试简化版Tavily请求...")
response = requests.post("https://api.tavily.com/search", json=payload, timeout=10)

print(f"状态码: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"成功! 找到 {len(data.get('results', []))} 条结果")
    
    # 显示前3条结果
    for i, result in enumerate(data.get('results', [])[:3], 1):
        print(f"\n{i}. {result.get('title', '无标题')}")
        print(f"   链接: {result.get('url', '无链接')}")
        content = result.get('content', '')[:200]
        print(f"   内容: {content}...")
else:
    print(f"错误: {response.text}")