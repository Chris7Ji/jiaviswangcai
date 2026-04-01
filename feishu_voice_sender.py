#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音文件发送工具
使用方法: python feishu_voice_sender.py <音频文件路径>
"""

import urllib.request
import json
import os
import sys
import subprocess

# 飞书应用配置
APP_ID = "cli_a9f596118438dcef"
APP_SECRET = "42X7fiT1ZWm3SxIJndukBeKrru1VHpGo"
USER_ID = "ou_b6c7778820b20031cd97bdc45d1cd9fa"

def get_tenant_token():
    """获取飞书tenant_access_token"""
    cmd = '''curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
      -H "Content-Type: application/json" \
      -d '{"app_id":"''' + APP_ID + '''","app_secret":"''' + APP_SECRET + '''"}' '''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        return json.loads(result.stdout)["tenant_access_token"]
    except:
        print("获取Token失败:", result.stdout)
        return None

def upload_file(token, file_path):
    """上传文件到飞书"""
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
      -H "Authorization: Bearer {token}" \
      -F "file=@{file_path}" \
      -F "file_name={os.path.basename(file_path)}" \
      -F "file_type=stream"'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        if data.get("code") == 0:
            return data["data"]["file_key"]
        print("上传失败:", data)
        return None
    except:
        print("上传解析失败:", result.stdout)
        return None

def send_voice_message(token, file_key):
    """发送语音文件消息"""
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{{
        "receive_id": "{USER_ID}",
        "msg_type": "file",
        "content": "{{\\\"file_key\\\": \\\"{file_key}\\\"}}"
      }}' '''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        if data.get("code") == 0:
            return True
        print("发送失败:", data)
        return False
    except:
        print("发送解析失败:", result.stdout)
        return False

def send_voice(file_path):
    """发送语音文件到飞书"""
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    
    print(f"📤 上传语音文件: {file_path}")
    
    # 获取token
    token = get_tenant_token()
    if not token:
        return False
    print("✅ Token获取成功")
    
    # 上传文件
    file_key = upload_file(token, file_path)
    if not file_key:
        return False
    print(f"✅ 文件上传成功: {file_key}")
    
    # 发送消息
    if send_voice_message(token, file_key):
        print("✅ 消息发送成功！")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python feishu_voice_sender.py <音频文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = send_voice(file_path)
    sys.exit(0 if success else 1)
