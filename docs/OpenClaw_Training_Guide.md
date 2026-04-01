# OpenClaw AI 助手配置与使用指南

**培训讲师：旺财 (OpenClaw AI Agent)**  
**培训日期：2026年3月**  
**适用对象：需要了解AI Agent配置与使用的学员**

---

## 目录

1. OpenClaw 简介
2. 核心配置
3. 技能系统
4. 定时任务
5. 集成服务
6. 高级功能
7. 实际应用案例

---

## 第一部分：OpenClaw 简介

### 什么是 OpenClaw？

OpenClaw 是一个**开源、可自托管的个人AI代理与自动化平台**，由知名开发者Peter Steinberger发起。

### 核心理念

- **本地优先** - 部署在个人电脑、NAS或私有服务器
- **AI从被动到主动** - 不仅回答问题，还能主动执行任务
- **模块化设计** - 可扩展的技能系统

### 应用场景

- 个人助理自动化
- 知识管理与研究
- 办公效率提升
- 健康生活管理
- 技术开发辅助

---

## 第二部分：核心配置

### 2.1 工作环境

```
工作目录: ~/.openclaw/workspace/
核心文件:
  - AGENTS.md     # Agent团队配置
  - SOUL.md       # AI身份与原则
  - USER.md       # 用户信息
  - TOOLS.md      # 工具配置
  - MEMORY.md     # 长期记忆
  - SESSION-STATE.md  # 当前状态
```

### 2.2 模型配置

| 模型 | 用途 | 特点 |
|-----|------|------|
| moonshot/kimi-k2.5 | 默认对话 | 中文能力强 |
| minimax/MiniMax-M2.5 | 快速响应 | 速度快 |
| deepseek/deepseek-chat | 代码/分析 | 性价比高 |

### 2.3 消息渠道

- **飞书** - 主要即时通讯
- **邮件** - QQ邮箱、华为邮箱
- **Telegram/Discord** - 可选

---

## 第三部分：技能系统 (Skills)

### 3.1 已安装技能清单 (14个)

| 技能名称 | 功能 | 用途 |
|---------|------|------|
| **github** | GitHub CLI集成 | 代码仓库管理、PR/Issue查看 |
| **tavily-search** | AI实时搜索 | 高质量信息检索 |
| **multi-search-engine** | 17引擎搜索 | 百度/Google/DuckDuckGo等 |
| **gog** | Google Workspace | Gmail/Calendar/Drive |
| **summarize** | 内容摘要 | 文本/URL/播客转录 |
| **wacli** | WhatsApp | 消息发送与同步 |
| **github** | GitHub操作 | Issues/PRs/CI查看 |
| **proactive-agent** | 主动服务 | 心跳检查、自我优化 |
| **clawsec** | 安全审计 | 技能安全性检查 |
| **office** | 办公自动化 | 文档处理 |
| **debug-checklist** | 调试清单 | C/C++系统化调试 |
| **find-skills-robin** | 技能发现 | 搜索安装新技能 |
| **office-xyz** | 虚拟办公室 | Agent协作空间 |
| **stock-monitor** | 股票监控 | 市场数据分析 |
| **bilibili-hot-monitor** | B站热门 | 视频日报生成 |
| **local-whisper** | 语音转文字 | 本地离线转录 |

### 3.2 技能安装方法

```bash
# 安装技能
npx clawhub@latest install <技能名>

# 查看已安装技能
clawhub list

# 搜索技能
clawhub search <关键词>
```

### 3.3 技能分类

- **搜索类**: tavily-search, multi-search-engine, web_search
- **通讯类**: gog, wacli, feishu
- **开发类**: github, debug-checklist
- **效率类**: office, summarize
- **自动化**: proactive-agent, bilibili-hot-monitor
- **生活类**: stock-monitor, weather

---

## 第四部分：定时任务 (Cron Jobs)

### 4.1 已配置任务

