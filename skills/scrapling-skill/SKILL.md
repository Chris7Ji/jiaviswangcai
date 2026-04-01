---
name: scrapling-skill
description: "基于Scrapling的网页抓取，支持动态渲染和Cloudflare绕过。触发词：抓取、爬取、绕过Cloudflare、动态页面、JS渲染页面"
author: based on scrapling.io
---

# Scrapling Skill 🕷️

自适应网页抓取框架，支持动态渲染和反爬绕过。

## 安装状态
- Python包: `scrapling[all]` ✅ 已安装
- Playwright浏览器: Chromium ✅ 已安装
- Python路径: `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`

## 三种模式

| 模式 | 用途 | 触发词 |
|------|------|--------|
| `Fetcher` (静态) | 快速静态页面 | 静态、抓取 |
| `StealthyFetcher` | 绕过反爬+Cloudflare | 绕过、反爬、stealth |
| `DynamicFetcher` | JavaScript动态渲染 | 动态、JS、渲染 |

## 使用示例

```python
# 动态页面抓取（微信文章、JS渲染页面）
from scrapling import DynamicFetcher
fetcher = DynamicFetcher()
page = fetcher.fetch('https://example.com')
print(page.get_all_text())

# 绕过Cloudflare
from scrapling import StealthyFetcher
fetcher = StealthyFetcher()
page = fetcher.fetch('https://cloudflare-protected.com')

# 静态抓取
from scrapling import Fetcher
page = Fetcher.get('https://example.com')
```

## 触发词
- "抓取 <url>"
- "爬取 <网站>"
- "绕过 Cloudflare"
- "动态页面"
- "JS渲染页面"
- "获取微信文章"

## 微信文章抓取示例

```python
from scrapling import DynamicFetcher
url = 'https://mp.weixin.qq.com/s/xxxxx'
fetcher = DynamicFetcher()
page = fetcher.fetch(url)
article = page.xpath('//div[@id="js_content"]')
text = article[0].get_all_text() if article else ''
```

## 注意事项
- DynamicFetcher 使用 Playwright 渲染JS，速度较慢
- WeChat文章必须用DynamicFetcher
- 内容为空时检查是否需要动态渲染

## 参考链接
- GitHub: https://github.com/N忧郁/Scrapling
- 文档: https://scrapling.io/
