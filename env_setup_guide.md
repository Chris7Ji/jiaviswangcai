# 📋 定时任务环境变量配置指南

## 🔑 必需的环境变量

### 1. TAVILY_API_KEY (搜索API)
**用途**: 所有新闻搜索任务都需要
**获取地址**: https://app.tavily.com/
**配置方法**:
```bash
# 临时设置
export TAVILY_API_KEY=your_api_key_here

# 永久设置（添加到 ~/.zshrc）
echo 'export TAVILY_API_KEY="your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 2. GEMINI_API_KEY (可选，用于摘要)
**用途**: 使用Gemini模型进行内容摘要
**获取地址**: https://makersuite.google.com/app/apikey
**配置方法**:
```bash
export GEMINI_API_KEY=your_api_key_here
```

## 📊 定时任务配置详情

### 任务列表
| 任务名称 | 执行时间 | 内容要求 |
|----------|----------|----------|
| **OpenClaw每日新闻监控** | 06:00 | OpenClaw官方更新、社区动态 |
| **AI新闻每日摘要** | 06:30 | 全球AI新闻，严格时效性 |
| **健康长寿科研成果监控** | 07:00 | 健康长寿最新研究成果 |
| **华为昇腾新闻监控** | 07:30 | 昇腾生态最新动态 |

### 输出文件位置
所有报告生成在: `/Users/jiyingguo/.openclaw/workspace/news_summaries/`

### 日志文件
执行日志在相同目录，格式: `cron_execution_YYYY-MM-DD*.log`

## 🛠️ 故障排除

### 常见问题
1. **搜索失败**: 检查TAVILY_API_KEY是否正确设置
2. **任务未执行**: 检查openclaw cron list状态
3. **报告未生成**: 检查日志文件查看具体错误
4. **格式问题**: 检查消息模板和agent配置

### 测试方法
```bash
# 测试环境变量
echo $TAVILY_API_KEY

# 测试单个任务
openclaw cron run <task_id>

# 查看任务日志
ls -la /Users/jiyingguo/.openclaw/workspace/news_summaries/*.log
```

## 🔄 手动执行命令

如果自动任务失败，可以手动执行：

```bash
# AI新闻日报
openclaw cron run 0bd3de5c-a4f9-4774-9511-75f344ba114c

# 健康长寿日报
openclaw cron run <health_task_id>

# OpenClaw日报
openclaw cron run 5aa186d0-d623-41aa-bef3-352aec56eb20

# 昇腾AI日报
openclaw cron run a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## 📞 支持
如有问题，检查:
1. 环境变量配置
2. API密钥有效性
3. 网络连接
4. 磁盘空间和权限

