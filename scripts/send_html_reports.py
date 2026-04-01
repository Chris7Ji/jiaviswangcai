#!/usr/bin/env python3
"""
发送HTML格式定时任务报告邮件
优化为易读版本，适合邮箱、飞书和手机APP阅读
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def read_report(file_path):
    """读取报告内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "报告内容读取失败"

def markdown_to_html(markdown_text, title):
    """将Markdown转换为优化HTML"""
    # 基础样式
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
                line-height: 1.8;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 28px;
                margin-bottom: 10px;
                font-weight: 600;
            }}
            .header .subtitle {{
                font-size: 14px;
                opacity: 0.9;
            }}
            .content {{
                padding: 30px;
            }}
            .news-item {{
                background: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
                transition: transform 0.2s;
            }}
            .news-item:hover {{
                transform: translateX(5px);
            }}
            .news-title {{
                font-size: 18px;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 10px;
            }}
            .news-content {{
                color: #4a5568;
                font-size: 15px;
                line-height: 1.7;
            }}
            .news-link {{
                display: inline-block;
                margin-top: 10px;
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
            }}
            .stats {{
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 12px;
                padding: 20px;
                margin: 20px 0;
            }}
            .stats h3 {{
                color: #2d3748;
                margin-bottom: 15px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
            }}
            .stat-item {{
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }}
            .stat-value {{
                font-size: 24px;
                font-weight: 700;
                color: #667eea;
            }}
            .stat-label {{
                font-size: 12px;
                color: #718096;
                margin-top: 5px;
            }}
            .footer {{
                background: #f7fafc;
                padding: 20px;
                text-align: center;
                color: #718096;
                font-size: 13px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            th {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                text-align: left;
                font-weight: 600;
            }}
            td {{
                padding: 12px 15px;
                border-bottom: 1px solid #e2e8f0;
            }}
            tr:hover {{
                background: #f7fafc;
            }}
            .badge {{
                display: inline-block;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 500;
            }}
            .badge-success {{
                background: #c6f6d5;
                color: #22543d;
            }}
            .badge-warning {{
                background: #feebc8;
                color: #744210;
            }}
            .highlight {{
                background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
                padding: 2px 6px;
                border-radius: 4px;
            }}
            @media (max-width: 600px) {{
                body {{ padding: 10px; }}
                .content {{ padding: 20px; }}
                .header h1 {{ font-size: 22px; }}
                .news-title {{ font-size: 16px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{title}</h1>
                <div class="subtitle">{datetime.now().strftime("%Y年%m月%d日")} | 旺财Jarvis 智能生成</div>
            </div>
            <div class="content">
    """
    
    # 简单Markdown转换
    lines = markdown_text.split('\n')
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 标题
        if line.startswith('# '):
            html_content += f"<h2 style='color:#2d3748;margin:25px 0 15px;font-size:22px;'>{line[2:]}</h2>"
        elif line.startswith('## '):
            html_content += f"<h3 style='color:#4a5568;margin:20px 0 10px;font-size:18px;'>{line[3:]}</h3>"
        elif line.startswith('### '):
            html_content += f"<h4 style='color:#718096;margin:15px 0 8px;font-size:16px;'>{line[4:]}</h4>"
        # 列表项
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list:
                html_content += "<ul style='margin:10px 0;padding-left:20px;'>"
                in_list = True
            content = line[2:]
            # 处理加粗
            content = content.replace('**', '<strong>').replace('**', '</strong>')
            html_content += f"<li style='margin:5px 0;color:#4a5568;'>{content}</li>"
        # 表格
        elif '|' in line and not line.startswith('|---'):
            if '<table>' not in html_content.split('<div class="content">')[-1]:
                html_content += "<table>"
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells:
                html_content += "<tr>"
                for cell in cells:
                    html_content += f"<td>{cell}</td>"
                html_content += "</tr>"
        # 普通段落
        else:
            if in_list:
                html_content += "</ul>"
                in_list = False
            if line.startswith('[') and '](' in line:
                # 链接
                text = line[line.find('[')+1:line.find(']')]
                url = line[line.find('(')+1:line.find(')')]
                html_content += f"<a href='{url}' class='news-link'>🔗 {text}</a>"
            elif line.startswith('**') and line.endswith('**'):
                # 加粗标题
                html_content += f"<div class='news-title'>{line[2:-2]}</div>"
            else:
                html_content += f"<p style='margin:10px 0;color:#4a5568;'>{line}</p>"
    
    if in_list:
        html_content += "</ul>"
    
    html_content += f"""
            </div>
            <div class="footer">
                <p>📧 本报告由 OpenClaw 大龙虾智能助手自动生成</p>
                <p>发送时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def send_html_email(subject, html_content, to_emails):
    """发送HTML邮件"""
    
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"
    sender_password = os.environ.get("QQ_EMAIL_PASSWORD", "")
    
    if not sender_password:
        print("❌ 错误：未设置QQ_EMAIL_PASSWORD")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        
        # 添加HTML内容
        msg.attach(MIMEText(html_content, 'html', 'utf-8'))
        
        # 发送
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ 邮件发送成功: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    
    # 报告配置
    reports = [
        {
            "title": "🤖 AI新闻摘要日报",
            "file": "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-18.md",
            "subject": "🤖 AI新闻摘要日报 - 2026年03月18日"
        },
        {
            "title": "📺 B站热门视频日报",
            "file": "/tmp/bilibili_report_2026-03-18.md",
            "subject": "📺 B站热门视频日报 - 2026年03月18日"
        },
        {
            "title": "📚 教育行业AI资讯日报",
            "file": "/tmp/education_ai_news_2026-03-18.md",
            "subject": "📚 教育行业AI资讯日报 - 2026年03月18日"
        },
        {
            "title": "📈 股票监控日报",
            "file": "/tmp/stock_report_2026-03-18.md",
            "subject": "📈 股票监控日报 - 2026年03月18日"
        },
        {
            "title": "📋 每日工作日报",
            "file": "/tmp/daily_report_2026-03-18.md",
            "subject": "📋 每日工作日报 - 2026年03月18日"
        }
    ]
    
    to_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    success_count = 0
    
    print("=" * 60)
    print("📧 发送HTML格式报告邮件")
    print("=" * 60)
    
    for i, report in enumerate(reports, 1):
        print(f"\n[{i}/5] 处理: {report['title']}")
        
        # 读取Markdown
        md_content = read_report(report['file'])
        
        # 转换为HTML
        html_content = markdown_to_html(md_content, report['title'])
        
        # 发送邮件
        if send_html_email(report['subject'], html_content, to_emails):
            success_count += 1
            # 保存HTML文件
            html_file = report['file'].replace('.md', '.html')
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"   💾 HTML已保存: {html_file}")
    
    print("\n" + "=" * 60)
    print(f"✅ 发送完成: {success_count}/{len(reports)} 封邮件")
    print("=" * 60)

if __name__ == "__main__":
    main()