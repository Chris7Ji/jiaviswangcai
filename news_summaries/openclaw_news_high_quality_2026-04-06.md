# 🦞 OpenClaw日报 - 2026年04月07日

## 📊 今日概览
- 精选动态：4条（中文1条，英文3条）
- 重点类别：[版本更新/技能生态/安全修复/实验性功能]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 版本与功能

### 1. 🎉 v2026.4.5 重磅发布：内置视频/音乐生成 + 12语言UI + 实验性记忆引擎
**📰 来源**：GitHub Official Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
OpenClaw v2026.4.5 于 2026-04-06 03:04 UTC 正式发布，这是 4 月初最重磅的更新之一，在多媒体创作、AI记忆系统和国际化方面实现重大突破：

- **重大变更 (Breaking)**：
  - 全面清理遗留配置别名（legacy public config aliases），移除 `talk.voiceId`/`talk.apiKey`、`agents.*.sandbox.perSession`、`browser.ssrfPolicy.allowPrivateNetwork`、`hooks.internal.handlers` 等老路径，统一迁移至标准公开配置路径，并提供 `openclaw doctor --fix` 自动迁移支持。

- **核心功能增强 (Changes)**：
  - **🚀 内置视频生成工具 (`video_generate`)**：全新内置工具，支持 xAI (`grok-imagine-video`)、阿里云 Model Studio Wan、Runway 三家视频提供方，并具备实时任务跟踪和完成后媒体直送能力。
  - **🎵 内置音乐生成工具 (`music_generate`)**：集成 Google Lyria、MiniMax、ComfyUI 工作流三大后端，支持异步任务追踪和音频成品直送。
  - **ComfyUI 工作流插件**：全新 `comfy` 插件，支持本地 ComfyUI / Comfy Cloud 工作流，包括 `image_generate`、`video_generate`、`music_generate` 完整工具链，支持参考图上传、实时测试和成品下载。
  - **多语言控制面板**：Control UI 新增**简体中文、繁体中文、日语、韩语、德语、法语、西班牙语、葡萄牙语、土耳其语、印尼语、波兰语、乌克兰语**等 12 种语言支持（感谢 @vincentkoc）。
  - **🧠 实验性记忆引擎 (Memory/Dreaming)**：全新的加权短时记忆提升系统，支持 `/dreaming` 命令、Dreams UI 界面、多语言概念标签、三阶段（Light/Deep/REM）协同调度，独立后台运行。大幅降低手动配置门槛（感谢 @vignesh07、@davemorin）。
  - **任务流引擎重构**：Task Flow 恢复核心基板，支持 Managed vs. Mirrored 双同步模式、持久化流程状态与版本追踪、`openclaw flows` 检查/恢复原语（感谢 @mbelinky）。
  - **Amazon Bedrock Mantle**：新增 Mantle 支持及推理配置自动发现，自动注入请求 Region，Claude、Qwen、Kimi、GLM 等路由开箱即用（感谢 @wirjo）。
  - **ACPX 运行时内嵌**：ACP 运行时直接嵌入 `acpx` 插件，移除外部 ACP CLI 调用依赖，降低传输开销并加固会话绑定。
  - **iOS / Matrix 原生执行审批**：APNs 推送通知直接打开应用内执行审批弹窗；Matrix 原生审批支持账号级审批者、频道/DM 投递和线程感知解析。
  - **Prompt 缓存优化**：跨传输回退、MCP 工具顺序、压缩、嵌入图像历史、系统提示指纹去重等多个路径提升缓存复用率，显著降低 API 成本。

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases/tag/v2026.4.5

---

## 🧩 技能生态

### 1. ComfyUI 工作流插件：本地 AI 媒体创作新时代
**📰 来源**：GitHub Release Notes | **🌐 语言**：中/英 | **✅ 验证状态**：已验证

**📝 核心内容**：
全新 `comfy` 插件打通了本地 ComfyUI / Comfy Cloud 工作流与 OpenClaw Agent 的完整链路：
- 支持 `image_generate`、`video_generate`、`music_generate` 三大内置工具
- 支持 Prompt 注入（工作流变量动态传参）
- 支持参考图像上传（ControlNet/IP-Adapter 等）
- 内置 Live Test 模式，支持输出预览和成品下载
- 已在官方集成包中默认打包

