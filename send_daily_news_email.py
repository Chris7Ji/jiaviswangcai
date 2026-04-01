#!/usr/bin/env python3
"""
发送AI新闻和OpenClaw新闻摘要到指定邮箱
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
from datetime import datetime

def read_file_content(file_path):
    """读取文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败: {str(e)}"

def send_email():
    """发送邮件"""
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"  # 发送者邮箱
    sender_password = os.getenv("QQ_EMAIL_PASSWORD")  # 从环境变量获取密码
    
    if not sender_password:
        print("错误: 请设置QQ_EMAIL_PASSWORD环境变量")
        return False
    
    # 收件人列表
    receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 获取今天的日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    date_str_cn = today.strftime('%Y年%m月%d日')
    
    # 读取AI新闻报告内容
    ai_md_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{date_str}.md"
    ai_html_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{date_str}.html"
    
    # 读取OpenClaw新闻报告内容
    openclaw_md_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/openclaw_news_high_quality_{date_str}.md"
    
    ai_md_content = read_file_content(ai_md_file)
    ai_html_content = read_file_content(ai_html_file)
    openclaw_md_content = read_file_content(openclaw_md_file)
    
    # 检查文件是否存在
    ai_exists = os.path.exists(ai_md_file)
    openclaw_exists = os.path.exists(openclaw_md_file)
    
    if not ai_exists and not openclaw_exists:
        print(f"错误: 今天的新闻文件都不存在 ({date_str})")
        return False
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = Header(f"AI与OpenClaw新闻摘要 - {date_str_cn}", 'utf-8')
    
    # 构建邮件正文 - Markdown格式
    md_body = f"""# AI与OpenClaw新闻摘要 - {date_str_cn}

---

"""
    
    if openclaw_exists:
        md_body += f"""## 🤖 OpenClaw每日新闻

{openclaw_md_content}

---

"""
    
    if ai_exists:
        md_body += f"""## 📰 AI行业新闻

{ai_md_content}

---

"""
    
    md_body += f"""
*发送时间: {today.strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    # 构建邮件正文 - HTML格式
    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI与OpenClaw新闻摘要 - {date_str_cn}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
        h2 {{ color: #2c5aa0; margin-top: 30px; border-left: 4px solid #1a73e8; padding-left: 10px; }}
        h3 {{ color: #444; }}
        .section {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }}
        .divider {{ border: none; border-top: 1px solid #ddd; margin: 30px 0; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 40px; text-align: center; }}
        a {{ color: #1a73e8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 15px; color: #666; margin: 15px 0; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background: #f8f9fa; }}
    </style>
</head>
<body>
    <h1>🤖 AI与OpenClaw新闻摘要</h1>
    <p style="color: #666; font-size: 14px;">{date_str_cn}</p>
    
    <hr class="divider">
"""
    
    if openclaw_exists:
        # 将Markdown转换为简单的HTML（这里简化处理）
        openclaw_html = openclaw_md_content.replace('\n\n', '</p><p>').replace('\n', '<br>')
        openclaw_html = f"<p>{openclaw_html}</p>"
        
        html_body += f"""
    <div class="section">
        <h2>🦞 OpenClaw每日新闻</h2>
        {openclaw_html}
    </div>
    
    <hr class="divider">
"""
    
    if ai_exists:
        html_body += f"""
    <div class="section">
        <h2>📰 AI行业新闻</h2>
        {ai_html_content if ai_html_content else ai_md_content.replace(chr(10), '<br>')}
    </div>
    
    <hr class="divider">
"""
    
    html_body += f"""
    <div class="footer">
        <p>发送时间: {today.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>
"""
    
    # 创建纯文本版本
    text_part = MIMEText(md_body, 'plain', 'utf-8')
    
    # 创建HTML版本
    html_part = MIMEText(html_body, 'html', 'utf-8')
    
    # 添加两个版本到邮件
    msg.attach(text_part)
    msg.attach(html_part)
    
    try:
        # 连接SMTP服务器并发送邮件
        print(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        print("正在登录邮箱...")
        server.login(sender_email, sender_password)
        print("正在发送邮件...")
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        print(f"✅ 邮件发送成功! 收件人: {receiver_emails}")
        
        # 记录发送日志
        log_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/email_sent_{date_str}.log"
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"邮件发送成功\n")
            f.write(f"发送时间: {today.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"收件人: {' '.join(receiver_emails)}\n")
            if openclaw_exists:
                f.write(f"OpenClaw新闻: {openclaw_md_file}\n")
            if ai_exists:
                f.write(f"AI新闻: {ai_md_file}\n")
        
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("开始发送AI与OpenClaw新闻摘要邮件...")
    print("=" * 60)
    if send_email():
        print("=" * 60)
        print("✅ 邮件发送任务完成!")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ 邮件发送任务失败!")
        print("=" * 60)
