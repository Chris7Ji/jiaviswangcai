# Summarize 使用指南
# 创建时间: 2026-03-14

## 快速开始

### 1. 配置 API Key（必需）

在使用 summarize 之前，需要配置至少一个 API Key：

```bash
# 推荐：Google Gemini（免费额度充足）
export GEMINI_API_KEY="your_gemini_api_key_here"

# 或者使用其他提供商
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
export XAI_API_KEY="your_xai_key"
```

**获取 Gemini API Key**:
1. 访问 https://ai.google.dev/
2. 登录 Google 账号
3. 创建 API Key
4. 复制并设置环境变量

### 2. 基本用法

#### 摘要网页
```bash
# 简短摘要
summarize "https://example.com" --length short

# 中等长度摘要
summarize "https://example.com" --length medium

# 详细摘要
summarize "https://example.com" --length long

# 超长摘要
summarize "https://example.com" --length xl
```

#### 摘要本地文件
```bash
# 文本文件
summarize "/path/to/document.txt"

# PDF 文件
summarize "/path/to/document.pdf"

# 指定长度
summarize "/path/to/file.txt" --length medium
```

#### 摘要 YouTube 视频
```bash
# 自动获取字幕
summarize "https://youtu.be/VIDEO_ID" --youtube auto

# 使用 yt-dlp 获取字幕
summarize "https://youtu.be/VIDEO_ID" --youtube yt-dlp

# 详细摘要
summarize "https://youtu.be/VIDEO_ID" --youtube auto --length long
```

### 3. 高级选项

```bash
# JSON 格式输出（便于程序处理）
summarize "URL" --json

# 仅提取内容（不生成摘要）
summarize "URL" --extract-only

# 设置最大输出 token 数
summarize "URL" --max-output-tokens 2000

# 指定模型
summarize "URL" --model google/gemini-3-flash-preview
summarize "URL" --model openai/gpt-4

# 使用 Firecrawl 处理被屏蔽的网站
summarize "URL" --firecrawl always
```

### 4. 视频处理（YouTube）

```bash
# 提取视频中的幻灯片
summarize "https://youtu.be/xxx" --slides --slides-max 10

# 包含时间戳
summarize "https://youtu.be/xxx" --youtube auto --timestamps

# 视频理解模式（分析视频内容而非仅字幕）
summarize "https://youtu.be/xxx" --video-mode understand
```

### 5. 配置文件

创建配置文件 `~/.summarize/config.json`：

```json
{
  "model": "google/gemini-3-flash-preview",
  "length": "medium",
  "max-output-tokens": 1000
}
```

### 6. 常用场景示例

#### 场景1: 快速了解新闻文章
```bash
summarize "https://news.example.com/article" --length short
```

#### 场景2: 深入学习技术文档
```bash
summarize "https://docs.example.com/guide" --length long --max-output-tokens 2000
```

#### 场景3: 总结会议录音
```bash
summarize "/path/to/meeting.mp3" --transcriber whisper --length medium
```

#### 场景4: 批量处理多个 URL
```bash
for url in $(cat urls.txt); do
    summarize "$url" --json >> summaries.jsonl
done
```

### 7. 故障排除

**问题**: "No API key found"
- **解决**: 设置 `GEMINI_API_KEY` 或其他提供商的 API Key

**问题**: "Failed to fetch URL"
- **解决**: 使用 `--firecrawl always` 绕过反爬虫

**问题**: YouTube 字幕获取失败
- **解决**: 安装 yt-dlp: `brew install yt-dlp`

**问题**: 中文内容乱码
- **解决**: 确保终端使用 UTF-8 编码

### 8. 最佳实践

1. **选择合适的模型**: Gemini Flash 速度快且便宜，GPT-4 质量更高
2. **调整长度参数**: short 适合快速浏览，long 适合深入学习
3. **使用 JSON 输出**: 便于后续程序化处理
4. **设置环境变量**: 将 API Key 添加到 `~/.zshrc` 避免重复输入

---

## 当前状态

- ✅ Summarize CLI: 已安装 (v0.10.0)
- ✅ Summarize Skill: 已安装 (v1.0.0)
- ⚠️ API Key: 未配置（需要设置 GEMINI_API_KEY 或其他）

## 下一步

1. 获取 Gemini API Key
2. 设置环境变量
3. 测试实际 URL 摘要
