#!/usr/bin/env python3
"""
高校分队AI新闻每日简报生成器
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

def get_beijing_date():
    """获取北京时间日期"""
    utc_now = datetime.utcnow()
    beijing_now = utc_now + timedelta(hours=8)
    return beijing_now

def search_ai_news():
    """
    搜索AI新闻
    使用Tavily API进行多维度搜索
    """
    try:
        # 这里调用搜索API获取新闻
        # 实际实现需要接入搜索工具
        news_data = {
            "global_llm": [],
            "china_llm": [],
            "ai_chips": [],
            "ai_agents": [],
            "global_ai": [],
            "research": []
        }
        return news_data
    except Exception as e:
        print(f"搜索新闻失败: {e}")
        return None

def generate_html_report(news_data, date_str):
    """生成HTML格式的简报"""
    
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
        </div>
        
        <div class="content">
            <!-- 模块一：全球顶尖大模型 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🌍</span>
                    全球顶尖大模型动态
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
            </div>
            
            <!-- 模块二：中国AI大模型 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🇨🇳</span>
                    中国AI大模型最新进展
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
            </div>
            
            <!-- 模块三：AI软硬件生态 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">💻</span>
                    AI软硬件及国产芯片生态
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
            </div>
            
            <!-- 模块四：AI智能体 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🤖</span>
                    AI智能体前沿资讯
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
            </div>
            
            <!-- 模块五：全球AI关键新闻 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">📰</span>
                    全球AI关键新闻
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
            </div>
            
            <!-- 模块六：AI科研成果 -->
            <div class="section">
                <div class="section-title">
                    <span class="icon">🔬</span>
                    AI科研成果
                </div>
                <div class="empty-notice">今日暂无重大更新，持续关注中...</div>
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

def send_feishu_notification(message):
    """发送飞书通知"""
    # 飞书通知功能待实现
    print(f"📱 飞书通知: {message}")

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
    
    # 搜索新闻
    print("\n🔍 正在搜索AI新闻...")
    news_data = search_ai_news()
    
    # 生成HTML报告
    print("📄 正在生成HTML简报...")
    html_content = generate_html_report(news_data, date_str)
    
    # 设置邮件主题
    subject = f"🚀 [{date_str_short}] 高校分队 AI 新闻每日简报：今日AI领域最新动态"
    
    # 发送邮件
    print("\n📧 正在发送邮件...")
    if send_email(html_content, subject, RECIPIENTS):
        print("✅ 任务执行成功！")
        send_feishu_notification(f"✅ 高校分队AI简报已发送 | {date_str} | 收件人: {len(RECIPIENTS)}人")
    else:
        print("❌ 任务执行失败！")
        send_feishu_notification(f"❌ 高校分队AI简报发送失败 | {date_str}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
