#!/bin/bash
# 记忆系统自动归档脚本
# 由老板（季）指示创建

set -e

LEARNINGS_DIR="/Users/jiyingguo/.openclaw/workspace/.learnings"
ARCHIVE_DIR="$LEARNINGS_DIR/archive"
DATE=$(date +%Y%m%d)

echo "=========================================="
echo "记忆系统自动归档"
echo "日期: $DATE"
echo "=========================================="

# 检查是否有需要归档的内容
if [ ! -f "$LEARNINGS_DIR/LEARNINGS.md" ]; then
    echo "❌ 找不到LEARNINGS.md文件"
    exit 1
fi

# 统计当前学习记录数量
LEARNING_COUNT=$(grep -c "^## 20" "$LEARNINGS_DIR/LEARNINGS.md" 2>/dev/null || echo "0")
echo "当前学习记录数量: $LEARNING_COUNT"

# 如果超过10条，进行归档
if [ "$LEARNING_COUNT" -gt 10 ]; then
    echo "📦 学习记录超过10条，需要归档"
    
    # 创建月度归档文件
    MONTH=$(date +%Y-%m)
    ARCHIVE_FILE="$ARCHIVE_DIR/monthly/learnings_$MONTH.md"
    
    echo "📝 归档到: $ARCHIVE_FILE"
    
    # 提取旧记录（保留最近5条）
    tail -n 100 "$LEARNINGS_DIR/LEARNINGS.md" > "$LEARNINGS_DIR/LEARNINGS.md.tmp"
    
    # 将旧记录追加到归档文件
    if [ -f "$ARCHIVE_FILE" ]; then
        echo "" >> "$ARCHIVE_FILE"
        echo "# 归档时间: $DATE" >> "$ARCHIVE_FILE"
        echo "" >> "$ARCHIVE_FILE"
    else
        echo "# 学习记录月度归档 - $MONTH" > "$ARCHIVE_FILE"
        echo "" >> "$ARCHIVE_FILE"
        echo "归档时间: $DATE" >> "$ARCHIVE_FILE"
        echo "" >> "$ARCHIVE_FILE"
    fi
    
    # 保留最新的5条记录
    head -n 50 "$LEARNINGS_DIR/LEARNINGS.md.tmp" > "$LEARNINGS_DIR/LEARNINGS.md"
    rm "$LEARNINGS_DIR/LEARNINGS.md.tmp"
    
    echo "✅ 归档完成"
else
    echo "✅ 学习记录数量正常，无需归档"
fi

# 检查ERRORS.md
if [ -f "$LEARNINGS_DIR/ERRORS.md" ]; then
    ERROR_COUNT=$(grep -c "^## 20" "$LEARNINGS_DIR/ERRORS.md" 2>/dev/null || echo "0")
    echo "错误记录数量: $ERROR_COUNT"
    
    if [ "$ERROR_COUNT" -gt 10 ]; then
        echo "📦 错误记录超过10条，需要归档"
        ARCHIVE_FILE="$ARCHIVE_DIR/monthly/errors_$MONTH.md"
        
        # 归档逻辑同上
        tail -n 100 "$LEARNINGS_DIR/ERRORS.md" > "$LEARNINGS_DIR/ERRORS.md.tmp"
        
        if [ -f "$ARCHIVE_FILE" ]; then
            echo "" >> "$ARCHIVE_FILE"
            echo "# 归档时间: $DATE" >> "$ARCHIVE_FILE"
            echo "" >> "$ARCHIVE_FILE"
        else
            echo "# 错误记录月度归档 - $MONTH" > "$ARCHIVE_FILE"
            echo "" >> "$ARCHIVE_FILE"
            echo "归档时间: $DATE" >> "$ARCHIVE_FILE"
            echo "" >> "$ARCHIVE_FILE"
        fi
        
        head -n 50 "$LEARNINGS_DIR/ERRORS.md.tmp" > "$LEARNINGS_DIR/ERRORS.md"
        rm "$LEARNINGS_DIR/ERRORS.md.tmp"
        
        echo "✅ 错误记录归档完成"
    fi
fi

echo "=========================================="
echo "归档任务完成"
echo "=========================================="