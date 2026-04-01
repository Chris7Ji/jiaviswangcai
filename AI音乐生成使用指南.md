# AI音乐生成技能使用指南

## 🎵 功能概述
使用AI生成高质量音乐，支持完整歌曲（含人声）、纯音乐、自定义歌词等多种模式。

## 📦 已安装技能

### 1. evolink-music (推荐)
- **基于**: Suno v4/v4.5/v5
- **特点**: 专业级音乐生成，支持完整歌曲
- **质量**: 录音室级别 (v5)
- **时长**: 最长240秒

### 2. music-generation
- **支持平台**: Suno, Udio, Stable Audio, MusicGen等
- **特点**: 多平台选择，适合不同场景

## 🔧 配置要求

### 必需配置
```bash
# 设置环境变量
export EVOLINK_API_KEY=your_api_key_here
```

### 获取API Key
1. 访问 https://evolink.ai
2. 注册账号
3. 进入 Dashboard → API Keys
4. 创建新的API Key

## 💡 使用方法

### 简单模式（推荐）
直接描述你想要的音乐：
```
生成一首关于[主题]的[风格]歌曲
```

**示例**:
- "生成一首关于春天的流行歌曲"
- "生成一段轻音乐，适合冥想，时长3分钟"
- "生成一首励志的摇滚歌曲，男声"

### 自定义模式
提供详细参数：
```
生成歌曲：
- 歌词：[你的歌词]
- 风格：流行，快节奏，120bpm
- 标题：春天的故事
- 人声：女声
```

### 纯音乐
```
生成一段背景音乐：
- 风格：古典，钢琴
- 情绪：宁静，优雅
- 时长：180秒
- 无人声
```

## 🎼 音乐模型选择

| 模型 | 质量 | 时长 | 适用场景 | 成本 |
|------|------|------|----------|------|
| suno-v4 | ⭐⭐⭐ | 120s | 日常创作 | 低 |
| suno-v4.5 | ⭐⭐⭐⭐ | 240s | 风格控制 | 中 |
| suno-v5 | ⭐⭐⭐⭐⭐ | 240s | 专业制作 | 高 |

**建议**:
- 快速测试 → v4
- 平衡质量 → v4.5
- 专业作品 → v5

## 🎨 风格标签参考

### 流派 (Genre)
- pop, rock, hip-hop, jazz, classical
- electronic, edm, lo-fi, ambient
- folk, country, blues, metal

### 情绪 (Mood)
- upbeat, happy, energetic, cheerful
- melancholic, sad, emotional, nostalgic
- calm, peaceful, relaxing, meditative
- aggressive, intense, powerful, dramatic

### 乐器 (Instruments)
- piano, guitar, violin, cello
- drums, bass, synth, strings
- flute, saxophone, trumpet

### 人声 (Vocals)
- male vocals, female vocals
- choir, rap, spoken word
- instrumental (无人声)

### 节奏 (Tempo)
- slow, mid-tempo, fast
- 60bpm, 120bpm, 140bpm

## 📝 歌词格式（自定义模式）

使用标准歌曲结构标签：
```
[Verse]
第一段歌词内容

[Chorus]
副歌歌词内容

[Verse]
第二段歌词内容

[Chorus]
副歌歌词内容

[Bridge]
桥段歌词内容

[Outro]
结尾歌词内容
```

## 🎬 使用场景

### 1. 视频背景音乐
```
生成一段背景音乐：
- 风格：电子，轻快
- 时长：与视频匹配
- 情绪：积极，现代
- 无人声
```

### 2. 播客片头/片尾
```
生成一段15秒的片头音乐：
- 风格：现代，专业
- 有节奏感
- 无人声
```

### 3. 个人创作
```
生成一首关于[个人经历]的歌曲：
- 风格：民谣，温暖
- 人声：男声
- 情绪：怀旧，温柔
```

### 4. 商业项目
```
生成一段适合广告的音乐：
- 风格：流行，活力
- 时长：30秒
- 情绪：积极，吸引人
```

## ⚠️ 注意事项

### 版权问题
- **个人使用**: 所有生成音乐均可使用
- **商业使用**: 需查看各平台最新许可条款
- **版权归属**: 通常归用户所有，但需确认平台政策

### 技术限制
- **生成时间**: 通常30-120秒
- **文件有效期**: 链接24小时有效，需及时下载
- **配额限制**: 根据API套餐有不同限制

### 最佳实践
1. **先测试短片段** - 确认风格后再生成长版本
2. **具体描述** - "钢琴独奏"比"音乐"效果更好
3. **多次尝试** - 第一次生成可能不完美，多试几次
4. **保存文件** - 生成后立即下载，链接会过期

## 🔗 相关资源

- **Evolink官网**: https://evolink.ai
- **Suno官网**: https://suno.ai
- **API文档**: `/Users/jiyingguo/.openclaw/workspace/skills/evolink-music/references/music-api-params.md`

## 📊 故障排除

### API Key无效
```
错误: 401 Unauthorized
解决: 检查EVOLINK_API_KEY是否正确设置
```

### 余额不足
```
错误: 402 Payment Required
解决: 在evolink.ai充值
```

### 生成失败
```
错误: generation_failed_no_content
解决: 修改提示词，简化描述后重试
```

### 内容违规
```
错误: content_policy_violation
解决: 修改歌词或描述，避免敏感内容
```

---

**配置时间**: 2026-03-17  
**最后更新**: 2026-03-17  
**状态**: ✅ 已安装，⚠️ 需配置API Key
