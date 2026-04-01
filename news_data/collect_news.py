#!/usr/bin/env python3
"""
AI News Collector - 自动收集AI新闻
使用SerpAPI搜索北美AI巨头最新动态
"""

import json
import requests
import sys
from datetime import datetime, timedelta
import re
import os

# ========== 配置 ==========
SERPAPI_KEY = "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f"
NEWS_DB_PATH = "/Users/jiyingguo/.openclaw/workspace/news_data/news_db.json"
OUTPUT_HTML_PATH = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/news.html"
WEBSITE_REPO_PATH = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai"

# 搜索关键词（英文）
SEARCH_QUERIES = [
    "OpenAI GPT-5 latest news March 2026",
    "Google Gemini AI news March 2026",
    "Anthropic Claude AI news March 2026",
    "NVIDIA AI chip Blackwell news March 2026",
    "OpenAI Sam Altman news March 2026",
    "Google DeepMind Demis Hassabis news March 2026",
    "AI artificial intelligence breakthrough March 2026",
    "ChatGPT GPT models latest update March 2026"
]

# 来源映射
SOURCE_MAP = {
    "openai.com": "OpenAI",
    "blog.google": "Google AI",
    "deepmind.google": "Google DeepMind",
    "anthropic.com": "Anthropic",
    "nvidia.com": "NVIDIA",
    "techcrunch.com": "TechCrunch",
    "theverge.com": "The Verge",
    "arstechnica.com": "Ars Technica",
    "hackernews.com": "Hacker News",
    "reddit.com": "Reddit",
    "reuters.com": "Reuters",
    "bloomberg.com": "Bloomberg"
}

def get_source_name(url):
    """从URL提取来源名称"""
    for domain, name in SOURCE_MAP.items():
        if domain in url.lower():
            return name
    return "Tech Media"

def search_news_serpapi(query, num_results=10):
    """使用SerpAPI搜索新闻"""
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "engine": "google",
            "tbm": "nws",  # News
            "num": num_results
        }
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get("news_results", [])
            return results
        else:
            print(f"SerpAPI错误: {response.status_code}")
            return []
    except Exception as e:
        print(f"搜索异常: {e}")
        return []

def search_news_tavily(query, num_results=10):
    """使用Tavily API搜索新闻（备用）"""
    try:
        tavily_key = "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"
        url = "https://api.tavily.com/search"
        payload = {
            "query": query,
            "api_key": tavily_key,
            "max_results": num_results,
            "topic": "news"
        }
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            return results
        else:
            print(f"Tavily错误: {response.status_code}")
            return []
    except Exception as e:
        print(f"Tavily搜索异常: {e}")
        return []

def deduplicate_news(news_list):
    """基于标题去重"""
    seen_titles = set()
    unique_news = []
    for item in news_list:
        title = item.get("title", "").lower()
        # 清理标题用于比较
        clean_title = re.sub(r'[^\w\s]', '', title)[:50]
        if clean_title not in seen_titles and len(title) > 10:
            seen_titles.add(clean_title)
            unique_news.append(item)
    return unique_news

def rank_news(news_list):
    """基于来源权威性和时效性对新闻排序"""
    authority_weights = {
        "OpenAI": 10,
        "Google AI": 9,
        "Google DeepMind": 9,
        "Anthropic": 10,
        "NVIDIA": 8,
        "TechCrunch": 7,
        "The Verge": 6,
        "Ars Technica": 6,
        "Hacker News": 5,
        "Reddit": 4,
        "Reuters": 7,
        "Bloomberg": 7
    }
    
    def get_weight(item):
        source = item.get("source", "")
        # 来源权重
        w = authority_weights.get(source, 5)
        # 标题关键词加权
        title = item.get("title", "").lower()
        if any(kw in title for kw in ["gpt", "gemini", "claude", "llama", "model", "breakthrough", "launch", "release"]):
            w += 2
        return w
    
    return sorted(news_list, key=get_weight, reverse=True)

