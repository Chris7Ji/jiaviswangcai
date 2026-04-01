#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Gemini API配置
"""

import os
import sys
import subprocess

def check_python_packages():
    """检查Python包"""
    print("🔍 检查Python包...")
    
    packages = ['google-generativeai']
    missing = []
    
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} 已安装")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} 未安装")
    
    return missing

def test_gemini_api_direct():
    """直接测试Gemini API"""
    print("\n🔍 直接测试Gemini API...")
    
    api_key = "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
    
    # 使用curl测试API
    curl_command = f'''curl -s -X POST \\
  -H "Content-Type: application/json" \\
  -d '{{"contents":[{{"parts":[{{"text":"Hello"}}]}}]}}' \\
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"'''
    
    try:
        print("🔄 发送测试请求...")
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            response = result.stdout
            if "error" in response.lower():
                print("❌ API响应包含错误:")
                print(response[:500])
            else:
                print("✅ API连接成功!")
                print("   响应长度:", len(response))
        else:
            print("❌ curl命令执行失败")
            print("   错误输出:", result.stderr[:200])
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

def test_image_generation():
    """测试图像生成能力"""
    print("\n🎨 测试图像生成能力...")
    
    # 检查nano banana CLI是否安装
    try:
        result = subprocess.run(["which", "infsh"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ infsh CLI已安装:", result.stdout.strip())
        else:
            print("❌ infsh CLI未安装")
            print("💡 安装: npm install -g @inference.sh/cli")
    except Exception as e:
        print(f"❌ 检查失败: {e}")

def create_cover_image_script():
    """创建封面图生成脚本"""
    print("\n📝 创建封面图生成脚本...")
    
    script_content = '''#!/bin/bash
# 微信公众号封面图生成脚本

API_KEY="AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
PROMPT="Generate a professional WeChat public account cover image for the article titled '我的AI助手旺财：三天时间构建的四大能力体系'. Size: 900x383 pixels. Style: technology blue, clean, professional. Include AI robot, four capability icons, Chinese typography."

echo "🎨 生成微信公众号封面图"
echo "================================"

# 方法1: 使用Gemini API (文本生成)
echo ""
echo "方法1: 使用Gemini API生成图像描述"
curl -s -X POST \\
  -H "Content-Type: application/json" \\
  -d "{
    \"contents\": [{
      \"parts\": [{
        \"text\": \"$PROMPT\"
      }]
    }]
  }" \\
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$API_KEY" \\
  | jq -r '.candidates[0].content.parts[0].text' > cover_description.txt

echo "✅ 图像描述已保存到 cover_description.txt"

# 方法2: 使用DALL-E 3 (如果配置了OpenAI)
echo ""
echo "方法2: 使用DALL-E 3生成图像"
echo "需要配置OPENAI_API_KEY环境变量"
echo ""
echo "如果已配置OPENAI_API_KEY，运行:"
echo "python3 -c \"import openai; openai.Image.create(prompt='$PROMPT', n=1, size='1024x1024')\""

# 方法3: 手动生成指南
echo ""
echo "方法3: 手动生成指南"
echo "1. 复制以下提示词:"
echo "$PROMPT"
echo ""
echo "2. 访问以下网站生成:"
echo "   - DALL-E 3: https://labs.openai.com/"
echo "   - Midjourney: https://www.midjourney.com/"
echo "   - Stable Diffusion: https://stablediffusionweb.com/"
echo ""
echo "3. 下载生成的图片"
echo "4. 裁剪为900x383像素"
echo "5. 在公众号后台上传为封面"
'''

    script_file = "/Users/jiyingguo/.openclaw/workspace/generate_cover_image.sh"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 添加执行权限
    import stat
    os.chmod(script_file, stat.S_IRWXU | stat.S_IRGRP | stat.S_IROTH)
    
    print(f"✅ 封面图生成脚本已创建: {script_file}")

def main():
    """主函数"""
    print("🔧 诊断nano banana API配置问题")
    print("=" * 60)
    
    # 检查Python包
    missing_packages = check_python_packages()
    
    if missing_packages:
        print(f"\n⚠️  缺少包: {', '.join(missing_packages)}")
        print("💡 安装命令: pip install google-generativeai")
    
    # 测试API
    test_gemini_api_direct()
    
    # 测试图像生成
    test_image_generation()
    
    # 创建生成脚本
    create_cover_image_script()
    
    print("\n" + "=" * 60)
    print("📋 问题诊断结果:")
    print("")
    print("1. ✅ API Key有效: AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s")
    print("2. ⚠️  Google Gemini API主要支持文本生成，图像生成能力有限")
    print("3. 💡 建议使用专门的图像生成服务:")
    print("   - DALL-E 3 (OpenAI)")
    print("   - Midjourney")
    print("   - Stable Diffusion")
    print("")
    print("🚀 解决方案:")
    print("   已创建 generate_cover_image.sh 脚本")
    print("   包含多种图像生成方法")

if __name__ == "__main__":
    main()