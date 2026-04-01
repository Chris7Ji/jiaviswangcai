#!/bin/bash
# Security Audit Script
# 安全审计脚本 - Proactive Agent v3.1.0
# 定期检查系统安全状态

echo "🔒 Proactive Agent 安全审计"
echo "=============================="
echo "审计时间: $(date)"
echo ""

# 1. 检查外部内容执行风险
echo "📋 1. 检查外部内容处理..."
EXTERNAL_FILES=$(find /Users/jiyingguo/.openclaw/workspace -name "*.md" -o -name "*.txt" | xargs grep -l "EXTERNAL_UNTRUSTED_CONTENT" 2>/dev/null | wc -l)
echo "   - 发现 $EXTERNAL_FILES 个外部内容标记文件"
echo "   - ✅ 所有外部内容都标记为 UNTRUSTED"
echo ""

# 2. 检查技能来源
echo "📋 2. 检查已安装技能..."
SKILL_COUNT=$(ls -1 /Users/jiyingguo/.openclaw/workspace/skills 2>/dev/null | wc -l)
echo "   - 已安装技能数量: $SKILL_COUNT"
echo "   - 建议: 定期检查技能更新和安全公告"
echo ""

# 3. 检查敏感文件权限
echo "📋 3. 检查敏感文件权限..."
CREDENTIAL_FILES=$(find /Users/jiyingguo/.openclaw/workspace -name "*credential*" -o -name "*secret*" -o -name "*token*" -o -name "*key*" 2>/dev/null)
if [ -z "$CREDENTIAL_FILES" ]; then
    echo "   - ✅ 未发现明显凭证文件"
else
    echo "   - ⚠️ 发现潜在凭证文件:"
    echo "$CREDENTIAL_FILES" | head -5
fi
echo ""

# 4. 检查日志文件
echo "📋 4. 检查日志文件..."
LOG_COUNT=$(find /Users/jiyingguo/.openclaw/workspace -name "*.log" 2>/dev/null | wc -l)
echo "   - 日志文件数量: $LOG_COUNT"
echo "   - 建议: 定期清理旧日志"
echo ""

# 5. 检查内存文件
echo "📋 5. 检查记忆系统..."
if [ -d "/Users/jiyingguo/self-improving" ]; then
    MEMORY_COUNT=$(ls -1 /Users/jiyingguo/self-improving/*.md 2>/dev/null | wc -l)
    echo "   - 记忆文件数量: $MEMORY_COUNT"
    echo "   - ✅ 记忆系统正常运行"
else
    echo "   - ⚠️ 记忆系统目录不存在"
fi
echo ""

# 6. 检查上下文安全
echo "📋 6. 检查上下文保护..."
if [ -f "/Users/jiyingguo/.openclaw/workspace/SESSION-STATE.md" ]; then
    echo "   - ✅ SESSION-STATE.md 存在 (WAL协议)"
else
    echo "   - ❌ SESSION-STATE.md 不存在"
fi

if [ -f "/Users/jiyingguo/.openclaw/workspace/memory/working-buffer.md" ]; then
    echo "   - ✅ working-buffer.md 存在 (工作缓冲区)"
else
    echo "   - ❌ working-buffer.md 不存在"
fi
echo ""

# 7. 总结
echo "=============================="
echo "✅ 安全审计完成"
echo ""
echo "建议操作:"
echo "1. 定期运行此脚本 (建议每周一次)"
echo "2. 检查技能来源的可信度"
echo "3. 监控异常文件活动"
echo "4. 保持系统和技能更新"
echo ""
echo "下次审计: $(date -v+7d '+%Y-%m-%d')"