def format_news_for_html(news_item, index, date_display):
    """将单条新闻格式化为HTML"""
    title = news_item.get("title", "无标题")
    link = news_item.get("link", "#")
    snippet = news_item.get("snippet", news_item.get("content", ""))
    source = news_item.get("source", get_source_name(link))
    
    # 截取摘要
    if len(snippet) > 150:
        snippet = snippet[:150] + "..."
    
    # 确定标签颜色
    tag_class = "tag-"
    if "openai" in link.lower() or "chatgpt" in title.lower():
        tag_class = "tag-openai"
    elif "google" in link.lower() or "gemini" in title.lower():
        tag_class = "tag-google"
    elif "anthropic" in link.lower() or "claude" in title.lower():
        tag_class = "tag-anthropic"
    elif "nvidia" in link.lower():
        tag_class = "tag-nvidia"
    else:
        tag_class = "tag-other"
    
    return f'''
                    <a href="{link}" target="_blank" class="news-item">
                        <span class="tag {tag_class}">{source}</span>
                        <h3>{title}</h3>
                        <p class="summary">{snippet}</p>
                        <div class="meta">
                            <span class="source">{source}</span>
                            <span>{date_display}</span>
                            <span class="read-more">阅读原文 →</span>
                        </div>
                    </a>'''

