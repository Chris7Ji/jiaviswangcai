import requests
import json

# 飞书配置
FEISHU_APP_ID = "cli_a6f596118438dcef"
FEISHU_APP_SECRET = "your_app_secret"  # 需要从环境变量或配置文件读取
RECEIVER_OPEN_ID = "ou_b6c7778820b20031cd97bdc45d1cd9fa"

# 读取HTML内容
with open('/Users/jiyingguo/.openclaw/workspace/dengta_project_daily_v4_20260318.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 提取文本内容（简化版）
text_content = """
🎯 高校分队-灯塔学校的每日动态（03月18日）

🏛️ 深圳河套学院（3条）
1. 广东省AI OPC行动方案发布，河套学院纳入核心布局
2. 全球青年AI论坛：港中大(深圳)×河套学院联合举办
3. AI创新创业工作坊启动：零风险实战孵化

🎓 中国科学技术大学（5条）
1. 光钟刷新人类计时极限：300亿年不差1秒
2. 合肥先进光源国家重大科技基础设施启动
3. 中国科大与华为签署战略合作协议
4. 中国科大AI学院获批国家级一流本科专业
5. 中国科大教授当选中国科学院院士

🔬 上海交通大学（5条）
🔥 井贤栋向上海交大捐赠1.3亿元支持AI教育
2. 上海交大荣获7项2025年"中国产学研合作促进会科技创新奖"
3. 上海交大党委常委会传达学习全国两会精神
4. 上海交大与商汤科技共建联合实验室
5. 上海交大AI研究院发布新一代大模型

📡 北京邮电大学（5条）
1. 张平院士团队MWC 2026亮相：6G技术引领全球
2. 北邮与联通共建5G-A联合创新中心
3. 北邮获批建设国家卓越工程师学院
4. 北邮学子获国际大学生程序设计竞赛金奖
5. 北邮举办2026年信息通信技术国际会议

🐉 中央民族大学（0条）
📭 今日监测：该板块暂无重大异动

---
此消息由OpenClaw自动发送
发送时间：每天06:45 | 数据来源：高校官网+官方微信公众号
"""

# 获取tenant_access_token
def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("tenant_access_token")
    return None

# 发送飞书消息
def send_feishu_message():
    token = get_tenant_access_token()
    if not token:
        print("❌ 获取飞书token失败")
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 构建消息内容
    message_content = {
        "text": text_content
    }
    
    params = {"receive_id_type": "open_id"}
    data = {
        "receive_id": RECEIVER_OPEN_ID,
        "msg_type": "text",
        "content": json.dumps(message_content)
    }
    
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        print("✅ 飞书消息发送成功！")
        return True
    else:
        print(f"❌ 发送失败: {response.text}")
        return False

if __name__ == "__main__":
    send_feishu_message()