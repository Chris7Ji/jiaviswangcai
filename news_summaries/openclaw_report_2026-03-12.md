# OpenClaw 每日新闻报告
**报告日期**: 2026年3月12日（周四）  
**数据来源**: GitHub Releases、官方文档、ClawHub  
**新闻数量**: 8条高质量新闻

---

## 📢 最新发布

### 1. OpenClaw v2026.3.9 正式发布（2025年3月9日）
**来源**: GitHub Releases (官方)  
**摘要**: 最新稳定版发布，带来多项重要功能更新和修复。

**主要更新内容**:
- **CLI备份功能**: 新增 `openclaw backup create` 和 `openclaw backup verify` 命令，支持本地状态归档，包含 `--only-config` 和 `--no-include-workspace` 选项
- **Talk模式增强**: 新增 `talk.silenceTimeoutMs` 配置，可自定义语音输入自动发送前的静音等待时间
- **TUI改进**: 在配置好的Agent工作区内启动时自动推断当前Agent
- **Brave搜索优化**: 新增 `tools.web.search.brave.mode: "llm-context"` 选项，支持Brave的LLM Context端点
- **ACP溯源**: 新增可选的ACP入口溯源元数据和可见收据注入功能 (`openclaw acp --provenance`)

**修复内容**:
- macOS启动代理重启问题修复
- Telegram DM路由去重修复
- Matrix DM路由安全回退增强
- Feishu插件引导流程优化

---

## 🔧 技术特性

### 2. 多Agent路由系统深度解析
**来源**: OpenClaw官方文档  
**摘要**: OpenClaw支持在同一Gateway中运行多个完全隔离的Agent。

**核心概念**:
- 每个Agent拥有独立的 **Workspace**（文件、配置、人格规则）
- 独立的 **State目录** (`agentDir`) 用于认证配置和模型注册
- 独立的 **Session存储** 位于 `~/.openclaw/agents/<agentId>/sessions`
- 认证配置文件按Agent隔离，避免冲突

**使用场景**:
- 工作Agent与个人Agent分离
- 不同项目使用不同Agent配置
- 多账号多身份管理

---

### 3. Canvas可视化工作空间详解
**来源**: OpenClaw官方文档  
**摘要**: macOS应用内置的Agent控制Canvas面板，基于WKWebView构建。

**功能特性**:
- 无边框可调整大小面板，锚定在菜单栏附近
- 支持HTML/CSS/JS和A2UI渲染
- 本地文件通过 `openclaw-canvas://` 协议访问
- 支持从Canvas触发Agent运行（通过deep link）

**A2UI支持**:
- 当前支持A2UI v0.8协议
- 支持 `beginRendering`, `surfaceUpdate`, `dataModelUpdate`, `deleteSurface` 命令
- 可通过CLI推送JSONL格式的UI更新

---

### 4. 浏览器自动化工具增强
**来源**: OpenClaw官方文档  
**摘要**: OpenClaw托管浏览器提供隔离的Agent专用浏览环境。

**核心功能**:
- **隔离配置**: 独立的 `openclaw` 浏览器配置文件（橙色主题）
- **多配置文件支持**: 支持 `openclaw`, `work`, `remote` 等多个配置文件
- **SSRF保护**: 内置SSRF防护策略，可配置私有网络访问权限
- **确定性控制**: 标签页列表/打开/聚焦/关闭，Agent动作（点击/输入/拖拽）

**配置亮点**:
- 默认浏览器端口基于Gateway端口派生（默认18791）
- 支持远程CDP连接（用于WSL2等场景）
- 可配置无头模式、沙箱禁用等选项

---

## 🛠️ 开发工具

### 5. Skill系统与ClawHub生态
**来源**: OpenClaw官方文档  
**摘要**: OpenClaw使用AgentSkills兼容的Skill文件夹来扩展Agent能力。

**Skill加载优先级**:
1. **Workspace Skills**: `<workspace>/skills`（最高优先级）
2. **本地Skills**: `~/.openclaw/skills`
3. **捆绑Skills**: 随安装包提供（最低优先级）

**ClawHub技能市场**:
- 官方Skill注册表: https://clawhub.com
- 支持 `clawhub install <skill-slug>` 安装
- 支持 `clawhub update --all` 批量更新
- 支持 `clawhub sync --all` 同步

**安全提示**:
- 第三方Skill视为不可信代码，启用前请阅读
- 敏感信息通过 `env` 和 `apiKey` 注入，不进入Prompt和日志

---

### 6. 备份与恢复功能上线
**来源**: GitHub Release Notes  
**摘要**: v2026.3.9版本引入完整的本地备份解决方案。

**功能详情**:
```bash
# 创建备份
openclaw backup create

# 仅备份配置
openclaw backup create --only-config

# 排除工作空间
openclaw backup create --no-include-workspace

# 验证备份完整性
openclaw backup verify
```

**备份内容**:
- 配置文件 (`openclaw.json`)
- 工作空间文件和Skill
- Agent状态和Session数据
- 认证配置文件

---

## 📱 平台支持

### 7. Android应用权限精简
**来源**: GitHub Release Notes  
**摘要**: 为符合Google Play政策，Android应用移除了多项敏感权限。

**变更内容**:
- 移除自更新功能
- 移除后台位置权限
- 移除屏幕录制功能
- 移除后台麦克风捕获
- 前台服务精简为仅 `dataSync`
- 清理遗留的 `location.enabledMode=always` 配置迁移

**影响**: 用户需要通过应用商店更新，无法使用后台录音和屏幕录制功能。

---

### 8. 飞书(Feishu)集成优化
**来源**: GitHub Release Notes  
**摘要**: 飞书频道插件引导流程得到改进。

**修复内容**:
- 修复安装频道插件后重复提示下载飞书的问题
- 在安装成功后清除短生命周期插件发现缓存
- 优化插件注册表重载流程

**使用提示**:
- 飞书是OpenClaw支持的企业级通讯平台之一
- 支持DM（私聊）和群聊两种模式
- 可配置mention规则和允许列表

---

## 📊 总结

| 类别 | 数量 | 亮点 |
|------|------|------|
| 新功能 | 4项 | 备份系统、Talk模式增强、ACP溯源、Brave搜索优化 |
| 修复改进 | 4项 | Android权限、Telegram路由、Matrix路由、Feishu引导 |
| 文档更新 | 3篇 | 多Agent路由、Canvas、浏览器工具 |

**推荐行动**:
1. 建议升级到 v2026.3.9 以获得备份功能和最新修复
2. 多Agent用户可探索新的路由绑定功能
3. 开发者可关注ClawHub上的新Skill发布

---

*报告由 OpenClaw 每日新闻监控自动生成*  
*数据来源: GitHub, docs.openclaw.ai, clawhub.com*
