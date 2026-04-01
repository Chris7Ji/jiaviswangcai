#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送今日AI新闻语音播报到飞书
"""

import sys
import os
import re
import hashlib
import time
import subprocess
import json

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def extract_news_from_md(file_path):
    """从Markdown文件中提取新闻"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式提取新闻标题和摘要
    pattern = r'### \d+\. (.*?)\n\*\*标题：\*\* (.*?)\n.*?\*\*完整摘要：\*\*\n(.*?)\n\*\*深度分析：\*\*'
    matches = re.findall(pattern, content, re.DOTALL)
    
    news_items = []
    for num_title, news_title, summary in matches[:4]:  # 只取前4条
        # 清理摘要文本
        clean_summary = summary.strip().replace('\n', ' ').replace('  ', ' ')
        news_items.append((news_title, clean_summary))
    
    return news_items

def create_voice_text(news_items):
    """创建语音播报文本"""
    voice_text = '''【AI新闻语音播报】2026年3月2日

大家好，我是旺财。现在为您播报今天的AI与科技新闻。

'''
    
    for i, (title, summary) in enumerate(news_items, 1):
        # 截取前150字
        short_summary = summary[:150] + '...' if len(summary) > 150 else summary
        voice_text += f'第{i}条新闻：{title}\n'
        voice_text += f'{short_summary}\n\n'
    
    voice_text += '以上就是今天的AI新闻摘要。更多详细内容请查看文字版。谢谢收听！'
    
    return voice_text

def generate_tts_voice(text, output_path):
    """使用Azure TTS生成语音文件"""
    try:
        from azure_tts_simple import azure_tts_simple
    except ImportError:
        print("❌ 无法导入azure_tts_simple模块")
        return None
    
    print(f"🎤 生成TTS语音...")
    print(f"📝 文本长度: {len(text)} 字符")
    
    # 生成TTS
    success, temp_file = azure_tts_simple(text, output_path)
    
    if success and temp_file:
        # 确保文件存在
        if os.path.exists(temp_file):
            file_size = os.path.getsize(temp_file)
            print(f"✅ TTS生成成功: {temp_file}")
            print(f"📊 文件大小: {file_size} 字节")
            return temp_file
        else:
            print(f"❌ 文件不存在: {temp_file}")
            return None
    else:
        print("❌ TTS生成失败")
        return None

def send_voice_to_feishu(file_path):
    """发送语音文件到飞书"""
    print(f"📤 发送语音文件到飞书: {file_path}")
    
    # 获取token
    token = get_tenant_token()
    if not token:
        print("❌ 无法获取飞书Token")
        return False
    print("✅ Token获取成功")
    
    # 上传文件
    file_key = upload_file(token, file_path)
    if not file_key:
        print("❌ 文件上传失败")
        return False
    print(f"✅ 文件上传成功: {file_key}")
    
    # 发送消息
    if send_voice_message(token, file_key):
        print("✅ 消息发送成功！")
        return True
    else:
        print("❌ 消息发送失败")
        return False

def main():
    print("🚀 开始发送今日AI新闻语音播报")
    print("=" * 50)
    
    # 1. 读取今日新闻
    news_file = "/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-02.md"
    if not os.path.exists(news_file):
        print(f"❌ 新闻文件不存在: {news_file}")
        return False
    
    print(f"📰 读取新闻文件: {news_file}")
    news_items = extract_news_from_md(news_file)
    print(f"📊 提取到 {len(news_items)} 条新闻")
    
    # 2. 创建语音文本
    voice_text = create_voice_text(news_items)
    print(f"📝 语音文本长度: {len(voice_text)} 字符")
    print("\n--- 语音文本预览 ---")
    print(voice_text[:300] + "..." if len(voice_text) > 300 else voice_text)
    print("--- 预览结束 ---\n")
    
    # 3. 生成语音文件
    # 使用MD5哈希作为文件名，避免重复生成
    md5_hash = hashlib.md5(voice_text.encode('utf-8')).hexdigest()
    
    # 创建缓存目录
    cache_dir = "/tmp/jarvis_voice_cache"
    os.makedirs(cache_dir, exist_ok=True)
    
    voice_file = os.path.join(cache_dir, f"ai_news_2026-03-02_{md5_hash[:8]}.mp3")
    
    # 检查缓存
    if os.path.exists(voice_file):
        print(f"✅ 使用缓存文件: {voice_file}")
        file_size = os.path.getsize(voice_file)
        print(f"📊 缓存文件大小: {file_size} 字节")
    else:
        print(f"🔄 生成新的语音文件: {voice_file}")
        voice_file = generate_tts_voice(voice_text, voice_file)
        if not voice_file:
            print("❌ 语音文件生成失败")
            return False
    
    # 4. 发送到飞书
    print("\n📱 发送到飞书...")
    success = send_voice_to_feishu(voice_file)
    
    if success:
        print("\n🎉 成功！AI新闻语音播报已发送到您的手机飞书")
        print(f"📄 语音文件: {voice_file}")
        return True
    else:
        print("\n❌ 发送失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)