def collect_and_save_news():
    """主函数：收集新闻并保存"""
    print(f"🚀 开始收集AI新闻... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_news = []
    
    # 1. 使用SerpAPI搜索
    print("📡 正在通过SerpAPI搜索...")
    for query in SEARCH_QUERIES:
        print(f"  搜索: {query[:50]}...")
        results = search_news_serpapi(query, 10)
        for item in results:
            all_news.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", ""),
                "source": get_source_name(item.get("link", "")),
                "date": item.get("date", ""),
                "collected_at": datetime.now().isoformat()
            })
        if len(results) > 0:
            print(f"    获得 {len(results)} 条结果")
    
    # 如果SerpAPI结果太少，用Tavily备用
    if len(all_news) < 15:
        print("📡 SerpAPI结果不足，使用Tavily备用...")
        for query in SEARCH_QUERIES[:4]:
            results = search_news_tavily(query, 10)
            for item in results:
                all_news.append({
                    "title": item.get("title", ""),
                    "link": item.get("url", ""),
                    "snippet": item.get("content", "")[:200],
                    "source": get_source_name(item.get("url", "")),
                    "date": item.get("published_date", ""),
                    "collected_at": datetime.now().isoformat()
                })
    
    print(f"📊 共收集到 {len(all_news)} 条原始新闻")
    
    # 2. 去重和排序
    unique_news = deduplicate_news(all_news)
    ranked_news = rank_news(unique_news)
    top_news = ranked_news[:15]  # 取前15条
    
    print(f"✅ 去重后保留 {len(unique_news)} 条，精选 {len(top_news)} 条")
    
    # 3. 保存到数据库
    today = datetime.now().strftime("%Y-%m-%d")
    db = {"last_updated": datetime.now().isoformat(), "news_by_date": {}}
    
    if os.path.exists(NEWS_DB_PATH):
        try:
            with open(NEWS_DB_PATH, 'r', encoding='utf-8') as f:
                db = json.load(f)
        except:
            pass
    
    db["last_updated"] = datetime.now().isoformat()
    db["news_by_date"][today] = top_news
    
    # 保留最近7天的数据
    cutoff = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    db["news_by_date"] = {k: v for k, v in db["news_by_date"].items() if k >= cutoff}
    
    with open(NEWS_DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    
    print(f"💾 已保存到数据库: {NEWS_DB_PATH}")
    
    return top_news, today

def generate_html_page(news_list, date_str):
    """生成news.html页面"""
    today_display = datetime.now().strftime("%Y年%m月%d日")
    date_display = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y年%m月%d日")
    
    # 生成日期选择器HTML
    date_pills = ""
    for i in range(7):
        d = datetime.now() - timedelta(days=i)
        date_str_i = d.strftime("%Y-%m-%d")
        display = d.strftime("%m/%d %a")
        is_active = "active" if date_str_i == date_str else ""
        date_pills += f'<a href="?date={date_str_i}" class="date-pill {is_active}">{display}</a>'
    
    # 生成新闻HTML
    if news_list:
        # 头条新闻
        top = news_list[0]
        featured_html = f'''
                <div class="featured-news">
                    <span class="tag">🔥 今日头条</span>
                    <h2>{top["title"]}</h2>
                    <p class="summary">{top["snippet"]}</p>
                    <div class="meta">
                        <span class="source">{top["source"]}</span>
                        <span>{date_display}</span>
                        <a href="{top["link"]}" target="_blank" style="color:white;margin-left:1rem;">阅读原文 →</a>
                    </div>
                </div>'''
        
        # 其他新闻
        other_news_html = ""
        for i, item in enumerate(news_list[1:], 1):
            other_news_html += format_news_for_html(item, i, date_display)
    else:
        featured_html = '''
                <div class="featured-news">
                    <span class="tag">📡 数据收集中</span>
                    <h2>正在获取最新AI新闻...</h2>
                    <p class="summary">系统正在自动收集今日AI行业最新动态，请稍后刷新页面查看。</p>
                    <div class="meta">
                        <span class="source">旺财Jarvis AI新闻系统</span>
                        <span>{date_display}</span>
                    </div>
                </div>'''
        other_news_html = ""
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AI新闻日报 - 旺财Jarvis</title>
    <meta name="description" content="每日AI行业新闻精选，涵盖Google、Anthropic、OpenAI、NVIDIA等北美AI巨头最新动态">
    
    <link rel="icon" href="images/logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/diary.css">
    <style>
        .news-hero {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 2rem 3rem;
            text-align: center;
            border-radius: 0 0 20px 20px;
        }}
        .news-hero h1 {{ font-size: 2.5rem; margin-bottom: 0.5rem; }}
        .news-hero p {{ opacity: 0.9; font-size: 1.1rem; }}
        
        .news-date-selector {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        .date-pills {{
            display: flex;
            gap: 0.5rem;
            overflow-x: auto;
            padding: 0.5rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .date-pill {{
            padding: 0.5rem 1rem;
            background: var(--bg-secondary);
            border-radius: 20px;
            text-decoration: none;
            color: var(--text-primary);
            font-size: 0.9rem;
            white-space: nowrap;
            transition: all 0.3s;
        }}
        .date-pill:hover, .date-pill.active {{
            background: var(--accent-gold);
            color: white;
        }}
        
        .news-container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }}
        
        .featured-news {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            color: white;
        }}
        .featured-news .tag {{
            background: rgba(255,255,255,0.2);
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.8rem;
            display: inline-block;
            margin-bottom: 0.75rem;
        }}
        .featured-news h2 {{
            font-size: 1.8rem;
            margin-bottom: 1rem;
            line-height: 1.4;
        }}
        .featured-news .summary {{
            font-size: 1rem;
            line-height: 1.6;
            opacity: 0.95;
            margin-bottom: 1rem;
        }}
        .featured-news .meta {{
            font-size: 0.85rem;
            opacity: 0.8;
        }}
        .featured-news .source {{ margin-right: 1rem; }}
        
        .news-section-title {{
            font-size: 1.3rem;
            color: var(--text-primary);
            margin: 2rem 0 1rem;
            padding-left: 1rem;
            border-left: 4px solid var(--accent-gold);
        }}
        
        .news-grid {{ display: grid; gap: 1rem; }}
        
        .news-item {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s;
            border: 1px solid transparent;
        }}
        .news-item:hover {{
            border-color: var(--accent-gold);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .news-item .tag {{
            color: white;
            padding: 0.2rem 0.6rem;
            border-radius: 8px;
            font-size: 0.75rem;
            display: inline-block;
            margin-bottom: 0.5rem;
        }}
        .tag-openai {{ background: #10a37f; }}
        .tag-google {{ background: #4285f4; }}
        .tag-anthropic {{ background: #d91e18; }}
        .tag-nvidia {{ background: #76b900; }}
        .tag-other {{ background: #6b7280; }}
        
        .news-item h3 {{
            font-size: 1.1rem;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            line-height: 1.5;
        }}
        .news-item .summary {{
            font-size: 0.9rem;
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: 0.75rem;
        }}
        .news-item .meta {{
            display: flex;
            gap: 1rem;
            font-size: 0.8rem;
            color: var(--text-tertiary);
            align-items: center;
        }}
        .news-item .source {{ color: var(--accent-gold); font-weight: 500; }}
        .news-item .read-more {{ margin-left: auto; color: var(--accent-blue); }}
        .news-item a {{ text-decoration: none; color: inherit; display: block; }}
        
        .update-info {{
            text-align: center;
            padding: 2rem;
            color: var(--text-tertiary);
            font-size: 0.85rem;
        }}
        
        @media (max-width: 768px) {{
            .news-hero h1 {{ font-size: 1.8rem; }}
            .featured-news h2 {{ font-size: 1.4rem; }}
            .news-item {{ padding: 1rem; }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">
                <img src="images/logo.png" class="logo-img" alt="旺财">
                <span class="logo-text">旺财Jarvis</span>
            </a>
            <ul class="nav-menu">
                <li><a href="index.html">首页</a></li>
                <li><a href="diary.html">📖 日志</a></li>
                <li><a href="skills.html">💡 技能</a></li>
                <li><a href="news.html" class="active">🚀 AI新闻日报</a></li>
                <li><a href="about.html">👤 关于我</a></li>
            </ul>
            <button class="nav-toggle" id="navToggle">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <header class="news-hero">
        <h1>🚀 AI新闻日报</h1>
        <p>每日追踪Google、Anthropic、OpenAI、NVIDIA等北美AI巨头最新动态</p>
    </header>

    <div class="news-date-selector">
        <div class="date-pills" id="datePills">
            {date_pills}
        </div>
    </div>

    <main class="news-container" id="newsContent">
        <div class="update-info">
            <p>📅 {date_display} · 🔄 最后更新: {datetime.now().strftime('%H:%M:%S')}</p>
        </div>
        
        {featured_html}
        
        <h3 class="news-section-title">📰 最新资讯 ({len(news_list)}条)</h3>
        <div class="news-grid">
            {other_news_html}
        </div>
        
        <div class="update-info">
            <p>📝 新闻来源: Google AI Blog · OpenAI Blog · Anthropic Blog · NVIDIA News · TechCrunch · The Verge · Ars Technica · Hacker News</p>
            <p>🔧 系统自动收集与精选 · 每日21:00自动更新</p>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>© 2026 旺财Jarvis · AI智能助手 · 持续进化中</p>
        </div>
    </footer>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const navToggle = document.getElementById('navToggle');
            const navMenu = document.querySelector('.nav-menu');
            if (navToggle && navMenu) {{
                navToggle.addEventListener('click', () => {{
                    navToggle.classList.toggle('active');
                    navMenu.classList.toggle('active');
                }});
            }}
        }});
    </script>
</body>
</html>'''
    
    return html

def main():
    """主执行流程"""
    # 1. 收集新闻
    news_list, today = collect_and_save_news()
    
    # 2. 生成HTML
    print("🎨 正在生成news.html...")
    html_content = generate_html_page(news_list, today)
    
    with open(OUTPUT_HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ news.html 已生成: {OUTPUT_HTML_PATH}")
    
    # 3. Git提交
    print("📤 正在提交到GitHub...")
    try:
        os.system(f'git -C {WEBSITE_REPO_PATH} add news.html')
        os.system(f'git -C {WEBSITE_REPO_PATH} commit -m "AI新闻日报更新: {today} 收集{len(news_list)}条新闻"')
        os.system(f'git -C {WEBSITE_REPO_PATH} push origin main')
        print("✅ Git提交成功!")
    except Exception as e:
        print(f"⚠️ Git提交失败: {e}")
    
    print(f"\n🎉 完成! 共收集 {len(news_list)} 条新闻")
    return news_list

if __name__ == "__main__":
    main()
