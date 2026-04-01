#!/bin/bash

# Brave搜索API配置脚本
# 使用方法：./configure_brave_search.sh YOUR_API_KEY

echo "=== Brave搜索API配置 ==="
echo "开始时间: $(date)"
echo ""

if [ $# -eq 0 ]; then
    echo "❌ 错误：请提供Brave API密钥"
    echo "用法: $0 YOUR_BRAVE_API_KEY"
    echo ""
    echo "获取API密钥："
    echo "1. 访问 https://brave.com/search/api/"
    echo "2. 注册/登录Brave账户"
    echo "3. 创建API密钥"
    echo "4. 复制密钥并运行此脚本"
    exit 1
fi

BRAVE_API_KEY="$1"
CONFIG_FILE="$HOME/.openclaw/config.json"
BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"

echo "🔑 提供的API密钥: ${BRAVE_API_KEY:0:8}******"
echo ""

# 备份现有配置
if [ -f "$CONFIG_FILE" ]; then
    echo "📁 备份现有配置: $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# 检查openclaw命令
if ! command -v openclaw &> /dev/null; then
    echo "❌ 错误：openclaw命令未找到"
    echo "请确保OpenClaw已正确安装"
    exit 1
fi

echo "🔄 配置OpenClaw web_search..."
echo ""

# 创建临时配置脚本
TEMP_SCRIPT=$(mktemp)
cat > "$TEMP_SCRIPT" << EOF
#!/usr/bin/env node
// OpenClaw配置脚本
const fs = require('fs');
const path = require('path');

const configPath = path.join(process.env.HOME, '.openclaw', 'config.json');
let config = {};

// 读取现有配置
try {
    if (fs.existsSync(configPath)) {
        config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    }
} catch (e) {
    console.log('读取现有配置失败，创建新配置');
}

// 设置web配置
if (!config.web) {
    config.web = {};
}

config.web.braveApiKey = process.argv[2];

// 写入配置
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
console.log('✅ 配置已保存到:', configPath);
console.log('🔑 API密钥已设置（部分显示）:', process.argv[2].substring(0, 8) + '******');
EOF

# 运行配置脚本
node "$TEMP_SCRIPT" "$BRAVE_API_KEY"
CONFIG_EXIT_CODE=$?

# 清理临时文件
rm -f "$TEMP_SCRIPT"

if [ $CONFIG_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "✅ Brave API密钥配置成功！"
    echo ""
    
    # 重启网关
    echo "🔄 重启OpenClaw网关..."
    if openclaw gateway restart 2>/dev/null; then
        echo "✅ 网关重启成功"
    else
        echo "⚠️  网关重启失败，请手动运行: openclaw gateway restart"
    fi
    
    echo ""
    echo "🎉 配置完成！您现在可以："
    echo ""
    echo "1. 让我帮您搜索（告诉我搜索需求）"
    echo "2. 使用web_search工具"
    echo "3. 测试搜索功能"
    echo ""
    echo "📋 验证配置："
    echo "运行: openclaw gateway status"
    echo ""
    echo "📁 配置文件位置: $CONFIG_FILE"
    echo "📁 备份文件位置: $BACKUP_FILE"
    
    # 创建使用示例
    cat > "$HOME/.openclaw/brave_search_examples.md" << EOF
# Brave搜索使用示例

## 通过我使用（最简单）：
告诉我您的搜索需求，例如：
- "搜索人工智能最新发展"
- "查找OpenClaw文档"
- "了解Tavily搜索API"

## 配置验证：
\`\`\`bash
# 检查网关状态
openclaw gateway status

# 测试配置
cat ~/.openclaw/config.json | grep -A2 -B2 brave
\`\`\`

## 功能特点：
✅ 高质量搜索结果
✅ 中文支持优秀
✅ 隐私保护良好
✅ 免费额度充足
✅ 响应速度快

## 免费额度：
- 每月免费搜索次数充足
- 适合个人和轻度使用
- 如需更多可升级计划

## 问题排查：
如果搜索失败，请：
1. 检查网关状态：\`openclaw gateway status\`
2. 验证API密钥：访问 https://brave.com/search/api/
3. 重启网关：\`openclaw gateway restart\`
4. 联系我获取帮助
EOF
    
    echo ""
    echo "📖 使用示例已保存: $HOME/.openclaw/brave_search_examples.md"
    
else
    echo "❌ 配置失败，退出码: $CONFIG_EXIT_CODE"
    echo ""
    echo "💡 手动配置方法："
    echo "1. 运行: openclaw configure --section web"
    echo "2. 输入Brave API密钥"
    echo "3. 按提示完成配置"
    exit 1
fi

exit 0