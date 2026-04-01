import os
import re
import datetime
import subprocess

WORKSPACE_SKILLS_DIR = "/Users/jiyingguo/.openclaw/workspace/skills"
HTML_FILE = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/skills.html"
JS_FILE = "/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/js/main.js"

# Core built-in skills definition
CORE_SKILLS = [
    {
        "category": "⚙️ 系统核心引擎 (System Core)",
        "items": [
            {"name": "read / write / edit", "desc": "文件读写核心。精准创建、修改或解析本地文件内容，防止大文件溢出内存。", "tags": ["文件管理", "编辑"]},
            {"name": "exec / process", "desc": "终端交互能力。安全执行受限白名单系统命令，管理长期后台进程与PTY会话。", "tags": ["Shell", "终端"]},
            {"name": "message", "desc": "多渠道通信枢纽。在Slack、Telegram、飞书等多渠道进行图文并茂、跨频道的通讯。", "tags": ["通讯", "原生"]},
            {"name": "canvas", "desc": "浏览器渲染引擎呈现。快照、渲染和呈现Web视图给用户端。", "tags": ["界面", "交互"]},
        ]
    },
    {
        "category": "🤖 智能编排与代理 (Orchestration)",
        "items": [
            {"name": "sessions_spawn", "desc": "子代理繁殖引擎。实时拉起专用子Agent来并行处理长时或复杂分层任务。", "tags": ["并发", "多代理"]},
            {"name": "subagents / sessions_list", "desc": "代理监控与生命周期。监控子代理的执行状态，提供接管或强制终止的能力。", "tags": ["管理", "监控"]},
            {"name": "sessions_send", "desc": "跨会话通信系统。实现在不同的平行会话与代理之间发送定向通讯。", "tags": ["通信", "同步"]},
        ]
    },
    {
        "category": "🧠 无损记忆与上下文 (Lossless Memory)",
        "items": [
            {"name": "lcm_grep", "desc": "记忆模糊搜寻。快速使用正则表达式或全文从被折叠压缩的历史记忆中检索蛛丝马迹。", "tags": ["检索", "记忆"]},
            {"name": "lcm_expand_query", "desc": "深层记忆唤醒。将记忆节点的摘要完整回溯到其子树，找回被压缩的精确上下文细节。", "tags": ["扩展", "上下文"]},
        ]
    },
    {
        "category": "👁️ 视觉与感知系统 (Perception)",
        "items": [
            {"name": "image", "desc": "原生视觉理解模型分析。传入图片进行分析与逻辑推演，看懂图表和界面设计。", "tags": ["视觉", "AI"]},
            {"name": "image_generate", "desc": "图像创造引擎。调用文生图或图生图模型，将灵感具现为高分辨率画作。", "tags": ["生成", "绘图"]},
            {"name": "tts", "desc": "原生文本转语音合成。提供自然人声朗读长文本的能力。", "tags": ["语音", "合成"]},
            {"name": "pdf", "desc": "文档结构拆解。分析并摄取PDF文档，保留文字排版与插图语境进行解读。", "tags": ["文档", "理解"]},
        ]
    },
    {
        "category": "📱 飞书全家桶集成 (Feishu Integration)",
        "items": [
            {"name": "feishu_doc / feishu_wiki", "desc": "飞书云文档/知识库操控。实现对飞书文档的逐段读写和知识库结构的完整重组。", "tags": ["飞书", "文档"]},
            {"name": "feishu_bitable", "desc": "飞书多维表格引擎。创建新表格应用、插入字段、增删改查上千条数据记录。", "tags": ["表格", "数据"]},
            {"name": "feishu_drive", "desc": "飞书云盘挂载。全面管理飞书个人云盘的文件结构与生命周期。", "tags": ["云盘", "文件"]},
        ]
    }
]

