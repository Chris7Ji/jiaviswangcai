#!/usr/bin/env python3
"""
飞书日历管理技能 - 超级助理包
支持查询、创建、修改日历事件
"""

import requests
import json
from datetime import datetime, timedelta
import os

# 飞书配置 - 从环境变量读取
FEISHU_CONFIG = {
    "app_id": os.environ.get("FEISHU_APP_ID"),
    "app_secret": os.environ.get("FEISHU_APP_SECRET"),
    "base_url": "https://open.feishu.cn/open-apis"
}

class FeishuCalendarManager:
    """飞书日历管理器"""
    
    def __init__(self):
        self.app_id = FEISHU_CONFIG["app_id"]
        self.app_secret = FEISHU_CONFIG["app_secret"]
        self.base_url = FEISHU_CONFIG["base_url"]
        self.access_token = None
        
    def get_access_token(self):
        """获取访问令牌"""
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                return True
            else:
                print(f"获取token失败: {result}")
                return False
        except Exception as e:
            print(f"请求失败: {e}")
            return False
    
    def get_headers(self):
        """获取请求头"""
        if not self.access_token:
            if not self.get_access_token():
                return None
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def get_calendars(self):
        """获取日历列表"""
        headers = self.get_headers()
        if not headers:
            return None
        
        url = f"{self.base_url}/calendar/v4/calendars"
        
        try:
            response = requests.get(url, headers=headers)
            result = response.json()
            if result.get("code") == 0:
                calendars = result.get("data", {}).get("calendar_list", [])
                return calendars
            else:
                print(f"获取日历列表失败: {result}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None
    
    def get_primary_calendar(self):
        """获取主日历"""
        calendars = self.get_calendars()
        if calendars:
            # 返回第一个日历作为主日历
            return calendars[0]
        return None
    
    def list_events(self, start_time=None, end_time=None, max_results=10):
        """列出日历事件"""
        headers = self.get_headers()
        if not headers:
            return []
        
        # 获取主日历ID
        calendar = self.get_primary_calendar()
        if not calendar:
            print("无法获取日历")
            return []
        
        calendar_id = calendar.get("calendar_id", "primary")
        
        # 默认查询今天到明天的事件（使用Unix时间戳，毫秒）
        if not start_time:
            start_time = str(int(datetime.now().timestamp() * 1000))
        if not end_time:
            end_time = str(int((datetime.now() + timedelta(days=7)).timestamp() * 1000))
        
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        params = {
            "start_time": start_time,
            "end_time": end_time,
            "page_size": max(max_results, 50)
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            result = response.json()
            if result.get("code") == 0:
                return result.get("data", {}).get("items", [])
            else:
                print(f"获取事件失败: {result}")
                return []
        except Exception as e:
            print(f"请求失败: {e}")
            return []
    
    def create_event(self, summary, start_time, end_time, description="", location=""):
        """创建日历事件"""
        headers = self.get_headers()
        if not headers:
            return False
        
        # 获取主日历ID
        calendar = self.get_primary_calendar()
        if not calendar:
            print("无法获取日历")
            return False
        
        calendar_id = calendar.get("calendar_id", "primary")
        
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        
        # 转换时间为Unix时间戳（毫秒）
        try:
            start_ts = int(datetime.fromisoformat(start_time.replace('Z', '+00:00')).timestamp() * 1000)
            end_ts = int(datetime.fromisoformat(end_time.replace('Z', '+00:00')).timestamp() * 1000)
        except:
            # 如果已经是时间戳格式
            start_ts = int(start_time) if start_time.isdigit() else int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
            end_ts = int(end_time) if end_time.isdigit() else int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
        
        # 飞书日历API使用ISO 8601格式的时间字符串
        data = {
            "summary": summary,
            "description": description,
            "start": {
                "date_time": start_time,
                "timezone": "Asia/Shanghai"
            },
            "end": {
                "date_time": end_time,
                "timezone": "Asia/Shanghai"
            }
        }
        
        if location:
            data["location"] = {"name": location}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            if result.get("code") == 0:
                print(f"✅ 事件创建成功: {summary}")
                return True
            else:
                print(f"创建事件失败: {result}")
                return False
        except Exception as e:
            print(f"请求失败: {e}")
            return False
    
    def delete_event(self, event_id):
        """删除日历事件"""
        headers = self.get_headers()
        if not headers:
            return False
        
        # 获取主日历ID
        calendar = self.get_primary_calendar()
        if not calendar:
            print("无法获取日历")
            return False
        
        calendar_id = calendar.get("calendar_id", "primary")
        
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}"
        
        try:
            response = requests.delete(url, headers=headers)
            result = response.json()
            if result.get("code") == 0:
                print(f"✅ 事件删除成功")
                return True
            else:
                print(f"删除事件失败: {result}")
                return False
        except Exception as e:
            print(f"请求失败: {e}")
            return False
    
    def format_events(self, events):
        """格式化事件列表"""
        if not events:
            return "暂无日程"
        
        output = []
        for i, event in enumerate(events, 1):
            summary = event.get("summary", "无标题")
            start = event.get("start", {}).get("date_time", "")
            end = event.get("end", {}).get("date_time", "")
            description = event.get("description", "")
            location = event.get("location", {}).get("name", "")
            
            # 格式化时间
            try:
                start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                time_str = start_dt.strftime("%m月%d日 %H:%M")
            except:
                time_str = start
            
            output.append(f"{i}. {summary}")
            output.append(f"   时间: {time_str}")
            if location:
                output.append(f"   地点: {location}")
            if description:
                output.append(f"   备注: {description[:50]}...")
            output.append("")
        
        return "\n".join(output)

def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 feishu_calendar.py <命令> [参数]")
        print("命令:")
        print("  list [n]           - 列出最近n个事件（默认10个）")
        print("  today              - 列出今天的事件")
        print("  create <标题> <开始时间> <结束时间> [描述] - 创建事件")
        print("  delete <事件ID>    - 删除事件")
        print("\n时间格式: 2026-03-07T15:00:00")
        sys.exit(1)
    
    command = sys.argv[1]
    manager = FeishuCalendarManager()
    
    if command == "list":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        events = manager.list_events(max_results=limit)
        print(f"\n最近 {len(events)} 个日程:\n")
        print(manager.format_events(events))
    
    elif command == "today":
        today_start = str(int(datetime.now().replace(hour=0, minute=0, second=0).timestamp() * 1000))
        today_end = str(int(datetime.now().replace(hour=23, minute=59, second=59).timestamp() * 1000))
        events = manager.list_events(start_time=today_start, end_time=today_end)
        print(f"\n今天 ({datetime.now().strftime('%Y-%m-%d')}) 的日程:\n")
        print(manager.format_events(events))
    
    elif command == "create":
        if len(sys.argv) < 5:
            print("用法: python3 feishu_calendar.py create <标题> <开始时间> <结束时间> [描述]")
            sys.exit(1)
        
        summary = sys.argv[2]
        start_time = sys.argv[3]
        end_time = sys.argv[4]
        description = sys.argv[5] if len(sys.argv) > 5 else ""
        
        manager.create_event(summary, start_time, end_time, description)
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法: python3 feishu_calendar.py delete <事件ID>")
            sys.exit(1)
        
        event_id = sys.argv[2]
        manager.delete_event(event_id)
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main()
