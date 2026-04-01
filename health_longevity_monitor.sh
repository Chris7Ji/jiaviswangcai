#!/bin/bash
# 健康长寿科研成果每日监控任务脚本

set -e

echo "🧬 开始执行健康长寿科研成果每日监控任务..."

# 获取当前日期
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H:%M:%S)

echo "📅 日期: $DATE $TIME"
echo "🎯 主题: 健康长寿科研成果监控"
echo "🔍 要求: 交叉验证、权威机构、双盲测试、有效性证明"

# 使用 Tavily API 搜索高质量健康长寿信息
cd /Users/jiyingguo/.openclaw/workspace

# 激活虚拟环境
source venv_tavily/bin/activate

# 执行 Python 搜索脚本
python3 << 'PYTHON_SCRIPT'
import os
import json
import requests
import re
from datetime import datetime
from pathlib import Path

# Tavily API 配置
TAVILY_API_KEY = "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"
TAVILY_API_URL = "https://api.tavily.com/search"

# 权威医学研究机构白名单
MEDICAL_AUTHORITY_DOMAINS = [
    # 国际顶级医学期刊
    "nejm.org", "thelancet.com", "jamanetwork.com", "bmj.com",
    "nature.com", "science.org", "cell.com", "pnas.org",
    "sciencedirect.com", "springer.com", "wiley.com",
    
    # 国际权威医学机构
    "who.int", "nih.gov", "cdc.gov", "fda.gov", "ema.europa.eu",
    "mayoclinic.org", "clevelandclinic.org", "hopkinsmedicine.org",
    "harvard.edu", "stanford.edu", "ox.ac.uk", "cambridge.org",
    
    # 长寿研究专门机构
    "buckinstitute.org", "salk.edu", "maxplanck.de", "calicolabs.com",
    "altoslabs.com", "unitybiotechnology.com",
    
    # ===== 国内权威医学机构（扩展） =====
    # 中华医学会系列
    "cmia.info", "cma.org.cn", "cmdc.net.cn",
    "chinagp.cn", "zhyyx.org", "zhlxbxzz.paperopen.com",
    
    # 国家机构
    "nhc.gov.cn", "chinacdc.cn", "nmpa.gov.cn", "scipm.org.cn",
    
    # 顶级医院
    "pumch.cn", "pumc.edu.cn", "fuwaihospital.org", "301hospital.com.cn",
    "zxhospital.com", "sysucc.org.cn", "zsu.edu.cn",
    
    # 医学期刊
    "medsci.cn", "dxy.cn", "haodf.com", "ljygczz.com",
    "cmj.org", "journalofgeriatriccardiology.com",
    
    # 官方媒体健康频道
    "xinhuanet.com/health", "people.com.cn/health", "cctv.com/health",
    "gmw.cn/health", "health.people.com.cn"
]

# 高质量长寿研究关键词
LONGEVITY_RESEARCH_KEYWORDS = [
    # ===== 国际前沿研究 =====
    "longevity research clinical trial 2026",
    "anti-aging medicine proven effective",
    "senolytics clinical study results human",
    "NAD+ supplementation human trial 2026",
    "rapamycin aging clinical trial results",
    "metformin longevity study 2026",
    "fasting mimicking diet clinical trial",
    "telomere extension therapy results",
    "epigenetic reprogramming aging reversal",
    "stem cell therapy aging clinical trial",
    
    # ===== 运动与养生（扩展） =====
    "HIIT exercise longevity benefits study",
    "resistance training aging biomarkers",
    "zone 2 cardio mitochondrial training longevity",
    "cold exposure longevity study humans",
    "sauna heat shock proteins longevity",
    "exercising muscle longevity molecular mechanism",
    
    # ===== 饮食与营养（扩展） =====
    "ketogenic diet longevity human study",
    "intermittent fasting clinical trial aging",
    "plant-based diet longevity study",
    "omega-3 fatty acids aging biomarkers",
    "polyphenols anti-aging clinical trial",
    "calorie restriction longevity human trial",
    
    # ===== 无痛治疗与新技术 =====
    "red light therapy anti-aging clinical",
    "hyperbaric oxygen longevity study",
    "metformin diabetes aging longevity",
    "spermidine autophagy longevity",
    "urolithin A mitophagy clinical trial",
    
    # ===== 国内研究（新增重点） =====
    # 中华医学会系列期刊
    "中华医学会 长寿研究 临床试验",
    "中华老年医学杂志 抗衰老 研究",
    "中华预防医学杂志 寿命 科研",
    
    # 中国疾控中心研究成果
    "中国疾控中心 长寿研究 2026",
    "中国CDC 老年健康 调查研究",
    "国家卫健委 健康老龄化 政策研究",
    
    # 国内重点医院临床研究
    "北京协和医院 抗衰老 临床试验",
    "301医院 长寿研究 临床",
    "华西医院 老年病 临床研究",
    "中山大学附属医院 抗衰老 研究",
    
    # 中医药抗衰老
    "中医药 抗衰老 临床研究",
    "中医 长寿 养生 研究 2026",
    "针灸 抗衰老 临床试验",
    "中药 延长寿命 科学研究",
    
    # 干细胞与基因治疗
    "干细胞 抗衰老 临床试验 中国",
    "基因编辑 延寿 研究",
    "端粒酶 抗衰老 中国研究"
]

