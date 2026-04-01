#!/bin/bash
# 进度监控脚本

echo "========================================"
echo "📊 OpenClaw技能安装进度监控"
echo "========================================"

# 获取当前技能数
CURRENT_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)
TARGET=100

# 计算进度
PERCENTAGE=$((CURRENT_COUNT * 100 / TARGET))
REMAINING=$((TARGET - CURRENT_COUNT))

# 进度条
BAR_LENGTH=50
FILLED=$((CURRENT_COUNT * BAR_LENGTH / TARGET))
EMPTY=$((BAR_LENGTH - FILLED))

printf "当前进度: ["
printf "%${FILLED}s" | tr ' ' '='
printf "%${EMPTY}s" | tr ' ' ' '
printf "] ${PERCENTAGE}%% (${CURRENT_COUNT}/${TARGET})\n"

echo ""
echo "📈 详细统计:"
echo "  已安装技能: ${CURRENT_COUNT} 个"
echo "  目标技能: ${TARGET} 个"
echo "  还需安装: ${REMAINING} 个"
echo "  完成度: ${PERCENTAGE}%"

# 检查最近日志
echo ""
echo "📋 最近安装日志:"
find /Users/jiyingguo/.openclaw/workspace/logs/ -name "*.log" -type f -mtime -7 2>/dev/null | \
    sort -r | head -3 | while read logfile; do
    echo "  $(basename "$logfile"): $(tail -1 "$logfile" 2>/dev/null || echo "无内容")"
done

# 检查今日安装
TODAY=$(date '+%Y%m%d')
TODAY_LOGS=$(find /Users/jiyingguo/.openclaw/workspace/logs/ -name "*${TODAY}*.log" 2>/dev/null | wc -l)
echo ""
echo "📅 今日安装情况:"
echo "  今日日志文件: ${TODAY_LOGS} 个"

if [ $TODAY_LOGS -gt 0 ]; then
    echo "  今日安装统计:"
    find /Users/jiyingguo/.openclaw/workspace/logs/ -name "*${TODAY}*.log" 2>/dev/null | \
        while read logfile; do
            success_count=$(grep -c "安装成功" "$logfile" 2>/dev/null || echo 0)
            fail_count=$(grep -c "安装失败" "$logfile" 2>/dev/null || echo 0)
            echo "    $(basename "$logfile"): 成功${success_count}, 失败${fail_count}"
        done
fi

# 建议
echo ""
echo "💡 建议:"
if [ $REMAINING -gt 40 ]; then
    echo "  建议开始第1天安装: ./scripts/install_day1.sh"
elif [ $REMAINING -gt 30 ]; then
    echo "  建议继续第2天安装: ./scripts/install_day2.sh"
elif [ $REMAINING -gt 20 ]; then
    echo "  建议继续第3天安装: ./scripts/install_day3.sh"
elif [ $REMAINING -gt 10 ]; then
    echo "  建议继续第4天安装: ./scripts/install_day4.sh"
elif [ $REMAINING -gt 0 ]; then
    echo "  建议完成第5天安装: ./scripts/install_day5.sh"
else
    echo "  🎉 恭喜！已达成100个技能目标！"
fi
