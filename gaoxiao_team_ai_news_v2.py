#!/usr/bin/env python3
"""
高校分队AI新闻每日简报生成器 - 真实新闻版本
定时任务：每天 06:15 (北京时间)
"""

import os
import sys
import json
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# 收件人列表
RECIPIENTS = [
    "qinhongyi2@huawei.com",
    "tiankunyang@huawei.com", 
    "jiawei18@huawei.com",
    "jiyingguo@huawei.com",
    "linfeng67@huawei.com",
    "liuwei44259@huawei.com",
    "lvluling1@huawei.com",
    "suqi1@huawei.com",
    "susha@huawei.com",
    "wangdongxiao@huawei.com",
    "xiongguifang@huawei.com",
    "xushengsheng@huawei.com",
    "zhangqianfeng2@huawei.com",
    "zhangyexing2@huawei.com"
]

# 邮件配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_PASSWORD = "icxhfzuyzbhbbjie"

# Tavily API配置
TAVILY_API_KEY = "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"

def get_beijing_date():
    """获取北京时间日期"""
    from datetime import timezone
    utc_now = datetime.now(timezone.utc)
    beijing_now = utc_now + timedelta(hours=8)
    return beijing_now

def search_with_tavily(query, max_results=5):
    """使用Tavily API搜索新闻"""
    try:
        url = "https://api.tavily.com/search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {TAVILY_API_KEY}"
        }
        data = {
            "query": query,
            "search_depth": "advanced",
            "max_results": max_results,
            "time_range": "day"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Tavily搜索失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"搜索出错: {e}")
        return None

def collect_all_news():
    """收集所有模块的新闻"""
    news_data = {
        "global_llm": [],
        "china_llm": [],
        "ai_chips": [],
        "ai_agents": [],
        "global_ai": [],
        "research": []
    }
    
    print("🔍 正在搜索全球顶尖大模型动态...")
    # OpenAI相关
    result = search_with_tavily("OpenAI GPT-4 ChatGPT latest news", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["global_llm"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "OpenAI/Google/Anthropic"
            })
    
    print("🔍 正在搜索中国AI大模型进展...")
    # 中国大模型
    result = search_with_tavily("Kimi Moonshot 智谱AI ChatGLM DeepSeek 最新动态", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["china_llm"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "中国AI"
            })
    
    print("🔍 正在搜索AI芯片动态...")
    # AI芯片
    result = search_with_tavily("华为昇腾 AI芯片 NVIDIA 英伟达 最新", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["ai_chips"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "AI芯片"
            })
    
    print("🔍 正在搜索AI智能体资讯...")
    # AI Agent
    result = search_with_tavily("AI Agent 智能体 OpenClaw 最新进展", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["ai_agents"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "AI Agent"
            })
    
    print("🔍 正在搜索全球AI关键新闻...")
    # 全球AI新闻
    result = search_with_tavily("artificial intelligence AI latest news today", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["global_ai"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "全球AI"
            })
    
    print("🔍 正在搜索AI科研成果...")
    # AI科研
    result = search_with_tavily("AI research breakthrough machine learning paper 2026", 3)
    if result and 'results' in result:
        for item in result['results'][:2]:
            news_data["research"].append({
                "title": item.get('title', ''),
                "summary": item.get('content', '')[:100] + '...' if len(item.get('content', '')) > 100 else item.get('content', ''),
                "url": item.get('url', ''),
                "source": "AI科研"
            })
    
    return news_data

def generate_news_html(news_list, empty_msg="今日暂无重大更新，持续关注中..."):
    """生成新闻列表的HTML"""
    if not news_list:
        return f'<div class="empty-notice">{empty_msg}</div>'
    
    html = ""
    for news in news_list:
        html += f'''
        <div class="news-item">
            <div class="news-title">{news.get('title', '')}</div>
            <div class="news-summary">{news.get('summary', '')}</div>
            <a href="{news.get('url', '#')}" class="news-link" target="_blank">[阅读原文]</a>
        </div>
        '''
    return html

