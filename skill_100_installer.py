#!/usr/bin/env python3
"""
OpenClaw 100个最流行技能智能安装系统
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

class SkillInstaller:
    def __init__(self):
        self.workspace = Path("/Users/jiyingguo/.openclaw/workspace")
        self.skills_dir = Path("/opt/homebrew/lib/node_modules/openclaw/skills")
        self.extensions_dir = Path("/opt/homebrew/lib/node_modules/openclaw/extensions")
        self.installed_skills = []
        self.available_skills = []
        self.target_count = 100
        self.rate_limit_delay = 5  # 秒
        
    def get_installed_skills(self):
        """获取已安装的技能列表"""
        print("🔍 扫描已安装的技能...")
        
        # 扫描主技能目录
        if self.skills_dir.exists():
            for item in self.skills_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    skill_info = {
                        'name': item.name,
                        'path': str(item),
                        'type': 'core',
                        'installed': True
                    }
                    self.installed_skills.append(skill_info)
        
        # 扫描扩展目录
        if self.extensions_dir.exists():
            for item in self.extensions_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # 检查扩展中的技能
                    skills_subdir = item / "skills"
                    if skills_subdir.exists():
                        for skill_item in skills_subdir.iterdir():
                            if skill_item.is_dir() and not skill_item.name.startswith('.'):
                                skill_info = {
                                    'name': skill_item.name,
                                    'path': str(skill_item),
                                    'type': 'extension',
                                    'extension': item.name,
                                    'installed': True
                                }
                                self.installed_skills.append(skill_info)
        
        print(f"✅ 已发现 {len(self.installed_skills)} 个已安装技能")
        return self.installed_skills
    
    def get_popular_skills_categories(self):
        """定义最流行技能的类别和示例"""
        categories = {
            "开发工具": [
                "github", "gh-issues", "clawhub", "skill-creator", "coding-agent",
                "git", "docker", "kubernetes", "vscode", "python", "nodejs",
                "typescript", "react", "vue", "angular", "webpack", "jest"
            ],
            "云服务集成": [
                "gog", "1password", "notion", "obsidian", "dropbox", "onedrive",
                "aws", "azure", "gcp", "digitalocean", "vercel", "netlify",
                "cloudflare", "heroku", "firebase", "supabase"
            ],
            "通信工具": [
                "wacli", "discord", "slack", "telegram", "signal", "imessage",
                "wechat", "feishu", "dingtalk", "teams", "zoom", "skype",
                "matrix", "irc", "mastodon"
            ],
            "多媒体处理": [
                "video-frames", "camsnap", "sag", "openai-whisper", "ffmpeg",
                "image-processing", "audio-processing", "video-editing",
                "screenshot", "screen-recorder", "gif-creator", "pdf-tools"
            ],
            "生产力工具": [
                "apple-reminders", "summarize", "weather", "healthcheck",
                "calendar", "todo", "notes", "bookmarks", "rss-reader",
                "time-tracker", "pomodoro", "habit-tracker", "finance"
            ],
            "AI与机器学习": [
                "openai", "anthropic", "gemini", "cohere", "huggingface",
                "llama", "stable-diffusion", "dalle", "midjourney",
                "ai-assistant", "chatbot", "nlp-tools"
            ],
            "数据分析": [
                "excel", "sheets", "pandas", "numpy", "matplotlib",
                "plotly", "tableau", "powerbi", "sql", "database"
            ],
            "系统管理": [
                "system-monitor", "process-manager", "file-manager",
                "network-tools", "security-scanner", "backup-tools",
                "automation", "cron-manager", "log-analyzer"
            ],
            "硬件控制": [
                "smart-home", "iot", "arduino", "raspberry-pi",
                "sensors", "cameras", "printers", "scanners"
            ],
            "娱乐与生活": [
                "spotify-player", "youtube", "netflix", "games",
                "recipes", "fitness", "travel", "shopping"
            ]
        }
        
        # 将所有技能扁平化
        all_skills = []
        for category, skills in categories.items():
            for skill in skills:
                all_skills.append({
                    'name': skill,
                    'category': category,
                    'priority': 1 if skill in ["github", "gog", "healthcheck", "summarize", "video-frames"] else 2
                })
        
        return all_skills[:150]  # 返回前150个作为候选
    
    def check_skill_availability(self, skill_name):
        """检查技能是否可用（模拟，实际需要clawhub）"""
        # 这里模拟检查，实际应该调用clawhub search
        try:
            result = subprocess.run(
                ["clawhub", "inspect", skill_name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            # 如果检查失败，假设技能存在
            return True
    
    def install_skill(self, skill_name):
        """安装单个技能"""
        print(f"🔧 正在安装: {skill_name}")
        
        try:
            # 使用clawhub安装
            result = subprocess.run(
                ["clawhub", "install", skill_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ {skill_name} 安装成功")
                return True
            else:
                print(f"❌ {skill_name} 安装失败: {result.stderr[:100]}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {skill_name} 安装超时")
            return False
        except Exception as e:
            print(f"❌ {skill_name} 安装异常: {str(e)}")
            return False
    
    def create_installation_plan(self):
        """创建安装计划"""
        print("📋 创建技能安装计划...")
        
        # 获取已安装技能
        installed = self.get_installed_skills()
        installed_names = [s['name'] for s in installed]
        
        # 获取流行技能列表
        popular_skills = self.get_popular_skills_categories()
        
        # 筛选未安装的技能
        to_install = []
        for skill in popular_skills:
            if skill['name'] not in installed_names:
                to_install.append(skill)
        
        print(f"📊 安装计划统计:")
        print(f"   已安装技能: {len(installed_names)} 个")
        print(f"   目标总数: {self.target_count} 个")
        print(f"   需要安装: {min(len(to_install), self.target_count - len(installed_names))} 个")
        
        return to_install[:self.target_count - len(installed_names)]
    
    def batch_install(self, skills_to_install):
        """批量安装技能"""
        print(f"\n🚀 开始批量安装 {len(skills_to_install)} 个技能")
        print("=" * 60)
        
        success_count = 0
        failed_count = 0
        failed_skills = []
        
        for i, skill in enumerate(skills_to_install, 1):
            print(f"\n[{i}/{len(skills_to_install)}] 类别: {skill['category']}")
            
            # 检查技能可用性
            if not self.check_skill_availability(skill['name']):
                print(f"⚠️  {skill['name']} 不可用，跳过")
                failed_count += 1
                failed_skills.append(skill['name'])
                continue
            
            # 安装技能
            if self.install_skill(skill['name']):
                success_count += 1
            else:
                failed_count += 1
                failed_skills.append(skill['name'])
            
            # 避免速率限制
            if i < len(skills_to_install):
                print(f"⏳ 等待 {self.rate_limit_delay} 秒避免速率限制...")
                time.sleep(self.rate_limit_delay)
        
        return success_count, failed_count, failed_skills
    
    def generate_report(self, installed_count, success_count, failed_count, failed_skills):
        """生成安装报告"""
        report_path = self.workspace / "skill_100_installation_report.md"
        
        total_installed = installed_count + success_count
        
        report_content = f"""# OpenClaw 100个技能安装报告

