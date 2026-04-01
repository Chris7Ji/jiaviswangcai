#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
音频速度控制工具
可以调整MP3文件的播放速度
"""

import os
import sys
import subprocess
import argparse

def check_ffmpeg():
    """检查ffmpeg是否可用"""
    try:
        result = subprocess.run(['which', 'ffmpeg'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return None
    except Exception as e:
        print(f"❌ 检查ffmpeg时出错: {e}")
        return None

def adjust_audio_speed(input_file, speed_factor=1.0, output_file=None):
    """
    调整音频文件播放速度
    
    参数:
        input_file: 输入音频文件路径
        speed_factor: 速度倍数 (0.5=半速, 1.0=原速, 1.5=1.5倍速, 2.0=2倍速)
        output_file: 输出文件路径 (如为None则自动生成)
    
    返回:
        (成功标志, 输出文件路径)
    """
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 输入文件不存在: {input_file}")
        return False, None
    
    # 检查ffmpeg
    ffmpeg_path = check_ffmpeg()
    if not ffmpeg_path:
        print("❌ ffmpeg未安装，请先安装: brew install ffmpeg")
        return False, None
    
    # 验证速度参数
    if speed_factor <= 0:
        print("❌ 速度倍数必须大于0")
        return False, None
    
    # ffmpeg的atempo过滤器有限制：0.5 <= atempo <= 2.0
    # 如果需要超出范围，需要串联多个atempo过滤器
    if speed_factor < 0.5 or speed_factor > 2.0:
        print("⚠️  速度倍数超出atempo限制范围(0.5-2.0)，将使用串联过滤器")
    
    # 生成输出文件名
    if output_file is None:
        base_name = os.path.splitext(input_file)[0]
        ext = os.path.splitext(input_file)[1]
        output_file = f"{base_name}_speed_{speed_factor}x{ext}"
    
    print(f"🎵 音频速度调整")
    print(f"📁 输入文件: {input_file}")
    print(f"⚡ 目标速度: {speed_factor}倍")
    print(f"💾 输出文件: {output_file}")
    
    # 构建ffmpeg命令
    # 处理速度倍数限制
    if 0.5 <= speed_factor <= 2.0:
        # 在有效范围内，使用单个atempo
        filter_str = f"atempo={speed_factor}"
    else:
        # 超出范围，使用串联过滤器
        # 例如：2.5倍速 = atempo=2.0,atempo=1.25
        factors = []
        remaining = speed_factor
        
        while remaining > 2.0:
            factors.append(2.0)
            remaining /= 2.0
        
        while remaining < 0.5:
            factors.append(0.5)
            remaining /= 0.5
        
        factors.append(remaining)
        filter_str = ",".join([f"atempo={f}" for f in factors])
    
    # 构建完整命令
    cmd = [
        ffmpeg_path,
        '-i', input_file,
        '-filter:a', filter_str,
        '-vn',  # 不要视频
        '-y',   # 覆盖输出文件
        output_file
    ]
    
    print(f"🔧 执行命令: {' '.join(cmd)}")
    
    try:
        # 执行ffmpeg命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 音频速度调整成功!")
            
            # 获取文件信息
            if os.path.exists(output_file):
                input_size = os.path.getsize(input_file)
                output_size = os.path.getsize(output_file)
                print(f"📊 文件大小: {output_size} 字节 ({output_size/1024:.1f} KB)")
                print(f"📈 大小变化: {output_size/input_size*100:.1f}%")
            
            return True, output_file
        else:
            print(f"❌ ffmpeg执行失败:")
            print(f"   错误: {result.stderr}")
            return False, None
            
    except Exception as e:
        print(f"❌ 处理音频时出错: {e}")
        return False, None

def play_audio(file_path, background=True):
    """播放音频文件"""
    if not os.path.exists(file_path):
        print(f"❌ 音频文件不存在: {file_path}")
        return False
    
    try:
        if background:
            # 后台播放
            subprocess.Popen(['afplay', file_path])
            print(f"🎵 正在后台播放: {file_path}")
        else:
            # 前台播放
            subprocess.run(['afplay', file_path])
            print(f"🎵 播放完成: {file_path}")
        
        return True
    except Exception as e:
        print(f"❌ 播放音频时出错: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='音频速度控制工具')
    parser.add_argument('input', help='输入音频文件路径')
    parser.add_argument('-s', '--speed', type=float, default=1.3, 
                       help='速度倍数 (默认: 1.3)')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-p', '--play', action='store_true', 
                       help='处理后立即播放')
    parser.add_argument('-b', '--background', action='store_true', 
                       help='后台播放')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("🎵 音频速度控制工具")
    print("=" * 50)
    
    # 调整音频速度
    success, output_file = adjust_audio_speed(
        args.input, 
        args.speed, 
        args.output
    )
    
    if success and args.play:
        print("\n" + "=" * 50)
        print("🔊 播放音频")
        print("=" * 50)
        play_audio(output_file, args.background)

if __name__ == "__main__":
    main()