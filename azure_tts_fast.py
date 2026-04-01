#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure TTS快速语速版本 - 语速提升30%
"""

import urllib.request
import urllib.error
import json
import os

# Azure TTS配置
AZURE_CONFIG = {
    "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
    "region": "eastasia",
    "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
    "voice": "zh-CN-XiaoxiaoNeural"
}

def azure_tts_fast(text, output_file="/tmp/azure_test_fast.mp3", rate="30%"):
    """Azure TTS - 语速提升"""
    try:
        # 构造SSML - 使用rate属性提升语速
        ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{AZURE_CONFIG["voice"]}'>
        <prosody rate="+{rate}">
            {text}
        </prosody>
    </voice>
</speak>"""
        
        # 请求URL
        url = AZURE_CONFIG["endpoint"]
        
        # 创建请求
        headers = {
            'Ocp-Apim-Subscription-Key': AZURE_CONFIG["key"],
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-48kbitrate-mono-mp3'
        }
        
        print(f"正在请求Azure TTS (语速+{rate})...")
        req = urllib.request.Request(url, data=ssml.encode('utf-8'), headers=headers, method='POST')
        
        # 发送请求
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()
            
            # 保存文件
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"✅ 成功！文件保存到: {output_file}")
            print(f"文件大小: {len(audio_data)} 字节")
            return True, output_file
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP错误: {e.code} - {e.reason}")
        return False, None
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False, None

if __name__ == "__main__":
    print("=" * 50)
    print("Azure TTS 快速语速测试 (+30%)")
    print("=" * 50)
    
    test_text = "Boss，这是语速提升30%的测试语音，听起来应该更快更流畅。"
    
    success, file_path = azure_tts_fast(test_text, rate="30%")
    
    if success:
        print(f"\n🎉 测试完成！")
        print(f"请检查文件: {file_path}")
    else:
        print("\n⚠️ 测试失败")
