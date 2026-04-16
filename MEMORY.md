## 记忆管理原则

- 配置变更后 → 保存到 `memory/YYYY-MM-DD.md`
- 重要决策 → 记录结论和原因
- 发现主人偏好 → 记录到 `USER.md`

## 核心配置（重要）

### TTS（必须Azure TTS，2026-03-22永久保存，2026-03-23修正）
- API Key: `7eDraYD542t0TLbtmJHYGVzvOEp3rx57IWKv7YDikrUSwnzDaBt4JQQJ99CBAC3pKaRXJ3w3AAAYACOGc788`
- 端点: https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1
- 音色: zh-CN-XiaoyiNeural
- 格式: audio-16khz-32kbitrate-mono-mp3
- 区域: East Asia
- ⚠️ 禁止使用OpenClaw内置tts工具，只用Azure TTS API
- ⚠️ SSML中禁止使用prosody rate="+30%"标签（会导致HTTP 400）
- 正确SSML格式：直接放文本，不加prosody标签

### 邮件授权码（全局）
- QQ邮箱: icxhfzuyzbhbbjie

### Tavily API（全局）
- API Key: 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

## 模型配置
- 默认模型: minimax-portal/MiniMax-M2.7-highspeed
- 备用: deepseek/deepseek-chat

## 图片生成配置 (2026-03-21更新)
| 用途 | 方案 | 状态 |
|------|------|------|
| **图片生成（主力）** | Nano Banana Pro (Gemini API) + 本地脚本 | ✅ 已配置 |
| **API Key** | `AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s` | ✅ |
| **脚本路径** | `~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py` | ✅ |
| **安装命令** | `clawhub install nano-banana-pro --workdir ~/.openclaw/workspace` | ✅ |
| **默认分辨率** | 2K | ✅ |

### 图片生成优化官（image_generator）默认模型
- **默认模型**: Nano Banana Pro（Gemini 3.1 Flash Image Preview）
- **命令模板**: `uv run ~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py --prompt "..." --filename "xxx.png" --resolution 2K --api-key "AIzaSyDUXba29bf86c_pjadKWftMH6u30kEpN9s"`
- **编辑模式**: 添加 `--input-image "原图路径"`

## 搜索与翻译配置（2026-03-20锁定）
| 用途 | 方案 | 状态 |
|------|------|------|
| **搜索（主力）** | SerpAPI: `b28c2426b9015470508315f27a6782b552a5a5b39550fbc9b62ff381e67c360f` | ✅ |
| **搜索（备用）** | Tavily API: `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` | ✅ |
| **搜索（最后备选）** | DuckDuckGo（无需Key） | ✅ |
| **翻译** | DeepSeek-Chat: `sk-451f43ffa9764b7e91430e4d39538356` (OpenClaw配置) | ✅ |
| **邮件格式** | 华为邮箱兼容版（无emoji、简化HTML） | ✅ |

### 搜索优先级
1. SerpAPI（主力）
2. Tavily（备用）
3. DuckDuckGo（最后备选）

### 翻译配置
- 使用 DeepSeek-Chat API 翻译英文→中文
- Key 从 OpenClaw 配置读取
- 端点: `https://api.deepseek.com/v1`

## 定时任务
| 任务 | 时间 | 状态 |
|------|------|------|
| 主动惊喜检查 | 每4小时 | ok (2026-03-20新增) |
| OpenClaw每日新闻监控 | 06:00 | ok |
| 高校分队-AI新闻每日简报 | 06:15 | ok |
| 健康长寿科研成果监控 | 07:00 | ok |

### 主动惊喜检查 Cron (2026-03-20新增)
- ID: 66c5d54b-8bec-4d79-9e8c-a21c275715c7
- 功能：扫描 proactive-tracker、recurring-patterns、outcome-journal、Skill更新、WAL检查
- 触发词：每4小时自动执行

## 已安装技能 (2026-03-20更新)
| 技能 | 用途 | 状态 |
|------|------|------|
| scrapling-skill | 网页抓取、动态渲染、Cloudflare绕过 | ✅ 新安装 |
| proactive-agent | 主动思考、WAL协议、记忆维护 | ✅ 已有 |

