#!/bin/bash
# 问题诊断脚本

echo "========================================"
echo "🔧 OpenClaw技能安装问题诊断"
echo "========================================"

DIAG_LOG="$LOG_DIR/diagnose_$(date '+%Y%m%d_%H%M%S').log"
echo "诊断开始: $(date)" | tee -a "$DIAG_LOG"

# 检查clawhub
echo "1. 检查clawhub..." | tee -a "$DIAG_LOG"
if command -v clawhub &> /dev/null; then
    echo "  ✅ clawhub已安装: $(clawhub --version | head -1)" | tee -a "$DIAG_LOG"
else
    echo "  ❌ clawhub未安装" | tee -a "$DIAG_LOG"
    echo "  解决方案: npm install -g @openclaw/clawhub" | tee -a "$DIAG_LOG"
fi

# 检查网络连接
echo "" | tee -a "$DIAG_LOG"
echo "2. 检查网络连接..." | tee -a "$DIAG_LOG"
if ping -c 1 -W 2 google.com &> /dev/null; then
    echo "  ✅ 网络连接正常" | tee -a "$DIAG_LOG"
else
    echo "  ❌ 网络连接失败" | tee -a "$DIAG_LOG"
    echo "  解决方案: 检查网络设置" | tee -a "$DIAG_LOG"
fi

# 检查磁盘空间
echo "" | tee -a "$DIAG_LOG"
echo "3. 检查磁盘空间..." | tee -a "$DIAG_LOG"
df -h /opt/homebrew 2>/dev/null | tee -a "$DIAG_LOG"

# 检查速率限制
echo "" | tee -a "$DIAG_LOG"
echo "4. 检查速率限制..." | tee -a "$DIAG_LOG"
RECENT_ERRORS=$(find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -l "Rate limit exceeded" {} \; 2>/dev/null | wc -l)
if [ $RECENT_ERRORS -gt 0 ]; then
    echo "  ⚠️  检测到速率限制错误: $RECENT_ERRORS 次" | tee -a "$DIAG_LOG"
    echo "  解决方案:" | tee -a "$DIAG_LOG"
    echo "    1. 等待2-3小时再尝试" | tee -a "$DIAG_LOG"
    echo "    2. 增加安装间隔时间" | tee -a "$DIAG_LOG"
    echo "    3. 减少每批安装数量" | tee -a "$DIAG_LOG"
else
    echo "  ✅ 未检测到速率限制错误" | tee -a "$DIAG_LOG"
fi

# 检查失败的安装
echo "" | tee -a "$DIAG_LOG"
echo "5. 检查失败的安装..." | tee -a "$DIAG_LOG"
FAILED_INSTALLS=$(find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -l "安装失败" {} \; 2>/dev/null | wc -l)
if [ $FAILED_INSTALLS -gt 0 ]; then
    echo "  ⚠️  检测到失败的安装: $FAILED_INSTALLS 次" | tee -a "$DIAG_LOG"
    echo "  最近失败记录:" | tee -a "$DIAG_LOG"
    find "$LOG_DIR" -name "*.log" -type f -mtime -1 -exec grep -h "安装失败" {} \; 2>/dev/null | tail -5 | tee -a "$DIAG_LOG"
else
    echo "  ✅ 未检测到失败的安装" | tee -a "$DIAG_LOG"
fi

# 检查技能目录权限
echo "" | tee -a "$DIAG_LOG"
echo "6. 检查目录权限..." | tee -a "$DIAG_LOG"
SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
if [ -d "$SKILLS_DIR" ]; then
    if [ -w "$SKILLS_DIR" ]; then
        echo "  ✅ 技能目录可写" | tee -a "$DIAG_LOG"
    else
        echo "  ❌ 技能目录不可写" | tee -a "$DIAG_LOG"
        echo "  解决方案: sudo chown -R $(whoami) $SKILLS_DIR" | tee -a "$DIAG_LOG"
    fi
else
    echo "  ⚠️  技能目录不存在" | tee -a "$DIAG_LOG"
fi

# 生成诊断报告
echo "" | tee -a "$DIAG_LOG"
echo "========================================" | tee -a "$DIAG_LOG"
echo "诊断完成: $(date)" | tee -a "$DIAG_LOG"
echo "" | tee -a "$DIAG_LOG"
echo "💡 建议操作:" | tee -a "$DIAG_LOG"

if [ $RECENT_ERRORS -gt 0 ]; then
    echo "  1. 暂停安装，等待速率限制恢复" | tee -a "$DIAG_LOG"
fi

if [ $FAILED_INSTALLS -gt 0 ]; then
    echo "  2. 重新尝试失败的安装" | tee -a "$DIAG_LOG"
fi

echo "  3. 运行测试脚本验证技能功能" | tee -a "$DIAG_LOG"
echo "  4. 定期生成进度报告" | tee -a "$DIAG_LOG"

echo "" | tee -a "$DIAG_LOG"
echo "详细诊断日志: $DIAG_LOG" | tee -a "$DIAG_LOG"
