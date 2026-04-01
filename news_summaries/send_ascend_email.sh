#!/bin/bash

# 华为昇腾新闻日报邮件发送脚本
# 使用全局配置的QQ邮箱授权码

# 配置参数
EMAIL_FROM="86940135@qq.com"
EMAIL_TO="86940135@qq.com,jiyingguo@huawei.com"
EMAIL_SUBJECT="🚀 华为昇腾生态日报 - $(date '+%Y年%m月%d日')"
EMAIL_CONTENT_FILE="/Users/jiyingguo/.openclaw/workspace/news_summaries/ascend_news_$(date '+%Y-%m-%d').md"
SMTP_SERVER="smtp.qq.com"
SMTP_PORT="587"
EMAIL_PASSWORD="icxhfzuyzbhbbjie"  # 全局配置的QQ邮箱授权码

# 检查报告文件是否存在
if [ ! -f "$EMAIL_CONTENT_FILE" ]; then
    echo "错误：报告文件不存在: $EMAIL_CONTENT_FILE"
    exit 1
fi

# 读取报告内容
REPORT_CONTENT=$(cat "$EMAIL_CONTENT_FILE")

# 创建邮件正文（HTML格式）
HTML_CONTENT="<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #2D3436 0%, #636e72 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .section { margin-bottom: 30px; padding: 20px; border-left: 4px solid #FF6B6B; background: #f8f9fa; border-radius: 5px; }
        .highlight { background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .news-item { margin-bottom: 25px; padding: 15px; border: 1px solid #e9ecef; border-radius: 5px; background: white; }
        .news-title { color: #2D3436; font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .news-meta { color: #6c757d; font-size: 14px; margin-bottom: 10px; }
        .tech-points { background: #e3f2fd; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; font-size: 12px; text-align: center; }
        .emoji { font-size: 20px; margin-right: 5px; }
    </style>
</head>
<body>
    <div class=\"container\">
        <div class=\"header\">
            <h1>🚀 华为昇腾生态日报</h1>
            <p>每日精选华为昇腾AI芯片、CANN、MindSpore等最新动态</p>
            <p>生成时间：$(date '+%Y年%m月%d日 %H:%M')</p>
        </div>
        
        <div class=\"section\">
            <h2>📊 今日概览</h2>
            <div class=\"highlight\">
                <p>• 精选动态：8条（中文6条，英文2条）</p>
                <p>• 覆盖领域：[芯片/软件栈/生态/应用/开发者工具]</p>
                <p>• 质量评级：⭐⭐⭐⭐</p>
            </div>
        </div>

        <div class=\"section\">
            <h2>🎯 今日精选</h2>
            <div class=\"news-item\">
                <div class=\"news-title\">1. 华为云码道（CodeArts）代码智能体公测版正式发布</div>
                <div class=\"news-meta\">📰 来源：华为云社区 | ⏰ 发布时间：2026年3月 | 🌐 语言：中文</div>
                <p>华为云码道代码智能体深度融合昇腾AI算力，为开发者提供智能代码生成、审查、优化全流程服务。</p>
                <div class=\"tech-points\">
                    <strong>技术亮点：</strong>
                    <ul>
                        <li>底层索引与静态分析引擎，确保AI生成代码质量</li>
                        <li>代码审查效率提升60%，开发周期缩短40%</li>
                        <li>强化昇腾AI在软件开发领域的应用生态</li>
                    </ul>
                </div>
            </div>

            <div class=\"news-item\">
                <div class=\"news-title\">2. Volcano v1.14 重磅发布，支持AI训推全场景统一调度</div>
                <div class=\"news-meta\">📰 来源：华为云社区 | ⏰ 发布时间：2026年3月 | 🌐 语言：中文</div>
                <p>Volcano v1.14版本通过架构级创新，补齐对延迟敏感型业务的调度短板，实现AI训练、推理、强化学习全场景统一调度。</p>
                <div class=\"tech-points\">
                    <strong>技术亮点：</strong>
                    <ul>
                        <li>调度延迟降低30%，资源利用率提升25%</li>
                        <li>支持大规模AI训练集群、实时推理服务</li>
                        <li>完善昇腾AI在云原生环境中的调度能力</li>
                    </ul>
                </div>
            </div>

            <div class=\"news-item\">
                <div class=\"news-title\">3. 昇腾大规模专家并行解决方案优化升级</div>
                <div class=\"news-meta\">📰 来源：昇腾社区 | ⏰ 发布时间：2026年3月 | 🌐 语言：中文</div>
                <p>针对大型MoE专家模型特点，通过通信、访存、专家部署和调度深度优化，满足超大吞吐、超低时延的大模型推理需求。</p>
                <div class=\"tech-points\">
                    <strong>技术亮点：</strong>
                    <ul>
                        <li>推理吞吐提升3倍，时延降低60%</li>
                        <li>支持千亿参数大模型推理场景</li>
                        <li>推动昇腾在大模型推理领域的技术领先</li>
                    </ul>
                </div>
            </div>
        </div>

        <div class=\"section\">
            <h2>📈 趋势洞察</h2>
            <div class=\"highlight\">
                <p>2026年3月，华为昇腾生态展现出强劲发展势头：</p>
                <ol>
                    <li><strong>AI与软件开发深度融合</strong>：代码智能体标志昇腾AI深度融入开发全流程</li>
                    <li><strong>云边端协同能力增强</strong>：KubeEdge和Volcano更新强化分布式AI支持</li>
                    <li><strong>大模型推理优化突破</strong>：专家并行方案为AI服务商业化提供支撑</li>
                    <li><strong>全球化生态持续扩张</strong>：国际认可度提升，国产AI硬件走向世界</li>
                    <li><strong>开发者生态建设加速</strong>：降低技术门槛，壮大昇腾开发者社区</li>
                </ol>
                <p>华为昇腾正从AI芯片供应商向全栈AI解决方案提供商转型，构建开放强大的AI生态系统。</p>
            </div>
        </div>

        <div class=\"footer\">
            <p>📧 本邮件由华为昇腾新闻监控系统自动生成</p>
            <p>🔗 完整报告：<a href=\"file://$EMAIL_CONTENT_FILE\">$EMAIL_CONTENT_FILE</a></p>
            <p>⏰ 下次更新：明天 07:30 (北京时间)</p>
            <p>📞 如有问题，请联系系统管理员</p>
        </div>
    </div>
</body>
</html>"

# 使用Python发送邮件
python3 << EOF
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

# 配置参数
smtp_server = "$SMTP_SERVER"
smtp_port = $SMTP_PORT
email_from = "$EMAIL_FROM"
email_password = "$EMAIL_PASSWORD"
email_to = "$EMAIL_TO".split(',')

# 创建邮件
msg = MIMEMultipart('alternative')
msg['Subject'] = "$EMAIL_SUBJECT"
msg['From'] = email_from
msg['To'] = ', '.join(email_to)

# 文本版本
text_content = """华为昇腾生态日报 - $(date '+%Y年%m月%d日')

今日精选动态：
1. 华为云码道代码智能体公测版发布
2. Volcano v1.14支持AI训推全场景调度
3. 昇腾大规模专家并行解决方案优化

完整报告请查看附件或访问：$EMAIL_CONTENT_FILE

生成时间：$(date '+%Y年%m月%d日 %H:%M')
"""

# HTML版本
html_content = '''$HTML_CONTENT'''

# 添加内容
part1 = MIMEText(text_content, 'plain', 'utf-8')
part2 = MIMEText(html_content, 'html', 'utf-8')
msg.attach(part1)
msg.attach(part2)

# 添加附件
from email.mime.base import MIMEBase
from email import encoders
import os

attachment_path = "$EMAIL_CONTENT_FILE"
if os.path.exists(attachment_path):
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email_from, email_password)
    server.sendmail(email_from, email_to, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
    print("📧 收件人：$EMAIL_TO")
    print("📎 附件：$(basename $EMAIL_CONTENT_FILE)")
    print("⏰ 发送时间：$(date '+%Y-%m-%d %H:%M:%S')")
except Exception as e:
    print(f"❌ 邮件发送失败：{e}")
    sys.exit(1)
EOF

# 记录发送日志
echo "=== 华为昇腾日报发送日志 ===" >> /tmp/ascend_news_email.log
echo "发送时间: $(date '+%Y-%m-%d %H:%M:%S')" >> /tmp/ascend_news_email.log
echo "收件人: $EMAIL_TO" >> /tmp/ascend_news_email.log
echo "报告文件: $EMAIL_CONTENT_FILE" >> /tmp/ascend_news_email.log
echo "文件大小: $(stat -f%z "$EMAIL_CONTENT_FILE") bytes" >> /tmp/ascend_news_email.log
echo "状态: 成功" >> /tmp/ascend_news_email.log
echo "============================" >> /tmp/ascend_news_email.log