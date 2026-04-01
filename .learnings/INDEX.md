# 记忆关键词索引
# 用途: 快速定位相关信息，避免依赖慢速的memory_search
# 更新频率: 每周回顾时更新
# 创建时间: 2026-03-10

## 🔴 核心身份与关系 (HOT - 每次加载)
- **老板身份**: SOUL.md#L28 - 季是我的老板，我是他的AI助理旺财
- **工作原则**: SOUL.md#L30 - 听从安排、尽全力完成、多想办法解决
- **核心性格**: SOUL.md#L7 - 真诚帮助、有主见、先尝试再询问

## 🛠️ 工具配置 (WARM - 常用)
### 邮件系统
- **QQ邮箱配置**: TOOLS.md#L20 - 86940135@qq.com, 授权码: swqfjvmoupdebhgh
- **邮件发送脚本**: 
  - AI新闻: news_summaries/send_email.py
  - 健康报告: send_health_email.py
- **收件人**: 86940135@qq.com, jiyingguo@huawei.com

### 定时任务
- **任务配置**: cron/jobs.json
- **AI新闻**: 每天06:30, ID: 0bd3de5c-a4f9-4774-9511-75f344ba114c
- **OpenClaw新闻**: 每天06:00, ID: 5aa186d0-d623-41aa-bef3-352aec56eb20
- **健康监控**: 每天08:30, ID: 784cee35-e004-40b4-a44a-a5102a930b7e
- **任务状态检查**: HEARTBEAT.md

### 搜索工具
- **Tavily搜索**: skills/tavily-search/search.sh - AI优化搜索
- **多搜索引擎**: skills/multi-search-engine - 17个引擎聚合
- **API密钥位置**: ~/.openclaw/workspace/tavily_api_key.txt

### 大模型配置
- **当前默认**: moonshot/kimi-k2.5
- **备选模型**: deepseek/deepseek-chat, minimax-cn/MiniMax-M2.5
- **配置位置**: openclaw.json

## 👥 Agent团队 (WARM - 任务派发)
- **总指挥(main)**: 我，默认模型kimi-k2.5
- **笔杆子(creator)**: 内容创作
- **运营官(yunying)**: 日常运营
- **参谋(canmou)**: 深度研究
- **进化官(jinhua)**: 代码开发
- **交易官(jiaoyi)**: 股票监控
- **社区官(shequ)**: 社区运营
- **昇腾AI官(ascend_ai_officer)**: 华为昇腾技术
- **配置**: AGENTS.md

## 📝 重要学习记录 (按主题分类)

### 邮件相关
- **LEARNINGS.md#learn-001**: OpenClaw gateway restart不需要sudo权限
- **健康报告邮件**: 2026-03-10配置完成，使用QQ邮箱

### 模型切换
- **2026-03-10**: 全部模型切换为kimi-k2.5
- **之前**: minimax-cn/MiniMax-M2.5 → deepseek/deepseek-chat → kimi-k2.5

### 技能安装
- **2026-03-10**: 安装Self-Improving Agent和systematic-debugging
- **已有技能**: 15个核心技能已安装

### 记忆系统优化
- **2026-03-10**: 建立三层记忆体系
- **归档策略**: 每周回顾、每月归档、每季审查

## 📂 常用路径速查

### 工作目录
- **Workspace**: ~/.openclaw/workspace/
- **新闻摘要**: ~/.openclaw/workspace/news_summaries/
- **学习记录**: ~/.openclaw/workspace/.learnings/
- **技能目录**: ~/.openclaw/workspace/skills/

### 配置文件
- **OpenClaw主配置**: ~/.openclaw/openclaw.json
- **定时任务**: ~/.openclaw/cron/jobs.json
- **核心记忆**: ~/.openclaw/workspace/MEMORY.md

### 脚本文件
- **AI新闻邮件**: news_summaries/auto_send_email.sh
- **健康报告邮件**: send_health_email.sh
- **自动归档**: .learnings/archive/auto_archive.sh

## 🎯 快速决策参考

### 何时使用直接读取 vs memory_search
| 场景 | 推荐方式 | 原因 |
|------|---------|------|
| 找老板身份/偏好 | 直接读SOUL.md | 快速可靠 |
| 找工具配置 | 直接读TOOLS.md | 快速可靠 |
| 找Agent配置 | 直接读AGENTS.md | 快速可靠 |
| 找历史学习案例 | 查本索引 → 读对应文件 | 避免超时 |
| 找相似模式 | 尝试memory_search | 语义匹配 |

### 常见任务快速路径
1. **发送邮件** → 用send_email.py或bash脚本
2. **检查定时任务** → 读cron/jobs.json
3. **切换模型** → 编辑openclaw.json
4. **安装技能** → clawhub install <skill>
5. **记录学习** → 写入.learnings/LEARNINGS.md

## 🔄 更新日志
- 2026-03-10: 创建初始索引
- 每周日: 更新索引内容

---
**使用说明**: 优先查本索引定位信息，避免慢速检索