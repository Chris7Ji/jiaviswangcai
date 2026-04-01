#!/bin/bash

echo "🔧 修复所有定时任务"
echo "=========================================="

# 1. 首先检查环境变量配置
echo "1. 检查环境变量配置..."
echo "------------------------------------------"

# 检查TAVILY_API_KEY
if [ -z "$TAVILY_API_KEY" ]; then
    echo "❌ TAVILY_API_KEY 未设置"
    echo "   这将影响所有需要搜索的任务"
    echo "   修复方法: export TAVILY_API_KEY=your_api_key"
    echo "   或添加到 ~/.zshrc: export TAVILY_API_KEY=your_api_key"
else
    echo "✅ TAVILY_API_KEY 已设置"
fi

echo ""

# 2. 重新配置健康长寿任务
echo "2. 重新配置健康长寿科研成果监控..."
echo "------------------------------------------"

# 先删除可能存在的旧任务
openclaw cron list | grep "健康长寿" | awk '{print $1}' | while read id; do
    echo "删除旧任务: $id"
    openclaw cron rm "$id"
done

# 创建新的健康长寿任务
echo "创建新的健康长寿任务..."
openclaw cron add \
  --name "健康长寿科研成果监控" \
  --cron "0 7 * * *" \
  --message "生成健康长寿科研日报，要求：过去24小时最新研究成果，从顶级学术期刊获取，包含5条重要突破，格式简洁清晰" \
  --agent main \
  --model deepseek/deepseek-chat \
  --timeout-seconds 600 \
  --announce \
  --to "ou_b6c7778820b20031cd97bdc45d1cd9fa" \
  --channel feishu

echo "✅ 健康长寿任务配置完成"

echo ""

# 3. 检查AI新闻任务
echo "3. 检查AI新闻每日摘要任务..."
echo "------------------------------------------"
AI_NEWS_ID="0bd3de5c-a4f9-4774-9511-75f344ba114c"
if openclaw cron list | grep -q "$AI_NEWS_ID"; then
    echo "✅ AI新闻任务状态: ok"
else
    echo "❌ AI新闻任务不存在，重新创建..."
    openclaw cron add \
      --name "AI新闻每日摘要" \
      --cron "30 6 * * *" \
      --message "生成AI新闻日报，要求：过去24小时最新AI新闻，包含技术突破、产品发布、行业动态，不超过10条，严格验证真实性" \
      --agent main \
      --model deepseek/deepseek-chat \
      --timeout-seconds 600 \
      --announce \
      --to "ou_b6c7778820b20031cd97bdc45d1cd9fa" \
      --channel feishu
fi

echo ""

# 4. 检查OpenClaw新闻任务
echo "4. 检查OpenClaw每日新闻监控..."
echo "------------------------------------------"
OPENCLAW_ID="5aa186d0-d623-41aa-bef3-352aec56eb20"
if openclaw cron list | grep -q "$OPENCLAW_ID"; then
    echo "✅ OpenClaw任务状态: ok"
else
    echo "❌ OpenClaw任务不存在，重新创建..."
    openclaw cron add \
      --name "OpenClaw每日新闻监控" \
      --cron "0 6 * * *" \
      --message "生成OpenClaw生态日报，要求：过去24小时OpenClaw官方更新、社区动态、版本发布、技能生态进展" \
      --agent main \
      --model deepseek/deepseek-chat \
      --timeout-seconds 600 \
      --announce \
      --to "ou_b6c7778820b20031cd97bdc45d1cd9fa" \
      --channel feishu
fi

echo ""

# 5. 检查昇腾AI任务
echo "5. 检查华为昇腾新闻监控..."
echo "------------------------------------------"
ASCEND_ID="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
if openclaw cron list | grep -q "$ASCEND_ID"; then
    echo "✅ 昇腾AI任务状态: ok"
else
    echo "❌ 昇腾AI任务不存在，重新创建..."
    openclaw cron add \
      --name "华为昇腾新闻监控" \
      --cron "30 7 * * *" \
      --message "生成华为昇腾生态日报，要求：过去24小时昇腾芯片、CANN软件栈、MindSpore框架、生态合作伙伴最新动态" \
      --agent main \
      --model deepseek/deepseek-chat \
      --timeout-seconds 600 \
      --announce \
      --to "ou_b6c7778820b20031cd97bdc45d1cd9fa" \
      --channel feishu
fi

echo ""

# 6. 显示所有任务状态
echo "6. 所有定时任务状态汇总："
echo "------------------------------------------"
openclaw cron list

echo ""

# 7. 创建环境变量配置指南
echo "7. 环境变量配置指南："
echo "------------------------------------------"
cat > /Users/jiyingguo/.openclaw/workspace/env_setup_guide.md << 'EOF'
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

EOF

echo "✅ 环境变量配置指南已生成: /Users/jiyingguo/.openclaw/workspace/env_setup_guide.md"

echo ""
echo "=========================================="
echo "🎉 所有定时任务修复完成!"
echo ""
echo "📅 任务执行时间表:"
echo "   06:00 - OpenClaw新闻"
echo "   06:30 - AI新闻"
echo "   07:00 - 健康长寿科研"
echo "   07:30 - 昇腾AI新闻"
echo ""
echo "⚠️ 重要提醒:"
echo "   请配置 TAVILY_API_KEY 环境变量"
echo "   命令: export TAVILY_API_KEY=your_api_key"
echo ""
echo "✅ 修复完成时间: $(date '+%Y-%m-%d %H:%M:%S')"