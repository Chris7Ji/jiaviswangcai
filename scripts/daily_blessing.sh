#!/bin/bash
# 每日早安祝福语配图生成脚本 v2
# 功能：生成积极向上的祝福语 + 精美写实风景配图，发送到飞书
# 风格：优美写实风景 + 中文书法祝福语，让人心旷神怡

# 配置
API_KEY="AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"
WORKSPACE="/Users/jiyingguo/.openclaw/workspace"
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
FILENAME="blessing_${TIMESTAMP}.png"

# 祝福语列表（100条，积极向上，面向中老年）
BLESSINGS=(
    # 健康长寿 (1-15)
    "健康是福，长寿是德"
    "身心健康，天天开心"
    "胃口好吃嘛嘛香"
    "睡眠充足精神好"
    "腿脚利索走路稳"
    "耳聪目明思维清"
    "血压血糖都正常"
    "心脏健康跳得欢"
    "骨骼强健身子硬"
    "免疫力强少生病"
    "科学养生身体好"
    "适度锻炼延年寿"
    "乐观开朗寿命长"
    "起居有常福满堂"
    "养生之道寿无疆"
    
    # 家庭幸福 (16-30)
    "家庭和睦万事兴"
    "子女孝顺福满门"
    "孙辈绕膝乐陶陶"
    "老伴相伴度余生"
    "天伦之乐享不尽"
    "家和万事兴又旺"
    "亲情无价暖人心"
    "儿孙自有儿孙福"
    "生活安稳无忧愁"
    "三代同堂福寿全"
    "相濡以沫共白头"
    "互敬互爱到永久"
    "家庭温暖避风港"
    "上有老来下有小"
    "平凡日子也幸福"
    
    # 平安喜乐 (31-45)
    "平平安安才是真"
    "岁岁平安年年好"
    "出入平安保平安"
    "一路平安到永远"
    "平安顺遂福星照"
    "无病无灾就是福"
    "顺风顺水顺心意"
    "顺心顺意好运气"
    "诸事顺遂皆如愿"
    "吉祥如意步步高"
    "福星高照好运来"
    "紫气东来祥云飘"
    "瑞雪兆丰年如意"
    "春风得意马蹄疾"
    "好事连连乐逍遥"
    
    # 福运连连 (46-60)
    "福如东海长流水"
    "寿比南山不老松"
    "福禄双全庆有余"
    "金玉满堂富贵来"
    "招财进宝福星照"
    "财源广进步步高"
    "五福临门喜盈门"
    "福寿安康享天年"
    "福气满满笑容灿"
    "好运连连福无疆"
    "福满人间春常在"
    "富贵安康度春秋"
    "吉祥如意过大年"
    "福星高照满堂红"
    "福瑞呈祥庆有余"
    
    # 美好生活 (61-75)
    "生活如诗画中游"
    "美好生活天天有"
    "幸福美满绽光彩"
    "精彩生活乐无边"
    "快乐生活每一天"
    "阳光生活心舒畅"
    "品质生活乐陶陶"
    "舒适生活美滋滋"
    "悠然生活自惬意"
    "惬意生活暖洋洋"
    "舒心日子笑着过"
    "美好时光永留存"
    "幸福时光乐无边"
    "快乐时光常相伴"
    "温馨时光暖心房"
    
    # 心情愉悦 (76-85)
    "笑口常开好运来"
    "心情舒畅精神爽"
    "心旷神怡乐陶陶"
    "神清气爽每一天"
    "心满意足笑开颜"
    "心花怒放好心情"
    "欢天喜地度时光"
    "喜气洋洋迎朝阳"
    "乐不可支笑颜开"
    "眉开眼笑福星照"
    
    # 友情长久 (86-92)
    "友情长存暖心间"
    "老友相聚乐融融"
    "知己相伴不孤单"
    "邻里和睦胜亲人"
    "友情岁月永铭记"
    "相聚时光美好多"
    "情谊深厚到永远"
    
    # 梦想与希望 (93-100)
    "梦想成真福满门"
    "希望在前路光明"
    "心怀梦想永年轻"
    "追逐美好向前行"
    "生活不止有眼前"
    "诗和远方在心中"
    "保持热爱赴山海"
    "眼里有光心里暖"
)

