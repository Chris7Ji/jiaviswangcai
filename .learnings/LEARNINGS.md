# 学习记录
# 注意: 详细记录已分类存储到by-topic/目录
# 本文件仅保留最新5条记录和索引

## 最新学习记录（最近5条）

## 2026-03-23 23:19:00
**ID**: learn-011
**优先级**: CRITICAL
**类别**: azure_tts
**摘要**: Azure TTS 正确用法 - 禁止使用 prosody rate 标签
**场景**: 老板测试 Azure TTS，发现 HTTP 400 错误
**错误原因**: SSML 中使用 `<prosody rate="+30%">` 标签，eastasia 区域不支持此参数
**正确做法**:
1. 不使用 prosody 标签，直接放文本内容
2. 端点: https://eastasia.tts.speech.microsoft.com/cognitiveservices/v1
3. 音色: zh-CN-XiaoyiNeural
4. 格式: audio-16khz-32kbitrate-mono-mp3
**正确 SSML 模板**:
```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='zh-CN'>
    <voice name='zh-CN-XiaoyiNeural'>
        要转换的文本内容
    </voice>
</speak>
```
**状态**: ✅ 已验证并记录

## 2026-03-10 23:24:00
**ID**: learn-010
**优先级**: CRITICAL
**类别**: system_optimization
**摘要**: 优化记忆检索效率，解决响应慢问题
**场景**: 老板反馈响应有点慢，要求优化记忆系统
**优化措施**:
1. 创建关键词索引 INDEX.md - 快速定位信息
2. 分类存储学习记录 by-topic/*.md - 减少单文件大小
3. 建立快速响应策略 - 避免慢速操作
4. 预加载核心文件 - 减少读取延迟
**相关文件**:
- INDEX.md - 关键词索引
- by-topic/email.md - 邮件相关
- by-topic/model-config.md - 模型配置
- by-topic/skills.md - 技能安装
- by-topic/cron.md - 定时任务
- PERFORMANCE.md - 性能优化配置
**状态**: ✅ 已实施

## 2026-03-10 23:18:00
**ID**: learn-002
**优先级**: CRITICAL
**类别**: identity
**摘要**: 明确与老板（季）的关系和工作原则
**详情**: 见SOUL.md#L28-35
**状态**: ✅ 已记录

## 2026-03-10 14:00:00
**ID**: learn-001
**优先级**: MEDIUM
**类别**: best_practice
**摘要**: OpenClaw gateway restart 命令不需要sudo权限
**详情**: 见by-topic/cron.md
**状态**: ✅ 已验证

---

## 📚 完整学习记录索引

按主题分类存储:
- **邮件相关**: by-topic/email.md
- **模型配置**: by-topic/model-config.md
- **技能安装**: by-topic/skills.md
- **定时任务**: by-topic/cron.md

## 🔍 快速查找指南

1. **找关键词** → 查 INDEX.md
2. **找邮件配置** → 读 by-topic/email.md
3. **找模型信息** → 读 by-topic/model-config.md
4. **找技能信息** → 读 by-topic/skills.md
5. **找定时任务** → 读 by-topic/cron.md
6. **找性能优化** → 读 PERFORMANCE.md

---
**维护说明**: 本文件只保留最近5条记录，旧记录自动归档到by-topic/或archive/