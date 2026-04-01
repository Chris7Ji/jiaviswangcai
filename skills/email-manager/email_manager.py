#!/usr/bin/env python3
"""
邮件管理技能 - 超级助理包
支持QQ邮箱和华为邮箱的IMAP/SMTP管理
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from datetime import datetime
import os
import json

# 邮箱配置
EMAIL_CONFIGS = {
    "qq": {
        "email": "86940135@qq.com",
        "password": os.environ.get("QQ_EMAIL_PASSWORD"),
        "imap_server": "imap.qq.com",
        "imap_port": 993,
        "smtp_server": "smtp.qq.com",
        "smtp_port": 587,
        "name": "QQ邮箱"
    },
    "huawei": {
        "email": "jiyingguo@huawei.com",
        "password": os.environ.get("HUAWEI_EMAIL_PASSWORD", ""),
        "imap_server": "imap.huawei.com",
        "imap_port": 993,
        "smtp_server": "smtp.huawei.com",
        "smtp_port": 587,
        "name": "华为邮箱"
    }
}

class EmailManager:
    """邮件管理器"""
    
    def __init__(self, config_key="qq"):
        self.config = EMAIL_CONFIGS.get(config_key)
        if not self.config:
            raise ValueError(f"未知的邮箱配置: {config_key}")
        self.imap_conn = None
        
    def connect_imap(self):
        """连接IMAP服务器"""
        try:
            self.imap_conn = imaplib.IMAP4_SSL(
                self.config["imap_server"], 
                self.config["imap_port"]
            )
            self.imap_conn.login(
                self.config["email"], 
                self.config["password"]
            )
            return True
        except Exception as e:
            print(f"IMAP连接失败: {e}")
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.imap_conn:
            try:
                self.imap_conn.logout()
            except:
                pass
            self.imap_conn = None
    
    def get_unread_count(self):
        """获取未读邮件数量"""
        if not self.imap_conn:
            if not self.connect_imap():
                return None
        
        try:
            self.imap_conn.select("INBOX")
            status, messages = self.imap_conn.search(None, "UNSEEN")
            if status == "OK":
                return len(messages[0].split())
            return 0
        except Exception as e:
            print(f"获取未读数量失败: {e}")
            return None
    
    def get_recent_emails(self, limit=10):
        """获取最近的邮件"""
        if not self.imap_conn:
            if not self.connect_imap():
                return []
        
        emails = []
        try:
            self.imap_conn.select("INBOX")
            status, messages = self.imap_conn.search(None, "ALL")
            
            if status != "OK":
                return []
            
            message_ids = messages[0].split()
            # 获取最新的limit封邮件
            recent_ids = message_ids[-limit:]
            
            for msg_id in reversed(recent_ids):
                status, msg_data = self.imap_conn.fetch(msg_id, "(RFC822)")
                if status != "OK":
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                # 解析邮件信息
                subject = self._decode_header(msg["Subject"])
                from_addr = self._decode_header(msg["From"])
                date = msg["Date"]
                
                # 获取邮件正文
                body = self._get_body(msg)
                
                emails.append({
                    "id": msg_id.decode(),
                    "subject": subject,
                    "from": from_addr,
                    "date": date,
                    "body": body[:500] if body else "",
                    "unread": msg_id in self.imap_conn.search(None, "UNSEEN")[1][0].split()
                })
            
            return emails
            
        except Exception as e:
            print(f"获取邮件失败: {e}")
            return []
    
    def _decode_header(self, header):
        """解码邮件头"""
        if not header:
            return ""
        decoded, charset = decode_header(header)[0]
        if isinstance(decoded, bytes):
            return decoded.decode(charset or "utf-8", errors="ignore")
        return decoded
    
    def _get_body(self, msg):
        """获取邮件正文"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        return part.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except:
                        pass
        else:
            try:
                return msg.get_payload(decode=True).decode("utf-8", errors="ignore")
            except:
                pass
        return ""
    
    def send_email(self, to_email, subject, body, html_body=None):
        """发送邮件"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["email"]
            msg['To'] = to_email
            
            # 添加纯文本内容
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # 添加HTML内容（如果有）
            if html_body:
                msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            
            # 连接SMTP服务器
            with smtplib.SMTP_SSL(self.config["smtp_server"], 465) as server:
                server.login(self.config["email"], self.config["password"])
                server.sendmail(self.config["email"], [to_email], msg.as_string())
            
            return True
        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 email_manager.py <命令> [参数]")
        print("命令:")
        print("  unread [qq|huawei]     - 获取未读邮件数量")
        print("  list [qq|huawei] [n]   - 列出最近n封邮件")
        print("  send <to> <subject> <body> - 发送邮件")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "unread":
        config_key = sys.argv[2] if len(sys.argv) > 2 else "qq"
        manager = EmailManager(config_key)
        count = manager.get_unread_count()
        manager.disconnect()
        
        if count is not None:
            print(f"{manager.config['name']} 未读邮件: {count} 封")
        else:
            print("获取未读邮件数量失败")
    
    elif command == "list":
        config_key = sys.argv[2] if len(sys.argv) > 2 else "qq"
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        manager = EmailManager(config_key)
        emails = manager.get_recent_emails(limit)
        manager.disconnect()
        
        if emails:
            print(f"\n最近 {len(emails)} 封邮件 ({manager.config['name']}):\n")
            for i, e in enumerate(emails, 1):
                unread_mark = "🔴" if e.get('unread') else "📧"
                print(f"{unread_mark} {i}. {e['subject']}")
                print(f"   发件人: {e['from']}")
                print(f"   时间: {e['date']}")
                if e['body']:
                    print(f"   摘要: {e['body'][:100]}...")
                print()
        else:
            print("没有邮件或获取失败")
    
    elif command == "send":
        if len(sys.argv) < 5:
            print("用法: python3 email_manager.py send <to> <subject> <body>")
            sys.exit(1)
        
        to_email = sys.argv[2]
        subject = sys.argv[3]
        body = sys.argv[4]
        
        manager = EmailManager("qq")  # 默认使用QQ邮箱发送
        if manager.send_email(to_email, subject, body):
            print(f"✅ 邮件发送成功到 {to_email}")
        else:
            print("❌ 邮件发送失败")
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
