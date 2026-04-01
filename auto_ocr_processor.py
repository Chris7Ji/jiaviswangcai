#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动OCR处理器
非交互式，自动安装Tesseract并处理图片
"""

import os
import sys
import subprocess
import tempfile
import re

def run_command(cmd, timeout=300):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=isinstance(cmd, str)
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"命令超时: {cmd}", "stdout": "", "stderr": "", "returncode": -1}
    except Exception as e:
        return {"success": False, "error": str(e), "stdout": "", "stderr": "", "returncode": -1}

def install_tesseract():
    """安装Tesseract OCR"""
    print("🔧 安装Tesseract OCR...")
    
    # 检查是否已安装
    check = run_command("which tesseract")
    if check["success"]:
        print("✅ Tesseract已安装")
        return True
    
    # 检查Homebrew
    brew_check = run_command("which brew")
    if not brew_check["success"]:
        print("❌ Homebrew未安装，无法自动安装Tesseract")
        return False
    
    # 安装Tesseract
    print("📦 安装Tesseract和语言包...")
    install_result = run_command("brew install tesseract tesseract-lang", timeout=600)
    
    if install_result["success"]:
        print("✅ Tesseract安装成功!")
        return True
    else:
        print(f"❌ Tesseract安装失败: {install_result.get('stderr', '未知错误')}")
        return False

def extract_text(image_path):
    """从图片中提取文字"""
    if not os.path.exists(image_path):
        return {"success": False, "error": f"图片文件不存在: {image_path}", "text": ""}
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
        output_base = tmp_file.name
    
    try:
        # 执行OCR
        cmd = f"tesseract '{image_path}' '{output_base.replace('.txt', '')}' -l eng+chi_sim"
        result = run_command(cmd, timeout=60)
        
        # 读取结果
        output_file = output_base.replace('.txt', '.txt')
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            return {
                "success": True,
                "text": text,
                "error": result.get("stderr", ""),
                "returncode": result.get("returncode", -1)
            }
        else:
            return {
                "success": False,
                "text": "",
                "error": f"OCR失败，未生成输出文件: {result.get('stderr', '未知错误')}",
                "returncode": result.get("returncode", -1)
            }
    except Exception as e:
        return {"success": False, "text": "", "error": str(e)}
    finally:
        # 清理临时文件
        for ext in ['.txt']:
            file_path = output_base.replace('.txt', ext)
            if os.path.exists(file_path):
                try:
                    os.unlink(file_path)
                except:
                    pass

def analyze_text(text):
    """分析提取的文字"""
    if not text:
        return {"type": "unknown", "content": "", "key_info": []}
    
    # 检查是否是Tavily API密钥
    tavily_patterns = [
        r'tvly-[a-fA-F0-9]{32}',
        r'API[_\s]*Key[:\s]*([a-fA-F0-9-]{36,})',
        r'Tavily[:\s]*([a-fA-F0-9-]{36,})'
    ]
    
    for pattern in tavily_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return {
                "type": "tavily_key",
                "content": matches[0] if isinstance(matches[0], str) else matches[0][0],
                "key_info": ["Tavily API密钥"],
                "full_text": text
            }
    
    # 检查是否是Brave API密钥
    brave_patterns = [
        r'brv_[a-zA-Z0-9]{32}',
        r'Brave[_\s]*Key[:\s]*([a-zA-Z0-9]{32,})',
        r'API[_\s]*Key[:\s]*(brv_[a-zA-Z0-9]{32})'
    ]
    
    for pattern in brave_patterns:
        matches = re.findall(pattern, text)
        if matches:
            return {
                "type": "brave_key",
                "content": matches[0] if isinstance(matches[0], str) else matches[0][0],
                "key_info": ["Brave API密钥"],
                "full_text": text
            }
    
    # 检查其他API密钥
    api_key_patterns = [
        r'[a-zA-Z0-9]{32,}',
        r'sk-[a-zA-Z0-9]{48,}',
        r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
    ]
    
    for pattern in api_key_patterns:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches:
                if len(match) >= 32:  # 可能是API密钥
                    return {
                        "type": "api_key",
                        "content": match,
                        "key_info": ["可能的API密钥"],
                        "full_text": text
                    }
    
    # 分析文本内容
    lines = text.split('\n')
    key_lines = []
    
    for line in lines:
        line = line.strip()
        if len(line) > 10:  # 忽略太短的行
            # 检查是否包含关键词
            keywords = ['key', 'api', 'token', 'secret', 'password', 'auth', 'access']
            if any(keyword in line.lower() for keyword in keywords):
                key_lines.append(line)
    
    return {
        "type": "general_text",
        "content": text[:500] + ("..." if len(text) > 500 else ""),
        "key_info": key_lines[:10],  # 最多10行关键信息
        "full_text": text
    }

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python auto_ocr_processor.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ 错误：图片文件不存在: {image_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔍 自动OCR处理器")
    print("=" * 60)
    print(f"📷 处理图片: {os.path.basename(image_path)}")
    print(f"📏 文件大小: {os.path.getsize(image_path)} 字节")
    print("")
    
    # 1. 安装Tesseract（如果需要）
    if not install_tesseract():
        print("❌ OCR工具安装失败，无法继续")
        sys.exit(1)
    
    # 2. 提取文字
    print("📝 正在提取图片文字...")
    result = extract_text(image_path)
    
    if not result["success"]:
        print(f"❌ OCR提取失败: {result['error']}")
        sys.exit(1)
    
    text = result["text"]
    print(f"✅ 文字提取成功，共 {len(text)} 字符")
    
    # 3. 分析文字
    print("🔍 分析提取的文字...")
    analysis = analyze_text(text)
    
    # 4. 输出结果
    print("")
    print("=" * 60)
    print("📊 OCR处理结果")
    print("=" * 60)
    
    if analysis["type"] == "tavily_key":
        print("🎯 检测到: Tavily API密钥")
        print(f"🔑 密钥: {analysis['content']}")
        print("")
        print("💡 建议: 运行配置脚本自动配置Tavily搜索")
        print(f"     ./configure_tavily_search.sh {analysis['content']}")
        
    elif analysis["type"] == "brave_key":
        print("🎯 检测到: Brave API密钥")
        print(f"🔑 密钥: {analysis['content']}")
        print("")
        print("💡 建议: 运行配置脚本自动配置Brave搜索")
        print(f"     ./configure_brave_search.sh {analysis['content']}")
        
    elif analysis["type"] == "api_key":
        print("🎯 检测到: 可能的API密钥")
        print(f"🔑 内容: {analysis['content']}")
        print("")
        print("⚠️  注意: 请确认这是否是有效的API密钥")
        
    else:
        print("📄 提取的文字内容:")
        print("-" * 50)
        print(analysis["content"])
        print("-" * 50)
        
        if analysis["key_info"]:
            print("")
            print("🔍 关键信息行:")
            for i, line in enumerate(analysis["key_info"], 1):
                print(f"  {i}. {line}")
    
    # 5. 保存完整结果
    output_file = f"ocr_result_{os.path.basename(image_path).split('.')[0]}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"图片: {image_path}\n")
        f.write(f"提取时间: {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}\n")
        f.write(f"字符数: {len(text)}\n")
        f.write("\n" + "="*50 + "\n")
        f.write("完整文字内容:\n")
        f.write("="*50 + "\n")
        f.write(text)
        f.write("\n" + "="*50 + "\n")
    
    print("")
    print(f"💾 完整结果已保存到: {output_file}")
    print("✅ OCR处理完成!")

if __name__ == "__main__":
    main()