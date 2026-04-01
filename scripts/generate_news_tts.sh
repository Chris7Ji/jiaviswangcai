#!/bin/bash
# 使用macOS本地TTS生成语音

# 新闻内容
NEWS1="近期，开源AI智能体龙虾持续走热，引发广泛讨论。所谓龙虾，是开源AI智能体OpenClaw的别称，因其图标是红色的龙虾而得名。龙虾智能体通过整合调用通信软件和大语言模型，在用户本地电脑自主执行文件管理、邮件收发、数据处理等复杂任务。专家建议用户在使用龙虾等AI智能体过程中，要把安全底线把握在自己手中，详细了解并落实安全配置规范要求，养成安全使用习惯。"

NEWS2="三月十三日晚，海尔以一场主题为科技进化爱的回响的AI科技全场景发布会，向全球用户展示了智慧生活的进化方向。海尔集团董事局主席、首席执行官周云杰作为主发布人亮相。周云杰表示，自己开通账号，不是为了打造人设，而是以真诚为底色，架起一座与用户深度交互的桥。截至二零二五年底，周云杰个人账号已经收到了超过九千条关于产品研发的建议，其中十七条建议已转化为正式的产品立项。本次发布会展示了AI之眼二点零技术，搭载AI之眼二点零系列家电已经达到L四智能等级，为目前行业最高智能级别。"

NEWS3="擎朗智能创始人兼CEO李通表示，机器人终局是走入千家万户，成为能洗衣、做饭、带孩子的机器人保姆。李通认为，未来必然是通用机器人与专用机器人混合共生的格局，二者并非相互替代，而是各展所长、协同协作。在擎朗的岗位化布局中，机器人并非追求一站式全能，而是先成为某一领域的专业选手。只有让机器人在一个个具体岗位中完成从技术到落地的验证，积累足够多的真实场景数据，再将这些单一岗位的能力综合起来，最终才能打造出走入家庭的全能机器人保姆。"

# 输出目录
OUTPUT_DIR="/tmp/tts_news"
mkdir -p "$OUTPUT_DIR"

# 生成语音文件
echo "正在生成第一条新闻语音..."
say -v Ting-Ting "$NEWS1" -o "$OUTPUT_DIR/news1.aiff"
ffmpeg -i "$OUTPUT_DIR/news1.aiff" -ar 44100 -ac 1 "$OUTPUT_DIR/news1.mp3" -y 2>/dev/null

echo "正在生成第二条新闻语音..."
say -v Ting-Ting "$NEWS2" -o "$OUTPUT_DIR/news2.aiff"
ffmpeg -i "$OUTPUT_DIR/news2.aiff" -ar 44100 -ac 1 "$OUTPUT_DIR/news2.mp3" -y 2>/dev/null

echo "正在生成第三条新闻语音..."
say -v Ting-Ting "$NEWS3" -o "$OUTPUT_DIR/news3.aiff"
ffmpeg -i "$OUTPUT_DIR/news3.aiff" -ar 44100 -ac 1 "$OUTPUT_DIR/news3.mp3" -y 2>/dev/null

# 清理临时文件
rm -f "$OUTPUT_DIR"/*.aiff

echo "语音生成完成！"
echo "文件位置:"
echo "  - $OUTPUT_DIR/news1.mp3"
echo "  - $OUTPUT_DIR/news2.mp3"
echo "  - $OUTPUT_DIR/news3.mp3"
