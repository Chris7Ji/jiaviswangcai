#!/usr/bin/env python3
"""
发送AI新闻摘要到指定邮箱
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
    
    # 读取报告内容
    md_file = "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-05.md"
    html_file = "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-05.html"
    
    md_content = read_file_content(md_file)
    html_content = read_file_content(html_file)
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_emails)
    msg['Subject'] = Header(f"AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}", 'utf-8')
    
    # 创建纯文本版本
    text_part = MIMEText(md_content, 'plain', 'utf-8')
    
    # 创建HTML版本
    html_part = MIMEText(html_content, 'html', 'utf-8')
    
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
        print(f"邮件发送成功! 收件人: {receiver_emails}")
        return True
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("开始发送AI新闻摘要邮件...")
    if send_email():
        print("邮件发送任务完成!")
    else:
        print("邮件发送任务失败!")