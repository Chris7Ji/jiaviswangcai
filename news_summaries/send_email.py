#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI新闻每日摘要邮件发送脚本
使用SMTP发送邮件
"""

import smtplib
import os
import sys
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# 配置
SMTP_SERVER = "smtp.qq.com"  # QQ邮箱SMTP服务器
SMTP_PORT = 587  # SSL端口
SENDER_EMAIL = "86940135@qq.com"  # 发件人邮箱
SENDER_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")  # 从环境变量获取邮箱密码/授权码

# 收件人列表
RECIPIENTS = [
    "86940135@qq.com",
    "jiyingguo@huawei.com"
]

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败 {filepath}: {e}")
        return None

def create_email_content(md_content, html_content):
    """创建邮件内容"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    # 创建多部分邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f'AI新闻每日摘要 - {today}'
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(RECIPIENTS)
    
    # 纯文本版本
    text_part = MIMEText(md_content, 'plain', 'utf-8')
    msg.attach(text_part)
    
    # HTML版本
    html_part = MIMEText(html_content, 'html', 'utf-8')
    msg.attach(html_part)
    
    return msg

def send_email(msg):
    """发送邮件"""
    try:
        print(f"正在连接SMTP服务器: {SMTP_SERVER}:{SMTP_PORT}")
        
        # 使用SSL连接（QQ邮箱需要）
        server = smtplib.SMTP_SSL(SMTP_SERVER, 465)
        
        if not SENDER_PASSWORD:
            print("错误: 未设置邮箱密码/授权码")
            print("请设置环境变量: export EMAIL_PASSWORD='your_password'")
            return False
        
        print(f"正在登录邮箱: {SENDER_EMAIL}")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        print(f"正在发送邮件到: {', '.join(RECIPIENTS)}")
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    """主函数"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 文件路径
    md_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.md"
    html_file = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.html"
    
    print("=" * 60)
    print("AI新闻每日摘要邮件发送系统")
    print("=" * 60)
    print(f"发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"发件人: {SENDER_EMAIL}")
    print(f"收件人: {', '.join(RECIPIENTS)}")
    print("=" * 60)
    
    # 检查文件是否存在
    if not os.path.exists(md_file):
        print(f"❌ 错误: Markdown文件不存在: {md_file}")
        sys.exit(1)
    
    if not os.path.exists(html_file):
        print(f"❌ 错误: HTML文件不存在: {html_file}")
        sys.exit(1)
    
    # 读取文件内容
    print("\n📖 正在读取新闻摘要文件...")
    md_content = read_file(md_file)
    html_content = read_file(html_file)
    
    if not md_content or not html_content:
        print("❌ 错误: 无法读取文件内容")
        sys.exit(1)
    
    print(f"✅ Markdown文件: {len(md_content)} 字符")
    print(f"✅ HTML文件: {len(html_content)} 字符")
    
    # 创建邮件
    print("\n📧 正在创建邮件...")
    msg = create_email_content(md_content, html_content)
    
    # 发送邮件
    print("\n📤 正在发送邮件...")
    success = send_email(msg)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 任务完成！")
        print(f"📄 Markdown文件: {md_file}")
        print(f"🌐 HTML文件: {html_file}")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("❌ 邮件发送失败")
        print("💡 提示: 请检查邮箱配置和授权码")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
