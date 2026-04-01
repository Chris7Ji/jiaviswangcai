#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure TTS正确端点测试
根据Azure文档，正确的TTS端点是：
https://{region}.tts.speech.microsoft.com/cognitiveservices/v1
"""

import urllib.request
import urllib.error
import os

# Azure TTS配置 - 使用正确的端点格式
AZURE_CONFIG = {
    "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
    "region": "eastasia",
    # 正确的TTS端点格式
    "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
    "voice": "zh-CN-XiaoxiaoNeural"
}

def test_azure_tts_correct():
    """测试正确的Azure TTS端点"""
    try:
        # 构造SSML
        ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{AZURE_CONFIG["voice"]}'>
        测试Azure TTS语音合成功能。这是一条测试消息。
    </voice>
</speak>"""
        
        # 请求头
        headers = {
            'Ocp-Apim-Subscription-Key': AZURE_CONFIG["key"],
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3',
            'User-Agent': 'Jarvis-TTS-Test'
        }
        
        print(f"使用端点: {AZURE_CONFIG['endpoint']}")
        print(f"区域: {AZURE_CONFIG['region']}")
        print(f"语音: {AZURE_CONFIG['voice']}")
        
        # 创建请求
        req = urllib.request.Request(
            AZURE_CONFIG["endpoint"],
            data=ssml.encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        # 发送请求
        response = urllib.request.urlopen(req)
        audio_data = response.read()
        
        # 保存文件
        output_file = "/tmp/azure_tts_correct.mp3"
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        print(f"✅ 成功！HTTP状态码: {response.status}")
        print(f"文件保存到: {output_file}")
        print(f"文件大小: {len(audio_data)} 字节")
        
        return True, output_file
        
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        print(f"响应头: {e.headers}")
        
        # 尝试读取错误信息
        try:
            error_body = e.read().decode('utf-8')
            print(f"错误详情: {error_body}")
        except:
            pass
            
        return False, None
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False, None

if __name__ == "__main__":
    print("=" * 60)
    print("Azure TTS 正确端点测试")
    print("=" * 60)
    
    success, file_path = test_azure_tts_correct()
    
    if success:
        print(f"\n🎉 测试成功！")
        print(f"音频文件: {file_path}")
        
        # 检查文件
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"文件大小: {size} 字节")
            print("✅ 可以发送测试语音")
    else:
        print("\n⚠️ 测试失败，尝试其他方案")