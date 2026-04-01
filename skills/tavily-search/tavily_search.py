#!/usr/bin/env python3
"""
Tavily AI搜索工具
高质量AI搜索，支持深度搜索和智能摘要
"""

import sys
import json
import os

# Tavily API配置 - 从环境变量读取
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def search_tavily(query, search_depth="basic", max_results=10, include_answer=True):
    """
    使用Tavily进行AI搜索
    
    Args:
        query: 搜索关键词
        search_depth: 搜索深度 (basic/advanced)
        max_results: 最大结果数量
        include_answer: 是否包含AI生成的答案
    
    Returns:
        dict: 搜索结果
    """
    try:
        # 直接使用 requests 调用 API，避免虚拟环境问题
        import requests
        
        url = "https://api.tavily.com/search"
        headers = {"Content-Type": "application/json"}
        data = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "search_depth": search_depth,
            "max_results": max_results,
            "include_answer": include_answer,
            "include_raw_content": True
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"搜索出错: {e}")
        return None

def format_results(response):
    """格式化搜索结果"""
    if not response:
        return "搜索失败"
    
    output = []
    
    # 显示AI生成的答案（如果有）
    answer = response.get('answer')
    if answer:
        output.append("🤖 AI摘要:")
        output.append(answer)
        output.append("")
        output.append("=" * 50)
        output.append("")
    
    # 显示搜索结果
    results = response.get('results', [])
    output.append(f"📊 找到 {len(results)} 条结果:\n")
    
    for i, r in enumerate(results, 1):
        title = r.get('title', '无标题')
        url = r.get('url', '')
        content = r.get('content', '')[:200]
        score = r.get('score', 0)
        
        output.append(f"{i}. {title} (相关度: {score:.2f})")
        output.append(f"   URL: {url}")
        output.append(f"   {content}...")
        output.append("")
    
    return "\n".join(output)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 tavily_search.py <搜索关键词> [深度] [数量]")
        print("示例: python3 tavily_search.py 'OpenClaw 最新版本' advanced 5")
        print("\n深度选项:")
        print("  basic    - 基础搜索（快）")
        print("  advanced - 深度搜索（慢但更详细）")
        sys.exit(1)
    
    query = sys.argv[1]
    search_depth = sys.argv[2] if len(sys.argv) > 2 else "basic"
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    
    print(f"🔍 Tavily搜索: {query}")
    print(f"   深度: {search_depth}, 数量: {max_results}")
    print("=" * 50)
    
    response = search_tavily(query, search_depth, max_results)
    
    if response:
        print(format_results(response))
        
        # 保存JSON结果
        output_file = "/tmp/tavily_search_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(response, f, ensure_ascii=False, indent=2)
        print(f"\n💾 完整结果已保存到: {output_file}")
    else:
        print("搜索失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
