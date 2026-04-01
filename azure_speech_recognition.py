#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure Speech-to-Text (语音识别) 测试脚本
使用现有Azure TTS密钥配置
"""

import os
import sys
import time
import subprocess
import tempfile

# 从现有TTS配置导入
AZURE_CONFIG = {
    "key": "1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P",
    "region": "eastasia",
    "endpoint": "https://eastasia.api.cognitive.microsoft.com/",
}

def convert_audio_to_wav(input_path, output_path=None):
    """转换音频为Azure Speech需要的格式：16kHz, 16bit, 单声道"""
    if output_path is None:
        temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
        os.close(temp_fd)
        output_path = temp_path
        is_temp = True
    else:
        is_temp = False
    
    cmd = [
        'ffmpeg', '-i', input_path,
        '-ar', '16000',          # 采样率16kHz
        '-ac', '1',              # 单声道
        '-acodec', 'pcm_s16le',  # 16位PCM
        '-y',                    # 覆盖输出文件
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ 音频转换完成: {input_path} -> {output_path}")
        return output_path, is_temp
    except subprocess.CalledProcessError as e:
        print(f"❌ 音频转换失败: {e}")
        if is_temp and os.path.exists(output_path):
            os.remove(output_path)
        raise

def test_azure_speech_offline():
    """测试Azure Speech SDK是否可用（不实际调用API）"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        print("✅ Azure Speech SDK可导入")
        
        # 创建配置对象（不实际连接）
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_CONFIG["key"],
            region=AZURE_CONFIG["region"]
        )
        print(f"✅ 配置创建成功: region={AZURE_CONFIG['region']}")
        
        # 检查语言支持
        speech_config.speech_recognition_language = "zh-CN"
        print("✅ 中文语音识别语言设置成功")
        
        return True, speechsdk
    except ImportError as e:
        print(f"❌ Azure Speech SDK未安装: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Azure配置错误: {e}")
        return False, None

def recognize_with_azure(audio_path):
    """使用Azure Speech SDK进行语音识别"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        # 配置
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_CONFIG["key"],
            region=AZURE_CONFIG["region"]
        )
        speech_config.speech_recognition_language = "zh-CN"
        
        # 转换音频格式
        wav_path, is_temp = convert_audio_to_wav(audio_path)
        
        try:
            # 创建音频配置
            audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
            
            # 创建识别器
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            print("🔄 开始语音识别...")
            
            # 识别结果
            result = speech_recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                print(f"✅ 识别成功: {result.text}")
                return result.text
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("❌ 无法识别语音内容")
                return None
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = speechsdk.CancellationDetails.from_result(result)
                print(f"❌ 识别取消: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    print(f"错误详情: {cancellation.error_details}")
                return None
            else:
                print(f"❌ 未知结果: {result.reason}")
                return None
                
        finally:
            if is_temp and os.path.exists(wav_path):
                os.remove(wav_path)
                
    except Exception as e:
        print(f"❌ Azure语音识别失败: {e}")
        return None

def recognize_with_azure_streaming(audio_path):
    """使用Azure流式语音识别（更高效）"""
    try:
        import azure.cognitiveservices.speech as speechsdk
        
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_CONFIG["key"],
            region=AZURE_CONFIG["region"]
        )
        speech_config.speech_recognition_language = "zh-CN"
        
        wav_path, is_temp = convert_audio_to_wav(audio_path)
        
        try:
            audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
            recognizer = speechsdk.SpeechRecognizer(speech_config, audio_config)
            
            # 使用流式识别
            done = False
            recognized_text = ""
            
            def stop_cb(evt):
                nonlocal done
                print(f"识别结束: {evt}")
                done = True
            
            def recognized_cb(evt):
                nonlocal recognized_text
                if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    recognized_text += evt.result.text + " "
                    print(f"部分结果: {evt.result.text}")
            
            recognizer.recognized.connect(recognized_cb)
            recognizer.session_stopped.connect(stop_cb)
            
            print("🔄 开始流式语音识别...")
            recognizer.start_continuous_recognition()
            
            # 等待识别完成（最长10秒）
            start_time = time.time()
            while not done and (time.time() - start_time) < 10:
                time.sleep(0.1)
            
            recognizer.stop_continuous_recognition()
            
            if recognized_text:
                print(f"✅ 流式识别结果: {recognized_text.strip()}")
                return recognized_text.strip()
            else:
                print("❌ 流式识别无结果")
                return None
                
        finally:
            if is_temp and os.path.exists(wav_path):
                os.remove(wav_path)
                
    except Exception as e:
        print(f"❌ 流式识别失败: {e}")
        return None

def main():
    """主测试函数"""
    print("=" * 60)
    print("Azure Speech-to-Text 语音识别测试")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <音频文件路径>")
        print("示例: python azure_speech_recognition.py test.ogg")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    if not os.path.exists(audio_file):
        print(f"❌ 文件不存在: {audio_file}")
        sys.exit(1)
    
    print(f"📁 测试文件: {audio_file}")
    print(f"🔑 使用密钥: {AZURE_CONFIG['key'][:12]}...")
    print(f"🌐 区域: {AZURE_CONFIG['region']}")
    
    # 步骤1: 测试SDK可用性
    print("\n步骤1: 检查Azure Speech SDK...")
    sdk_available, speechsdk = test_azure_speech_offline()
    
    if not sdk_available:
        print("⚠️ SDK未安装，尝试安装: pip install azure-cognitiveservices-speech")
        print("继续测试其他方法...")
        sys.exit(1)
    
    # 步骤2: 使用单次识别
    print("\n步骤2: 尝试单次语音识别...")
    result = recognize_with_azure(audio_file)
    
    if result:
        print(f"\n🎉 成功！识别结果: {result}")
        return result
    else:
        print("\n⚠️ 单次识别失败，尝试流式识别...")
        
        # 步骤3: 尝试流式识别
        result = recognize_with_azure_streaming(audio_file)
        
        if result:
            print(f"\n🎉 流式识别成功！结果: {result}")
            return result
        else:
            print("\n❌ 所有Azure识别方法都失败")
            return None

if __name__ == "__main__":
    main()