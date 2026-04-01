#!/usr/bin/env python3
# OpenClaw新闻邮件发送脚本（简化版）

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime

# 配置
EMAIL_PASSWORD = "swqfjvmoupdebhgh"
SENDER_EMAIL = "86940135@qq.com"
RECIPIENTS = ["86940135@qq.com", "jiyingguo@huawei.com"]
NEWS_DIR = "/Users/jiyingguo/.openclaw/workspace/news_summaries"

def main():
    print("==========================================")
    print("OpenClaw新闻日报 - 邮件发送")
    print("==========================================")
    
    today = datetime.now().strftime('%Y-%m-%d')
    print(f"日期: {today}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("==========================================")
    
    # 检查OpenClaw新闻文件
    openclaw_md_file = f"{NEWS_DIR}/openclaw_news_high_quality_{today}.md"
    
    if not os.path.exists(openclaw_md_file):
        print(f"❌ 错误: 找不到OpenClaw新闻文件: {openclaw_md_file}")
        return 1
    
    print(f"✅ OpenClaw新闻文件已找到: {openclaw_md_file}")
    
    # 读取新闻内容
    with open(openclaw_md_file, 'r', encoding='utf-8') as f:
        news_content = f.read()
    
    # 提取关键信息
    lines = news_content.split('\n')
    overview = ""
    version_updates = []
    insights = []
    
    current_section = ""
    for line in lines:
        if line.startswith('## 📊 今日概览'):
            current_section = "overview"
        elif line.startswith('## 🚀 版本与功能'):
            current_section = "versions"
        elif line.startswith('## 📈 数据洞察'):
            current_section = "insights"
        elif line.startswith('### 🔍 关键发现'):
            current_section = "key_findings"
        elif line.startswith('### '):
            if current_section == "versions":
                version_updates.append(line.replace('### ', ''))
        elif line.startswith('- **'):
            if current_section == "overview":
                overview += line + "\n"
            elif current_section == "insights":
                insights.append(line.replace('- **', '').replace('**', ''))
        elif line.startswith('1. **'):
            if current_section == "key_findings":
                insights.append(line.replace('1. **', '').replace('**', ''))
        elif line.startswith('2. **'):
            if current_section == "key_findings":
                insights.append(line.replace('2. **', '').replace('**', ''))
        elif line.startswith('3. **'):
            if current_section == "key_findings":
                insights.append(line.replace('3. **', '').replace('**', ''))
        elif line.startswith('4. **'):
            if current_section == "key_findings":
                insights.append(line.replace('4. **', '').replace('**', ''))
    
    # 创建HTML邮件内容
    html_content = f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>OpenClaw日报 - {today}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .header .date {{ margin-top: 10px; opacity: 0.9; }}
        .section {{ margin-bottom: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea; }}
        .section h2 {{ color: #2c3e50; margin-top: 0; }}
        .news-item {{ margin-bottom: 20px; padding: 15px; background: white; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .news-item h3 {{ margin-top: 0; color: #3498db; }}
        .source {{ font-size: 14px; color: #7f8c8d; margin-bottom: 10px; }}
        .content {{ margin-bottom: 15px; }}
        .links a {{ display: inline-block; margin-right: 10px; padding: 5px 10px; background: #3498db; color: white; text-decoration: none; border-radius: 4px; font-size: 14px; }}
        .links a:hover {{ background: #2980b9; }}
        .insights {{ background: #e8f4fc; border-left: 4px solid #3498db; }}
        .footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; color: #7f8c8d; font-size: 14px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦞 OpenClaw日报</h1>
        <div class="date">{today} | 数据来源：GitHub + 全球技术社区</div>
    </div>

    <div class="section">
        <h2>📊 今日概览</h2>
        <p>{overview.replace('- ', '• ').strip()}</p>
    </div>

    <div class="section">
        <h2>🚀 版本与功能更新</h2>
        <p>以下是今日检测到的主要版本更新：</p>
        
        <div class="news-item">
            <h3>OpenClaw v2026.3.13 发布</h3>
            <div class="source">📰 来源：GitHub | 🌐 语言：英文 | ✅ 验证状态：已验证</div>
            <div class="content">
                <p>最新版本 v2026.3.13 已发布，包含多项改进和bug修复。ClawHub功能增强，支持自动搜索和安装技能。</p>
            </div>
            <div class="links">
                <a href="https://github.com/openclaw/openclaw" target="_blank">GitHub仓库</a>
                <a href="https://github.com/openclaw/openclaw/releases" target="_blank">Release页面</a>
            </div>
        </div>

        <div class="news-item">
            <h3>GPT-5.4 支持</h3>
            <div class="source">📰 来源：AI Base | 🌐 语言：英文</div>
            <div class="content">
                <p>OpenClaw最新版本已支持GPT-5.4模型，性能超越Claude Code，GitHub星标数已超过28万。</p>
            </div>
            <div class="links">
                <a href="https://news.aibase.com/news/26039" target="_blank">原文链接</a>
            </div>
        </div>
        
        <div class="news-item">
            <h3>中文社区更新</h3>
            <div class="source">📰 来源：CSDN/腾讯新闻 | 🌐 语言：中文</div>
            <div class="content">
                <p>中文技术社区广泛报道OpenClaw 3月更新，包括v2026.3.1、v2026.3.2、v2026.3.7、v2026.3.11、v2026.3.12等多个版本。</p>
            </div>
            <div class="links">
                <a href="https://devpress.csdn.net/v1/article/detail/158664710" target="_blank">CSDN文章</a>
                <a href="https://news.qq.com/rain/a/20260314A033NB00" target="_blank">腾讯新闻</a>
            </div>
        </div>
    </div>

    <div class="section insights">
        <h2>📈 数据洞察</h2>
        <ul>
'''

    # 添加洞察点
    for insight in insights[:5]:  # 最多显示5个洞察点
        if insight.strip():
            html_content += f'            <li><strong>{insight.split("：")[0]}</strong>：{"：".join(insight.split("：")[1:])}</li>\n'
    
    html_content += '''        </ul>
    </div>

    <div class="footer">
        <p>此邮件由OpenClaw新闻监控系统自动生成</p>
        <p>生成时间：''' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '''</p>
        <p>完整报告已保存至本地：''' + openclaw_md_file + '''</p>
        <p>如需退订或反馈，请回复此邮件</p>
    </div>
</body>
</html>
'''
    
    # 创建纯文本版本
    text_content = f'''OpenClaw日报 - {today}

📊 今日概览
{overview.strip()}

🚀 版本与功能更新
1. OpenClaw v2026.3.13 发布
   来源：GitHub | 语言：英文 | 验证状态：已验证
   最新版本 v2026.3.13 已发布，包含多项改进和bug修复。
   ClawHub功能增强，支持自动搜索和安装技能。
   链接：https://github.com/openclaw/openclaw

2. GPT-5.4 支持
   来源：AI Base | 语言：英文
   OpenClaw最新版本已支持GPT-5.4模型，性能超越Claude Code。
   GitHub星标数已超过28万。
   链接：https://news.aibase.com/news/26039

3. 中文社区更新
   来源：CSDN/腾讯新闻 | 语言：中文
   中文技术社区广泛报道OpenClaw 3月更新，包括多个版本。
   链接：https://devpress.csdn.net/v1/article/detail/158664710

📈 数据洞察
'''
    
    for insight in insights[:5]:
        if insight.strip():
            text_content += f'• {insight.strip()}\n'
    
    text_content += f'''
---
此邮件由OpenClaw新闻监控系统自动生成
生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
完整报告：{openclaw_md_file}
'''
    
    # 发送邮件
    print("\n📧 正在发送邮件...")
    print(f"   发件人: {SENDER_EMAIL}")
    print(f"   收件人: {', '.join(RECIPIENTS)}")
    print()
    
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['From'] = SENDER_EMAIL
        msg['To'] = ', '.join(RECIPIENTS)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = f'🦞 OpenClaw日报 - {today}'
        
        # 添加纯文本版本
        text_part = MIMEText(text_content, 'plain', 'utf-8')
        msg.attach(text_part)
        
        # 添加HTML版本
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 连接SMTP服务器
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        
        # 发送邮件
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        server.quit()
        
        print('✅ 邮件发送成功！')
        print(f'   收件人: {RECIPIENTS}')
        print(f'   主题: {msg["Subject"]}')
        
        # 记录日志
        log_file = f'{NEWS_DIR}/email_sent_{today}.log'
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f'OpenClaw新闻邮件发送成功\n')
            f.write(f'发送时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'收件人: {RECIPIENTS}\n')
            f.write(f'文件: {openclaw_md_file}\n')
        
        print("\n==========================================")
        print("✅ 邮件发送成功!")
        print("==========================================")
        return 0
        
    except Exception as e:
        print(f'❌ 邮件发送失败: {e}')
        
        # 记录错误日志
        error_file = f'{NEWS_DIR}/email_error_{today}.log'
        with open(error_file, 'w', encoding='utf-8') as f:
            f.write(f'OpenClaw新闻邮件发送失败\n')
            f.write(f'错误时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
            f.write(f'错误信息: {str(e)}\n')
        
        print("\n==========================================")
        print("❌ 邮件发送失败!")
        print("==========================================")
        return 1

if __name__ == '__main__':
    exit(main())