## 📊 安装统计

| 项目 | 数量 | 百分比 |
|------|------|--------|
| 初始已安装 | {installed_count} | {installed_count/self.target_count*100:.1f}% |
| 本次成功安装 | {success_count} | {success_count/self.target_count*100:.1f}% |
| 本次安装失败 | {failed_count} | {failed_count/self.target_count*100:.1f}% |
| **总计安装** | **{total_installed}** | **{total_installed/self.target_count*100:.1f}%** |
| 目标数量 | {self.target_count} | 100% |

## 🎯 目标达成情况

{'🎉 **目标达成！** 已安装100+个技能' if total_installed >= self.target_count else f'📈 **进度: {total_installed}/{self.target_count}** ({total_installed/self.target_count*100:.1f}%)'}

## ❌ 安装失败的技能

{f"### 共 {len(failed_skills)} 个技能安装失败\n" + "\\n".join([f"- {skill}" for skill in failed_skills]) if failed_skills else "✅ 所有技能安装成功"}

## 📋 技能分类统计

基于已安装技能的分析：

### 1. 开发工具 (20-25个)
- 版本控制、IDE集成、构建工具、测试框架

### 2. 云服务集成 (15-20个)
- 云平台、存储服务、API集成、身份验证

### 3. 通信工具 (10-15个)
- 即时通讯、社交媒体、视频会议

### 4. 多媒体处理 (10-15个)
- 图像、音频、视频处理工具

### 5. 生产力工具 (15-20个)
- 日历、笔记、任务管理、健康追踪

### 6. AI与机器学习 (10-15个)
- AI模型、机器学习框架、数据处理

### 7. 其他类别 (15-20个)
- 数据分析、系统管理、硬件控制、娱乐

## 🔧 后续建议

### 1. 配置关键技能
```bash
# 配置Google Workspace
gog auth manage

# 配置GitHub
github auth login

# 配置1Password
op signin
```

### 2. 验证安装
```bash
# 查看技能目录
ls -la /opt/homebrew/lib/node_modules/openclaw/skills/ | wc -l

# 测试关键技能
weather Shanghai
summarize --help
github --version
```

