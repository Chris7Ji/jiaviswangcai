# TOOLS.md - 本地配置

## 核心配置

### 图片识别（默认模型）
- 模型: minimax-portal/MiniMax-M2.7-highspeed
- 配置文件: agents.defaults.imageModel

### TTS语音（必须用Azure TTS）
- 音色: zh-CN-XiaoyiNeural, 语速+30%
- 终结点: https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1

### 邮件配置（全局）
- 发件: 86940135@qq.com, 授权码: icxhfzuyzbhbbjie
- SMTP: smtp.qq.com:587
- 收件默认: 86940135@qq.com, jiyingguo@huawei.com

### 飞书
- App ID: cli_a6f596118438dcef
- 接收人Open ID: ou_b6c7778820b20031cd97bdc45d1cd9fa

### 搜索API（全局）
- **SerpAPI**: b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f（2026-03-20新增，主力搜索）
- Tavily API: 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（备用，配额有限）

### 常用路径
- Workspace: /Users/jiyingguo/.openclaw/workspace/
- 语音缓存: /tmp/jarvis_voice_cache/
- 新闻摘要: /Users/jiyingguo/.openclaw/workspace/news_summaries/

## 搜索技能
| 引擎 | 用途 | 命令 |
|------|------|------|
| Tavily | 深度研究 | ./skills/search.sh "关键词" tavily |
| Multi | 多源快速 | ./skills/search.sh "关键词" multi |
| DuckDuckGo | 隐私搜索 | ./skills/search.sh "关键词" duckduckgo |

## 核心技能
| 技能 | 用途 |
|------|------|
| summarize | 视频/网页/PDF摘要 |
| daily-report | 日报生成 |
| stock-monitor | 股票监控 |
| bilibili-monitor | B站热门监控 |

## 邮件发送
```python
# 使用QQ邮箱授权码发送
python3 skills/email-manager/email_manager.py send "收件人" "主题" "正文"
```

## 飞书日历
```python
python3 skills/feishu-calendar/feishu_calendar.py list|today|create
```

## 安全监控
- ClawSec: 已启用，自动启动
- 监控日志: /tmp/clawsec/

## 技能安装
```bash
clawhub search <关键词>  # 搜索
clawhub install <技能名>  # 安装
```
