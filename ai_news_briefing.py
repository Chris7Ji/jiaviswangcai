#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""AI News Daily Briefing Generator and Email Sender"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import json

# Email configuration
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_AUTH_CODE = "icxhfzuyzbhbbjie"

# Recipients (15 people, primary)
RECIPIENTS = [
    "liuwei44259@huawei.com",
    "tiankunyang@huawei.com",
    "qinhongyi2@huawei.com",
    "jiawei18@huawei.com",
    "jiyingguo@huawei.com",
    "linfeng67@huawei.com",
    "lvluling1@huawei.com",
    "suqi1@huawei.com",
    "susha@huawei.com",
    "wangdongxiao@huawei.com",
    "xiongguifang@huawei.com",
    "xushengsheng@huawei.com",
    "zhangqianfeng2@huawei.com",
    "zhangyexing2@huawei.com",
    "86940135@qq.com"
]

# DeepSeek Translation API
DEEPSEEK_API_KEY = "sk-451f43ffa9764b7e91430e4d39538356"
DEEPSEEK_ENDPOINT = "https://api.deepseek.com/v1"

def translate_to_chinese(text):
    u"""Translate English text to Chinese using DeepSeek API"""
    import urllib.request
    import urllib.error
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a professional translator. Translate the following English text to Chinese. Keep it concise and professional, suitable for a news briefing. Only output the translation, nothing else."},
            {"role": "user", "content": text}
        ],
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(
        DEEPSEEK_ENDPOINT + "/chat/completions",
        data=json_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + DEEPSEEK_API_KEY
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Translation error: " + str(e))
        return text  # Return original if translation fails

def generate_html_newsletter(news_data, date_str):
    u"""Generate HTML newsletter"""
    
    html = (u'<!DOCTYPE html>\n'
            u'<html>\n'
            u'<head>\n'
            u'    <meta charset="UTF-8">\n'
            u'    <title>高校分队 AI 新闻每日简报 - ' + date_str + u'</title>\n'
            u'    <style>\n'
            u'        body { font-family: "Microsoft YaHei", Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }\n'
            u'        h1 { color: #1a1a1a; border-bottom: 3px solid #0077b6; padding-bottom: 10px; }\n'
            u'        h2 { color: #0077b6; margin-top: 30px; border-left: 4px solid #0077b6; padding-left: 10px; }\n'
            u'        .news-item { margin-bottom: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }\n'
            u'        .news-title { font-weight: bold; color: #333; font-size: 16px; }\n'
            u'        .news-summary { color: #555; margin-top: 8px; }\n'
            u'        .news-link { margin-top: 5px; }\n'
            u'        .news-link a { color: #0077b6; text-decoration: none; }\n'
            u'        .news-link a:hover { text-decoration: underline; }\n'
            u'        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; font-size: 12px; }\n'
            u'    </style>\n'
            u'</head>\n'
            u'<body>\n'
            u'    <h1>高校分队 AI 新闻每日简报</h1>\n'
            u'    <p style="color:#666;">日期：' + date_str + u' | 来源：TechCrunch, The Verge, 36氪, GitHub Trending, Hacker News</p>\n')
    
    for module_name, news_items in news_data.items():
        html += u'    <h2>' + module_name + u'</h2>\n'
        
        if not news_items:
            html += u'    <p>今日暂无重大更新</p>\n'
        else:
            for item in news_items:
                html += (u'    <div class="news-item">\n'
                        u'        <div class="news-title">' + item['title'] + u'</div>\n'
                        u'        <div class="news-summary">' + item['summary'] + u'</div>\n'
                        u'        <div class="news-link"><a href="' + item['url'] + u'" target="_blank">原文链接</a></div>\n'
                        u'    </div>\n')
    
    html += (u'    <div class="footer">\n'
             u'        <p>本简报由旺财Jarvis自动生成 | ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + u'</p>\n'
             u'    </div>\n'
             u'</body>\n'
             u'</html>')
    
    return html

def send_email(subject, html_content, recipients):
    u"""Send email using QQ SMTP"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = ', '.join(recipients)
    
    # Plain text version (fallback)
    text_content = "此邮件需要HTML支持。请使用支持HTML的邮件客户端查看。"
    msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
    
    # HTML version
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_AUTH_CODE)
        server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
        server.quit()
        print("Email sent successfully to " + str(len(recipients)) + " recipients")
        return True
    except Exception as e:
        print("Email sending failed: " + str(e))
        return False

# News data structure
today = datetime.now().strftime('%Y年%m月%d日')
date_str = datetime.now().strftime('%Y-%m-%d')

news_data = {
    u"一、全球顶尖大模型及公司动态": [
        {
            "title": u"OpenAI Sora视频生成服务正式关停，存活仅25个月",
            "summary": u"OpenAI于2024年2月推出Sora，2026年3月24日正式宣布关停该服务。Sora每天运营成本高达数千万美元，但商业化收入未能覆盖成本。此举被视为OpenAI战略重组、专注企业市场的重要信号。",
            "url": "https://techcrunch.com/2026/03/24/openais-sora-was-the-creepiest-app-on-your-phone-now-its-shutting-down/"
        },
        {
            "title": u"英伟达CEO黄仁勋称「我们已实现AGI」，引发业界争议",
            "summary": u"黄仁勋在采访中表示AGI已实现，但业界普遍认为这一定义过于宽泛。AGI至今没有统一标准，黄仁勋的定义被认为是在为英伟达GPU业务背书。",
            "url": "https://www.theverge.com/ai-artificial-intelligence/899086/jensen-huang-nvidia-agi"
        },
        {
            "title": u"苹果与谷歌达成Gemini授权协议，可用于训练端侧小模型",
            "summary": u"苹果可通过蒸馏谷歌Gemini大模型来训练专为iPhone和Mac设计的「学生」AI模型。这些小模型计算需求更低，更适合在设备端运行。",
            "url": "https://www.theverge.com/ai-artificial-intelligence/901014/apples-deal-with-google-lets-it-use-gemini-to-train-smaller-ai-models"
        },
        {
            "title": u"OpenAI洽谈收购核聚变公司Helion，Altman卸任董事会",
            "summary": u"OpenAI正与Altman个人投资的Helion Energy洽谈购电协议，计划到2035年获得50GW清洁能源供电。但核聚变技术本身仍面临重大科学挑战。",
            "url": "https://www.theverge.com/science/899231/openai-altman-nuclear-fusion-helion-electricity"
        },
        {
            "title": u"Anthropic Claude Code新增更安全的自动模式",
            "summary": u"Anthropic为Claude Code推出了更安全的自动模式，在赋予AI更多控制权的同时保持安全限制。该更新旨在提升开发者体验同时确保系统安全。",
            "url": "https://techcrunch.com/2026/03/24/anthropic-hands-claude-code-more-control-but-keeps-it-on-a-leash/"
        },
        {
            "title": u"ARM发布首款自研芯片，将用于Meta AI数据中心",
            "summary": u"ARM成立35年来首次推出自研CPU，将于今年晚些时候部署在Meta的AI数据中心。这是ARM从IP授权向垂直整合转型的重要标志。",
            "url": "https://techcrunch.com/2026/03/24/arm-is-releasing-its-first-in-house-chip-in-its-35-year-history/"
        }
    ],
    
    u"二、中国AI大模型最新进展": [
        {
            "title": u"MiniMax估值超3300亿元，B端业务增长亮眼但盈利承压",
            "summary": u"中国AI独角兽MiniMax估值已达3300亿元，超越百度市值。B端业务增长强劲，但高昂的算力成本仍制约盈利，商业化压力持续加大。",
            "url": "https://36kr.com/p/3738262674436864"
        },
        {
            "title": u"Cursor承认新编程模型基于Moonshot AI的Kimi构建",
            "summary": u"AI编程工具Cursor被曝光其最新编程模型基于中国Moonshot AI的Kimi模型构建，凸显中国AI模型在编程辅助领域的技术竞争力。",
            "url": "https://techcrunch.com/2026/03/22/cursor-admits-its-new-coding-model-was-built-on-top-of-moonshot-ais-kimi/"
        },
        {
            "title": u"OpenAI揭秘：AI「幻觉」可能是模型故意出错",
            "summary": u"OpenAI研究团队发现，部分被认为是AI幻觉的错误输出可能是模型「故意」生成的。这一发现对AI可信度和安全性研究具有重要意义。",
            "url": "https://36kr.com/p/3737905780064519"
        },
        {
            "title": u"宇树科技IPO获受理，人形机器人加速登陆资本市场",
            "summary": u"宇树科技IPO申请获受理，成为中国人形机器人企业登陆资本市场的先行者。机器人4S店开业、椰树招标等产业动作密集，行业发展进入新阶段。",
            "url": "https://36kr.com/p/3738094857908738"
        }
    ],
    
    u"三、AI软硬件及国产芯片生态": [
        {
            "title": u"Intel发布Arc Pro B70 GPU，专为AI工作负载设计",
            "summary": u"Intel推出Arc Pro B70「Big Battlegame」桌面GPU，32GB VRAM，32 Xe2核心，售价949美元。这是Intel在AI GPU市场的重要布局，瞄准专业AI推理市场。",
            "url": "https://www.theverge.com/tech/899948/intels-long-awaited-big-gpu-is-just-for-ai-and-starts-at-nearly-1000"
        },
        {
            "title": u"Google发布TurboQuant：全新AI内存压缩算法",
            "summary": u"Google推出TurboQuant内存压缩算法，可显著降低AI模型部署的内存需求。该技术被网友称为AI版的Pied Piper。",
            "url": "https://techcrunch.com/2026/03/25/google-turboquant-ai-memory-compression-silicon-valley-pied-piper/"
        },
        {
            "title": u"Google发布Lyria 3 Pro音乐生成模型",
            "summary": u"Google推出Lyria 3 Pro，可生成更长的AI音乐。与前代相比，生成质量和时长均有提升，音乐创作AI竞争加剧。",
            "url": "https://techcrunch.com/2026/03/25/google-launches-lyria-3-pro-music-generation-model/"
        },
        {
            "title": u"数据中心从AC向DC供电转型加速",
            "summary": u"IEEE报告显示，数据中心正加速从交流电（AC）向直流电（DC）供电转型，可显著提升能效、降低PUE。AI大模型训练的高功耗需求推动这一趋势。",
            "url": "https://spectrum.ieee.org/data-center-dc"
        }
    ],
    
    u"四、AI智能体前沿资讯": [
        {
            "title": u"「龙虾」大战升级：Claude获电脑控制能力",
            "summary": u"Anthropic密集更新回应OpenAI挑战。Claude新增电脑控制能力（Computer Use），可自主操作桌面应用。AI Agent竞争进入白热化阶段。",
            "url": "https://36kr.com/p/3738140731064324"
        },
        {
            "title": u"字节跳动DeepFlow开源项目火爆GitHub，斩获4.6万星",
            "summary": u"字节跳动开源的DeepFlow项目在GitHub上获得4.6万星，成为AI Agent框架热门项目。该项目支持沙子箱、记忆、工具、子Agent等功能，可处理从分钟到小时级别的复杂任务。",
            "url": "https://github.com/bytedance/deer-flow"
        },
        {
            "title": u"Ruvnet ruflo项目：Claude Agent编排平台获2.6万星",
            "summary": u"Ruvnet推出的ruflo项目是一个Claude Agent编排平台，支持多Agent协同、自主工作流编排、企业级架构，已获2.6万星关注。",
            "url": "https://github.com/ruvnet/ruflo"
        },
        {
            "title": u"Letta AI推出Claude Code「潜意识」模块",
            "summary": u"Letta AI发布claude-subconscious项目，为Claude Code赋予「潜意识」能力，可实现更深层次的上下文理解和推理规划。",
            "url": "https://github.com/letta-ai/claude-subconscious"
        }
    ],
    
    u"五、其他全球AI领域重要资讯": [
        {
            "title": u"美国参议院民主党议员拟将Anthropic的AI「红线」法典化",
            "summary": u"美国参议院民主党议员提议立法，将Anthropic自愿遵守的AI安全承诺（包括禁止自主武器和大规模监控）纳入法律框架。AI安全治理进入立法层面。",
            "url": "https://www.theverge.com/policy/900341/senator-schiff-anthropic-autonomous-weapons-mass-surveillance"
        },
        {
            "title": u"Anthropic与美国国防部诉讼案开庭审理",
            "summary": u"Anthropic就其被列入美国军方供应链风险名单一事起诉特朗普政府，案件已开庭审理。判决预计近日公布，对AI军事应用监管具有风向标意义。",
            "url": "https://www.theverge.com/ai-artificial-intelligence/899937/anthropic-and-the-pentagon-just-finished-sparring-in-court"
        },
        {
            "title": u"Meta AI眼镜因欧盟电池法规无法在欧洲上市",
            "summary": u"Meta的Ray-Ban Display智能眼镜因欧盟要求设备电池可拆卸的法规无法进入欧洲市场。此外AI监管和供应链问题也阻碍了全球化扩张。",
            "url": "https://www.theverge.com/ai-artificial-intelligence/900147/eu-battery-rules-are-blocking-metas-ai-glasses-expansion"
        },
        {
            "title": u"Kleiner Perkins推出35亿美元AI专项基金",
            "summary": u"老牌风投Kleiner Perkins宣布35亿美元AI专项基金完成募集，将全面押注AI领域。这是当前AI投资热潮的又一标志性事件。",
            "url": "https://techcrunch.com/2026/03/24/with-3-5b-in-fresh-capital-kleiner-perkins-is-going-all-in-on-ai/"
        },
        {
            "title": u"Trump成立包含扎克伯格、黄仁勋的新「科技顾问委员会」",
            "summary": u"特朗普宣布成立新的科技顾问委员会，Meta CEO扎克伯格和英伟达CEO黄仁勋加入。科技大佬与政府的关系进入新阶段。",
            "url": "https://www.theverge.com/policy/900340/trump-tech-panel-mark-zuckerberg-jensen-huang"
        }
    ]
}

# Generate newsletter
html_content = generate_html_newsletter(news_data, today)

# Email subject
subject = "[" + date_str + "] 高校分队 AI 新闻每日简报"

# Send email
print("Generating newsletter...")
print("Date: " + today)
total_items = sum(len(v) for v in news_data.values())
print("Total news items: " + str(total_items))
print("Recipients: " + str(len(RECIPIENTS)))
print("\n--- Newsletter Preview (first 500 chars) ---")
print(html_content[:500].encode('utf-8'))

print("\n--- Sending Email ---")
success = send_email(subject, html_content, RECIPIENTS)

if success:
    print("\n=== TASK COMPLETED SUCCESSFULLY ===")
    print("Recipients: " + str(len(RECIPIENTS)))
    print("Total news items: " + str(total_items))
    print("Search sources: TechCrunch, The Verge, 36氪, GitHub Trending, Hacker News")
else:
    print("\n=== TASK FAILED ===")
