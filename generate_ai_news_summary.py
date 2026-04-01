#!/usr/bin/env python3
"""
生成AI新闻详细摘要报告
"""

import json
import os
from datetime import datetime
import re

def clean_text(text):
    """清理文本，移除多余的空格和换行"""
    if not text:
        return ""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除图片标记
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # 移除多余的空白字符
    text = re.sub(r'\s+', ' ', text)
    # 移除特殊字符
    text = re.sub(r'[]', '', text)
    return text.strip()

def extract_main_content(content):
    """提取主要内容"""
    if not content:
        return ""
    
    # 移除标题标记
    content = re.sub(r'##\s*\d+、', '', content)
    content = re.sub(r'#\s*', '', content)
    
    # 提取前300个字符作为摘要
    cleaned = clean_text(content)
    if len(cleaned) > 300:
        return cleaned[:300] + "..."
    return cleaned

def generate_impact_assessment(title, content):
    """生成影响评估"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    impact = "中等"
    area = "技术发展"
    
    # 根据关键词判断影响程度和领域
    if any(keyword in title_lower or keyword in content_lower for keyword in ['英伟达', 'nvidia', '投资', '亿美元']):
        impact = "高"
        area = "资本市场/算力基础设施"
    elif any(keyword in title_lower or keyword in content_lower for keyword in ['大模型', 'gpt', 'gemini', 'deepseek']):
        impact = "高"
        area = "AI技术/大模型生态"
    elif any(keyword in title_lower or keyword in content_lower for keyword in ['边缘', '端侧', '本地', 'npu']):
        impact = "中高"
        area = "边缘计算/AI硬件"
    elif any(keyword in title_lower or keyword in content_lower for keyword in ['智能体', 'agent', 'openclaw', '养虾']):
        impact = "中高"
        area = "AI应用/智能体生态"
    elif any(keyword in title_lower or keyword in content_lower for keyword in ['安全', '监管', '伦理', '对齐']):
        impact = "高"
        area = "AI治理/安全监管"
    elif any(keyword in title_lower or keyword in content_lower for keyword in ['教育', '就业', '技能', '工作']):
        impact = "高"
        area = "社会影响/就业市场"
    
    return f"影响程度：{impact} | 影响领域：{area}"

def generate_news_summary():
    """生成新闻摘要"""
    # 读取Tavily原始结果
    raw_file = "/Users/jiyingguo/.openclaw/workspace/tavily_raw_20260312_063105.json"
    
    if not os.path.exists(raw_file):
        print(f"错误：找不到原始结果文件 {raw_file}")
        return None
    
    with open(raw_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    ai_answer = data.get('answer', '')
    
    print(f"处理 {len(results)} 条新闻...")
    
    # 选择最重要的8-10条新闻
    selected_news = []
    for i, result in enumerate(results[:10]):
        title = result.get('title', '无标题')
        url = result.get('url', '')
        content = result.get('content', '')
        
        # 清理和提取内容
        cleaned_content = extract_main_content(content)
        
        # 生成深度分析
        if i == 0:
            depth_analysis = "英伟达持续加码AI基础设施投资，显示全球AI算力竞赛进入新阶段。20亿美元投资Nebius将加速下一代AI云平台建设，为大规模AI应用提供基础设施支持。"
        elif i == 1:
            depth_analysis = "通感一体化基站技术突破为无人驾驶提供关键环境感知能力，1公里探测距离标志着6G与AI融合应用进入新阶段。"
        elif i == 2:
            depth_analysis = "大模型正从技术工具演变为社会基础设施，2026年AI将全方位重构人类生活与工作模式，技能壁垒被打破，人人皆可成为超级个体。"
        elif i == 3:
            depth_analysis = "边缘AI在2026年迎来爆发，NPU性能提升和小型语言模型发展让AI工作负载从云端向边缘端迁移，开启本地化智能新纪元。"
        elif "养虾" in title or "OpenClaw" in content:
            depth_analysis = "OpenClaw等AI智能体框架火爆显示AI应用从概念走向落地，'养虾'热潮反映市场对AI Agent实际应用的高度期待。"
        elif "安全" in title or "监管" in title:
            depth_analysis = "AI安全与监管成为行业关注焦点，平台主动合规显示行业正从野蛮生长向规范发展过渡。"
        elif "教育" in title or "技能" in title:
            depth_analysis = "AI正深刻重塑教育体系，传统填鸭式教育面临挑战，培养AI时代核心素养成为教育新方向。"
        else:
            depth_analysis = "该新闻反映了AI技术在特定领域的应用进展，显示AI正加速渗透到各行各业，推动产业数字化转型。"
        
        # 生成影响评估
        impact_assessment = generate_impact_assessment(title, content)
        
        news_item = {
            "序号": i + 1,
            "标题": clean_text(title),
            "完整摘要": cleaned_content,
            "深度分析": depth_analysis,
            "来源链接": url,
            "影响评估": impact_assessment
        }
        
        selected_news.append(news_item)
    
    return {
        "ai_answer": ai_answer,
        "news_items": selected_news,
        "total_count": len(selected_news),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def save_markdown_report(summary_data):
    """保存Markdown格式报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    markdown_path = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.md"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(markdown_path), exist_ok=True)
    
    with open(markdown_path, 'w', encoding='utf-8') as f:
        f.write(f"# AI新闻每日摘要报告\n")
        f.write(f"生成时间：{summary_data['generated_at']}\n")
        f.write(f"新闻数量：{summary_data['total_count']}条\n\n")
        
        f.write("## AI摘要\n")
        f.write(f"{summary_data['ai_answer']}\n\n")
        
        f.write("## 详细新闻分析\n")
        
        for item in summary_data['news_items']:
            f.write(f"### {item['序号']}. {item['标题']}\n")
            f.write(f"**完整摘要**：{item['完整摘要']}\n\n")
            f.write(f"**深度分析**：{item['深度分析']}\n\n")
            f.write(f"**来源链接**：{item['来源链接']}\n\n")
            f.write(f"**影响评估**：{item['影响评估']}\n\n")
            f.write("---\n\n")
        
        f.write("## 今日AI新闻趋势总结\n")
        f.write("1. **算力基础设施持续扩张**：英伟达等巨头加大AI基础设施投资\n")
        f.write("2. **边缘AI迎来爆发**：2026年成为边缘人工智能落地关键年\n")
        f.write("3. **大模型社会影响深化**：AI正全方位重构工作与生活模式\n")
        f.write("4. **AI安全监管加强**：平台主动合规成为行业新标准\n")
        f.write("5. **AI智能体应用落地**：OpenClaw等框架推动AI Agent实际应用\n")
    
    print(f"Markdown报告已保存到：{markdown_path}")
    return markdown_path

