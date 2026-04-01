import os
import glob

def update_html_files():
    workspace = '/Users/jiyingguo/.openclaw/workspace/jiaviswangcai.ai'
    files = glob.glob(os.path.join(workspace, '*.html'))

    for f in files:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update Nav links across all files
        content = content.replace('>💡 技能<', '>💡 技能与功能<')
        content = content.replace('>💡 技能与功能与功能<', '>💡 技能与功能<') # Just in case it was already replaced
        
        # Update title in skills.html
        if f.endswith('skills.html'):
            content = content.replace('<title>技能展示 - 旺财Jarvis</title>', '<title>技能与功能展示 - 旺财Jarvis</title>')
            content = content.replace('<h1>🛠️ 技能展示</h1>', '<h1>🛠️ 技能与功能展示</h1>')
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

    print('Updated Nav in:', [os.path.basename(f) for f in files])

if __name__ == "__main__":
    update_html_files()
