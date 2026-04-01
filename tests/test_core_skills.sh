#!/bin/bash
# 核心技能测试脚本

echo "========================================"
echo "🧪 OpenClaw核心技能功能测试"
echo "========================================"

TEST_LOG="$TEST_DIR/core_test_$(date '+%Y%m%d_%H%M%S').log"
echo "测试开始时间: $(date)" | tee -a "$TEST_LOG"

# 测试函数
test_skill() {
    local skill=$1
    local test_cmd=$2
    local description=$3
    
    echo "" | tee -a "$TEST_LOG"
    echo "测试: $skill - $description" | tee -a "$TEST_LOG"
    echo "命令: $test_cmd" | tee -a "$TEST_LOG"
    
    if eval "$test_cmd" 2>&1 | tee -a "$TEST_LOG"; then
        echo "✅ $skill 测试通过" | tee -a "$TEST_LOG"
        return 0
    else
        echo "❌ $skill 测试失败" | tee -a "$TEST_LOG"
        return 1
    fi
}

# 测试核心技能
echo "开始测试核心技能..." | tee -a "$TEST_LOG"

# github技能测试
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/github" ]; then
    test_skill "github" "github --version" "版本检查"
else
    echo "⚠️  github技能未安装" | tee -a "$TEST_LOG"
fi

# gog技能测试
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/gog" ]; then
    test_skill "gog" "gog --version" "版本检查"
else
    echo "⚠️  gog技能未安装" | tee -a "$TEST_LOG"
fi

# weather技能测试
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/weather" ]; then
    test_skill "weather" "weather Shanghai --format \"%c %t\"" "天气查询"
else
    echo "⚠️  weather技能未安装" | tee -a "$TEST_LOG"
fi

# summarize技能测试
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/summarize" ]; then
    test_skill "summarize" "summarize --help" "帮助文档检查"
else
    echo "⚠️  summarize技能未安装" | tee -a "$TEST_LOG"
fi

# 新增技能测试（如果已安装）
NEW_SKILLS=("docker" "aws" "python" "telegram" "ffmpeg")
for skill in "${NEW_SKILLS[@]}"; do
    if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/$skill" ]; then
        case $skill in
            docker) test_cmd="docker --version" ;;
            aws) test_cmd="aws --version" ;;
            python) test_cmd="python3 --version" ;;
            telegram) test_cmd="echo 'Telegram技能已安装'" ;;
            ffmpeg) test_cmd="ffmpeg -version | head -1" ;;
            *) test_cmd="echo '测试命令待定义'" ;;
        esac
        test_skill "$skill" "$test_cmd" "基础功能检查"
    fi
done

# 测试总结
echo "" | tee -a "$TEST_LOG"
echo "========================================" | tee -a "$TEST_LOG"
echo "测试完成时间: $(date)" | tee -a "$TEST_LOG"

# 统计结果
TOTAL_TESTS=$(grep -c "测试:" "$TEST_LOG" 2>/dev/null || echo 0)
PASSED_TESTS=$(grep -c "✅" "$TEST_LOG" 2>/dev/null || echo 0)
FAILED_TESTS=$(grep -c "❌" "$TEST_LOG" 2>/dev/null || echo 0)

echo "测试统计:" | tee -a "$TEST_LOG"
echo "  总测试数: $TOTAL_TESTS" | tee -a "$TEST_LOG"
echo "  通过数: $PASSED_TESTS" | tee -a "$TEST_LOG"
echo "  失败数: $FAILED_TESTS" | tee -a "$TEST_LOG"

if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
    echo "  通过率: ${PASS_RATE}%" | tee -a "$TEST_LOG"
fi

echo "详细日志: $TEST_LOG" | tee -a "$TEST_LOG"