# 随机选择一条祝福语
RANDOM_INDEX=$((RANDOM % ${#BLESSINGS[@]}))
BLESSING_TEXT="${BLESSINGS[$RANDOM_INDEX]}"

echo "生成的祝福语: ${BLESSING_TEXT}"

# 随机选择一组风景主题 (每次生成不同风格的优美写实风景)
SCENIC_INDEX=$((RANDOM % 10))
case $SCENIC_INDEX in
    0) SCENIC_PROMPT=" breathtaking tropical beach with crystal clear turquoise water, pristine white sandy beach, coconut palm trees swaying gently, soft golden sunset light, turquoise waves gently lapping shore, professional photography, National Geographic style, 8K resolution "
        ;;
    1) SCENIC_PROMPT=" stunning Provence lavender field in full bloom, endless purple lavender rows stretching to horizon, warm golden sunlight, distant rolling hills, bees buzzing, traditional French farmhouse, fragrant warm breeze, romantic atmosphere, fine art photography, 8K resolution "
        ;;
    2) SCENIC_PROMPT=" peaceful Japanese cherry blossom scene in spring, soft pink sakura petals falling like snow, traditional wooden temple with curved roof, koi pond with lotus flowers, stone lantern, Mt Fuji in background with cap clouds, serene morning light, magical atmosphere, professional photography, 8K resolution "
        ;;
    3) SCENIC_PROMPT=" majestic Jiuzhaigou colorful lake landscape, crystal clear turquoise water reflecting autumn foliage, vibrant red yellow orange leaves on surrounding mountains, flowing stream connecting pearl waterfall, magical fairy tale scenery, soft diffused light through trees, nature photography masterpiece, 8K resolution "
        ;;
    4) SCENIC_PROMPT=" enchanting flower meadow with colorful wildflowers, poppies cornflowers daisies lavender in full bloom, butterflies fluttering, warm golden afternoon sunlight, rolling green hills in background, idyllic countryside pastoral scene, storybook landscape, fine art photography, 8K resolution "
        ;;
    5) SCENIC_PROMPT=" spectacular sunset over the ocean, golden orange red sky reflecting on calm sea, silhouettes of palm trees, gentle waves with sparkles, cumulus clouds painted in warm colors, peaceful romantic atmosphere, travel photography, 8K resolution "
        ;;
    6) SCENIC_PROMPT=" beautiful bamboo forest pathway in China, tall green bamboo stalks filtering soft dappled sunlight, moss-covered stone path winding through grove, gentle stream nearby, tranquil zen atmosphere, traditional Chinese landscape painting feeling, photorealistic, 8K resolution "
        ;;
    7) SCENIC_PROMPT=" breathtaking Swiss alpine meadow at sunrise, snow-capped Jungfrau mountain in background, wildflowers covering green valley, crystal clear alpine lake with mountain reflection, soft morning golden light, traditional wooden chalet, peaceful paradise atmosphere, award-winning landscape photography, 8K resolution "
        ;;
    8) SCENIC_PROMPT=" mesmerizing autumn forest path, golden red orange maple trees forming canopy overhead, sunlight filtering through colorful foliage, fallen leaves on winding stone path, soft misty atmosphere, fairy tale forest feeling, warm afternoon light, fine art nature photography, 8K resolution "
        ;;
    9) SCENIC_PROMPT=" spectacular Tulip fields in Netherlands in spring, endless rows of red yellow pink purple tulips stretching to horizon, traditional Dutch windmill in background, fluffy white clouds, bright sunny day, vibrant colors, iconic landscape, professional photography, 8K resolution "
        ;;
esac

# 构建完整提示词：写实优美风景 + 祝福语书法
FULL_PROMPT="Chinese blessing card, elegant flowing calligraphy text '${BLESSING_TEXT}' as central focal point in gold/white color, overlaid on breathtaking ${SCENIC_PROMPT} The calligraphy should be graceful and harmonious with the scene, creating a sense of peace, joy and美好的祝福, warm color tones, professional graphic design, high quality, masterpiece"

echo "风景主题: ${SCENIC_INDEX}"

# 生成图片
cd "${WORKSPACE}" || exit 1
uv run ~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py \
    --prompt "${FULL_PROMPT}" \
    --filename "${FILENAME}" \
    --resolution 2K \
    --api-key "${API_KEY}"

# 检查图片是否生成成功
if [ -f "${WORKSPACE}/${FILENAME}" ]; then
    echo "图片生成成功: ${FILENAME}"
    
    # 使用 Python 脚本发送图片到飞书（绕过 OpenClaw message 工具的 bug）
    python3 << 'PYTHON_SCRIPT'
import subprocess
import json
import sys
import os

WORKSPACE = os.environ.get('WORKSPACE', '/Users/jiyingguo/.openclaw/workspace')
FILENAME = os.environ.get('FILENAME', '')

# 获取 Token
token_cmd = '''curl -s -X POST -H Content-Type: application/json -d '{"app_id":"cli_a9f596118438dcef","app_secret":"42X7fiT1ZWm3SxIJndukBeKrru1VHpGo"}' https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'''
token_result = subprocess.run(token_cmd, shell=True, capture_output=True, text=True)
token_data = json.loads(token_result.stdout)
token = token_data.get('tenant_access_token', '')

if not token:
    print('获取Token失败')
    sys.exit(1)

# 上传图片
image_path = f"{WORKSPACE}/{FILENAME}"
upload_cmd = f'''curl -s -X POST -H 'Authorization: Bearer {token}' -F 'image_type=message' -F 'image=@{image_path}' https://open.feishu.cn/open-apis/im/v1/images'''
upload_result = subprocess.run(upload_cmd, shell=True, capture_output=True, text=True)

try:
    upload_data = json.loads(upload_result.stdout)
    img_key = upload_data.get('data', {}).get('image_key', '')
except:
    print(f'上传响应解析失败: {upload_result.stdout[:200]}')
    sys.exit(1)

if img_key:
    # 发送消息
    msg_data = {
        'receive_id': 'ou_b6c7778820b20031cd97bdc45d1cd9fa',
        'receive_id_type': 'open_id',
        'msg_type': 'image',
        'content': json.dumps({'image_key': img_key})
    }
    msg_cmd = f"""curl -s -X POST -H 'Authorization: Bearer {token}' -H 'Content-Type: application/json' -d '{json.dumps(msg_data)}' 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id'"""
    msg_result = subprocess.run(msg_cmd, shell=True, capture_output=True, text=True)
    print(f'发送成功: {img_key}')
else:
    print(f'图片上传失败: {upload_result.stdout[:200]}')
    sys.exit(1)
PYTHON_SCRIPT
    echo "发送完成！"
else
    echo "图片生成失败"
    exit 1
fi
