#!/usr/bin/env python3
"""
自动化邮件搜索脚本
使用前请设置环境变量
"""

import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta

def search_qq_emails():
    """搜索QQ邮箱"""
    try:
        # 从环境变量获取配置
        username = os.getenv('QQ_EMAIL')
        password = os.getenv('QQ_APP_PASSWORD')
        
        if not username or not password:
            print("❌ 请设置QQ_EMAIL和QQ_APP_PASSWORD环境变量")
            return []
        
        # 连接到QQ邮箱
        print("🔗 连接到QQ邮箱...")
        mail = imaplib.IMAP4_SSL('imap.qq.com', 993)
        mail.login(username, password)
        
        # 选择收件箱
        mail.select('INBOX')
        
        # 设置搜索条件（明天）
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')
        search_criteria = f'(SINCE "{tomorrow}") (OR SUBJECT "会议" SUBJECT "meeting")'
        
        # 搜索邮件
        status, messages = mail.search(None, search_criteria)
        
        results = []
        if status == 'OK':
            email_ids = messages[0].split()
            print(f"📨 QQ邮箱找到 {len(email_ids)} 封相关邮件")
            
            # 获取前5封邮件的详情
            for i, email_id in enumerate(email_ids[:5]):
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 解析主题
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    results.append({
                        'source': 'QQ邮箱',
                        'subject': subject,
                        'from': msg.get('From', ''),
                        'date': msg.get('Date', '')
                    })
        
        mail.logout()
        return results
        
    except Exception as e:
        print(f"❌ QQ邮箱搜索失败: {str(e)}")
        return []

def search_gmail_emails():
    """搜索Gmail"""
    try:
        # 从环境变量获取配置
        username = os.getenv('GMAIL_ADDRESS')
        password = os.getenv('GMAIL_APP_PASSWORD')
        
        if not username or not password:
            print("❌ 请设置GMAIL_ADDRESS和GMAIL_APP_PASSWORD环境变量")
            return []
        
        # 连接到Gmail
        print("🔗 连接到Gmail...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(username, password)
        
        # 选择收件箱
        mail.select('INBOX')
        
        # 设置搜索条件
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%d-%b-%Y')
        search_criteria = f'(SINCE "{tomorrow}") (OR SUBJECT "meeting" SUBJECT "conference")'
        
        # 搜索邮件
        status, messages = mail.search(None, search_criteria)
        
        results = []
        if status == 'OK':
            email_ids = messages[0].split()
            print(f"📨 Gmail找到 {len(email_ids)} 封相关邮件")
            
            # 获取前5封邮件的详情
            for i, email_id in enumerate(email_ids[:5]):
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # 解析主题
                    subject, encoding = decode_header(msg['Subject'])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else 'utf-8')
                    
                    results.append({
                        'source': 'Gmail',
                        'subject': subject,
                        'from': msg.get('From', ''),
                        'date': msg.get('Date', '')
                    })
        
        mail.logout()
        return results
        
    except Exception as e:
        print(f"❌ Gmail搜索失败: {str(e)}")
        return []

def main():
    """主函数"""
    print("="*60)
    print("📧 自动化邮件搜索")
    print("="*60)
    
    # 搜索QQ邮箱
    qq_results = search_qq_emails()
    
    # 搜索Gmail
    gmail_results = search_gmail_emails()
    
    # 显示结果
    all_results = qq_results + gmail_results
    
    if all_results:
        print(f"
🎯 总共找到 {len(all_results)} 封相关邮件:")
        for i, result in enumerate(all_results, 1):
            print(f"
{i}. [{result['source']}]")
            print(f"   主题: {result['subject']}")
            print(f"   发件人: {result['from']}")
            print(f"   日期: {result['date']}")
    else:
        print("
📭 未找到相关会议邮件")
        print("💡 建议:")
        print("   1. 检查环境变量配置")
        print("   2. 尝试手动搜索")
        print("   3. 检查垃圾邮件文件夹")

if __name__ == "__main__":
    main()
