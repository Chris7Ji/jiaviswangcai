#!/bin/bash
# 智能慢速安装策略 - 应对clawhub速率限制

echo "========================================"
echo "🐢 智能慢速安装策略"
echo "========================================"
echo "检测到clawhub速率限制，采用保守安装策略"
echo ""

# 配置
SKILLS_TO_INSTALL=("docker" "aws" "telegram" "ffmpeg" "calendar" "python" "vscode" "vercel" "zoom" "openai")
INSTALL_DELAY=180  # 3分钟延迟，避免速率限制
MAX_RETRIES=2
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/logs/slow_install_$(date '+%Y%m%d_%H%M%S').log"

# 检查当前状态
CURRENT_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)
echo "当前技能数: $CURRENT_COUNT/100"
echo "计划安装: ${#SKILLS_TO_INSTALL[@]} 个技能"
echo "预计总时间: $(( ${#SKILLS_TO_INSTALL[@]} * INSTALL_DELAY / 60 )) 分钟"
echo "日志文件: $LOG_FILE"
echo ""

# 确认
read -p "是否开始慢速安装? (y/n): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo "安装取消"
    exit 0
fi

echo "开始时间: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 安装函数
install_with_care() {
    local skill=$1
    local attempt=1
    
    echo "" | tee -a "$LOG_FILE"
    echo "🔄 尝试安装: $skill" | tee -a "$LOG_FILE"
    
    # 检查是否已安装
    if [ -d "/opt/homebrew/lib/node_modules/openclaw/skills/$skill" ]; then
        echo "✅ $skill 已安装，跳过" | tee -a "$LOG_FILE"
        return 0
    fi
    
    while [ $attempt -le $MAX_RETRIES ]; do
        echo "  尝试 $attempt/$MAX_RETRIES..." | tee -a "$LOG_FILE"
        
        # 使用更保守的方式安装
        if clawhub install "$skill" --no-input 2>&1 | tee -a "$LOG_FILE"; then
            echo "✅ $skill 安装成功" | tee -a "$LOG_FILE"
            return 0
        else
            echo "⚠️  $skill 安装失败" | tee -a "$LOG_FILE"
            
            # 检查是否是速率限制
            if grep -q "Rate limit exceeded" "$LOG_FILE"; then
                echo "  检测到速率限制，等待10分钟..." | tee -a "$LOG_FILE"
                sleep 600  # 等待10分钟
            fi
            
            ((attempt++))
            if [ $attempt -le $MAX_RETRIES ]; then
                echo "  等待30秒后重试..." | tee -a "$LOG_FILE"
                sleep 30
            fi
        fi
    done
    
    echo "❌ $skill 安装失败（达到重试限制）" | tee -a "$LOG_FILE"
    return 1
}

# 主安装循环
SUCCESS_COUNT=0
FAILED_COUNT=0
FAILED_SKILLS=()

for i in "${!SKILLS_TO_INSTALL[@]}"; do
    skill="${SKILLS_TO_INSTALL[$i]}"
    echo "" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
    echo "[$((i+1))/${#SKILLS_TO_INSTALL[@]}] 处理: $skill" | tee -a "$LOG_FILE"
    
    if install_with_care "$skill"; then
        ((SUCCESS_COUNT++))
    else
        ((FAILED_COUNT++))
        FAILED_SKILLS+=("$skill")
    fi
    
    # 不是最后一个技能，则等待
    if [ $i -lt $((${#SKILLS_TO_INSTALL[@]}-1)) ]; then
        echo "" | tee -a "$LOG_FILE"
        echo "⏳ 等待 $INSTALL_DELAY 秒避免速率限制..." | tee -a "$LOG_FILE"
        
        # 显示倒计时
        for ((sec=INSTALL_DELAY; sec>0; sec--)); do
            printf "\r继续倒计时: %3d 秒" $sec
            sleep 1
        done
        echo ""
    fi
done

# 生成报告
echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "安装完成: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
echo "📊 安装统计:" | tee -a "$LOG_FILE"
echo "  成功安装: $SUCCESS_COUNT 个技能" | tee -a "$LOG_FILE"
echo "  安装失败: $FAILED_COUNT 个技能" | tee -a "$LOG_FILE"

if [ ${#FAILED_SKILLS[@]} -gt 0 ]; then
    echo "  失败技能: ${FAILED_SKILLS[*]}" | tee -a "$LOG_FILE"
fi

# 更新总计数
NEW_COUNT=$(ls -1 /opt/homebrew/lib/node_modules/openclaw/skills/ 2>/dev/null | wc -l)
echo "  当前总数: $NEW_COUNT/100" | tee -a "$LOG_FILE"
echo "  进度: $((NEW_COUNT * 100 / 100))%" | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "💡 建议:" | tee -a "$LOG_FILE"
if [ $SUCCESS_COUNT -eq 0 ]; then
    echo "  检测到严重速率限制，建议:" | tee -a "$LOG_FILE"
    echo "  1. 等待24小时再尝试" | tee -a "$LOG_FILE"
    echo "  2. 联系clawhub支持" | tee -a "$LOG_FILE"
    echo "  3. 考虑手动下载技能" | tee -a "$LOG_FILE"
elif [ $SUCCESS_COUNT -lt 5 ]; then
    echo "  安装进度较慢，建议:" | tee -a "$LOG_FILE"
    echo "  1. 明天再继续安装" | tee -a "$LOG_FILE"
    echo "  2. 增加等待时间到5分钟" | tee -a "$LOG_FILE"
    echo "  3. 分批安装，每天5个技能" | tee -a "$LOG_FILE"
else
    echo "  安装进展良好，建议:" | tee -a "$LOG_FILE"
    echo "  1. 明天继续第2批安装" | tee -a "$LOG_FILE"
    echo "  2. 测试已安装的技能" | tee -a "$LOG_FILE"
    echo "  3. 生成进度报告" | tee -a "$LOG_FILE"
fi

echo "" | tee -a "$LOG_FILE"
echo "📄 详细日志: $LOG_FILE" | tee -a "$LOG_FILE"
echo "🚀 下一步: 运行测试脚本验证安装" | tee -a "$LOG_FILE"