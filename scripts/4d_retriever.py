#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from datetime import datetime

# ==========================================
# 四维前置检索系统 (4D Pre-retrieval System)
# 维度定义：
# 1D: Keyword (关键词匹配)
# 2D: Semantic (语义意图 - 预留接口)
# 3D: GraphRAG (知识星图关系)
# 4D: Time (时间序列与演化)
# ==========================================

WORKSPACE = "/Users/jiyingguo/.openclaw/workspace"
GRAPH_PATH = os.path.join(WORKSPACE, "memory", "ontology", "knowledge_graph.json")

def search_1d_keyword(query):
    print(f"\n[1D] 🔍 文本维度检索 (Keyword Match)...")
    # Search in .learnings and memory
    cmd = f"grep -rnw -i '{query}' {WORKSPACE}/.learnings {WORKSPACE}/memory 2>/dev/null | head -n 5"
    try:
        res = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        if res:
            for line in res.split('\n'):
                # clean up path for display
                clean_line = line.replace(WORKSPACE, "")
                print(f"  📄 {clean_line}")
        else:
            print("  - 未发现直接文本匹配。")
    except subprocess.CalledProcessError:
        print("  - 未发现直接文本匹配。")

def search_2d_semantic(query):
    print(f"\n[2D] 🧠 语义维度检索 (Semantic Vector)...")
    print(f"  - 命中意图：推测用户正在查询关于 [{query}] 的上下文或历史记录。")
    print(f"  - (待接入本地 Ollama nomic-embed-text 嵌入向量)")

def search_3d_graphrag(query):
    print(f"\n[3D] 🌌 星图维度检索 (GraphRAG)...")
    if not os.path.exists(GRAPH_PATH):
        print("  - 知识星图尚未构建，请先运行 build_star_graph.py。")
        return
        
    with open(GRAPH_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    
    match_ids = [n_id for n_id, n in nodes.items() if query.lower() in n_id.lower() or query.lower() in n.get("label", "").lower()]
    
    if not match_ids:
        print(f"  - 知识星图中未发现与 [{query}] 强关联的实体。")
        return
        
    for m_id in match_ids[:3]: # limit to top 3 concepts
        m_node = nodes[m_id]
        print(f"  🌟 实体锚点: [{m_node['type']}] {m_node['label']}")
        
        rel_count = 0
        for edge in edges:
            if edge["source"] == m_id:
                target = nodes[edge["target"]]
                print(f"    ↳ {edge['relation']} ↳ [{target['type']}] {target['label']}")
                rel_count += 1
            elif edge["target"] == m_id:
                source = nodes[edge["source"]]
                print(f"    ↲ {edge['relation']} ↲ [{source['type']}] {source['label']}")
                rel_count += 1
            if rel_count >= 5: # Limit relation output
                print(f"    ... (还有更多关联)")
                break

def search_4d_time(query):
    print(f"\n[4D] ⏳ 时间维度检索 (Chronological Evolution)...")
    # Check git log or file modification times for the query
    cmd = f"find {WORKSPACE}/.learnings {WORKSPACE}/memory -type f -exec grep -l -i '{query}' {{}} + 2>/dev/null | xargs stat -f '%m %N' 2>/dev/null | sort -nr | head -n 3"
    try:
        res = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        if res:
            for line in res.split('\n'):
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    ts, path = parts
                    dt = datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M')
                    clean_path = path.replace(WORKSPACE, "")
                    print(f"  🕒 {dt} (最后活跃) -> {clean_path}")
        else:
            print("  - 无时间序列演化数据。")
    except subprocess.CalledProcessError:
        print("  - 无时间序列演化数据。")

def main():
    if len(sys.argv) < 2:
        print("用法: 4d_retriever.py <搜索词>")
        sys.exit(1)
        
    query = sys.argv[1]
    print(f"========== 旺财Jarvis 四维前置检索 (4D-RAG) ==========")
    print(f"正在为您全息扫描记忆锚点: [{query}]")
    print(f"=======================================================")
    
    search_1d_keyword(query)
    search_2d_semantic(query)
    search_3d_graphrag(query)
    search_4d_time(query)
    
    print(f"\n=======================================================")
    print("检索完成。已获取四维全息上下文。")

if __name__ == "__main__":
    main()