---

### 2. 插件配置 TUI：交互式引导安装体验
**📰 来源**：GitHub PR #60590, #60544 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 新增插件配置 TUI 提示，融入引导式安装/设置流程
- 新增 `openclaw plugins install --force` 命令，支持覆盖已安装插件和 Hook 包，无需使用 `--dangerously-force-unsafe-install` 标志
- ClawHub 搜索、详情页和安装流程已直接在 Skills 面板中内嵌（感谢 @samzong）

---

## 🔐 安全修复专区

### 1. Claude CLI 安全隔离大升级：三重防护全面落地
**📰 来源**：GitHub Security Fixes | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
v2026.4.5 包含 OpenClaw 历史上最激进的安全修复，聚焦 Claude CLI 后门会话隔离：
- 清理继承的 `CLAUDE_CONFIG_DIR` 和 `CLAUDE_CODE_PLUGIN_*` 环境变量，防止 Claude CLI 被悄悄重定向至恶意配置树
- 清理继承的 Claude CLI 提供商路由和托管认证环境变量，阻止代理、Bedrock、Vertex、Foundry 或父级托管令牌上下文被静默劫持
- 强制 `--setting-sources user`，阻止仓库本地 `.claude` 项目设置/钩子/插件在非交互式 OpenClaw 会话中执行
- 将畸形 `--permission-mode` 后端覆盖视为缺失，安全回退至 `bypassPermissions`
- 设备配对安全：要求非管理员配对设备会话仅能管理自身设备，防跨设备 Token 窃取
- 网关鉴权：循环遍历浏览器来源鉴权节流，阻止同一 localhost 来源锁定不同 localhost 浏览器来源

---

### 2. 通用安全加固：插件工具白名单与SSRF防护
**📰 来源**：GitHub Security Advisory | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 保留严格的插件专用工具白名单，`/allowlist add` 和 `/allowlist remove` 要求所有者权限
- `before_tool_call` 钩子崩溃时默认拒绝（Fails Closed）
- 阻止浏览器 SSRF 重定向绕过
- 插件市场远程 symlink 逃逸防护（感谢 @eleqtrizit）
- Synology Chat HTTPS Helper TLS 验证默认开启

---

## 💬 社区精选

### 1. 平台兼容性全面提升：Telegram / Discord / WhatsApp / MS Teams
**📰 来源**：GitHub Commits & Issues | **🌐 语言**：中/英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **Telegram**：修复模型选择器检查、HTML 格式确认消息、主题回复、持久化 Reaction 所有权、媒体占位符、群组图片读取等多项问题；DM 语音笔记恢复预检转录
- **Discord**：修复代理配置、组件媒体发送、`@everyone`/`@here` 提及门控；图片生成工具输出包含真实 `MEDIA:` 路径，修复生成的图片回复指向丢失本地文件的问题
- **WhatsApp**：恢复 `blockStreaming` 并在重连后重置看门狗超时，修复静默聊天重连循环
- **MS Teams**：用 `httpServerAdapter` 替换已弃用的 Teams SDK HttpPlugin Stub；支持通过 Graph API 下载内联 DM 图片并保留频道回复线程

---

## 📈 数据洞察
- **发布热度**：v2026.4.5 发布后迅速积累 **138 个 Reactions**（63👍 10😄 13🎉 22❤️ 18🚀 12👀），**103 位贡献者被提及**，社区反响极为热烈
- **仓库趋势**：基于 v2026.4.2（4月2日）至 v2026.4.5（4月6日）密集发布，4天内完成多个关键里程碑，多媒体生成、记忆引擎、国际化三大方向同步突破
- **中国社区**：Qwen、Fireworks AI、StepFun、MiniMax 等中国AI厂商首次进入官方捆绑包，彰显 OpenClaw 对中国AI生态的重视

---
*报告生成时间：2026-04-07 06:00 | 数据来源：GitHub + 全球技术社区*