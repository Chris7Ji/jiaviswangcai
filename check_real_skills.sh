#!/bin/bash
# 真实技能状态检查

echo "========================================"
echo "🔍 OpenClaw真实技能状态检查"
echo "========================================"

SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
echo "技能目录: $SKILLS_DIR"
echo ""

# 检查目录是否存在
if [ ! -d "$SKILLS_DIR" ]; then
    echo "❌ 技能目录不存在"
    exit 1
fi

# 统计
TOTAL_SKILLS=$(ls -1 "$SKILLS_DIR" 2>/dev/null | wc -l)
echo "📊 统计信息:"
echo "  总技能数: $TOTAL_SKILLS"
echo "  目标数量: 100"
echo "  完成进度: $((TOTAL_SKILLS * 100 / 100))%"
echo ""

# 检查关键技能
echo "🎯 关键技能状态:"

check_skill() {
    local skill=$1
    local display_name=$2
    
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "  ✅ $display_name: 已安装"
        
        # 检查是否有可执行文件
        if command -v "$skill" &> /dev/null; then
            echo "     命令可用: $(which $skill)"
        elif [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
            echo "     查看文档: cat $SKILLS_DIR/$skill/SKILL.md | head -5"
        else
            echo "     需要配置或特殊调用"
        fi
    else
        echo "  ❌ $display_name: 未安装"
    fi
}

check_skill "github" "GitHub集成"
check_skill "gog" "Google Workspace"
check_skill "healthcheck" "系统健康检查"
check_skill "summarize" "内容摘要"
check_skill "video-frames" "视频帧提取"
check_skill "wacli" "WhatsApp集成"
check_skill "1password" "密码管理"
check_skill "apple-reminders" "苹果提醒"
check_skill "gh-issues" "GitHub Issue自动化"
check_skill "weather" "天气查询"

echo ""
echo "🔧 测试几个可用技能:"

# 测试gog
echo ""
echo "1. 测试gog (Google Workspace):"
if command -v gog &> /dev/null; then
    gog --version
else
    echo "  gog命令不可用"
fi

# 测试summarize
echo ""
echo "2. 测试summarize (内容摘要):"
if command -v summarize &> /dev/null; then
    summarize --version 2>/dev/null || echo "  版本检查失败，但命令存在"
else
    echo "  summarize命令不可用"
fi

# 测试clawhub
echo ""
echo "3. 测试clawhub (技能管理):"
if command -v clawhub &> /dev/null; then
    clawhub --cli-version
else
    echo "  clawhub命令不可用"
fi

echo ""
echo "📋 技能分类统计:"

# 分类统计
count_by_category() {
    local category=$1
    local pattern=$2
    
    count=$(ls -1 "$SKILLS_DIR" 2>/dev/null | grep -i "$pattern" | wc -l)
    echo "  $category: $count 个技能"
}

count_by_category "开发工具" "git\|code\|docker\|node\|python"
count_by_category "云服务" "gog\|aws\|azure\|gcp"
count_by_category "通信工具" "wacli\|discord\|slack\|telegram"
count_by_category "多媒体" "video\|audio\|image\|camera"
count_by_category "生产力" "reminder\|todo\|note\|calendar\|weather"
count_by_category "AI/ML" "ai\|ml\|openai\|gemini"

echo ""
echo "💡 建议:"
if [ $TOTAL_SKILLS -ge 50 ]; then
    echo "  1. 你已经有强大的技能基础 (52个技能)"
    echo "  2. 重点深度使用现有技能，而非追求数量"
    echo "  3. 学习组合使用多个技能完成复杂任务"
    echo "  4. 考虑clawhub速率限制，缓慢增加新技能"
else
    echo "  1. 继续安装核心技能"
    echo "  2. 测试每个新安装的技能"
    echo "  3. 建立技能使用文档"
fi

echo ""
echo "🚀 下一步行动建议:"
echo "  运行: ./scripts/monitor_progress.sh 查看详细进度"
echo "  运行: ./scripts/generate_report.sh 生成报告"
echo "  运行: ./today_one_skill.sh 尝试安装1个新技能"