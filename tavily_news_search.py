#!/usr/bin/env python3
"""
使用Tavily API搜索AI新闻的脚本
"""

import os
import json
import requests
from datetime import datetime, timedelta

def search_ai_news_with_tavily(api_key, query="AI人工智能最新新闻", max_results=5):
    """
    使用Tavily API搜索AI新闻
    
    Args:
        api_key: Tavily API密钥
        query: 搜索查询
        max_results: 最大结果数
        
    Returns:
        list: 新闻结果列表
    """
    url = "https://api.tavily.com/search"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 搜索最近7天的新闻
    search_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "advanced",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": False,
        "max_results": max_results,
        "time_range": search_date
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # 提取新闻结果
        news_results = []
        if "results" in data:
            for result in data["results"]:
                news_item = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "published_date": result.get("published_date", ""),
                    "score": result.get("score", 0)
                }
                news_results.append(news_item)
        
        # 如果有答案，也包含进来
        if "answer" in data and data["answer"]:
            news_results.append({
                "title": "AI新闻摘要",
                "content": data["answer"],
                "url": "",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "score": 1.0
            })
        
        return news_results
        
    except requests.exceptions.RequestException as e:
        print(f"Tavily API请求失败: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return []

def format_news_for_summary(news_results):
    """
    将新闻结果格式化为摘要格式
    
    Args:
        news_results: Tavily API返回的新闻结果
        
    Returns:
        str: 格式化后的新闻摘要
    """
    if not news_results:
        return "今天没有找到相关的AI新闻。"
    
    today = datetime.now().strftime("%Y年%m月%d日")
    summary = f"# AI新闻每日摘要 - {today}\n\n"
    summary += "## 今日重要AI新闻概览（通过Tavily API搜索）\n\n"
    
    for i, news in enumerate(news_results, 1):
        title = news.get("title", "无标题")
        content = news.get("content", "")
        url = news.get("url", "")
        date = news.get("published_date", today)
        
        summary += f"### {i}. {title}\n"
        summary += f"**来源：** {url if url else 'Tavily搜索'}\n"
        summary += f"**发布日期：** {date}\n\n"
        
        # 截取内容，避免太长
        if len(content) > 500:
            content = content[:500] + "..."
        
        summary += f"**摘要：**\n{content}\n\n"
        
        if url:
            summary += f"**原文链接：** {url}\n"
        
        summary += "---\n\n"
    
    return summary

def main():
    """主函数"""
    # 读取Tavily API密钥
    api_key_path = "/Users/jiyingguo/.openclaw/workspace/tavily_api_key.txt"
    
    if not os.path.exists(api_key_path):
        print(f"错误：找不到Tavily API密钥文件 {api_key_path}")
        return
    
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()
    
    if not api_key:
        print("错误：Tavily API密钥为空")
        return
    
    print("正在使用Tavily API搜索AI新闻...")
    
    # 搜索AI新闻
    news_results = search_ai_news_with_tavily(
        api_key=api_key,
        query="人工智能 AI 最新技术 机器学习 深度学习 2026年",
        max_results=5
    )
    
    if news_results:
        print(f"成功找到 {len(news_results)} 条AI新闻")
        
        # 格式化新闻摘要
        summary = format_news_for_summary(news_results)
        
        # 保存到文件
        today_str = datetime.now().strftime("%Y-%m-%d")
        output_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_tavily_{today_str}.md"
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"新闻摘要已保存到: {output_file}")
        
        # 打印前3条新闻的标题
        print("\n今日AI新闻头条:")
        for i, news in enumerate(news_results[:3], 1):
            print(f"{i}. {news.get('title', '无标题')}")
    else:
        print("未找到AI新闻，将使用备用新闻源")

if __name__ == "__main__":
    main()