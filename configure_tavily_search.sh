#!/bin/bash

# Tavily搜索API配置脚本
# 使用方法：./configure_tavily_search.sh YOUR_Tavily_API_KEY

echo "=== Tavily搜索API配置 ==="
echo "开始时间: $(date)"
echo ""

if [ $# -eq 0 ]; then
    echo "❌ 错误：请提供Tavily API密钥"
    echo "用法: $0 YOUR_TAVILY_API_KEY"
    echo ""
    echo "密钥格式类似: tvly-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    echo ""
    echo "如果您还没有Tavily API密钥："
    echo "1. 访问 https://tavily.com/"
    echo "2. 注册账户"
    echo "3. 获取API密钥"
    echo "4. 复制密钥并运行此脚本"
    exit 1
fi

TAVILY_API_KEY="$1"
CONFIG_DIR="$HOME/.openclaw"
CONFIG_FILE="$CONFIG_DIR/config.json"
TAVILY_SCRIPT="$CONFIG_DIR/tavily_search.py"
BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"

echo "🔑 提供的Tavily API密钥: ${TAVILY_API_KEY:0:8}******"
echo ""

# 备份现有配置
if [ -f "$CONFIG_FILE" ]; then
    echo "📁 备份现有配置: $BACKUP_FILE"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
fi

# 创建配置目录
mkdir -p "$CONFIG_DIR"

echo "🔄 创建Tavily搜索脚本..."
echo ""

# 创建Tavily搜索Python脚本
cat > "$TAVILY_SCRIPT" << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tavily搜索集成脚本
使用Tavily API进行AI优化搜索
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Any

class TavilySearch:
    """Tavily搜索客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('TAVILY_API_KEY')
        if not self.api_key:
            raise ValueError("Tavily API密钥未设置。请设置TAVILY_API_KEY环境变量或传递api_key参数")
        
        self.base_url = "https://api.tavily.com"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })
    
    def search(
        self,
        query: str,
        max_results: int = 5,
        include_answer: bool = True,
        include_raw_content: bool = False,
        search_depth: str = "basic",
        include_images: bool = False,
        include_domains: Optional[List[str]] = None,
        exclude_domains: Optional[List[str]] = None,
        time_range: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        执行Tavily搜索
        
        Args:
            query: 搜索查询
            max_results: 最大结果数 (1-10)
            include_answer: 是否包含AI生成的答案
            include_raw_content: 是否包含原始内容
            search_depth: 搜索深度 ("basic" 或 "advanced")
            include_images: 是否包含图片
            include_domains: 包含的域名列表
            exclude_domains: 排除的域名列表
            time_range: 时间范围 ("d", "w", "m", "y")
        
        Returns:
            搜索结果字典
        """
        # 验证参数
        if not 1 <= max_results <= 10:
            raise ValueError("max_results必须在1到10之间")
        
        # 准备请求数据
        payload = {
            "query": query,
            "max_results": max_results,
            "include_answer": include_answer,
            "include_raw_content": include_raw_content,
            "search_depth": search_depth,
            "include_images": include_images
        }
        
        # 可选参数
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains
        if time_range:
            payload["time_range"] = time_range
        
        try:
            response = self.session.post(
                f"{self.base_url}/search",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Tavily搜索请求失败: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"响应状态码: {e.response.status_code}")
                print(f"响应内容: {e.response.text[:500]}")
            return {"error": str(e), "results": []}
        except Exception as e:
            print(f"Tavily搜索处理失败: {e}")
            return {"error": str(e), "results": []}
    
    def get_ai_answer(self, query: str, **kwargs) -> Optional[str]:
        """获取AI生成的答案"""
        result = self.search(query, include_answer=True, **kwargs)
        return result.get('answer')
    
    def search_simple(self, query: str, max_results: int = 5) -> List[Dict]:
        """简化搜索，只返回结果列表"""
        result = self.search(query, max_results=max_results, include_answer=False)
        return result.get('results', [])
    
    def save_results(self, query: str, results: Dict, filename: str = None):
        """保存搜索结果到文件"""
        if filename is None:
            import time
            timestamp = int(time.time())
            filename = f"tavily_results_{timestamp}.json"
        
        data = {
            "query": query,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 搜索结果已保存到: {filename}")
        return filename

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python tavily_search.py '搜索查询' [最大结果数]")
        print("示例: python tavily_search.py '人工智能最新发展' 5")
        sys.exit(1)
    
    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    # 从环境变量获取API密钥
    api_key = os.getenv('TAVILY_API_KEY')
    if not api_key:
        print("❌ 错误：TAVILY_API_KEY环境变量未设置")
        print("请设置环境变量: export TAVILY_API_KEY='your-api-key'")
        sys.exit(1)
    
    # 执行搜索
    print(f"🔍 搜索: {query}")
    print(f"📊 最大结果数: {max_results}")
    print("")
    
    searcher = TavilySearch(api_key)
    results = searcher.search(query, max_results=max_results, include_answer=True)
    
    if 'error' in results:
        print(f"❌ 搜索失败: {results['error']}")
        sys.exit(1)
    
    # 显示结果
    if 'answer' in results and results['answer']:
        print("🤖 AI答案:")
        print(results['answer'])
        print("")
    
    if 'results' in results and results['results']:
        print(f"📈 找到 {len(results['results'])} 个结果:")
        print("")
        
        for i, item in enumerate(results['results'], 1):
            print(f"🔹 结果{i}: {item.get('title', '无标题')}")
            print(f"   链接: {item.get('url', '无链接')}")
            print(f"   摘要: {item.get('content', '无内容')[:200]}...")
            print(f"   评分: {item.get('score', 'N/A')}")
            print("")
    
    # 保存结果
    searcher.save_results(query, results)
    
    print("✅ 搜索完成")

if __name__ == "__main__":
    main()
EOF

# 设置脚本权限
chmod +x "$TAVILY_SCRIPT"

echo "✅ Tavily搜索脚本已创建: $TAVILY_SCRIPT"
echo ""

# 更新OpenClaw配置
echo "🔄 更新OpenClaw配置..."
if [ -f "$CONFIG_FILE" ]; then
    # 读取现有配置
    if command -v jq &> /dev/null; then
        # 使用jq更新配置
        jq '.tavily = {apiKey: "'"$TAVILY_API_KEY"'", enabled: true}' "$CONFIG_FILE" > "${CONFIG_FILE}.tmp" && mv "${CONFIG_FILE}.tmp" "$CONFIG_FILE"
        echo "✅ 使用jq更新配置成功"
    else
        # 简单文本处理
        echo "⚠️  jq未安装，使用简单配置更新"
        if ! grep -q '"tavily"' "$CONFIG_FILE"; then
            # 在文件末尾添加tavily配置
            sed -i '' '$ s/}$/,\n  "tavily": {\n    "apiKey": "'"$TAVILY_API_KEY"'",\n    "enabled": true\n  }\n}/' "$CONFIG_FILE"
        fi
    fi
else
    # 创建新配置
    cat > "$CONFIG_FILE" << EOF
{
  "tavily": {
    "apiKey": "$TAVILY_API_KEY",
    "enabled": true
  }
}
EOF
    echo "✅ 创建新配置文件"
fi

echo "📁 配置文件: $CONFIG_FILE"
echo ""

# 设置环境变量
echo "🔧 设置环境变量..."
SHELL_CONFIG=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

if [ -n "$SHELL_CONFIG" ]; then
    # 检查是否已设置
    if ! grep -q "TAVILY_API_KEY" "$SHELL_CONFIG"; then
        echo "" >> "$SHELL_CONFIG"
        echo "# Tavily API配置" >> "$SHELL_CONFIG"
        echo "export TAVILY_API_KEY=\"$TAVILY_API_KEY\"" >> "$SHELL_CONFIG"
        echo "✅ 环境变量已添加到: $SHELL_CONFIG"
        echo "💡 请运行: source $SHELL_CONFIG"
    else
        echo "✅ 环境变量已存在"
    fi
else
    echo "⚠️  未找到shell配置文件，请手动设置环境变量:"
    echo "   export TAVILY_API_KEY=\"$TAVILY_API_KEY\""
fi

echo ""
echo "🎉 Tavily配置完成！"
echo ""
echo "📋 使用方法："
echo ""
echo "1. 通过Python脚本使用："
echo "   python $TAVILY_SCRIPT '搜索查询'"
echo ""
echo "2. 在Python代码中使用："
echo "   from tavily_search import TavilySearch"
echo "   searcher = TavilySearch()"
echo "   results = searcher.search('您的查询')"
echo ""
echo "3. 环境变量："
echo "   TAVILY_API_KEY 已设置"
echo ""
echo "🔍 测试搜索："
echo "   python $TAVILY_SCRIPT '测试搜索' 3"
echo ""
echo "📁 文件位置："
echo "   - 配置脚本: $TAVILY_SCRIPT"
echo "   - 配置文件: $CONFIG_FILE"
echo "   - 备份文件: $BACKUP_FILE"
echo ""
echo "💡 提示：Tavily API可能有使用限制，请查看 https://tavily.com/pricing"

exit 0