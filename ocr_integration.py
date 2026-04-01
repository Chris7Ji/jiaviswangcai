#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OCR集成脚本
使用Tesseract OCR提取图片中的文字
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict, List
import json

class OCRProcessor:
    """OCR处理器"""
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        初始化OCR处理器
        
        Args:
            tesseract_path: Tesseract可执行文件路径，如果为None则自动查找
        """
        self.tesseract_path = tesseract_path or self._find_tesseract()
        if not self.tesseract_path:
            raise FileNotFoundError("未找到Tesseract OCR。请先安装: brew install tesseract tesseract-lang")
        
        self.supported_languages = self._get_supported_languages()
    
    def _find_tesseract(self) -> Optional[str]:
        """查找Tesseract可执行文件"""
        # 尝试常见路径
        possible_paths = [
            "/usr/local/bin/tesseract",
            "/opt/homebrew/bin/tesseract",
            "/usr/bin/tesseract",
            shutil.which("tesseract")
        ]
        
        for path in possible_paths:
            if path and os.path.exists(path):
                try:
                    # 验证tesseract是否可用
                    result = subprocess.run(
                        [path, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return path
                except:
                    continue
        
        return None
    
    def _get_supported_languages(self) -> List[str]:
        """获取支持的语言列表"""
        try:
            result = subprocess.run(
                [self.tesseract_path, "--list-langs"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # 解析输出，跳过第一行"List of available languages (3):"
                lines = result.stdout.strip().split('\n')
                if len(lines) > 1:
                    return [lang.strip() for lang in lines[1:] if lang.strip()]
            
            # 默认支持的语言
            return ["eng", "chi_sim", "chi_tra"]
        except:
            return ["eng", "chi_sim", "chi_tra"]
    
    def extract_text(
        self,
        image_path: str,
        languages: List[str] = None,
        config: str = "",
        timeout: int = 30
    ) -> Dict[str, any]:
        """
        从图片中提取文字
        
        Args:
            image_path: 图片文件路径
            languages: 语言列表，如 ["chi_sim", "eng"]
            config: Tesseract配置参数
            timeout: 超时时间（秒）
        
        Returns:
            包含提取文字和元数据的字典
        """
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"图片文件不存在: {image_path}",
                "text": "",
                "metadata": {}
            }
        
        # 设置默认语言
        if languages is None:
            languages = ["chi_sim", "eng"]  # 中文简体 + 英文
        
        # 过滤不支持的语言
        valid_languages = [lang for lang in languages if lang in self.supported_languages]
        if not valid_languages:
            valid_languages = ["eng"]  # 默认英文
        
        lang_param = "+".join(valid_languages)
        
        # 创建临时输出文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp_file:
            output_base = tmp_file.name
        
        try:
            # 构建命令
            cmd = [self.tesseract_path, image_path, output_base.replace('.txt', '')]
            
            # 添加语言参数
            if lang_param:
                cmd.extend(["-l", lang_param])
            
            # 添加配置参数
            if config:
                cmd.extend(["--oem", "3"])  # 默认使用LSTM引擎
                cmd.extend(["--psm", "3"])  # 自动页面分割
                # 可以添加更多配置
            
            # 执行OCR
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            # 读取输出文件
            output_file = output_base.replace('.txt', '.txt')
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    extracted_text = f.read().strip()
                
                # 获取图片信息
                image_info = self._get_image_info(image_path)
                
                return {
                    "success": True,
                    "text": extracted_text,
                    "language": lang_param,
                    "metadata": {
                        "image_path": image_path,
                        "image_info": image_info,
                        "tesseract_version": self._get_tesseract_version(),
                        "command": " ".join(cmd),
                        "return_code": result.returncode,
                        "stderr": result.stderr.strip() if result.stderr else "",
                        "supported_languages": self.supported_languages
                    }
                }
            else:
                return {
                    "success": False,
                    "error": f"OCR处理失败，未生成输出文件。错误: {result.stderr}",
                    "text": "",
                    "metadata": {
                        "return_code": result.returncode,
                        "stderr": result.stderr.strip() if result.stderr else "",
                        "stdout": result.stdout.strip() if result.stdout else ""
                    }
                }
                
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"OCR处理超时（{timeout}秒）",
                "text": "",
                "metadata": {}
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"OCR处理异常: {str(e)}",
                "text": "",
                "metadata": {}
            }
        finally:
            # 清理临时文件
            for ext in ['.txt']:
                file_path = output_base.replace('.txt', ext)
                if os.path.exists(file_path):
                    try:
                        os.unlink(file_path)
                    except:
                        pass
    
    def _get_image_info(self, image_path: str) -> Dict[str, any]:
        """获取图片信息"""
        try:
            # 使用file命令获取图片信息
            result = subprocess.run(
                ["file", image_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            info = {
                "path": image_path,
                "size_bytes": os.path.getsize(image_path),
                "file_command": result.stdout.strip() if result.returncode == 0 else ""
            }
            
            # 尝试获取图片尺寸（需要PIL或类似库）
            try:
                from PIL import Image
                with Image.open(image_path) as img:
                    info["dimensions"] = {
                        "width": img.width,
                        "height": img.height,
                        "format": img.format,
                        "mode": img.mode
                    }
            except ImportError:
                # PIL未安装，跳过尺寸信息
                pass
            except Exception:
                # 其他错误，跳过尺寸信息
                pass
            
            return info
        except Exception:
            return {"path": image_path, "size_bytes": os.path.getsize(image_path)}
    
    def _get_tesseract_version(self) -> str:
        """获取Tesseract版本"""
        try:
            result = subprocess.run(
                [self.tesseract_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # 提取版本号
                lines = result.stdout.strip().split('\n')
                if lines:
                    return lines[0]
            return "未知版本"
        except:
            return "未知版本"
    
    def batch_process(
        self,
        image_paths: List[str],
        languages: List[str] = None,
        output_dir: Optional[str] = None
    ) -> Dict[str, any]:
        """
        批量处理多张图片
        
        Args:
            image_paths: 图片路径列表
            languages: 语言列表
            output_dir: 输出目录，如果提供则保存结果到文件
        
        Returns:
            批量处理结果
        """
        results = []
        successful = 0
        failed = 0
        
        for i, image_path in enumerate(image_paths, 1):
            print(f"处理图片 {i}/{len(image_paths)}: {os.path.basename(image_path)}")
            
            result = self.extract_text(image_path, languages)
            results.append({
                "image": os.path.basename(image_path),
                "path": image_path,
                **result
            })
            
            if result["success"]:
                successful += 1
            else:
                failed += 1
        
        # 如果需要保存到文件
        if output_dir and os.path.isdir(output_dir):
            timestamp = subprocess.run(
                ["date", "+%Y%m%d_%H%M%S"],
                capture_output=True,
                text=True
            ).stdout.strip()
            
            output_file = os.path.join(output_dir, f"ocr_results_{timestamp}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": timestamp,
                    "total_images": len(image_paths),
                    "successful": successful,
                    "failed": failed,
                    "results": results
                }, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 结果已保存到: {output_file}")
        
        return {
            "total": len(image_paths),
            "successful": successful,
            "failed": failed,
            "results": results
        }

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python ocr_integration.py <图片路径> [语言]")
        print("示例: python ocr_integration.py image.jpg chi_sim+eng")
        print("示例: python ocr_integration.py image.jpg")
        print("")
        print("批量处理: python ocr_integration.py --batch 图片1.jpg 图片2.jpg ...")
        print("")
        print("支持的语言:")
        print("  chi_sim - 中文简体")
        print("  chi_tra - 中文繁体")
        print("  eng     - 英文")
        print("  jpn     - 日文")
        print("  kor     - 韩文")
        sys.exit(1)
    
    try:
        processor = OCRProcessor()
        print(f"✅ Tesseract找到: {processor.tesseract_path}")
        print(f"📚 支持的语言: {', '.join(processor.supported_languages)}")
        print("")
        
        # 检查是否是批量模式
        if sys.argv[1] == "--batch":
            image_paths = sys.argv[2:]
            if not image_paths:
                print("❌ 错误：请提供图片路径")
                sys.exit(1)
            
            # 验证图片文件
            valid_paths = []
            for path in image_paths:
                if os.path.exists(path):
                    valid_paths.append(path)
                else:
                    print(f"⚠️  警告：图片不存在，跳过: {path}")
            
            if not valid_paths:
                print("❌ 错误：没有有效的图片文件")
                sys.exit(1)
            
            print(f"🔍 批量处理 {len(valid_paths)} 张图片...")
            result = processor.batch_process(valid_paths)
            
            print("")
            print("📊 批量处理结果:")
            print(f"   总图片数: {result['total']}")
            print(f"   成功: {result['successful']}")
            print(f"   失败: {result['failed']}")
            
            # 显示成功的结果
            for item in result['results']:
                if item['success']:
                    print(f"\n📄 {item['image']}:")
                    print(f"   文字: {item['text'][:200]}..." if len(item['text']) > 200 else f"   文字: {item['text']}")
                else:
                    print(f"\n❌ {item['image']}: {item['error']}")
            
        else:
            # 单张图片处理
            image_path = sys.argv[1]
            languages = sys.argv[2].split('+') if len(sys.argv) > 2 else None
            
            print(f"🔍 处理图片: {image_path}")
            if languages:
                print(f"🌐 使用语言: {'+'.join(languages)}")
            
            result = processor.extract_text(image_path, languages)
            
            print("")
            if result['success']:
                print("✅ OCR处理成功!")
                print("")
                print("📄 提取的文字:")
                print("-" * 50)
                print(result['text'])
                print("-" * 50)
                
                if result['metadata']:
                    print("")
                    print("📊 元数据:")
                    print(f"   图片: {result['metadata'].get('image_path', 'N/A')}")
                    if 'image_info' in result['metadata']:
                        info = result['metadata']['image_info']
                        if 'dimensions' in info:
                            dim = info['dimensions']
                            print(f"   尺寸: {dim.get('width', 'N/A')}x{dim.get('height', 'N/A')}")
                    print(f"   语言: {result.get('language', 'N/A')}")
                    print(f"   Tesseract版本: {result['metadata'].get('tesseract_version', 'N/A')}")
            else:
                print("❌ OCR处理失败!")
                print(f"   错误: {result['error']}")
                if result['metadata'] and 'stderr' in result['metadata']:
                    print(f"   详细错误: {result['metadata']['stderr']}")
                
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("")
        print("💡 安装Tesseract OCR:")
        print("  macOS: brew install tesseract tesseract-lang")
        print("  Ubuntu/Debian: sudo apt install tesseract-ocr tesseract-ocr-chi-sim")
        print("  CentOS/RHEL: sudo yum install tesseract tesseract-langpack-chi_sim")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 处理异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()