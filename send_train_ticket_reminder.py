#!/usr/bin/env python3
"""
火车票购买提醒发送脚本
发送时间: 2026-03-30 10:00/12:00/15:00/18:00
"""

import sys
import os
import requests
from datetime import datetime

# 添加email-manager路径
sys.path.insert(0, '/Users/jiyingguo/.openclaw/workspace/skills/email-manager')
from email_manager import EmailManager

# 飞书配置
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "cli_a6f596118438dcef")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_BASE_URL = "https://open.feishu.cn/open-apis"
FEISHU_USER_OPEN_ID = "ou_b6c7778820b20031cd97bdc45d1cd9fa"

# 邮件配置
EMAIL_RECIPIENTS = ["86940135@qq.com", "jiyingguo@huawei.com"]
EMAIL_SUBJECT = "🚄 提醒：购买火车票"
EMAIL_CONTENT = """老板，这是购买火车票的时间提醒！

⏰ 提醒时间：{reminder_time}

请及时登录12306或其他购票平台购买火车票，以免错过出行计划。

— 旺财Jarvis 自动提醒"""

def get_feishu_access_token():
    """获取飞书访问令牌"""
    url = f"{FEISHU_BASE_URL}/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            return result.get("tenant_access_token")
        else:
            print(f"❌ 获取飞书token失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 请求飞书API失败: {e}")
        return None

def send_feishu_message(message_text):
    """发送飞书消息"""
    token = get_feishu_access_token()
    if not token:
        return False
    
    url = f"{FEISHU_BASE_URL}/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": FEISHU_USER_OPEN_ID,
        "msg_type": "text",
        "content": f'{{"text":"{message_text}"}}'
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        result = response.json()
        if result.get("code") == 0:
            print("✅ 飞书消息发送成功!")
            return True
        else:
            print(f"❌ 飞书消息发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送飞书消息异常: {e}")
        return False

def send_email_reminder(reminder_time):
    """发送邮件提醒"""
    try:
        manager = EmailManager("qq")
        content = EMAIL_CONTENT.format(reminder_time=reminder_time)
        
        success_count = 0
        for recipient in EMAIL_RECIPIENTS:
            success = manager.send_email(recipient, EMAIL_SUBJECT, content)
            if success:
                success_count += 1
                print(f"✅ 邮件发送成功: {recipient}")
            else:
                print(f"⚠️ 邮件发送失败: {recipient}")
        
        manager.disconnect()
        
        if success_count == len(EMAIL_RECIPIENTS):
            print("✅ 所有邮件发送成功!")
            return True
        elif success_count > 0:
            print(f"⚠️ 部分邮件发送成功 ({success_count}/{len(EMAIL_RECIPIENTS)})")
            return True
        else:
            print("❌ 所有邮件发送失败")
            return False
            
    except Exception as e:
        print(f"❌ 发送邮件异常: {e}")
        return False

def send_reminder(reminder_time_str):
    """发送完整提醒"""
    print(f"\n{'='*50}")
    print(f"🚄 火车票购买提醒 - {reminder_time_str}")
    print(f"{'='*50}")
    
    # 发送飞书消息
    feishu_msg = f"🚄 提醒：购买火车票 ({reminder_time_str})"
    feishu_success = send_feishu_message(feishu_msg)
    
    # 发送邮件
    email_success = send_email_reminder(reminder_time_str)
    
    print(f"\n📊 发送结果:")
    print(f"  飞书: {'✅ 成功' if feishu_success else '❌ 失败'}")
    print(f"  邮件: {'✅ 成功' if email_success else '❌ 失败'}")
    
    return feishu_success or email_success

if __name__ == "__main__":
    # 从命令行参数获取提醒时间
    if len(sys.argv) > 1:
        reminder_time = sys.argv[1]
    else:
        reminder_time = datetime.now().strftime("%H:%M")
    
    success = send_reminder(reminder_time)
    sys.exit(0 if success else 1)
