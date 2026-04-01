#!/bin/bash

# 简化版重试脚本 - 只关注multi-search-engine

echo "=== Multi-Search Engine 安装重试 ==="
echo "开始时间: $(date)"
echo ""

# 要尝试的技能（按优先级）
SKILLS=("multi-search-engine" "multi-search-engine-2")
MAX_ATTEMPTS=3
ATTEMPT_INTERVAL=3600  # 1小时

for attempt in $(seq 1 $MAX_ATTEMPTS); do
    echo ""
    echo "=== 第 $attempt 次尝试 ==="
    echo "时间: $(date)"
    
    for skill in "${SKILLS[@]}"; do
        echo ""
        echo "尝试安装: $skill"
        
        # 尝试安装
        OUTPUT=$(clawhub install "$skill" 2>&1)
        EXIT_CODE=$?
        
        if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ 成功安装: $skill"
            echo "输出: $OUTPUT"
            
            # 验证安装
            echo ""
            echo "=== 验证安装 ==="
            clawhub list
            
            # 检查技能目录
            if [ -d "/Users/jiyingguo/.openclaw/workspace/skills/$skill" ]; then
                echo "✅ 技能目录已创建: skills/$skill"
                ls -la "/Users/jiyingguo/.openclaw/workspace/skills/$skill/"
            fi
            
            exit 0
        else
            echo "❌ 安装失败: $skill"
            echo "错误: $OUTPUT"
        fi
    done
    
    # 如果不是最后一次尝试，等待
    if [ $attempt -lt $MAX_ATTEMPTS ]; then
        echo ""
        echo "⏳ 等待 $((ATTEMPT_INTERVAL/60)) 分钟后重试..."
        echo "下次尝试时间: $(date -v+${ATTEMPT_INTERVAL}S)"
        sleep $ATTEMPT_INTERVAL
    fi
done

echo ""
echo "=== 最终结果 ==="
echo "❌ 所有尝试都失败"
echo "总尝试次数: $MAX_ATTEMPTS"
echo "最后尝试时间: $(date)"
echo ""
echo "建议:"
echo "1. 等待更长时间后重试（clawhub速率限制可能较严格）"
echo "2. 使用现有web_search工具满足搜索需求"
echo "3. 明天再尝试安装"

exit 1