#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试搜索合并功能
"""
import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 设置API Key
os.environ['SERPAPI_KEY'] = 'b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f'
os.environ['TAVILY_API_KEY'] = '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'

from ai_news_search import search_news

def main():
    print("=" * 60)
    print("测试搜索合并功能")
    print("=" * 60)
    
    query = "AI人工智能 最新新闻"
    max_results = 5
    
    print(f"\n查询词: {query}")
    print(f"最大结果: {max_results}")
    print()
    
    try:
        results = search_news(query, max_results)
        print(f"\n✅ 成功！共获取 {len(results)} 条结果\n")
        
        for i, r in enumerate(results, 1):
            title = r.get('title', '无标题')
            source = r.get('source', '未知来源')
            url = r.get('url', '')
            print(f"  {i}. [{source}] {title[:50]}...")
            print(f"     URL: {url[:60]}...")
            print()
            
    except Exception as e:
        print(f"\n❌ 失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
