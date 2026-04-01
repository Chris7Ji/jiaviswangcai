#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jarvis最终版自动语音回复系统
配置：+30%语速，0%音调，XiaoyiNeural音色
"""

import urllib.request
import urllib.error
import os
import time
import hashlib
import json

class JarvisVoiceSystem:
    """Jarvis最终语音系统 - Boss选择的配置"""
    
    VERSION = "1.0"
    CONFIG_NAME = "Boss精选配置"
    
    def __init__(self, azure_key=None):
        # Boss最终选择的配置
        self.config = {
            "key": azure_key or "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
            "endpoint": "https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1",
            "voice": "zh-CN-XiaoyiNeural",      # Boss选择：年轻女声，更活泼
            "speed": "+30%",                     # Boss选择：比正常快30%
            "pitch": "0%",                       # Boss选择：正常音调
            "output_format": "audio-24khz-48kbitrate-mono-mp3",
            "volume": "+0%"                      # 正常音量
        }
        
        # 系统配置
        self.cache_dir = "/tmp/jarvis_voice_cache"
        self.stats_file = f"{self.cache_dir}/stats.json"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 加载统计
        self.stats = self._load_stats()
        
        print(f"🚀 Jarvis语音系统 v{self.VERSION}")
        print(f"   配置: {self.CONFIG_NAME}")
        print(f"   音色: {self.config['voice']}")
        print(f"   语速: {self.config['speed']}")
        print(f"   音调: {self.config['pitch']}")
    
    def _load_stats(self):
        """加载统计信息"""
        default_stats = {
            "total_requests": 0,
            "successful": 0,
            "failed": 0,
            "total_chars": 0,
            "total_audio_bytes": 0,
            "total_time": 0.0,
            "config_name": self.CONFIG_NAME,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return default_stats
    
    def _save_stats(self):
        """保存统计信息"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def text_to_speech(self, text, use_cache=True):
        """
        将文本转换为语音 - 使用Boss选择的配置
        返回: (success, file_path, audio_size, response_time)
        """
        start_time = time.time()
        self.stats["total_requests"] += 1
        self.stats["total_chars"] += len(text)
        
        try:
            # 生成缓存文件名
            if use_cache:
                text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:16]
                cache_file = f"{self.cache_dir}/boss_{text_hash}.mp3"
                
                # 检查缓存
                if os.path.exists(cache_file):
                    file_size = os.path.getsize(cache_file)
                    response_time = time.time() - start_time
                    self.stats["successful"] += 1
                    self.stats["total_audio_bytes"] += file_size
                    self.stats["total_time"] += response_time
                    self._save_stats()
                    
                    print(f"⚡ 缓存命中: {len(text)}字符")
                    return True, cache_file, file_size, response_time
            else:
                timestamp = int(time.time() * 1000)
                cache_file = f"{self.cache_dir}/temp_{timestamp}.mp3"
            
            # 构造SSML - 使用Boss选择的配置
            ssml = f"""<speak version='1.0' xml:lang='zh-CN'>
    <voice xml:lang='zh-CN' name='{self.config["voice"]}'>
        <prosody rate='{self.config["speed"]}' 
                 pitch='{self.config["pitch"]}' 
                 volume='{self.config["volume"]}'>
            {text}
        </prosody>
    </voice>
</speak>"""
            
            # 请求头
            headers = {
                'Ocp-Apim-Subscription-Key': self.config["key"],
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': self.config["output_format"],
                'User-Agent': f'Jarvis-Voice/{self.VERSION}'
            }
            
            # 发送请求
            req = urllib.request.Request(
                self.config["endpoint"],
                data=ssml.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            response = urllib.request.urlopen(req, timeout=20)
            audio_data = response.read()
            
            # 保存文件
            with open(cache_file, 'wb') as f:
                f.write(audio_data)
            
            response_time = time.time() - start_time
            self.stats["successful"] += 1
            self.stats["total_audio_bytes"] += len(audio_data)
            self.stats["total_time"] += response_time
            self._save_stats()
            
            print(f"✅ 语音生成: {len(text)}字符 → {len(audio_data)}字节 ({response_time:.2f}秒)")
            return True, cache_file, len(audio_data), response_time
            
        except urllib.error.HTTPError as e:
            response_time = time.time() - start_time
            self.stats["failed"] += 1
            self.stats["total_time"] += response_time
            self._save_stats()
            
            print(f"❌ HTTP错误 {e.code}: {e.reason}")
            return False, None, 0, response_time
        except Exception as e:
            response_time = time.time() - start_time
            self.stats["failed"] += 1
            self.stats["total_time"] += response_time
            self._save_stats()
            
            print(f"❌ 错误: {str(e)}")
            return False, None, 0, response_time
    
    def generate_reply_with_voice(self, user_message):
        """
        生成AI回复并转换为语音
        返回完整的回复数据
        """
        print("=" * 60)
        print(f"💬 用户: {user_message[:100]}...")
        print("-" * 60)
        
        # 生成AI回复（这里应该调用实际的AI模型）
        ai_reply = self._generate_ai_reply(user_message)
        print(f"🤖 AI回复: {ai_reply[:100]}...")
        
        # 生成语音
        voice_start = time.time()
        success, audio_file, audio_size, gen_time = self.text_to_speech(ai_reply)
        
        result = {
            "success": success,
            "user_message": user_message,
            "ai_reply": ai_reply,
            "reply_length": len(ai_reply),
            "voice_generated": success,
            "voice_file": audio_file if success else None,
            "voice_size": audio_size if success else 0,
            "generation_time": gen_time,
            "config": {
                "voice": self.config["voice"],
                "speed": self.config["speed"],
                "pitch": self.config["pitch"]
            }
        }
        
        if success:
            total_time = time.time() - voice_start
            result["total_time"] = total_time
            
            print(f"\n🎉 回复完成!")
            print(f"   文字: {len(ai_reply)}字符")
            print(f"   语音: {audio_size}字节")
            print(f"   生成: {gen_time:.2f}秒")
            print(f"   总计: {total_time:.2f}秒")
        else:
            print(f"\n⚠️ 语音生成失败，仅文字回复")
        
        return result
    
    def _generate_ai_reply(self, user_message):
        """生成AI回复（模拟函数）"""
        # 这里应该调用DeepSeek等AI模型
        # 暂时返回模拟回复
        
        # 简单回复逻辑
        user_lower = user_message.lower()
        
        if any(word in user_lower for word in ["你好", "嗨", "hello"]):
            return "Boss，您好！我是Jarvis，现在使用您选择的配置为您服务：XiaoyiNeural音色，+30%语速。"
        
        elif any(word in user_lower for word in ["时间", "几点", "现在"]):
            current_time = time.strftime("%Y年%m月%d日 %H:%M:%S")
            return f"Boss，现在是{current_time}，北京时间。"
        
        elif any(word in user_lower for word in ["天气", "温度", "下雨"]):
            return "今天天气晴朗，温度20-25度，东南风2-3级，适合外出。"
        
        elif any(word in user_lower for word in ["测试", "语音", "声音"]):
            return "这是语音测试回复。使用XiaoyiNeural音色，+30%语速，0%音调。声音应该清晰活泼。"
        
        else:
            return f"Boss，收到您的消息：'{user_message[:50]}...'。这是使用您精选配置的自动语音回复。"
    
    def get_system_info(self):
        """获取系统信息"""
        total_requests = self.stats["total_requests"]
        success_rate = (self.stats["successful"] / total_requests * 100) if total_requests > 0 else 0
        avg_time = (self.stats["total_time"] / total_requests) if total_requests > 0 else 0
        
        return {
            "系统版本": self.VERSION,
            "配置名称": self.CONFIG_NAME,
            "语音配置": {
                "音色": self.config["voice"],
                "语速": self.config["speed"],
                "音调": self.config["pitch"],
                "音量": self.config["volume"]
            },
            "性能统计": {
                "总请求数": total_requests,
                "成功数": self.stats["successful"],
                "失败数": self.stats["failed"],
                "成功率": f"{success_rate:.1f}%",
                "总字符数": self.stats["total_chars"],
                "总音频大小": f"{self.stats['total_audio_bytes'] / 1024:.1f} KB",
                "平均响应时间": f"{avg_time:.2f}秒"
            },
            "缓存目录": self.cache_dir,
            "创建时间": self.stats.get("created_at", "未知")
        }

def test_final_configuration():
    """测试最终配置"""
    print("🎯 Jarvis最终语音系统测试")
    print("=" * 60)
    print("配置确认:")
    print(f"   音色: zh-CN-XiaoyiNeural (年轻女声，更活泼)")
    print(f"   语速: +30% (比正常快30%)")
    print(f"   音调: 0% (正常音调)")
    print("=" * 60)
    
    system = JarvisVoiceSystem()
    
    # 测试消息
    test_cases = [
        "你好，Jarvis",
        "测试一下语音系统",
        "现在几点了？",
        "今天的天气怎么样？",
        "这个配置我很满意"
    ]
    
    results = []
    for i, message in enumerate(test_cases):
        print(f"\n测试 {i+1}/{len(test_cases)}: '{message}'")
        result = system.generate_reply_with_voice(message)
        results.append(result)
        
        if result["success"] and result["voice_generated"]:
            print(f"   ✅ 成功 (生成: {result['generation_time']:.2f}秒)")
        else:
            print(f"   ⚠️ 失败")
        
        time.sleep(1)
    
    # 显示系统信息
    print("\n" + "=" * 60)
    print("📊 系统信息:")
    info = system.get_system_info()
    
    print(f"   版本: {info['系统版本']}")
    print(f"   配置: {info['配置名称']}")
    print(f"   音色: {info['语音配置']['音色']}")
    print(f"   语速: {info['语音配置']['语速']}")
    print(f"   音调: {info['语音配置']['音调']}")
    
    stats = info['性能统计']
    print(f"\n   性能统计:")
    print(f"     总请求: {stats['总请求数']}")
    print(f"     成功率: {stats['成功率']}")
    print(f"     平均响应: {stats['平均响应时间']}")
    
    print("\n🎉 最终配置测试完成！")
    print("系统已准备好自动语音回复。")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    test_final_configuration()
    
    print("\n📋 使用说明:")
    print("1. 创建系统: system = JarvisVoiceSystem(azure_key='您的密钥')")
    print("2. 生成回复: result = system.generate_reply_with_voice('用户消息')")
    print("3. 获取信息: info = system.get_system_info()")
    print("\n💡 提示: 实际使用需要集成到OpenClaw的消息处理流程中")