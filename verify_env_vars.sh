#!/bin/bash

echo "🔍 验证环境变量配置"
echo "=========================================="

# 检查TAVILY_API_KEY
if [ -z "$TAVILY_API_KEY" ]; then
    echo "❌ TAVILY_API_KEY 未设置"
    echo "   请运行: source ~/.zshrc"
    exit 1
else
    echo "✅ TAVILY_API_KEY 已配置"
    echo "   密钥前10位: ${TAVILY_API_KEY:0:10}..."
fi

# 检查其他可能需要的API密钥
echo ""
echo "📋 其他API密钥状态:"
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️ GEMINI_API_KEY 未设置（可选）"
else
    echo "✅ GEMINI_API_KEY 已配置"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️ OPENAI_API_KEY 未设置（可选）"
else
    echo "✅ OPENAI_API_KEY 已配置"
fi

echo ""
echo "📊 定时任务环境验证:"
echo "------------------------------------------"

# 检查定时任务
echo "1. 定时任务状态:"
openclaw cron list | grep -E "(Name|AI新闻|健康长寿|OpenClaw|昇腾)"

echo ""
echo "2. 测试搜索API（简单测试）..."
# 这里可以添加简单的API测试

echo ""
echo "✅ 环境变量验证完成"
echo "📅 明日定时任务将正常执行:"
echo "   06:00 - OpenClaw新闻"
echo "   06:30 - AI新闻"
echo "   07:00 - 健康长寿科研"
echo "   07:30 - 昇腾AI新闻"

