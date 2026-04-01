#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最后尝试发送邮件 - 使用最简化的方式
"""

import subprocess
import os
from datetime import datetime

def send_via_sendmail():
    """使用sendmail命令发送邮件"""
    
    # 创建邮件内容
    email_content = f"""From: Jarvis AI助手 <jarvis@openclaw.ai>
To: 86940135@qq.com, jiyingguo@huawei.com
Subject: AI新闻每日摘要 - {datetime.now().strftime('%Y年%m月%d日')}
Content-Type: text/plain; charset=utf-8

尊敬的Boss，

由于QQ邮箱SMTP服务暂时受限，今日AI新闻摘要已通过飞书完整发送。

今日新闻头条：
1. ⚠️ AI战争模拟风险 - 95%情况下AI首选核打击
2. 💰 智谱AI启动IPO - 国内"AI六小龙"首家
3. 🧮 Claude数学突破 - 仅31步攻克图论猜想
4. 🤖 具身智能养老 - 破解失能老人照护难题
5. 📝 AI内容水印制度 - 人大代表建议不可去除标识
6. 🏠 家庭服务机器人 - 前小米高管入局获顶级VC竞逐
7. 🏞️ DeepSeek景区应用 - 国产大模型旅游场景获好评
8. 📈 2026年AI趋势 - 垂直领域、世界模型与智能体工程

AI指数: 📈 78/100（较昨日+2）

完整内容请查看飞书消息，或访问本地文件：
/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_2026-03-05.md

需要重新配置邮箱发送功能，请提供新的QQ邮箱授权码。

祝好！
Jarvis AI助手
{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
"""
    
    # 尝试发送
    try:
        # 写入临时文件
        with open("/tmp/email_temp.txt", "w", encoding="utf-8") as f:
            f.write(email_content)
        
        # 使用sendmail发送
        result = subprocess.run(
            ["sendmail", "-t"],
            input=email_content.encode("utf-8"),
            capture_output=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ 邮件发送成功（通过sendmail）")
            return True
        else:
            print(f"❌ sendmail失败: {result.stderr.decode()}")
            return False
            
    except FileNotFoundError:
        print("❌ sendmail命令未找到")
        return False
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def send_via_curl():
    """使用curl通过邮件API发送"""
    
    # 简化邮件内容
    simple_content = f"AI新闻每日摘要 - {datetime.now().strftime('%Y-%m-%d')}\\n\\n今日头条：AI战争模拟风险、智谱AI IPO、Claude数学突破等8条重要新闻。完整内容已通过飞书发送。"
    
    # 尝试使用mailgun或其他免费邮件API（需要配置）
    print("⚠️ 需要配置邮件API服务（如Mailgun、SendGrid等）")
    return False

if __name__ == "__main__":
    print("尝试最后一种邮件发送方案...")
    
    # 尝试sendmail
    if send_via_sendmail():
        print("🎉 邮件发送成功！")
    else:
        print("\n😞 邮件发送失败。建议：")
        print("1. 检查QQ邮箱网页版，重新生成授权码")
        print("2. 确保SMTP服务已开启")
        print("3. 或提供其他邮箱配置")
        print("\n✅ 新闻内容已通过飞书完整发送")
        print("✅ 语音播报MP3已发送到飞书")
        print("✅ 本地文件已保存")