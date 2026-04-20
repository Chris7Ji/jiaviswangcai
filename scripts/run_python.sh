#!/bin/bash
# 快速运行Python代码片段
# 用法: bash /Users/jiyingguo/.openclaw/workspace/scripts/run_python.sh "print('hello')"
# 或: bash /Users/jiyingguo/.openclaw/workspace/scripts/run_python.sh -c "print('hello')"

SCRIPT_DIR="/Users/jiyingguo/.openclaw/workspace/scripts"

if [ -z "$1" ]; then
    echo "用法:"
    echo "  bash $SCRIPT_DIR/run_python.sh \"print('hello world')\""
    echo "  bash $SCRIPT_DIR/run_python.sh -c \"import json; print(json.dumps({'a':1}))\""
    exit 1
fi

CODE=""
if [ "$1" = "-c" ] || [ "$1" = "--code" ]; then
    CODE="$2"
else
    CODE="$1"
fi

# 创建临时文件执行
TEMP_FILE=$(mktemp /tmp/jarvis_debug_XXXXXX.py)
echo "$CODE" > "$TEMP_FILE"
python3 "$TEMP_FILE"
RESULT=$?
rm -f "$TEMP_FILE"
exit $RESULT
