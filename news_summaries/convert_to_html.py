#!/usr/bin/env python3
# 简单的Markdown转HTML转换器

import re
import sys
import os

def markdown_to_html(md_text):
    """将Markdown转换为简单的HTML"""
    
    # 转换标题
    md_text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)
    
    # 转换列表
    md_text = re.sub(r'^- (.*?)$', r'<li>\1</li>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'(<li>.*?</li>\n)+', r'<ul>\g<0></ul>', md_text)
    
    # 转换粗体
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', md_text)
    
    # 转换链接
    md_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', md_text)
    
    # 转换代码块
    md_text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', md_text, flags=re.DOTALL)
    md_text = re.sub(r'`(.*?)`', r'<code>\1</code>', md_text)
    
    # 转换段落
    lines = md_text.split('\n')
    html_lines = []
    in_paragraph = False
    current_paragraph = []
    
    for line in lines:
        if line.strip() == '':
            if current_paragraph:
                html_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
                in_paragraph = False
        elif line.startswith('<') and line.endswith('>'):
            # 已经是HTML标签
            if current_paragraph:
                html_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
                current_paragraph = []
            html_lines.append(line)
        else:
            current_paragraph.append(line)
            in_paragraph = True
    
    if current_paragraph:
        html_lines.append('<p>' + ' '.join(current_paragraph) + '</p>')
    
    return '\n'.join(html_lines)

def main():
    if len(sys.argv) != 3:
        print("用法: python3 convert_to_html.py input.md output.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)
    
    # 读取Markdown文件
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 转换为HTML
    html_body = markdown_to_html(md_content)
    
    # 创建完整的HTML文档
    html_template = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI新闻日报 - 2026年3月16日</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            padding-bottom: 5px;
            border-bottom: 1px solid #eee;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        .overview {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #3498db;
        }}
        .news-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 25px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-left: 4px solid #2ecc71;
        }}
        .source {{
            color: #7f8c8d;
            font-size: 0.9em;
            margin: 10px 0;
        }}
        .analysis {{
            background: #e8f6f3;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            border-left: 3px solid #1abc9c;
        }}
        .trend {{
            background: #e8f4fc;
            padding: 20px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 4px solid #3498db;
        }}
        a {{
            color: #2980b9;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
            color: #1a5276;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        .footer {{
            color: #95a5a6;
            font-size: 0.9em;
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
        }}
        code {{
            background: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
{html_body}
<div class="footer">
    报告生成时间：2026-03-16 06:30 | 数据来源：Tavily API全球搜索<br>
    AI新闻监控系统 - 每日自动生成
</div>
</body>
</html>'''
    
    # 写入HTML文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"✅ HTML文件已生成: {output_file}")

if __name__ == "__main__":
    main()