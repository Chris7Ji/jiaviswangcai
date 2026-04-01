# Skills 安装与启动状态报告
# 生成时间: 2026-03-14 03:18

## 📊 总体概况

| 类别 | 数量 |
|------|------|
| **总安装技能** | 26个 |
| **已启动运行** | 8个 |
| **已安装待配置** | 2个 |
| **需要CLI安装** | 3个 |

---

## ✅ 已启动运行的技能 (8个)

| # | 技能名称 | 版本 | 状态 | 说明 |
|---|---------|------|------|------|
| 1 | **ClawSec** | 1.0.0 | 🟢 运行中 | PID 7006, 系统级监控 |
| 2 | **Proactive Agent** | 3.1.0 | 🟢 已启用 | 完全启用v3.1.0架构 |
| 3 | **Self-Improving Agent** | 3.0.0 | 🟢 运行中 | 3个记忆文件活跃 |
| 4 | **Summarize** | 1.0.0 | 🟢 就绪 | CLI v0.10.0, API已配置 |
| 5 | **Gog** | 1.0.0 | 🟢 就绪 | CLI已安装, 待Google API配置 |
| 6 | **Stock Monitor** | 1.3.0 | 🟢 运行中 | 股票监控活跃 |
| 7 | **Bilibili Hot Monitor** | 1.0.21 | 🟢 运行中 | B站热门监控活跃 |
| 8 | **Local Whisper** | 1.0.0 | 🟢 就绪 | CLI已安装, 本地语音识别 |

---

## 📦 已安装但未启动的技能 (18个)

### 框架/架构类
- **find-skills-robin** 0.1.0 - 技能发现助手
- **debug-checklist** 1.0.0 - 调试检查清单

### 搜索类
- **multi-search-engine** 2.0.1 - 多搜索引擎集成
- **duckduckgo-search** - DuckDuckGo搜索
- **serpapi** - SerpAPI搜索
- **tavily-search** - Tavily AI搜索

### 内容生成类
- **nano-banana-pro** 1.0.1 - Nano Banana Pro图像生成
- **nano-banana-2** 0.1.1 - Nano Banana 2图像生成

### 办公/生产力类
- **office** 1.0.0 - Office办公套件
- **office-xyz** 1.0.0 - 虚拟办公平台
- **obsidian-ontology-sync** 1.0.1 - Obsidian知识库同步

### 开发工具类
- **github** 1.0.0 - GitHub操作

### 娱乐类
- **games** 1.0.0 - 游戏系统

### 自定义脚本
- **email-manager** - 邮件管理脚本
- **feishu-calendar** - 飞书日历管理
- **self-improving** - 自我改进系统目录

---

## ⚙️ 技能详细状态

### 🔒 ClawSec (安全监控)
- **状态**: 🟢 运行中
- **PID**: 7006
- **启动时间**: 2026-03-14 02:55
- **监控模式**: Tunnel (HTTP)
- **自动启动**: ✅ 系统级配置完成
- **日志**: /tmp/clawsec/

### 🦞 Proactive Agent (主动式智能体)
- **状态**: 🟢 已启用
- **版本**: v3.1.0
- **核心文件**: 
  - SESSION-STATE.md ✅
  - working-buffer.md ✅
  - AGENTS.md (已更新) ✅
  - SOUL.md (已更新) ✅

### 🧠 Self-Improving Agent (自我改进)
- **状态**: 🟢 运行中
- **记忆文件**: 3个
- **位置**: ~/self-improving/
- **活跃记录**: LEARNINGS.md, ERRORS.md, index.md

### 📝 Summarize (内容摘要)
- **状态**: 🟢 就绪
- **CLI版本**: 0.10.0
- **API Key**: ✅ Gemini已配置
- **测试状态**: ✅ 已通过
- **支持格式**: URL, PDF, YouTube, 本地文件

### 📧 Gog (Google Workspace)
- **状态**: 🟡 就绪但未配置
- **CLI**: 已安装
- **OAuth**: ❌ 待配置
- **说明**: 需要Google API凭证才能使用

### 📈 Stock Monitor (股票监控)
- **状态**: 🟢 运行中
- **版本**: 1.3.0
- **功能**: 股票分析、市场监控

### 📺 Bilibili Hot Monitor (B站监控)
- **状态**: 🟢 运行中
- **版本**: 1.0.21
- **功能**: B站热门视频日报

### 🎤 Local Whisper (语音识别)
- **状态**: 🟢 就绪
- **CLI**: 已安装
- **功能**: 本地语音转文字

---

## 🔧 需要关注的技能

| 技能 | 问题 | 建议操作 |
|------|------|---------|
| **Gog** | OAuth未配置 | 配置Google API凭证 |
| **YouTube视频处理** | 处理时间长 | 安装yt-dlp加速 |

---

## 📋 技能启动命令参考

```bash
# ClawSec
python3 /tmp/clawsec-monitor.py status
python3 /tmp/clawsec-monitor.py start --no-mitm

# Summarize
summarize "URL" --length medium
summarize "/path/to/file.pdf"

# Gog (需先配置OAuth)
gog auth credentials /path/to/client_secret.json
gog auth add your-email@gmail.com --services gmail,calendar,drive

# Local Whisper
whisper /path/to/audio.mp3 --model medium
```

---

*报告生成时间: 2026-03-14 03:18*
*Proactive Agent v3.1.0 监控中*