def generate_html_report(news_data, date_str):
    """生成HTML格式的简报"""
    
    # 统计新闻总数
    total_news = sum(len(v) for v in news_data.values())
    
    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>高校分队AI新闻每日简报</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
        }}
        .header .date {{
            margin-top: 10px;
            font-size: 16px;
            opacity: 0.9;
        }}
        .header .stats {{
            margin-top: 15px;
            font-size: 14px;
            opacity: 0.8;
            background: rgba(255,255,255,0.1);
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 30px;
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 700;
            color: #1e3c72;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            display: flex;
            align-items: center;
        }}
        .section-title .icon {{
            margin-right: 10px;
            font-size: 24px;
        }}
        .news-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }}
        .news-item:hover {{
            transform: translateX(5px);
        }}
        .news-title {{
            font-size: 16px;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .news-summary {{
            font-size: 14px;
            color: #5a6c7d;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        .news-link {{
            font-size: 13px;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }}
        .news-link:hover {{
            text-decoration: underline;
        }}
        .empty-notice {{
            text-align: center;
            color: #95a5a6;
            font-style: italic;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 高校分队 AI 新闻每日简报</h1>
            <div class="date">{date_str} | 北京时间</div>
            <div class="stats">📊 今日精选 {total_news} 条新闻</div>
        </div>
        
        <div class="content">
            <!-- 模块一：全球顶尖大模型 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🌍</span>
                    全球顶尖大模型动态
                </div>
                {generate_news_html(news_data.get('global_llm', []))}
            </div>
            
            <!-- 模块二：中国AI大模型 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🇨🇳</span>
                    中国AI大模型最新进展
                </div>
                {generate_news_html(news_data.get('china_llm', []))}
            </div>
            
            <!-- 模块三：AI软硬件生态 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">💻</span>
                    AI软硬件及国产芯片生态
                </div>
                {generate_news_html(news_data.get('ai_chips', []))}
            </div>
            
            <!-- 模块四：AI智能体 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🤖</span>
                    AI智能体前沿资讯
                </div>
                {generate_news_html(news_data.get('ai_agents', []))}
            </div>
            
            <!-- 模块五：全球AI关键新闻 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">📰</span>
                    全球AI关键新闻
                </div>
                {generate_news_html(news_data.get('global_ai', []))}
            </div>
            
            <!-- 模块六：AI科研成果 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🔬</span>
                    AI科研成果
                </div>
                {generate_news_html(news_data.get('research', []))}
            </div>
        </div>
        
        <div class="footer">
            <p>高校分队 AI 新闻每日简报 | 自动生成</p>
            <p>如有问题请联系：旺财Jarvis</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def send_email(html_content, subject, recipients):
    """发送邮件"""
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(recipients)
        msg['Subject'] = subject
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 连接SMTP服务器并发送
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件发送成功！收件人: {len(recipients)}人")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 高校分队AI新闻每日简报生成器")
    print("=" * 60)
    
    # 获取当前日期
    beijing_now = get_beijing_date()
    date_str = beijing_now.strftime("%Y年%m月%d日")
    date_str_short = beijing_now.strftime("%m月%d日")
    
    print(f"\n📅 当前日期: {date_str}")
    print(f"👥 收件人数量: {len(RECIPIENTS)}人")
    
    # 收集新闻
    print("\n🔍 开始收集AI新闻...")
    news_data = collect_all_news()
    
    # 统计新闻总数
    total_news = sum(len(v) for v in news_data.values())
    print(f"\n📊 共收集到 {total_news} 条新闻")
    
    # 生成HTML报告
    print("📄 正在生成HTML简报...")
    html_content = generate_html_report(news_data, date_str)
    
    # 设置邮件主题
    # 找出最重磅的新闻作为副标题
    top_news = None
    for module_news in news_data.values():
        if module_news:
            top_news = module_news[0]
            break
    
    if top_news:
        subtitle = top_news.get('title', '今日AI领域最新动态')[:30] + '...'
    else:
        subtitle = "今日AI领域最新动态"
    
    subject = f"🚀 [{date_str_short}] 高校分队 AI 新闻每日简报：{subtitle}"
    
    # 发送邮件
    print("\n📧 正在发送邮件...")
    if send_email(html_content, subject, RECIPIENTS):
        print("✅ 任务执行成功！")
    else:
        print("❌ 任务执行失败！")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
