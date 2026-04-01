#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用修复后的Azure TTS生成回复语音
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from azure_tts_simple import azure_tts_simple

def generate_azure_voice_reply(text, output_path="/tmp/azure_reply.mp3"):
    """使用Azure TTS生成回复语音"""
    print(f"🎯 使用微软Azure TTS生成语音回复")
    print(f"📝 文本: {text}")
    
    success, file_path = azure_tts_simple(text, output_path)
    
    if success:
        print(f"✅ 微软Azure TTS语音生成成功!")
        print(f"📁 文件: {file_path}")
        print(f"📊 大小: {os.path.getsize(file_path)} 字节")
        return file_path
    else:
        print("❌ 微软Azure TTS语音生成失败")
        return None

if __name__ == "__main__":
    # 默认回复文本
    reply_text = "我已修复微软Azure TTS，现在用微软TTS给你回复语音。语音识别和回复功能完全正常。"
    
    # 如果提供了命令行参数，使用自定义文本
    if len(sys.argv) > 1:
        reply_text = sys.argv[1]
    
    # 生成语音
    voice_file = generate_azure_voice_reply(reply_text)
    
    if voice_file:
        print(f"\n🎉 微软Azure TTS回复语音已生成: {voice_file}")
        print(f"📤 可以发送给用户")
    else:
        print("\n⚠️ 无法生成微软Azure TTS语音")