#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高校分队AI新闻简报邮件发送脚本 - 简化版（华为邮箱兼容）

功能：
- 使用QQ邮箱SMTP发送简化格式邮件
- 移除emoji，使用简洁的HTML格式
- 华为邮箱兼容版本
"""

import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# 配置信息
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_PASSWORD = "icxhfzuyzbhbbjie"

RECIPIENTS = [
    "jiyingguo@huawei.com",
    "xushengsheng@huawei.com",
    "86940135@qq.com"
]

def create_simple_html():
    """创建简化格式的HTML邮件内容"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高校分队 AI 新闻每日简报</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px;">
    <div style="background: #1e3a8a; color: white; padding: 20px; text-align: center; border-radius: 5px;">
        <h1 style="margin: 0; font-size: 24px;">高校分队 AI 新闻每日简报</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">2026年3月19日</p>
    </div>
    
    <div style="margin-top: 20px;">
        <h2 style="color: #1e3a8a; border-left: 4px solid #3b82f6; padding-left: 10px;">全球顶尖大模型及公司动态</h2>
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">Anthropic以73%概率保持3月最佳AI模型地位</p>
            <p style="margin: 0 0 10px 0; color: #666;">AI预测市场显示Anthropic打破Google六个月连胜纪录，在企业AI采用方面保持领先。</p>
            <a href="https://mlq.ai/prediction/brief/ai/ai-prediction-markets-anthropics-march-lead-faces-google-challenge-2026-03-07/" style="color: #3b82f6;">阅读原文</a>
        </div>
        
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">Google Gemini付费订阅同比增长258%</p>
            <p style="margin: 0 0 10px 0; color: #666;">Google Gemini展现出强劲增长势头，付费订阅者同比增长258%，超过Claude的200%增长。</p>
            <a href="https://ucstrategies.com/news/googles-ai-grew-258-while-openai-and-anthropic-fought-in-court/" style="color: #3b82f6;">阅读原文</a>
        </div>
        
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">GPT-5.4正式超越人类桌面任务基准测试表现</p>
            <p style="margin: 0 0 10px 0; color: #666;">OpenAI GPT-5.4在桌面任务基准测试中正式超越人类表现，标志着AI在复杂GUI操作方面取得重大突破。</p>
            <a href="http://kersai.com/ai-breakthroughs-in-2026-march-update/" style="color: #3b82f6;">阅读原文</a>
        </div>
    </div>
    
    <div style="margin-top: 20px;">
        <h2 style="color: #1e3a8a; border-left: 4px solid #3b82f6; padding-left: 10px;">中国AI大模型最新进展</h2>
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">DeepSeek V4发布：1万亿参数重置价格性能基准</p>
            <p style="margin: 0 0 10px 0; color: #666;">DeepSeek发布V4版本，拥有1万亿参数，在性能和成本方面实现重大突破。</p>
            <a href="https://www.abhs.in/blog/china-ai-model-war-doubao-qwen-deepseek-kimi-2026" style="color: #3b82f6;">阅读原文</a>
        </div>
        
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">字节跳动发布Doubao 2.0，中国AI聊天应用排名第一</p>
            <p style="margin: 0 0 10px 0; color: #666;">字节跳动正式发布Doubao 2.0，专为Agent时代设计，在成本效益方面具有显著优势。</p>
            <a href="https://www.reuters.com/world/asia-pacific/chinas-bytedance-releases-doubao-20-ai-chatbot-2026-02-14/" style="color: #3b82f6;">阅读原文</a>
        </div>
    </div>
    
    <div style="margin-top: 20px;">
        <h2 style="color: #1e3a8a; border-left: 4px solid #3b82f6; padding-left: 10px;">AI软硬件及国产芯片生态</h2>
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">华为发布Cloud Matrix 384超节点，部分性能超英伟达</p>
            <p style="margin: 0 0 10px 0; color: #666;">华为正式发布Cloud Matrix 384超节点，黄仁勋公开表示部分性能已超过英伟达产品。</p>
            <a href="https://news.southcn.com/node_17a07e5926/0543a47541.shtml" style="color: #3b82f6;">阅读原文</a>
        </div>
        
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">IDC：华为昇腾市场份额国内第一</p>
            <p style="margin: 0 0 10px 0; color: #666;">IDC数据显示，2025下半年华为昇腾在中国AI芯片市场份额位居第一。</p>
            <a href="https://news.caijingmobile.com/article/detail/563097?source_id=40" style="color: #3b82f6;">阅读原文</a>
        </div>
    </div>
    
    <div style="margin-top: 20px;">
        <h2 style="color: #1e3a8a; border-left: 4px solid #3b82f6; padding-left: 10px;">AI智能体前沿资讯</h2>
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">OpenClaw 2026.3.7发布：支持GPT-5.4和内存热插拔</p>
            <p style="margin: 0 0 10px 0; color: #666;">OpenClaw核心版本2026.3.7正式发布，新增对OpenAI GPT-5.4和Google最新前沿模型的原生支持。</p>
            <a href="https://news.aibase.com/news/26036" style="color: #3b82f6;">阅读原文</a>
        </div>
    </div>
    
    <div style="margin-top: 20px;">
        <h2 style="color: #1e3a8a; border-left: 4px solid #3b82f6; padding-left: 10px;">其他全球AI领域重要资讯</h2>
        <div style="background: #f8fafc; padding: 15px; margin: 10px 0; border-radius: 5px;">
            <p style="font-weight: bold; margin: 0 0 10px 0;">摩根士丹利预警：变革性AI飞跃即将到来</p>
            <p style="margin: 0 0 10px 0; color: #666;">摩根士丹利发布报告警告，由顶级AI实验室前所未有的算力积累驱动，变革性AI突破即将到来。</p>
            <a href="https://finance.yahoo.com/news/morgan-stanley-warns-ai-breakthrough-072000084.html" style="color: #3b82f6;">阅读原文</a>
        </div>
    </div>
    
    <div style="margin-top: 30px; padding: 15px; background: #f1f5f9; text-align: center; border-radius: 5px; color: #666; font-size: 12px;">
        <p>高校分队 AI 新闻每日简报 | 由旺财Jarvis自动生成</p>
        <p>2026年3月19日 | 数据来源：Tavily AI Search</p>
    </div>
</body>
</html>"""
    return html

def send_email():
    """发送邮件"""
    try:
        # 创建邮件
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "2026年3月19日 高校分队- AI 新闻每日简报：GPT-5.4超越人类表现"
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECIPIENTS)
        
        # 获取HTML内容
        html_content = create_simple_html()
        
        # 添加HTML内容
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        # 连接SMTP服务器
        print(f"Connecting to {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        
        # 登录
        print("Logging in...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # 发送邮件
        print(f"Sending email to: {', '.join(RECIPIENTS)}")
        server.sendmail(SENDER_EMAIL, RECIPIENTS, msg.as_string())
        
        # 关闭连接
        server.quit()
        
        print("Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    success = send_email()
    sys.exit(0 if success else 1)
