#!/usr/bin/env python3
"""
测试SpeechRecognition库的语音识别功能
"""

import speech_recognition as sr
import subprocess
import tempfile
import os
import sys

def convert_ogg_to_wav(ogg_path, wav_path=None):
    """转换OGG到WAV格式（16kHz单声道）"""
    if wav_path is None:
        temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
        os.close(temp_fd)
        wav_path = temp_path
        is_temp = True
    else:
        is_temp = False
    
    cmd = [
        'ffmpeg', '-i', ogg_path,
        '-ar', '16000',
        '-ac', '1',
        '-acodec', 'pcm_s16le',
        '-y',
        wav_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"转换完成: {ogg_path} -> {wav_path}")
        return wav_path, is_temp
    except subprocess.CalledProcessError as e:
        print(f"转换失败: {e}")
        if is_temp:
            os.remove(wav_path)
        raise

def recognize_with_google(audio_path):
    """使用Google Web Speech API识别（需要网络）"""
    r = sr.Recognizer()
    
    # 先转换为WAV
    wav_path, is_temp = convert_ogg_to_wav(audio_path)
    
    try:
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
            
            # 尝试Google识别
            try:
                text = r.recognize_google(audio, language='zh-CN')
                print(f"Google识别结果: {text}")
                return text, "google"
            except sr.UnknownValueError:
                print("Google无法识别音频")
                return None, "google"
            except sr.RequestError as e:
                print(f"Google API请求失败: {e}")
                return None, "google"
                
    finally:
        if is_temp and os.path.exists(wav_path):
            os.remove(wav_path)

def recognize_with_sphinx(audio_path):
    """使用CMU Sphinx离线识别（需要语言模型）"""
    r = sr.Recognizer()
    
    wav_path, is_temp = convert_ogg_to_wav(audio_path)
    
    try:
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
            
            try:
                # 尝试中文识别，但需要中文语言模型
                text = r.recognize_sphinx(audio, language='zh-CN')
                print(f"Sphinx识别结果: {text}")
                return text, "sphinx"
            except sr.UnknownValueError:
                print("Sphinx无法识别音频")
                return None, "sphinx"
            except LookupError:
                print("Sphinx中文语言模型未安装")
                return None, "sphinx"
                
    finally:
        if is_temp and os.path.exists(wav_path):
            os.remove(wav_path)

def recognize_with_all(audio_path):
    """尝试所有可用的识别方法"""
    results = []
    
    # 尝试Google
    text, engine = recognize_with_google(audio_path)
    if text:
        results.append((engine, text))
    
    # 尝试Sphinx
    text, engine = recognize_with_sphinx(audio_path)
    if text:
        results.append((engine, text))
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <音频文件路径>")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"错误: 文件不存在: {audio_file}")
        sys.exit(1)
    
    print(f"测试语音识别: {audio_file}")
    results = recognize_with_all(audio_file)
    
    if results:
        print("\n识别结果:")
        for engine, text in results:
            print(f"  {engine}: {text}")
    else:
        print("所有识别方法都失败了")