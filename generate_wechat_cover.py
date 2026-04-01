#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成微信公众号封面图配置
"""

import os
import json
from datetime import datetime

def generate_cover_config():
    """生成封面图配置"""
    print("🎨 生成微信公众号封面图配置")
    print("=" * 50)
    
    # 封面图配置
    cover_config = {
        "title": "我的AI助手旺财：三天时间构建的四大能力体系",
        "description": "AI助手能力进化封面图 - 展示AI机器人、四大能力图标、科技蓝主题",
        "prompt": """Generate a professional WeChat public account cover image for the article titled "我的AI助手旺财：三天时间构建的四大能力体系" (My AI Assistant Wangcai: Building Four Major Capabilities in Three Days).

Article theme: AI assistant capability evolution, technology growth, content creation
Style requirements: Technology sense, clean, professional, visually impactful
Elements required: Include AI, robot, evolution, four major capabilities elements
Color requirements: Technology blue, white, gray as main colors
Size requirements: 900x383 pixels (WeChat public account cover image standard size)
Resolution: 2K

Visual elements:
1. A futuristic AI robot/assistant in the center
2. Four glowing icons around it representing: Content Creation, Blog Writing, AI Image Generation, Text Humanization
3. Clean blue and white color scheme with gradient background
4. Subtle circuit board or data flow patterns
5. Professional Chinese typography for the title
6. Modern, sleek design suitable for technology content""",
        "size": "900x383",
        "aspect_ratio": "2.35:1",
        "colors": ["#007AFF", "#FFFFFF", "#1A1A1A", "#F0F8FF"],
        "elements": [
            "AI机器人/助手",
            "四个能力图标",
            "科技背景图案",
            "中文标题文字",
            "渐变色彩",
            "光效元素"
        ],
        "api_key": "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s",
        "api_provider": "Google Gemini",
        "generated_at": datetime.now().isoformat(),
        "status": "config_ready",
        "note": "Use this prompt with image generation services like DALL-E 3, Midjourney, or Stable Diffusion"
    }
    
    # 保存配置
    config_file = "/Users/jiyingguo/.openclaw/workspace/wechat_cover_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(cover_config, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 封面图配置已生成: {config_file}")
    print(f"   标题: {cover_config['title']}")
    print(f"   尺寸: {cover_config['size']}")
    print(f"   颜色: {', '.join(cover_config['colors'])}")
    print(f"   API密钥: 已配置")
    
    # 创建快速生成脚本
    create_quick_generate_script()
    
    return cover_config

def create_quick_generate_script():
    """创建快速生成脚本"""
    script_content = """#!/bin/bash
# 微信公众号封面图快速生成脚本

echo "🎨 微信公众号封面图生成选项"
echo "================================"
echo ""
echo "选择生成方式:"
echo "1. 使用DALL-E 3生成 (需要OpenAI API Key)"
echo "2. 使用Stable Diffusion生成 (本地运行)"
echo "3. 使用Midjourney生成 (需要Discord账号)"
echo "4. 手动设计 (使用设计工具)"
echo ""
echo "📋 封面图要求:"
echo "   尺寸: 900x383像素"
echo "   主题: AI助手能力进化"
echo "   颜色: 科技蓝、白色、灰色"
echo "   元素: AI机器人 + 四大能力图标"
echo ""
echo "💡 提示:"
echo "   已保存配置到 wechat_cover_config.json"
echo "   包含详细的生成提示词(prompt)"
echo ""
echo "🚀 快速开始:"
echo "   查看配置: cat wechat_cover_config.json | jq '.prompt'"
echo "   复制提示词到您的图像生成工具"
"""

    script_file = "/Users/jiyingguo/.openclaw/workspace/generate_cover.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 添加执行权限
    import stat
    os.chmod(script_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    print(f"✅ 快速生成脚本已创建: {script_file}")
    
    # 创建占位符图片说明
    placeholder_note = """# 封面图占位符说明

由于图像生成API限制，当前使用占位符方案：

## 📋 当前方案
1. **配置已准备** - 详细的生成提示词和参数
2. **API密钥已配置** - Gemini API密钥可用
3. **手动生成建议** - 使用其他图像生成服务

## 🎨 推荐生成工具
1. **DALL-E 3** (OpenAI) - 质量最高，支持中文提示
2. **Midjourney** - 艺术风格优秀
3. **Stable Diffusion** - 本地运行，可定制性强
4. **Canva/稿定设计** - 在线设计工具

## 🚀 快速生成步骤
1. 复制 `wechat_cover_config.json` 中的 prompt
2. 粘贴到您选择的图像生成工具
3. 设置尺寸为 900x383 像素
4. 生成并下载图片
5. 在公众号后台上传为封面

## 📁 生成的文件
- `wechat_cover_config.json` - 封面图配置
- `generate_cover.sh` - 快速生成脚本
- 本文档 - 生成说明

**建议立即使用DALL-E 3生成封面图，然后继续发布流程。**
"""
    
    note_file = "/Users/jiyingguo/.openclaw/workspace/COVER_IMAGE_GUIDE.md"
    with open(note_file, 'w', encoding='utf-8') as f:
        f.write(placeholder_note)
    
    print(f"✅ 生成指南已创建: {note_file}")

def main():
    """主函数"""
    print("🚀 微信公众号封面图生成工具")
    print("=" * 60)
    
    # 生成配置
    config = generate_cover_config()
    
    print("\n" + "=" * 60)
    print("✅ 封面图配置完成！")
    print("\n📋 下一步:")
    print("1. 使用配置中的prompt生成封面图")
    print("2. 或使用现有图片作为封面")
    print("3. 然后继续发布文章")
    print("\n💡 提示: 公众号发布可以没有封面图，但建议添加以提升点击率")

if __name__ == "__main__":
    main()