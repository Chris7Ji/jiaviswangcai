#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的邮件发送脚本
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_simple_email():
    """发送简单的文本邮件"""
    
    # QQ邮箱配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465  # 使用SSL端口
    sender_email = "86940135@qq.com"
    password = "gD4UHVCn5E6nG3f"  # QQ邮箱授权码
    
    # 收件人
    receivers = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 读取邮件内容
    with open("/Users/jiyingguo/.openclaw/workspace/news_summaries/email_body_2026-03-05.txt", "r", encoding="utf-8") as f:
        email_content = f.read()
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receivers)
    msg['Subject'] = f"AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}"
    
    # 添加正文
    msg.attach(MIMEText(email_content, 'plain', 'utf-8'))
    
    try:
        # 使用SSL连接
        print("正在连接QQ邮箱SMTP服务器 (SSL)...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)  # 显示调试信息
        
        print("正在登录邮箱...")
        server.login(sender_email, password)
        
        print("正在发送邮件...")
        server.sendmail(sender_email, receivers, msg.as_string())
        
        print("✅ 邮件发送成功！")
        server.quit()
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    send_simple_email()