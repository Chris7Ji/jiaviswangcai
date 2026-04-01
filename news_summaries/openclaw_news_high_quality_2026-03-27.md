# 🦞 OpenClaw日报 - 2026年03月27日

## 📊 今日概览
- 精选动态：2条（中文0条，英文2条）
- 重点类别：[版本更新/平台集成/开发者工具]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 版本与功能

### 1. OpenClaw v2026.3.24 发布（平台集成大版本）
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **版本**：v2026.3.24（Latest，2026-03-25 16:35发布）
- **发布时间**：2026-03-25 16:35（约38小时前）
- **贡献者**：vincentkoc, davidguttman, hnshah, VACInc, huntharo, gfzhx, sallyom, JonathanJing, amsminn, BunsDev, Kimbo7870, w-sss +10 others（**22人**）
- **反应**：110人（77👍 8😄 16🎉 21❤️ 25🚀 7👀）
- **Commit数**：**184 commits** to main since this release

**📌 定位**：平台集成与开发者工具重大更新版本

**⚠️ Breaking变更**：
- 无重大破坏性变更

**🧩 新增功能（18项）**：

| 类别 | 功能 | PR |
|------|------|-----|
| **Gateway/OpenAI** | 新增 `/v1/models` 和 `/v1/embeddings` 端点，支持更广泛的客户端和RAG兼容性 | - |
| **Agents/tools** | `/tools` 显示当前agent实际可用的工具，Control UI增加"Available Right Now"实时区域 | - |
| **Microsoft Teams** | 迁移到官方Teams SDK，支持streaming 1:1回复、欢迎卡片、反馈机制、typing indicators | #51808 |
| **Microsoft Teams** | 新增消息编辑和删除支持 | #49925 |
| **Skills/一键安装** | 为coding-agent, gh-issues, openai-whisper-api, session-logs, tmux, trello, weather添加一键安装配方 | #53411 |
| **Control UI/技能** | 新增状态过滤标签（All/Ready/Needs Setup/Disabled），详情弹窗显示依赖、开关、安装动作、API key入口 | #53411 |
| **Slack/交互回复** | 恢复direct deliveries的丰富回复对等性，自动将Options:行渲染为buttons/selects | #53389 |
| **CLI/容器** | 新增 `--container` 和 `OPENCLAW_CONTAINER` 参数，支持在Docker/Podman容器内运行openclaw命令 | #52651 |
| **Discord/自动线程** | 新增 `autoThreadName: "generated"` 选项，支持LLM生成线程标题 | #43366 |
| **Plugins/hooks** | 新增 `before_dispatch` hook，支持规范化的inbound元数据 | #50444 |
| **Control UI/markdown** | agent工作区文件行改为可展开`<details>`，懒加载markdown预览 | #53411 |
| **Control UI/预览** | 使用`@create-markdown/preview` v2系统主题，支持light/dark模式 | #53411 |
| **macOS/导航** | 用可折叠树形侧边栏替换水平药丸导航 | #53411 |
| **CLI/skills** | 将"missing"标签软化为"needs setup"，在`openclaw skills info`中显示API key设置指导 | #53411 |
| **Runtime/Node** | 降低Node 22最低支持到22.14+ | - |
| **CLI/update** | 在运行全局包安装前检查engines.node | - |

**🔧 关键修复（15项）**：

| 类别 | 修复内容 | PR |
|------|----------|-----|
| **安全/media** | 关闭mediaUrl/fileUrl alias bypass，防止media-root限制被绕过 | #54034 |
| **Gateway/重启** | 重启后通过heartbeat唤醒中断的agent session | #53940 |
| **Docker/安装** | 避免pre-start openclaw-cli共享网络命名空间循环 | #53385 |
| **Gateway/通道** | 保持通道启动顺序，隔离单通道启动失败 | #54215 |
| **Embedded/密钥** | 防止未解析的SecretRef配置导致embedded agent崩溃 | #45838 |
| **WhatsApp/群组** | 跟踪最近发送的消息ID，抑制匹配的群组回声 | #53624 |
| **Telegram/论坛** | 当Telegram省略论坛元数据时恢复#General主题路由 | #53699 |
| **Discord/超时** | 当inbound Discord worker超时时发送可见超时回复 | #53823 |
| **Telegram/照片** | 预检照片尺寸和宽高比规则，无效时回退到文档发送 | #52545 |
| **Slack/运行时** | 削减Slack DM回复开销，恢复Codex自动传输 | #53957 |

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases/tag/v2026.3.24
- Compare：https://github.com/openclaw/openclaw/compare/v2026.3.24...main

---

### 2. OpenClaw v2026.3.23/v2026.3.22 反应持续增长
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：

| 版本 | 发布日期 | 贡献者 | 当前反应 | 24h增长 |
|------|----------|--------|----------|---------|
| **v2026.3.23** | 03-23 23:15 | 15人 | 201人 | +30 |
| **v2026.3.22** | 03-23 11:11 | 119人 | 218人 | +6 |

**📌 说明**：v2026.3.23和v2026.3.22在v2026.3.24发布后仍持续获得社区关注，反应数继续增长。

---

## 📈 数据洞察

### GitHub 仓库状态（截至2026-03-27）
| 指标 | 数值 | 变化 |
|------|------|------|
| ⭐ Stars | 328,730 | +393 |
| 👁 Watchers | 328,730 | - |
| 🍴 Forks | 66,100 | +310 |
| 🗣 语言 | TypeScript | - |

### 版本发布节奏（近4天）
| 版本 | 日期 | 类型 | 贡献者 | Commit数 | 反应 |
|------|------|------|--------|----------|------|
| **v2026.3.24** | 03-25 16:35 | 稳定版 | 22 | 184 | 110 |
| **v2026.3.24-beta.2** | 03-25 14:11 | 预发布 | 1 | - | 25 |
| **v2026.3.24-beta.1** | 03-25 11:54 | 预发布 | 33 | - | 23 |
| **v2026.3.23** | 03-23 23:15 | 修复版 | 15 | - | 201 |

---

## 🔮 趋势观察

1. **Microsoft Teams战略**：官方SDK迁移标志 Teams集成进入成熟阶段
2. **Skills生态系统完善**：一键安装recipe降低用户入门门槛
3. **Control UI全面升级**：从技能管理到文件预览全面重构
4. **开发者工具增强**：Docker容器支持、CLI/skills改进
5. **安全持续加固**：media dispatch安全修复、SecretRef处理改进

---

## 🔐 安全更新

| 类别 | 修复内容 | PR |
|------|----------|-----|
| **media dispatch bypass** | 关闭mediaUrl/fileUrl alias bypass，防止media-root限制被绕过 | #54034 |
| **SecretRef处理** | 防止未解析的SecretRef配置导致embedded agent崩溃 | #45838 |

---

*报告生成时间：2026-03-27 06:14 | 数据来源：GitHub openclaw/openclaw v2026.3.24 Release*