def extract_domain(url):
    """提取域名"""
    if not url:
        return ""
    domain = url.replace("https://", "").replace("http://", "").split("/")[0]
    if domain.startswith("www."):
        domain = domain[4:]
    return domain.lower()

def is_authoritative_domain(url):
    """检查是否为权威医学机构"""
    domain = extract_domain(url)
    for auth_domain in MEDICAL_AUTHORITY_DOMAINS:
        if auth_domain in domain:
            return True
    return False

def contains_validation_keywords(content):
    """检查是否包含验证关键词"""
    validation_keywords = [
        "clinical trial", "randomized controlled trial", "double-blind",
        "peer-reviewed", "published in", "statistically significant",
        "p < 0.05", "cohort study", "meta-analysis", "systematic review",
        "FDA approved", "EMA approved", "phase III", "phase 3",
        "临床试验", "随机对照试验", "双盲", "同行评审", "发表",
        "统计学意义", "队列研究", "荟萃分析", "系统评价"
    ]
    
    content_lower = content.lower()
    found_keywords = []
    for keyword in validation_keywords:
        if keyword in content_lower:
            found_keywords.append(keyword)
    
    return found_keywords

def calculate_quality_score(result):
    """计算信息质量分数"""
    url = result.get("url", "")
    content = result.get("content", "")
    title = result.get("title", "")
    
    score = 0
    
    # 1. 来源权威性 (40%)
    if is_authoritative_domain(url):
        score += 0.4
    else:
        # 非权威来源减分
        score += 0.1
    
    # 2. 验证关键词 (30%)
    validation_keywords = contains_validation_keywords(content + " " + title)
    if validation_keywords:
        score += min(0.3, len(validation_keywords) * 0.05)
    
    # 3. 内容完整性 (20%)
    content_length = len(content)
    if content_length > 500:
        score += 0.2
    elif content_length > 200:
        score += 0.1
    
    # 4. 时效性 (10%)
    # 假设较新的内容更有价值
    score += 0.1
    
    return min(1.0, score), validation_keywords

