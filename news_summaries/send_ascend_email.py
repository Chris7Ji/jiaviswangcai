#!/usr/bin/env python3
"""
发送华为昇腾新闻摘要到指定邮箱
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
        return None

def send_ascend_email():
    """发送华为昇腾新闻邮件"""
    # 邮件配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    sender_email = "86940135@qq.com"
    sender_password = os.getenv("EMAIL_PASSWORD") or os.getenv("QQ_EMAIL_PASSWORD")
    
    if not sender_password:
        print("错误: 请设置EMAIL_PASSWORD或QQ_EMAIL_PASSWORD环境变量")
        return False
    
    # 收件人列表
    receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 获取今天的日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    date_str_cn = today.strftime('%Y年%m月%d日')
    
    news_dir = "/Users/jiyingguo/.openclaw/workspace/news_summaries"
    
    # 读取华为昇腾新闻
    ascend_md_file = f"{news_dir}/ascend_news_{date_str}.md"
    ascend_html_file = f"{news_dir}/ascend_news_{date_str}.html"
    ascend_md_content = read_file_content(ascend_md_file)
    ascend_html_content = read_file_content(ascend_html_file)
    
    if not ascend_md_content:
        print(f"错误: 今天的新闻文件不存在 ({date_str})")
        return False
    
    print(f"✅ 华为昇腾新闻已找到")
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = Header(f"🔥 华为昇腾每日新闻 - {date_str_cn}", 'utf-8')
    
    # 构建邮件正文 - Markdown格式
    md_body = f"""# 🔥 华为昇腾每日新闻 - {date_str_cn}

---

{ascend_md_content}

---

*发送时间: {today.strftime('%Y-%m-%d %H:%M:%S')}*
*由旺财AI助手自动生成*
"""
    
    # 构建邮件正文 - HTML格式
    html_body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>华为昇腾每日新闻 - {date_str_cn}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #CF0A2C; border-bottom: 3px solid #CF0A2C; padding-bottom: 15px; margin-bottom: 30px; }}
        h2 {{ color: #2c5aa0; margin-top: 40px; border-left: 4px solid #CF0A2C; padding-left: 15px; background: #f8f9fa; padding: 10px 15px; }}
        h3 {{ color: #444; margin-top: 25px; }}
        .section {{ margin: 30px 0; }}
        .divider {{ border: none; border-top: 2px solid #e0e0e0; margin: 40px 0; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 50px; text-align: center; padding-top: 20px; border-top: 1px solid #e0e0e0; }}
        a {{ color: #CF0A2C; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; font-size: 14px; }}
        pre {{ background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; border-left: 3px solid #CF0A2C; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 15px; color: #666; margin: 15px 0; background: #f9f9f9; padding: 10px 15px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 10px; text-align: left; }}
        th {{ background: #f8f9fa; font-weight: bold; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        .emoji {{ font-size: 1.2em; }}
        .highlight {{ background: #fff3cd; padding: 15px; border-radius: 5px; border-left: 4px solid #ffc107; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1><span class="emoji">🔥</span> 华为昇腾每日新闻</h1>
        <p style="color: #666; font-size: 14px; margin-top: -10px;">{date_str_cn}</p>
        
        <div class="section">
            {ascend_html_content if ascend_html_content else ascend_md_content.replace(chr(10), '<br>')}
        </div>
        
        <hr class="divider">
        
        <div class="footer">
            <p>发送时间: {today.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p>由旺财AI助手自动生成</p>
        </div>
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
        server.starttls()
        print("正在登录邮箱...")
        server.login(sender_email, sender_password)
        print("正在发送邮件...")
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        print(f"✅ 邮件发送成功! 收件人: {receiver_emails}")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("开始发送华为昇腾新闻摘要邮件...")
    print("=" * 60)
    if send_ascend_email():
        print("=" * 60)
        print("✅ 邮件发送任务完成!")
        print("=" * 60)
    else:
        print("=" * 60)
        print("❌ 邮件发送任务失败!")
        print("=" * 60)
