import os

def insert_article():
    file_path = '/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai/skills.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # The article HTML block
    article_html = """
        <!-- 新增核心功能文章模块 -->
        <section class="feature-article" style="margin-bottom: 4rem; background: var(--bg-card); border-radius: 12px; border: 1px solid var(--border-color); padding: 3rem; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
                <div style="width: 8px; height: 32px; background: var(--accent-gold); border-radius: 4px;"></div>
                <h2 style="font-size: 1.8rem; color: var(--text-primary);">✨ 核心功能：多层 4D 记忆系统架构全景</h2>
            </div>
            
            <p style="font-size: 1.15rem; color: var(--text-secondary); line-height: 1.8; margin-bottom: 2.5rem;">
                作为一个不断进化的 Proactive Agent，旺财Jarvis 的大脑已经从最初的“扁平化文件堆叠”演进为<strong>“全息立体知识库”</strong>。它不仅能执行指令，更能通过一套具备<strong>时空感知、关系推理、自动代谢</strong>的立体记忆检索架构，在您提问的瞬间零延迟穿梭于四个维度，拼凑出最立体的上下文全貌。
            </p>

            <h3 style="font-size: 1.4rem; color: var(--accent-blue); margin-bottom: 1.5rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem;">🌌 记忆系统层级解析</h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
                <!-- Layer 0 -->
                <div style="padding: 1.5rem; background: var(--bg-primary); border-radius: 8px; border-left: 4px solid #A8D0E6;">
                    <h4 style="margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size:1.2em;">🟢</span> Layer 0: 活跃感知层 (Working Memory)</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem;"><strong>机制</strong>：OpenClaw 原生无损上下文 (LCM) 与 SESSION-STATE。<br><strong>作用</strong>：犹如短期记忆区，处理当前对话。上下文超60%安全水位时触发自动压缩，保证工作流永不宕机。</p>
                </div>
                <!-- Layer 1 -->
                <div style="padding: 1.5rem; background: var(--bg-primary); border-radius: 8px; border-left: 4px solid #F8E9A1;">
                    <h4 style="margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size:1.2em;">🟡</span> Layer 1: 1D 文本精准维 (Keyword)</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem;"><strong>机制</strong>：原生高优检索，直连本地记忆库。<br><strong>作用</strong>：“所见即所得”的实体召回。需要找回特定配置代码、具体报错日志时，提供最高效、最原汁原味的锚点查询。</p>
                </div>
                <!-- Layer 2 -->
                <div style="padding: 1.5rem; background: var(--bg-primary); border-radius: 8px; border-left: 4px solid #7EC8E3;">
                    <h4 style="margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size:1.2em;">🔵</span> Layer 2: 2D 语义意图维 (Semantic Vector)</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem;"><strong>机制</strong>：本地 Ollama 向量嵌入 (Nomic-embed-text)。<br><strong>作用</strong>：懂您“言外之意”的模糊映射。即使提问字眼不完全匹配，也能通过向量空间相似度捞出潜在关联文档。</p>
                </div>
                <!-- Layer 3 -->
                <div style="padding: 1.5rem; background: var(--bg-primary); border-radius: 8px; border-left: 4px solid #B0A8B9;">
                    <h4 style="margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size:1.2em;">🟣</span> Layer 3: 3D 星图关系维 (GraphRAG)</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem;"><strong>机制</strong>：基于定时生成的知识星图，解析 WikiLink 关联。<br><strong>作用</strong>：顺藤摸瓜式的深度推理。将零散知识连点成线，发现背后“A导致B”或“项目C引用配置D”的结构化关系。</p>
                </div>
                <!-- Layer 4 -->
                <div style="padding: 1.5rem; background: var(--bg-primary); border-radius: 8px; border-left: 4px solid #F76C6C;">
                    <h4 style="margin-bottom: 0.8rem; display: flex; align-items: center; gap: 0.5rem;"><span style="font-size:1.2em;">🔴</span> Layer 4: 4D 时空演化维 (Chronological)</h4>
                    <p style="color: var(--text-secondary); font-size: 0.95rem;"><strong>机制</strong>：文件时间戳追踪与 Git 历史轨迹结合。<br><strong>作用</strong>：理清事物的“前世今生”。按照时间轴倒序明确最新生效版本，彻底消除过时旧数据带来的幻觉干扰。</p>
                </div>
            </div>

            <h3 style="font-size: 1.4rem; color: var(--accent-blue); margin-bottom: 1.5rem; border-bottom: 1px solid #eee; padding-bottom: 0.5rem;">♻️ 记忆呼吸与新陈代谢系统</h3>
            <ul style="color: var(--text-secondary); line-height: 1.8; font-size: 1.05rem; list-style: none; padding-left: 0;">
                <li style="margin-bottom: 1rem; position: relative; padding-left: 1.8rem;">
                    <span style="position: absolute; left: 0; color: var(--accent-gold);">✓</span>
                    <strong>自我进化闭环 (Self-Improvement)：</strong> 运行中踩过的坑均会反思提炼成通用法则，并最终固化为核心守则。
                </li>
                <li style="position: relative; padding-left: 1.8rem;">
                    <span style="position: absolute; left: 0; color: var(--accent-gold);">✓</span>
                    <strong>自动代谢机制 (Auto-Archive)：</strong> 每晚 23:00 的 Cron 定时任务会自动将冷数据（超 30 天不活跃）安全转储至归档区，保持主脑库极致轻量。
                </li>
            </ul>
        </section>

        <!-- 技能列表模块标题 -->
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
            <div style="width: 8px; height: 32px; background: var(--accent-gold); border-radius: 4px;"></div>
            <h2 style="font-size: 1.8rem; color: var(--text-primary);">📦 已安装技能库大本营</h2>
        </div>
"""

    # Look for the insertion point
    target = '<!-- 技能图例 -->'
    
    if target in html and "核心功能：多层 4D 记忆系统" not in html:
        html = html.replace(target, article_html + '\n        ' + target)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Successfully injected 4D Memory article into skills.html!")
    else:
        print("Target not found or already injected.")

if __name__ == "__main__":
    insert_article()