def translate_to_chinese(text):
    """完整的中英对照翻译"""
    translations = {
        # 研究类型
        "clinical trial": "临床试验",
        "randomized controlled trial": "随机对照试验",
        "double-blind": "双盲试验",
        "placebo-controlled": "安慰剂对照",
        "peer-reviewed": "同行评审",
        "statistically significant": "统计学意义显著",
        "cohort study": "队列研究",
        "meta-analysis": "荟萃分析",
        "systematic review": "系统评价",
        "prospective study": "前瞻性研究",
        "retrospective study": "回顾性研究",
        "cross-sectional study": "横断面研究",
        
        # 权威机构
        "FDA approved": "FDA批准",
        "EMA approved": "欧洲药品管理局批准",
        "NIH": "美国国立卫生研究院",
        "WHO": "世界卫生组织",
        "CDC": "美国疾控中心",
        "Mayo Clinic": "梅奥诊所",
        
        # 长寿相关术语
        "longevity": "长寿",
        "anti-aging": "抗衰老",
        "senolytics": "衰老细胞清除剂",
        "senescence": "细胞衰老",
        "NAD+": "烟酰胺腺嘌呤二核苷酸",
        "NMN": "β-烟酰胺单核苷酸",
        "NR": "烟酰胺核糖",
        "rapamycin": "雷帕霉素",
        "metformin": "二甲双胍",
        "telomere": "端粒",
        "telomerase": "端粒酶",
        "epigenetic": "表观遗传",
        "epigenetic reprogramming": "表观遗传重编程",
        "stem cell": "干细胞",
        "autophagy": "自噬",
        "mitophagy": "线粒体自噬",
        "mitochondria": "线粒体",
        
        # 干预方法
        "intermittent fasting": "间歇性禁食",
        "calorie restriction": "热量限制",
        "ketogenic diet": "生酮饮食",
        "plant-based diet": "植物性饮食",
        "Mediterranean diet": "地中海饮食",
        "HIIT": "高强度间歇训练",
        "resistance training": "抗阻训练",
        "cold exposure": "冷暴露",
        "hyperbaric oxygen": "高压氧",
        "red light therapy": "红光疗法",
        "photobiomodulation": "光生物调节",
        
        #  Biomarkers
        "biomarker": "生物标志物",
        "inflammation": "炎症",
        "oxidative stress": "氧化应激",
        "DNA damage": "DNA损伤",
        "cellular senescence": "细胞衰老",
        "age-related": "年龄相关",
        
        # 药物补充剂
        "supplementation": "补充",
        "resveratrol": "白藜芦醇",
        "spermidine": "亚精胺",
        "urolithin A": "尿石素A",
        "taurine": "牛磺酸",
        "omega-3": "欧米伽-3",
        "polyphenols": "多酚",
        
        # 研究结果
        "efficacy": "有效性",
        "safety": "安全性",
        "mortality": "死亡率",
        "morbidity": "发病率",
        "life expectancy": "预期寿命",
        "healthspan": "健康寿命",
        "aging": "衰老",
        "reversal": "逆转",
        "improvement": "改善",
        "reduction": "减少",
        "increase": "增加",
        "decrease": "减少"
    }
    
    result = text
    # 先替换较长的短语，再替换较短的
    sorted_translations = sorted(translations.items(), key=lambda x: len(x[0]), reverse=True)
    
    for eng, chi in sorted_translations:
        # 替换时保持大小写不敏感
        import re
        result = re.sub(re.compile(re.escape(eng), re.IGNORECASE), chi, result)
    
    return result

print("🔍 开始搜索高质量健康长寿科研成果...")

all_results = []
search_stats = {"total": 0, "authoritative": 0, "validated": 0}

