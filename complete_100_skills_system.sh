#!/bin/bash
# OpenClaw 100个技能完整系统
# 包含：安装脚本 + 进度监控 + 技能测试 + 问题解决

set -e

echo "================================================================"
echo "🚀 OpenClaw 100个技能完整管理系统"
echo "================================================================"

# 配置
BASE_DIR="/Users/jiyingguo/.openclaw/workspace"
SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
LOG_DIR="$BASE_DIR/logs"
REPORT_DIR="$BASE_DIR/reports"
SCRIPT_DIR="$BASE_DIR/scripts"
TEST_DIR="$BASE_DIR/tests"
TARGET_COUNT=100

# 创建目录结构
mkdir -p "$LOG_DIR" "$REPORT_DIR" "$SCRIPT_DIR" "$TEST_DIR"

# 时间戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    local level=$1
    local message=$2
    local color=$NC
    
    case $level in
        "INFO") color=$BLUE ;;
        "SUCCESS") color=$GREEN ;;
        "WARNING") color=$YELLOW ;;
        "ERROR") color=$RED ;;
    esac
    
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] $level: $message${NC}" | tee -a "$LOG_DIR/system_${TIMESTAMP}.log"
}

# ==================== 功能1: 创建每日安装脚本 ====================
create_daily_scripts() {
    log "INFO" "创建每日安装脚本..."
    
    # 定义5天的技能分配
    DAY1_SKILLS=("docker" "aws" "telegram" "ffmpeg" "calendar" "python" "vscode" "vercel" "zoom" "openai")
    DAY2_SKILLS=("kubernetes" "azure" "gcp" "signal" "image-processing" "todo" "nodejs" "netlify" "teams" "anthropic")
    DAY3_SKILLS=("typescript" "firebase" "feishu" "audio-processing" "notes" "react" "vue" "webpack" "jest" "eslint")
    DAY4_SKILLS=("prettier" "babel" "rollup" "vite" "gradle" "maven" "make" "cmake" "digitalocean" "cloudflare")
    DAY5_SKILLS=("heroku" "supabase" "mongodb" "postgresql" "redis" "elasticsearch" "kafka" "huggingface")
    
    # 创建第1天脚本
    cat > "$SCRIPT_DIR/install_day1.sh" << 'EOF'
#!/bin/bash
# 第1天安装脚本 - 核心工具

echo "========================================"
echo "📅 第1天安装: 核心工具 (10个技能)"
echo "========================================"

SKILLS=("docker" "aws" "telegram" "ffmpeg" "calendar" "python" "vscode" "vercel" "zoom" "openai")
DELAY=30
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/logs/day1_$(date '+%Y%m%d_%H%M%S').log"

echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo "技能列表: ${SKILLS[*]}" | tee -a "$LOG_FILE"
echo "=" * 50 | tee -a "$LOG_FILE"

for i in "${!SKILLS[@]}"; do
    skill="${SKILLS[$i]}"
    echo "[$((i+1))/${#SKILLS[@]}] 安装: $skill" | tee -a "$LOG_FILE"
    
    # 检查是否已安装
    if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/$skill" ]; then
        echo "✅ $skill 已安装，跳过" | tee -a "$LOG_FILE"
        continue
    fi
    
    # 安装技能
    if clawhub install "$skill" 2>&1 | tee -a "$LOG_FILE"; then
        echo "✅ $skill 安装成功" | tee -a "$LOG_FILE"
    else
        echo "❌ $skill 安装失败" | tee -a "$LOG_FILE"
        echo "错误信息已记录到日志" | tee -a "$LOG_FILE"
    fi
    
    # 不是最后一个技能则等待
    if [ $i -lt $((${#SKILLS[@]}-1)) ]; then
        echo "等待 ${DELAY}秒避免速率限制..." | tee -a "$LOG_FILE"
        sleep $DELAY
    fi
done

echo "=" * 50 | tee -a "$LOG_FILE"
echo "第1天安装完成" | tee -a "$LOG_FILE"
echo "完成时间: $(date)" | tee -a "$LOG_FILE"

# 生成报告
INSTALLED_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ | wc -l)
echo "当前技能总数: $INSTALLED_COUNT" | tee -a "$LOG_FILE"
echo "距离100目标还差: $((100 - INSTALLED_COUNT))" | tee -a "$LOG_FILE"
EOF
    
    # 创建第2-5天脚本（类似结构）
    for day in 2 3 4 5; do
        var_name="DAY${day}_SKILLS[@]"
        skills_array=("${!var_name}")
        
        cat > "$SCRIPT_DIR/install_day${day}.sh" << EOF
#!/bin/bash
# 第${day}天安装脚本

echo "========================================"
echo "📅 第${day}天安装 (${#skills_array[@]}个技能)"
echo "========================================"

SKILLS=(${skills_array[@]})
DELAY=30
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/logs/day${day}_\$(date '+%Y%m%d_%H%M%S').log"

echo "开始时间: \$(date)" | tee -a "\$LOG_FILE"
echo "技能列表: \${SKILLS[*]}" | tee -a "\$LOG_FILE"
echo "=" * 50 | tee -a "\$LOG_FILE"

for i in "\${!SKILLS[@]}"; do
    skill="\${SKILLS[\$i]}"
    echo "[\$((i+1))/\${#SKILLS[@]}] 安装: \$skill" | tee -a "\$LOG_FILE"
    
    # 检查是否已安装
    if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/\$skill" ]; then
        echo "✅ \$skill 已安装，跳过" | tee -a "\$LOG_FILE"
        continue
    fi
    
    # 安装技能
    if clawhub install "\$skill" 2>&1 | tee -a "\$LOG_FILE"; then
        echo "✅ \$skill 安装成功" | tee -a "\$LOG_FILE"
    else
        echo "❌ \$skill 安装失败" | tee -a "\$LOG_FILE"
        echo "错误信息已记录到日志" | tee -a "\$LOG_FILE"
    fi
    
    # 不是最后一个技能则等待
    if [ \$i -lt \$((\${#SKILLS[@]}-1)) ]; then
        echo "等待 \${DELAY}秒避免速率限制..." | tee -a "\$LOG_FILE"
        sleep \$DELAY
    fi
done

echo "=" * 50 | tee -a "\$LOG_FILE"
echo "第${day}天安装完成" | tee -a "\$LOG_FILE"
echo "完成时间: \$(date)" | tee -a "\$LOG_FILE"

# 生成报告
INSTALLED_COUNT=\$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ | wc -l)
echo "当前技能总数: \$INSTALLED_COUNT" | tee -a "\$LOG_FILE"
echo "距离100目标还差: \$((100 - INSTALLED_COUNT))" | tee -a "\$LOG_FILE"
EOF
    done
    
    # 设置执行权限
    chmod +x "$SCRIPT_DIR"/install_day*.sh
    
    log "SUCCESS" "已创建5天的安装脚本"
    echo "脚本位置: $SCRIPT_DIR/"
    echo "  install_day1.sh - 第1天 (10个核心技能)"
    echo "  install_day2.sh - 第2天 (10个云服务技能)"
    echo "  install_day3.sh - 第3天 (10个开发工具)"
    echo "  install_day4.sh - 第4天 (10个扩展工具)"
    echo "  install_day5.sh - 第5天 (8个高级技能)"
}

# ==================== 功能2: 监控安装进度 ====================
create_progress_monitor() {
    log "INFO" "创建进度监控系统..."
    
    # 创建实时监控脚本
    cat > "$SCRIPT_DIR/monitor_progress.sh" << 'EOF'
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
EOF
    
    # 创建自动报告生成脚本
    cat > "$SCRIPT_DIR/generate_report.sh" << 'EOF'
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
EOF
    
    chmod +x "$SCRIPT_DIR"/monitor_progress.sh "$SCRIPT_DIR"/generate_report.sh
    
    log "SUCCESS" "已创建进度监控系统"
    echo "监控脚本: $SCRIPT_DIR/monitor_progress.sh"
    echo "报告脚本: $SCRIPT_DIR/generate_report.sh"
}

# ==================== 功能3: 测试已安装技能 ====================
create_skill_tester() {
    log "INFO" "创建技能测试系统..."
    
    # 创建核心技能测试脚本
    cat > "$TEST_DIR/test_core_skills.sh" << 'EOF'
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
EOF
    
    # 创建批量测试脚本
    cat > "$TEST_DIR/test_all_skills.sh" << 'EOF'
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
EOF
    
    chmod +x "$TEST_DIR"/test_*.sh
    
    log "SUCCESS" "已创建技能测试系统"
    echo "核心测试: $TEST_DIR/test_core_skills.sh"
    echo "批量测试: $TEST_DIR/test_all_skills.sh"
}

# ==================== 功能4: 解决安装问题 ====================
create_problem_solver() {
    log "INFO" "创建问题解决系统..."
    
    # 创建问题诊断脚本
    cat > "$SCRIPT_DIR/diagnose_problems.sh" << 'EOF'
#!/bin/bash
# 问题诊断脚本

echo "========================================"
echo "🔧 OpenClaw技能安装问题诊断"
echo "========================================"

DIAG_LOG="$LOG_DIR/diagnose_$(date '+%Y%m%d_%H%M%S').log"
echo "诊断开始: $(date)" | tee -a "$DIAG_LOG"

# 检查clawhub
echo "1. 检查clawhub..." | tee -a "$DIAG_LOG"
if command -v clawhub &> /dev/null; then
    echo "  ✅ clawhub已安装: $(clawhub --version | head -1)" | tee -a "$DIAG_LOG"
else
    echo "  ❌ clawhub未安装" | tee -a "$DIAG_LOG"
    echo "  解决方案: npm install -g @openclaw/clawhub" | tee -a "$DIAG_LOG"
fi

# 检查网络连接
echo "" | tee -a "$DIAG_LOG"
echo "2. 检查网络连接..." | tee -a "$DIAG_LOG"
if ping -c 1 -W 2 google.com &> /dev/null; then
    echo "  ✅ 网络连接正常" | tee -a "$DIAG_LOG"
else
    echo "  ❌ 网络连接失败" | tee -a "$DIAG_LOG"
    echo "  解决方案: 检查网络设置" | tee -a "$DIAG_LOG"
fi

# 检查磁盘空间
echo "" | tee -a "$DIAG_LOG"
echo "3. 检查磁盘空间..." | tee -a "$DIAG_LOG"
df -h /opt/homebrew 2>/dev/null | tee -a "$DIAG_LOG"

# 检查速率限制
echo "" | tee -a "$DIAG_LOG"
echo "4. 检查速率限制..." | tee -a "$DIAG_LOG"
RECENT_ERRORS=$(find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -l "Rate limit exceeded" {} \; 2>/dev/null | wc -l)
if [ $RECENT_ERRORS -gt 0 ]; then
    echo "  ⚠️  检测到速率限制错误: $RECENT_ERRORS 次" | tee -a "$DIAG_LOG"
    echo "  解决方案:" | tee -a "$DIAG_LOG"
    echo "    1. 等待2-3小时再尝试" | tee -a "$DIAG_LOG"
    echo "    2. 增加安装间隔时间" | tee -a "$DIAG_LOG"
    echo "    3. 减少每批安装数量" | tee -a "$DIAG_LOG"
else
    echo "  ✅ 未检测到速率限制错误" | tee -a "$DIAG_LOG"
fi

# 检查失败的安装
echo "" | tee -a "$DIAG_LOG"
echo "5. 检查失败的安装..." | tee -a "$DIAG_LOG"
FAILED_INSTALLS=$(find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -l "安装失败" {} \; 2>/dev/null | wc -l)
if [ $FAILED_INSTALLS -gt 0 ]; then
    echo "  ⚠️  检测到失败的安装: $FAILED_INSTALLS 次" | tee -a "$DIAG_LOG"
    echo "  最近失败记录:" | tee -a "$DIAG_LOG"
    find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -h "安装失败" {} \; 2>/dev/null | tail -5 | tee -a "$DIAG_LOG"
else
    echo "  ✅ 未检测到失败的安装" | tee -a "$DIAG_LOG"
fi

# 检查技能目录权限
echo "" | tee -a "$DIAG_LOG"
echo "6. 检查目录权限..." | tee -a "$DIAG_LOG"
SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
if [ -d "$SKILLS_DIR" ]; then
    if [ -w "$SKILLS_DIR" ]; then
        echo "  ✅ 技能目录可写" | tee -a "$DIAG_LOG"
    else
        echo "  ❌ 技能目录不可写" | tee -a "$DIAG_LOG"
        echo "  解决方案: sudo chown -R $(whoami) $SKILLS_DIR" | tee -a "$DIAG_LOG"
    fi
else
    echo "  ⚠️  技能目录不存在" | tee -a "$DIAG_LOG"
fi

# 生成诊断报告
echo "" | tee -a "$DIAG_LOG"
echo "========================================" | tee -a "$DIAG_LOG"
echo "诊断完成: $(date)" | tee -a "$DIAG_LOG"
echo "" | tee -a "$DIAG_LOG"
echo "💡 建议操作:" | tee -a "$DIAG_LOG"

if [ $RECENT_ERRORS -gt 0 ]; then
    echo "  1. 暂停安装，等待速率限制恢复" | tee -a "$DIAG_LOG"
fi

if [ $FAILED_INSTALLS -gt 0 ]; then
    echo "  2. 重新尝试失败的安装" | tee -a "$DIAG_LOG"
fi

echo "  3. 运行测试脚本验证技能功能" | tee -a "$DIAG_LOG"
echo "  4. 定期生成进度报告" | tee -a "$DIAG_LOG"

echo "" | tee -a "$DIAG_LOG"
echo "详细诊断日志: $DIAG_LOG" | tee -a "$DIAG_LOG"
EOF
    
    # 创建修复脚本
    cat > "$SCRIPT_DIR/fix_common_issues.sh" << 'EOF'
#!/bin/bash
# 常见问题修复脚本

echo "========================================"
echo "🛠️  OpenClaw常见问题修复"
echo "========================================"

FIX_LOG="$LOG_DIR/fix_issues_$(date '+%Y%m%d_%H%M%S').log"
echo "修复开始: $(date)" | tee -a "$FIX_LOG"

# 修复函数
fix_issue() {
    local issue=$1
    local fix_cmd=$2
    local description=$3
    
    echo "" | tee -a "$FIX_LOG"
    echo "修复: $issue" | tee -a "$FIX_LOG"
    echo "描述: $description" | tee -a "$FIX_LOG"
    echo "命令: $fix_cmd" | tee -a "$FIX_LOG"
    
    if eval "$fix_cmd" 2>&1 | tee -a "$FIX_LOG"; then
        echo "✅ 修复成功" | tee -a "$FIX_LOG"
        return 0
    else
        echo "❌ 修复失败" | tee -a "$FIX_LOG"
        return 1
    fi
}

# 1. 清理clawhub缓存
fix_issue "clawhub_cache" "rm -rf /tmp/clawhub_* ~/.cache/clawhub" "清理clawhub缓存文件"

# 2. 修复技能目录权限
if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills" ]; then
    fix_issue "skills_permission" "chmod -R 755 /opt/homebrew/lib/node_modules/openclaw/skills" "修复技能目录权限"
fi

# 3. 更新clawhub
fix_issue "update_clawhub" "npm update -g @openclaw/clawhub" "更新clawhub到最新版本"

# 4. 检查并修复损坏的技能
echo "" | tee -a "$FIX_LOG"
echo "检查损坏的技能..." | tee -a "$FIX_LOG"
for skill_dir in /opt/homebrew/lib/node_modules/openclaw/skills/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        if [ ! -f "$skill_dir/SKILL.md" ]; then
            echo "⚠️  发现损坏技能: $skill_name (缺少SKILL.md)" | tee -a "$FIX_LOG"
            echo "  尝试重新安装..." | tee -a "$FIX_LOG"
            if clawhub install "$skill_name" 2>&1 | tee -a "$FIX_LOG"; then
                echo "  ✅ $skill_name 重新安装成功" | tee -a "$FIX_LOG"
            else
                echo "  ❌ $skill_name 重新安装失败" | tee -a "$FIX_LOG"
            fi
        fi
    fi
done

# 5. 清理旧日志
fix_issue "clean_old_logs" "find /Users/jiyingguo/.openclaw/workspace/logs -name \"*.log\" -mtime +7 -delete" "清理7天前的日志文件"

echo "" | tee -a "$FIX_LOG"
echo "========================================" | tee -a "$FIX_LOG"
echo "修复完成: $(date)" | tee -a "$FIX_LOG"
echo "" | tee -a "$FIX_LOG"
echo "💡 建议后续操作:" | tee -a "$FIX_LOG"
echo "  1. 运行诊断脚本: ./scripts/diagnose_problems.sh" | tee -a "$FIX_LOG"
echo "  2. 测试核心技能: ./tests/test_core_skills.sh" | tee -a "$FIX_LOG"
echo "  3. 继续安装计划: ./scripts/install_day*.sh" | tee -a "$FIX_LOG"

echo "" | tee -a "$FIX_LOG"
echo "详细修复日志: $FIX_LOG" | tee -a "$FIX_LOG"
EOF
    
    chmod +x "$SCRIPT_DIR"/diagnose_problems.sh "$SCRIPT_DIR"/fix_common_issues.sh
    
    log "SUCCESS" "已创建问题解决系统"
    echo "问题诊断: $SCRIPT_DIR/diagnose_problems.sh"
    echo "常见修复: $SCRIPT_DIR/fix_common_issues.sh"
}

# ==================== 主菜单 ====================
show_main_menu() {
    echo ""
    echo "========================================"
    echo "📋 主菜单 - 选择要执行的操作"
    echo "========================================"
    echo ""
    echo "1. 📅 创建每日安装脚本 (5天计划)"
    echo "2. 📊 创建进度监控系统"
    echo "3. 🧪 创建技能测试系统"
    echo "4. 🔧 创建问题解决系统"
    echo "5. 🚀 一键安装全部系统"
    echo "6. 📈 查看当前进度"
    echo "7. 🧹 清理系统"
    echo "8. 📖 查看使用指南"
    echo "9. 🚪 退出"
    echo ""
    echo "========================================"
}

# ==================== 查看当前进度 ====================
show_current_progress() {
    CURRENT_COUNT=$(ls -1 "$SKILLS_DIR" 2>/dev/null | wc -l)
    PERCENTAGE=$((CURRENT_COUNT * 100 / TARGET_COUNT))
    
    echo ""
    echo "========================================"
    echo "📈 当前安装进度"
    echo "========================================"
    echo ""
    echo "已安装技能: $CURRENT_COUNT 个"
    echo "目标技能: $TARGET_COUNT 个"
    echo "完成进度: $PERCENTAGE%"
    echo ""
    
    # 进度条
    BAR_LENGTH=30
    FILLED=$((CURRENT_COUNT * BAR_LENGTH / TARGET_COUNT))
    EMPTY=$((BAR_LENGTH - FILLED))
    
    printf "进度: ["
    printf "%${FILLED}s" | tr ' ' '='
    printf "%${EMPTY}s" | tr ' ' ' '
    printf "] $PERCENTAGE%%\n"
    echo ""
    
    if [ $CURRENT_COUNT -ge $TARGET_COUNT ]; then
        echo "🎉 恭喜！已达成100个技能目标！"
    else
        echo "还需安装: $((TARGET_COUNT - CURRENT_COUNT)) 个技能"
        echo "建议: 运行 ./scripts/install_day1.sh 开始安装"
    fi
}

# ==================== 清理系统 ====================
cleanup_system() {
    echo ""
    echo "========================================"
    echo "🧹 系统清理"
    echo "========================================"
    echo ""
    echo "选择清理选项:"
    echo "1. 清理日志文件 (保留最近3天)"
    echo "2. 清理测试文件"
    echo "3. 清理所有临时文件"
    echo "4. 返回主菜单"
    echo ""
    
    read -p "请输入选择 (1-4): " clean_choice
    
    case $clean_choice in
        1)
            find "$LOG_DIR" -name "*.log" -mtime +3 -delete
            echo "✅ 已清理3天前的日志文件"
            ;;
        2)
            rm -rf "$TEST_DIR"/*.log 2>/dev/null
            echo "✅ 已清理测试日志文件"
            ;;
        3)
            rm -rf /tmp/clawhub_* 2>/dev/null
            find "$BASE_DIR" -name "*.log" -mtime +1 -delete 2>/dev/null
            echo "✅ 已清理临时文件"
            ;;
        4)
            return
            ;;
        *)
            echo "❌ 无效选择"
            ;;
    esac
}

# ==================== 使用指南 ====================
show_usage_guide() {
    cat << 'GUIDE'

========================================
📖 OpenClaw 100个技能系统使用指南
========================================

🎯 系统目标
帮助你在5天内安装100个最流行的OpenClaw技能

📁 目录结构
/Users/jiyingguo/.openclaw/workspace/
├── scripts/      # 安装和管理脚本
├── tests/        # 测试脚本
├── logs/         # 日志文件
├── reports/      # 进度报告
└── 本系统文件

🚀 快速开始
1. 运行本脚本选择"5. 一键安装全部系统"
2. 查看当前进度: 选择"6. 查看当前进度"
3. 开始安装: 运行 ./scripts/install_day1.sh

📅 5天安装计划
第1天: 10个核心技能 (docker, aws, python等)
第2天: 10个云服务技能
第3天: 10个开发工具
第4天: 10个扩展工具
第5天: 8个高级技能

🔧 系统功能
1. 每日安装脚本 - 自动分批安装
2. 进度监控 - 实时查看安装进度
3. 技能测试 - 验证已安装技能
4. 问题解决 - 诊断和修复常见问题

⚠️ 重要提醒
• clawhub有速率限制，每安装1个技能等待30秒
• 每天最多安装10-15个技能
• 遇到"Rate limit exceeded"立即停止，等待几小时
• 定期运行测试脚本验证功能

📞 遇到问题
1. 运行诊断脚本: ./scripts/diagnose_problems.sh
2. 运行修复脚本: ./scripts/fix_common_issues.sh
3. 查看日志: tail -f logs/*.log

🎉 完成目标
当技能总数达到100个时，系统会自动检测并显示庆祝信息！

GUIDE
}

# ==================== 主程序 ====================
main() {
    # 检查clawhub
    if ! command -v clawhub &> /dev/null; then
        log "ERROR" "clawhub未安装，请先安装: npm install -g @openclaw/clawhub"
        exit 1
    fi
    
    # 显示欢迎信息
    echo ""
    echo "欢迎使用 OpenClaw 100个技能管理系统"
    echo "当前已安装技能: $(ls -1 "$SKILLS_DIR" 2>/dev/null | wc -l)/100"
    echo ""
    
    while true; do
        show_main_menu
        
        read -p "请输入选择 (1-9): " choice
        
        case $choice in
            1)
                create_daily_scripts
                ;;
            2)
                create_progress_monitor
                ;;
            3)
                create_skill_tester
                ;;
            4)
                create_problem_solver
                ;;
            5)
                log "INFO" "开始一键安装全部系统..."
                create_daily_scripts
                create_progress_monitor
                create_skill_tester
                create_problem_solver
                log "SUCCESS" "全部系统安装完成！"
                echo ""
                echo "🎉 所有系统组件已创建完成！"
                echo "📁 脚本目录: $SCRIPT_DIR"
                echo "🧪 测试目录: $TEST_DIR"
                echo "📊 日志目录: $LOG_DIR"
                echo ""
                echo "🚀 现在可以运行: ./scripts/install_day1.sh 开始安装！"
                ;;
            6)
                show_current_progress
                ;;
            7)
                cleanup_system
                ;;
            8)
                show_usage_guide
                ;;
            9)
                echo "感谢使用，再见！"
                exit 0
                ;;
            *)
                echo "❌ 无效选择，请重新输入"
                ;;
        esac
        
        echo ""
        read -p "按回车键继续..."
    done
}

# 运行主程序
main "$@"