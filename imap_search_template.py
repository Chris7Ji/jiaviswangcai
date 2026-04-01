#!/usr/bin/env python3
"""
IMAP邮件搜索模板
需要配置邮箱信息后使用
"""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta
import sys

class EmailSearcher:
    def __init__(self, config):
        """
        初始化邮件搜索器
        
        Args:
            config (dict): 包含以下键:
                - server: IMAP服务器地址
                - port: IMAP端口 (默认993)
                - username: 邮箱用户名
                - password: 邮箱密码或应用专用密码
                - use_ssl: 是否使用SSL (默认True)
        """
        self.config = config
        self.connection = None
        
    def connect(self):
        """连接到IMAP服务器"""
        try:
            if self.config.get('use_ssl', True):
                self.connection = imaplib.IMAP4_SSL(
                    self.config['server'], 
                    self.config.get('port', 993)
                )
            else:
                self.connection = imaplib.IMAP4(
                    self.config['server'], 
                    self.config.get('port', 143)
                )
            
            print(f"🔗 连接到 {self.config['server']}...")
            self.connection.login(self.config['username'], self.config['password'])
            print("✅ 登录成功")
            return True
            
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            return False
    
    def search_emails(self, search_criteria):
        """
        搜索邮件
        
        Args:
            search_criteria (str): IMAP搜索条件
            
        Returns:
            list: 邮件ID列表
        """
        if not self.connection:
            print("❌ 未连接到服务器")
            return []
        
        try:
            # 选择收件箱
            self.connection.select('INBOX')
            
            # 搜索邮件
            print(f"🔍 搜索条件: {search_criteria}")
            status, messages = self.connection.search(None, search_criteria)
            
            if status == 'OK':
                email_ids = messages[0].split()
                print(f"📨 找到 {len(email_ids)} 封邮件")
                return email_ids
            else:
                print("❌ 搜索失败")
                return []
                
        except Exception as e:
            print(f"❌ 搜索出错: {str(e)}")
            return []
    
    def get_email_details(self, email_id):
        """获取邮件详情"""
        try:
            status, msg_data = self.connection.fetch(email_id, '(RFC822)')
            
            if status == 'OK':
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # 解析邮件头
                subject, encoding = decode_header(msg['Subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')
                
                from_header = msg.get('From', '')
                date_header = msg.get('Date', '')
                
                return {
                    'id': email_id.decode(),
                    'subject': subject,
                    'from': from_header,
                    'date': date_header,
                    'has_attachment': self._has_attachment(msg)
                }
                
        except Exception as e:
            print(f"❌ 获取邮件详情失败: {str(e)}")
        
        return None
    
    def _has_attachment(self, msg):
        """检查邮件是否有附件"""
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                return True
        return False
    
    def disconnect(self):
        """断开连接"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
                print("🔒 连接已关闭")
            except:
                pass

def get_tomorrow_search_criteria():
    """获取明天的搜索条件"""
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%d-%b-%Y')
    
    # 多种搜索条件
    criteria_list = [
        f'(SINCE "{tomorrow_str}")',  # 从明天开始
        f'(ON "{tomorrow_str}")',     # 正好是明天
        f'(SUBJECT "meeting") (SINCE "{tomorrow_str}")',
        f'(SUBJECT "会议") (SINCE "{tomorrow_str}")',
        f'(OR SUBJECT "meeting" SUBJECT "会议") (SINCE "{tomorrow_str}")',
        f'(TEXT "agenda") (SINCE "{tomorrow_str}")',
        f'(TEXT "议程") (SINCE "{tomorrow_str}")',
    ]
    
    return criteria_list

def print_config_template():
    """打印配置模板"""
    print("\n" + "="*60)
    print("📋 邮箱配置模板")
    print("="*60)
    
    print("\n1. QQ邮箱配置:")
    print("""
    qq_config = {
        'server': 'imap.qq.com',
        'port': 993,
        'username': '你的QQ号@qq.com',
        'password': '你的授权码（不是登录密码）',
        'use_ssl': True
    }
    
    ⚠️ 注意：QQ邮箱需要开启IMAP服务并获取授权码
    获取授权码步骤：
    1. 登录QQ邮箱网页版
    2. 设置 → 账户 → POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
    3. 开启IMAP/SMTP服务
    4. 生成授权码
    """)
    
    print("\n2. Gmail配置:")
    print("""
    gmail_config = {
        'server': 'imap.gmail.com',
        'port': 993,
        'username': '你的Gmail地址@gmail.com',
        'password': '你的应用专用密码',
        'use_ssl': True
    }
    
    ⚠️ 注意：Gmail需要开启两步验证并生成应用专用密码
    获取应用专用密码步骤：
    1. 登录Google账户
    2. 安全性 → 两步验证 → 应用专用密码
    3. 生成新密码
    """)

def main():
    """主函数"""
    print("="*70)
    print("📧 IMAP邮件搜索脚本模板")
    print("="*70)
    
    print("\n🎯 功能说明:")
    print("   1. 支持通过IMAP协议搜索邮件")
    print("   2. 可以搜索特定日期的会议邮件")
    print("   3. 支持多种搜索条件组合")
    print("   4. 安全提醒：不要硬编码密码")
    
    # 显示配置模板
    print_config_template()
    
    # 显示搜索条件示例
    print("\n" + "="*60)
    print("🔍 搜索条件示例")
    print("="*60)
    
    criteria_list = get_tomorrow_search_criteria()
    for i, criteria in enumerate(criteria_list, 1):
        print(f"{i}. {criteria}")
    
    print("\n📝 使用步骤:")
    print("   1. 复制配置模板，填写你的邮箱信息")
    print("   2. 将密码存储在环境变量中:")
    print("      export QQ_EMAIL_PASSWORD='你的授权码'")
    print("      export GMAIL_APP_PASSWORD='你的应用密码'")
    print("   3. 修改脚本使用环境变量")
    print("   4. 运行脚本搜索邮件")
    
    print("\n💡 安全建议:")
    print("   1. 使用环境变量存储敏感信息")
    print("   2. 考虑使用.keyring或密钥管理服务")
    print("   3. 定期更新授权码/应用密码")
    print("   4. 不要将配置提交到版本控制系统")
    
    print("\n🤖 我可以帮你:")
    print("   1. 根据你的具体配置修改脚本")
    print("   2. 添加更多搜索功能")
    print("   3. 优化搜索结果展示")

if __name__ == "__main__":
    main()