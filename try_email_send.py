#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试使用不同设置的邮件发送
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def try_send_email():
    """尝试发送邮件"""
    
    # 配置
    sender_email = "86940135@qq.com"
    password = "gD4UHVCn5E6nG3f"
    receivers = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 读取邮件内容
    with open("/Users/jiyingguo/.openclaw/workspace/news_summaries/email_body_2026-03-05.txt", "r", encoding="utf-8") as f:
        email_content = f.read()
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(receivers)
    msg['Subject'] = f"AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}"
    msg.attach(MIMEText(email_content, 'plain', 'utf-8'))
    
    print("尝试方案1: SMTP SSL (端口465)...")
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=10)
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("✅ 方案1成功！")
        return True
    except Exception as e:
        print(f"❌ 方案1失败: {e}")
    
    print("\n尝试方案2: SMTP TLS (端口587)...")
    try:
        server = smtplib.SMTP("smtp.qq.com", 587, timeout=10)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("✅ 方案2成功！")
        return True
    except Exception as e:
        print(f"❌ 方案2失败: {e}")
    
    print("\n尝试方案3: SMTP普通 (端口25)...")
    try:
        server = smtplib.SMTP("smtp.qq.com", 25, timeout=10)
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("✅ 方案3成功！")
        return True
    except Exception as e:
        print(f"❌ 方案3失败: {e}")
    
    print("\n尝试方案4: 使用smtp.exmail.qq.com (企业邮箱服务器)...")
    try:
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465, timeout=10)
        server.login(sender_email, password)
        server.sendmail(sender_email, receivers, msg.as_string())
        server.quit()
        print("✅ 方案4成功！")
        return True
    except Exception as e:
        print(f"❌ 方案4失败: {e}")
    
    return False

if __name__ == "__main__":
    print("开始尝试发送邮件...")
    if try_send_email():
        print("\n🎉 邮件发送成功！")
    else:
        print("\n😞 所有方案都失败了，需要检查QQ邮箱设置。")

if __name__ == "__main__":
    try_send_email()