def get_third_party_skills():
    skills = []
    if os.path.exists(WORKSPACE_SKILLS_DIR):
        for entry in os.listdir(WORKSPACE_SKILLS_DIR):
            skill_dir = os.path.join(WORKSPACE_SKILLS_DIR, entry)
            if os.path.isdir(skill_dir) and not entry.startswith('.'):
                skill_md_path = os.path.join(skill_dir, "SKILL.md")
                name = entry
                desc = "第三方扩展功能包，提供专项场景下的处理与自动化能力。"
                tags = []
                
                if os.path.exists(skill_md_path):
                    try:
                        with open(skill_md_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.startswith('---'):
                                fm_end = content.find('---', 3)
                                if fm_end != -1:
                                    fm = content[3:fm_end]
                                    for line in fm.split('\n'):
                                        if line.startswith('description:'):
                                            # handle quotes
                                            val = line.split('description:', 1)[1].strip()
                                            val = val.strip('\'"')
                                            if val: desc = val
                                        elif line.startswith('name:'):
                                            val = line.split('name:', 1)[1].strip()
                                            val = val.strip('\'"')
                                            if val: name = val
                    except:
                        pass
                
                tags = [name.split('-')[0]] if '-' in name else [name]
                if "monitor" in name or "analyzer" in name: tags.append("监控")
                if "report" in name: tags.append("报告")
                
                skills.append({
                    "name": name,
                    "desc": desc,
                    "tags": tags[:3]
                })
    
    skills.sort(key=lambda x: x['name'])
    return skills

def generate_html():
    third_party = get_third_party_skills()
    html = []
    html.append('    <main class="container">')
    
    html.append('''
        <!-- 技能图例 -->
        <div style="margin-bottom: 2.5rem; padding: 1.5rem; background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border-color); display: flex; gap: 3rem; align-items: center; justify-content: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
            <div style="font-weight: bold; font-size: 1.1rem; color: var(--text-primary);">图例说明：</div>
            <div style="display: flex; align-items: center; gap: 0.8rem; font-size: 1.1rem;"><span style="color: #5D6D7E; font-size: 1.3em;">⚙️</span> <b>系统内置核心组件</b></div>
            <div style="display: flex; align-items: center; gap: 0.8rem; font-size: 1.1rem;"><span style="color: var(--accent-gold); font-size: 1.3em;">🌟</span> <b>第三方扩展应用技能</b></div>
        </div>
''')

    total_count = 0
    
    for cat in CORE_SKILLS:
        html.append(f'        <section class="category">\n            <h2 style="font-size: 1.5rem; padding-bottom: 0.5rem; border-bottom: 2px dashed var(--border-color); margin-bottom: 1.5rem;">{cat["category"]}</h2>\n            <div class="skills-grid">')
        for item in cat["items"]:
            total_count += 1
            tags_html = "".join([f'<span class="skill-tag">{t}</span>' for t in item["tags"]])
            html.append(f'''
                <div class="skill-card">
                    <h3 style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.15rem;">{item["name"]}</span> 
                        <span style="color: #5D6D7E; font-size: 1.2em;" title="系统内置核心技能">⚙️</span>
                    </h3>
                    <p style="margin-top: 0.8rem; min-height: 4rem; color: var(--text-secondary);">{item["desc"]}</p>
                    <div class="skill-tags" style="margin-top: 1rem;">{tags_html}</div>
                </div>''')
        html.append('            </div>\n        </section>')

    html.append(f'        <section class="category">\n            <h2 style="font-size: 1.5rem; padding-bottom: 0.5rem; border-bottom: 2px dashed var(--border-color); margin-bottom: 1.5rem;">🌟 第三方扩展应用技能 (Extension Skills)</h2>\n            <div class="skills-grid">')
    for item in third_party:
        total_count += 1
        tags_html = "".join([f'<span class="skill-tag">{t}</span>' for t in item["tags"]])
        html.append(f'''
                <div class="skill-card">
                    <h3 style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.15rem;">{item["name"]}</span> 
                        <span style="color: var(--accent-gold); font-size: 1.2em;" title="扩展应用技能">🌟</span>
                    </h3>
                    <p style="margin-top: 0.8rem; min-height: 4rem; color: var(--text-secondary);">{item["desc"]}</p>
                    <div class="skill-tags" style="margin-top: 1rem;">{tags_html}</div>
                </div>''')
    html.append('            </div>\n        </section>')
    
    html.append('    </main>')
    return '\n'.join(html), total_count

def update_file():
    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    main_start = content.find('<main class="container">')
    main_end = content.find('</main>') + 7
    
    if main_start == -1 or main_end < 7:
        print("Could not find main tag")
        return
    
    new_main_html, total_count = generate_html()
    
    content = content[:main_start] + new_main_html + content[main_end:]
    
    content = re.sub(
        r'<span class="skill-count">\d+</span> 个技能持续为您服务',
        f'<span class="skill-count">{total_count}</span> 个技能持续为您服务',
        content
    )
    content = re.sub(
        r'共 \d+ 个技能，持续学习进化中\.\.\.',
        f'共 {total_count} 个技能，持续学习进化中...',
        content
    )
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated HTML successfully with {total_count} skills!")

    if os.path.exists(JS_FILE):
        with open(JS_FILE, 'r', encoding='utf-8') as f:
            js_content = f.read()
        js_content = re.sub(
            r"skillsCount:\s*\{\s*value:\s*\d+,",
            f"skillsCount: {{ value: {total_count},",
            js_content
        )
        with open(JS_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Updated main.js successfully!")

if __name__ == "__main__":
    update_file()
