#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure TTS测试脚本
使用Azure认知服务语音合成
"""

import os
import requests
import json
import time
from pathlib import Path

# Azure TTS配置 - 使用Boss提供的密钥
AZURE_TTS_CONFIG = {
    "subscription_key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",  # 使用第一个密钥
    "region": "eastasia",
    "endpoint": "https://eastasia.api.cognitive.microsoft.com/",
    "voice_name": "zh-CN-XiaoxiaoNeural",  # 中文女声，声音自然
    "output_format": "audio-24khz-48kbitrate-mono-mp3"
}

def text_to_speech_azure(text, output_file="azure_tts_output.mp3"):
    """
    使用Azure TTS将文本转换为语音
    """
    try:
        # 构造请求URL
        tts_url = f"{AZURE_TTS_CONFIG['endpoint']}cognitiveservices/v1"
        
        # 请求头
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_TTS_CONFIG['subscription_key'],
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": AZURE_TTS_CONFIG['output_format'],
            "User-Agent": "Jarvis-TTS-Test"
        }
        
        # SSML格式的请求体
        ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' xml:gender='Female' name='{AZURE_TTS_CONFIG['voice_name']}'>
        <prosody rate='0%' pitch='0%'>
            {text}
        </prosody>
    </voice>
</speak>"""
        
        print(f"正在请求Azure TTS服务...")
        print(f"区域: {AZURE_TTS_CONFIG['region']}")
        print(f"语音: {AZURE_TTS_CONFIG['voice_name']}")
        print(f"文本长度: {len(text)} 字符")
        
        # 发送请求
        response = requests.post(tts_url, headers=headers, data=ssml.encode('utf-8'))
        
        if response.status_code == 200:
            # 保存音频文件
            with open(output_file, 'wb') as audio_file:
                audio_file.write(response.content)
            
            file_size = os.path.getsize(output_file)
            print(f"✅ TTS成功！文件已保存: {output_file}")
            print(f"文件大小: {file_size} 字节")
            return True, output_file
        else:
            print(f"❌ TTS失败！状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False, None

def test_azure_tts():
    """测试Azure TTS功能"""
    print("=" * 60)
    print("Azure TTS 功能测试")
    print("=" * 60)
    
    # 测试文本
    test_text = "Boss，Azure TTS测试成功！这是使用Azure认知服务生成的语音消息，声音质量应该比之前的工具好很多。现在我们可以用这个进行语音交互了。"
    
    print(f"测试文本: {test_text}")
    print("-" * 60)
    
    # 生成语音
    output_file = "/tmp/azure_tts_test.mp3"
    success, file_path = text_to_speech_azure(test_text, output_file)
    
    if success:
        print(f"\n🎉 测试完成！")
        print(f"音频文件: {file_path}")
        
        # 检查文件
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"文件大小: {size} 字节")
            print(f"文件可正常访问")
            
            # 返回文件路径供发送
            return file_path
        else:
            print("❌ 文件未生成")
            return None
    else:
        print("❌ TTS测试失败")
        return None

if __name__ == "__main__":
    # 运行测试
    audio_file = test_azure_tts()
    
    if audio_file:
        print(f"\n📁 音频文件路径: {audio_file}")
        print("请使用此文件进行发送测试")
    else:
        print("\n⚠️ 测试失败，请检查配置")