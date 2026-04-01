#!/bin/bash
# 批量测试所有已安装技能

echo "========================================"
echo "🔍 OpenClaw技能批量测试"
echo "========================================"

SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
TEST_LOG="$TEST_DIR/batch_test_$(date '+%Y%m%d_%H%M%S').log"
SUMMARY_LOG="$TEST_DIR/test_summary_$(date '+%Y%m%d').log"

echo "测试开始: $(date)" | tee -a "$TEST_LOG"
echo "技能目录: $SKILLS_DIR" | tee -a "$TEST_LOG"

if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ 技能目录不存在" | tee -a "$TEST_LOG"
    exit 1
fi

# 获取所有技能
SKILLS=($(ls -1 "$SKILLS_DIR" 2>/dev/null | sort))
TOTAL_SKILLS=${#SKILLS[@]}

echo "发现技能数: $TOTAL_SKILLS" | tee -a "$TEST_LOG"
echo "" | tee -a "$TEST_LOG"

# 测试计数器
TESTED=0
WORKING=0
BROKEN=0
UNTESTABLE=0

# 测试每个技能
for skill in "${SKILLS[@]}"; do
    ((TESTED++))
    echo "[$TESTED/$TOTAL_SKILLS] 测试: $skill" | tee -a "$TEST_LOG"
    
    # 检查SKILL.md文档
    if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
        echo "  📄 文档存在" | tee -a "$TEST_LOG"
        
        # 尝试读取技能描述
        description=$(grep -m1 "^#" "$SKILLS_DIR/$skill/SKILL.md" | sed 's/^# //' 2>/dev/null || echo "无描述")
        echo "  描述: $description" | tee -a "$TEST_LOG"
        
        # 基础测试：检查是否有可执行文件
        if [ -f "$SKILLS_DIR/$skill/package.json" ]; then
            echo "  📦 包含Node.js包" | tee -a "$TEST_LOG"
            ((WORKING++))
        elif [ -f "$SKILLS_DIR/$skill/requirements.txt" ]; then
            echo "  🐍 包含Python依赖" | tee -a "$TEST_LOG"
            ((WORKING++))
        elif [ -f "$SKILLS_DIR/$skill/setup.py" ]; then
            echo "  🐍 包含Python安装脚本" | tee -a "$TEST_LOG"
            ((WORKING++))
        else
            echo "  ⚠️  无法确定技能类型" | tee -a "$TEST_LOG"
            ((UNTESTABLE++))
        fi
    else
        echo "  ⚠️  缺少SKILL.md文档" | tee -a "$TEST_LOG"
        ((BROKEN++))
    fi
    
    echo "" | tee -a "$TEST_LOG"
done

# 生成总结报告
echo "========================================" | tee -a "$TEST_LOG"
echo "测试完成: $(date)" | tee -a "$TEST_LOG"
echo "" | tee -a "$TEST_LOG"
echo "📊 测试总结:" | tee -a "$TEST_LOG"
echo "  总技能数: $TOTAL_SKILLS" | tee -a "$TEST_LOG"
echo "  已测试: $TESTED" | tee -a "$TEST_LOG"
echo "  正常技能: $WORKING" | tee -a "$TEST_LOG"
echo "  异常技能: $BROKEN" | tee -a "$TEST_LOG"
echo "  无法测试: $UNTESTABLE" | tee -a "$TEST_LOG"

if [ $TOTAL_SKILLS -gt 0 ]; then
    HEALTH_RATE=$((WORKING * 100 / TOTAL_SKILLS))
    echo "  健康率: ${HEALTH_RATE}%" | tee -a "$TEST_LOG"
fi

# 保存到每日总结
cat >> "$SUMMARY_LOG" << SUMMARY
测试时间: $(date '+%Y-%m-%d %H:%M:%S')
技能总数: $TOTAL_SKILLS
正常技能: $WORKING
异常技能: $BROKEN
健康率: ${HEALTH_RATE}%
---
SUMMARY

echo "" | tee -a "$TEST_LOG"
echo "详细日志: $TEST_LOG" | tee -a "$TEST_LOG"
echo "每日总结: $SUMMARY_LOG" | tee -a "$TEST_LOG"
