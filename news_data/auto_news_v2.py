import requests
import json
import os
import subprocess
from datetime import datetime

SERPAPI_KEY = "b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f"
DEEPSEEK_KEY = "sk-451f43ffa9764b7e91430e4d39538356"

WORKSPACE = "/Users/jiyingguo/.openclaw/workspace"
REPO_DIR = f"{WORKSPACE}/jiaviswangcai.ai"
DB_PATH = f"{WORKSPACE}/news_data/news_db.json"
HTML_PATH = f"{REPO_DIR}/news.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 AI新闻日报 - 旺财Jarvis</title>
    <link rel="icon" href="images/logo.png">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="css/diary.css">
    <style>
        .news-hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 100px 2rem 3rem; text-align: center; border-radius: 0 0 20px 20px; }
        .news-hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
        .news-hero p { opacity: 0.9; font-size: 1.1rem; }
        .news-date-selector { max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
        .date-pills { display: flex; gap: 0.5rem; overflow-x: auto; padding: 0.5rem; justify-content: flex-start; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
        .date-pills::-webkit-scrollbar { height: 6px; }
        .date-pills::-webkit-scrollbar-thumb { background: #ccc; border-radius: 3px; }
        .date-pill { padding: 0.5rem 1rem; border-radius: 20px; background: #f0f0f0; color: #333; text-decoration: none; transition: all 0.2s; white-space: nowrap; cursor: pointer; border: none; font-size: 0.95rem; font-family: inherit; }
        .date-pill:hover { background: #e0e0e0; }
        .date-pill.active { background: #667eea; color: white; font-weight: bold; }
        .news-container { max-width: 1000px; margin: 0 auto; padding: 0 1rem 4rem; }
        .update-info { text-align: center; color: #666; margin-bottom: 2rem; font-size: 0.9rem; }
        .featured-news { background: #fff; border-radius: 12px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-left: 5px solid #667eea; transition: transform 0.2s; }
        .featured-news .tag { background: #ffeb3b; color: #f57f17; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: bold; display: inline-block; margin-bottom: 1rem; }
        .featured-news h2 { margin-top: 0; color: #333; }
        .featured-news .summary { color: #555; line-height: 1.6; font-size: 1.05rem; }
        .news-section-title { margin: 3rem 0 1.5rem; border-bottom: 2px solid #eee; padding-bottom: 0.5rem; }
        .news-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }
        .news-item { background: #fff; border-radius: 8px; padding: 1.5rem; border: 1px solid #eaeaea; transition: all 0.2s; display: flex; flex-direction: column; text-decoration: none; color: inherit; }
        .news-item h3 { margin: 0 0 1rem 0; font-size: 1.1rem; line-height: 1.4; color: #2c3e50; }
        .news-item p { color: #666; font-size: 0.95rem; line-height: 1.5; flex-grow: 1; }
        .news-item .meta { margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee; display: flex; justify-content: space-between; font-size: 0.85rem; color: #999; align-items: center; }
        .source { font-weight: 500; color: #3d9ca8; }
        .navbar { background: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); position: fixed; top: 0; width: 100%; z-index: 1000; display: flex; justify-content: space-between; align-items: center; }
        .logo a { display: flex; align-items: center; gap: 10px; text-decoration: none; color: #333; font-weight: bold; font-size: 1.2rem; }
        .logo img { height: 40px; border-radius: 50%; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #666; font-weight: 500; transition: color 0.3s; }
        .nav-links a:hover, .nav-links a.active { color: #d4a84b; }
        
        .day-news-container { display: none; animation: fadeIn 0.4s ease; }
        .day-news-container.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="logo"><a href="index.html"><img src="images/logo.png" alt="旺财Jarvis Logo">旺财Jarvis</a></div>
        <div class="nav-links">
            <a href="index.html">首页</a>
            <a href="diary.html">📖 成长日记</a>
            <a href="skills.html">💡 技能与功能</a>
            <a href="ascend.html">⚡️ 昇腾AI知识</a>
            <a href="news.html" class="active">🚀 AI新闻日报</a>
            <a href="about.html">👤 关于我</a>
        </div>
    </nav>
    <header class="news-hero">
        <h1>🚀 AI 新闻日报</h1>
        <p>为你精选过去半个月科技巨头、大模型公司的最新动态</p>
    </header>
    
    <div class="news-date-selector">
        <div class="date-pills" id="datePillsContainer">
            {date_pills}
        </div>
    </div>
    
    <main class="news-container">
        {all_days_html}
    </main>
    
    <footer>
        <p>© 2026 旺财Jarvis. Build by Iron Man.</p>
    </footer>

    <script>
        function showDate(dateStr) {
            document.querySelectorAll('.date-pill').forEach(btn => {
                if (btn.dataset.date === dateStr) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
            
            document.querySelectorAll('.day-news-container').forEach(container => {
                if (container.id === 'news-' + dateStr) {
                    container.classList.add('active');
                } else {
                    container.classList.remove('active');
                }
            });
        }
    </script>
</body>
</html>
"""

def generate_html(target_date, items):
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    dates = sorted(db.get("news_by_date", {}).keys(), reverse=True)
    dates = dates[:15] # top 15 days
    
    if not dates:
        print("No news to render.")
        return

    date_pills_html = ""
    all_days_html = ""
    
    for i, date_str in enumerate(dates):
        day_items = db["news_by_date"][date_str]
        
        is_active = "active" if i == 0 else ""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            display_date = f"{dt.month}月{dt.day}日"
            if i == 0:
                display_date += " (最新)"
        except:
            display_date = date_str
            
        date_pills_html += f'<button class="date-pill {is_active}" data-date="{date_str}" onclick="showDate(\'{date_str}\')">{display_date}</button>\n            '
        
        if not day_items:
            continue
            
        featured = day_items[0]
        rest = day_items[1:]
        
        feat_article_date = featured.get('article_date', '')
        feat_date_str = f'<span style="margin-left:1rem; color:#888;">{feat_article_date}</span>' if feat_article_date else ''
        
        featured_html = f"""
            <div class="featured-news">
                <span class="tag">🔥 重点头条</span>
                <h2>{featured.get('title', '')}</h2>
                <p class="summary">{featured.get('summary', '')}</p>
                <div class="meta" style="margin-top: 1rem; font-size: 0.9rem;">
                    <div>
                        <span class="source">{featured.get('source', '')}</span>
                        {feat_date_str}
                    </div>
                    <a href="{featured.get('url', '#')}" target="_blank" style="color:#667eea;font-weight:bold;margin-left:1rem;">阅读原文 →</a>
                </div>
            </div>
        """
        
        grid_html = ""
        for item in rest:
            item_article_date = item.get('article_date', '')
            item_date_str = f'<span style="margin-left:1rem; color:#888; font-size:0.8rem;">{item_article_date}</span>' if item_article_date else ''
            
            grid_html += f"""
                <a href="{item.get('url', '#')}" target="_blank" class="news-item">
                    <h3>{item.get('title', '')}</h3>
                    <p>{item.get('summary', '')}</p>
                    <div class="meta">
                        <div>
                            <span class="source">{item.get('source', '')}</span>
                            {item_date_str}
                        </div>
                        <span>阅读原文 &rarr;</span>
                    </div>
                </a>
            """
            
        day_html = f"""
        <div id="news-{date_str}" class="day-news-container {is_active}">
            <div class="update-info"><p>📅 日报日期: {date_str} · 共有 {len(day_items)} 条资讯</p></div>
            {featured_html}
            <h3 class="news-section-title">📰 更多资讯</h3>
            <div class="news-grid">{grid_html}</div>
        </div>
        """
        all_days_html += day_html
        
    final_html = HTML_TEMPLATE.replace("{date_pills}", date_pills_html).replace("{all_days_html}", all_days_html)
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(final_html)

def fetch_news():
    print("Fetching from SerpAPI...")
    url = f"https://serpapi.com/search.json?q=AI+OR+OpenAI+OR+Anthropic+OR+Nvidia+latest+news&tbm=nws&api_key={SERPAPI_KEY}&tbs=qdr:d2&gl=us&hl=en"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json().get('news_results', [])
    except Exception as e:
        print("SerpAPI Error:", e)
    return []

def translate_and_summarize(title, snippet):
    print(f"Translating: {title}")
    prompt = f"请把以下英文新闻标题和摘要翻译成中文，并写一段详细的中文内容（100字左右），说明其核心内容和影响。直接输出JSON格式：{{\"title\": \"中文标题\", \"summary\": \"详细的中文摘要\"}}。原文标题: {title}，原文摘要: {snippet}"
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "response_format": {"type": "json_object"}}
    try:
        resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=20)
        res = resp.json()['choices'][0]['message']['content']
        return json.loads(res)
    except Exception as e:
        print("DeepSeek Error:", e)
        return {"title": title, "summary": snippet}

def run_cmd(cmd):
    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("STDERR:", res.stderr)
    return res.returncode

def run():
    raw_results = fetch_news()
    valid_news = []
    
    for r in raw_results:
        link = r.get('link', '')
        try:
            head = requests.head(link, timeout=5, allow_redirects=True, headers={'User-Agent': 'Mozilla/5.0'})
            if head.status_code not in [200, 301, 302, 307, 308, 403]:
                continue
        except:
            continue
            
        trans = translate_and_summarize(r['title'], r.get('snippet', ''))
        valid_news.append({
            "title": trans.get('title', r['title']),
            "summary": trans.get('summary', r.get('snippet', '')),
            "url": link,
            "source": r.get('source', ''),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "article_date": r.get('date', '')
        })
        if len(valid_news) >= 12: break

    if not valid_news:
        print("No valid news found.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    try:
        with open(DB_PATH) as f: db = json.load(f)
    except:
        db = {"last_updated": "", "news_by_date": {}}
        
    db["last_updated"] = datetime.now().isoformat()
    db["news_by_date"][today] = valid_news
    
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

    generate_html(today, valid_news)

    run_cmd(['git', '-C', REPO_DIR, 'add', '-A'])
    run_cmd(['git', '-C', REPO_DIR, 'commit', '-m', f'AI新闻日报自动更新: {today}'])
    run_cmd(['git', '-C', REPO_DIR, 'push'])

print("Auto News Script Ready!")
run()
