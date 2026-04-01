#!/bin/bash
# 生成详细报告

REPORT_FILE="/Users/jiyingguo/.openclaw/workspace/reports/skill_report_$(date '+%Y%m%d_%H%M%S').md"
CURRENT_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)

cat > "$REPORT_FILE" << REPORT
# OpenClaw技能安装进度报告

## 基本信息
- **报告时间**: $(date '+%Y-%m-%d %H:%M:%S')
- **当前技能数**: ${CURRENT_COUNT} 个
- **目标技能数**: 100 个
- **完成进度**: $((CURRENT_COUNT * 100 / 100))%

## 技能分类统计

### 已安装技能列表
$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | sort | sed 's/^/- /')

## 安装日志摘要

### 最近安装记录
$(find /Users/jiyingguo/.openclaw/workspace/logs/ -name "*.log" -type f -mtime -3 2>/dev/null | sort -r | head -5 | while read logfile; do
    echo "#### $(basename "$logfile")"
    echo "最后记录: $(tail -1 "$logfile" 2>/dev/null || echo '无内容')"
    echo ""
done)

## 建议

根据当前进度 ($((CURRENT_COUNT)) / 100)，建议：

$(if [ $CURRENT_COUNT -lt 60 ]; then
    echo "1. 继续执行每日安装脚本"
    echo "2. 关注速率限制，适当增加延迟"
    echo "3. 定期运行监控脚本检查进度"
elif [ $CURRENT_COUNT -lt 90 ]; then
    echo "1. 即将完成目标，保持当前节奏"
    echo "2. 测试已安装技能的功能"
    echo "3. 准备庆祝达成100个技能！"
else
    echo "1. 🎉 即将达成目标！"
    echo "2. 测试所有核心技能功能"
    echo "3. 考虑整理技能使用文档"
fi)

## 系统信息
- **操作系统**: $(uname -s) $(uname -r)
- **clawhub版本**: $(clawhub --version 2>/dev/null | head -1 || echo "未知")
- **报告生成脚本**: generate_report.sh

REPORT

echo "报告已生成: $REPORT_FILE"
