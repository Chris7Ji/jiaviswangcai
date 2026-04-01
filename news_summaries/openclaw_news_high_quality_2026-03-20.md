# 🦞 OpenClaw日报 - 2026年03月20日

## 📊 今日概览
- 精选动态：7条（英文7条）
- 重点类别：[版本更新/安全修复/功能增强]
- 质量评级：⭐⭐⭐⭐⭐

---

## 🚀 版本与功能

### 1. OpenClaw v2026.3.13 发布（含Recovery版本）
**📰 来源**：GitHub Release | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **最新稳定版**：v2026.3.13-1（Recovery版本，修复正式版问题）
- **Beta版**：v2026.3.13-beta.1 于 2026-03-14 发布
- 同期版本：v2026.3.12（2026-03-13）、v2026.3.11 正式版及Beta（2026-03-12）
- 快速迭代节奏：连续5天发布新版本（3月12日-16日），进入高频维护期
- 当前主分支SHA：a66b98a9daae61139a05ebc6e709f6e0bff10647

**🔗 相关链接**：
- Release页面：https://github.com/openclaw/openclaw/releases
- 主仓库：https://github.com/openclaw/openclaw

---

### 2. 【安全】修复Shell命令分析器Heredoc安全漏洞（高危）
**📰 来源**：GitHub PR #20177 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **漏洞编号**：GHSA-65rx-fvh6-r4h2
- **漏洞类型**：Allowlist绕过（命令替换注入）
- **问题描述**：`splitShellPipeline` 在解析shell命令时，当遇到未加引号的heredoc定界符（如 `<<EOF`）时，会跳过整个heredoc body不检查其中是否包含危险令牌（`$(...)`, `` `...` ``, `${...}`）
- **攻击场景**：在无值守Gateway部署中，攻击者可利用 `cat <<EOF\n$(id)\nEOF` 绕过allowlist执行任意命令
- **修复方案**：在 `parseHeredocDelimiter` 增加 `quoted` 标志，扫描未加引号heredoc body中的危险令牌；加引号heredoc（`<<'EOF'`）不受影响
- **测试覆盖**：7个新测试覆盖各类攻击路径
- **提交**：a54bba6 | **作者**：orlyjamie

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/20177
- 安全公告：https://github.com/openclaw/openclaw/security/advisories/GHSA-65rx-fvh6-r4h2

---

## 🔧 代码质量与构建

### 3. 构建系统优化：新增 `pnpm build:runtime` 目标
**📰 来源**：GitHub PR #17636 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：新增 `pnpm build:runtime` 脚本，跳过plugin-sdk TypeScript声明文件生成
- **用途**：打包厂商从源码构建时通常不需要 `.d.ts` 声明文件，可节省构建时间
- **影响**：`pnpm build` 保持不变，仅新增运行时构建目标
- **提交**：3254bae | **作者**：joshp123 | **标签**：maintainer

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/17636

---

### 4. 测试框架重构：MockFn类型结构化改进
**📰 来源**：GitHub PR #16544 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **问题**：最近CI/tsgo失败（TS2742）由从harness模块导出Vitest推断类型导致
- **修复**：在 `src/test-utils/vitest-mock-fn.ts` 定义结构化 `MockFn` 类型（不引用Vitest内部类型）
- **额外改进**：
  - 更新所有harness使用 `vi.fn<T>()` 避免类型宽化
  - 修复 `monitor.skips-group-messages-without-mention-by-default.test.ts` 的oxlint警告
  - 为 `exec-approvals.test.ts` 添加Windows平台保护（safe bins在Windows上因PowerShell解析差异被禁用）
- **提交**：ec349c4 | **作者**：steipete | **标签**：maintainer

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/16544

---

## 🤖 Agent能力增强

