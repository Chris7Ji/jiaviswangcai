#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音消息发送工具 - 使用opus格式
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

def convert_to_opus(mp3_path, opus_path):
    """将MP3转换为opus格式"""
    cmd = f"ffmpeg -i {mp3_path} -c:a libopus -b:a 24k {opus_path} -y 2>&1"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if os.path.exists(opus_path):
        return True
    print("转换失败:", result.stderr)
    return False

def upload_voice(token, opus_path, duration_ms):
    """上传语音文件到飞书"""
    # 获取文件时长（秒）
    cmd = f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {opus_path}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        duration_sec = float(result.stdout.strip())
        duration_ms = int(duration_sec * 1000)
    except:
        duration_ms = 30000  # 默认30秒
    
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
      -H "Authorization: Bearer {token}" \
      -F "file_type=opus" \
      -F "file_name=voice.opus" \
      -F "duration={duration_ms}" \
      -F "file=@{opus_path}"'''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        if data.get("code") == 0:
            return data["data"]["file_key"], duration_ms
        print("上传失败:", data)
        return None, 0
    except Exception as e:
        print("上传解析失败:", e, result.stdout)
        return None, 0

def send_voice_message(token, file_key, duration_ms):
    """发送语音消息"""
    content = json.dumps({
        "file_key": file_key,
        "duration": duration_ms
    })
    
    cmd = f'''curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
      -H "Authorization: Bearer {token}" \
      -H "Content-Type: application/json" \
      -d '{json.dumps({
          "receive_id": USER_ID,
          "msg_type": "voice",
          "content": content
      })}' '''
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    try:
        data = json.loads(result.stdout)
        if data.get("code") == 0:
            return True
        print("发送失败:", data)
        return False
    except Exception as e:
        print("发送解析失败:", e, result.stdout)
        return False

def send_voice(mp3_path):
    """发送语音文件到飞书"""
    if not os.path.exists(mp3_path):
        print(f"文件不存在: {mp3_path}")
        return False
    
    opus_path = mp3_path.replace('.mp3', '.opus')
    
    # 转换为opus格式
    print(f"🎵 转换为opus格式...")
    if not convert_to_opus(mp3_path, opus_path):
        return False
    print(f"✅ 转换成功: {opus_path}")
    
    # 获取token
    token = get_tenant_token()
    if not token:
        return False
    print("✅ Token获取成功")
    
    # 上传文件
    file_key, duration_ms = upload_voice(token, opus_path, 30000)
    if not file_key:
        return False
    print(f"✅ 文件上传成功: {file_key}, 时长: {duration_ms}ms")
    
    # 发送消息
    if send_voice_message(token, file_key, duration_ms):
        print("✅ 语音消息发送成功！")
        # 清理临时文件
        if os.path.exists(opus_path):
            os.remove(opus_path)
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python feishu_voice_opus.py <mp3文件路径>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = send_voice(file_path)
    sys.exit(0 if success else 1)
