#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动语音回复系统
集成Azure TTS，自动将回复转换为语音并发送
"""

import urllib.request
import urllib.error
import os
import time
import json

class AutoVoiceSystem:
    """自动语音回复系统"""
    
    def __init__(self):
        # Azure TTS配置
        self.azure_config = {
            "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
            "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
            "voice": "zh-CN-XiaoxiaoNeural",
            "output_format": "audio-24khz-48kbitrate-mono-mp3"
        }
        
        # 飞书配置
        self.feishu_user_id = "ou_b6c7778820b20031cd97bdc45d1cd9fa"
        
        # 缓存目录
        self.cache_dir = "/tmp/tts_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def generate_voice(self, text):
        """使用Azure TTS生成语音"""
        try:
            # 生成文件名（基于文本内容的哈希）
            import hashlib
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
            timestamp = int(time.time())
            output_file = f"{self.cache_dir}/voice_{text_hash}_{timestamp}.mp3"
            
            # 检查缓存
            if os.path.exists(output_file):
                print(f"使用缓存语音: {output_file}")
                return True, output_file, os.path.getsize(output_file)
            
            # 构造SSML
            ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{self.azure_config["voice"]}'>
        <prosody rate="0%" pitch="0%">
            {text}
        </prosody>
    </voice>
</speak>"""
            
            # 请求头
            headers = {
                'Ocp-Apim-Subscription-Key': self.azure_config["key"],
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': self.azure_config["output_format"],
                'User-Agent': 'Jarvis-Auto-Voice/1.0'
            }
            
            # 发送请求
            req = urllib.request.Request(
                self.azure_config["endpoint"],
                data=ssml.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            response = urllib.request.urlopen(req, timeout=10)
            audio_data = response.read()
            
            # 保存文件
            with open(output_file, 'wb') as f:
                f.write(audio_data)
            
            print(f"✅ 生成语音: {len(text)}字符 → {len(audio_data)}字节")
            return True, output_file, len(audio_data)
            
        except urllib.error.HTTPError as e:
            print(f"❌ TTS HTTP错误 {e.code}")
            return False, None, 0
        except Exception as e:
            print(f"❌ TTS错误: {str(e)}")
            return False, None, 0
    
    def send_to_feishu(self, text, audio_file):
        """发送文字和语音到飞书（模拟）"""
        # 实际发送需要通过OpenClaw的message工具
        # 这里返回模拟结果
        
        if not audio_file or not os.path.exists(audio_file):
            print("⚠️ 音频文件不存在，只发送文字")
            return {
                "text_sent": True,
                "audio_sent": False,
                "audio_file": None
            }
        
        file_size = os.path.getsize(audio_file)
        print(f"📤 准备发送到飞书:")
        print(f"   文字: {text[:100]}...")
        print(f"   语音: {audio_file} ({file_size}字节)")
        print(f"   收件人: {self.feishu_user_id}")
        
        return {
            "text_sent": True,
            "audio_sent": True,
            "audio_file": audio_file,
            "file_size": file_size,
            "user_id": self.feishu_user_id
        }
    
    def auto_reply(self, user_text, bot_reply_text):
        """
        自动回复流程：
        1. 生成回复文字的语音
        2. 发送文字+语音到飞书
        """
        print("=" * 60)
        print(f"用户消息: {user_text[:100]}...")
        print(f"AI回复: {bot_reply_text[:100]}...")
        print("-" * 60)
        
        # 生成语音
        voice_success, audio_file, audio_size = self.generate_voice(bot_reply_text)
        
        if voice_success:
            # 发送到飞书
            send_result = self.send_to_feishu(bot_reply_text, audio_file)
            
            print(f"\n🎉 自动回复完成!")
            print(f"   文字长度: {len(bot_reply_text)}字符")
            print(f"   语音文件: {audio_file}")
            print(f"   语音大小: {audio_size}字节")
            
            return {
                "success": True,
                "text": bot_reply_text,
                "audio_file": audio_file,
                "audio_size": audio_size,
                "send_result": send_result
            }
        else:
            print(f"\n⚠️ 语音生成失败，只发送文字")
            send_result = self.send_to_feishu(bot_reply_text, None)
            
            return {
                "success": False,
                "text": bot_reply_text,
                "audio_file": None,
                "error": "语音生成失败",
                "send_result": send_result
            }

def test_auto_system():
    """测试自动语音系统"""
    print("🤖 自动语音回复系统测试")
    print("=" * 60)
    
    system = AutoVoiceSystem()
    
    # 测试对话
    test_conversations = [
        {
            "user": "你好，今天天气怎么样？",
            "bot": "Boss，今天天气不错，晴天，温度在20-25度之间，适合外出。"
        },
        {
            "user": "帮我查一下明天的日程安排",
            "bot": "好的，Boss。根据您的日历，明天上午10点有团队会议，下午2点需要审阅项目报告，晚上7点有个线上分享会。"
        },
        {
            "user": "Azure TTS语音质量怎么样？",
            "bot": "Azure TTS的语音质量非常好！这是目前最先进的语音合成技术之一，声音自然流畅，几乎听不出是机器生成的。我们已经成功配置并测试通过。"
        }
    ]
    
    for i, conv in enumerate(test_conversations):
        print(f"\n测试对话 {i+1}/{len(test_conversations)}")
        result = system.auto_reply(conv["user"], conv["bot"])
        
        if result["success"]:
            print(f"   ✅ 成功生成语音")
        else:
            print(f"   ⚠️ 仅发送文字")
        
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "=" * 60)
    print("测试完成！系统已准备好自动语音回复。")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    test_auto_system()
    
    print("\n📋 使用说明:")
    print("1. 创建系统: system = AutoVoiceSystem()")
    print("2. 自动回复: result = system.auto_reply(用户消息, AI回复)")
    print("3. 结果包含文字和语音文件路径")
    print("\n💡 提示: 实际发送需要集成OpenClaw的message工具")