#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成Agent Skills介绍语音播报
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from azure_tts_simple import azure_tts_simple

def generate_agent_skills_voice():
    """生成Agent Skills介绍语音"""
    
    # 读取介绍文本
    text_file = "/Users/jiyingguo/.openclaw/workspace/agent_skills_intro.txt"
    if not os.path.exists(text_file):
        print(f"❌ 介绍文本文件不存在: {text_file}")
        return None
    
    with open(text_file, 'r', encoding='utf-8') as f:
        intro_text = f.read().strip()
    
    print(f"📚 Agent Skills介绍文本长度: {len(intro_text)} 字符")
    
    # 输出文件路径
    output_file = "/tmp/agent_skills_intro_20260228.mp3"
    
    # 使用Azure TTS生成语音
    print("🎯 使用Azure TTS生成语音播报...")
    success, file_path = azure_tts_simple(intro_text, output_file)
    
    if success:
        print(f"✅ 语音生成成功!")
        print(f"📁 文件: {file_path}")
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"📊 大小: {file_size} 字节 ({file_size/1024:.1f} KB)")
            duration_estimate = file_size / 16000  # 粗略估计时长（16kbps）
            print(f"⏱️  预计时长: {duration_estimate:.1f} 秒")
        return file_path
    else:
        print("❌ 语音生成失败")
        return None

if __name__ == "__main__":
    print("=" * 50)
    print("🎙️  Agent Skills介绍语音播报生成器")
    print("=" * 50)
    
    voice_file = generate_agent_skills_voice()
    
    if voice_file and os.path.exists(voice_file):
        print("\n🎉 Agent Skills介绍语音已生成!")
        print(f"🔊 文件路径: {voice_file}")
        print(f"\n💡 播放方式:")
        print(f"   1. 直接播放: afplay {voice_file}")
        print(f"   2. 后台播放: afplay {voice_file} &")
        print(f"   3. 发送到飞书: python3 feishu_voice_sender.py {voice_file}")
        
        # 自动开始播放
        print(f"\n🎵 正在播放Agent Skills介绍...")
        os.system(f"afplay {voice_file} &")
    else:
        print("\n❌ 语音生成失败")