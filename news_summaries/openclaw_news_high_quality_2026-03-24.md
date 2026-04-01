# 🦞 OpenClaw日报 - 2026年03月24日

## 📊 今日概览
- 精选动态：4条（中文0条，英文4条）
- 重点类别：[版本更新/安全修复/平台稳定性]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 版本与功能

### 1. OpenClaw v2026.3.23 发布（快速修复版本）
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **版本**：v2026.3.23（Latest）
- **发布时间**：2026-03-23 23:15（约53分钟前）
- **贡献者**：vincentkoc, osolmaz, +5 other contributors（7人）
- **反应**：15人点赞（1🎉 15❤️）
- **Commit数**：6 commits to main since this release
- **Commit**：`ccfeecb6887cd97937e33a71877ad512741e82b2`

**📌 定位**：v2026.3.22之后的快速修复版本，主要修复ClawHub认证和Browser MCP问题

**🔧 关键修复列表**：

| 类别 | 修复内容 | PR |
|------|----------|-----|
| **Browser/Chrome MCP** | 等待existing-session浏览器标签页可用后再attach，减少macOS上的超时和重复授权 | #52930 |
| **Browser/CDP** | 复用已运行的loopback浏览器，避免慢速headless Linux上的第二启动失败 | #53004 |
| **ClawHub/macOS** | 识别macOS auth config和XDG auth路径，修复skill浏览时静默降级为未认证模式 | #53034 |
| **ClawHub/skills** | 为gateway skill浏览解析本地ClawHub auth token | #52949 |
| **Plugins/message** | Discord components和Slack blocks变回可选，Feishu media sends修复 | #52970, #52962 |
| **Gateway/model pricing** | 阻止openrouter/auto定价刷新无限递归 | #53035 |
| **Mistral/models** | 降低max-token默认值到安全输出预算，修复历史配置的422错误 | #52599 |
| **Agents/web_search** | 使用active runtime web_search provider而非stale/default选择 | #53020 |
| **OpenAI Codex OAuth** | 在代理环境修复OAuth token刷新 | #52228 |
| **Plugins/memory-lancedb** | 修复LanceDB在全局npm安装后的引导问题 | #26100 |
| **Config/plugins** | 将stale unknown plugin ids视为警告而非致命错误 | #52992 |
| **DeepSeek provider** | 重构为共享单provider插件入口 | #48762 |
| **Matrix** | 修复duplicate runtime-api exports导致的启动崩溃 | #52909 |
| **Security/exec** | 保持shell-wrapper positional-argv allowlist匹配在真实直接载体上 | - |
| **Gateway/supervision** | 阻止lock冲突在launchd/systemd下崩溃循环 | #52922 |
| **Gateway/auth** | canvas路由需要auth，agent session reset需要admin scope | - |

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- Compare：https://github.com/openclaw/openclaw/compare/v2026.3.23...main
- Commit：https://github.com/openclaw/openclaw/commit/ccfeecb6887cd97937e33a71877ad512741e82b2

---

### 2. OpenClaw v2026.3.22 发布（平台重构里程碑）
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **版本**：v2026.3.22（稳定版，2026-03-23 11:11发布）
- **发布时间**：2026-03-23 11:11（约12小时前）
- **贡献者**：vincentkoc, steipete, +116 other contributors（117人）
- **反应**：174人点赞（127👍 20😄 36🎉 36❤️ 28🚀 23👀）
- **Commit数**：9 commits to main
- **Commit**：`e7d11f6`

**⚠️ 重大破坏性变更（Breaking）**：
1. **ClawHub优先**：插件安装现在优先使用ClawHub而非npm
2. **Chrome扩展移除**：废弃Chrome扩展relay路径，迁移到existing-session/user browser config
3. **图片生成标准化**：统一使用核心image_generate工具，移除nano-banana-pro
4. **Plugin SDK重构**：openclaw/extension-api已移除，迁移到openclaw/plugin-sdk/*
5. **消息发现API变更**：必须使用ChannelMessageActionAdapter.describeMessageTool(...)
6. **新Matrix插件**：基于官方matrix-js-sdk的新实现
7. **环境变量清理**：移除CLAWDBOT_*和MOLTBOT_*兼容性别名
8. **Exec沙箱加固**：阻止JVM/Gradle/.NET注入攻击

**🧩 新增功能**：
- SSH沙箱后端
- Anthropic Vertex provider（通过Google Vertex AI支持Claude）
- Chutes provider（带OAuth/API-key认证）
- Exa、Tavily、Firecrawl网页搜索插件
- MiniMax M2.7和M2.7-highspeed模型

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases/tag/v2026.3.22

---

## 🧩 技能生态

### ClawHub生态系统完善
| 功能 | 状态 | 说明 |
|------|------|------|
| openclaw skills search | 🆕 | 原生搜索支持 |
| openclaw skills install | 🆕 | 原生安装支持 |
| openclaw skills update | 🆕 | 原生更新支持 |
| openclaw plugins install clawhub:\<package\> | 🆕 | ClawHub优先安装 |
| macOS auth config | 🆕 (本版本修复) | macOS认证路径支持 |
| XDG auth paths | 🆕 (本版本修复) | Linux风格认证路径 |

---

## 📈 数据洞察

### GitHub 仓库状态（截至2026-03-24）
| 指标 | 数值 | 变化 |
|------|------|------|
| ⭐ Stars | 328,242 | +101 |
| 👁 Watchers | 328,242 | - |
| 🍴 Forks | 64,720 | +220 |
| 🐛 Open Issues | ~14,600 | - |
| 🗣 语言 | TypeScript | - |

### 版本发布节奏（3天内9个版本）
| 版本 | 日期 | 类型 | 亮点 |
|------|------|------|------|
| **v2026.3.23** | 03-23 23:15 | 修复版 | 22+修复，ClawHub/Browser MCP修复 |
| **v2026.3.22** | 03-23 11:11 | 稳定版 | 平台重构，117贡献者，174反应 |
| **v2026.3.22-beta.1** | 03-23 09:37 | 预发布 | v2026.3.22的beta版 |
| v2026.3.13-1 | 03-14 | 修复版 | recovery release |

---

## 🔮 值得关注的趋势

1. **快速修复周期**：v2026.3.22发布后12小时内即发布v2026.3.23修复ClawHub认证问题
2. **ClawHub战略**：从npm生态向ClawHub原生生态转型
3. **平台稳定性**：大量修复集中在认证、代理、浏览器集成等基础设施
4. **多模态扩展**：新增Exa/Tavily/Firecrawl等网页搜索插件
5. **开发者体验**：修复了大量DX问题（超时、认证、OAuth代理等）

---

## 🔐 安全更新

| 类别 | 修复内容 |
|------|----------|
| **exec approvals** | 保持shell-wrapper positional-argv allowlist匹配在真实直接载体上 |
| **Gateway/auth** | canvas路由需要auth，agent session reset需要admin scope |
| **Browser/CDP** | SSRF policy增强，private/internal hosts警告 |

---

*报告生成时间：2026-03-24 08:07 | 数据来源：GitHub openclaw/openclaw v2026.3.23 + v2026.3.22 Releases*
