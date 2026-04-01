#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监控新语音文件并立即处理
用于实时测试
"""

import os
import sys
import time
import hashlib
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from voice_processing_pipeline import VoiceProcessingPipeline
    PIPELINE_AVAILABLE = True
except ImportError as e:
    print(f"❌ 无法导入语音处理管道: {e}")
    PIPELINE_AVAILABLE = False

def get_file_hash(filepath):
    """计算文件哈希值"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return hashlib.md5(filepath.encode()).hexdigest()

def monitor_and_process():
    """监控并处理新语音文件"""
    audio_dir = "/Users/jiyingguo/.openclaw/media/inbound"
    processed_file = "/tmp/processed_hashes.json"
    
    # 加载已处理文件记录
    processed = set()
    if os.path.exists(processed_file):
        try:
            with open(processed_file, 'r') as f:
                processed = set(json.load(f))
        except:
            pass
    
    # 初始化管道
    if PIPELINE_AVAILABLE:
        pipeline = VoiceProcessingPipeline(use_azure=True)
        print("✅ 语音处理管道初始化成功")
    else:
        print("❌ 语音处理管道不可用")
        return
    
    print(f"🔍 开始监控目录: {audio_dir}")
    print("📱 等待用户发送语音消息...")
    print("💡 提示：用户现在可以发送语音消息进行测试")
    
    # 初始文件列表
    initial_files = set()
    for f in os.listdir(audio_dir):
        if f.lower().endswith(('.ogg', '.mp3', '.wav', '.m4a')):
            initial_files.add(f)
    
    try:
        while True:
            # 检查新文件
            current_files = set()
            for f in os.listdir(audio_dir):
                if f.lower().endswith(('.ogg', '.mp3', '.wav', '.m4a')):
                    current_files.add(f)
            
            new_files = current_files - initial_files
            
            for filename in new_files:
                filepath = os.path.join(audio_dir, filename)
                file_hash = get_file_hash(filepath)
                
                if file_hash in processed:
                    print(f"⏭️  文件已处理过: {filename}")
                    continue
                
                print(f"🎯 发现新语音文件: {filename}")
                print(f"  路径: {filepath}")
                print(f"  大小: {os.path.getsize(filepath)} 字节")
                
                # 处理文件
                try:
                    print("🔄 开始处理...")
                    result = pipeline.process_voice_message(filepath)
                    
                    if result.get("success", False):
                        print("✅ 处理成功！")
                        print(f"   识别结果: {result.get('recognized_text', '')}")
                        print(f"   AI回复: {result.get('ai_response', '')}")
                        print(f"   语音文件: {result.get('tts_output', '')}")
                        
                        # 标记为已处理
                        processed.add(file_hash)
                        with open(processed_file, 'w') as f:
                            json.dump(list(processed), f)
                        
                        print("📤 可以发送回复给用户")
                    else:
                        print("❌ 处理失败")
                        
                except Exception as e:
                    print(f"❌ 处理异常: {e}")
            
            # 更新初始文件列表
            initial_files = current_files
            
            # 等待5秒
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n👋 监控停止")
    except Exception as e:
        print(f"❌ 监控异常: {e}")

if __name__ == "__main__":
    monitor_and_process()