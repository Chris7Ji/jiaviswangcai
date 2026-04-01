# AI视频制作技能指南

## 概述
支持37个AI视频模型的视频生成技能，包括Sora、Kling、Veo 3等顶级模型。

## 安装

### 方式1：npx安装（需要--force）
```bash
npx clawhub@latest install evolink-video --force
```

### 方式2：手动配置
由于技能被标记为可疑，可以：
1. 下载技能代码审查
2. 确认安全后手动安装
3. 或直接使用Evolink API

## 支持的模型（37个）

### 顶级模型
- **Sora** - OpenAI，高质量视频生成
- **Kling** - 快手，国内领先
- **Veo 3** - Google，最新一代
- **Seedance** - 字节跳动
- **Hailuo** - 海螺视频
- **WAN** - 阿里
- **Grok** - xAI

### 其他模型
共37个模型，覆盖各种风格和用途。

## 核心功能

### 1. 文生视频（Text-to-Video）
```bash
# 输入文字描述，生成视频
prompt: "一只猫在草地上玩耍，阳光明媚"
```

### 2. 图生视频（Image-to-Video）
```bash
# 上传图片，生成动态视频
input_image: "cat.jpg"
prompt: "让猫动起来，摇尾巴"
```

### 3. 首尾帧视频
```bash
# 提供开始和结束帧，AI生成中间过渡
first_frame: "start.jpg"
last_frame: "end.jpg"
```

### 4. 自动配音
```bash
# 视频自动生成配音
voice: "zh-CN-XiaoxiaoNeural"
```

## 配置要求

### 1. API Key
需要Evolink API Key：
```bash
export EVOLINK_API_KEY="your-api-key"
```

获取方式：
1. 访问 https://evolink.ai
2. 注册账号
3. 获取API Key

### 2. 环境变量
```bash
# 添加到 ~/.zshrc
export EVOLINK_API_KEY="your-key"
```

## 使用示例

### 文生视频
```python
# 生成视频
result = evolink_video.generate(
    prompt="一只可爱的金毛犬在海边奔跑",
    model="sora",
    duration=10,  # 秒
    resolution="1080p"
)
```

### 图生视频
```python
# 图片转视频
result = evolink_video.image_to_video(
    image_path="photo.jpg",
    prompt="让人物微笑，背景动起来",
    model="kling"
)
```

### 首尾帧视频
```python
# 首尾帧生成
result = evolink_video.frame_interpolation(
    first_frame="frame1.jpg",
    last_frame="frame2.jpg",
    duration=5
)
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| prompt | 视频描述 | "猫咪玩耍" |
| model | AI模型 | "sora", "kling", "veo3" |
| duration | 时长（秒） | 10 |
| resolution | 分辨率 | "1080p", "4k" |
| style | 风格 | "cinematic", "anime" |

## 当前状态

⚠️ **技能安装受限** - 被标记为可疑，需要--force或手动审查

**替代方案**:
1. **直接使用Evolink平台**: https://evolink.ai
2. **使用单个模型平台**:
   - Sora: https://openai.com/sora
   - Kling: https://klingai.com
   - Veo: Google AI
3. **其他视频工具**:
   - Runway: https://runwayml.com
   - Pika: https://pika.art
   - HeyGen: https://heygen.com

## 建议

由于技能安装受限，建议：
1. 直接使用Evolink平台生成视频
2. 或申请API Key后手动调用
3. 等待技能更新解决安全问题

---

**状态**: 安装受限 ⚠️
**替代方案**: 直接使用Evolink平台或其他AI视频工具
