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
    <title>高校分队 AI 新闻每日简报 - 2026年3月28日晚间版</title>
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
        <div class="date">2026年3月28日晚间版</div>
    </div>

    <div class="section">
        <h2>一、全球顶尖大模型及公司动态</h2>
        
        <div class="news-item">
            <div class="news-title">最强Claude意外泄露！代号「卡皮巴拉」，完胜Opus 4.6<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-28 05:13</div>
            <div class="news-summary">Anthropic意外泄露新模型Claude Mythos（代号卡皮巴拉），性能远超现有最强模型Opus 4.6，在多领域实现显著提升，属于闭源大模型的技术突破。奥特曼又要睡不着了！</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032874528.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Harness：AI从"能做"到"稳做"的系统层革命<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-28 12:10</div>
            <div class="news-summary">Harness聚焦AI落地核心痛点，通过构建系统架构约束AI行为，而非纯文本规则，实现从"能做"到"稳做"的系统层革命，验证了其在智能合约开发等场景的稳定执行价值。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032845613.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">林俊旸离职后首次发声！复盘千问的弯路，指出AI的新路</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 04:21</div>
            <div class="news-summary">林俊旸离职阿里千问后首次发声，复盘千问合并thinking与instruct模式的弯路，指出AI未来方向为从推理模型转向智能体式思维，强调需在思考与行动间切换。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032704173.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">GitHub悄悄改了规则，你的代码可能正在被拿去训练AI</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:23</div>
            <div class="news-summary">GitHub宣布自2026年4月24日起，Copilot Free、Pro和Pro+个人及小团队用户的交互数据默认用于训练AI模型。老用户若曾设置不允许收集则不受影响。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032683497.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>二、AI智能体前沿资讯</h2>
        
        <div class="news-item">
            <div class="news-title">Claude Code开启团战模式！Agent Teams必须用起来<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-28 07:58</div>
            <div class="news-summary">Claude Code推出Agent Teams功能，为Sub Agents的超级加强版，可协调多个Claude Code实例协作完成复杂任务，包括启动条件、适用场景及与子代理的对比。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032823049.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Tair短期记忆架构实践：淘宝闪购AI Agent的秒级响应</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 18:20</div>
            <div class="news-summary">介绍淘宝闪购与千问合作项目中，Tair作为AI Agent短期记忆层的核心技术实践，包括数据模型设计、压缩策略及并发控制等，支持AI Agent的秒级响应。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032762573.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code太烧钱了？5招把token成本砍了一半！</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 19:23</div>
            <div class="news-summary">Claude Code使用成本高，作者分享5招降低token成本：切换模型、控制上下文在60%以下、优化规则与技能使用、用依赖图工具减少文件读取等，实测节省一半token。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032649736.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Anthropic官方复盘Claude Code：智能体系统设计的四个核心</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 15:31</div>
            <div class="news-summary">Anthropic复盘Claude Code开发中智能体系统设计的核心，重点探讨工具设计的重要性及相关尝试，为AI智能体开发提供官方最佳实践参考。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032674031.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>三、AI软硬件及国产芯片生态</h2>
        
        <div class="news-item">
            <div class="news-title">Harness is the New Dataset：模型智能提升的下一个关键方向</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:17</div>
            <div class="news-summary">harness engineering成为继prompt engineering、context engineering之后的新热点，被视为模型智能提升的关键方向。DeepMind等团队已开始实践。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032668704.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Google亲手证明：GUI已死，但尸体还在动</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 20:10</div>
            <div class="news-summary">Google DeepMind推出的浏览器可借助Gemini 3.1 Flash-Lite实时生成网站，展示了大模型在实时响应与代码生成上的能力，挑战传统GUI模式。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032697524.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Google极限压缩算法：内存砍6倍，速度快8倍</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 12:30</div>
            <div class="news-summary">Google Research发布TurboQuant压缩算法，将内存占用降6倍、推理速度提升8倍且精度无损失，优化大模型本地部署显存压力。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032634675.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>四、中国AI大模型最新进展</h2>
        
        <div class="news-item">
            <div class="news-title">淘宝闪购AI Agent实践：Tair短期记忆架构</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 18:20</div>
            <div class="news-summary">淘宝闪购与千问合作项目中，Tair作为AI Agent短期记忆层的核心技术实践，支持AI Agent的秒级响应及多轮对话中的记忆管理。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032762573.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">林俊旸复盘千问弯路：AI的新方向是智能体式思维</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27 04:21</div>
            <div class="news-summary">前阿里千问核心成员林俊旸指出AI未来方向：从推理模型转向智能体式思维，认为未来竞争力来自环境设计、harness工程及系统训练。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032704173.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>五、其他全球AI领域重要资讯</h2>
        
        <div class="news-item">
            <div class="news-title">治愈Cursor AI编程的"幻觉"？规格驱动开发来帮忙</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 17:56</div>
            <div class="news-summary">天玑前端团队通过规格驱动开发（SDD）结合OpenSpec、Spec Kit、BMAD等工具，自研适配Cursor的AI研发流（Specflow），解决大模型生成代码的"幻觉"问题。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032672386.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code auto mode：AI分类器替代人工审批</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-26 13:22</div>
            <div class="news-summary">Claude Code推出auto mode，通过AI分类器替代人工审批，解决安全审批疲劳及操作越界问题，是Claude的里程碑式能力进化。</div>
            <a class="news-link" href="https://www.53ai.com/news/LargeLanguageModel/2026032638276.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="footer">
        <p>本简报由高校分队AI新闻监控系统自动生成</p>
        <p>新闻来源：53ai.com/news/LargeLanguageModel（浏览器获取）</p>
        <p>生成时间：2026年3月28日 22:20 (北京时间)</p>
    </div>
</body>
</html>"""

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    plain_text = "高校分队 AI 新闻每日简报 2026年3月28日晚间版\n\n请使用HTML格式查看完整内容。"
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        print(f"Sent to {to_email}")

subject = "[2026-03-28晚] 高校分队 AI 新闻每日简报"
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
