#!/bin/bash
# 高校分队灯塔项目定时任务配置脚本
# 执行方式: bash setup_dengta_cron.sh

echo "🎯 配置高校分队灯塔项目定时任务..."

# 任务1: 邮件版
echo "📧 创建邮件版定时任务..."
openclaw task create \
  --name "高校分队灯塔每日动态-邮件版" \
  --schedule "45 6 * * * Asia/Shanghai" \
  --command "python3 /Users/jiyingguo/.openclaw/workspace/send_dengta_final.py" \
  --cwd "/Users/jiyingguo/.openclaw/workspace" \
  --enabled

if [ $? -eq 0 ]; then
    echo "✅ 邮件版定时任务创建成功"
else
    echo "❌ 邮件版定时任务创建失败"
fi

# 任务2: 飞书版
echo "💬 创建飞书版定时任务..."
openclaw task create \
  --name "高校分队灯塔每日动态-飞书版" \
  --schedule "45 6 * * * Asia/Shanghai" \
  --command "python3 /Users/jiyingguo/.openclaw/workspace/send_dengta_feishu.py" \
  --cwd "/Users/jiyingguo/.openclaw/workspace" \
  --enabled

if [ $? -eq 0 ]; then
    echo "✅ 飞书版定时任务创建成功"
else
    echo "❌ 飞书版定时任务创建失败"
fi

echo ""
echo "📋 验证任务列表:"
openclaw task list

echo ""
echo "🎉 配置完成！任务将在每天06:45自动执行。"