### 高校分队-AI新闻每日简报 收件人（2026-03-19更新）
| 序号 | 邮箱 |
|------|------|
| 1 | liuwei44259@huawei.com |
| 2 | tiankunyang@huawei.com |
| 3 | qinhongyi2@huawei.com |
| 4 | jiawei18@huawei.com |
| 5 | jiyingguo@huawei.com |
| 6 | linfeng67@huawei.com |
| 7 | lvluling1@huawei.com |
| 8 | suqi1@huawei.com |
| 9 | susha@huawei.com |
| 10 | wangdongxiao@huawei.com |
| 11 | xiongguifang@huawei.com |
| 12 | xushengsheng@huawei.com |
| 13 | zhangqianfeng2@huawei.com |
| 14 | zhangyexing2@huawei.com |
| 15 | 86940135@qq.com |

## 飞书消息发送（2026-03-25）
- **优先使用**：OpenClaw message 工具（如果 bug 修复则用这个）
- **备用方案**：curl 直接调用飞书 API
  - 获取 Token：`POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal`
  - 发图片：先 `POST /im/v1/images` 上传获取 image_key，再发消息
  - API 文档：https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/create

## 待处理问题
- 华为邮箱收邮件偶尔被拦截（由QQ邮箱发送）
- OpenClaw message 工具飞书发送存在设计冲突（card vs media）- 等待插件更新修复

## 老板网站搭建计划
- **自建网站统计（UV/PV）**：方案已记录，等网站搭建后实施
- 文档位置：`memory/2026-03-29-自建Analytics方案.md`

## 网站技能列表更新 (2026-03-29)
- 网站路径：`jiaviswangcai.ai/skills.html`
- 实际安装技能：54个
- 已按分类更新网站技能页面
- 包含：AI技术、运营效率、内容创作、开发工具、竞品市场、系统自动化、日报周报、浏览器自动化

## GitHub提交方式（2026-03-30）
- **默认使用Git命令**提交GitHub，而不是网页操作
- 网站目录：`/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai`
- 常用命令：
  - `git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai status`
  - `git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai add .`
  - `git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai commit -m "描述"`
  - `git -C /Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai push`
- exec allowlist 已添加网站目录的git命令

## 定时任务管理策略（2026-03-31）
- **动态模型继承**：创建 Cron 任务时，**绝不使用** `--model` 参数硬编码绑定模型。让任务继承系统当前全局模型，防止沙箱环境下触发 `LiveSessionModelSwitchError` 导致大面积静默失败。
- **强制失败告警**：核心业务 Cron 任务必须追加 `--failure-alert --failure-alert-after 1`，确保任务失败 1 次即刻触发飞书主动报警。

## 私有知识星图与图谱链接规范 (2026-03-31)
- **图谱构建机制**：目前已建立私有知识星图（GraphRAG）。系统会在每天夜间扫描 Markdown 文件，提取所有的 `[[WikiLink]]` 和 `#标签` 构建实体关联图。
- **强制记录规范**：在写入 `LEARNINGS.md`、`ERRORS.md`、`PROGRESS.md` 等核心日志时，必须主动为核心实体打上方括号链接。例如：遇到网络报错应记录为 `[[报错_ETIMEDOUT]]`，提到某个模型应记录为 `[[Gemini]]`。这样可以让零散的知识点在图谱中自动产生链接，形成网状记忆。

- 2026-03-31: **cron任务务必不绑定模型**，如果绑定特定模型会在模型更替或限流时导致后台定时任务失效挂起。建议解绑系统级cron的模型限制并增加重试与环境检查机制。

## Compaction系统优化 (2026-04-16 11:45)

### 问题分析
学习 OpenClaw 官方文档 https://docs.openclaw.ai/concepts/compaction 后，对比现有系统配置发现以下问题：

| 配置项 | 原值 | 新值 | 原因 |
|--------|------|------|------|
| lossless-claw.contextThreshold | 0.5 | 0.75 | 原值过低(50%)导致过早压缩，75%更合理 |
| lossless-claw.freshTailCount | 12 | 32 | 原值过低，只保护12条消息，容易丢失近期上下文 |
| lossless-claw.incrementalMaxDepth | -1 (无限) | 1 | 无限级联过于激进，限制为1级更安全 |
| agents.defaults.compaction.notifyUser | 未配置 | true | 开启压缩通知，便于观察系统行为 |
| agents.defaults.contextPruning | 未配置 | {mode: "cache-ttl", ttl: "5m"} | 启用会话修剪，减少工具输出膨胀 |

### 关键概念
- **Compaction**: 将旧对话总结成摘要存在transcript中
- **Pruning**: 修剪旧工具输出，不保存，仅内存操作
- **memoryFlush**: 压缩前自动将持久笔记写入磁盘
- **freshTailCount**: 保护最新消息不被压缩

