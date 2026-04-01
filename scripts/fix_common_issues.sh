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
