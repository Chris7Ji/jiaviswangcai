import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
EMAIL = "86940135@qq.com"
PASSWORD = "icxhfzuyzbhbbjie"

FAILED_EMAILS = [
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
    <title>高校分队 AI 新闻每日简报 - 2026年3月27日晚间版</title>
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
        .note { background-color: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 20px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>高校分队 AI 新闻每日简报</h1>
        <div class="date">2026年3月27日晚间版</div>
    </div>
    
    <div class="note">
        <strong>说明：</strong>本简报为晚间补充版，新闻来源与上午版相同（53ai.com 3月26-27日更新）。
    </div>

    <div class="section">
        <h2>一、全球顶尖大模型及公司动态</h2>
        
        <div class="news-item">
            <div class="news-title">林俊旸离职后首次发声！复盘千问的弯路，指出AI的新路<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 04:21</div>
            <div class="news-summary">林俊旸离职阿里千问后首次发声，复盘千问合并thinking与instruct模式的弯路，指出AI未来方向为从推理模型转向智能体式思维，强调需在思考与行动间切换、动态规划工具调用等。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032704173.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">GitHub悄悄改了规则，你的代码可能正在被拿去训练AI<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:23</div>
            <div class="news-summary">GitHub宣布自2026年4月24日起，Copilot Free、Pro和Pro+个人及小团队用户的交互数据默认用于训练AI模型。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032683497.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Harness is the New Dataset：模型智能提升的下一个关键方向</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:17</div>
            <div class="news-summary">harness engineering成为继prompt engineering、context engineering之后的新热点，被视为模型智能提升的关键方向。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032668704.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Google亲手证明：GUI已死，但尸体还在动</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:10</div>
            <div class="news-summary">Google DeepMind推出的浏览器可借助Gemini 3.1 Flash-Lite实时生成网站，挑战传统GUI模式。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032697524.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>二、AI智能体前沿资讯</h2>
        
        <div class="news-item">
            <div class="news-title">Claude Code太烧钱了？5招把token成本砍了一半！</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 19:23</div>
            <div class="news-summary">Claude Code使用成本高，作者分享5招降低token成本：切换模型、控制上下文、优化规则与技能使用等。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032649736.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Anthropic官方复盘Claude Code：智能体系统设计的四个核心</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 15:31</div>
            <div class="news-summary">Anthropic复盘Claude Code开发中智能体系统设计的核心，为AI智能体开发提供官方最佳实践参考。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032674031.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code auto mode解析：如何用AI分类器替代人工审批<span class="badge-hot">重要</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 13:22</div>
            <div class="news-summary">Claude Code推出auto mode，通过AI分类器替代人工审批，解决安全审批疲劳及操作越界问题。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032638276.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>三、AI软硬件及算法突破</h2>
        
        <div class="news-item">
            <div class="news-title">Google极限压缩算法：内存砍6倍，速度快8倍<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 12:30</div>
            <div class="news-summary">Google Research发布TurboQuant压缩算法，将内存占用降6倍、推理速度提升8倍且精度无损失。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032634675.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude团队祭出"自动模式"！里程碑式进化</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 07:50</div>
            <div class="news-summary">Claude Code"自动模式"可自动处理文件写入、bash命令等编程任务，是里程碑式能力进化。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032626971.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>四、中国AI大模型最新进展</h2>
        
        <div class="news-item">
            <div class="news-title">林俊旸复盘千问弯路：AI的新方向是智能体式思维</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 04:21</div>
            <div class="news-summary">前阿里千问核心成员林俊旸指出AI未来方向：从推理模型转向智能体式思维。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032704173.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>五、其他全球AI领域重要资讯</h2>
        
        <div class="news-item">
            <div class="news-title">拒绝"感觉有效"：用数据证明AI Coding的真实团队价值</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-25 16:29</div>
            <div class="news-summary">天猫团队构建三层AI Coding度量体系，用数据证明AI Coding的团队价值。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032534015.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="footer">
        <p>本简报由高校分队AI新闻监控系统自动生成</p>
        <p>新闻来源：53ai.com/news/LargeLanguageModel</p>
        <p>生成时间：2026年3月27日 21:25 (北京时间)</p>
    </div>
</body>
</html>"""

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    plain_text = "高校分队 AI 新闻每日简报 2026年3月27日晚间版\n\n请使用HTML格式查看完整内容。"
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        print(f"Sent to {to_email}")

subject = "[2026-03-27晚] 高校分队 AI 新闻每日简报"
sent_count = 0
failed = []
for to in FAILED_EMAILS:
    try:
        send_email(to, subject, HTML_CONTENT)
        sent_count += 1
    except Exception as e:
        print(f"Failed to send to {to}: {e}")
        failed.append(to)

print(f"\n=== Retry Summary ===")
print(f"Total: {len(FAILED_EMAILS)}, Sent: {sent_count}, Failed: {len(failed)}")
if failed:
    print(f"Failed: {failed}")