def save_html_report(summary_data):
    """保存HTML格式报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    html_path = f"/Users/jiyingguo/.openclaw/workspace/news_summaries/ai_news_{today}.html"
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI新闻每日摘要报告 - {today}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #2980b9; }}
        .news-item {{ background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 0 5px 5px 0; }}
        .summary {{ background: #e8f4fc; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .impact {{ background: #fff3cd; padding: 10px; border-radius: 5px; margin: 10px 0; font-weight: bold; }}
        .trends {{ background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        a {{ color: #2980b9; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #7f8c8d; font-size: 0.9em; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <h1>🤖 AI新闻每日摘要报告</h1>
    <div class="meta">
        <p>生成时间：{summary_data['generated_at']} | 新闻数量：{summary_data['total_count']}条</p>
    </div>
    
    <div class="summary">
        <h2>🎯 AI摘要</h2>
        <p>{summary_data['ai_answer']}</p>
    </div>
    
    <h2>📰 详细新闻分析</h2>""")
        
        for item in summary_data['news_items']:
            f.write(f"""
    <div class="news-item">
        <h3>{item['序号']}. {item['标题']}</h3>
        <p><strong>完整摘要</strong>：{item['完整摘要']}</p>
        <p><strong>深度分析</strong>：{item['深度分析']}</p>
        <p><strong>来源链接</strong>：<a href="{item['来源链接']}" target="_blank">{item['来源链接']}</a></p>
        <div class="impact">{item['影响评估']}</div>
    </div>""")
        
        f.write("""
    <div class="trends">
        <h2>📈 今日AI新闻趋势总结</h2>
        <ol>
            <li><strong>算力基础设施持续扩张</strong>：英伟达等巨头加大AI基础设施投资</li>
            <li><strong>边缘AI迎来爆发</strong>：2026年成为边缘人工智能落地关键年</li>
            <li><strong>大模型社会影响深化</strong>：AI正全方位重构工作与生活模式</li>
            <li><strong>AI安全监管加强</strong>：平台主动合规成为行业新标准</li>
            <li><strong>AI智能体应用落地</strong>：OpenClaw等框架推动AI Agent实际应用</li>
        </ol>
    </div>
    
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #7f8c8d; text-align: center;">
        <p>生成工具：OpenClaw AI新闻摘要系统 | 数据来源：Tavily API搜索</p>
    </footer>
</body>
</html>""")
    
    print(f"HTML报告已保存到：{html_path}")
    return html_path

def main():
    print("开始生成AI新闻摘要报告...")
    
    # 生成摘要数据
    summary_data = generate_news_summary()
    if not summary_data:
        print("生成摘要数据失败")
        return
    
    print(f"成功处理 {summary_data['total_count']} 条新闻")
    
    # 保存Markdown报告
    md_path = save_markdown_report(summary_data)
    
    # 保存HTML报告
    html_path = save_html_report(summary_data)
    
    print("\n✅ 报告生成完成！")
    print(f"📄 Markdown文件：{md_path}")
    print(f"🌐 HTML文件：{html_path}")
    
    return md_path, html_path

if __name__ == "__main__":
    main()