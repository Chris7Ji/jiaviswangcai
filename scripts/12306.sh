#!/bin/bash
# 12306火车票查询便捷脚本
# 用法: bash /Users/jiyingguo/.openclaw/workspace/scripts/12306.sh 上海 北京 2026-04-30

SCRIPT="/Users/jiyingguo/.openclaw/workspace/skills/12306/scripts/query.mjs"

if [ -z "$1" ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "12306火车票查询"
    echo "用法:"
    echo "  bash $SCRIPT 上海 北京 2026-04-30"
    echo "  bash $SCRIPT 上海 北京 2026-04-30 G"
    echo ""
    echo "参数: 出发地 目的地 日期 [车型]"
    echo "车型: G(高铁) D(动车) C(城际) K(快速) T(特快) Z(直达)"
    exit 0
fi

FROM="$1"
TO="$2"
DATE="$3"
TRAIN_TYPE="${4:-}"  # 可选，如 G D C K T Z

if [ -z "$FROM" ] || [ -z "$TO" ] || [ -z "$DATE" ]; then
    echo "错误: 请提供出发地、目的地和日期"
    echo "用法: bash $SCRIPT 上海 北京 2026-04-30"
    exit 1
fi

# 构建参数
ARGS="--from $FROM --to $TO --date $DATE"
if [ -n "$TRAIN_TYPE" ]; then
    ARGS="$ARGS --train-type $TRAIN_TYPE"
fi

echo "查询: $FROM → $TO, 日期: $DATE"
echo "执行: node $SCRIPT $ARGS"
echo ""

node "$SCRIPT" $ARGS
