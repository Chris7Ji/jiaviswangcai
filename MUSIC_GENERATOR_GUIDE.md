# AI音乐生成技能指南

## 概述
根据结构化作曲计划（Composition Plan）生成高质量音频文件。

## 安装

### 方式1：通过npx安装（推荐）
```bash
npx clawhub@latest install music-generator
```

### 方式2：从GitHub克隆
```bash
git clone https://github.com/openclaw/skills.git
cd skills/skills/wells1137/music-generator
```

## 核心功能

### 1. 作曲计划驱动
- 基于JSON格式的Composition Plan生成音乐
- 严格匹配设计规格

### 2. 精确时长控制
- 输出音频时长精确匹配目标长度
- 容差：±0.5秒

### 3. 质量验证
- 自动生成后验证质量
- 不合格自动重试
- 确保输出符合标准

## 工作流程

### 步骤1：创建Composition Plan
```json
{
  "title": "背景音乐",
  "duration_ms": 30000,
  "style": "electronic",
  "mood": "upbeat",
  "instruments": ["synth", "drums", "bass"],
  "tempo": 120,
  "output_format": "mp3"
}
```

### 步骤2：配置生成参数
- **duration_ms**: 总时长（精确匹配）
- **output_format**: WAV（制作）/ MP3（交付）
- **instrumental**: true（纯音乐，无 vocals）

### 步骤3：执行生成
```bash
# 调用音乐生成API
# 传入Composition Plan和配置参数
```

### 步骤4：质量验证
检查项目：
- ✅ 时长匹配（±0.5秒）
- ✅ 风格一致性
- ✅ 音频质量
- ✅ 避免负面风格

## 使用场景

### ✅ 适合使用
- 已有完整的Composition Plan
- 需要生成最终音频文件
- 需要精确时长控制

### ❌ 避免使用
- 只有设计想法，没有具体计划
- 不需要生成音频，只需要设计
- 对时长没有精确要求

## 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| duration_ms | 总时长（毫秒） | 30000 |
| output_format | 输出格式 | "mp3" / "wav" |
| instrumental | 是否纯音乐 | true |
| style | 音乐风格 | "electronic" |
| mood | 情绪 | "upbeat" |

## 质量验证标准

1. **时长匹配**: 实际时长与目标时长误差 ≤ 0.5秒
2. **风格一致性**: 符合positive_global_styles，避免negative_global_styles
3. **音频质量**: 无杂音、无失真
4. **完整性**: 开头结尾自然，不突兀

## 当前状态

⚠️ **技能安装中** - 正在从GitHub克隆

**替代方案**:
- 使用在线AI音乐工具（Suno、Udio等）
- 等待技能安装完成
- 手动创建Composition Plan后批量生成

## 相关工具

- **Suno**: https://suno.ai
- **Udio**: https://udio.com
- **AIVA**: https://aiva.ai

---

**状态**: 安装中 ⏳
**预计完成**: 2-5分钟
