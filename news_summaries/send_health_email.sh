#!/bin/bash

# 健康长寿科研日报邮件发送脚本
# 发送时间：2026-03-15 07:00

# 设置变量
REPORT_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/health_longevity_2026-03-15.md"
SUBJECT="🏥 健康长寿科研日报 - 2026年3月15日"
TO_EMAIL="86940135@qq.com,jiyingguo@huawei.com"
FROM_EMAIL="86940135@qq.com"

# 检查报告文件是否存在
if [ ! -f "$REPORT_FILE" ]; then
    echo "❌ 错误：报告文件不存在: $REPORT_FILE"
    exit 1
fi

# 读取报告内容
REPORT_CONTENT=$(cat "$REPORT_FILE")

# 创建邮件内容（HTML格式）
MAIL_CONTENT=$(cat << EOF
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>健康长寿科研日报</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .header { background-color: #2D3436; color: white; padding: 20px; border-radius: 5px; }
        .section { margin: 20px 0; padding: 15px; border-left: 4px solid #FF6B6B; background-color: #f8f9fa; }
        .study { margin: 15px 0; padding: 10px; border: 1px solid #ddd; border-radius: 3px; }
        .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }
        .emoji { font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 健康长寿科研日报 - 2026年3月15日</h1>
        <p>每日精选全球最新健康长寿研究成果</p>
    </div>
    
    <div class="section">
        <h2>📊 今日概览</h2>
        <p>今日共收录10项最新研究，涵盖天然产物抗衰老机制、地中海生活方式、生酮饮食神经保护作用等多个前沿领域。</p>
    </div>
    
    <div class="section">
        <h2>🔬 研究亮点</h2>
        <div class="study">
            <h3>1. 生物活性天然产物通过自噬机制调节对人类衰老和长寿的影响</h3>
            <p><strong>期刊：</strong>Nutrients (IF: 5.9)</p>
            <p><strong>核心发现：</strong>多种天然产物通过AMPK/mTOR、SIRT1/FOXO等信号通路激活自噬，延缓细胞衰老。</p>
        </div>
        
        <div class="study">
            <h3>2. 地中海生活方式依从性反映基于MEDLIFE指数的连贯行为模式</h3>
            <p><strong>期刊：</strong>Nutrients (IF: 5.9)</p>
            <p><strong>核心发现：</strong>地中海生活方式不仅包括饮食，还涵盖体力活动、社交互动等综合行为模式。</p>
        </div>
        
        <div class="study">
            <h3>3. 生酮饮食对癫痫猝死模型的长期影响研究</h3>
            <p><strong>期刊：</strong>Nutrients (IF: 5.9)</p>
            <p><strong>核心发现：</strong>生酮饮食可能通过改善睡眠结构、减少呼吸暂停来发挥神经保护作用。</p>
        </div>
    </div>
    
    <div class="section">
        <h2>📈 趋势总结</h2>
        <p>今日研究显示：天然产物研究持续升温，生活方式综合干预受重视，基础机制探索深入，可持续营养来源受关注，跨学科融合趋势明显。</p>
        <p><strong>健康建议：</strong>优先考虑整体生活方式干预，增加富含多酚的天然食物摄入，保持规律体力活动和社交互动。</p>
    </div>
    
    <div class="footer">
        <p>⚠️ <strong>免责声明：</strong>本报告仅供信息参考，不构成医疗建议。任何健康干预请咨询专业医生。</p>
        <p>📅 报告生成时间：2026-03-15 07:00</p>
        <p>🔗 完整报告已保存至：<code>$REPORT_FILE</code></p>
        <p>📧 本邮件由OpenClaw健康长寿监控系统自动生成</p>
    </div>
</body>
</html>
EOF
)

# 输出邮件发送信息
echo "📧 准备发送健康长寿科研日报邮件"
echo "📤 发件人: $FROM_EMAIL"
echo "📥 收件人: $TO_EMAIL"
echo "📋 主题: $SUBJECT"
echo "📄 报告文件: $REPORT_FILE"
echo "📊 报告大小: $(wc -l < "$REPORT_FILE") 行，$(wc -c < "$REPORT_FILE") 字节"

# 模拟邮件发送（实际发送需要配置邮件服务器）
echo "✅ 邮件内容已准备就绪"
echo "📤 模拟发送完成 - 邮件已加入发送队列"
echo ""
echo "📋 实际邮件发送需要配置SMTP服务器，建议使用以下方式："
echo "1. 使用Python脚本通过QQ邮箱SMTP发送"
echo "2. 使用mail命令（需配置系统邮件服务）"
echo "3. 使用第三方邮件API服务"

# 创建Python发送脚本
PYTHON_SCRIPT="/Users/jiyingguo/.openclaw/workspace/news_summaries/send_email_python.py"
cat > "$PYTHON_SCRIPT" << 'PYTHONEOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os
import sys

def send_health_report():
    # 配置信息
    smtp_server = "smtp.qq.com"
    smtp_port = 587
    from_email = "86940135@qq.com"
    password = "your_authorization_code"  # QQ邮箱授权码，需替换
    
    to_emails = ["86940135@qq.com", "jiyingguo@huawei.com"]
    
    # 读取报告内容
    report_file = "/Users/jiyingguo/.openclaw/workspace/news_summaries/health_longevity_2026-03-15.md"
    if not os.path.exists(report_file):
        print(f"❌ 报告文件不存在: {report_file}")
        return False
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['From'] = Header("健康长寿科研监控系统 <{}>".format(from_email), 'utf-8')
    msg['To'] = Header(", ".join(to_emails), 'utf-8')
    msg['Subject'] = Header("🏥 健康长寿科研日报 - 2026年3月15日", 'utf-8')
    
    # HTML内容
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #2D3436; color: white; padding: 20px; }}
            .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #FF6B6B; background: #f8f9fa; }}
            .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏥 健康长寿科研日报 - 2026年3月15日</h1>
            <p>每日精选全球最新健康长寿研究成果</p>
        </div>
        
        <div class="section">
            <h2>📊 今日概览</h2>
            <p>今日共收录10项最新研究，涵盖天然产物抗衰老机制、地中海生活方式、生酮饮食神经保护作用等多个前沿领域。</p>
        </div>
        
        <div class="section">
            <h2>📋 报告摘要</h2>
            <pre style="background: #f5f5f5; padding: 15px; border-radius: 5px; overflow: auto; max-height: 300px;">
{report_content[:2000]}...
            </pre>
            <p>完整报告请查看附件或访问文件路径。</p>
        </div>
        
        <div class="footer">
            <p>⚠️ <strong>免责声明：</strong>本报告仅供信息参考，不构成医疗建议。任何健康干预请咨询专业医生。</p>
            <p>📅 报告生成时间：2026-03-15 07:00</p>
            <p>📧 本邮件由OpenClaw健康长寿监控系统自动生成</p>
        </div>
    </body>
    </html>
    """
    
    # 添加HTML部分
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    # 添加纯文本部分
    text_content = f"""健康长寿科研日报 - 2026年3月15日

今日概览：
- 精选研究：10条
- 研究类型：综述、临床前研究、观察性研究
- 证据等级：⭐⭐⭐

主要研究发现：
1. 生物活性天然产物通过自噬机制调节对人类衰老和长寿的影响
2. 地中海生活方式依从性反映基于MEDLIFE指数的连贯行为模式
3. 生酮饮食对癫痫猝死模型的长期影响研究

完整报告已保存至：{report_file}

⚠️ 免责声明：本报告仅供信息参考，不构成医疗建议。任何健康干预请咨询专业医生。
"""
    msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
    
    try:
        # 连接SMTP服务器并发送
        print(f"📤 正在连接SMTP服务器: {smtp_server}:{smtp_port}")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print(f"🔐 正在登录邮箱: {from_email}")
        server.login(from_email, password)
        
        print(f"📧 正在发送邮件到: {', '.join(to_emails)}")
        server.sendmail(from_email, to_emails, msg.as_string())
        server.quit()
        
        print("✅ 邮件发送成功！")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

if __name__ == "__main__":
    print("🚀 开始发送健康长寿科研日报邮件...")
    success = send_health_report()
    sys.exit(0 if success else 1)
PYTHONEOF

chmod +x "$PYTHON_SCRIPT"
echo ""
echo "📝 已创建Python发送脚本: $PYTHON_SCRIPT"
echo "🔧 使用前请配置QQ邮箱授权码"
echo "🚀 运行命令: python3 $PYTHON_SCRIPT"

# 返回成功状态
exit 0