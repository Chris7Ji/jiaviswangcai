#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音消息处理器
接收音频文件，调用语音处理管道，发送回复
"""

import os
import sys
import json
import time
import hashlib
import logging
from datetime import datetime
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/feishu_voice_handler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from voice_processing_pipeline import VoiceProcessingPipeline
    PIPELINE_AVAILABLE = True
except ImportError as e:
    logger.error(f"无法导入语音处理管道: {e}")
    PIPELINE_AVAILABLE = False

class FeishuVoiceHandler:
    """飞书语音消息处理器"""
    
    def __init__(self, config_path=None):
        self.config = self.load_config(config_path)
        self.pipeline = None
        self.processed_files = set()
        self.load_processed_history()
        
        if PIPELINE_AVAILABLE:
            self.pipeline = VoiceProcessingPipeline(use_azure=True)
            logger.info("语音处理管道初始化成功")
        else:
            logger.warning("语音处理管道不可用，仅记录模式")
    
    def load_config(self, config_path):
        """加载配置文件"""
        default_config = {
            "audio_input_dir": "/Users/jiyingguo/.openclaw/media/inbound",
            "processed_db": "/tmp/feishu_voice_processed.json",
            "check_interval": 30,  # 检查间隔(秒)
            "max_file_age": 300,   # 最大文件年龄(秒)
            "user_id": "ou_b6c7778820b20031cd97bdc45d1cd9fa",
            "enable_voice_reply": True,
            "enable_text_reply": True,
            "azure_enabled": True,
            "fallback_to_text": True
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"从 {config_path} 加载配置")
            except Exception as e:
                logger.error(f"加载配置文件失败: {e}")
        
        logger.info(f"使用配置: {json.dumps(default_config, indent=2, ensure_ascii=False)}")
        return default_config
    
    def load_processed_history(self):
        """加载已处理文件历史"""
        db_path = self.config.get("processed_db")
        if os.path.exists(db_path):
            try:
                with open(db_path, 'r', encoding='utf-8') as f:
                    self.processed_files = set(json.load(f))
                logger.info(f"加载已处理文件记录: {len(self.processed_files)} 个文件")
            except Exception as e:
                logger.error(f"加载处理记录失败: {e}")
                self.processed_files = set()
    
    def save_processed_history(self):
        """保存已处理文件历史"""
        db_path = self.config.get("processed_db")
        try:
            with open(db_path, 'w', encoding='utf-8') as f:
                json.dump(list(self.processed_files), f)
        except Exception as e:
            logger.error(f"保存处理记录失败: {e}")
    
    def get_new_audio_files(self):
        """获取新的音频文件"""
        input_dir = self.config.get("audio_input_dir")
        if not os.path.exists(input_dir):
            logger.error(f"输入目录不存在: {input_dir}")
            return []
        
        new_files = []
        max_age = self.config.get("max_file_age")
        now = time.time()
        
        for filename in os.listdir(input_dir):
            # 检查音频文件扩展名
            if not filename.lower().endswith(('.ogg', '.mp3', '.wav', '.m4a')):
                continue
            
            filepath = os.path.join(input_dir, filename)
            
            # 检查文件年龄
            file_age = now - os.path.getmtime(filepath)
            if file_age > max_age:
                logger.debug(f"文件太旧跳过: {filename} ({file_age:.1f}秒)")
                continue
            
            # 检查是否已处理
            file_hash = self.get_file_hash(filepath)
            if file_hash in self.processed_files:
                logger.debug(f"文件已处理跳过: {filename}")
                continue
            
            new_files.append({
                "path": filepath,
                "filename": filename,
                "hash": file_hash,
                "age": file_age
            })
        
        logger.info(f"发现 {len(new_files)} 个新音频文件")
        return new_files
    
    def get_file_hash(self, filepath):
        """计算文件哈希值"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"计算文件哈希失败 {filepath}: {e}")
            return hashlib.md5(filepath.encode()).hexdigest()
    
    def process_audio_file(self, audio_info):
        """处理单个音频文件"""
        filepath = audio_info["path"]
        filename = audio_info["filename"]
        file_hash = audio_info["hash"]
        
        logger.info(f"开始处理音频文件: {filename}")
        
        try:
            if not self.pipeline:
                logger.error("语音处理管道不可用，跳过处理")
                return False
            
            # 调用语音处理管道
            result = self.pipeline.process_voice_message(filepath)
            
            if not result.get("success", False):
                logger.error(f"语音处理失败: {filename}")
                return False
            
            # 提取结果
            recognized_text = result.get("recognized_text", "")
            ai_response = result.get("ai_response", "")
            tts_file = result.get("tts_output", "")
            
            logger.info(f"处理成功: {filename}")
            logger.info(f"识别结果: {recognized_text}")
            logger.info(f"AI回复: {ai_response}")
            
            # 标记为已处理
            self.processed_files.add(file_hash)
            self.save_processed_history()
            
            # 清理临时文件
            if result.get("is_temp_file") and os.path.exists(tts_file):
                os.remove(tts_file)
                logger.debug(f"清理临时文件: {tts_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"处理音频文件失败 {filename}: {e}", exc_info=True)
            return False
    
    def run_once(self):
        """单次运行检查和处理"""
        logger.info("开始检查新音频文件...")
        
        new_files = self.get_new_audio_files()
        if not new_files:
            logger.info("没有发现新音频文件")
            return 0
        
        processed_count = 0
        for audio_info in new_files:
            success = self.process_audio_file(audio_info)
            if success:
                processed_count += 1
        
        logger.info(f"处理完成: {processed_count}/{len(new_files)} 个文件")
        return processed_count
    
    def run_continuous(self):
        """持续运行模式"""
        logger.info("启动持续运行模式")
        check_interval = self.config.get("check_interval", 30)
        
        try:
            while True:
                self.run_once()
                logger.info(f"等待 {check_interval} 秒后再次检查...")
                time.sleep(check_interval)
        except KeyboardInterrupt:
            logger.info("收到中断信号，停止运行")
        except Exception as e:
            logger.error(f"运行异常: {e}", exc_info=True)

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书语音消息处理器")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--once", action="store_true", help="单次运行模式")
    parser.add_argument("--continuous", action="store_true", help="持续运行模式")
    
    args = parser.parse_args()
    
    # 创建处理器
    handler = FeishuVoiceHandler(args.config)
    
    if args.continuous:
        handler.run_continuous()
    else:
        # 默认单次运行
        handler.run_once()

if __name__ == "__main__":
    main()