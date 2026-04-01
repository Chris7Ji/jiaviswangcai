# 🦞 OpenClaw日报 - 2026年03月21日

## 📊 今日概览
- 精选动态：6条（英文6条）
- 重点类别：[功能增强/多渠道支持/测试优化]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 功能增强

### 1. Voice Call：修复流式TTS静默回归问题
**📰 来源**：GitHub PR #51500 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **问题**：`stream TTS` 出现静默回归，用户无法听到语音输出
- **修复**：强制执行语音输出契约（spoken-output contract）
- **影响范围**：Voice Call功能的所有用户
- **提交**：3f7f2c8 | **作者**：joshavant | **提交时间**：2026-03-21 2小时前
- **CI状态**：34/43检查通过

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/51500

---

### 2. Telegram：支持自定义apiRoot配置
**📰 来源**：GitHub PR #48842 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：支持Telegram使用自定义apiRoot，实现替代API端点
- **使用场景**：
  - 使用Telegram Bot API的第三方兼容服务
  - 企业内网部署需要自定义API地址
  - 开发者测试环境
- **作者**：Cypherm、claude、obviyus（3人协作）
- **提交**：6b4c24c | **提交时间**：2026-03-21 6小时前

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/48842

---

## ☁️ 平台扩展

### 3. 新增Anthropic-Vertex Provider：Claude可通过GCP Vertex AI调用
**📰 来源**：GitHub PR #43356 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：新增 `anthropic-vertex` provider，支持通过Google Cloud Platform的Vertex AI调用Claude模型
- **技术实现**：
  - 企业用户可在GCP环境中使用Claude
  - 支持GCP认证和配额管理
  - 与现有Vertex AI工作流集成
- **作者**：sallyom | **提交**：6e20c4b | **提交时间**：2026-03-20

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/43356

---

## 🔧 核心引擎优化

### 4. Context Engine：传递incoming prompt至assemble
**📰 来源**：GitHub PR #50848 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：Context Engine现在可以接收并处理incoming prompt并传递至assemble流程
- **意义**：增强上下文处理能力，让prompt组装更加灵活
- **作者**：danhdoan、jalehman | **提交**：e78129a | **提交时间**：2026-03-21 11小时前

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/50848

---

### 5. Context Engine Transcript维护功能
**📰 来源**：GitHub PR #51191 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：新增context engine transcript维护功能
- **用途**：自动管理对话转录的生命周期
- **作者**：jalehman | **提交**：751d5b7 | **提交时间**：2026-03-20

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/51191

---

## 📱 移动端优化

### 6. iOS QR配对流程改进
**📰 来源**：GitHub PR #51359 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：改进iOS端的QR码配对流程
- **改进点**：
  - 更流畅的配对体验
  - 更好的错误处理
- **作者**：BunsDev | **提交**：2fd3728 | **提交时间**：2026-03-21 5小时前

---

## 📈 数据洞察

### GitHub 仓库状态（截至2026-03-21）
| 指标 | 数值 |
|------|------|
| ⭐ Stars | 328,000+ |
| 🍴 Forks | 63,500+ |
| 📅 最新Release | v2026.3.13-1 (2026-03-14) |

### 今日Commit统计（2026-03-21）
- **总Commit数**：16条
- **主要贡献者**：joshavant、BunsDev、obviyus、sallyom、steipete、vincentkoc等
- **CI状态**：大部分检查处于failure状态（CI进行中）

### 昨日Commit统计（2026-03-20）
- **总Commit数**：19条
- **主要贡献者**：steipete、jalehman、vincentkoc、sallyom等
- **主题**：测试框架增强（test coverage）、性能优化

---

## 💬 社区动态

### 其他活跃Commit（未详细介绍）
**今日重点**：
- `fix(subagent): include partial progress when subagent times out (#40700)` - 超时子Agent现在返回部分进度
- `CLI: respect full timeout for loopback gateway probes (#47533)` - CLI超时处理改进
- `UI: fix and optimize overview log panels (#51477)` - 日志面板优化
- `fix: defer plugin runtime globals until use` - 插件运行时优化

**昨日重点**：
- `Exec: harden host env override handling across gateway and node (#51207)` - 环境变量安全加固
- `fix: sanitize malformed replay tool calls (#50005)` - 修复replay中的畸形工具调用
- 多项测试覆盖率提升（openai、openrouter、plugin-sdk）

---

## 🔮 值得关注的趋势

1. **多云支持**：新增Vertex AI provider表明OpenClaw正在加强企业级多云支持
2. **质量优先**：大量test coverage相关commit，优化CI/CD流程
3. **Telegram生态**：自定义apiRoot支持使Telegram集成更加灵活
4. **Voice Call稳定**：紧急修复TTS静默问题，显示对实时功能的质量关注
5. **发布时间线**：最新Release为7天前（3月14日），可能近期将有新版本发布

---

## 📅 版本发布时间线

| 日期 | 版本 | 亮点 |
|------|------|------|
| 03-14 | v2026.3.13-1 | Recovery版本，SSRF修复，内存优化 |
| 03-13 | v2026.3.12 | Dashboard v2，GPT-5.4快速模式 |
| 03-12 | v2026.3.11 | WebSocket安全修复，iOS/macOS改进 |
| 03-09 | v2026.3.8 | 多项功能更新 |
| 03-08 | v2026.3.7 | Breaking changes，重大更新 |

---

*报告生成时间：2026-03-21 19:14 | 数据来源：GitHub API + openclaw/openclaw仓库*
*注：最新Release仍为v2026.3.13-1（2026-03-14），过去24小时内无新Release发布*
