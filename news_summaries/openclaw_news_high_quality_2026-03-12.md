# OpenClaw 每日高质量新闻摘要

**日期**: 2026年3月12日（星期四）  
**来源**: GitHub官方仓库、OpenClaw文档、ClawHub  
**编辑**: 旺财 🐶

---

## 📰 今日精选新闻 (8条)

### 1️⃣ OpenClaw v2026.3.9 稳定版发布 🚀

**发布时间**: 2026年3月9日  
**来源**: GitHub Releases (官方)

OpenClaw 发布了最新的稳定版本 v2026.3.9，带来了多项重要更新：

**主要新功能**:
- **CLI备份功能**: 新增 `openclaw backup create` 和 `openclaw backup verify` 命令，支持本地状态归档，包括 `--only-config` 仅配置备份、`--no-include-workspace` 排除工作区等选项
- **Talk模式增强**: 新增 `talk.silenceTimeoutMs` 配置，可自定义语音输入后的静默等待时间
- **TUI智能识别**: 在已配置的Agent工作区中启动TUI时，自动推断当前Agent
- **Brave搜索LLM上下文**: 新增 `tools.web.search.brave.mode: "llm-context"` 选项，可调用Brave的LLM Context端点获取带来源元数据的摘要
- **ACP来源追溯**: 新增可选的ACP入口来源元数据，支持 `--provenance off|meta|meta+receipt` 参数

**修复内容**:
- macOS启动代理重启问题修复
- Android应用移除后台定位、录屏等功能，符合Play商店政策
- Telegram DM路由去重修复
- Matrix DM路由安全检测增强
- Feishu插件引导流程优化

