#!/usr/bin/env python3
"""
直接调用Gemini API生成图片（使用标准库urllib）
"""
import subprocess
import os
import random
from datetime import datetime
import json
import urllib.request
import urllib.parse

API_KEY = "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
WORKSPACE = "/Users/jiyingguo/.openclaw/workspace"

BLESSINGS = [
    "健康是福，长寿是德",
    "笑口常开好运来",
    "心旷神怡乐陶陶",
    "福如东海长流水",
    "生活如诗画中游",
    "家庭和睦万事兴",
    "平平安安才是真",
    "青春永驻，活力满满",
    "阳光心态，天天精彩",
    "幸福美满，诗意人生",
]

def main():
    blessing = random.choice(BLESSINGS)
    print(f"祝福语: {blessing}")
    
    # 构造API请求
    prompt = f"""Chinese traditional greeting card design, beautiful elegant calligraphy text '{blessing}' in stunning flowing calligraphy font as the central focal point, surrounded by vibrant flourishing scenery: cherry blossoms, peonies, cranes, sunrise, warm golden colors, traditional Chinese painting style, masterpiece"""
    
    # 使用Gemini API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.0-flash-preview:predict?key={API_KEY}"
    
    data = {
        "instances": [{"prompt": prompt}],
        "parameters": {"resolution": "1K"}
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=json_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("API响应:", json.dumps(result, indent=2)[:500])
            
            # 检查是否有图片数据
            if 'predictions' in result and len(result['predictions']) > 0:
                print("图片生成成功!")
            else:
                print("未返回图片数据")
                
    except Exception as e:
        print(f"API调用失败: {e}")
        
    print("测试完成")

if __name__ == "__main__":
    main()
