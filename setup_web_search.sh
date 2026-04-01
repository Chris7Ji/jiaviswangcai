#!/bin/bash
# OpenClaw 网络搜索功能快速设置脚本

echo "========================================"
echo "🌐 OpenClaw 网络搜索功能设置"
echo "========================================"

# 颜色定义
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
    
    echo -e "${color}[$(date '+%H:%M:%S')] $level: $message${NC}"
}

# 检查当前状态
check_current_status() {
    log "INFO" "检查当前OpenClaw状态..."
    
    # 检查网关状态
    if openclaw gateway status 2>/dev/null | grep -q "running"; then
        log "SUCCESS" "OpenClaw网关正在运行"
    else
        log "WARNING" "OpenClaw网关未运行"
    fi
    
    # 检查配置
    if [ -f "/Users/jiyingguo/.openclaw/openclaw.json" ]; then
        log "SUCCESS" "配置文件存在"
        
        # 检查是否已有web配置
        if grep -q "web\|brave\|search" /Users/jiyingguo/.openclaw/openclaw.json; then
            log "INFO" "检测到可能的web配置"
        else
            log "WARNING" "未检测到web搜索配置"
        fi
    else
        log "ERROR" "配置文件不存在"
    fi
    
    # 检查环境变量
    if [ -n "$BRAVE_API_KEY" ]; then
        log "SUCCESS" "BRAVE_API_KEY环境变量已设置"
        echo "  Key预览: ${BRAVE_API_KEY:0:10}..."
    else
        log "WARNING" "BRAVE_API_KEY环境变量未设置"
    fi
}

# 显示API密钥获取指南
show_api_key_guide() {
    echo ""
    echo "========================================"
    echo "🔑 获取Brave Search API密钥"
    echo "========================================"
    echo ""
    echo "请按以下步骤获取API密钥:"
    echo ""
    echo "1. 🌐 访问: https://brave.com/search/api/"
    echo "2. 📝 点击 'Get Started' 或 'Sign Up'"
    echo "3. 📧 创建账户并验证邮箱"
    echo "4. 🔑 在控制台获取API密钥"
    echo "5. 💾 复制密钥备用"
    echo ""
    echo "💡 提示:"
    echo "   • 免费套餐通常有使用限制"
    echo "   • 可能需要信用卡验证（免费套餐通常不需要）"
    echo "   • 密钥格式类似: 'BSA-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'"
    echo ""
    
    read -p "是否已获取API密钥? (y/n): " has_key
    
    if [[ $has_key =~ ^[Yy]$ ]]; then
        read -p "请输入您的Brave Search API密钥: " api_key
        
        if [ -n "$api_key" ]; then
            # 临时设置环境变量
            export BRAVE_API_KEY="$api_key"
            log "SUCCESS" "API密钥已设置为环境变量"
            
            # 询问是否保存到配置文件
            read -p "是否保存到OpenClaw配置文件? (y/n): " save_config
            
            if [[ $save_config =~ ^[Yy]$ ]]; then
                configure_openclaw "$api_key"
            fi
        else
            log "ERROR" "未输入API密钥"
        fi
    else
        log "INFO" "请先获取API密钥，然后重新运行此脚本"
        echo ""
        echo "📋 备用方案:"
        echo "   1. 使用web_fetch工具（无需API密钥）"
        echo "   2. 配置其他搜索提供商"
        echo "   3. 使用已有技能进行信息获取"
    fi
}

# 配置OpenClaw
configure_openclaw() {
    local api_key=$1
    
    log "INFO" "配置OpenClaw web搜索..."
    
    # 创建临时配置文件
    TEMP_CONFIG="/tmp/openclaw_web_config.json"
    
    cat > "$TEMP_CONFIG" << EOF
{
  "web": {
    "brave": {
      "apiKey": "${api_key}"
    },
    "fetch": {
      "timeout": 30000,
      "maxRedirects": 5,
      "userAgent": "OpenClaw/2026.2.26"
    }
  }
}
EOF
    
    log "INFO" "临时配置文件已创建: $TEMP_CONFIG"
    echo "配置内容:"
    cat "$TEMP_CONFIG"
    echo ""
    
    # 询问用户确认
    read -p "是否应用此配置? (y/n): " apply_config
    
    if [[ $apply_config =~ ^[Yy]$ ]]; then
        log "INFO" "正在配置OpenClaw..."
        
        # 这里需要实际配置OpenClaw
        # 由于openclaw configure是交互式的，我们提供指导
        
        echo ""
        echo "📝 请手动执行以下命令:"
        echo "----------------------------------------"
        echo "openclaw configure --section web"
        echo "----------------------------------------"
        echo ""
        echo "在配置向导中:"
        echo "1. 选择 'web' 配置部分"
        echo "2. 输入您的API密钥: ${api_key:0:10}..."
        echo "3. 按照提示完成配置"
        echo ""
        
        read -p "按回车键继续查看配置说明..."
        
        show_configuration_instructions "$api_key"
    else
        log "INFO" "配置已取消"
    fi
}

