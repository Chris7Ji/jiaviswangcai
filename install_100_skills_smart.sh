#!/bin/bash
# OpenClaw 100个最流行技能智能安装脚本
# 采用分批安装、智能重试、进度跟踪策略

set -e

echo "================================================================"
echo "🚀 OpenClaw 100个最流行技能智能安装系统"
echo "================================================================"

# 配置
SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
WORKSPACE="/Users/jiyingguo/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs"
REPORT_DIR="$WORKSPACE/reports"
TARGET_COUNT=100
BATCH_SIZE=5  # 每批安装数量
RETRY_LIMIT=3 # 重试次数
DELAY_BETWEEN_BATCHES=30 # 批次间延迟（秒）
DELAY_BETWEEN_SKILLS=5   # 技能间延迟（秒）

# 创建目录
mkdir -p "$LOG_DIR" "$REPORT_DIR"

# 时间戳
TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$LOG_DIR/skill_install_${TIMESTAMP}.log"
REPORT_FILE="$REPORT_DIR/skill_install_report_${TIMESTAMP}.md"

# 初始化统计
TOTAL_INSTALLED=0
TOTAL_SUCCESS=0
TOTAL_FAILED=0
START_TIME=$(date +%s)

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查clawhub
check_clawhub() {
    if ! command -v clawhub &> /dev/null; then
        log "❌ 错误: clawhub未安装"
        log "请先安装: npm install -g @openclaw/clawhub"
        exit 1
    fi
    log "✅ clawhub已安装: $(clawhub --version | head -1)"
}

# 获取已安装技能数量
get_installed_count() {
    if [ -d "$SKILLS_DIR" ]; then
        ls -1 "$SKILLS_DIR" | grep -v '^\.' | wc -l | tr -d ' '
    else
        echo "0"
    fi
}

# 定义最流行的100个技能（分类）
define_popular_skills() {
    # 核心技能（必须安装）
    CORE_SKILLS=(
        "github" "gog" "healthcheck" "summarize" "video-frames"
        "weather" "wacli" "1password" "apple-reminders" "gh-issues"
        "clawhub" "skill-creator" "coding-agent" "nano-pdf" "camsnap"
    )
    
    # 开发工具
    DEV_SKILLS=(
        "git" "docker" "kubernetes" "vscode" "python" "nodejs"
        "typescript" "react" "vue" "angular" "webpack" "jest"
        "eslint" "prettier" "babel" "rollup" "vite" "npm"
        "yarn" "pnpm" "gradle" "maven" "make" "cmake"
    )
    
    # 云服务
    CLOUD_SKILLS=(
        "aws" "azure" "gcp" "digitalocean" "vercel" "netlify"
        "cloudflare" "heroku" "firebase" "supabase" "mongodb"
        "postgresql" "mysql" "redis" "elasticsearch" "kafka"
    )
    
    # 通信工具
    COMM_SKILLS=(
        "discord" "slack" "telegram" "signal" "imessage"
        "feishu" "dingtalk" "teams" "zoom" "skype"
        "matrix" "irc" "mastodon" "twitter" "linkedin"
    )
    
    # 多媒体
    MEDIA_SKILLS=(
        "ffmpeg" "image-processing" "audio-processing" "video-editing"
        "screenshot" "screen-recorder" "gif-creator" "pdf-tools"
        "ocr" "speech-recognition" "text-to-speech" "audio-converter"
    )
    
    # 生产力
    PRODUCTIVITY_SKILLS=(
        "calendar" "todo" "notes" "bookmarks" "rss-reader"
        "time-tracker" "pomodoro" "habit-tracker" "finance"
        "password-manager" "backup" "sync" "automation"
    )
    
    # AI/ML
    AI_SKILLS=(
        "openai" "anthropic" "gemini" "cohere" "huggingface"
        "llama" "stable-diffusion" "dalle" "midjourney"
        "ai-assistant" "chatbot" "nlp-tools" "computer-vision"
    )
    
    # 组合所有技能
    ALL_SKILLS=(
        "${CORE_SKILLS[@]}"
        "${DEV_SKILLS[@]}"
        "${CLOUD_SKILLS[@]}"
        "${COMM_SKILLS[@]}"
        "${MEDIA_SKILLS[@]}"
        "${PRODUCTIVITY_SKILLS[@]}"
        "${AI_SKILLS[@]}"
    )
    
    # 去重并限制数量
    echo "${ALL_SKILLS[@]}" | tr ' ' '\n' | sort -u | head -100
}

