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
    <title>高校分队 AI 新闻每日简报 - 2026年3月26日</title>
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
        <div class="date">2026年3月26日</div>
    </div>

    <div class="section">
        <h2>一、全球顶尖大模型及公司动态</h2>
        
        <div class="news-item">
            <div class="news-title">Anthropic宣布Claude现已可操控用户电脑完成任务<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：新浪财经 | 发布时间：2026-03-25</div>
            <div class="news-summary">Anthropic宣布Claude现已具备电脑操控能力，用户可授权其直接操作电脑完成各类任务，这是AI智能体发展的重要里程碑，Claude正全力推进AI智能体研发，与OpenAI、谷歌展开激烈竞争。</div>
            <a class="news-link" href="https://finance.sina.com.cn/world/2026-03-25/doc-inhscnun7197388.shtml" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">OpenAI的"特洛伊木马"叩击谷歌搜索命门<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：新浪财经 | 发布时间：2026-03-25</div>
            <div class="news-summary">OpenAI推出具有革命性的搜索功能，其"特洛伊木马"战略直指谷歌核心搜索业务。AI搜索大战升级，OpenAI已要求谷歌将ChatGPT列为默认搜索引擎之一，双方竞争进入白热化阶段。</div>
            <a class="news-link" href="https://finance.sina.com.cn/roll/2026-03-25/doc-inhscxkk3819448.shtml" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">OpenAI近万人扩招：企业AI大战全面升级</div>
            <div class="news-meta">来源：新浪新闻 | 发布时间：2026-03-25</div>
            <div class="news-summary">OpenAI宣布大规模扩招计划，拟增员近万人，全面升级企业AI服务。这场企业AI大战正在全面升级，各大科技公司纷纷加大投入，竞争态势日趋激烈。</div>
            <a class="news-link" href="https://k.sina.com.cn/article_5953189932_162d6782c06703z1bi.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">谷歌Gemini 3夜袭全球，暴击GPT-5.1</div>
            <div class="news-meta">来源：36氪 | 发布时间：2026-03-25</div>
            <div class="news-summary">谷歌发布Gemini 3大模型，以强大性能夜袭全球，对OpenAI的GPT-5.1形成正面冲击。值得注意的是，OpenAI CEO奥特曼罕见对谷歌表示祝贺，业界格局正在发生微妙变化。</div>
            <a class="news-link" href="https://www.36kr.com/p/3559153267244164" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>二、中国AI大模型最新进展</h2>
        
        <div class="news-item">
            <div class="news-title">通义千问2.5大模型再升级：18万亿字符训练打造中英文AI助手</div>
            <div class="news-meta">来源：科技行者 | 发布时间：2026-03-09</div>
            <div class="news-summary">阿里巴巴发布通义千问2.5大语言模型技术报告，训练数据扩展至18万亿字符，打造强大的中英文AI助手。阿里云持续深耕大模型研发，中文性能全面赶超GPT-4 Turbo。</div>
            <a class="news-link" href="https://www.techwalker.com/2026/0309/3180557.shtml" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">百度发布文心大模型5.0正式版：2.4万亿参数全模态大模型</div>
            <div class="news-meta">来源：科技日报 | 发布时间：2026-01-24</div>
            <div class="news-summary">百度发布文心大模型5.0正式版，参数达2.4万亿，采用原生全模态统一建模技术。在40余项权威基准的综合评测中，文心5.0的语言与多模态理解能力超越Gemini等竞品。</div>
            <a class="news-link" href="https://www.stdaily.com/web/gdxw/2026-01/24/content_465754.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>三、AI软硬件及国产芯片生态</h2>
        
        <div class="news-item">
            <div class="news-title">华为发布Atlas 350：昇腾950PR加持，算力是英伟达H20的3倍<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：快科技 | 发布时间：2026-03-22</div>
            <div class="news-summary">华为发布搭载昇腾950PR处理器的AI训练推理加速卡Atlas 350，单卡算力是英伟达H20的2.87-3倍，是目前国内唯一支持FP4低精度的推理产品。华为强势挑战英伟达H20市场主导地位。</div>
            <a class="news-link" href="https://finance.sina.com.cn/tech/roll/2026-03-23/doc-inhrxmcx5535251.shtml" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">华为8192超节点全球最强：硅谷精英承认</div>
            <div class="news-meta">来源：新浪新闻 | 发布时间：2026-03-10</div>
            <div class="news-summary">华为Atlas 950超节点于2025年华为全联接大会首次亮相，最大可支持8192张昇腾950DT卡通过"灵衢"协议实现全光互联，FP8算力达8E FLOPS。硅谷精英承认，这是全球最强的AI超节点。</div>
            <a class="news-link" href="https://www.sina.cn/news/detail-5274965328003423.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>四、AI智能体前沿资讯</h2>
        
        <div class="news-item">
            <div class="news-title">Claude Code Agent Teams：多智能体开发实战指南</div>
            <div class="news-meta">来源：腾讯云 | 发布时间：2026-03-13</div>
            <div class="news-summary">Claude Code Agent Teams将单线程AI编码体验转变为协调式多智能体系统，多个独立Claude实例可相互通信、共享任务并在代码库上并行工作。这代表了开发者与AI编码助手交互方式的根本性转变。</div>
            <a class="news-link" href="https://cloud.tencent.com/developer/article/2638621" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">实战复盘：利用Claude Code从零构建个性化AI Agent系统</div>
            <div class="news-meta">来源：80aj.com | 发布时间：2026-03-20</div>
            <div class="news-summary">详细记录以Claude Code为核心从零构建个人专属AI Agent（代号"龙虾"）的实战全过程。采用DAG-based系统优化记忆管理，预示着"Vibe Coding"时代个人软件定制的未来趋势。</div>
            <a class="news-link" href="https://www.80aj.com/2026/03/20/claude-code-ai-agent-2/" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>五、其他全球AI领域重要资讯</h2>
        
        <div class="news-item">
            <div class="news-title">GPT-5.4 vs Gemini 3.1 Pro：推理与效率的终极对决</div>
            <div class="news-meta">来源：太平洋科技 | 发布时间：2026-03-19</div>
            <div class="news-summary">2026年大模型双雄并立：GPT-5.4以原生计算机使用和工具搜索重新定义智能体能力，Gemini 3.1 Pro凭并行处理能力占据效率优势。两者在不同场景各具优势，竞争格局日趋多元。</div>
            <a class="news-link" href="https://www.pconline.com.cn/ai/article/1545289.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Google DeepMind升级Gemini API：引入多工具链与上下文循环</div>
            <div class="news-meta">来源：AIBASE | 发布时间：2026-03-19</div>
            <div class="news-summary">Google DeepMind宣布Gemini API重大功能扩展，推出多工具链与"上下文循环"机制。此举旨在解决开发者调用大模型时步骤繁琐、响应迟缓的痛点，提升开发效率。</div>
            <a class="news-link" href="https://news.aibase.com/zh/news/26363" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="footer">
        <p>本简报由高校分队AI新闻监控系统自动生成</p>
        <p>搜索来源：Ollama Web Search（SerpAPI/Tavily/DuckDuckGo备选）</p>
        <p>生成时间：2026年3月26日 06:20 (北京时间)</p>
    </div>
</body>
</html>"""

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    plain_text = "高校分队 AI 新闻每日简报 2026年3月26日\n\n请使用HTML格式查看完整内容。"
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        print(f"Sent to {to_email}")

subject = "[2026-03-26] 高校分队 AI 新闻每日简报"
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
