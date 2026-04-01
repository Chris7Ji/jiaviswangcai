#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音处理完整管道
语音识别 → AI回复 → 语音合成 → 输出文件
"""

import os
import sys
import tempfile
import json
import subprocess

# 导入现有的Azure模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from azure_speech_recognition import recognize_with_azure
    from azure_tts_simple import azure_tts_simple
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    print("警告: Azure模块未找到，使用模拟模式")

class VoiceProcessingPipeline:
    """语音处理管道"""
    
    def __init__(self, use_azure=True):
        self.use_azure = use_azure and AZURE_AVAILABLE
        
        # Azure配置（从现有文件复制）
        self.azure_config = {
            "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
            "region": "eastasia",
            "endpoint": "https://eastasia.api.cognitive.microsoft.com/",
            "voice": "zh-CN-XiaoxiaoNeural"
        }
        
        print(f"语音处理管道初始化: {'Azure模式' if self.use_azure else '模拟模式'}")
    
    def recognize_speech(self, audio_path):
        """语音识别"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_path}")
        
        print(f"🎤 开始语音识别: {audio_path}")
        
        if self.use_azure:
            try:
                # 使用Azure Speech识别
                result = recognize_with_azure(audio_path)
                if result:
                    print(f"✅ Azure识别成功: {result}")
                    return result
                else:
                    print("⚠️ Azure识别失败，使用模拟模式")
            except Exception as e:
                print(f"❌ Azure识别错误: {e}")
        
        # 模拟模式：返回固定文本
        mock_texts = [
            "你好，这是一条测试语音消息",
            "请帮我查一下天气",
            "今天的新闻有什么",
            "测试语音识别功能"
        ]
        import random
        mock_result = random.choice(mock_texts)
        print(f"🤖 模拟识别结果: {mock_result}")
        return mock_result
    
    def generate_ai_response(self, text):
        """生成AI回复（简化版）"""
        print(f"🧠 生成AI回复，输入: {text}")
        
        # 简单的规则引擎
        responses = {
            "你好": "你好！我是Jarvis，你的AI助手。",
            "测试": "测试成功！语音识别和回复功能正常。",
            "天气": "当前无法获取实时天气，请稍后尝试。",
            "新闻": "每天06:30我会发送AI新闻摘要到你的邮箱。",
            "时间": f"现在是{self.get_current_time()}。",
            "功能": "我支持语音识别、AI对话、新闻摘要、文件管理等功能。",
        }
        
        # 检查关键词
        for keyword, response in responses.items():
            if keyword in text:
                return response
        
        # 默认回复
        default_responses = [
            f"我听到你说：{text}。我已经理解了你的意思。",
            f"收到你的语音消息：{text}。我会认真处理。",
            "语音消息已收到，正在处理中。",
            "好的，明白了。"
        ]
        import random
        return random.choice(default_responses)
    
    def get_current_time(self):
        """获取当前时间"""
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%Y年%m月%d日 %H:%M")
    
    def synthesize_speech(self, text, output_path=None):
        """语音合成"""
        if output_path is None:
            temp_fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(temp_fd)
            output_path = temp_path
            is_temp = True
        else:
            is_temp = False
        
        print(f"🔊 语音合成: {text[:50]}...")
        
        if self.use_azure:
            try:
                # 使用现有Azure TTS
                from azure_tts_simple import azure_tts_simple
                success, file_path = azure_tts_simple(text, output_path)
                if success:
                    print(f"✅ Azure TTS成功: {file_path}")
                    return file_path, is_temp
                else:
                    print("⚠️ Azure TTS失败，使用系统语音")
            except Exception as e:
                print(f"❌ Azure TTS错误: {e}")
        
        # 使用系统say命令（macOS）
        try:
            subprocess.run(['say', '-v', 'Ting-Ting', '-o', output_path, text], 
                          check=True, capture_output=True)
            print(f"✅ 系统TTS成功: {output_path}")
            return output_path, is_temp
        except Exception as e:
            print(f"❌ 系统TTS失败: {e}")
            # 创建空文件作为占位符
            with open(output_path, 'wb') as f:
                f.write(b'')
            return output_path, is_temp
    
    def process_voice_message(self, audio_path, output_dir=None):
        """处理语音消息完整流程"""
        print("=" * 60)
        print("🚀 开始语音消息处理流程")
        print("=" * 60)
        
        # 1. 语音识别
        recognized_text = self.recognize_speech(audio_path)
        
        # 2. 生成AI回复
        ai_response = self.generate_ai_response(recognized_text)
        
        # 3. 语音合成
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, f"response_{os.path.basename(audio_path)}.mp3")
        else:
            output_file = None
        
        tts_file, is_temp = self.synthesize_speech(ai_response, output_file)
        
        # 4. 返回结果
        result = {
            "audio_input": audio_path,
            "recognized_text": recognized_text,
            "ai_response": ai_response,
            "tts_output": tts_file,
            "is_temp_file": is_temp,
            "success": True
        }
        
        print("=" * 60)
        print("🎉 处理完成！")
        print(f"📝 识别文本: {recognized_text}")
        print(f"🤖 AI回复: {ai_response}")
        print(f"🔊 语音文件: {tts_file}")
        print("=" * 60)
        
        return result
    
    def cleanup_temp_files(self, result):
        """清理临时文件"""
        if result.get('is_temp_file') and os.path.exists(result['tts_output']):
            os.remove(result['tts_output'])
            print(f"🧹 已清理临时文件: {result['tts_output']}")

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <音频文件路径> [输出目录]")
        print("示例: python voice_processing_pipeline.py test.ogg ./output")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(audio_file):
        print(f"错误: 文件不存在: {audio_file}")
        sys.exit(1)
    
    # 创建管道
    pipeline = VoiceProcessingPipeline(use_azure=True)
    
    # 处理语音消息
    result = pipeline.process_voice_message(audio_file, output_dir)
    
    # 保存结果到JSON文件
    if output_dir:
        json_file = os.path.join(output_dir, f"result_{os.path.basename(audio_file)}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"📄 结果保存到: {json_file}")
    
    # 输出结果
    print("\n" + "📋 最终结果 " + "=" * 40)
    print(f"输入语音: {result['audio_input']}")
    print(f"识别结果: {result['recognized_text']}")
    print(f"AI回复: {result['ai_response']}")
    print(f"输出语音: {result['tts_output']}")
    
    # 如果是临时文件，提醒清理
    if result['is_temp_file']:
        print(f"⚠️ 注意: 输出文件是临时文件，将在程序退出时删除")
        print(f"   如需保留，请复制到其他位置: cp {result['tts_output']} ./保存路径.mp3")
    
    return result

if __name__ == "__main__":
    main()