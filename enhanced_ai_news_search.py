#!/usr/bin/env python3
"""
增强版AI新闻搜索脚本 - 结合Tavily API和传统新闻源
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
import subprocess

def search_with_tavily(api_key, query="AI人工智能最新新闻 2026年", max_results=5):
    """使用Tavily API搜索新闻"""
    url = "https://api.tavily.com/search"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # 搜索最近3天的新闻
    search_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    
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
        return data
        
    except Exception as e:
        print(f"Tavily搜索失败: {e}")
        return None

def fetch_xinhua_news():
    """抓取新华网科技新闻（备用方案）"""
    try:
        # 这里可以调用现有的web_fetch功能
        # 暂时返回空结果，由主任务处理
        return []
    except Exception as e:
        print(f"新华网抓取失败: {e}")
        return []

def process_tavily_results(tavily_data):
    """处理Tavily API返回的结果"""
    if not tavily_data or "results" not in tavily_data:
        return []
    
    news_items = []
    
    # 处理搜索结果
    for result in tavily_data.get("results", []):
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()
        
        if title and content:
            # 提取发布日期（从内容中推断或使用当前日期）
            published_date = result.get("published_date", datetime.now().strftime("%Y-%m-%d"))
            
            news_item = {
                "title": title,
                "url": url,
                "content": content[:500] + "..." if len(content) > 500 else content,
                "source": "Tavily搜索",
                "date": published_date,
                "score": result.get("score", 0)
            }
            news_items.append(news_item)
    
    # 处理答案（如果有）
    if "answer" in tavily_data and tavily_data["answer"]:
        news_items.append({
            "title": "AI新闻综合摘要",
            "content": tavily_data["answer"],
            "url": "",
            "source": "Tavily AI摘要",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "score": 1.0
        })
    
    return news_items

def format_news_summary(news_items, use_tavily=True):
    """格式化新闻摘要"""
    if not news_items:
        return "今天没有找到相关的AI新闻。"
    
    today = datetime.now().strftime("%Y年%m月%d日")
    source_note = "（通过Tavily API智能搜索）" if use_tavily else "（通过传统新闻源）"
    
    summary = f"# AI新闻每日摘要 - {today}\n\n"
    summary += f"## 今日重要AI新闻概览{source_note}\n\n"
    
    # 按分数排序
    sorted_news = sorted(news_items, key=lambda x: x.get("score", 0), reverse=True)
    
    for i, news in enumerate(sorted_news[:4], 1):  # 取前4条
        title = news.get("title", "无标题")
        content = news.get("content", "")
        url = news.get("url", "")
        source = news.get("source", "未知来源")
        date = news.get("date", today)
        
        summary += f"### {i}. {title}\n"
        summary += f"**来源：** {source}\n"
        
        if url:
            summary += f"**链接：** {url}\n"
        
        summary += f"**发布日期：** {date}\n\n"
        summary += f"**内容摘要：**\n{content}\n\n"
        
        if url:
            summary += f"**原文链接：** {url}\n"
        
        summary += "---\n\n"
    
    return summary

def main():
    """主函数"""
    # 读取Tavily API密钥
    api_key_path = "/Users/jiyingguo/.openclaw/workspace/tavily_api_key.txt"
    
    if not os.path.exists(api_key_path):
        print("错误：找不到Tavily API密钥文件")
        return None
    
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()
    
    if not api_key:
        print("错误：Tavily API密钥为空")
        return None
    
    print("正在使用Tavily API搜索AI新闻...")
    
    # 搜索AI新闻
    tavily_data = search_with_tavily(
        api_key=api_key,
        query="人工智能 AI 机器学习 深度学习 大模型 2026年 最新技术",
        max_results=8
    )
    
    news_items = []
    use_tavily = False
    
    if tavily_data and "results" in tavily_data:
        news_items = process_tavily_results(tavily_data)
        use_tavily = True
        print(f"✅ 通过Tavily API找到 {len(news_items)} 条AI新闻")
    else:
        print("⚠️ Tavily API未返回结果，将使用备用新闻源")
        # 这里可以调用现有的新闻抓取逻辑
        news_items = []
    
    # 生成摘要
    summary = format_news_summary(news_items, use_tavily)
    
    # 保存到文件
    today_str = datetime.now().strftime("%Y-%m-%d")
    output_dir = "/Users/jiyingguo/.openclaw/workspace/news_summaries"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = f"{output_dir}/ai_news_enhanced_{today_str}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"✅ 增强版新闻摘要已保存到: {output_file}")
    
    # 返回摘要内容
    return summary

if __name__ == "__main__":
    result = main()
    if result:
        print("\n" + "="*50)
        print("新闻摘要生成完成！")
        print("="*50)