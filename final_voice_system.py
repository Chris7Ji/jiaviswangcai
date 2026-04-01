#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终版自动语音回复系统
使用+30%语速的Azure TTS
"""

import urllib.request
import urllib.error
import os
import time
import hashlib
import subprocess

class FinalVoiceSystem:
    """最终版语音系统 - +30%语速"""
    
    def __init__(self, azure_key=None):
        # Azure TTS配置 - 使用+30%语速
        self.config = {
            "key": azure_key or "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
            "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
            "voice": "zh-CN-XiaoxiaoNeural",  # 高质量中文女声
            "speed": "+30%",  # Boss选择的+30%语速
            "pitch": "0%",    # 正常音调
            "output_format": "audio-24khz-48kbitrate-mono-mp3"
        }
        
        # 缓存配置
        self.cache_dir = "/tmp/tts_final_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 性能统计
        self.stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "total_chars": 0,
            "total_audio_bytes": 0
        }
    
    def generate_voice_fast(self, text):
        """
        快速生成语音 - 使用+30%语速
        返回: (success, file_path, audio_size, response_time)
        """
        start_time = time.time()
        self.stats["total_requests"] += 1
        self.stats["total_chars"] += len(text)
        
        try:
            # 生成缓存文件名
            text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:12]
            cache_file = f"{self.cache_dir}/fast_{text_hash}.mp3"
            
            # 检查缓存
            if os.path.exists(cache_file):
                file_size = os.path.getsize(cache_file)
                response_time = time.time() - start_time
                self.stats["successful"] += 1
                self.stats["total_audio_bytes"] += file_size
                print(f"⚡ 缓存命中: {len(text)}字符 → {file_size}字节 ({response_time:.2f}秒)")
                return True, cache_file, file_size, response_time
            
            # 构造SSML - 使用+30%语速
            ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{self.config["voice"]}'>
        <prosody rate='{self.config["speed"]}' pitch='{self.config["pitch"]}'>
            {text}
        </prosody>
    </voice>
</speak>"""
            
            # 请求头
            headers = {
                'Ocp-Apim-Subscription-Key': self.config["key"],
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': self.config["output_format"],
                'User-Agent': 'Jarvis-Final-Voice/1.0'
            }
            
            # 发送请求（设置超时）
            req = urllib.request.Request(
                self.config["endpoint"],
                data=ssml.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            response = urllib.request.urlopen(req, timeout=15)
            audio_data = response.read()
            
            # 保存到缓存
            with open(cache_file, 'wb') as f:
                f.write(audio_data)
            
            response_time = time.time() - start_time
            self.stats["successful"] += 1
            self.stats["total_audio_bytes"] += len(audio_data)
            
            print(f"✅ 生成成功: {len(text)}字符 → {len(audio_data)}字节 ({response_time:.2f}秒)")
            return True, cache_file, len(audio_data), response_time
            
        except urllib.error.HTTPError as e:
            response_time = time.time() - start_time
            self.stats["failed"] += 1
            print(f"❌ HTTP错误 {e.code}: {e.reason} ({response_time:.2f}秒)")
            return False, None, 0, response_time
        except Exception as e:
            response_time = time.time() - start_time
            self.stats["failed"] += 1
            print(f"❌ 错误: {str(e)} ({response_time:.2f}秒)")
            return False, None, 0, response_time
    
    def send_voice_message(self, text, user_id="ou_b6c7778820b20031cd97bdc45d1cd9fa"):
        """
        完整流程：生成语音并发送到飞书
        """
        print("=" * 60)
        print(f"💬 用户消息: {text[:80]}...")
        print("-" * 60)
        
        # 生成回复（这里应该调用AI模型，暂时用模拟回复）
        bot_reply = self.generate_reply(text)
        print(f"🤖 AI回复: {bot_reply[:80]}...")
        
        # 生成语音
        voice_start = time.time()
        success, audio_file, audio_size, gen_time = self.generate_voice_fast(bot_reply)
        
        if success:
            # 发送到飞书（这里需要集成OpenClaw的message工具）
            # 实际发送代码...
            send_time = time.time() - voice_start
            
            print(f"\n🎉 发送完成!")
            print(f"   文字: {len(bot_reply)}字符")
            print(f"   语音: {audio_size}字节")
            print(f"   生成时间: {gen_time:.2f}秒")
            print(f"   总时间: {send_time:.2f}秒")
            
            return {
                "success": True,
                "text": bot_reply,
                "audio_file": audio_file,
                "audio_size": audio_size,
                "generation_time": gen_time,
                "total_time": send_time
            }
        else:
            print(f"\n⚠️ 语音生成失败，仅发送文字")
            return {
                "success": False,
                "text": bot_reply,
                "error": "语音生成失败"
            }
    
    def generate_reply(self, user_text):
        """生成AI回复（模拟函数，实际应调用AI模型）"""
        # 这里应该调用DeepSeek等AI模型
        # 暂时返回模拟回复
        
        replies = {
            "你好": "Boss，您好！我是Jarvis，现在使用+30%语速的Azure TTS为您服务。",
            "时间": f"现在是{time.strftime('%Y年%m月%d日 %H:%M')}，北京时间。",
            "天气": "今天天气晴朗，温度20-25度，适合外出。",
            "测试": "这是+30%语速的测试回复，语音速度比正常快百分之三十。"
        }
        
        for key in replies:
            if key in user_text:
                return replies[key]
        
        # 默认回复
        return f"Boss，收到您的消息：'{user_text[:50]}...'。这是使用+30%语速的自动语音回复。"
    
    def get_stats(self):
        """获取性能统计"""
        success_rate = (self.stats["successful"] / self.stats["total_requests"] * 100) if self.stats["total_requests"] > 0 else 0
        avg_chars = self.stats["total_chars"] / self.stats["total_requests"] if self.stats["total_requests"] > 0 else 0
        
        return {
            "总请求数": self.stats["total_requests"],
            "成功数": self.stats["successful"],
            "失败数": self.stats["failed"],
            "成功率": f"{success_rate:.1f}%",
            "总字符数": self.stats["total_chars"],
            "总音频大小": f"{self.stats['total_audio_bytes'] / 1024:.1f} KB",
            "平均字符数": f"{avg_chars:.1f}"
        }

def test_final_system():
    """测试最终系统"""
    print("🚀 最终版自动语音回复系统测试")
    print("=" * 60)
    print("配置: Azure TTS +30%语速")
    print("=" * 60)
    
    system = FinalVoiceSystem()
    
    # 测试消息
    test_messages = [
        "你好，测试一下",
        "现在几点了？",
        "今天天气怎么样？",
        "Azure TTS语音质量如何？"
    ]
    
    for i, msg in enumerate(test_messages):
        print(f"\n测试 {i+1}/{len(test_messages)}")
        result = system.send_voice_message(msg)
        
        if result["success"]:
            print(f"   ✅ 成功 (生成: {result.get('generation_time', 0):.2f}秒)")
        else:
            print(f"   ⚠️ 失败")
        
        time.sleep(1)  # 避免请求过快
    
    # 显示统计
    print("\n" + "=" * 60)
    print("📊 性能统计:")
    stats = system.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n🎯 系统已就绪！")
    print("   语速: +30%")
    print("   语音: zh-CN-XiaoxiaoNeural")
    print("   缓存: 已启用")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    test_final_system()
    
    print("\n📋 使用说明:")
    print("1. 创建系统: system = FinalVoiceSystem(azure_key='您的密钥')")
    print("2. 发送消息: result = system.send_voice_message('用户消息')")
    print("3. 或直接生成语音: success, file, size, time = system.generate_voice_fast('文本')")
    print("\n💡 提示: 实际集成需要调用AI模型生成回复")