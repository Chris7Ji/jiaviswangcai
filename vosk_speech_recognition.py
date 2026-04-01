#!/usr/bin/env python3
"""
Vosk离线语音识别模块
支持中文，完全离线，无需网络连接
"""

import os
import sys
import subprocess
import json
import wave
import tempfile
from vosk import Model, KaldiRecognizer

class VoskSpeechRecognizer:
    def __init__(self, model_path=None):
        """
        初始化Vosk语音识别器
        
        Args:
            model_path: Vosk模型路径，如果为None则使用默认路径
        """
        if model_path is None:
            # 默认模型路径
            model_path = os.path.expanduser("~/.openclaw/models/vosk/vosk-model-small-cn-0.22")
        
        self.model_path = model_path
        
        # 检查模型是否存在
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk模型未找到: {self.model_path}")
        
        print(f"加载Vosk模型: {self.model_path}", file=sys.stderr)
        self.model = Model(self.model_path)
        
    def convert_audio(self, input_path, output_path=None):
        """
        转换音频文件为Vosk所需的格式：16kHz, 单声道, PCM
        
        Args:
            input_path: 输入音频文件路径（支持OGG, MP3等）
            output_path: 输出WAV文件路径，如果为None则创建临时文件
            
        Returns:
            转换后的WAV文件路径
        """
        if output_path is None:
            # 创建临时文件
            temp_fd, temp_path = tempfile.mkstemp(suffix='.wav')
            os.close(temp_fd)
            output_path = temp_path
            is_temp = True
        else:
            is_temp = False
        
        # 使用ffmpeg转换
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
            print(f"音频转换完成: {input_path} -> {output_path}", file=sys.stderr)
            return output_path, is_temp
        except subprocess.CalledProcessError as e:
            print(f"音频转换失败: {e}", file=sys.stderr)
            if is_temp and os.path.exists(output_path):
                os.remove(output_path)
            raise
    
    def transcribe(self, audio_path):
        """
        转录音频文件为文本
        
        Args:
            audio_path: 音频文件路径（支持多种格式，自动转换）
            
        Returns:
            识别的文本字符串
        """
        # 先转换为WAV格式
        wav_path, is_temp = self.convert_audio(audio_path)
        
        try:
            # 打开WAV文件
            wf = wave.open(wav_path, "rb")
            
            # 检查音频格式
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000]:
                print(f"警告: 音频格式可能不兼容: channels={wf.getnchannels()}, "
                      f"sample_width={wf.getsampwidth()}, rate={wf.getframerate()}", file=sys.stderr)
            
            # 创建识别器
            rec = KaldiRecognizer(self.model, wf.getframerate())
            rec.SetWords(True)  # 获取单词时间戳
            
            results = []
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    if 'text' in result and result['text']:
                        results.append(result['text'])
            
            # 获取最终结果
            final_result = json.loads(rec.FinalResult())
            if 'text' in final_result and final_result['text']:
                results.append(final_result['text'])
            
            wf.close()
            
            # 合并所有结果
            full_text = " ".join(results).strip()
            print(f"语音识别结果: '{full_text}'", file=sys.stderr)
            return full_text
            
        finally:
            # 清理临时文件
            if is_temp and os.path.exists(wav_path):
                os.remove(wav_path)
    
    def transcribe_ogg(self, ogg_path):
        """专门处理OGG格式的语音消息（飞书默认格式）"""
        return self.transcribe(ogg_path)

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print(f"用法: {sys.argv[0]} <音频文件路径> [模型路径]", file=sys.stderr)
        print(f"示例: {sys.argv[0]} test.ogg", file=sys.stderr)
        sys.exit(1)
    
    audio_file = sys.argv[1]
    model_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(audio_file):
        print(f"错误: 音频文件不存在: {audio_file}", file=sys.stderr)
        sys.exit(1)
    
    try:
        recognizer = VoskSpeechRecognizer(model_path)
        text = recognizer.transcribe(audio_file)
        print(text)
    except Exception as e:
        print(f"语音识别失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()