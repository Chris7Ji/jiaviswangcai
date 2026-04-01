#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure TTS集成脚本
将文本转换为高质量语音并发送到飞书
"""

import urllib.request
import urllib.error
import os
import tempfile
import time

class AzureTTS:
    """Azure TTS服务封装"""
    
    def __init__(self):
        # Azure TTS配置 - 使用Boss提供的密钥
        self.config = {
            "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
            "region": "eastasia",
            "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
            "voice": "zh-CN-XiaoxiaoNeural",  # 中文女声，自然
            "output_format": "audio-24khz-48kbitrate-mono-mp3"
        }
    
    def text_to_speech(self, text, output_file=None):
        """
        将文本转换为语音
        """
        if not output_file:
            # 创建临时文件
            timestamp = int(time.time())
            output_file = f"/tmp/azure_tts_{timestamp}.mp3"
        
        try:
            # 构造SSML（支持更自然的语音）
            ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{self.config["voice"]}'>
        <prosody rate="0%" pitch="0%">
            {text}
        </prosody>
    </voice>
</speak>"""
            
            # 请求头
            headers = {
                'Ocp-Apim-Subscription-Key': self.config["key"],
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': self.config["output_format"],
                'User-Agent': 'Jarvis-Azure-TTS/1.0'
            }
            
            # 创建请求
            req = urllib.request.Request(
                self.config["endpoint"],
                data=ssml.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            # 发送请求
            response = urllib.request.urlopen(req)
            audio_data = response.read()
            
            # 保存文件
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"✅ Azure TTS成功: {len(text)}字符 → {len(audio_data)}字节")
            return True, output_file, len(audio_data)
            
        except urllib.error.HTTPError as e:
            print(f"❌ Azure TTS HTTP错误 {e.code}: {e.reason}")
            return False, None, 0
        except Exception as e:
            print(f"❌ Azure TTS错误: {str(e)}")
            return False, None, 0
    
    def batch_convert(self, texts):
        """批量转换文本为语音"""
        results = []
        for i, text in enumerate(texts):
            print(f"处理 {i+1}/{len(texts)}: {text[:50]}...")
            success, file_path, size = self.text_to_speech(text)
            if success:
                results.append((text, file_path, size))
            else:
                results.append((text, None, 0))
        return results

def create_tts_wrapper():
    """创建TTS包装器，用于集成到OpenClaw"""
    tts = AzureTTS()
    
    def wrapper(text, user_id="ou_b6c7778820b20031cd97bdc45d1cd9fa"):
        """
        包装器函数：生成语音并发送到飞书
        """
        print(f"为用户 {user_id} 生成语音: {text[:100]}...")
        
        # 生成语音
        success, audio_file, size = tts.text_to_speech(text)
        
        if success and audio_file:
            # 这里可以集成发送逻辑
            # 实际发送会在主程序中处理
            return {
                "success": True,
                "audio_file": audio_file,
                "file_size": size,
                "text_length": len(text)
            }
        else:
            return {
                "success": False,
                "error": "TTS生成失败"
            }
    
    return wrapper

# 测试函数
def test_integration():
    """测试集成功能"""
    print("=" * 60)
    print("Azure TTS 集成测试")
    print("=" * 60)
    
    tts = AzureTTS()
    
    # 测试文本
    test_texts = [
        "Boss，Azure TTS集成测试成功！现在我们可以进行高质量的语音交互了。",
        "这是一条较长的测试消息，用于验证Azure TTS处理长文本的能力。语音合成质量应该非常自然流畅。",
        "明天天气怎么样？需要我带伞吗？"
    ]
    
    for i, text in enumerate(test_texts):
        print(f"\n测试 {i+1}: {text}")
        success, file_path, size = tts.text_to_speech(text)
        
        if success:
            print(f"  生成文件: {file_path}")
            print(f"  文件大小: {size} 字节")
        else:
            print("  生成失败")
    
    print("\n" + "=" * 60)
    print("集成测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    test_integration()
    
    print("\n📋 使用说明:")
    print("1. 导入: from azure_tts_integration import AzureTTS, create_tts_wrapper")
    print("2. 创建实例: tts = AzureTTS()")
    print("3. 生成语音: success, file_path, size = tts.text_to_speech('你的文本')")
    print("4. 或使用包装器: tts_wrapper = create_tts_wrapper()")
    print("5. 结果: result = tts_wrapper('要转换的文本')")