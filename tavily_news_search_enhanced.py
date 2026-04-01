#!/usr/bin/env python3
"""
增强版Tavily API搜索AI新闻脚本
"""

import os
import json
import requests
from datetime import datetime

def search_ai_news_with_tavily(api_key, query="AI news artificial intelligence", max_results=8):
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
    
    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": True,
        "max_results": max_results
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"Tavily API响应: {json.dumps(data, ensure_ascii=False)[:500]}...")
        
        # 提取新闻结果
        news_results = []
        if "results" in data:
            for result in data["results"]:
                news_item = {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "raw_content": result.get("raw_content", ""),
                    "published_date": result.get("published_date", datetime.now().strftime("%Y-%m-%d")),
                    "score": result.get("score", 0)
                }
                news_results.append(news_item)
        
        # 如果有答案，也包含进来
        if "answer" in data and data["answer"]:
            news_results.append({
                "title": "AI新闻摘要",
                "content": data["answer"],
                "raw_content": data["answer"],
                "url": "",
                "published_date": datetime.now().strftime("%Y-%m-%d"),
                "score": 1.0
            })
        
        return news_results
        
    except requests.exceptions.RequestException as e:
        print(f"Tavily API请求失败: {e}")
        if hasattr(e.response, 'text'):
            print(f"响应内容: {e.response.text}")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")
        return []