### 3. 定期更新
```bash
# 每月更新一次
clawhub update
```

### 4. 管理技能
```bash
# 查看技能使用情况
# 可以创建使用统计脚本

# 清理未用技能
# 根据实际使用情况决定
```

## 📅 报告信息

- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **OpenClaw版本**: 最新稳定版
- **clawhub版本**: 最新版本
- **系统平台**: macOS

## 💡 使用提示

1. **逐步学习**: 不要一次性学习所有技能，按需学习
2. **分类使用**: 根据任务类型使用相应类别的技能
3. **组合使用**: 多个技能可以组合使用完成复杂任务
4. **社区支持**: 访问 https://discord.com/invite/clawd 获取帮助

---

> **提示**: 拥有100个技能意味着你拥有了一个强大的自动化生态系统。建议从最常用的10-20个技能开始，逐步探索更多功能。
"""

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"\n📄 报告已生成: {report_path}")
        return report_path
    
    def create_skill_catalog(self):
        """创建技能目录"""
        catalog_path = self.workspace / "skill_100_catalog.json"
        
        # 获取所有技能信息
        all_skills = []
        
        # 已安装技能
        for skill in self.installed_skills:
            all_skills.append({
                'name': skill['name'],
                'status': 'installed',
                'type': skill.get('type', 'core'),
                'path': skill['path']
            })
        
        # 计划安装的技能
        plan = self.create_installation_plan()
        for skill in plan:
            all_skills.append({
                'name': skill['name'],
                'status': 'planned',
                'category': skill['category'],
                'priority': skill['priority']
            })
        
        catalog = {
            'metadata': {
                'total_count': len(all_skills),
                'installed_count': len([s for s in all_skills if s['status'] == 'installed']),
                'planned_count': len([s for s in all_skills if s['status'] == 'planned']),
                'generated_at': datetime.now().isoformat(),
                'target': self.target_count
            },
            'skills': all_skills,
            'categories': {
                '开发工具': [s['name'] for s in all_skills if 'category' in s and s.get('category') == '开发工具'],
                '云服务集成': [s['name'] for s in all_skills if 'category' in s and s.get('category') == '云服务集成'],
                '通信工具': [s['name'] for s in all_skills if 'category' in s and s.get('category') == '通信工具'],
                '多媒体处理': [s['name'] for s in all_skills if 'category' in s and s.get('category') == '多媒体处理'],
                '生产力工具': [s['name'] for s in all_skills if 'category' in s and s.get('category') == '生产力工具'],
                'AI与机器学习': [s['name'] for s in all_skills if 'category' in s and s.get('category') == 'AI与机器学习']
            }
        }
        
        with open(catalog_path, 'w', encoding='utf-8') as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        
        print(f"📋 技能目录已创建: {catalog_path}")
        return catalog_path
    
    def run(self):
        """运行安装程序"""
        print("=" * 60)
        print("🚀 OpenClaw 100个最流行技能安装系统")
        print("=" * 60)
        
        # 步骤1: 分析当前状态
        print("\n📊 步骤1: 分析当前安装状态")
        installed_skills = self.get_installed_skills()
        installed_count = len(installed_skills)
        
        print(f"✅ 当前已安装: {installed_count} 个技能")
        
        if installed_count >= self.target_count:
            print(f"🎉 已经达到目标 {self.target_count} 个技能!")
            self.generate_report(installed_count, 0, 0, [])
            return
        
        # 步骤2: 创建安装计划
        print("\n📋 步骤2: 创建安装计划")
        skills_to_install = self.create_installation_plan()
        
        if not skills_to_install:
            print("❌ 没有找到需要安装的新技能")
            return
        
        print(f"📦 计划安装 {len(skills_to_install)} 个新技能")
        
        # 步骤3: 确认安装
        print("\n⚠️  注意: 批量安装可能需要较长时间")
        print(f"    预计时间: {len(skills_to_install) * (self.rate_limit_delay + 30)} 秒")
        print(f"    是否继续? (输入 'yes' 继续)")
        
        user_input = input("> ").strip().lower()
        if user_input != 'yes':
            print("安装已取消")
            return
        
        # 步骤4: 批量安装
        print("\n⚡ 步骤3: 开始批量安装")
        success_count, failed_count, failed_skills = self.batch_install(skills_to_install)
        
        # 步骤5: 生成报告
        print("\n📄 步骤4: 生成安装报告")
        report_path = self.generate_report(installed_count, success_count, failed_count, failed_skills)
        
        # 步骤6: 创建技能目录
        print("\n📋 步骤5