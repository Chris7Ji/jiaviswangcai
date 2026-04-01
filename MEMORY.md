## 记忆管理原则

- 配置变更后 → 保存到 `memory/YYYY-MM-DD.md`
- 重要决策 → 记录结论和原因
- 发现主人偏好 → 记录到 `USER.md`

## 核心配置（重要）

### TTS（必须Azure TTS，2026-03-22永久保存，2026-03-23修正）
- API Key: `1C9HVfo8CWdYWU5x6n16fQjr0bnjWCr4MYRuMS1B3Ojd9LNEIbkKJQQJ99CBAC3pKaRXJ3w3AAAYACOGZ07P`
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