# 显示配置说明
show_configuration_instructions() {
    local api_key=$1
    
    echo ""
    echo "========================================"
    echo "⚙️  OpenClaw Web搜索配置说明"
    echo "========================================"
    echo ""
    echo "方法1: 使用命令行配置（推荐）"
    echo "----------------------------------------"
    echo "运行: openclaw configure --section web"
    echo "然后按照向导输入API密钥"
    echo ""
    
    echo "方法2: 手动编辑配置文件"
    echo "----------------------------------------"
    echo "编辑: /Users/jiyingguo/.openclaw/openclaw.json"
    echo "在文件末尾添加:"
    cat << 'EOF'
  "web": {
    "brave": {
      "apiKey": "YOUR_API_KEY_HERE"
    }
  }
EOF
    echo ""
    
    echo "方法3: 环境变量配置"
    echo "----------------------------------------"
    echo "在 ~/.zshrc 或 ~/.bashrc 中添加:"
    echo "export BRAVE_API_KEY=\"${api_key:0:10}...\""
    echo ""
    echo "然后运行: source ~/.zshrc"
    echo ""
    
    echo "🔧 配置完成后，重启OpenClaw网关:"
    echo "----------------------------------------"
    echo "openclaw gateway restart"
    echo ""
}

# 测试配置
test_configuration() {
    echo ""
    echo "========================================"
    echo "🧪 测试网络搜索配置"
    echo "========================================"
    echo ""
    
    log "INFO" "测试步骤:"
    echo "1. 确保OpenClaw网关正在运行"
    echo "2. 在OpenClaw会话中尝试:"
    echo "   web_search query=\"test search\""
    echo "3. 如果成功，会返回搜索结果"
    echo "4. 如果失败，查看错误信息"
    echo ""
    
    read -p "是否现在测试? (y/n): " run_test
    
    if [[ $run_test =~ ^[Yy]$ ]]; then
        log "INFO" "启动测试..."
        
        # 检查网关状态
        if openclaw gateway status 2>/dev/null | grep -q "running"; then
            log "SUCCESS" "网关正在运行，可以开始测试"
            echo ""
            echo "💡 在OpenClaw会话中输入:"
            echo "   web_search query=\"OpenClaw skills\""
            echo ""
            echo "或者尝试:"
            echo "   web_fetch url=\"https://example.com\""
        else
            log "ERROR" "网关未运行，请先启动:"
            echo "   openclaw gateway start"
        fi
    fi
}

# 显示替代方案
show_alternatives() {
    echo ""
    echo "========================================"
    echo "🔄 网络搜索替代方案"
    echo "========================================"
    echo ""
    
    echo "方案A: 使用web_fetch工具（无需API密钥）"
    echo "----------------------------------------"
    echo "命令: web_fetch url=\"https://example.com\""
    echo "用途: 直接抓取网页内容"
    echo "限制: 只能获取特定网页，不能进行关键词搜索"
    echo ""
    
    echo "方案B: 使用已有技能"
    echo "----------------------------------------"
    echo "1. summarize技能: 摘要网页内容"
    echo "   summarize https://example.com"
    echo ""
    echo "2. 专用信息获取技能:"
    echo "   • 天气查询"
    echo "   • 新闻获取"
    echo "   • 技术文档查询"
    echo ""
    
    echo "方案C: 浏览器自动化"
    echo "----------------------------------------"
    echo "需要Chrome扩展支持"
    echo "命令: browser action=\"open\" targetUrl=\"https://google.com\""
    echo ""
}

# 主菜单
show_main_menu() {
    echo ""
    echo "========================================"
    echo "📋 主菜单 - 选择操作"
    echo "========================================"
    echo ""
    echo "1. 🔍 检查当前状态"
    echo "2. 🔑 获取并配置API密钥"
    echo "3. ⚙️  查看配置说明"
    echo "4. 🧪 测试配置"
    echo "5. 🔄 查看替代方案"
    echo "6. 📖 查看详细指南"
    echo "7. 🚪 退出"
    echo ""
}

# 主程序
main() {
    echo "欢迎使用OpenClaw网络搜索配置工具"
    echo "当前时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    while true; do
        show_main_menu
        
        read -p "请输入选择 (1-7): " choice
        
        case $choice in
            1)
                check_current_status
                ;;
            2)
                show_api_key_guide
                ;;
            3)
                show_configuration_instructions "your_api_key"
                ;;
            4)
                test_configuration
                ;;
            5)
                show_alternatives
                ;;
            6)
                echo ""
                echo "详细指南位于: /Users/jiyingguo/.openclaw/workspace/web_search_setup_guide.md"
                echo "使用命令查看: cat /Users/jiyingguo/.openclaw/workspace/web_search_setup_guide.md | less"
                ;;
            7)
                echo "感谢使用，再见！"
                exit 0
                ;;
            *)
                echo "❌ 无效选择"
                ;;
        esac
        
        echo ""
        read -p "按回车键继续..."
    done
}

# 运行主程序
main "$@"