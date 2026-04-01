#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用新授权码发送邮件
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

def send_email_with_new_auth():
    """使用新授权码发送邮件"""
    
    # 新授权码
    NEW_AUTH_CODE = "swqfjvmoupdebhgh"
    
    # QQ邮箱配置
    smtp_server = "smtp.qq.com"
    smtp_port = 465  # SSL端口
    sender_email = "86940135@qq.com"
    password = NEW_AUTH_CODE
    
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
    
    print(f"📧 使用新授权码发送邮件...")
    print(f"发件人: {sender_email}")
    print(f"收件人: {', '.join(receivers)}")
    print(f"主题: AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}")
    
    try:
        # 使用SSL连接
        print("正在连接QQ邮箱SMTP服务器 (SSL 465)...")
        server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=30)
        
        print("正在登录邮箱...")
        server.login(sender_email, password)
        
        print("正在发送邮件...")
        server.sendmail(sender_email, receivers, msg.as_string())
        
        print("✅ 邮件发送成功！")
        server.quit()
        
        # 更新MEMORY.md中的授权码
        update_memory_auth_code(NEW_AUTH_CODE)
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def update_memory_auth_code(new_code):
    """更新MEMORY.md中的授权码"""
    try:
        with open("/Users/jiyingguo/.openclaw/workspace/MEMORY.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 替换旧的授权码
        old_code = "gD4UHVCn5E6nG3f"
        if old_code in content:
            content = content.replace(old_code, new_code)
            with open("/Users/jiyingguo/.openclaw/workspace/MEMORY.md", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 已更新MEMORY.md中的授权码: {old_code} → {new_code}")
        else:
            # 直接添加新授权码记录
            with open("/Users/jiyingguo/.openclaw/workspace/MEMORY.md", "a", encoding="utf-8") as f:
                f.write(f"\n## 2026-03-05 邮箱授权码更新\n")
                f.write(f"- **新QQ邮箱授权码**: `{new_code}` (更新于 {datetime.now().strftime('%Y-%m-%d %H:%M')})\n")
            print(f"✅ 已添加新授权码到MEMORY.md")
            
    except Exception as e:
        print(f"⚠️ 更新MEMORY.md失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("开始使用新授权码发送今日AI新闻")
    print("=" * 60)
    
    if send_email_with_new_auth():
        print("\n" + "=" * 60)
        print("🎉 邮件发送成功！")
        print("=" * 60)
        print(f"✅ 新闻已发送到: 86940135@qq.com, jiyingguo@huawei.com")
        print(f"✅ 授权码已更新到MEMORY.md")
        print(f"✅ 发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("\n" + "=" * 60)
        print("😞 邮件发送失败")
        print("=" * 60)
        print("请检查：")
        print("1. QQ邮箱SMTP服务是否开启")
        print("2. 授权码是否正确")
        print("3. 网络连接是否正常")