def format_news_for_summary(news_results):
    """
    将新闻结果格式化为详细摘要格式
    
    Args:
        news_results: Tavily API返回的新闻结果
        
    Returns:
        tuple: (markdown格式, html格式)
    """
    if not news_results:
        today = datetime.now().strftime("%Y年%m月%d日")
        no_news_md = f"# AI新闻每日摘要 - {today}\n\n## 今日重要AI新闻概览\n\n今天没有找到相关的AI新闻。\n\n---\n\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        no_news_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI新闻每日摘要 - {today}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px; }}
        h2 {{ color: #555; }}
        .news-item {{ margin-bottom: 30px; padding: 15px; border-left: 4px solid #4CAF50; background-color: #f9f9f9; }}
        .title {{ font-size: 18px; font-weight: bold; color: #333; }}
        .summary {{ margin: 10px 0; }}
        .source {{ color: #666; font-size: 14px; }}
        .footer {{ margin-top: 30px; padding-top: 10px; border-top: 1px solid #ddd; color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>AI新闻每日摘要 - {today}</h1>
    <h2>今日重要AI新闻概览</h2>
    <p>今天没有找到相关的AI新闻。</p>
    <div class="footer">
        生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</body>
</html>"""
        return no_news_md, no_news_html
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # Markdown格式
    md_summary = f"# AI新闻每日摘要 - {today}\n\n"
    md_summary += "## 今日重要AI新闻概览（通过Tavily API搜索）\n\n"
    md_summary += f"共找到 {len(news_results)} 条AI相关新闻\n\n"
    
    for i, news in enumerate(news_results, 1):
        title = news.get("title", "无标题")
        content = news.get("content", "")
        raw_content = news.get("raw_content", content)
        url = news.get("url", "")
        date = news.get("published_date", today)
        
        # 使用raw_content如果可用，否则使用content
        full_content = raw_content if raw_content else content
        
        md_summary += f"### {i}. {title}\n"
        md_summary += f"**来源：** {url if url else 'Tavily搜索'}\n"
        md_summary += f"**发布日期：** {date}\n\n"
        
        # 完整摘要（150-200字）
        if full_content:
            # 清理内容，移除多余空格和换行
            clean_content = ' '.join(full_content.split())
            # 截取适当长度
            if len(clean_content) > 400:
                summary_text = clean_content[:400] + "..."
            else:
                summary_text = clean_content
        else:
            summary_text = "暂无详细内容"
        
        md_summary += f"**完整摘要：**\n{summary_text}\n\n"
        
        # 深度分析（基于内容生成）
        analysis = generate_analysis(title, summary_text)
        md_summary += f"**深度分析：**\n{analysis}\n\n"
        
        # 影响评估
        impact = assess_impact(title, summary_text)
        md_summary += f"**影响评估：**\n{impact}\n\n"
        
        if url:
            md_summary += f"**原文链接：** [{url}]({url})\n"
        
        md_summary += "---\n\n"
    
    md_summary += f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    md_summary += "*数据来源: Tavily AI搜索 API*\n"
    
    # HTML格式
    html_summary = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI新闻每日摘要 - {today}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }}
        .container {{ background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 15px; margin-bottom: 25px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #2c3e50; margin-top: 25px; }}
        .news-item {{ margin-bottom: 35px; padding: 20px; border-left: 5px solid #3498db; background-color: #f8f9fa; border-radius: 5px; }}
        .news-number {{ display: inline-block; background-color: #3498db; color: white; width: 30px; height: 30px; text-align: center; line-height: 30px; border-radius: 50%; margin-right: 10px; font-weight: bold; }}
        .news-title {{ font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 10px; }}
        .meta {{ color: #7f8c8d; font-size: 14px; margin-bottom: 15px; }}
        .section {{ margin-bottom: 15px; }}
        .section-title {{ font-weight: bold; color: #2c3e50; margin-bottom: 5px; }}
        .summary {{ background-color: #f1f8ff; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .analysis {{ background-color: #fff8e1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .impact {{ background-color: #f1f8e9; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .link {{ margin-top: 10px; }}
        .link a {{ color: #2980b9; text-decoration: none; }}
        .link a:hover {{ text-decoration: underline; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #95a5a6; font-size: 13px; text-align: center; }}
        .stats {{ background-color: #ecf0f1; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>AI新闻每日摘要 - {today}</h1>
        
        <div class="stats">
            共找到 {len(news_results)} 条AI相关新闻（通过Tavily API搜索）
        </div>
        
        <h2>今日重要AI新闻概览</h2>
"""
    
    for i, news in enumerate(news_results, 1):
        title = news.get("title", "无标题")
        content = news.get("content", "")
        raw_content = news.get("raw_content", content)
        url = news.get("url", "")
        date = news.get("published_date", today)
        
        full_content = raw_content if raw_content else content
        if full_content:
            clean_content = ' '.join(full_content.split())
            if len(clean_content) > 400:
                summary_text = clean_content[:400] + "..."
            else:
                summary_text = clean_content
        else:
            summary_text = "暂无详细内容"
        
        analysis = generate_analysis(title, summary_text)
        impact = assess_impact(title, summary_text)
        
        html_summary += f"""
        <div class="news-item">
            <div class="news-title">
                <span class="news-number">{i}</span>{title}
            </div>
            <div class="meta">
                <strong>来源：</strong>{url if url else 'Tavily搜索'} | 
                <strong>发布日期：</strong>{date}
            </div>
            
            <div class="section">
                <div class="section-title">完整摘要：</div>
                <div class="summary">{summary_text}</div>
            </div>
            
            <div class="section">
                <div class="section-title">深度分析：</div>
                <div class="analysis">{analysis}</div>
            </div>
            
            <div class="section">
                <div class="section-title">影响评估：</div>
                <div class="impact">{impact}</div>
            </div>
"""
        
        if url:
            html_summary += f"""
            <div class="link">
                <strong>原文链接：</strong> <a href="{url}" target="_blank">{url}</a>
            </div>
"""
        
        html_summary += """
        </div>
"""
    
    html_summary += f"""
        <div class="footer">
            生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            数据来源: Tavily AI搜索 API
        </div>
    </div>
</body>
</html>"""
    
    return md_summary, html_summary

def generate_analysis(title, content):
    """生成深度分析"""
    keywords = ["AI", "人工智能", "机器学习", "深度学习", "大模型", "GPT", "LLM", "神经网络"]
    
    has_ai_keyword = any(keyword.lower() in title.lower() or keyword.lower() in content.lower() 
                         for keyword in keywords)
    
    if has_ai_keyword:
        if "突破" in title or "突破" in content or "重大" in title:
            return "这是一项重要的技术突破，可能对AI行业发展产生深远影响。该技术展示了AI领域的最新进展，值得业界密切关注。"
        elif "安全" in title or "安全" in content or "风险" in title:
            return "这涉及到AI安全的重要议题。随着AI技术的快速发展，安全性和伦理问题日益凸显，需要行业共同关注和解决。"
        elif "应用" in title or "应用" in content or "落地" in title:
            return "这表明AI技术正在从理论研究走向实际应用。商业化落地是AI技术价值实现的关键环节，对产业发展有积极意义。"
        else:
            return "这是AI领域的最新动态，反映了技术发展的趋势和方向。虽然具体影响尚待观察，但显示了行业的活跃度和创新力。"
    else:
        return "这是一般性的科技新闻，可能与AI技术有间接关联。需要进一步关注其与AI领域的交叉点和潜在影响。"

def assess_impact(title, content):
    """评估影响"""
    impact_keywords_high = ["革命性", "颠覆", "重大突破", "里程碑", "改变游戏规则"]
    impact_keywords_medium = ["重要进展", "显著提升", "创新", "突破性"]
    impact_keywords_low = ["更新", "改进", "优化", "调整"]
    
    title_lower = title.lower()
    content_lower = content.lower()
    
    for keyword in impact_keywords_high:
        if keyword in title_lower or keyword in content_lower:
            return "🔴 高影响：可能对行业产生重大影响，值得高度关注"
    
    for keyword in impact_keywords_medium:
        if keyword in title_lower or keyword in content_lower:
            return "🟡 中影响：对特定领域有重要意义，需要关注发展"
    
    for keyword in impact_keywords_low:
        if keyword in title_lower or keyword in content_lower:
            return "🟢 低影响：渐进式改进，对行业影响有限"
    
    return "⚪ 待观察：影响程度需要进一步评估"

def main():
    """主函数"""
    # 读取Tavily API密钥
    api_key_path = "/Users/jiyingguo/.openclaw/workspace/tavily_api_key.txt"
    
    if not os.path.exists(api_key_path):
        print(f"错误：找不到Tavily API密钥文件 {api_key_path}")
        return None, None
    
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()
    
    if not api_key:
        print("错误：Tavily API密钥为空")
        return None, None
    
    print("正在使用Tavily API搜索AI新闻...")
    
    # 搜索AI新闻 - 使用中文查询
    news_results = search_ai_news_with_tavily(
        api_key=api_key,
        query="AI 人工智能 最新新闻 2026年 机器学习 深度学习 大模型",
        max_results=8
    )
    
    if not news_results:
        print("尝试使用英文查询...")
        news_results = search_ai_news_with_tavily(
            api_key=api_key,
            query="AI artificial intelligence latest news 2026 machine learning deep learning large language models",
            max_results=8
        )
    
    if news_results:
        print(f"成功找到 {len(news_results)} 条AI新闻")
        
        # 格式化新闻摘要
        md_summary, html_summary = format_news_for_summary(news_results)
        
        return md_summary, html_summary
    else:
        print("未找到AI新闻")
        md_summary, html_summary = format_news_for_summary([])
        return md_summary, html_summary

if __name__ == "__main__":
    md, html = main()
    if md:
        today_str = datetime.now().strftime("%Y-%m-%d")
        output_dir = "/Users/jiyingguo/.openclaw/workspace/news_summaries"
        os.makedirs(output_dir, exist_ok=True)
        
        md_file = os.path.join(output_dir, f"ai_news_{today_str}.md")
        html_file = os.path.join(output_dir, f"ai_news_{today_str}.html")
        
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"新闻摘要已保存到:")
        print(f"  Markdown: {md_file}")
        print(f"  HTML: {html_file}")
        
        # 打印前3条新闻的标题
        print("\n今日AI新闻头条:")
        # 这里需要重新