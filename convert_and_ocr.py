#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换图片格式并尝试OCR
"""

import os
import sys
import tempfile
from PIL import Image

def convert_webp_to_png(webp_path):
    """将WebP转换为PNG"""
    try:
        # 打开WebP图片
        with Image.open(webp_path) as img:
            # 创建临时PNG文件
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                png_path = tmp_file.name
            
            # 转换为PNG并保存
            img.save(png_path, 'PNG')
            
            print(f"✅ WebP转换为PNG: {png_path}")
            print(f"   原始尺寸: {img.size}, 模式: {img.mode}")
            
            return png_path
            
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return None

def try_simple_ocr(image_path):
    """尝试简单的OCR方法"""
    try:
        # 尝试使用在线OCR，但指定文件类型
        import requests
        import base64
        
        # 读取图片并转换为base64
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 尝试不同的在线OCR服务
        
        # 方法1: OCR.space（指定文件类型）
        print("🔄 尝试OCR.space API...")
        api_url = "https://api.ocr.space/parse/image"
        
        # 获取文件扩展名
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        if ext == 'webp':
            ext = 'png'  # WebP可能不被支持，使用png
        
        response = requests.post(
            api_url,
            files={"image": (f"image.{ext}", image_data, f"image/{ext}")},
            data={
                "apikey": "helloworld",  # 免费API密钥
                "language": "eng",
                "isOverlayRequired": False,
                "filetype": ext.upper() if ext in ['PNG', 'JPG', 'JPEG', 'PDF'] else 'PNG'
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            if not result.get("IsErroredOnProcessing"):
                text = ""
                for item in result.get("ParsedResults", []):
                    text += item.get("ParsedText", "") + "\n"
                
                if text.strip():
                    return {"success": True, "text": text.strip(), "method": "ocr.space"}
        
        # 方法2: 简单的图像处理尝试提取文字（如果图片主要是文字）
        print("🔄 尝试图像处理分析...")
        from PIL import Image
        import pytesseract
        
        # 尝试设置tesseract路径
        try:
            # 尝试导入pytesseract
            img = Image.open(image_path)
            
            # 尝试简单的图像处理增强对比度
            from PIL import ImageEnhance
            
            # 转换为灰度
            if img.mode != 'L':
                img = img.convert('L')
            
            # 增强对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            
            # 二值化
            threshold = 128
            img = img.point(lambda p: p > threshold and 255)
            
            # 保存处理后的图片用于调试
            debug_path = image_path.replace('.png', '_processed.png')
            img.save(debug_path)
            print(f"💾 处理后的图片保存到: {debug_path}")
            
            # 尝试OCR
            try:
                text = pytesseract.image_to_string(img, lang='eng')
                if text.strip():
                    return {"success": True, "text": text.strip(), "method": "pytesseract_processed"}
            except:
                pass
                
        except ImportError:
            print("⚠️  pytesseract未安装")
        except Exception as e:
            print(f"⚠️  图像处理失败: {e}")
        
        return {"success": False, "error": "所有OCR方法都失败"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python convert_and_ocr.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ 错误：图片文件不存在: {image_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔄 图片转换与OCR尝试")
    print("=" * 60)
    
    # 检查文件格式
    file_ext = os.path.splitext(image_path)[1].lower()
    print(f"📷 原始文件: {image_path}")
    print(f"📁 格式: {file_ext}")
    print(f"📏 大小: {os.path.getsize(image_path)} 字节")
    
    # 如果是WebP，转换为PNG
    if file_ext == '.webp':
        print("🔄 检测到WebP格式，转换为PNG...")
        png_path = convert_webp_to_png(image_path)
        if png_path:
            image_path = png_path
            print(f"✅ 使用转换后的PNG文件: {png_path}")
        else:
            print("❌ 转换失败，使用原始文件")
    else:
        print("✅ 文件格式无需转换")
    
    print("")
    print("🔍 尝试OCR提取文字...")
    
    # 尝试OCR
    result = try_simple_ocr(image_path)
    
    print("")
    print("=" * 60)
    print("📊 处理结果")
    print("=" * 60)
    
    if result.get("success"):
        text = result.get("text", "")
        method = result.get("method", "未知")
        
        print(f"✅ OCR成功! (方法: {method})")
        print(f"📄 提取的文字 ({len(text)} 字符):")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
        # 保存结果
        output_file = f"ocr_extracted_text.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"图片: {sys.argv[1]}\n")
            f.write(f"方法: {method}\n")
            f.write(f"字符数: {len(text)}\n")
            f.write("\n" + "="*50 + "\n")
            f.write("提取的文字:\n")
            f.write("="*50 + "\n")
            f.write(text)
            f.write("\n" + "="*50 + "\n")
        
        print(f"💾 结果已保存到: {output_file}")
        
        # 分析文字内容
        print("")
        print("🔍 文字内容分析:")
        
        # 检查是否是API密钥
        import re
        
        # Tavily API密钥模式
        tavily_pattern = r'tvly-[a-fA-F0-9]{32}'
        tavily_matches = re.findall(tavily_pattern, text)
        if tavily_matches:
            print(f"🔑 找到Tavily API密钥: {tavily_matches[0]}")
        
        # Brave API密钥模式
        brave_pattern = r'brv_[a-zA-Z0-9]{32}'
        brave_matches = re.findall(brave_pattern, text)
        if brave_matches:
            print(f"🔑 找到Brave API密钥: {brave_matches[0]}")
        
        # 通用API密钥模式
        api_patterns = [
            r'[a-zA-Z0-9]{32,}',
            r'sk-[a-zA-Z0-9]{48,}',
            r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match) >= 32:
                    print(f"🔑 找到可能的API密钥: {match}")
                    break
        
        # 显示前几行
        lines = text.split('\n')
        if lines:
            print("")
            print("📝 文字行预览:")
            for i, line in enumerate(lines[:10]):
                if line.strip():
                    print(f"  {i+1}. {line.strip()}")
        
    else:
        print("❌ OCR提取失败")
        print(f"   错误: {result.get('error', '未知错误')}")
        print("")
        print("💡 建议:")
        print("  1. 使用Mac预览程序:")
        print("     - 双击打开图片")
        print("     - 工具 → 文字识别 → 识别文本")
        print("     - 复制文字")
        print("  2. 使用在线OCR: https://ocr.space/")
        print("  3. 手动查看图片并输入关键信息")
    
    print("")
    print("✅ 处理完成")

if __name__ == "__main__":
    main()