#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多方法OCR尝试脚本
尝试多种方法提取图片文字
"""

import os
import sys
import subprocess
import tempfile
import requests
import json
from pathlib import Path

def method1_mac_preview(image_path):
    """方法1: 使用macOS预览程序（通过AppleScript）"""
    try:
        # 创建AppleScript调用预览程序OCR
        applescript = f'''
        tell application "Preview"
            activate
            open POSIX file "{image_path}"
            delay 2
            tell application "System Events"
                tell process "Preview"
                    click menu item "文字识别" of menu "工具" of menu bar 1
                    delay 2
                    click menu item "识别文本" of menu "文字识别" of menu "工具" of menu bar 1
                    delay 3
                end tell
            end tell
            close document 1
        end tell
        '''
        
        # 保存AppleScript到临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
            f.write(applescript)
            script_path = f.name
        
        # 执行AppleScript
        result = subprocess.run(['osascript', script_path], capture_output=True, text=True, timeout=30)
        
        # 清理
        os.unlink(script_path)
        
        if result.returncode == 0:
            # 实际上，AppleScript不会直接返回文字，需要其他方法获取
            # 这里只是演示框架
            return {"success": False, "error": "AppleScript执行成功但无法获取文字", "method": "mac_preview"}
        else:
            return {"success": False, "error": f"AppleScript失败: {result.stderr}", "method": "mac_preview"}
            
    except Exception as e:
        return {"success": False, "error": str(e), "method": "mac_preview"}

def method2_tesseract_cli(image_path):
    """方法2: 使用Tesseract命令行"""
    try:
        # 创建临时输出文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            output_base = tmp_file.name
        
        # 尝试不同路径的tesseract
        tesseract_paths = [
            '/opt/homebrew/bin/tesseract',
            '/usr/local/bin/tesseract', 
            '/usr/bin/tesseract',
            'tesseract'
        ]
        
        for tesseract_cmd in tesseract_paths:
            try:
                # 检查命令是否存在
                check = subprocess.run(['which', tesseract_cmd], capture_output=True, text=True)
                if check.returncode != 0 and not os.path.exists(tesseract_cmd):
                    continue
                
                # 执行OCR
                cmd = [tesseract_cmd, image_path, output_base.replace('.txt', ''), '-l', 'eng+chi_sim']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                
                # 读取结果
                output_file = output_base.replace('.txt', '.txt')
                if os.path.exists(output_file):
                    with open(output_file, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    
                    # 清理
                    if os.path.exists(output_file):
                        os.unlink(output_file)
                    
                    return {
                        "success": True,
                        "text": text,
                        "method": "tesseract_cli",
                        "command": tesseract_cmd
                    }
                    
            except Exception as e:
                continue
        
        return {"success": False, "error": "所有Tesseract路径都失败", "method": "tesseract_cli"}
        
    except Exception as e:
        return {"success": False, "error": str(e), "method": "tesseract_cli"}

def method3_pytesseract(image_path):
    """方法3: 使用pytesseract库"""
    try:
        import pytesseract
        from PIL import Image
        
        # 打开图片
        img = Image.open(image_path)
        
        # 设置tesseract路径（尝试多个）
        possible_paths = [
            '/opt/homebrew/bin/tesseract',
            '/usr/local/bin/tesseract',
            '/usr/bin/tesseract'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                break
        
        # 提取文字
        text = pytesseract.image_to_string(img, lang='eng+chi_sim')
        
        return {
            "success": True,
            "text": text.strip(),
            "method": "pytesseract"
        }
        
    except ImportError:
        return {"success": False, "error": "pytesseract或PIL未安装", "method": "pytesseract"}
    except Exception as e:
        return {"success": False, "error": str(e), "method": "pytesseract"}

def method4_easyocr(image_path):
    """方法4: 使用easyocr库"""
    try:
        import easyocr
        
        # 创建reader（中英文）
        reader = easyocr.Reader(['ch_sim', 'en'])
        
        # 读取图片
        result = reader.readtext(image_path)
        
        # 合并所有文本
        text = ' '.join([item[1] for item in result])
        
        return {
            "success": True,
            "text": text.strip(),
            "method": "easyocr",
            "details": result
        }
        
    except ImportError:
        return {"success": False, "error": "easyocr未安装", "method": "easyocr"}
    except Exception as e:
        return {"success": False, "error": str(e), "method": "easyocr"}

def method5_online_ocr(image_path):
    """方法5: 使用在线OCR服务（需要网络）"""
    try:
        # 使用免费的OCR.space API
        api_url = "https://api.ocr.space/parse/image"
        
        # 读取图片文件
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 发送请求
        response = requests.post(
            api_url,
            files={"image": image_data},
            data={
                "apikey": "helloworld",  # 免费API密钥
                "language": "eng+chi_sim",
                "isOverlayRequired": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("IsErroredOnProcessing"):
                return {"success": False, "error": result.get("ErrorMessage", "未知错误"), "method": "online_ocr"}
            
            # 提取文字
            text = ""
            for item in result.get("ParsedResults", []):
                text += item.get("ParsedText", "") + "\n"
            
            return {
                "success": True,
                "text": text.strip(),
                "method": "online_ocr",
                "api_response": result
            }
        else:
            return {"success": False, "error": f"API请求失败: {response.status_code}", "method": "online_ocr"}
            
    except Exception as e:
        return {"success": False, "error": str(e), "method": "online_ocr"}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python multi_ocr_attempt.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ 错误：图片文件不存在: {image_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 多方法OCR尝试")
    print("=" * 60)
    print(f"📷 图片: {os.path.basename(image_path)}")
    print(f"📏 大小: {os.path.getsize(image_path)} 字节")
    print("")
    
    # 尝试所有方法
    methods = [
        ("Tesseract命令行", method2_tesseract_cli),
        ("pytesseract库", method3_pytesseract),
        ("easyocr库", method4_easyocr),
        ("在线OCR服务", method5_online_ocr),
        # ("macOS预览程序", method1_mac_preview),  # 暂时注释，需要用户交互
    ]
    
    results = []
    successful = False
    
    for method_name, method_func in methods:
        print(f"🔄 尝试方法: {method_name}...")
        result = method_func(image_path)
        results.append((method_name, result))
        
        if result.get("success"):
            print(f"✅ {method_name} 成功!")
            successful = True
            break
        else:
            print(f"❌ {method_name} 失败: {result.get('error', '未知错误')}")
    
    print("")
    print("=" * 60)
    print("📊 OCR处理结果")
    print("=" * 60)
    
    if successful:
        # 找到第一个成功的方法
        for method_name, result in results:
            if result.get("success"):
                text = result.get("text", "")
                print(f"🎯 成功方法: {method_name}")
                print(f"📄 提取的文字 ({len(text)} 字符):")
                print("-" * 50)
                print(text)
                print("-" * 50)
                
                # 保存结果
                output_file = f"ocr_result_{os.path.basename(image_path).split('.')[0]}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"图片: {image_path}\n")
                    f.write(f"方法: {method_name}\n")
                    f.write(f"字符数: {len(text)}\n")
                    f.write("\n" + "="*50 + "\n")
                    f.write("提取的文字:\n")
                    f.write("="*50 + "\n")
                    f.write(text)
                    f.write("\n" + "="*50 + "\n")
                
                print(f"💾 结果已保存到: {output_file}")
                break
    else:
        print("❌ 所有OCR方法都失败了!")
        print("")
        print("💡 建议:")
        print("  1. 使用Mac预览程序手动提取:")
        print("     - 双击打开图片")
        print("     - 工具 → 文字识别 → 识别文本")
        print("     - 复制文字")
        print("  2. 使用在线OCR: https://ocr.space/")
        print("  3. 手动输入关键信息")
        
        # 显示所有错误
        print("")
        print("🔍 详细错误信息:")
        for method_name, result in results:
            print(f"  • {method_name}: {result.get('error', '未知错误')}")
    
    print("")
    print("✅ OCR尝试完成")

if __name__ == "__main__":
    main()