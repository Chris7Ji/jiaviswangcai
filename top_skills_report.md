# 📊 OpenClaw Top 10 最有用的Skills报告

## 🎯 基于你的系统已安装的技能分析

根据你的OpenClaw安装，以下是已经安装的**最有用和流行的10个技能**：

---

## 🏆 Top 10 最有用的OpenClaw Skills

### 1. **github** - GitHub集成
**用途**: GitHub仓库管理、Issue跟踪、PR审查、CI/CD监控
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/github`
**关键功能**:
- 查看PR状态和CI运行
- 创建/评论Issue
- 代码审查辅助
- 仓库管理

### 2. **gog** - Google Workspace CLI
**用途**: Gmail、Calendar、Drive、Contacts、Sheets、Docs管理
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/gog`
**关键功能**:
- 邮件搜索和管理
- 日历事件查看
- Google Drive文件操作
- 联系人管理

### 3. **healthcheck** - 系统健康检查
**用途**: 主机安全加固、风险配置、安全审计
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/healthcheck`
**关键功能**:
- 安全漏洞扫描
- 防火墙配置检查
- SSH安全审计
- 系统更新状态

### 4. **summarize** - 内容摘要
**用途**: URL、播客、本地文件的文本摘要和提取
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/summarize`
**关键功能**:
- 网页内容摘要
- 视频转录摘要
- 文档内容提取
- 多语言支持

### 5. **video-frames** - 视频帧提取
**用途**: 使用ffmpeg从视频中提取帧或短片
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/video-frames`
**关键功能**:
- 视频帧截图
- GIF创建
- 视频剪辑提取
- 时间戳定位

### 6. **weather** - 天气查询
**用途**: 当前天气和天气预报
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/weather`
**关键功能**:
- 实时天气查询
- 多日天气预报
- 全球位置支持
- 无需API密钥

### 7. **wacli** - WhatsApp集成
**用途**: 发送WhatsApp消息、搜索/同步历史记录
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/wacli`
**关键功能**:
- 发送WhatsApp消息
- 消息历史搜索
- 联系人管理
- 群组操作

### 8. **1password** - 密码管理
**用途**: 1Password CLI设置和使用
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/1password`
**关键功能**:
- 密码读取和注入
- 安全笔记管理
- 多账户支持
- 桌面应用集成

### 9. **apple-reminders** - 苹果提醒事项
**用途**: 通过remindctl CLI管理Apple Reminders
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/apple-reminders`
**关键功能**:
- 提醒事项列表
- 添加/编辑/完成提醒
- 列表管理
- JSON/纯文本输出

### 10. **gh-issues** - GitHub Issue自动化
**用途**: 获取GitHub issues、自动修复、PR创建
**已安装**: ✅ 是
**位置**: `/opt/homebrew/lib/node_modules/openclaw/skills/gh-issues`
**关键功能**:
- Issue自动分类
- 代码修复生成
- PR自动创建
- 审查评论处理

---

## 📈 其他有用的已安装技能

### 开发工具类:
- **clawhub** - 技能搜索和安装
- **skill-creator** - 技能创建工具
- **coding-agent** - 编码助手
- **nano-pdf** - PDF编辑

### 通信集成:
- **discord** - Discord集成
- **slack** - Slack集成
- **feishu** - 飞书集成（在extensions目录）

### 多媒体处理:
- **camsnap** - 摄像头截图
- **sag** - ElevenLabs TTS
- **openai-whisper** - 语音转录

### 生产力工具:
- **notion** - Notion集成
- **obsidian** - Obsidian笔记
- **things-mac** - Things 3集成

---

## 🔧 技能使用指南

### 如何查看技能详情:
```bash
# 查看技能文档
cat /opt/homebrew/lib/node_modules/openclaw/skills/<技能名>/SKILL.md

# 示例：查看github技能
cat /opt/homebrew/lib/node_modules/openclaw/skills/github/SKILL.md
```

### 如何更新技能:
```bash
# 使用clawhub更新
clawhub update --dir /opt/homebrew/lib/node_modules/openclaw/skills

# 或重新安装特定技能
clawhub install <技能名>
```

### 如何发现新技能:
```bash
# 搜索技能
clawhub search <关键词>

# 浏览最新技能
clawhub explore --limit 10
```

---

## 🚀 推荐配置顺序

1. **首先配置**:
   - `gog` - 需要Google账户认证
   - `1password` - 需要1Password CLI设置
   - `github` - 需要GitHub token

2. **日常使用**:
   - `weather` - 随时查询天气
   - `summarize` - 快速摘要内容
   - `apple-reminders` - 任务管理

3. **专业用途**:
   - `gh-issues` - 开发工作流
   - `healthcheck` - 系统维护
   - `video-frames` - 媒体处理

---

## 📊 技能分类统计

| 类别 | 数量 | 代表技能 |
|------|------|----------|
| **开发工具** | 6+ | github, gh-issues, clawhub, skill-creator |
| **云服务集成** | 4+ | gog, 1password, notion, obsidian |
| **通信工具** | 5+ | wacli, discord, slack, feishu |
| **多媒体** | 5+ | video-frames, camsnap, sag, openai-whisper |
| **生产力** | 4+ | apple-reminders, summarize, weather, healthcheck |
| **其他** | 10+ | 各种专业工具 |

---

## 💡 使用建议

### 新手入门:
1. 从 `weather` 和 `summarize` 开始，最简单易用
2. 配置 `gog` 管理Google服务
3. 使用 `apple-reminders` 管理日常任务

### 开发者:
1. 深度使用 `github` 和 `gh-issues`
2. 配置 `1password` 管理密钥
3. 使用 `healthcheck` 维护服务器

### 内容创作者:
1. 使用 `video-frames` 处理视频
2. 用 `summarize` 整理资料
3. 通过 `wacli` 管理社交媒体

---

## 🔄 维护建议

1. **定期更新**:
   ```bash
   # 每月更新一次
   clawhub update
   ```

2. **清理未用技能**:
   ```bash
   # 查看技能使用频率
   ls -la /opt/homebrew/lib/node_modules/openclaw/skills/
   ```

3. **备份配置**:
   ```bash
   # 备份技能配置
   cp -r /opt/homebrew/lib/node_modules/openclaw/skills/ ~/backup/openclaw-skills/
   ```

---

## 📞 获取帮助

- **官方文档**: https://docs.openclaw.ai
- **技能市场**: https://clawhub.com
- **社区支持**: https://discord.com/invite/clawd
- **GitHub**: https://github.com/openclaw/openclaw

---

**报告生成时间**: 2026-02-28 21:56 GMT+8  
**OpenClaw版本**: 最新稳定版  
**技能总数**: 50+ 个已安装技能  
**推荐指数**: ⭐⭐⭐⭐⭐ (技能生态丰富)

> 💡 提示: 你已经拥有了一个非常强大的OpenClaw技能生态系统，可以满足大多数日常和专业需求！