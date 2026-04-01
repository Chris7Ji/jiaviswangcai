import sys
import json
import os

GRAPH_PATH = "/Users/jiyingguo/.openclaw/workspace/memory/ontology/knowledge_graph.json"

if len(sys.argv) < 2:
    print("Usage: python query_star_graph.py <query_concept_or_tag>")
    sys.exit(1)

query = sys.argv[1].lower()

with open(GRAPH_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

nodes = {n["id"]: n for n in data["nodes"]}
edges = data["edges"]

# Find matching node IDs
match_ids = []
for n_id, n in nodes.items():
    if query in n_id.lower() or query in n.get("label", "").lower():
        match_ids.append(n_id)

if not match_ids:
    print(f"❌ No matching concepts, tags, or documents found for '{query}' in the Star Graph.")
    sys.exit(0)

print(f"🔍 GraphRAG Search Results for '{query}':\n")
for m_id in match_ids:
    m_node = nodes[m_id]
    print(f"[{m_node['type']}] {m_node['label']}")
    
    # Find connections
    connections = []
    for edge in edges:
        if edge["source"] == m_id:
            target = nodes[edge["target"]]
            connections.append(f"  → {edge['relation']} → [{target['type']}] {target['label']}")
        elif edge["target"] == m_id:
            source = nodes[edge["source"]]
            connections.append(f"  ← {edge['relation']} ← [{source['type']}] {source['label']}")
            
    for c in connections:
        print(c)
    print("-" * 40)
