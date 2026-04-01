#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily API密钥提取脚本
专门用于从图片中提取Tavily API密钥
"""

import os
import sys
import re
import subprocess
import tempfile
from pathlib import Path

def check_tesseract_installed():
    """检查Tesseract是否已安装"""
    try:
        result = subprocess.run(
            ["which", "tesseract"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False

def install_tesseract():
    """安装Tesseract OCR"""
    print("🔧 安装Tesseract OCR...")
    
    # 检查Homebrew是否安装
    brew_check = subprocess.run(["which", "brew"], capture_output=True, text=True)
    if brew_check.returncode != 0:
        print("❌ Homebrew未安装，无法自动安装Tesseract")
        print("💡 请手动安装:")
        print("   1. 先安装Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        print("   2. 再运行: brew install tesseract tesseract-lang")
        return False
    
    try:
        # 安装Tesseract
        print("📦 安装Tesseract和语言包...")
        install_cmd = ["brew", "install", "tesseract", "tesseract-lang"]
        result = subprocess.run(install_cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Tesseract安装成功!")
            return True
        else:
            print(f"❌ Tesseract安装失败: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ 安装超时，请手动安装: brew install tesseract tesseract-lang")
        return False
    except Exception as e:
        print(f"❌ 安装异常: {e}")
        return False

def extract_text_from_image(image_path, languages=["chi_sim", "eng"]):
    """从图片中提取文字"""
    if not os.path.exists(image_path):
        return {"success": False, "error": f"图片文件不存在: {image_path}", "text": ""}
    
    # 创建临时输出文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        output_base = tmp_file.name
    
    try:
        # 构建Tesseract命令
        lang_param = "+".join(languages)
        cmd = ["tesseract", image_path, output_base.replace('.txt', ''), "-l", lang_param]
        
        # 执行OCR
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # 读取输出文件
        output_file = output_base.replace('.txt', '.txt')
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                extracted_text = f.read().strip()
            
            return {
                "success": True,
                "text": extracted_text,
                "error": result.stderr if result.stderr else "",
                "return_code": result.returncode
            }
        else:
            return {
                "success": False,
                "text": "",
                "error": f"OCR处理失败，未生成输出文件。错误: {result.stderr}",
                "return_code": result.returncode
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "OCR处理超时（30秒）", "text": ""}
    except Exception as e:
        return {"success": False, "error": f"OCR处理异常: {str(e)}", "text": ""}
    finally:
        # 清理临时文件
        for ext in ['.txt']:
            file_path = output_base.replace('.txt', ext)
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except:
                    pass

def extract_tavily_api_key(text):
    """从文本中提取Tavily API密钥"""
    # Tavily API密钥模式: tvly-后面跟着32个十六进制字符
    patterns = [
        r'tvly-[a-fA-F0-9]{32}',  # 标准格式: tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        r'Tavily[:\s]*([a-fA-F0-9-]{36,})',  # Tavily: 密钥
        r'API[_\s]*Key[:\s]*([a-fA-F0-9-]{36,})',  # API Key: 密钥
        r'([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})',  # UUID格式
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            # 清理匹配结果
            for match in matches:
                key = match.strip()
                # 确保是Tavily格式
                if key.startswith('tvly-'):
                    return key
                elif len(key) >= 36:  # 可能是完整的密钥
                    return key
    
    # 如果没有找到标准格式，尝试查找类似密钥的字符串
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        # 查找包含"key"、"api"、"token"的行
        if any(keyword in line.lower() for keyword in ['key', 'api', 'token', 'secret']):
            # 提取看起来像密钥的部分
            parts = re.split(r'[:=\s]+', line)
            for part in parts:
                part = part.strip()
                if len(part) >= 20 and any(c.isalpha() for c in part) and any(c.isdigit() for c in part):
                    return part
    
    return None

def process_image_file(image_path):
    """处理图片文件，提取Tavily API密钥"""
    print(f"🔍 处理图片: {image_path}")
    print(f"📏 文件大小: {os.path.getsize(image_path)} 字节")
    
    # 检查Tesseract
    if not check_tesseract_installed():
        print("❌ Tesseract OCR未安装")
        choice = input("是否自动安装Tesseract? (y/n): ").strip().lower()
        if choice == 'y':
            if install_tesseract():
                print("✅ 安装完成，继续处理...")
            else:
                print("❌ 安装失败，请手动安装")
                return None
        else:
            print("💡 请手动安装: brew install tesseract tesseract-lang")
            return None
    
    # 提取文字
    print("📝 正在提取图片文字...")
    result = extract_text_from_image(image_path, languages=["eng", "chi_sim"])
    
    if not result["success"]:
        print(f"❌ OCR提取失败: {result['error']}")
        return None
    
    extracted_text = result["text"]
    print(f"✅ 文字提取成功，共 {len(extracted_text)} 字符")
    
    # 显示提取的文字（前500字符）
    if extracted_text:
        preview = extracted_text[:500] + ("..." if len(extracted_text) > 500 else "")
        print("\n📄 提取的文字预览:")
        print("-" * 50)
        print(preview)
        print("-" * 50)
    
    # 提取Tavily API密钥
    print("\n🔑 正在查找Tavily API密钥...")
    api_key = extract_tavily_api_key(extracted_text)
    
    if api_key:
        print(f"✅ 找到Tavily API密钥: {api_key}")
        
        # 验证密钥格式
        if api_key.startswith('tvly-') and len(api_key) == 37:  # tvly- + 32字符
            print("✅ 密钥格式正确")
        else:
            print("⚠️  密钥格式可能不标准，请验证")
        
        return api_key
    else:
        print("❌ 未找到Tavily API密钥")
        print("💡 建议:")
        print("   1. 检查图片是否清晰")
        print("   2. 手动查看提取的文字")
        print("   3. 手动输入密钥")
        
        # 显示所有可能的关键字
        lines = extracted_text.split('\n')
        possible_keys = []
        for line in lines:
            if any(keyword in line.lower() for keyword in ['key', 'api', 'token', 'secret', 'tvly']):
                possible_keys.append(line.strip())
        
        if possible_keys:
            print("\n🔍 可能包含密钥的行:")
            for key_line in possible_keys[:5]:  # 显示前5行
                print(f"   - {key_line}")
        
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("🔑 Tavily API密钥提取工具")
    print("=" * 60)
    
    if len(sys.argv) < 2:
        print("用法: python extract_tavily_key.py <图片路径>")
        print("示例: python extract_tavily_key.py tavily_key.jpg")
        print("")
        print("或者直接拖拽图片到终端:")
        print("  python extract_tavily_key.py /path/to/your/image.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ 错误：图片文件不存在: {image_path}")
        sys.exit(1)
    
    # 处理图片
    api_key = process_image_file(image_path)
    
    if api_key:
        print("\n" + "=" * 60)
        print("🎉 Tavily API密钥提取成功!")
        print("=" * 60)
        print(f"\n🔑 您的Tavily API密钥: {api_key}")
        print("\n💡 下一步:")
        print("   1. 保存此密钥")
        print("   2. 运行配置脚本: ./configure_tavily_search.sh " + api_key)
        print("   3. 开始使用Tavily搜索")
        
        # 询问是否立即配置
        choice = input("\n是否立即配置Tavily搜索? (y/n): ").strip().lower()
        if choice == 'y':
            config_script = os.path.join(os.path.dirname(__file__), "configure_tavily_search.sh")
            if os.path.exists(config_script):
                os.system(f"chmod +x {config_script}")
                os.system(f"{config_script} {api_key}")
            else:
                print(f"❌ 配置脚本未找到: {config_script}")
    else:
        print("\n" + "=" * 60)
        print("❌ 未能提取Tavily API密钥")
        print("=" * 60)
        print("\n💡 替代方案:")
        print("   1. 使用Mac预览程序手动提取:")
        print("      - 双击打开图片")
        print("      - 菜单栏: 工具 → 文字识别")
        print("      - 复制识别出的文字")
        print("   2. 在线OCR工具: https://ocr.space/")
        print("   3. 手动输入密钥")

if __name__ == "__main__":
    main()