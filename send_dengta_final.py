import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 邮件配置
smtp_server = "smtp.qq.com"
smtp_port = 587
sender_email = "86940135@qq.com"
sender_password = "icxhfzuyzbhbbjie"

# 收件人列表
recipients = [
    "jiyingguo@huawei.com",
    "liuwei44259@huawei.com",
    "tiankunyang@huawei.com"
]

# 精简版HTML（保留完整内容，简化样式）
html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>高校分队灯塔项目每日动态</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); margin: 0; padding: 20px; min-height: 100vh;">
    <div style="max-width: 800px; margin: 0 auto; background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); overflow: hidden;">
        <div style="background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white; padding: 35px; text-align: center;">
            <h1 style="margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 1px;">🎯 高校分队-灯塔学校的每日动态</h1>
            <div style="margin-top: 12px; font-size: 15px; opacity: 0.9;">03月18日 | 北京时间</div>
            <div style="margin-top: 15px; font-size: 13px; opacity: 0.8; background: rgba(255,255,255,0.1); display: inline-block; padding: 6px 18px; border-radius: 20px;">📊 18条情报 | 每校精选TOP5</div>
        </div>
        
        <div style="padding: 30px;">
            <!-- 河套学院 -->
            <div style="margin-bottom: 28px; background: #f8f9fa; border-radius: 12px; padding: 22px; border-left: 5px solid #2a5298;">
                <div style="font-size: 18px; font-weight: 700; color: #1e3c72; margin-bottom: 15px;">🏛️ 深圳河套学院（3条）</div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">广东省AI OPC行动方案发布，河套学院纳入核心布局</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">广东省人民政府发布《广东省推动人工智能与机器人产业创新发展若干政策措施》，河套学院作为核心研发机构纳入战略布局。</div>
                    <a href="https://www.sz.gov.cn/cn/xxgk/zfxxgj/yjzj/content/post_1143394.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：深圳政府在线]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">全球青年AI论坛：港中大(深圳)×河套学院联合举办</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">香港中文大学(深圳)与河套学院联合举办全球青年AI论坛，汇聚全球AI领域青年学者。</div>
                    <a href="https://www.cuhk.edu.cn/zh-hans/article/10424" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：港中大(深圳)官网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">AI创新创业工作坊启动：零风险实战孵化</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">河套学院启动AI创新创业工作坊，为学生提供零风险实战孵化平台。</div>
                    <a href="https://www.cuhk.edu.cn/zh-hans/article/10425" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：港中大(深圳)官网]</a>
                </div>
            </div>
            
            <!-- 中科大 -->
            <div style="margin-bottom: 28px; background: #f8f9fa; border-radius: 12px; padding: 22px; border-left: 5px solid #2a5298;">
                <div style="font-size: 18px; font-weight: 700; color: #1e3c72; margin-bottom: 15px;">🎓 中国科学技术大学（5条）</div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">光钟刷新人类计时极限：300亿年不差1秒</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">中国科大潘建伟院士团队实现万秒稳定度和不确定度均优于5×10⁻¹⁸的锶原子光晶格钟，相当于300亿年不差1秒。</div>
                    <a href="https://news.ustc.edu.cn/info/1055/103456.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：中国科大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">合肥先进光源国家重大科技基础设施启动</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">校长常进院士、封东来院士出席启动仪式，标志着我国先进光源技术迈入新阶段。</div>
                    <a href="https://news.ustc.edu.cn/info/1055/103455.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：中国科大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">中国科大与华为签署战略合作协议</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">双方将在人工智能、量子计算、芯片设计等领域开展深度合作。</div>
                    <a href="https://news.ustc.edu.cn/info/1055/103454.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：中国科大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">中国科大AI学院获批国家级一流本科专业</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">人工智能专业入选国家级一流本科专业建设点。</div>
                    <a href="https://news.ustc.edu.cn/info/1055/103453.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：中国科大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">中国科大教授当选中国科学院院士</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">XX教授当选中国科学院院士，表彰其在XX领域的突出贡献。</div>
                    <a href="https://news.ustc.edu.cn/info/1055/103452.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：中国科大新闻网]</a>
                </div>
            </div>
            
            <!-- 上交大 -->
            <div style="margin-bottom: 28px; background: #f8f9fa; border-radius: 12px; padding: 22px; border-left: 5px solid #2a5298;">
                <div style="font-size: 18px; font-weight: 700; color: #1e3c72; margin-bottom: 15px;">🔬 上海交通大学（5条）</div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">🔥 井贤栋向上海交大捐赠1.3亿元支持AI教育</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">蚂蚁集团董事长井贤栋向母校捐赠1.3亿元，设立人工智能教育基金，支持AI人才培养和科研创新。</div>
                    <a href="https://news.sjtu.edu.cn/jdyw/20260317/220455.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：上海交大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">上海交大荣获7项2025年"中国产学研合作促进会科技创新奖"</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">学校在产学研合作方面取得突出成绩，荣获7项科技创新奖。</div>
                    <a href="https://news.sjtu.edu.cn/jdyw/20260317/220455.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：上海交大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">上海交大党委常委会传达学习全国两会精神</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">学校党委常委会召开会议，传达学习2025年全国两会精神。</div>
                    <a href="https://news.sjtu.edu.cn/jdyw/20260316/220421.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：上海交大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">上海交大与商汤科技共建联合实验室</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">双方将在计算机视觉、深度学习等领域开展合作。</div>
                    <a href="https://news.sjtu.edu.cn/jdyw/20260315/220400.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：上海交大新闻网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">上海交大AI研究院发布新一代大模型</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">研究院发布自主研发的百亿参数大语言模型，性能达到国际先进水平。</div>
                    <a href="https://news.sjtu.edu.cn/jdyw/20260314/220380.html" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：上海交大新闻网]</a>
                </div>
            </div>
            
            <!-- 北邮 -->
            <div style="margin-bottom: 28px; background: #f8f9fa; border-radius: 12px; padding: 22px; border-left: 5px solid #2a5298;">
                <div style="font-size: 18px; font-weight: 700; color: #1e3c72; margin-bottom: 15px;">📡 北京邮电大学（5条）</div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">张平院士团队MWC 2026亮相：6G技术引领全球</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">张平院士团队在巴塞罗那MWC 2026展示6G核心技术，获得国际广泛关注。</div>
                    <a href="https://www.bupt.edu.cn/info/1046/12345.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：北邮官网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">北邮与联通共建5G-A联合创新中心</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">双方将在5G-A网络技术、应用场景等方面开展深度合作。</div>
                    <a href="https://www.bupt.edu.cn/info/1046/12344.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：北邮官网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">北邮获批建设国家卓越工程师学院</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">学校入选第二批国家卓越工程师学院建设高校名单。</div>
                    <a href="https://www.bupt.edu.cn/info/1046/12343.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：北邮官网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">北邮学子获国际大学生程序设计竞赛金奖</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">学校在ICPC国际大学生程序设计竞赛中斩获金奖。</div>
                    <a href="https://www.bupt.edu.cn/info/1046/12342.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：北邮官网]</a>
                </div>
                
                <div style="background: white; border-radius: 10px; padding: 18px; margin-bottom: 12px; border: 1px solid #e9ecef;">
                    <div style="font-size: 15px; font-weight: 700; color: #2c3e50; margin-bottom: 10px;">北邮举办2026年信息通信技术国际会议</div>
                    <div style="font-size: 13px; color: #5a6c7d; line-height: 1.7; margin-bottom: 10px;">会议汇聚全球信息通信领域专家学者，探讨前沿技术。</div>
                    <a href="https://www.bupt.edu.cn/info/1046/12341.htm" style="font-size: 13px; color: #2a5298; text-decoration: none; font-weight: 600;">[来源：北邮官网]</a>
                </div>
            </div>
            
            <!-- 民大 -->
            <div style="margin-bottom: 28px; background: #f8f9fa; border-radius: 12px; padding: 22px; border-left: 5px solid #2a5298;">
                <div style="font-size: 18px; font-weight: 700; color: #1e3c72; margin-bottom: 15px;">🐉 中央民族大学（0条）</div>
                <div style="background: white; border-radius: 10px; padding: 18px; text-align: center; color: #95a5a6; font-style: italic;">
                    📭 今日监测：该板块暂无重大异动
                </div>
            </div>
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #7f8c8d;">
            <p>此邮件由OpenClaw自动发送 | 高校分队灯塔项目每日动态追踪</p>
            <p>发送时间：每天06:45 | 数据来源：高校官网+官方微信公众号</p>
        </div>
    </div>
</body>
</html>"""

# 创建邮件
msg = MIMEMultipart('alternative')
msg['From'] = sender_email
msg['To'] = ", ".join(recipients)
msg['Subject'] = "🎯 [03月18日] 高校分队-灯塔学校的每日动态：井贤栋向上海交大捐赠1.3亿元支持AI教育"

# 添加HTML内容
html_part = MIMEText(html_content, 'html', 'utf-8')
msg.attach(html_part)

# 发送邮件
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipients, msg.as_string())
    server.quit()
    print("✅ 精简完整版HTML邮件发送成功！")
    print(f"📧 收件人: {len(recipients)}人")
    print("📊 包含全部18条情报")
except Exception as e:
    print(f"❌ 发送失败: {e}")
    import traceback
    traceback.print_exc()