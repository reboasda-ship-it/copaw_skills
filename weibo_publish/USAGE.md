# 微博发布技能使用指南

## 📋 目录

- [快速开始](#快速开始)
- [功能特性](#功能特性)
- [使用场景](#使用场景)
- [完整示例](#完整示例)
- [集成到 CoPaw](#集成到-copaw)
- [注意事项](#注意事项)

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 基础使用

```python
from scripts.weibo_publish import weibo_publish_skill

# 发布纯文字微博
weibo_publish_skill(
    content="这是一条测试微博 #Python自动化#"
)
```

### 3. 首次登录

- 脚本会自动打开浏览器
- 使用手机微博 APP 扫码登录
- 登录成功后会自动保存状态
- 下次运行无需重新登录

## ✨ 功能特性

| 功能 | 说明 | 状态 |
|------|------|------|
| 文字发布 | 支持最多 2000 字 | ✅ |
| 图片发布 | 支持最多 9 张图片 | ✅ |
| 扫码登录 | 安全稳定的登录方式 | ✅ |
| 登录保持 | 自动保存 cookies | ✅ |
| 反检测 | 避免被识别为机器人 | ✅ |
| 错误处理 | 自动截图保存错误现场 | ✅ |
| 批量发布 | 支持批量发布多条 | ✅ |
| 定时发布 | 配合 CoPaw cron | ✅ |
| 无头模式 | 后台运行不显示窗口 | ✅ |

## 🎯 使用场景

### 场景 1: 个人博主定时发布

```python
# 每天早上 9:00 自动发布早安微博
weibo_publish_skill(
    content="早安！新的一天开始了 ☀️ #早安#",
    headless=True  # 后台运行
)
```

### 场景 2: 营销推广批量发布

```python
import time

products = [
    {"name": "产品A", "image": "product_a.jpg"},
    {"name": "产品B", "image": "product_b.jpg"},
]

for product in products:
    weibo_publish_skill(
        content=f"新品推荐：{product['name']} #新品上市#",
        image_paths=[product['image']]
    )
    time.sleep(600)  # 间隔 10 分钟
```

### 场景 3: 新闻媒体自动同步

```python
# 从 RSS 获取新闻并发布到微博
import feedparser

feed = feedparser.parse('https://news.example.com/rss')

for entry in feed.entries[:5]:  # 发布最新 5 条
    weibo_publish_skill(
        content=f"{entry.title}\n{entry.link} #新闻#"
    )
    time.sleep(300)  # 间隔 5 分钟
```

### 场景 4: 摄影师作品分享

```python
import os
from pathlib import Path

# 自动发布文件夹中的照片
photo_dir = Path("photos")
photos = list(photo_dir.glob("*.jpg"))

for i in range(0, len(photos), 9):  # 每次最多 9 张
    batch = photos[i:i+9]
    weibo_publish_skill(
        content="今日摄影作品分享 📷 #摄影# #风景#",
        image_paths=[str(p) for p in batch]
    )
    time.sleep(600)  # 间隔 10 分钟
```

## 📝 完整示例

### 示例 1: 带图片发布

```python
weibo_publish_skill(
    content="分享今天的美食 🍜 #美食# #生活#",
    image_paths=["food1.jpg", "food2.jpg", "food3.jpg"],
    headless=False,  # 可视化运行
    login_timeout=60,  # 登录超时 60 秒
    save_cookies=True,  # 保存登录状态
    keep_browser_open=False,  # 发布后自动关闭浏览器
    wait_after_publish=5  # 发布后等待 5 秒再关闭
)
```

### 示例 1.1: 保持浏览器打开

```python
# 发布后不自动关闭浏览器，方便查看结果
weibo_publish_skill(
    content="测试微博，查看发布效果",
    headless=False,
    keep_browser_open=True  # 浏览器保持打开，按 Ctrl+C 退出
)
```

### 示例 1.2: 批量连续发布（推荐）

```python
from weibo_publish import weibo_batch_publish

# 准备多条微博
posts = [
    {"content": "第一条微博 #Python#", "image_paths": None},
    {"content": "第二条微博 #自动化#", "image_paths": ["photo1.jpg"]},
    {"content": "第三条微博", "image_paths": ["photo2.jpg", "photo3.jpg"]},
]

# 批量发布（浏览器只打开一次，连续发布）
result = weibo_batch_publish(
    posts=posts,
    headless=False,
    interval=300  # 每条微博间隔 5 分钟（300 秒）
)

print(f"发布完成：成功 {result['success']} 条，失败 {result['failed']} 条")
```

### 示例 2: 批量发布

```python
import time
from datetime import datetime

posts = [
    {
        "content": "早安！新的一天开始了 ☀️ #早安#",
        "image_paths": None
    },
    {
        "content": "午餐时间到了 🍱 #午餐#",
        "image_paths": ["lunch.jpg"]
    },
    {
        "content": "晚安，好梦 🌙 #晚安#",
        "image_paths": None
    }
]

for i, post in enumerate(posts, 1):
    print(f"[{datetime.now()}] 正在发布第 {i}/{len(posts)} 条...")
    
    try:
        weibo_publish_skill(**post)
        print(f"✅ 第 {i} 条发布成功")
    except Exception as e:
        print(f"❌ 第 {i} 条发布失败: {e}")
    
    if i < len(posts):
        print("等待 5 分钟...")
        time.sleep(300)
```

### 示例 3: 错误处理

```python
def safe_publish(content, **kwargs):
    """安全发布，带重试机制"""
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            weibo_publish_skill(content=content, **kwargs)
            print("✅ 发布成功")
            return True
        except Exception as e:
            print(f"❌ 第 {attempt + 1} 次尝试失败: {e}")
            if attempt < max_retries - 1:
                print("等待 30 秒后重试...")
                time.sleep(30)
    
    print("❌ 发布失败，已达到最大重试次数")
    return False

# 使用
safe_publish(
    content="测试微博",
    image_paths=["photo.jpg"]
)
```

## 🔗 集成到 CoPaw

### 方式 1: 通过 Agent 调用

在 CoPaw 对话中直接使用：

```
用户: 帮我发一条微博，内容是"今天天气真好 #天气#"

Agent: 好的，我来帮你发布微博...
[调用 weibo_publish 技能]
✅ 微博发布成功！
```

### 方式 2: 定时任务

创建定时发布任务：

```bash
# 每天早上 9:00 发布早安微博
copaw cron create \
  --type agent \
  --name "每日早安微博" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user "system" \
  --target-session "default" \
  --text "使用 weibo_publish 技能发布：早安，新的一天开始了！#早安#"

# 每周一 10:00 发布周报
copaw cron create \
  --type agent \
  --name "每周周报" \
  --cron "0 10 * * 1" \
  --channel console \
  --target-user "system" \
  --target-session "default" \
  --text "使用 weibo_publish 技能发布本周工作总结"
```

### 方式 3: 命令行直接调用

```bash
# 发布纯文字
python scripts/weibo_publish.py "测试微博内容"

# 发布带图片
python scripts/weibo_publish.py "测试微博" -i photo1.jpg photo2.jpg

# 无头模式
python scripts/weibo_publish.py "测试微博" --headless

# 自定义超时
python scripts/weibo_publish.py "测试微博" --timeout 120

# 保持浏览器打开（不自动关闭）
python scripts/weibo_publish.py "测试微博" --keep-open

# 自定义等待时间（发布后等待 10 秒再关闭）
python scripts/weibo_publish.py "测试微博" --wait 10

# 组合使用
python scripts/weibo_publish.py "测试微博" -i photo.jpg --keep-open
```

## ⚠️ 注意事项

### 频率控制

- ✅ 每次发布间隔至少 **5 分钟**
- ✅ 每天发布不超过 **20 条**
- ❌ 避免每分钟发布多条
- ❌ 避免深夜频繁发布

### 内容规范

- ✅ 确保内容符合微博社区规范
- ✅ 避免发布违规内容
- ✅ 不要完全重复相同内容
- ❌ 避免敏感词汇

### 账号安全

- ✅ 保护 `weibo_cookies.json` 文件
- ✅ 不要在公共环境使用
- ✅ 定期更换密码
- ❌ 不要分享登录状态文件

### 图片要求

- ✅ 支持 JPG、PNG、GIF 格式
- ✅ 单张图片不超过 **5MB**
- ✅ 最多上传 **9 张**图片
- ❌ 不支持视频上传

## 📚 相关文档

- [SKILL.md](SKILL.md) - 技能说明
- [README.md](README.md) - 项目说明
- [快速入门](references/quickstart.md) - 5 分钟上手
- [API 参考](references/api_reference.md) - 详细 API 文档
- [故障排查](references/troubleshooting.md) - 问题解决

## 🆘 获取帮助

遇到问题？

1. 查看 [故障排查指南](references/troubleshooting.md)
2. 检查错误截图（`weibo_*.png`）
3. 运行测试脚本：`python scripts/test_weibo.py`
4. 提交 Issue

## 📄 许可证

Apache 2.0 License

