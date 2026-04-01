#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 SerpAPI 不同参数的效果
"""
import requests
import urllib.parse
import os

SERPAPI_KEY = os.environ.get('SERPAPI_KEY', 'b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f')

def test_serpapi(query, use_news=True):
    """测试 SerpAPI 搜索"""
    print(f"\n{'='*60}")
    print(f"测试: {query}")
    print(f"新闻模式: {'开启' if use_news else '关闭'}")
    print('='*60)
    
    params = {
        'q': query,
        'api_key': SERPAPI_KEY,
        'num': 5,
        'hl': 'zh-CN',
        'gl': 'cn',
    }
    
    if use_news:
        params['tbm'] = 'nws'  # 新闻模式
    
    url = f"https://serpapi.com/search?{'&'.join(f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items())}"
    
    print(f"URL: {url[:100]}...")
    
    try:
        response = requests.get(url, timeout=30)
        print(f"状态码: {response.status_code}")
        
        data = response.json()
        
        if use_news:
            results = data.get('news_results', [])
            print(f"news_results: {len(results)} 条")
        else:
            results = data.get('organic_results', [])
            print(f"organic_results: {len(results)} 条")
        
        # 也打印一下整体响应结构
        print(f"\n响应中的keys: {list(data.keys())[:10]}")
        
        if results:
            print(f"\n前3条结果:")
            for i, r in enumerate(results[:3], 1):
                print(f"  {i}. {r.get('title', '无标题')[:60]}")
        else:
            print(f"\n无结果，打印完整响应:")
            print(f"  {str(data)[:500]}")
            
    except Exception as e:
        print(f"错误: {e}")

def main():
    queries = [
        "AI人工智能",
        "人工智能 最新消息",
        "AI artificial intelligence news",
    ]
    
    for query in queries:
        test_serpapi(query, use_news=True)
        test_serpapi(query, use_news=False)

if __name__ == "__main__":
    main()