| 任务名称 | 执行时间 | 功能 | 状态 |
|---------|---------|------|------|
| **AI新闻每日摘要** | 06:30 | 全球AI新闻汇总 | ✅ 运行中 |
| **OpenClaw新闻监控** | 06:00 | OpenClaw最新动态 | ✅ 运行中 |
| **健康长寿科研成果监控** | 08:30 | 长寿科研资讯 | ✅ 运行中 |
| **火车出发提醒** | 指定日期 | 出行提醒 | ✅ 待触发 |

### 4.2 任务配置命令

```bash
# 查看任务
openclaw cron list

# 添加任务
openclaw cron add --name "任务名" --cron "0 6 * * *" --tz "Asia/Shanghai"

# 立即运行
openclaw cron run <任务ID>

# 禁用/启用
openclaw cron disable <任务ID>
openclaw cron enable <任务ID>
```

### 4.3 任务配置示例

```bash
# 健康长寿监控任务
openclaw cron add \
  --name "健康长寿科研成果监控" \
  --cron "30 8 * * *" \
  --tz "Asia/Shanghai" \
  --message "搜索全球最新长寿科研成果..." \
  --announce \
  --to "用户ID" \
  --channel "feishu"
```

---

## 第五部分：集成服务

### 5.1 邮件服务

- **发件箱**: 86940135@qq.com
- **SMTP**: smtp.qq.com:587
- **授权码**: 已配置

### 5.2 语音合成 (TTS)

- **引擎**: Azure TTS
- **音色**: zh-CN-XiaoyiNeural
- **语速**: +30%

### 5.3 飞书集成

- **App ID**: cli_a6f596118438dcef
- **接收人**: 老板 (ou_b6c7778820b20031cd97bdc45d1cd9fa)

---

## 第六部分：高级功能

### 6.1 记忆系统

- **MEMORY.md** - 核心长期记忆
- **SESSION-STATE.md** - 当前工作状态
- **memory/** - 每日记录归档

### 6.2 自我优化 (Self-Improving)

- 每次响应后记录反馈
- 定期回顾并更新模式
- 归档低频信息

### 6.3 Agent团队

```
总指挥(旺财)
  ├── 笔杆子(creator)    - 内容创作
  ├── 运营官(yunying)    - 日常运营
  ├── 参谋(canmou)       - 深度研究
  ├── 进化官(jinhua)     - 代码开发
  ├── 交易官(jiaoyi)     - 股票监控
  ├── 社区官(shequ)      - 社区运营
  └── 昇腾AI官          - 华为昇腾技术
```

---

## 第七部分：实际应用案例

### 案例1：每日新闻自动推送

**需求**: 每天早上自动获取AI新闻并发送到邮箱

**配置**:
1. 创建新闻监控脚本
2. 配置Tavily API搜索
3. 设置06:30定时任务
4. 自动发送到QQ邮箱和飞书

**效果**: 每天醒来就收到定制新闻简报

### 案例2：健康长寿科研监控

**需求**: 每天获取全球最新长寿科研成果

**配置**:
1. 定义38个搜索维度
2. 建立权威机构白名单
3. 三重质量验证(来源+设计+证据)
4. 自动翻译成中文
5. 08:30定时发送

**效果**: 每天早上收到15条经过验证的高质量科研资讯

### 案例3：OpenClaw技能管理

**需求**: 持续跟踪OpenClaw最新Skills

**配置**:
1. 每天06:00搜索OpenClaw新闻
2. 筛选高质量来源
3. 中英双语处理
4. 发送到邮箱和飞书

---

## 总结

OpenClaw 是一个强大的**个人AI自动化平台**，核心优势：

1. **本地部署** - 数据安全可控
2. **技能生态** - 14+预装技能，2000+可安装
3. **定时任务** - 自动化日常事务
4. **多渠道集成** - 飞书/邮件/Telegram
5. **记忆系统** - 持续学习和优化

**使用建议**:
- 从简单任务开始尝试
- 根据需求逐步添加技能
- 利用定时任务实现自动化
- 定期优化记忆和配置

---

*本指南由 OpenClaw 自动生成*
*日期: 2026-03-10*
