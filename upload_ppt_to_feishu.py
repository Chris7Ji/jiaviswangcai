#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上传PPT文件到飞书并发送给用户
"""

import requests
import json
import sys
import os

def get_tenant_access_token():
    """获取飞书租户访问令牌"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    
    # 使用你的飞书应用凭证
    app_id = "cli_a9f596118438dcef"
    app_secret = "42X7fiT1ZWm3SxIJndukBeKrru1VHpGo"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("tenant_access_token")
        else:
            print(f"获取token失败: {result}")
            return None
    except Exception as e:
        print(f"获取token异常: {str(e)}")
        return None

def upload_file_to_feishu(file_path, token):
    """上传文件到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    file_name = os.path.basename(file_path)
    
    try:
        with open(file_path, 'rb') as f:
            files = {
                'file': (file_name, f, 'application/vnd.openxmlformats-officedocument.presentationml.presentation'),
                'file_name': (None, file_name),
                'file_type': (None, 'stream')
            }
            
            response = requests.post(url, headers=headers, files=files, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            if result.get("code") == 0:
                file_key = result.get("data", {}).get("file_key")
                print(f"✅ 文件上传成功，file_key: {file_key}")
                return file_key
            else:
                print(f"文件上传失败: {result}")
                return None
    except Exception as e:
        print(f"文件上传异常: {str(e)}")
        return None

def send_file_message(token, file_key, receive_id):
    """发送文件消息"""
    url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("code") == 0:
            message_id = result.get("data", {}).get("message_id")
            print(f"✅ 消息发送成功，message_id: {message_id}")
            return message_id
        else:
            print(f"消息发送失败: {result}")
            return None
    except Exception as e:
        print(f"消息发送异常: {str(e)}")
        return None

def main():
    """主函数"""
    ppt_file = "/Users/jiyingguo/.openclaw/workspace/2026_AI发展趋势预测.pptx"
    receive_id = "ou_b6c7778820b20031cd97bdc45d1cd9fa"  # 你的飞书open_id
    
    # 检查文件是否存在
    if not os.path.exists(ppt_file):
        print(f"❌ PPT文件不存在: {ppt_file}")
        return False
    
    print(f"📁 找到PPT文件: {ppt_file}")
    print(f"📊 文件大小: {os.path.getsize(ppt_file)} 字节")
    
    # 1. 获取访问令牌
    print("\n🔑 获取飞书访问令牌...")
    token = get_tenant_access_token()
    if not token:
        print("❌ 无法获取访问令牌")
        return False
    
    print(f"✅ 获取到token: {token[:20]}...")
    
    # 2. 上传文件
    print("\n📤 上传PPT文件到飞书...")
    file_key = upload_file_to_feishu(ppt_file, token)
    if not file_key:
        print("❌ 文件上传失败")
        return False
    
    # 3. 发送消息
    print(f"\n📨 发送文件消息给用户 {receive_id}...")
    message_id = send_file_message(token, file_key, receive_id)
    if not message_id:
        print("❌ 消息发送失败")
        return False
    
    print("\n🎉 所有操作完成！")
    print(f"📄 文件: {os.path.basename(ppt_file)}")
    print(f"🔑 file_key: {file_key}")
    print(f"💬 message_id: {message_id}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)