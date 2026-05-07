#!/bin/bash
# ============================================================
# 日记生成验证脚本
# 检查今天的日记是否已生成，如果没生成则告警
# 建议在每日 21:30 运行（日记 cron 在 21:00 运行）
# ============================================================

TODAY=$(date +%Y%m%d)
TODAY_CN=$(date +%Y年%m月%d日)
TODAY_FMT=$(date +%Y-%m-%d)

WEBSITE_DIR="/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai"
ALERT_SCRIPT="/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/scripts/alert_diary_missing.sh"

echo "========== $(date) =========="
echo "🔍 验证今日日记是否已生成..."
echo "  日期: $TODAY_CN"
echo "  期望ID: $TODAY"

FAILURES=0

# 检查1: diary.js 中是否有今日条目
echo ""
echo "[1/2] 检查 js/diary.js..."
if grep -q "id: '$TODAY'" "$WEBSITE_DIR/js/diary.js" 2>/dev/null; then
    echo "  ✅ diary.js: 今日条目存在"
    
    # 进一步检查内容是否为空/占位
    CONTENT_LEN=$(python3 -c "
import re
with open('$WEBSITE_DIR/js/diary.js') as f:
    c = f.read()
m = re.search(r\"id:\s*'$TODAY'[\s\S]*?content:\s*\x60([\s\S]*?)\x60\", c)
if m:
    print(len(m.group(1).strip()))
else:
    print(0)
" 2>/dev/null)
    
    if [ "$CONTENT_LEN" -gt 100 ]; then
        echo "  ✅ diary.js: 内容长度 ${CONTENT_LEN} 字符，正常"
    else
        echo "  ⚠️  diary.js: 内容过短（${CONTENT_LEN} 字符），可能不完整"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "  ❌ diary.js: 今日条目缺失！"
    FAILURES=$((FAILURES + 1))
fi

# 检查2: post.html 中是否有今日条目
echo ""
echo "[2/2] 检查 post.html..."
if grep -q "id: '$TODAY'" "$WEBSITE_DIR/post.html" 2>/dev/null; then
    echo "  ✅ post.html: 今日条目存在"
    
    # 检查内容长度
    CONTENT_LEN=$(python3 -c "
import re
with open('$WEBSITE_DIR/post.html') as f:
    c = f.read()
m = re.search(r\"id:\s*'$TODAY'[\s\S]*?content:\s*\x60([\s\S]*?)\x60\", c)
if m:
    print(len(m.group(1).strip()))
else:
    print(0)
" 2>/dev/null)
    
    if [ "$CONTENT_LEN" -gt 100 ]; then
        echo "  ✅ post.html: 内容长度 ${CONTENT_LEN} 字符，正常"
    else
        echo "  ⚠️  post.html: 内容过短（${CONTENT_LEN} 字符），可能不完整"
        FAILURES=$((FAILURES + 1))
    fi
else
    echo "  ❌ post.html: 今日条目缺失！"
    FAILURES=$((FAILURES + 1))
fi

echo ""
echo "========== 验证结果 =========="
if [ "$FAILURES" -eq 0 ]; then
    echo "✅ 今日日记已完整生成，所有检查通过！"
    exit 0
else
    echo "🚨 发现 ${FAILURES} 个问题！今日日记可能未生成或不完整。"
    echo "  日期: $TODAY_CN"
    echo "  时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 如果存在告警脚本，调用它
    if [ -f "$ALERT_SCRIPT" ]; then
        bash "$ALERT_SCRIPT" "$TODAY_CN" "$FAILURES"
    fi
    
    exit 1
fi