### 5. RLM Harness：无限上下文窗口（实验性）
**📰 来源**：GitHub PR #17749 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **核心功能**：添加递归语言模型（RLM）引擎，使用沙箱JavaScript REPL让Agent迭代式解决问题
- **工作原理**：Agent不将所有内容塞入上下文窗口，而是写小代码片段、观察输出、用符号检索/切片逐步工作
- **技术基础**：基于arXiv论文《2512.24601》及DSPy参考实现
- **性能提升**：大上下文任务（长文档、多文件搜索、信息聚合）RLM持续优于标准LLM调用
- **API运行时**：`context_read/search`、`repo_read/search`、`llm_query`、`tool_call`、`get_var/set_var`、`print`、`submit`
- **使用方式**：配置 `tools.rlm.enabled: true`，然后 `/rlm summarize this project`
- **可调参数**：`maxDepth`(0-8)、`maxIterations`(1-96)、`maxLlmCalls`(1-2048)、`timeoutSeconds`、`extractOnMaxIterations`
- **提交**：8d63d45b | **作者**：cezarc1 | **标签**：agents, size: XL

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/17749
- RLM论文：https://arxiv.org/pdf/2512.24601
- DSPy实现：https://dspy.ai/api/modules/RLM/

---

### 6. Agent系统提示增强：子Agent生成指导
**📰 来源**：GitHub PR #14432 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **功能**：在生成的Agent系统提示中添加何时使用 `sessions_spawn`（后台子Agent）的具体指导
- **位置**：`src/agents/system-prompt.ts` 的工具部分
- **配套测试**：新增单元测试验证新引导文本存在
- **提交**：060c6d6 | **作者**：vignesh07 | **标签**：maintainer, agents

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/14432

---

### 7. HEARTBEAT.md 仅在新工作区初始化（Bug修复）
**📰 来源**：GitHub PR #19482 | **🌐 语言**：英 | **✅ 验证状态**：已验证

**📝 核心内容**：
- **问题**：`ensureAgentWorkspace()` 为每个缺少HEARTBEAT.md的工作区创建文件——包括用户故意删除的现有工作区
- **修复**：将 `writeFileIfMissing(heartbeatPath, ...)` 门控在 `isBrandNewWorkspace` 检查后
- **效果**：真正的新工作区仍收到模板；用户删除HEARTBEAT.md的现有工作区不再每次会话启动时重新创建
- **测试**：新增2个e2e测试（品牌新工作区创建 / 已存在但缺少文件的工作区不重新创建）
- **提交**：acc511a | **作者**：CornBrother0x | **标签**：agents, size: XS

**🔗 相关链接**：
- PR页面：https://github.com/openclaw/openclaw/pull/19482

---

## 📈 数据洞察

### GitHub 仓库状态（截至2026-03-19）
| 指标 | 数值 |
|------|------|
| ⭐ Stars | 325,141 |
| 👁 Watchers | 325,141 |
| 🍴 Forks | 62,749 |
| 🐛 Open Issues | 14,643 |
| 📦 仓库大小 | 311,032 KB |
| 🗣 语言 | TypeScript |
| 📅 创建时间 | 2025-11-24 |
| 🏷 主题 | ai, assistant, crutacean, molty, openclaw, own-your-data, personal |

### 近期发布频率
- **3月12日**：v2026.3.11-beta.1、v2026.3.11 正式版
- **3月13日**：v2026.3.12 正式版
- **3月14日**：v2026.3.13-beta.1、v2026.3.13-1 Recovery版
- **趋势**：近9天内连续高频发布，开发活跃度高

---

## 💬 社区精选

### 其他活跃PR（未详细介绍）
- **PR #19362**：Discord频道删除时自动清理孤立会话，防止会话存储膨胀（涉及CHANNEL_DELETE事件监听器）
- **PR #18778**：Discord Canvas支持（draft，语音活动功能）
- **PR #12975**：Config Builder重构，与OpenClaw Web UI技术栈对齐

---

## 🔮 值得关注的趋势

1. **安全优先**：Heredoc漏洞修复（GHSA-65rx-fvh6-r4h2）表明项目对安全问题的快速响应
2. **构建优化**：runtime-only构建目标反映了大规模部署需求
3. **Agent能力扩展**：RLM Harness实验性功能代表上下文窗口处理的新方向
4. **快速迭代**：连续5天发布新版本，进入高强度维护期

---

*报告生成时间：2026-03-20 06:09 | 数据来源：GitHub API + openclaw/openclaw仓库*
