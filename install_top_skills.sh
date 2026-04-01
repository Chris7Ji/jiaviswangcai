#!/bin/bash
# 安装最流行和最有用的10个OpenClaw skill

echo "=========================================="
echo "🤖 开始安装Top 10 OpenClaw Skills"
echo "=========================================="

# 技能列表（基于流行度和实用性）
SKILLS=(
    "github"              # GitHub操作和管理
    "gog"                 # Google Workspace集成
    "feishu-agent"        # 飞书集成
    "healthcheck"         # 系统健康检查
    "summarize"           # 内容摘要
    "video-frames"        # 视频帧提取
    "weather"             # 天气查询
    "wacli"               # WhatsApp集成
    "1password"           # 密码管理
    "apple-reminders"     # 苹果提醒事项
)

# 检查clawhub是否安装
if ! command -v clawhub &> /dev/null; then
    echo "❌ 错误: clawhub未安装"
    echo "请先安装clawhub: npm install -g @openclaw/clawhub"
    exit 1
fi

# 创建技能目录
SKILLS_DIR="/Users/jiyingguo/.openclaw/workspace/skills"
mkdir -p "$SKILLS_DIR"
echo "📁 技能目录: $SKILLS_DIR"

# 安装计数器
INSTALLED=0
FAILED=0

# 安装每个技能
for skill in "${SKILLS[@]}"; do
    echo ""
    echo "🔧 正在安装: $skill"
    echo "------------------------------------------"
    
    # 检查是否已安装
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "✅ $skill 已安装，跳过..."
        continue
    fi
    
    # 尝试安装
    if clawhub install "$skill" --dir "$SKILLS_DIR"; then
        echo "✅ $skill 安装成功"
        ((INSTALLED++))
        
        # 显示技能信息
        if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
            echo "📄 技能描述:"
            head -5 "$SKILLS_DIR/$skill/SKILL.md" | grep -v "^#" | sed 's/^/    /'
        fi
    else
        echo "❌ $skill 安装失败"
        ((FAILED++))
    fi
    
    # 避免速率限制，添加延迟
    sleep 2
done

echo ""
echo "=========================================="
echo "📊 安装完成报告"
echo "=========================================="
echo "✅ 成功安装: $INSTALLED 个技能"
echo "❌ 安装失败: $FAILED 个技能"
echo "📁 技能目录: $SKILLS_DIR"

# 列出已安装的技能
echo ""
echo "📋 已安装技能列表:"
ls -la "$SKILLS_DIR" | grep -E "^d" | awk '{print "  • " $9}'

echo ""
echo "💡 使用提示:"
echo "1. 技能文件位于: $SKILLS_DIR"
echo "2. 每个技能都有SKILL.md文件说明使用方法"
echo "3. 重启OpenClaw或重新加载技能配置"
echo "4. 使用 'clawhub update' 更新所有技能"

# 创建技能索引文件
cat > "$SKILLS_DIR/README.md" << EOF
# OpenClaw Skills 目录

本目录包含已安装的OpenClaw技能。

## 已安装技能 ($(date '+%Y-%m-%d %H:%M:%S'))

$(for skill in "${SKILLS[@]}"; do
    if [ -d "$SKILLS_DIR/$skill" ]; then
        echo "### $skill"
        if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
            grep -m1 "^#" "$SKILLS_DIR/$skill/SKILL.md" | sed 's/^# //'
        fi
        echo ""
    fi
done)

## 管理命令

\`\`\`bash
# 更新所有技能
clawhub update --dir "$SKILLS_DIR"

# 搜索新技能
clawhub search <关键词>

# 安装新技能
clawhub install <技能名> --dir "$SKILLS_DIR"
\`\`\`

## 注意事项

1. 技能可能需要额外的配置才能正常工作
2. 某些技能需要API密钥或认证
3. 定期更新技能以获取最新功能
4. 查看每个技能的SKILL.md文件了解详细用法
EOF

echo ""
echo "📝 已创建技能索引: $SKILLS_DIR/README.md"
echo "🎉 安装完成！"