#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成北京天气语音播报
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 尝试导入不同的Azure TTS模块
try:
    from azure_tts_simple import azure_tts_simple
    print("✅ 导入 azure_tts_simple 成功")
    TTS_MODULE = "simple"
except ImportError:
    try:
        from azure_tts_integration import AzureTTS
        print("✅ 导入 AzureTTS 成功")
        TTS_MODULE = "integration"
    except ImportError:
        print("❌ 无法导入Azure TTS模块")
        sys.exit(1)

def generate_weather_voice():
    """生成北京天气语音"""
    
    # 读取天气文本
    text_file = "/Users/jiyingguo/.openclaw/workspace/beijing_weather_text.txt"
    if not os.path.exists(text_file):
        print(f"❌ 天气文本文件不存在: {text_file}")
        return None
    
    with open(text_file, 'r', encoding='utf-8') as f:
        weather_text = f.read().strip()
    
    print(f"🌤️ 北京天气文本: {weather_text}")
    
    # 输出文件路径
    output_file = "/tmp/beijing_weather_20260228.mp3"
    
    # 使用Azure TTS生成语音
    if TTS_MODULE == "simple":
        print("🎯 使用 azure_tts_simple 生成语音...")
        success, file_path = azure_tts_simple(weather_text, output_file)
        
        if success:
            print(f"✅ 语音生成成功!")
            print(f"📁 文件: {file_path}")
            if os.path.exists(file_path):
                print(f"📊 大小: {os.path.getsize(file_path)} 字节")
            return file_path
        else:
            print("❌ 语音生成失败")
            return None
    
    elif TTS_MODULE == "integration":
        print("🎯 使用 AzureTTS 生成语音...")
        tts = AzureTTS()
        try:
            file_path = tts.text_to_speech(weather_text, output_file)
            print(f"✅ 语音生成成功!")
            print(f"📁 文件: {file_path}")
            if os.path.exists(file_path):
                print(f"📊 大小: {os.path.getsize(file_path)} 字节")
            return file_path
        except Exception as e:
            print(f"❌ 语音生成失败: {e}")
            return None

if __name__ == "__main__":
    print("=" * 50)
    print("🎙️  北京天气语音播报生成器")
    print("=" * 50)
    
    voice_file = generate_weather_voice()
    
    if voice_file and os.path.exists(voice_file):
        print("\n🎉 语音文件已生成!")
        print(f"🔊 文件路径: {voice_file}")
        print(f"💡 您可以通过以下方式播放:")
        print(f"   1. 直接打开: open {voice_file}")
        print(f"   2. 使用命令行: afplay {voice_file}")
        print(f"   3. 发送到飞书: 使用feishu_voice_sender.py")
    else:
        print("\n❌ 语音生成失败")