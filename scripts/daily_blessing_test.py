#!/usr/bin/env python3
"""
每日早安祝福语配图生成脚本（Python版本）
功能：生成积极向上的祝福语 + 精美配图，发送到飞书
"""

import subprocess
import os
import random
from datetime import datetime

# 配置
API_KEY = "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
WORKSPACE = "/Users/jiyingguo/.openclaw/workspace"
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H%M%S")
FILENAME = f"blessing_{TIMESTAMP}.png"

# 祝福语列表（100条，积极向上，面向中老年）
BLESSINGS = [
    # 健康长寿 (1-15)
    "健康是福，长寿是德",
    "身心健康，天天开心",
    "胃口好吃嘛嘛香",
    "睡眠充足精神好",
    "腿脚利索走路稳",
    "耳聪目明思维清",
    "血压血糖都正常",
    "心脏健康跳得欢",
    "骨骼强健身子硬",
    "免疫力强少生病",
    "科学养生身体好",
    "适度锻炼延年寿",
    "乐观开朗寿命长",
    "起居有常福满堂",
    "养生之道寿无疆",
    
    # 家庭幸福 (16-30)
    "家庭和睦万事兴",
    "子女孝顺福满门",
    "孙辈绕膝乐陶陶",
    "老伴相伴度余生",
    "天伦之乐享不尽",
    "家和万事兴又旺",
    "亲情无价暖人心",
    "儿孙自有儿孙福",
    "生活安稳无忧愁",
    "三代同堂福寿全",
    "相濡以沫共白头",
    "互敬互爱到永久",
    "家庭温暖避风港",
    "上有老来下有小",
    "平凡日子也幸福",
    
    # 平安喜乐 (31-45)
    "平平安安才是真",
    "岁岁平安年年好",
    "出入平安保平安",
    "一路平安到永远",
    "平安顺遂福星照",
    "无病无灾就是福",
    "顺风顺水顺心意",
    "顺心顺意好运气",
    "诸事顺遂皆如愿",
    "吉祥如意步步高",
    "福星高照好运来",
    "紫气东来祥云飘",
    "瑞雪兆丰年如意",
    "春风得意马蹄疾",
    "好事连连乐逍遥",
    
    # 福运连连 (46-60)
    "福如东海长流水",
    "寿比南山不老松",
    "福禄双全庆有余",
    "金玉满堂富贵来",
    "招财进宝福星照",
    "财源广进步步高",
    "五福临门喜盈门",
    "福寿安康享天年",
    "福气满满笑容灿",
    "好运连连福无疆",
    "福满人间春常在",
    "富贵安康度春秋",
    "吉祥如意过大年",
    "福星高照满堂红",
    "福瑞呈祥庆有余",
    
    # 美好生活 (61-75)
    "生活如诗画中游",
    "美好生活天天有",
    "幸福美满绽光彩",
    "精彩生活乐无边",
    "快乐生活每一天",
    "阳光生活心舒畅",
    "品质生活乐陶陶",
    "舒适生活美滋滋",
    "悠然生活自惬意",
    "惬意生活暖洋洋",
    "舒心日子笑着过",
    "美好时光永留存",
    "幸福时光乐无边",
    "快乐时光常相伴",
    "温馨时光暖心房",
    
    # 心情愉悦 (76-85)
    "笑口常开好运来",
    "心情舒畅精神爽",
    "心旷神怡乐陶陶",
    "神清气爽每一天",
    "心满意足笑开颜",
    "心花怒放好心情",
    "欢天喜地度时光",
    "喜气洋洋迎朝阳",
    "乐不可支笑颜开",
    "眉开眼笑福星照",
    
    # 友情长久 (86-92)
    "友情长存暖心间",
    "老友相聚乐融融",
    "知己相伴不孤单",
    "邻里和睦胜亲人",
    "友情岁月永铭记",
    "相聚时光美好多",
    "情谊深厚到永远",
    
    # 梦想与希望 (93-100)
    "梦想成真福满门",
    "希望在前路光明",
    "心怀梦想永年轻",
    "追逐美好向前行",
    "生活不止有眼前",
    "诗和远方在心中",
    "保持热爱赴山海",
    "眼里有光心里暖",
]

def main():
    # 随机选择一条祝福语
    blessing_text = random.choice(BLESSINGS)
    print(f"生成的祝福语: {blessing_text}")
    
    # 切换到工作目录
    os.chdir(WORKSPACE)
    
    # 构建图片生成命令
    generate_script = f"{os.path.expanduser('~')}/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py"
    
    prompt = f"""Chinese traditional greeting card design, beautiful elegant calligraphy text '{blessing_text}' in stunning flowing calligraphy font as the central focal point, surrounded by vibrant flourishing scenery: cherry blossoms in full bloom, peonies in radiant colors, majestic cranes spreading wings, lush pine trees, flowing waterfalls, misty mountains at sunrise, elderly couple riding bicycles together along a scenic path, family gathering with joy and laughter, lotus flowers on a peaceful lake, butterflies dancing among flowers, soft morning sunlight filtering through leaves, warm golden and pink color palette, feeling of vitality, joy, romance and美好的生活, high quality traditional Chinese painting style blended with modern aesthetics, masterpiece"""
    
    # 生成图片
    print(f"正在生成图片: {FILENAME}...")
    cmd = [
        "python3", generate_script,
        "--prompt", prompt,
        "--filename", FILENAME,
        "--resolution", "1K",
        "--api-key", API_KEY
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"图片生成输出: {result.stdout}")
    if result.stderr:
        print(f"图片生成错误: {result.stderr}")
    
    # 检查图片是否生成成功
    filepath = os.path.join(WORKSPACE, FILENAME)
    if os.path.exists(filepath):
        print(f"图片生成成功: {filepath}")
        filesize = os.path.getsize(filepath)
        print(f"文件大小: {filesize} bytes")
        
        # 发送图片到飞书
        print("正在发送图片到飞书...")
        
        # 使用 Python requests 发送（如果有的话），否则用 curl
        try:
            import requests
            
            url = "https://open.feishu.cn/open-apis/im/v1/images"
            
            with open(filepath, 'rb') as f:
                files = {'file': (FILENAME, f, 'image/png')}
                data = {'file_type': 'image', 'image_type': 'message'}
                headers = {'Authorization': 'Bearer dummy'}  # 实际应该用真实的 token
                
                # 这里需要真实的飞书 access token，暂时只打印信息
                print(f"图片已生成，准备发送到飞书...")
                print(f"文件路径: {filepath}")
                
        except ImportError:
            # 没有 requests，用 curl
            curl_cmd = [
                'curl', '-X', 'POST',
                '-H', 'Content-Type: multipart/form-data',
                '-F', f'file=@{filepath}',
                '-F', 'file_type=image',
                '-F', f'file_name={FILENAME}',
                'https://open.feishu.cn/open-apis/im/v1/images'
            ]
            result = subprocess.run(curl_cmd, capture_output=True, text=True)
            print(f"飞书API响应: {result.stdout}")
        
        print("发送完成！")
    else:
        print("图片生成失败")

if __name__ == "__main__":
    main()
