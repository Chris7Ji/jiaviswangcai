#!/bin/bash

# Tavily技能明天自动重试脚本
# 执行时间：明天早上08:00

echo "=== Tavily技能安装自动重试 ==="
echo "开始时间: $(date)"
echo "目标技能: openclaw-tavily-search, tavily-tool, tavily-skill"
echo ""

# 日志文件
LOG_FILE="/Users/jiyingguo/.openclaw/workspace/tavily_retry_$(date +%Y%m%d).log"
echo "=== Tavily安装重试日志 $(date) ===" > "$LOG_FILE"

# 要尝试的技能（按优先级）
SKILLS=("openclaw-tavily-search" "tavily-tool" "tavily-skill")

# 检查clawhub
if ! command -v clawhub &> /dev/null; then
    echo "错误: clawhub CLI未安装" | tee -a "$LOG_FILE"
    exit 1
fi

# 显示当前已安装技能
echo "" | tee -a "$LOG_FILE"
echo "=== 当前已安装技能 ===" | tee -a "$LOG_FILE"
clawhub list 2>&1 | tee -a "$LOG_FILE"

# 尝试安装每个技能
success_count=0
for skill in "${SKILLS[@]}"; do
    echo "" | tee -a "$LOG_FILE"
    echo "=== 尝试安装: $skill ===" | tee -a "$LOG_FILE"
    echo "时间: $(date)" | tee -a "$LOG_FILE"
    
    # 尝试安装
    OUTPUT=$(clawhub install "$skill" 2>&1)
    EXIT_CODE=$?
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ 成功安装: $skill" | tee -a "$LOG_FILE"
        echo "输出: $OUTPUT" | tee -a "$LOG_FILE"
        success_count=$((success_count + 1))
        
        # 验证安装
        echo "" | tee -a "$LOG_FILE"
        echo "=== 验证安装 ===" | tee -a "$LOG_FILE"
        clawhub list 2>&1 | tee -a "$LOG_FILE"
        
        # 检查技能目录
        SKILL_DIR="/Users/jiyingguo/.openclaw/workspace/skills/$skill"
        if [ -d "$SKILL_DIR" ]; then
            echo "✅ 技能目录已创建: $SKILL_DIR" | tee -a "$LOG_FILE"
            ls -la "$SKILL_DIR/" | tee -a "$LOG_FILE"
        fi
        
        # 生成成功通知
        create_success_notification "$skill"
        
        # 如果成功安装一个，可以停止尝试其他
        break
    else
        echo "❌ 安装失败: $skill" | tee -a "$LOG_FILE"
        echo "错误信息: $OUTPUT" | tee -a "$LOG_FILE"
    fi
done

# 最终结果
echo "" | tee -a "$LOG_FILE"
echo "=== 最终结果 ===" | tee -a "$LOG_FILE"
echo "尝试技能数: ${#SKILLS[@]}" | tee -a "$LOG_FILE"
echo "成功安装数: $success_count" | tee -a "$LOG_FILE"
echo "完成时间: $(date)" | tee -a "$LOG_FILE"

if [ $success_count -gt 0 ]; then
    echo "🎉 Tavily技能安装成功！" | tee -a "$LOG_FILE"
else
    echo "⚠️  所有尝试都失败，clawhub速率限制可能仍然存在" | tee -a "$LOG_FILE"
    echo "建议：" | tee -a "$LOG_FILE"
    echo "1. 等待更长时间后重试" | tee -a "$LOG_FILE"
    echo "2. 使用替代搜索方案（Brave搜索等）" | tee -a "$LOG_FILE"
    echo "3. 联系clawhub支持了解限制详情" | tee -a "$LOG_FILE"
fi

# 生成通知文件
create_notification_file

exit $([ $success_count -gt 0 ] && echo 0 || echo 1)

# 函数：创建成功通知
create_success_notification() {
    local skill=$1
    local notification_file="/Users/jiyingguo/.openclaw/workspace/tavily_install_success.txt"
    
    cat > "$notification_file" << EOF
🎉 Tavily技能安装成功通知

时间: $(date)
成功安装的技能: $skill

安装详情:
- 技能名称: $skill
- 安装时间: $(date)
- 状态: ✅ 成功安装

验证信息:
$(clawhub list 2>/dev/null)

下一步建议:
1. 测试Tavily搜索功能
2. 查看技能文档: ~/.openclaw/workspace/skills/$skill/SKILL.md
3. 开始使用AI优化搜索功能

日志文件: $LOG_FILE
EOF
}

# 函数：创建通知文件
create_notification_file() {
    local summary_file="/Users/jiyingguo/.openclaw/workspace/tavily_retry_summary.txt"
    
    cat > "$summary_file" << EOF
Tavily安装重试摘要

执行时间: $(date)
尝试技能: ${SKILLS[*]}
成功安装: $success_count/${#SKILLS[@]}

详细结果:
$(tail -50 "$LOG_FILE" 2>/dev/null)

建议后续操作:
$([ $success_count -gt 0 ] && echo "1. 开始使用Tavily搜索功能" || echo "1. 考虑使用替代搜索方案")
2. 查看完整日志: $LOG_FILE
3. 如需进一步帮助，请提供反馈

已安装技能列表:
$(clawhub list 2>/dev/null)
EOF
}