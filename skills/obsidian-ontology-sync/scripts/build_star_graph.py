import os
import re
import json
from pathlib import Path

WORKSPACE = "/Users/jiyingguo/.openclaw/workspace"
GRAPH_PATH = os.path.join(WORKSPACE, "memory", "ontology")
os.makedirs(GRAPH_PATH, exist_ok=True)

# Regex for Obsidian-style [[WikiLinks]] and #tags
wikilink_pattern = re.compile(r'\[\[(.*?)\]\]')
# Match tags like #tag but ignore markdown headers (needs space or start of line)
tag_pattern = re.compile(r'(?:^|\s)#([A-Za-z0-9_/-]+)')

nodes = {}
edges = []

def get_node(node_id, node_type="Concept", label=None):
    if node_id not in nodes:
        nodes[node_id] = {"id": node_id, "type": node_type, "label": label or node_id, "properties": {}}
    return nodes[node_id]

# Scan core memory, learnings, and logs
scan_dirs = [
    ".",
    ".learnings",
    "jiaviswangcai.ai",
]

for d in scan_dirs:
    dir_path = os.path.join(WORKSPACE, d)
    if not os.path.exists(dir_path): continue
    
    for file_path in Path(dir_path).rglob('*.md'):
        if "node_modules" in str(file_path) or ".venv" in str(file_path) or "skills/" in str(file_path) and d == ".": 
            continue
            
        rel_path = str(file_path.relative_to(WORKSPACE))
        doc_node_id = f"doc:{rel_path}"
        doc_node = get_node(doc_node_id, "Document", file_path.name)
        doc_node["properties"]["path"] = rel_path
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            continue
            
        # Extract tags
        for tag in tag_pattern.findall(content):
            if not tag.strip(): continue
            tag_id = f"tag:{tag}"
            get_node(tag_id, "Tag", f"#{tag}")
            edges.append({"source": doc_node_id, "target": tag_id, "relation": "has_tag"})
            
        # Extract wikilinks
        for link in wikilink_pattern.findall(content):
            # link might be File|Alias
            link_parts = link.split("|")
            target = link_parts[0].strip()
            if not target: continue
            link_id = f"concept:{target}"
            get_node(link_id, "Concept", target)
            edges.append({"source": doc_node_id, "target": link_id, "relation": "mentions"})

graph_data = {
    "nodes": list(nodes.values()),
    "edges": edges
}

with open(os.path.join(GRAPH_PATH, "knowledge_graph.json"), "w", encoding="utf-8") as f:
    json.dump(graph_data, f, ensure_ascii=False, indent=2)

print(f"✅ Knowledge Graph (Star Graph) Built Successfully!")
print(f"📊 Extracted {len(nodes)} nodes (Documents, Tags, Concepts) and {len(edges)} connections.")
print(f"💾 Saved to: {os.path.join(GRAPH_PATH, 'knowledge_graph.json')}")
