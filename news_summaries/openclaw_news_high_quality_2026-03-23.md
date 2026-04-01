# 🦞 OpenClaw日报 - 2026年03月23日

## 📊 今日概览
- 精选动态：6条（中文0条，英文6条）
- 重点类别：[版本更新/安全修复/平台扩展]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 版本与功能

### 1. OpenClaw v2026.3.22-beta.1 发布（重磅更新）
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **版本**：v2026.3.22-beta.1（Pre-release for npm beta tag）
- **发布时间**：2026-03-23 09:37（今日）
- **贡献者**：vincentkoc, steipete, +116 other contributors（117人）
- **反应**：22人点赞（11👍 8🎉 4❤️ 8🚀）
- **Commit数**：9 commits to main since this release
- **macOS**：本次Beta无新macOS app build，macOS资产仍基于稳定版2026.3.22

**⚠️ 重大破坏性变更（Breaking）**：
1. **ClawHub优先**：插件安装现在优先使用ClawHub而非npm
2. **Chrome扩展移除**：废弃Chrome扩展relay路径，迁移到existing-session/user browser config
3. **图片生成标准化**：统一使用核心image_generate工具，移除nano-banana-pro包装
4. **Plugin SDK重构**：openclaw/extension-api已移除，迁移到openclaw/plugin-sdk/*
5. **消息发现API变更**：必须使用ChannelMessageActionAdapter.describeMessageTool(...)
6. **新Matrix插件**：基于官方matrix-js-sdk的新实现
7. **环境变量清理**：移除CLAWDBOT_*和MOLTBOT_*兼容性别名
8. **状态目录清理**：移除.moltbot状态目录自动检测
9. **Exec沙箱加固**：阻止JVM注入(MAVEN_OPTS/SBT_OPTS/GRADLE_OPTS)、glibc tunables、.NET依赖劫持

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases/tag/v2026.3.22-beta.1
- Commit：https://github.com/openclaw/openclaw/commit/d8d545bac1ee36078a3c2e5e8c85b92456e7423f
- 对比：https://github.com/openclaw/openclaw/compare/v2026.3.22-beta.1...main

---

### 2. 【安全】Voice Call Webhooks安全加固
**📰 来源**：GitHub PR (v2026.3.22-beta.1) | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 在body读取前验证provider签名头
- 预认证body预算降至64KB/5s（原1MB/30s）
- 每个源IP的并发预认证请求设置上限
- 防止未认证调用者强制使用旧的1MB/30s缓冲路径
- 感谢@SEORY0报告

**🔗 相关链接**：
- PR: #51500 (Voice Call: enforce spoken-output contract)

---

### 3. 【安全】Windows远程媒体路径阻塞
**📰 来源**：GitHub PR (v2026.3.22-beta.1) | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 在本地文件系统解析前阻止远程host的file://媒体URL
- 阻止UNC和网络路径
- 防止Windows上结构化本地媒体输入触发外向SMB凭证握手
- 感谢@RacerZ-fighting报告

---

### 4. 【新功能】ClawHub原生支持
**📰 来源**：GitHub PR (v2026.3.22-beta.1) | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 新增openclaw skills search|install|update命令
- 支持openclaw plugins install clawhub:<package>
- 支持跟踪更新元数据
- Gateway skill-install/update支持ClawHub请求

**🔗 相关链接**：
- 文档：https://docs.openclaw.ai/tools/clawhub

---

### 5. 【新功能】新沙箱后端（SSH + OpenShell）
**📰 来源**：GitHub PR (v2026.3.22-beta.1) | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **SSH沙箱后端**：支持secret备份的密钥、证书和known_hosts输入
- **OpenShell后端**：支持mirror和remote工作区模式
- 沙箱list/recreate/prune现在支持后端感知而非仅Docker

---

### 6. 【性能】Agent默认超时提升至48小时
**📰 来源**：GitHub PR (v2026.3.22-beta.1) | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- 共享默认agent超时从600s提升至48h
- 长时运行的ACP和agent会话不再轻易失败
- 除非用户配置更短的限制

---

## 🧩 新增提供商/插件

| 提供商 | 变更类型 | 说明 |
|--------|----------|------|
| **Anthropic Vertex** | 新增 | 通过Google Vertex AI支持Claude |
| **Chutes** | 新增 | 带OAuth/API-key认证的bundle provider |
| **Exa** | 新增 | 捆捆绑Web搜索插件 |
| **Tavily** | 新增 | 专用tavily_search和tavily_extract工具 |
| **Firecrawl** | 新增 | onboard/configure搜索提供商 |
| **Matrix** | 重构 | 基于matrix-js-sdk的新实现 |
| **MiniMax** | 扩展 | 新增M2.7和M2.7-highspeed模型 |

---

## 🔐 安全修复汇总（来自v2026.3.22-beta.1）

| 编号 | 类型 | 描述 |
|------|------|------|
| GHSA-7jrw-x62h-64p8 | Device pairing | iOS设置码绑定到目标节点配置文件 |
| - | Nostr | 入站DM策略在解密前执行，添加加密前速率/大小防护 |
| - | Synology Chat | 回复传递绑定到稳定numeric user_id |
| - | Media | Windows UNC路径和file:// URL阻塞 |
| - | Voice webhooks | 预认证body限制和并发限制 |
| - | SSRF | 显式代理SSRF固定增强 |
| - | Browser CDP | 远程CDP目标private/internal hosts警告 |

---

## 📈 数据洞察

### GitHub 仓库状态（截至2026-03-23）
| 指标 | 数值 |
|------|------|
| ⭐ Stars | 328,141 (+3,000) |
| 👁 Watchers | 328,141 |
| 🍴 Forks | 64,500 (+751) |
| 🐛 Open Issues | 14,643 |
| 🗣 语言 | TypeScript |

### 版本发布节奏
- **v2026.3.22-beta.1**: 2026-03-23（今日）
- **v2026.3.13**: 2026-03-14（9天前）
- **趋势**：版本号从.13跳到.22，说明这期间大量开发和合并

---

## 💬 其他重要变更

- **Discord命令**：切换到Carbon reconcile，减少重启时的命令抖动
- **Telegram**：支持自定义apiRoot、自定义Bot API端点
- **Feishu**：新增交互式审批卡片、流式推理显示
- **Android**：系统级深色主题、Talk语音合成迁移到gateway
- **Control UI**：圆角主题可调节、session下拉标签优化

---

## 🔮 值得关注的趋势

1. **平台化战略**：ClawHub、Marketplace、Plugin SDK全面升级
2. **安全优先**：大量安全修复，webhook预认证加固
3. **多提供商扩展**：新增Vertex、Chutes、Exa、Tavily、Firecrawl
4. **性能优化**：WhatsApp冷启动从"数十秒"降至秒级
5. **国际化**：Feishu深度集成（审批卡片、流式推理）

---

*报告生成时间：2026-03-23 18:54 | 数据来源：GitHub openclaw/openclaw v2026.3.22-beta.1 Release*
