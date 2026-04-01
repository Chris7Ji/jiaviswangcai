#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure TTS简单测试脚本 - 使用urllib
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

def azure_tts_simple(text, output_file="/tmp/azure_test.mp3"):
    """简单的Azure TTS测试"""
    try:
        # 构造SSML
        ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{AZURE_CONFIG["voice"]}'>
        {text}
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
        
        print("正在请求Azure TTS...")
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
        if e.code == 401:
            print("可能原因: API密钥错误或已过期")
        elif e.code == 404:
            print("可能原因: 终结点URL错误")
        return False, None
    except Exception as e:
        print(f"❌ 错误: {str(e)}")
        return False, None

# 测试
if __name__ == "__main__":
    print("=" * 50)
    print("Azure TTS 快速测试")
    print("=" * 50)
    
    test_text = "Boss，Azure TTS测试成功！这是高质量的语音合成。"
    
    success, file_path = azure_tts_simple(test_text)
    
    if success:
        print(f"\n🎉 测试完成！")
        print(f"请检查文件: {file_path}")
        
        # 显示文件信息
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"文件大小: {size} 字节")
            print(f"✅ 可以发送测试")
    else:
        print("\n⚠️ 测试失败")