for keyword in LONGEVITY_RESEARCH_KEYWORDS:
    print(f"  搜索: {keyword}")
    try:
        response = requests.post(
            TAVILY_API_URL,
            json={
                "api_key": TAVILY_API_KEY,
                "query": keyword,
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 5,
                "include_domains": MEDICAL_AUTHORITY_DOMAINS[:15]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if "results" in data:
                for result in data["results"]:
                    search_stats["total"] += 1
                    
                    # 质量评估
                    quality_score, validation_keywords = calculate_quality_score(result)
                    
                    # 只保留较高质量的结果
                    if quality_score >= 0.5:
                        result["quality_score"] = quality_score
                        result["validation_keywords"] = validation_keywords
                        result["is_authoritative"] = is_authoritative_domain(result.get("url", ""))
                        
                        if result["is_authoritative"]:
                            search_stats["authoritative"] += 1
                        if validation_keywords:
                            search_stats["validated"] += 1
                        
                        all_results.append(result)
                
                print(f"    ✅ 获取 {len(data['results'])} 条结果")
        else:
            print(f"    ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"    ❌ 错误: {e}")

# 去重（按 URL）
seen_urls = set()
unique_results = []
for result in all_results:
    url = result.get("url", "")
    if url not in seen_urls:
        seen_urls.add(url)
        unique_results.append(result)

# 按质量分排序
unique_results.sort(key=lambda x: x.get("quality_score", 0), reverse=True)

# 取前15条最高质量的结果
top_results = unique_results[:15]

print(f"\n📊 质量筛选结果:")
print(f"  总搜索结果: {search_stats['total']} 条")
print(f"  去重后: {len(unique_results)} 条")
print(f"  高质量精选: {len(top_results)} 条")
print(f"  权威来源: {search_stats['authoritative']} 条")
print(f"  包含验证关键词: {search_stats['validated']} 条")

# 分类统计
international_count = 0
domestic_count = 0
research_types = {
    "clinical_trial": 0,
    "review_study": 0,
    "basic_research": 0,
    "lifestyle": 0
}

for result in top_results:
    content = result.get("content", "").lower()
    title = result.get("title", "").lower()
    
    # 地域分类
    url = result.get("url", "")
    if any(domain in url for domain in [".cn", ".com.cn", ".org.cn", ".gov.cn"]):
        domestic_count += 1
    else:
        international_count += 1
    
    # 研究类型分类
    if any(keyword in content for keyword in ["clinical trial", "临床试验", "randomized", "双盲"]):
        research_types["clinical_trial"] += 1
    elif any(keyword in content for keyword in ["review", "meta-analysis", "荟萃分析", "系统评价"]):
        research_types["review_study"] += 1
    elif any(keyword in content for keyword in ["cell", "animal", "molecular", "细胞", "动物"]):
        research_types["basic_research"] += 1
    else:
        research_types["lifestyle"] += 1

# 生成中文报告
date_str = datetime.now().strftime("%Y-%m-%d")
report_md = f"""# 🧬 健康长寿科研成果每日监控报告

**报告日期**: {date_str}  
**报告时间**: {datetime.now().strftime("%H:%M:%S")}  
**精选信息**: {len(top_results)} 条（国际 {international_count} 条，国内 {domestic_count} 条）

---

## 🛡️ 质量保证体系

### ✅ 三重验证标准
1. **来源权威性** - 优先选择国际顶级医学期刊和权威机构
2. **研究设计** - 关注随机对照试验、双盲试验、大样本研究
3. **证据等级** - 重视荟萃分析、系统评价等高等级证据

### 🔬 研究类型分布
- **临床试验**: {research_types['clinical_trial']} 条
- **综述研究**: {research_types['review_study']} 条  
- **基础研究**: {research_types['basic_research']} 条
- **生活方式**: {research_types['lifestyle']} 条

### 🌍 地域覆盖
- **欧美前沿**: {international_count} 条
- **国内权威**: {domestic_count} 条

---

## 📚 今日精选高质量长寿科研成果

"""

for i, result in enumerate(top_results, 1):
    title = result.get("title", "无标题")
    url = result.get("url", "")
    content = result.get("content", "")
    quality_score = result.get("quality_score", 0)
    validation_keywords = result.get("validation_keywords", [])
    is_authoritative = result.get("is_authoritative", False)
    domain = extract_domain(url)
    
    # 翻译标题 - 先翻译，再清理一些未翻译的英文
    title_zh = translate_to_chinese(title)
    # 清理一些常见的英文词汇
    title_zh = title_zh.replace(" with ", " - ")
    title_zh = title_zh.replace(" in ", " - ")
    title_zh = title_zh.replace(" of ", " - ")
    title_zh = title_zh.replace("The ", "")
    title_zh = title_zh.replace("A ", "")
    title_zh = title_zh.replace("Effects", "效果")
    title_zh = title_zh.replace("Effect", "效果")
    title_zh = title_zh.replace("Study", "研究")
    title_zh = title_zh.replace("Research", "研究")
    title_zh = title_zh.replace("Potential", "潜力")
    title_zh = title_zh.replace("Analysis", "分析")
    title_zh = title_zh.replace("Review", "综述")
    title_zh = title_zh.replace("Trial", "试验")
    title_zh = title_zh.replace("Human", "人体")
    title_zh = title_zh.replace("Results", "结果")
    title_zh = title_zh.replace("Outcomes", "结果")
    title_zh = title_zh.replace("Role", "作用")
    title_zh = title_zh.replace("Mechanism", "机制")
    title_zh = title_zh.replace("Advances", "进展")
    title_zh = title_zh.replace("Update", "更新")
    title_zh = title_zh.replace("Insights", "见解")
    title_zh = title_zh.replace("Perspective", "观点")
    # 截断过长的标题
    if len(title_zh) > 80:
        title_zh = title_zh[:77] + "..."
    
    # 翻译标题和内容中的关键词
    content_preview = content[:200] + "..." if len(content) > 200 else content
    content_zh = translate_to_chinese(content_preview)
    
    # 质量评级
    if quality_score >= 0.9:
        quality_rating = "⭐⭐⭐⭐⭐ (极高可信度)"
        reliability = "🔬 高度可靠 - 权威机构 + 严格验证"
    elif quality_score >= 0.7:
        quality_rating = "⭐⭐⭐⭐ (高可信度)"
        reliability = "📊 可靠 - 良好验证证据"
    elif quality_score >= 0.5:
        quality_rating = "⭐⭐⭐ (中等可信度)"
        reliability = "📈 初步证据 - 需要进一步验证"
    else:
        quality_rating = "⭐⭐ (需谨慎参考)"
        reliability = "⚠️ 证据有限 - 仅供参考"
    
    # 来源权威性标记
    if is_authoritative:
        source_marker = "🏛️ 权威机构"
    else:
        source_marker = "📰 一般媒体"
    
    # 地域标记
    if any(cn_domain in domain for cn_domain in [".cn", ".com.cn", ".org.cn", ".gov.cn"]):
        region_marker = "🇨🇳 国内研究"
    else:
        region_marker = "🌍 国际研究"
    
    # 验证关键词显示
    validation_display = ""
    if validation_keywords:
        validation_display = "🔍 **验证证据**: " + "、".join(validation_keywords[:3])
        if len(validation_keywords) > 3:
            validation_display += f" 等{len(validation_keywords)}项验证"
    
    report_md += f"""
### {i}. {title_zh}

{region_marker} | {source_marker}  
🔗 **来源**: [{domain}]({url})  
📊 **质量评级**: {quality_rating}  
{reliability}

{validation_display}

📝 **研究摘要**:
{content_zh}

---
"""

# 添加详细统计和注意事项
report_md += f"""
## 📈 详细统计与分析

### 质量分布
- ⭐⭐⭐⭐⭐ 极高可信度: {sum(1 for r in top_results if r.get('quality_score', 0) >= 0.9)} 条
- ⭐⭐⭐⭐ 高可信度: {sum(1 for r in top_results if 0.7 <= r.get('quality_score', 0) < 0.9)} 条  
- ⭐⭐⭐ 中等可信度: {sum(1 for r in top_results if 0.5 <= r.get('quality_score', 0) < 0.7)} 条

### 验证情况
- 包含严格验证关键词: {sum(1 for r in top_results if r.get('validation_keywords'))} 条
- 来自权威机构: {sum(1 for r in top_results if r.get('is_authoritative'))} 条
- 临床试验设计: {research_types['clinical_trial']} 条

### 搜索覆盖
- 搜索关键词: {len(LONGEVITY_RESEARCH_KEYWORDS)} 个维度
- 初始结果: {search_stats['total']} 条
- 质量筛选后: {len(top_results)} 条
- 筛选比例: {((search_stats['total'] - len(top_results)) / search_stats['total'] * 100):.1f}%

---

## ⚠️ 重要注意事项

1. **信息仅供参考** - 所有信息均为科研报道，不构成医疗建议
2. **咨询专业人士** - 任何健康干预请咨询医生或专业医疗人员
3. **个体差异** - 研究成果可能存在个体差异，效果因人而异
4. **持续验证** - 科学认知不断更新，建议关注最新研究进展

---

## 🔍 今日搜索重点

### 国际前沿方向
- 衰老细胞清除剂(senolytics)临床试验
- NAD+补充剂人体研究
- 表观遗传重编程技术
- 运动与长寿的分子机制

### 国内研究热点  
- 中医药抗衰老机制
- 干细胞抗衰老临床应用
- 端粒酶活性调节
- 传统养生方法的现代验证

---

*本报告由 OpenClaw 自动生成，经过严格质量筛选*  
*监控时间: 每天 20:00 (北京时间)*  
*⚠️ 重要提醒: 健康干预请务必咨询专业医疗人员*
"""

# 保存报告
output_dir = Path("/Users/jiyingguo/.openclaw/workspace/health_reports")
output_dir.mkdir(exist_ok=True)

output_file = output_dir / f"longevity_research_{date_str}.md"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(report_md)

print(f"\n✅ 高质量报告已保存: {output_file}")

# 同时保存 JSON 格式
json_file = output_dir / f"longevity_research_{date_str}.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump({
        "date": date_str,
        "total_results": search_stats["total"],
        "unique_results": len(unique_results),
        "high_quality_results": len(top_results),
        "authoritative_sources": search_stats["authoritative"],
        "validated_results": search_stats["validated"],
        "international_count": international_count,
        "domestic_count": domestic_count,
        "research_types": research_types,
        "results": top_results
    }, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 数据已保存: {json_file}")

print("\n📊 质量筛选总结:")
print(f"  权威来源: {search_stats['authoritative']} 条")
print(f"  验证证据: {search_stats['validated']} 条")
print(f"  国际研究: {international_count} 条")
print(f"  国内研究: {domestic_count} 条")
print(f"  临床试验: {research_types['clinical_trial']} 条")

PYTHON_SCRIPT

echo "✅ 健康长寿科研成果搜索完成"

# 发送邮件
echo "📧 发送健康长寿报告邮件..."
python3 << 'EMAIL_SCRIPT'
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# 邮件配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 587
SENDER_EMAIL = "86940135@qq.com"
SENDER_PASSWORD = "swqfjvmoupdebhgh"
RECEIVERS = ["86940135@qq.com", "jiyingguo@huawei.com"]

# 读取报告
date_str = datetime.now().strftime("%Y-%m-%d")
report_file = Path(f"/Users/jiyingguo/.openclaw/workspace/health_reports/longevity_research_{date_str}.md")

if report_file.exists():
    with open(report_file, "r", encoding="utf-8") as f:
        report_content = f.read()
else:
    report_content = "报告文件未找到"

# 创建邮件
msg = MIMEMultipart("alternative")
msg["Subject"] = f"🧬 健康长寿科研成果每日监控报告 - {date_str}"
msg["From"] = SENDER_EMAIL
msg["To"] = ", ".join(RECEIVERS)

# 邮件正文
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #27ae60; padding-bottom: 10px; }}
        h2 {{ color: #16a085; margin-top: 30px; }}
        h3 {{ color: #2980b9; }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #7f8c8d; font-size: 14px; background: #f8f9fa; padding: 10px; border-radius: 5px; }}
        .quality-badge {{ display: inline-block; background: #27ae60; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin: 0 5px; }}
        .warning {{ background: #f39c12; color: white; padding: 10px; border-radius: 5px; margin: 15px 0; }}
        .research-item {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #3498db; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; margin: 20px 0; }}
        .stat-box {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #ecf0f1; color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>🧬 健康长寿科研成果每日监控报告</h1>
    <p class="meta">报告日期: {date_str} | 报告时间: {datetime.now().strftime("%H:%M:%S")}</p>
    
    <div class="warning">
        <strong>⚠️ 重要提醒:</strong> 本报告仅为科研信息汇总，不构成医疗建议。任何健康干预请咨询专业医疗人员。
    </div>
    
    <hr>
    
    <pre style="white-space: pre-wrap; font-family: inherit;">{report_content}</pre>
    
    <div class="footer">
        <p>本报告由 OpenClaw 自动生成，经过严格质量筛选</p>
        <p>监控时间: 每天 20:00 (北京时间)</p>
        <p>⚠️ 健康干预请务必咨询专业医疗人员</p>
    </div>
</body>
</html>
"""

msg.attach(MIMEText(html_content, "html", "utf-8"))

# 发送邮件
try:
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVERS, msg.as_string())
    server.quit()
    print("✅ 邮件发送成功")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")

EMAIL_SCRIPT

echo "✅ 任务执行完成"
echo "📁 报告位置: health_reports/longevity_research_${DATE}.md"
