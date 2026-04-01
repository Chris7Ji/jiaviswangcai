#!/usr/bin/env python3
"""
增强版Tavily AI新闻搜索
"""

import requests
import json
import sys
import os
from datetime import datetime

def enhanced_tavily_search():
    # 读取API密钥
    api_key_path = "/Users/jiyingguo/.openclaw/workspace/tavily_api_key.txt"
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()

    # 搜索查询
    search_query = "AI人工智能最新新闻 2026年 机器学习 深度学习 大模型 生成式AI"

    print(f"开始搜索: {search_query}")
    print(f"API密钥: {api_key[:10]}...")

    # Tavily API请求
    payload = {
        "api_key": api_key,
        "query": search_query,
        "max_results": 10,
        "include_answer": True,
        "search_depth": "advanced",
        "include_images": False,
        "include_raw_content": True,
        "time_range": "month"  # 最近一个月
    }

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            answer = data.get('answer', '')
            
            print(f"成功! 找到 {len(results)} 条结果")
            
            # 保存原始结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw_output_path = f"/Users/jiyingguo/.openclaw/workspace/tavily_raw_{timestamp}.json"
            with open(raw_output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"原始结果已保存到: {raw_output_path}")
            
            # 显示结果摘要
            print("\n=== 搜索结果摘要 ===")
            if answer:
                print(f"AI摘要: {answer[:500]}...")
            
            print(f"\n=== 详细结果 ({len(results)}条) ===")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result.get('title', '无标题')}")
                print(f"   来源: {result.get('url', '无链接')}")
                content = result.get('content', '')[:150]
                print(f"   摘要: {content}...")
                
            return data
            
        else:
            print(f"Tavily API错误: {response.status_code}")
            print(f"响应: {response.text}")
            return None
            
    except Exception as e:
        print(f"请求异常: {e}")
        return None

if __name__ == "__main__":
    enhanced_tavily_search()