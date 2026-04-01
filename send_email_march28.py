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
    <title>高校分队 AI 新闻每日简报 - 2026年3月28日</title>
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
        <div class="date">2026年3月28日</div>
    </div>

    <div class="section">
        <h2>一、全球顶尖大模型及公司动态</h2>
        
        <div class="news-item">
            <div class="news-title">Claude Opus 4.6 vs GPT-5.4 vs Gemini 3.1 Pro：旗舰大模型终极横评<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：Claude官网中文版 | 发布时间：2026-03-23</div>
            <div class="news-summary">2026年3月旗舰大模型横评发布，数据来源包括SWE-bench、ARC-AGI-2、GPQA Diamond、Chatbot Arena等权威基准测试。Claude Opus 4.6与GPT-5.4、Gemini 3.1 Pro三大旗舰模型全面对比，为开发者选型提供参考。</div>
            <a class="news-link" href="https://www.claude-anthropic.com/model-comparison/137.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">GPT-5.4、Claude、Gemini三方混战：AI Agent native能力终极PK</div>
            <div class="news-meta">来源：53AI | 发布时间：2026-03-27</div>
            <div class="news-summary">三大模型在AI Agent native能力方面展开终极PK，GPT-5.4、Claude、Gemini各自展现其在智能体领域的独特优势与差异化能力。</div>
            <a class="news-link" href="http://www.53ai.com/news/LargeLanguageModel/2026030863209.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">OpenAI计划年底扩招至8000人，缩小与Anthropic差距</div>
            <div class="news-meta">来源：Financial Times | 发布时间：2026-03-24</div>
            <div class="news-summary">OpenAI宣布计划在2026年底前将员工规模扩招至8000人，以缩小与竞争对手Anthropic的差距。这场AI人才争夺战正在全面升级。</div>
            <a class="news-link" href="https://hk.marketscreener.com/news/openai-plans-to-increase-staff-to-8-000-by-end-of-2026-in-bid-to-close-gap-with-rival-anthropic-ft-ce7e5edcd889f520" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">微软、英伟达和Anthropic宣布结盟</div>
            <div class="news-meta">来源：锐潮新途 | 发布时间：2026-03-24</div>
            <div class="news-summary">微软、英伟达和Anthropic宣布建立新的战略合作伙伴关系，Anthropic正在微软Azure上快速增加Claude部署，三方联手打造AI新生态。</div>
            <a class="news-link" href="http://www.iroqo47.cn/news/50d1199938.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>二、中国AI大模型最新进展</h2>
        
        <div class="news-item">
            <div class="news-title">深入解析阿里通义千问系列：从开源先锋到全球第一</div>
            <div class="news-meta">来源：三郎君的日常 | 发布时间：2026-03-13</div>
            <div class="news-summary">2026年2月16日，阿里发布Qwen3.5系列，首发模型Qwen3.5-397B-A17B——全参数3970亿、激活参数仅170亿的原生多模态大语言模型。通义千问从追随者变成领跑者。</div>
            <a class="news-link" href="https://sanlangcode.com/index.php/2026/03/13/%E6%B7%B1%E5%85%A5%E8%A7%A3%E6%9E%90%E9%98%BF%E9%87%8C%E9%80%9A%E4%B9%89%E5%8D%83%E9%97%AE%EF%BC%88qwen%EF%BC%89%E7%B3%BB%E5%88%97%E6%A8%A1%E5%9E%8B%EF%BC%9A%E4%BB%8E%E5%BC%80%E6%BA%90%E5%85%88-2/" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">2026年全网最全大模型API横评：20+主流模型八大厂商对比</div>
            <div class="news-meta">来源：七牛云 | 发布时间：2026-03</div>
            <div class="news-summary">2026年全网最全大模型API横评发布，涵盖Claude、GPT、Gemini等八大厂商20+主流模型，从性能、价格、易用性等多维度进行对比评测。</div>
            <a class="news-link" href="https://news.qiniu.com/archives/1774508972073" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">文心一言4.5大模型深度评测：突破与惊喜并存</div>
            <div class="news-meta">来源：新浪新闻 | 发布时间：2026-03</div>
            <div class="news-summary">文心一言4.5大模型深度评测发布，在注意力机制、代码能力、推理能力等方面展现突破性进展，为国产大模型发展提供重要参考。</div>
            <a class="news-link" href="https://k.sina.com.cn/article_7879848900_1d5acf3c401902rynm.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>三、AI软硬件及国产芯片生态</h2>
        
        <div class="news-item">
            <div class="news-title">华为Atlas 350发布：昇腾950PR算力是H20的2.87倍<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：新浪财经 | 发布时间：2026-03-21</div>
            <div class="news-summary">华为发布搭载昇腾950PR处理器的AI训练推理加速卡Atlas 350，单卡算力是英伟达H20的2.87倍，为目前国内唯一支持FP4低精度推理的产品。</div>
            <a class="news-link" href="https://finance.sina.com.cn/wm/2026-03-21/doc-inhrukzr5712241.shtml" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">昇腾人工智能伙伴峰会2026圆满举办</div>
            <div class="news-meta">来源：新浪新闻 | 发布时间：2026-03-23</div>
            <div class="news-summary">昇腾人工智能伙伴峰会2026在深圳举办，联合20家行业伙伴推出2026昇腾AI应用场景解决方案，7大伙伴基于Atlas 350的整机产品亮相。</div>
            <a class="news-link" href="https://news.sina.cn/sx/2026-03-23/detail-inhrynrt4102805.d.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">华为昇腾AI生态蓬勃发展：开发者超400万，合作伙伴突破3000家</div>
            <div class="news-meta">来源：新浪新闻 | 发布时间：2026-03-23</div>
            <div class="news-summary">华为昇腾AI生态持续壮大，开发者数量已超400万，合作伙伴突破3000家。徐直军表示芯片规划持续推进，昇腾生态蓬勃发展。</div>
            <a class="news-link" href="https://k.sina.com.cn/article_7879848900_1d5acf3c401902rr6m.html" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>四、AI智能体前沿资讯</h2>
        
        <div class="news-item">
            <div class="news-title">Claude推出电脑操作功能，向Agent方向迈出重要一步<span class="badge-new">今日重大</span></div>
            <div class="news-meta">来源：腾讯新闻 | 发布时间：2026-03-24</div>
            <div class="news-summary">Anthropic旗下Claude推出"Computer Use"功能，允许用户授权其直接操作电脑完成各类任务。这标志着AI助手从单纯指令响应向更自主任务执行迈出重要一步。</div>
            <a class="news-link" href="https://news.qq.com/rain/a/20260324A03PPH00" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code Auto Mode重磅上线：AI终于"自己开车"<span class="badge-hot">今日重要</span></div>
            <div class="news-meta">来源：AIBASE | 发布时间：2026-03-25</div>
            <div class="news-summary">Claude Code正式推出Auto Mode模式，AI能够自主判断代码操作安全性：安全操作直接执行，存在风险的操作则自动拦截并询问用户。这是编程辅助的重大突破。</div>
            <a class="news-link" href="https://news.aibase.com/zh/news/26548" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code进化：越来越像openclaw等通用Agent靠拢</div>
            <div class="news-meta">来源：CN-SEC 中文网 | 发布时间：2026-03-16</div>
            <div class="news-summary">Claude Code一周发布5个版本，新增MCP交互、工作流自动化等功能。Anthropic投入1亿美元扩展Claude合作伙伴生态并成立独立安全研究机构。</div>
            <a class="news-link" href="https://cn-sec.com/archives/5099343.html" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">Claude Code Agent Teams：多智能体协作开发完整指南</div>
            <div class="news-meta">来源：AI Free API | 发布时间：2026-03</div>
            <div class="news-summary">Claude Code Agent Teams将单线程体验转变为协调式多智能体系统，多个独立Claude实例可相互通信、共享任务并在代码库上并行工作。</div>
            <a class="news-link" href="https://www.aifreeapi.com/zh/posts/claude-code-agent-teams" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="section">
        <h2>五、其他全球AI领域重要资讯</h2>
        
        <div class="news-item">
            <div class="news-title">微软2026财季报告：AI战略成效显著</div>
            <div class="news-meta">来源：新浪财经 | 发布时间：2026-03</div>
            <div class="news-summary">微软2026财季报告显示AI战略成效显著，OpenAI与Anthropic贡献巨大回报。微软与OpenAI的合作伙伴关系持续深化。</div>
            <a class="news-link" href="https://cj.sina.cn/articles/view/7879848900/1d5acf3c401902v0u8" target="_blank">查看原文</a>
        </div>
        
        <div class="news-item">
            <div class="news-title">OpenAI与微软联合声明：深化合作伙伴关系</div>
            <div class="news-meta">来源：OpenAI官网 | 发布时间：2026-02-27</div>
            <div class="news-summary">OpenAI与微软发布联合声明，自2019年以来的合作伙伴关系已演变为科技界最具影响力的协作范例之一，双方持续深化技术融合与创新合作。</div>
            <a class="news-link" href="https://openai.com/zh-Hans-CN/index/continuing-microsoft-partnership/" target="_blank">查看原文</a>
        </div>
    </div>

    <div class="footer">
        <p>本简报由高校分队AI新闻监控系统自动生成</p>
        <p>搜索来源：SerpAPI + 53ai.com</p>
        <p>生成时间：2026年3月28日 09:20 (北京时间)</p>
    </div>
</body>
</html>"""

def send_email(to_email, subject, html_body):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    plain_text = "高校分队 AI 新闻每日简报 2026年3月28日\n\n请使用HTML格式查看完整内容。"
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to_email], msg.as_string())
        print(f"Sent to {to_email}")

subject = "[2026-03-28] 高校分队 AI 新闻每日简报"
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
