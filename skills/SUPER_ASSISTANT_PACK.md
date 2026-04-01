# 💼 超级助理技能包

## 概述
你的全能私人助理——邮件、日程、搜索、文档，动动嘴就搞定。

## 包含技能（6个）

### ✅ 已配置技能

| 技能 | 状态 | 功能 | 使用方法 |
|------|------|------|----------|
| 📧 邮件管理 | ✅ 已配置 | QQ邮箱管理、收发邮件 | `python3 skills/email-manager/email_manager.py <命令>` |
| 📅 飞书日历 | ✅ 已配置 | 日程查询、创建事件 | `python3 skills/feishu-calendar/feishu_calendar.py <命令>` |
| 📝 飞书文档 | ✅ 已就绪 | 读写飞书文档 | 使用feishu_doc工具 |
| 🔍 网页搜索 | ✅ 已配置 | Tavily AI搜索（主）+ DuckDuckGo（备） | `bash skills/tavily-search/search.sh "关键词"` |
| 🌤️ 天气查询 | ✅ 已就绪 | 实时天气查询 | 使用weather工具 |
| 🧠 基础智能包 | ✅ 已就绪 | 搜索、翻译、计算 | 内置能力 |

## 快速使用指南

### 邮件管理
```bash
# 检查未读邮件
python3 skills/email-manager/email_manager.py unread qq

# 列出最近10封邮件
python3 skills/email-manager/email_manager.py list qq 10

# 发送邮件
python3 skills/email-manager/email_manager.py send "收件人邮箱" "主题" "正文"
```

### 飞书日历
```bash
# 查看今天日程
python3 skills/feishu-calendar/feishu_calendar.py today

# 列出最近日程
python3 skills/feishu-calendar/feishu_calendar.py list

# 创建事件
python3 skills/feishu-calendar/feishu_calendar.py create "会议标题" "2026-03-07T15:00:00" "2026-03-07T16:00:00" "描述"
```

### 网页搜索
```bash
# 搜索关键词
python3 skills/duckduckgo-search/duckduckgo_search.py "OpenClaw 最新版本"
```

## 自然语言指令

可以直接对我说：

### 邮件相关
- "检查未读邮件"
- "列出最近邮件"
- "发送邮件给xxx"

### 日历相关
- "今天有什么会"
- "明天下午有什么安排"
- "帮我创建一个会议"

### 搜索相关
- "搜索今天的AI新闻"
- "找Docker入门教程"
- "查技术方案最佳实践"

### 天气相关
- "北京今天天气怎么样"
- "明天会下雨吗"

## 待完善配置

### 华为邮箱
- 需要华为邮箱密码/授权码
- IMAP服务器地址待确认

### Brave Search API Key
- 可选配置，可获得更稳定的搜索结果
- 获取地址: https://api.search.brave.com/app/keys

## 技能文档

- [邮件管理技能](skills/email-manager/SKILL.md)
- [飞书日历技能](skills/feishu-calendar/SKILL.md)
- [网页搜索技能](skills/duckduckgo-search/SKILL.md)

## 更新日志

- 2026-03-07: 超级助理技能包初始配置完成
  - ✅ 邮件管理（QQ邮箱）
  - ✅ 飞书日历
  - ✅ 网页搜索（DuckDuckGo）
  - ✅ 飞书文档（内置）
  - ✅ 天气查询（内置）
  - ✅ 基础智能包（内置）
