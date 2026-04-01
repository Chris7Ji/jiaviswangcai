#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复飞书语音播放问题 - 把TTS文件保存到飞书可访问的目录
"""

import sys
import os

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from azure_tts_simple import azure_tts_simple

# 飞书可访问的输出目录
OUTPUT_DIR = "/Users/jiyingguo/.openclaw/media/outbound"

def generate_tts_for_feishu(text, custom_filename=None):
    """生成飞书可播放的TTS语音"""
    
    # 生成文件名
    if custom_filename:
        filename = custom_filename
    else:
        import time
        timestamp = int(time.time())
        filename = f"tts_voice_{timestamp}.mp3"
    
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    print(f"🎯 为飞书生成TTS语音...")
    print(f"📝 文本: {text}")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print(f"📄 文件名: {filename}")
    
    # 生成TTS
    success, temp_file = azure_tts_simple(text, output_path)
    
    if success and temp_file:
        # 复制到目标目录
        import shutil
        shutil.copy2(temp_file, output_path)
        print(f"✅ 语音文件已保存到: {output_path}")
        
        # 验证文件
        file_size = os.path.getsize(output_path)
        print(f"📊 文件大小: {file_size} 字节")
        
        if file_size > 0:
            return output_path
        else:
            print("❌ 文件为空")
            return None
    else:
        print("❌ TTS生成失败")
        return None

if __name__ == "__main__":
    # 默认测试文本
    test_text = "这是飞书语音测试，修复了文件路径问题。"
    
    # 如果提供了命令行参数，使用自定义文本
    if len(sys.argv) > 1:
        test_text = sys.argv[1]
    
    # 生成语音
    voice_file = generate_tts_for_feishu(test_text)
    
    if voice_file:
        print(f"\n🎉 成功! 语音文件: {voice_file}")
        print(f"📤 可以使用此文件发送飞书消息")
    else:
        print("\n❌ 语音生成失败")