#!/usr/bin/env python3
# 测试邮件发送功能

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_test_email():
    # QQ邮箱SMTP配置
    smtp_server = "smtp.qq.com"
    smtp_port = 587  # 或 465 for SSL
    sender_email = "86940135@qq.com"
    # 使用授权码，不是邮箱密码
    password = "ngjkdlyvxlqpbhej"  # Boss提供的授权码
    receiver_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 创建邮件内容
    subject = "OpenClaw AI新闻摘要 - 邮件功能测试"
    body = """
    <html>
    <body>
        <h2>✅ 邮件发送功能测试成功！</h2>
        <p>这是来自OpenClaw的测试邮件，用于验证邮件发送功能。</p>
        <p><strong>测试信息：</strong></p>
        <ul>
            <li>发件人：86940135@qq.com</li>
            <li>收件人：86940135@qq.com, jiyingguo@huawei.com</li>
            <li>时间：2026-02-13 23:00</li>
            <li>状态：测试中</li>
        </ul>
        <p>如果收到此邮件，说明邮件发送功能配置成功。</p>
        <p>明天早上6:30将开始发送AI新闻每日摘要。</p>
        <hr>
        <p><em>OpenClaw AI助手 - Jarvis</em></p>
    </body>
    </html>
    """
    
    try:
        # 创建MIME消息
        msg = MIMEMultipart("alternative")
        msg["From"] = sender_email
        msg["To"] = ", ".join(receiver_emails)
        msg["Subject"] = subject
        
        # 添加HTML内容
        html_part = MIMEText(body, "html")
        msg.attach(html_part)
        
        print(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        
        # 连接SMTP服务器并发送邮件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # 启用TLS加密
            print("TLS加密已启用")
            
            print(f"正在登录邮箱: {sender_email}")
            server.login(sender_email, password)
            print("登录成功")
            
            print(f"正在发送邮件到: {receiver_emails}")
            server.sendmail(sender_email, receiver_emails, msg.as_string())
            print("✅ 邮件发送成功！")
            
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        print("\n可能的原因：")
        print("1. QQ邮箱授权码错误")
        print("2. 未开启SMTP服务")
        print("3. 网络连接问题")
        print("4. 防火墙阻止")
        return False

if __name__ == "__main__":
    print("开始测试邮件发送功能...")
    success = send_test_email()
    sys.exit(0 if success else 1)