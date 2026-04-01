#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送PPT文件到飞书
"""

import sys
import os
import subprocess
import json

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
    file_name = os.path.basename(file_path)
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
      -H "Authorization: Bearer {token}" \
      -F "file=@{file_path}" \
      -F "file_name={file_name}" \
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

def send_file_message(token, file_key, file_name):
    """发送文件消息"""
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

def send_ppt_to_feishu(ppt_file):
    """发送PPT文件到飞书"""
    if not os.path.exists(ppt_file):
        print(f"❌ 文件不存在: {ppt_file}")
        return False
    
    file_name = os.path.basename(ppt_file)
    file_size = os.path.getsize(ppt_file)
    
    print(f"📤 发送PPT文件到飞书")
    print(f"📄 文件名: {file_name}")
    print(f"📊 文件大小: {file_size} 字节")
    print(f"📁 文件路径: {ppt_file}")
    
    # 获取token
    token = get_tenant_token()
    if not token:
        print("❌ 无法获取飞书Token")
        return False
    print("✅ Token获取成功")
    
    # 上传文件
    print("📤 上传文件中...")
    file_key = upload_file(token, ppt_file)
    if not file_key:
        print("❌ 文件上传失败")
        return False
    print(f"✅ 文件上传成功: {file_key}")
    
    # 发送消息
    print("📨 发送消息中...")
    if send_file_message(token, file_key, file_name):
        print("✅ 消息发送成功！")
        return True
    else:
        print("❌ 消息发送失败")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python send_ppt_to_feishu.py <PPT文件路径>")
        print("示例: python send_ppt_to_feishu.py ./2026_AI发展趋势_精美科技版.pptx")
        return False
    
    ppt_file = sys.argv[1]
    success = send_ppt_to_feishu(ppt_file)
    
    if success:
        print(f"\n🎉 成功！PPT文件已发送到您的手机飞书")
        print(f"📄 文件: {os.path.basename(ppt_file)}")
        return True
    else:
        print("\n❌ 发送失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)