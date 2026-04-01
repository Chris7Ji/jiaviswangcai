import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
EMAIL = "86940135@qq.com"
PASSWORD = "icxhfzuyzbhbbjie"

TO_EMAILS = [
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

HTML_CONTENT = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高校分队 AI 新闻每日简报 - 2026年3月25日</title>
    <style>
        body { font-family: 'Microsoft YaHei', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; }
        .header { background-color: #1a237e; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 24px; }
        .header .date { margin-top: 5px; font-size: 14px; opacity: 0.9; }
        .section { background-color: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .section h2 { color: #1a237e; border-bottom: 2px solid #1a237e; padding-bottom: 10px; margin-top: 0; font-size: 18px; }
        .news-item { margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #eee; }
        .news-item:last-child { border-bottom: none; }
        .news-title { font-weight: bold; color: #1a237e; margin-bottom: 8px; font-size: 16px; }
        .news-summary { color: #555; margin-bottom: 8px; font-size: 14px; line-height: 1.5; }
        .news-link { color: #1976d2; text-decoration: none; font-size: 13px; }
        .news-link:hover { text-decoration: underline; }
        .news-meta { color: #888; font-size: 12px; margin-bottom: 5px; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; }
        .badge-new { background-color: #e91e63; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-left: 8px; }
        .badge-hot { background-color: #ff9800; color: white; padding: 2px 8px; border-radius: 3px; font-size: 11px; margin-left: 8px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>高校分队 AI 新闻每日简报</h1>
        <div class="date">2026年3月25日</div>
    </div>

    <div class="section">
        <h2>一、全球顶尖大模型及公司动态</h2>
        
        <div class="news-item">
            <div class="news-title">Claude推出电脑操作功能，向Agent方向迈进<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 12:50</div>
            <div class="news-summary">Anthropic旗下AI助手Claude推出"Computer Use"功能，允许用户授权其直接操作电脑完成各类任务，集成在Claude Cowork和Claude Code中，通过手机Dispatch分配任务，帮助用户更高效管理工作流程，标志AI助手向更自主任务执行迈进。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032489275.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">刚刚，Anthropic发布官方龙虾</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 11:10</div>
            <div class="news-summary">Anthropic发布Claude新功能，包括电脑控制（Claude可通过手机App远程操控电脑完成导出PPT、启动开发服务器、批量处理照片等任务）、云端定时任务及Claude Code Desktop，借助手机发令实现电脑端任务处理，提升个人工作效率。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032489143.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Token的正式命名来了！</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 19:50</div>
            <div class="news-summary">Token作为大模型调用量的评估标准和计费单位，定义为大模型理解和生成语言的最小语义单元（词元），介绍其Token化过程、不同语言换算差异及在大模型应用中的计价、上下文窗口、任务执行消耗等关键角色。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032453874.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>二、中国AI大模型最新进展</h2>
        
        <div class="news-item">
            <div class="news-title">阿里云重磅上线Qoder专家团模式，AI编程进入组团作战时代</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-23 12:33</div>
            <div class="news-summary">阿里云Qoder推出专家团模式，采用多Agent协作架构解决单个AI Agent处理复杂任务的上下文瓶颈问题，实现工程化的组团作战，提升AI编程效率。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032360472.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>三、AI软硬件及国产芯片生态</h2>
        
        <div class="news-item">
            <div class="news-title">53AI Hub：跨平台的智能体发布与运营平台（开源）</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-21</div>
            <div class="news-summary">53AI Hub无缝对接字节扣子、腾讯元器、Dify、FastGPT、RAGFlow等智能体开发平台，让开发者和企业能够快速搭建生产运营级的AI门户，极大降低了AI应用落地的门槛。</div>
            <a class="news-link" href="https://hub.53ai.com" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>四、AI智能体前沿资讯</h2>
        
        <div class="news-item">
            <div class="news-title">Claude Code推出云端龙虾：/schedule命令让AI自己排班干活<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 07:04</div>
            <div class="news-summary">Claude Code推出/schedule命令，支持在云端创建定时任务，让Claude自动执行如代码同步、文档更新等任务，支持多种频率及外部服务连接，替代员工部分工作。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032450712.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code /init改版：对话式配置，自动定制专属环境</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-23 09:00</div>
            <div class="news-summary">Claude Code的/init命令改版为对话式配置，通过与用户交互提问（如项目技术栈、特殊需求等），自动定制专属环境（配置技能和钩子），提升初始化效率，降低认知负担，新手也能快速上手。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032345720.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>五、其他全球AI领域重要资讯</h2>
        
        <div class="news-item">
            <div class="news-title">上下文工程的六大支柱：压缩和编排</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 20:00</div>
            <div class="news-summary">介绍上下文工程的压缩技术，探讨信息密度挑战，阐述压缩的两种哲学（抽取式与抽象式），并介绍基于信息熵的剪枝技术Selective Context等具体方法。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032459678.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Token批发转零售的三种溢价与半衰期</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 07:03</div>
            <div class="news-summary">分析LLM商业化本质为"算力批发转零售"的价值再创造，探讨算法、数据、算力三维溢价，对比OpenAI平台流量与Claude专业信任策略，指出算力溢价的脆弱性及零售商通过"结果确定性"实现价值增厚。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032413598.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">业务逻辑的"坍塌"：当应用层只剩下胶水代码</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-24 08:45</div>
            <div class="news-summary">探讨大模型预训练成本、模型参数与结构（如W矩阵、FFN、Linear及Attention机制）对输出不确定性的影响，反思AI Agent时代应用层架构的构建，核心围绕大模型底层技术原理展开。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032441572.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="footer">
        <p>本简报由高校分队AI新闻监控系统自动生成</p>
        <p>数据来源：53AI等权威媒体</p>
        <p>搜索来源：53AI（浏览器访问）</p>
        <p>生成时间：2026年3月25日 06:20 (北京时间)</p>
    </div>
</body>
</html>"""

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    plain_text = "高校分队 AI 新闻每日简报 2026年3月25日\n\n请使用HTML格式查看完整内容。"
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        print(f"Sent to {to_email}")

subject = "[2026-03-25] 高校分队 AI 新闻每日简报"
sent_count = 0
failed = []
for to in TO_EMAILS:
    try:
        send_email(to, subject, HTML_CONTENT)
        sent_count += 1
    except Exception as e:
        print(f"Failed to send to {to}: {e}")
        failed.append(to)

print(f"\n=== Summary ===")
print(f"Total: {len(TO_EMAILS)}, Sent: {sent_count}, Failed: {len(failed)}")
if failed:
    print(f"Failed: {failed}")
