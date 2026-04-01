#!/usr/bin/env python3
"""
火车出发提醒发送脚本
发送时间: 2026-03-08 17:30
"""

import sys
sys.path.insert(0, '/Users/jiyingguo/.openclaw/workspace/skills/email-manager')

from email_manager import EmailManager

def send_train_reminder():
    """发送火车提醒"""
    
    # 读取提醒内容
    with open('/tmp/train_reminder_2026-03-08.txt', 'r') as f:
        reminder_content = f.read()
    
    subject = "🚄 火车出发提醒 - 今天19:00北京站"
    
    # 发送邮件提醒
    try:
        manager = EmailManager("qq")
        
        # 发送到QQ邮箱
        success1 = manager.send_email(
            "86940135@qq.com",
            subject,
            reminder_content
        )
        
        # 发送到华为邮箱
        success2 = manager.send_email(
            "jiyingguo@huawei.com",
            subject,
            reminder_content
        )
        
        manager.disconnect()
        
        if success1 and success2:
            print("✅ 邮件提醒发送成功!")
            return True
        else:
            print("⚠️ 部分邮件发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    send_train_reminder()
