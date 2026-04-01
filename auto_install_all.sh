#!/bin/bash
# 自动安装全部系统

echo "开始一键安装全部系统..."
echo ""

# 创建目录
mkdir -p /Users/jiyingguo/.openclaw/workspace/{scripts,tests,logs,reports}

# 运行主脚本并自动选择选项5
cd /Users/jiyingguo/.openclaw/workspace
chmod +x complete_100_skills_system.sh

# 使用expect自动输入选项5
cat > /tmp/auto_input.exp << 'EOF'
#!/usr/bin/expect -f
set timeout 10

spawn /Users/jiyingguo/.openclaw/workspace/complete_100_skills_system.sh

expect "请输入选择 (1-9):"
send "5\r"

expect "按回车键继续"
send "\r"

expect eof
EOF

chmod +x /tmp/auto_input.exp
/tmp/auto_input.exp

echo ""
echo "✅ 一键安装完成！"
echo ""
echo "📁 创建的目录结构:"
ls -la /Users/jiyingguo/.openclaw/workspace/
echo ""
echo "🚀 现在可以运行: ./scripts/install_day1.sh 开始安装技能！"