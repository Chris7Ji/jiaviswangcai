#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终OCR尝试：使用在线API
"""

import os
import sys
import base64
import requests
import json
from PIL import Image
import tempfile

def convert_webp_to_jpg(webp_path):
    """将WebP转换为JPG（更兼容）"""
    try:
        with Image.open(webp_path) as img:
            # 转换为RGB模式（JPG需要）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 创建临时JPG文件
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                jpg_path = tmp_file.name
            
            # 保存为JPG
            img.save(jpg_path, 'JPEG', quality=90)
            
            print(f"✅ WebP转换为JPG: {jpg_path}")
            return jpg_path
            
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return None

def try_ocrspace_api(image_path):
    """尝试OCR.space API"""
    try:
        # 读取图片
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        # 获取文件扩展名
        ext = os.path.splitext(image_path)[1].lower().replace('.', '')
        if ext == 'webp':
            # 转换为JPG
            jpg_path = convert_webp_to_jpg(image_path)
            if jpg_path:
                with open(jpg_path, 'rb') as f:
                    image_data = f.read()
                ext = 'jpg'
                # 清理临时文件
                os.unlink(jpg_path)
        
        # 将图片转换为base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        print(f"🔄 调用OCR.space API...")
        print(f"   图片格式: {ext}")
        print(f"   图片大小: {len(image_data)} 字节")
        print(f"   base64长度: {len(image_base64)} 字符")
        
        # OCR.space API端点
        api_url = "https://api.ocr.space/parse/image"
        
        # 准备请求数据
        payload = {
            "apikey": "helloworld",  # 免费API密钥
            "language": "eng",  # 英文
            "isOverlayRequired": False,
            "base64Image": f"data:image/{ext};base64,{image_base64}",
            "filetype": ext.upper() if ext.upper() in ['PNG', 'JPG', 'JPEG', 'PDF'] else 'JPG'
        }
        
        # 发送请求
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(api_url, data=payload, headers=headers, timeout=30)
        
        print(f"   响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   API响应: {json.dumps(result, ensure_ascii=False)[:200]}...")
            
            if result.get("IsErroredOnProcessing"):
                error_msg = result.get("ErrorMessage", "未知错误")
                print(f"❌ API错误: {error_msg}")
                return {"success": False, "error": error_msg}
            
            # 提取文字
            text = ""
            for item in result.get("ParsedResults", []):
                text += item.get("ParsedText", "") + "\n"
            
            text = text.strip()
            if text:
                print(f"✅ 提取到文字: {len(text)} 字符")
                return {"success": True, "text": text, "method": "ocr.space"}
            else:
                print("❌ 未提取到文字")
                return {"success": False, "error": "未提取到文字"}
        else:
            error_msg = f"HTTP错误: {response.status_code}"
            print(f"❌ {error_msg}")
            return {"success": False, "error": error_msg}
            
    except Exception as e:
        print(f"❌ 异常: {e}")
        return {"success": False, "error": str(e)}

def try_google_vision_simulate(image_path):
    """模拟Google Vision API（实际上使用简单图像处理）"""
    try:
        print("🔄 尝试简单图像分析...")
        
        from PIL import Image, ImageEnhance, ImageFilter
        import pytesseract
        
        # 打开图片
        img = Image.open(image_path)
        print(f"   原始尺寸: {img.size}, 模式: {img.mode}")
        
        # 如果是WebP，先转换
        if image_path.endswith('.webp'):
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                png_path = tmp_file.name
            img.save(png_path, 'PNG')
            img = Image.open(png_path)
            os.unlink(png_path)
        
        # 图像预处理
        # 1. 转换为灰度
        if img.mode != 'L':
            img = img.convert('L')
        
        # 2. 增强对比度
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)
        
        # 3. 锐化
        img = img.filter(ImageFilter.SHARPEN)
        
        # 4. 二值化
        threshold = 150
        img = img.point(lambda p: p > threshold and 255)
        
        # 保存处理后的图片
        with tempfile.NamedTemporaryFile(suffix='_processed.png', delete=False) as tmp_file:
            processed_path = tmp_file.name
        img.save(processed_path)
        print(f"💾 处理后的图片: {processed_path}")
        
        # 尝试使用pytesseract（如果可用）
        try:
            # 设置tesseract路径
            tesseract_paths = [
                '/opt/homebrew/bin/tesseract',
                '/usr/local/bin/tesseract',
                '/usr/bin/tesseract'
            ]
            
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
            
            # 提取文字
            text = pytesseract.image_to_string(img, lang='eng')
            text = text.strip()
            
            if text:
                print(f"✅ pytesseract提取到文字: {len(text)} 字符")
                return {"success": True, "text": text, "method": "pytesseract_processed"}
            else:
                print("❌ pytesseract未提取到文字")
                
        except Exception as e:
            print(f"⚠️  pytesseract失败: {e}")
        
        # 如果pytesseract失败，尝试简单的文字检测
        # 这里只是演示，实际上需要更复杂的算法
        print("⚠️  所有OCR方法都失败，图片可能不包含可识别文字")
        return {"success": False, "error": "图片可能不包含可识别文字"}
        
    except ImportError:
        return {"success": False, "error": "缺少依赖库"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python final_ocr_attempt.py <图片路径>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"❌ 错误：图片文件不存在: {image_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("🔄 最终OCR尝试")
    print("=" * 60)
    print(f"📷 图片: {os.path.basename(image_path)}")
    print(f"📏 大小: {os.path.getsize(image_path)} 字节")
    print("")
    
    # 方法1: 在线OCR API
    print("1. 尝试在线OCR API...")
    result = try_ocrspace_api(image_path)
    
    if result.get("success"):
        text = result.get("text", "")
        print("")
        print("=" * 60)
        print("✅ OCR成功!")
        print("=" * 60)
        print(f"方法: {result.get('method', '未知')}")
        print(f"字符数: {len(text)}")
        print("")
        print("📄 提取的文字:")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
        # 保存结果
        output_file = "ocr_final_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"图片: {image_path}\n")
            f.write(f"方法: {result.get('method', '未知')}\n")
            f.write(f"字符数: {len(text)}\n")
            f.write("\n" + "="*50 + "\n")
            f.write("提取的文字:\n")
            f.write("="*50 + "\n")
            f.write(text)
            f.write("\n" + "="*50 + "\n")
        
        print(f"💾 结果已保存到: {output_file}")
        
        # 分析内容
        print("")
        print("🔍 内容分析:")
        import re
        
        # 检查API密钥
        patterns = {
            "Tavily API密钥": r'tvly-[a-fA-F0-9]{32}',
            "Brave API密钥": r'brv_[a-zA-Z0-9]{32}',
            "通用API密钥": r'[a-zA-Z0-9]{32,}',
            "UUID格式": r'[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}'
        }
        
        found_keys = []
        for key_type, pattern in patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                for match in matches:
                    if len(match) >= 32:  # 确保是足够长的字符串
                        found_keys.append((key_type, match))
        
        if found_keys:
            print("🔑 找到的密钥:")
            for key_type, key in found_keys:
                print(f"  • {key_type}: {key}")
        else:
            print("📝 文字内容（前10行）:")
            lines = text.split('\n')
            for i, line in enumerate(lines[:10]):
                if line.strip():
                    print(f"  {i+1}. {line.strip()}")
        
        return
    
    print("")
    print("❌ 在线OCR API失败，尝试方法2...")
    
    # 方法2: 本地图像处理
    print("2. 尝试本地图像处理...")
    result2 = try_google_vision_simulate(image_path)
    
    if result2.get("success"):
        text = result2.get("text", "")
        print("")
        print("=" * 60)
        print("✅ OCR成功!")
        print("=" * 60)
        print(f"方法: {result2.get('method', '未知')}")
        print(f"字符数: {len(text)}")
        print("")
        print("📄 提取的文字:")
        print("-" * 50)
        print(text[:500] + ("..." if len(text) > 500 else ""))
        print("-" * 50)
        
        output_file = "ocr_final_result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"图片: {image_path}\n")
            f.write(f"方法: {result2.get('method', '未知')}\n")
            f.write(f"字符数: {len(text)}\n")
            f.write("\n" + "="*50 + "\n")
            f.write("提取的文字:\n")
            f.write("="*50 + "\n")
            f.write(text)
            f.write("\n" + "="*50 + "\n")
        
        print(f"💾 结果已保存到: {output_file}")
        return
    
    print("")
    print("=" * 60)
    print("❌ 所有OCR方法都失败了!")
    print("=" * 60)
    print("")
    print("💡 最终建议:")
    print("")
    print("1. 📱 **使用Mac预览程序（最可靠）**:")
    print("   双击图片 → 工具 → 文字识别 → 识别文本 → 复制")
    print("")
    print("2. 🌐 **使用在线OCR网站**:")
    print("   访问 https://ocr.space/ → 上传图片 → 复制结果")
    print("")
    print("3. ✍️ **直接告诉我图片内容**:")
    print("   查看图片 → 输入关键信息 → 我帮您处理")
    print("")
    print("4. 🔧 **手动安装OCR工具**:")
    print("   brew install tesseract tesseract-lang")
    print("   然后我可以使用本地OCR")
    print("")
    print("**推荐方案1**，1分钟内即可完成!")

if __name__ == "__main__":
    main()