🔗 [查看完整Release](https://github.com/openclaw/openclaw/releases)

---

### 2️⃣ ClawHub 技能市场持续扩展 🛠️

**来源**: ClawHub (clawhub.com)

ClawHub 作为 OpenClaw 的官方技能注册中心，持续扩展其生态系统：

**核心功能**:
- 浏览和发现社区贡献的 AgentSkills
- 一键安装技能到工作区: `clawhub install <skill-slug>`
- 批量更新所有已安装技能: `clawhub update --all`
- 同步扫描和发布更新: `clawhub sync --all`

**技能加载优先级** (从高到低):
1. `<workspace>/skills` - 工作区技能 (最高优先级)
2. `~/.openclaw/skills` - 本地管理技能
3. Bundled skills - 随安装包附带技能
4. `skills.load.extraDirs` - 额外配置目录

**安全提醒**:
- 第三方技能视为不受信任代码，启用前请阅读
- 敏感操作建议使用沙盒运行
- 通过 `skills.entries.*.env` 和 `apiKey` 注入密钥到主机进程

🔗 [访问 ClawHub](https://clawhub.com)

---

### 3️⃣ Feishu (飞书) 集成完全指南 📱

**来源**: OpenClaw 官方文档

OpenClaw 现已原生支持飞书(Lark)平台，无需额外插件安装：

**快速开始**:
```bash
# 方式1: 使用引导向导
openclaw onboard

# 方式2: CLI手动添加
openclaw channels add
```

**配置步骤**:
1. 访问 [飞书开放平台](https://open.feishu.cn/app) 创建企业应用
2. 获取 App ID (格式: `cli_xxx`) 和 App Secret
3. 配置权限 (包括 im:message、im:message:send_as_bot 等)
4. 启用机器人能力
5. 在 OpenClaw 中配置凭证

**权限清单**:
- `im:message` - 消息读取和发送
- `im:message.group_at_msg:readonly` - 群组@消息读取
- `im:message.p2p_msg:readonly` - 单聊消息读取
- `im:message:send_as_bot` - 以机器人身份发送消息
- `contact:user.employee_id:readonly` - 用户员工ID读取

**国际版 Lark 用户**: 使用 `https://open.larksuite.com/app` 并在配置中设置 `domain: "lark"`

🔗 [完整文档](https://docs.openclaw.ai/channels/feishu)

---

### 4️⃣ AgentSkills 规范详解 📚

**来源**: OpenClaw 官方文档

OpenClaw 采用 **AgentSkills** 兼容的技能格式，让Agent学会使用工具：

**SKILL.md 格式要求**:
```markdown
---
name: skill-name
description: 技能描述
---

# 技能说明...
```

**关键配置项**:
- `user-invocable`: `true|false` (默认true) - 是否暴露为用户斜杠命令
- `disable-model-invocation`: `true|false` (默认false) - 是否排除在模型调用外
- `homepage`: 技能主页URL
- `metadata`: 单行JSON对象，包含额外元数据

**多Agent环境**:
- **Per-agent技能**: 位于 `<workspace>/skills`，仅当前Agent可见
- **共享技能**: 位于 `~/.openclaw/skills`，所有Agent可见
- **插件技能**: 通过 `openclaw.plugin.json` 声明，随插件加载

**最佳实践**:
- 使用 `{baseDir}` 引用技能文件夹路径
- 保持 `metadata` 为单行JSON
- 敏感信息通过 `env` 和 `apiKey` 注入，避免硬编码

🔗 [技能文档](https://docs.openclaw.ai/tools/skills)

---

### 5️⃣ 社区 Showcase 精选项目 🌟

**来源**: OpenClaw Discord 社区

来自社区的真实应用案例：

#### 🍷 酒窖管理技能
**作者**: @prades_maxime
- 通过对话快速创建本地酒窖管理技能
- 支持CSV导入 (示例: 962瓶酒的数据)
- 完全本地化，无需外部API

#### 🛒 Tesco 购物自动化
**作者**: @marchattonhere
- 每周膳食计划 → 常规商品 → 预订配送时段 → 确认订单
- 无需API，纯浏览器控制完成
- 端到端购物流程自动化

#### 🔍 PR 代码审查 → Telegram 反馈
**作者**: @bangnokia
- OpenCode 完成代码修改并创建PR
- OpenClaw 自动审查diff
- 在Telegram中回复审查意见和合并建议

#### 📊 SNAG 屏幕截图分析
- 截图 → 自动分析 → 生成结构化报告
- 适用于bug报告和UI审查

🔗 [查看更多案例](https://docs.openclaw.ai/start/showcase)

---

### 6️⃣ OpenClaw 核心架构解析 🏗️

**来源**: GitHub README + 官方文档

**系统架构**:
```
聊天应用 + 插件 → Gateway → Pi Agent
                    ↓
              CLI / Web UI / macOS App / 移动端
```

**核心组件**:
1. **Gateway (网关)**: 单控制平面，管理会话、频道、工具和事件
2. **Pi Agent Runtime**: RPC模式运行，支持工具流和块流
3. **Session Model**: 多会话隔离，支持多Agent路由
4. **Web Control UI**: 浏览器仪表板，支持聊天、配置、会话管理

**支持的频道** (20+):
WhatsApp、Telegram、Discord、iMessage、Signal、Slack、Google Chat、BlueBubbles、IRC、Microsoft Teams、Matrix、Feishu、LINE、Mattermost、Nextcloud Talk、Nostr、Synology Chat、Tlon、Twitch、Zalo、WebChat

**平台支持**:
- macOS (菜单栏应用 + Canvas)
- iOS/Android (Node 配套应用)
- Linux/Windows (WSL2)

**安全特性**:
- DM配对机制 (dmPolicy="pairing")
- 本地允许列表存储
- `openclaw doctor` 风险检测
- 可选沙盒运行

🔗 [GitHub仓库](https://github.com/openclaw/openclaw)

---

### 7️⃣ 快速入门指南 🚀

**来源**: OpenClaw 官方文档

**5分钟快速开始**:

```bash
# 1. 安装 OpenClaw (需要 Node ≥22)
npm install -g openclaw@latest

# 2. 运行引导向导并安装守护进程
openclaw onboard --install-daemon

# 3. 配对频道 (如WhatsApp)
openclaw channels login

# 4. 启动网关
openclaw gateway --port 18789
```

**常用命令**:
```bash
# 发送消息
openclaw message send --to +1234567890 --message "Hello"

# 与Agent对话
openclaw agent --message "任务描述" --thinking high

# 检查网关状态
openclaw gateway status
openclaw logs --follow

# 更新到最新版
openclaw update --channel stable
```

**开发版本切换**:
- `stable`: 标签版本 (推荐)
- `beta`: 预发布版本
- `dev`: 主分支最新代码

**浏览器控制面板**:
- 本地访问: http://127.0.0.1:18789/
- 支持远程访问 (Tailscale/SSH)

🔗 [完整入门指南](https://docs.openclaw.ai/start/getting-started)

---

### 8️⃣ 语音与 Canvas 功能 🎙️🎨

**来源**: OpenClaw 官方文档

**Voice Wake (语音唤醒)**:
- macOS/iOS 支持语音唤醒词
- Android 支持连续语音模式
- 集成 ElevenLabs + 系统TTS 回退

**Live Canvas (实时画布)**:
- Agent 驱动的可视化工作区
- 支持 A2UI (Agent-to-User Interface)
- macOS 原生支持，移动端通过 Node 配套应用

**Talk 模式增强** (v2026.3.9):
- 新增 `talk.silenceTimeoutMs` 配置
- 可自定义语音输入后的静默检测时间
- 各平台保持默认暂停窗口行为

**移动端 Node**:
- iOS/Android 配套应用
- 支持 Canvas、相机、语音工作流
- 设备配对后可通过 Gateway 控制

🔗 [Voice Wake 文档](https://docs.openclaw.ai/nodes/voicewake)  
🔗 [Canvas 文档](https://docs.openclaw.ai/platforms/mac/canvas)

---

## 📊 数据统计

| 指标 | 数值 |
|------|------|
| 今日精选新闻 | 8条 |
| 官方来源 | GitHub Releases、官方文档 |
| 社区案例 | 4个 |
| 支持平台 | 20+ 聊天频道 |

---

## 🔗 相关链接

- **官网**: https://openclaw.ai
- **文档**: https://docs.openclaw.ai
- **GitHub**: https://github.com/openclaw/openclaw
- **ClawHub**: https://clawhub.com
- **Discord**: https://discord.gg/clawd
- **Twitter/X**: @openclaw

---

*本报告由 旺财 (OpenClaw AI助手) 自动生成*  
*生成时间: 2026-03-12 06:05 CST*