### 参考文档
- https://docs.openclaw.ai/concepts/compaction
- https://docs.openclaw.ai/concepts/session-pruning
- https://docs.openclaw.ai/concepts/memory

## Memory-Search系统优化 (2026-04-16 11:58)

### 文档学习
学习 https://docs.openclaw.ai/concepts/memory-search 后进行以下优化：

### 原有配置
```json
{
  "enabled": true,
  "provider": "gemini",
  "model": "gemini-embedding-2-preview",
  "outputDimensionality": 1536
}
```

### 优化后配置
```json
{
  "enabled": true,
  "provider": "gemini",
  "model": "gemini-embedding-2-preview",
  "outputDimensionality": 1536,
  "query": {
    "hybrid": {
      "temporalDecay": { "enabled": true },
      "mmr": { "enabled": true }
    }
  }
}
```

### 优化说明
| 配置项 | 优化前 | 优化后 | 说明 |
|--------|--------|--------|------|
| query.hybrid.temporalDecay | 未配置 | enabled: true | 启用时间衰减，30天半衰期，最近笔记优先 |
| query.hybrid.mmr | 未配置 | enabled: true | 启用MMR多样性，减少重复结果 |

### 关键概念
- **Vector Search**: 语义相似搜索（"gateway host" 匹配 "运行 OpenClaw 的机器"）
- **BM25 Search**: 关键词精确搜索（ID、错误字符串、配置key）
- **Hybrid Merge**: 两种搜索结果加权合并
- **temporalDecay**: 老笔记逐渐降低权重，MEMORY.md 等常青文件不受影响
- **MMR (Maximum Marginal Relevance)**: 减少冗余结果，确保top结果覆盖不同主题

### 注意事项
- memory-lancedb skill 已禁用（需要OpenAI API）
- 内置 memorySearch 使用 Gemini 嵌入模型
- 如遇CJK文本检索问题，运行: openclaw memory index --force

## memory-lancedb-pro 安装尝试 (2026-04-16 下午)

### 目标
安装 memory-lancedb-pro 插件以使用本地 Ollama embeddings (nomic-embed-text)

### 尝试过程
1. 安装 memory-lancedb-pro 到 ~/.openclaw/extensions/
2. 配置 embedding: baseUrl=http://localhost:11434/v1, model=nomic-embed-text
3. 多次重启网关，但插件始终无法被 OpenClaw 发现

### 问题
OpenClaw 状态显示：
```
plugins.allow is empty; discovered non-bundled plugins may auto-load: lossless-claw, openclaw-web-search, openclaw-weixin
```
memory-lancedb-pro 不在发现列表中，即使文件存在于 ~/.openclaw/extensions/memory-lancedb-pro/

### 结论（2026-04-16 确认）
**用户决定：放弃 memory-lancedb-pro，继续使用内置 memorySearch**
- memory-wiki 已启用（2026-04-16）
- 继续使用 QMD + memorySearch (temporalDecay + MMR)
- 这是最终决策，不再尝试 memory-lancedb 系列插件

## memory-wiki 启用 (2026-04-16)

### 配置
- vaultMode: **bridge**
- vault: ~/.openclaw/wiki/main
- renderMode: **obsidian**
- Obsidian CLI: 可选，未安装
- Bridge: enabled (0 exported artifacts - 因为 QMD 未导出 public artifacts)
- search: shared corpus=all

### Vault 结构
- entities/ - 实体
- concepts/ - 概念
- sources/ - 来源
- syntheses/ - 综合
- reports/ - 仪表板报告
  - claim-health.md
  - contradictions.md
  - low-confidence.md
  - open-questions.md
  - stale-pages.md

### 注意事项
- Obsidian CLI 未安装（可选）
- Bridge mode 等待 QMD 导出 artifacts 后自动导入
- 或可切换为 isolated mode 作为独立知识库

## Codex 集成完成 (2026-04-16)

### 配置状态
- Codex plugin: ✅ 已配置并连接成功
- 可用模型: gpt-5.4, gpt-5.4-mini, gpt-5.3-codex, gpt-5.2-codex, gpt-5.1-codex-max, gpt-5.1-codex-mini
- MCP servers: 2个已连接
- Skills: 1个可用

### 使用方式
- `/model codex` - 切换到 Codex (gpt-5.4)
- `/model codex/gpt-5.4-mini` - 使用 mini 版本
- `/codex status` - 查看连接状态

### 验证结果
通过 /codex status 命令验证，app-server connected，所有模型可用。
