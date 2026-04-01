#!/usr/bin/env python3
"""
AI新闻每日简报邮件发送脚本 - 测试版（单收件人）
只发送给老板本人测试
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import sys
from datetime import datetime

def send_ai_news_email_test():
    """发送AI新闻每日简报邮件到单收件人（测试用）"""
    
    # 邮件配置
    sender = '86940135@qq.com'
    
    # 只发送给老板本人（两个邮箱都加，确保收到）
    receivers = [
        'jiyingguo@huawei.com',  # 华为邮箱
        # '86940135@qq.com'  # QQ邮箱（如果需要）
    ]
    
    # QQ邮箱授权码
    password = 'icxhfzuyzbhbbjie'
    
    # 获取动态日期
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')
    date_str_cn = today.strftime('%Y年%m月%d日')
    
    # 邮件主题（标注测试版）
    subject = f'【测试】[{date_str}] AI 新闻每日简报'
    
    # 读取HTML内容 - 多种可能的文件名格式
    possible_files = [
        f'/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{date_str}.html',
        f'/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today.strftime("%Y_%m_%d")}.html',
    ]
    
    html_file = None
    for f in possible_files:
        if os.path.exists(f):
            html_file = f
            break
    
    if not html_file:
        print(f"错误：找不到今天的新闻文件")
        print(f"搜索路径: {possible_files}")
        return False
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        print(f"成功读取HTML文件: {html_file}")
    except FileNotFoundError:
        print(f"错误：找不到文件 {html_file}")
        return False
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return False
    
    # 创建邮件
    message = MIMEMultipart('alternative')
    message['From'] = sender  # QQ邮箱要求纯地址格式
    message['To'] = ','.join(receivers)
    message['Subject'] = subject
    
    # 添加HTML版本
    html_part = MIMEText(html_content, 'html', 'utf-8')
    message.attach(html_part)
    
    # 添加纯文本版本（备用）
    text_content = f"""
AI 新闻每日简报 - {date_str_cn}（测试版）

详细内容请查看HTML版本邮件。
"""
    text_part = MIMEText(text_content, 'plain', 'utf-8')
    message.attach(text_part)
    
    try:
        # 连接SMTP服务器
        smtp_server = 'smtp.qq.com'
        smtp_port = 587
        
        print(f"正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port, timeout=30)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        
        # 发送邮件
        print(f"正在发送测试邮件到 {len(receivers)} 位收件人: {receivers}")
        server.sendmail(sender, receivers, message.as_string())
        server.quit()
        
        print(f"测试邮件发送成功！发送给: {receivers}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("SMTP认证失败：请检查邮箱和授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"SMTP错误：{e}")
        return False
    except Exception as e:
        print(f"发送邮件时出错：{e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("开始发送AI新闻每日简报（测试版 - 单收件人）...")
    print("=" * 60)
    success = send_ai_news_email_test()
    
    if success:
        print("=" * 60)
        print("测试邮件发送成功!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("=" * 60)
        print("测试邮件发送失败!")
        print("=" * 60)
        sys.exit(1)
