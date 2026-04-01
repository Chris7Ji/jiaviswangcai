#!/bin/bash
# 今天只安装1个技能 - 超级保守策略

echo "========================================"
echo "🎯 今日目标: 只安装1个核心技能"
echo "========================================"
echo "基于当前速率限制情况，采用最保守策略"
echo "确保今天至少有1个成功安装"
echo ""

# 选择最简单的技能
TARGET_SKILL="docker"  # 选择docker，因为它是开发核心工具

echo "🎯 目标技能: $TARGET_SKILL"
echo "📊 当前技能数: $(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)/100"
echo ""

# 检查是否已安装
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/$TARGET_SKILL" ]; then
    echo "✅ $TARGET_SKILL 已安装！"
    echo "🎉 今日目标已完成！"
    exit 0
fi

echo "准备安装 $TARGET_SKILL ..."
echo "这将测试clawhub的当前状态"
echo ""

read -p "是否开始安装? (y/n): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "安装取消"
    exit 0
fi

echo ""
echo "开始时间: $(date)"
echo "========================================"

# 尝试安装
echo "尝试安装 $TARGET_SKILL ..."
echo "如果遇到速率限制，我们会知道需要等待多久"

if clawhub install "$TARGET_SKILL" 2>&1; then
    echo ""
    echo "🎉 成功！$TARGET_SKILL 已安装"
    echo "✅ 今日目标完成"
else
    echo ""
    echo "⚠️  安装失败，可能是速率限制"
    echo ""
    echo "💡 建议:"
    echo "1. 等待至少2小时再尝试"
    echo "2. 或者明天再继续安装"
    echo "3. 当前已有52个技能，已经很强大了"
fi

echo ""
echo "当前技能总数: $(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)/100"
echo "完成时间: $(date)"