#!/bin/bash
# 微信公众号封面图生成脚本

API_KEY="AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
PROMPT="Generate a professional WeChat public account cover image for the article titled '我的AI助手旺财：三天时间构建的四大能力体系'. Size: 900x383 pixels. Style: technology blue, clean, professional. Include AI robot, four capability icons, Chinese typography."

echo "🎨 生成微信公众号封面图"
echo "================================"

# 方法1: 使用Gemini API (文本生成)
echo ""
echo "方法1: 使用Gemini API生成图像描述"
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{
    "contents": [{
      "parts": [{
        "text": "$PROMPT"
      }]
    }]
  }" \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$API_KEY" \
  | jq -r '.candidates[0].content.parts[0].text' > cover_description.txt

echo "✅ 图像描述已保存到 cover_description.txt"

# 方法2: 使用DALL-E 3 (如果配置了OpenAI)
echo ""
echo "方法2: 使用DALL-E 3生成图像"
echo "需要配置OPENAI_API_KEY环境变量"
echo ""
echo "如果已配置OPENAI_API_KEY，运行:"
echo "python3 -c "import openai; openai.Image.create(prompt='$PROMPT', n=1, size='1024x1024')""

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