# 检查技能是否已安装
is_skill_installed() {
    local skill="$1"
    [ -d "$SKILLS_DIR/$skill" ] && return 0 || return 1
}

# 安装单个技能（带重试）
install_skill_with_retry() {
    local skill="$1"
    local attempt=1
    
    while [ $attempt -le $RETRY_LIMIT ]; do
        log "🔧 安装 $skill (尝试 $attempt/$RETRY_LIMIT)"
        
        if clawhub install "$skill" 2>&1 | tee -a "$LOG_FILE"; then
            log "✅ $skill 安装成功"
            return 0
        else
            log "⚠️  $skill 安装失败，等待重试..."
            sleep $((attempt * 5)) # 指数退避
            ((attempt++))
        fi
    done
    
    log "❌ $skill 安装失败（达到重试限制）"
    return 1
}

# 安装一批技能
install_batch() {
    local batch_skills=("$@")
    local batch_success=0
    local batch_failed=0
    
    for skill in "${batch_skills[@]}"; do
        # 检查是否已安装
        if is_skill_installed "$skill"; then
            log "✅ $skill 已安装，跳过"
            ((TOTAL_INSTALLED++))
            continue
        fi
        
        # 安装技能
        if install_skill_with_retry "$skill"; then
            ((batch_success++))
            ((TOTAL_SUCCESS++))
        else
            ((batch_failed++))
            ((TOTAL_FAILED++))
        fi
        
        # 技能间延迟
        if [ ${#batch_skills[@]} -gt 1 ]; then
            sleep $DELAY_BETWEEN_SKILLS
        fi
    done
    
    echo "$batch_success $batch_failed"
}

# 生成报告
generate_report() {
    local end_time=$(date +%s)
    local duration=$((end_time - START_TIME))
    
    cat > "$REPORT_FILE" << EOF
# OpenClaw 100个技能安装报告

## 📊 安装统计

| 项目 | 数量 | 说明 |
|------|------|------|
| 目标技能数量 | $TARGET_COUNT | 计划安装总数 |
| 初始已安装 | $(get_installed_count) | 安装前已存在的技能 |
| 本次成功安装 | $TOTAL_SUCCESS | 本次安装成功的技能 |
| 本次安装失败 | $TOTAL_FAILED | 本次安装失败的技能 |
| **总计安装** | **$(( $(get_installed_count) + TOTAL_SUCCESS ))** | **当前总安装数** |

## ⏱️ 时间信息

- **开始时间**: $(date -r $START_TIME '+%Y-%m-%d %H:%M:%S')
- **结束时间**: $(date -r $end_time '+%Y-%m-%d %H:%M:%S')
- **总耗时**: $((duration / 60))分钟$((duration % 60))秒

## 📈 进度分析

### 安装进度
$(( ($(get_installed_count) + TOTAL_SUCCESS) * 100 / TARGET_COUNT ))% 完成 ($(( $(get_installed_count) + TOTAL_SUCCESS ))/$TARGET_COUNT)

### 成功率
$(( TOTAL_SUCCESS * 100 / (TOTAL_SUCCESS + TOTAL_FAILED) ))% ($TOTAL_SUCCESS/$((TOTAL_SUCCESS + TOTAL_FAILED)))

## 🎯 技能分类

### 1. 核心技能 (15个)
GitHub集成、Google Workspace、系统健康检查、内容摘要、视频处理等

### 2. 开发工具 (25个)
Docker、Kubernetes、VSCode、Python、Node.js、TypeScript等

### 3. 云服务 (15个)
AWS、Azure、GCP、Vercel、Netlify、Firebase等

### 4. 通信工具 (15个)
Discord、Slack、Telegram、飞书、钉钉、Zoom等

### 5. 多媒体处理 (10个)
FFmpeg、图像处理、音频处理、视频编辑等

### 6. 生产力工具 (10个)
日历、待办、笔记、时间追踪、习惯追踪等

### 7. AI/机器学习 (10个)
OpenAI、Anthropic、Gemini、Hugging Face、Stable Diffusion等

## 🔧 后续步骤

### 1. 验证安装
\`\`\`bash
# 查看技能总数
ls -1 "$SKILLS_DIR" | wc -l

# 测试关键技能
weather Shanghai
summarize --help
github --version
\`\`\`

### 2. 配置关键技能
\`\`\`bash
# Google Workspace
gog auth manage

# GitHub
github auth login

# 1Password
op signin
\`\`\`

### 3. 技能管理
\`\`\`bash
# 更新所有技能
clawhub update

# 搜索新技能
clawhub search "关键词"

# 查看技能文档
cat "$SKILLS_DIR/github/SKILL.md" | head -20
\`\`\`

## 📋 详细日志

安装详细日志位于: \`$LOG_FILE\`

## 💡 使用建议

1. **逐步学习**: 不要一次性学习所有技能
2. **按需使用**: 根据任务类型选择相应技能
3. **组合使用**: 多个技能组合完成复杂任务
4. **社区支持**: 访问 https://discord.com/invite/clawd

---

**报告生成时间**: $(date '+%Y-%m-%d %H:%M:%S')

> 💡 提示: 拥有100个技能意味着你拥有了一个强大的自动化生态系统！
EOF
    
    log "📄 报告已生成: $REPORT_FILE"
}

# 主函数
main() {
    log "开始安装流程..."
    
    # 检查环境
    check_clawhub
    
    # 获取初始状态
    INITIAL_COUNT=$(get_installed_count)
    log "初始已安装技能: $INITIAL_COUNT 个"
    
    if [ $INITIAL_COUNT -ge $TARGET_COUNT ]; then
        log "🎉 已经达到目标 $TARGET_COUNT 个技能!"
        generate_report
        exit 0
    fi
    
    # 获取技能列表
    log "获取最流行的100个技能列表..."
    read -r -a ALL_SKILLS <<< "$(define_popular_skills)"
    log "找到 ${#ALL_SKILLS[@]} 个候选技能"
    
    # 过滤已安装的技能
    SKILLS_TO_INSTALL=()
    for skill in "${ALL_SKILLS[@]}"; do
        if ! is_skill_installed "$skill"; then
            SKILLS_TO_INSTALL+=("$skill")
        fi
    done
    
    NEED_TO_INSTALL=${#SKILLS_TO_INSTALL[@]}
    log "需要安装 $NEED_TO_INSTALL 个新技能"
    
    if [ $NEED_TO_INSTALL -eq 0 ]; then
        log "✅ 所有流行技能都已安装!"
        generate_report
        exit 0
    fi
    
    # 分批安装
    log "开始分批安装 (每批 $BATCH_SIZE 个技能)..."
    
    for ((i=0; i<${#SKILLS_TO_INSTALL[@]}; i+=BATCH_SIZE)); do
        batch=("${SKILLS_TO_INSTALL[@]:i:BATCH_SIZE}")
        batch_num=$((i/BATCH_SIZE + 1))
        total_batches=$(( (${#SKILLS_TO_INSTALL[@]} + BATCH_SIZE - 1) / BATCH_SIZE ))
        
        log "📦 批次 $batch_num/$total_batches: ${batch[*]}"
        
        read batch_success batch_failed <<< $(install_batch "${batch[@]}")
        
        log "批次完成: 成功 $batch_success, 失败 $batch_failed"
        
        # 批次间延迟（最后一个批次除外）
        if [ $((i + BATCH_SIZE)) -lt ${#SKILLS_TO_INSTALL[@]} ]; then
            log "⏳ 等待 $DELAY_BETWEEN_BATCHES 秒后继续下一批..."
            sleep $DELAY_BETWEEN_BATCHES
        fi
    done
    
    # 生成最终报告
    log "安装完成，生成报告..."
    generate_report
    
    # 最终统计
    FINAL_COUNT=$(get_installed_count)
    log "================================================================"
    log "🎉 安装完成!"
    log "   初始技能: $INITIAL_COUNT"
    log "   本次成功: $TOTAL_SUCCESS"
    log "   本次失败: $TOTAL_FAILED"
    log "   最终总数: $FINAL_COUNT"
    log "   目标达成: $((FINAL_COUNT * 100 / TARGET_COUNT))%"
    log "================================================================"
    log "📄 详细报告: $REPORT_FILE"
    log "📋 安装日志: $LOG_FILE"
}

# 运行主函数
main "$@"