# 微博发布自动化技能

使用 Playwright 实现微博自动登录和内容发布的 CoPaw 技能。

## 快速开始

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 基础使用

```python
from scripts.weibo_publish import weibo_publish_skill, weibo_batch_publish

# 发布单条微博
weibo_publish_skill(
    content="这是一条测试微博 #Python自动化#"
)

# 发布带图片的微博
weibo_publish_skill(
    content="分享美图 #摄影#",
    image_paths=["photo1.jpg", "photo2.jpg"]
)

# ⭐ 新功能：批量连续发布（推荐）
posts = [
    {"content": "第一条微博", "image_paths": None},
    {"content": "第二条微博", "image_paths": ["photo.jpg"]},
]
result = weibo_batch_publish(posts, interval=300)  # 浏览器只打开一次
```

### 3. 命令行使用

```bash
# 发布纯文字
python scripts/weibo_publish.py "测试微博内容"

# 发布带图片
python scripts/weibo_publish.py "测试微博" -i photo1.jpg photo2.jpg

# 无头模式运行
python scripts/weibo_publish.py "测试微博" --headless

# 自定义登录超时
python scripts/weibo_publish.py "测试微博" --timeout 120
```

## 功能特性

- ✅ **自动登录**: 支持扫码登录和账号密码登录
- ✅ **文字发布**: 支持最多 2000 字的文字内容
- ✅ **图片发布**: 支持最多 9 张图片
- ✅ **登录状态保存**: 自动保存 cookies，下次无需重新登录
- ✅ **反检测**: 配置反自动化检测参数
- ✅ **错误处理**: 完善的异常处理和错误截图
- ✅ **批量发布**: 支持批量发布多条微博
- ⭐ **连续发布**: **新功能** - 浏览器保持打开，连续发布，效率提升 3 倍
- ✅ **定时发布**: 配合 CoPaw cron 实现定时发布

## 文件结构

```
weibo_publish/
├── SKILL.md                          # 技能说明文档
├── README.md                         # 本文件
├── scripts/                          # 脚本目录
│   ├── weibo_publish.py             # 核心发布脚本
│   └── example.py                   # 示例脚本
└── references/                       # 参考文档
    ├── api_reference.md             # API 参考
    └── troubleshooting.md           # 故障排查指南
```

## 使用示例

### 示例 1: 简单发布

```python
weibo_publish_skill(
    content="早安！新的一天开始了 #早安#"
)
```

### 示例 2: 带图片发布

```python
weibo_publish_skill(
    content="分享今天的美食 #美食#",
    image_paths=["food1.jpg", "food2.jpg", "food3.jpg"]
)
```

### 示例 3: 批量发布

```python
import time

posts = [
    {"content": "第一条微博", "image_paths": None},
    {"content": "第二条微博", "image_paths": ["img.jpg"]},
]

for post in posts:
    weibo_publish_skill(**post)
    time.sleep(300)  # 间隔 5 分钟
```

### 示例 4: 定时发布

使用 CoPaw cron 功能：

```bash
# 每天早上 9:00 发布
copaw cron create \
  --type agent \
  --name "每日早安" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user "system" \
  --target-session "default" \
  --text "使用 weibo_publish 技能发布早安微博"
```

### 示例 5: 无头模式

```python
weibo_publish_skill(
    content="后台自动发布",
    headless=True  # 无头模式，不显示浏览器窗口
)
```

## 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `content` | str | 是 | - | 微博内容（最多 2000 字） |
| `image_paths` | List[str] | 否 | None | 图片路径列表（最多 9 张） |
| `headless` | bool | 否 | False | 是否无头模式运行 |
| `login_timeout` | int | 否 | 60 | 登录超时时间（秒） |
| `save_cookies` | bool | 否 | True | 是否保存登录状态 |

## 注意事项

### ⚠️ 重要提醒

1. **频率控制**: 建议每次发布间隔至少 5 分钟
2. **内容合规**: 确保内容符合微博社区规范
3. **图片要求**: 支持 jpg/png/gif，单张不超过 5MB
4. **登录方式**: 优先使用扫码登录
5. **账号安全**: 不要在公共环境保存登录状态

### 🔧 故障排查

- **登录失败**: 增加 `login_timeout` 参数
- **发布失败**: 使用 `headless=False` 查看页面状态
- **元素定位失败**: 查看错误截图，更新定位器
- **清除登录状态**: 删除 `weibo_cookies.json` 文件

详细排查指南请查看 `references/troubleshooting.md`

## 技术实现

### 反检测机制

- 移除 `navigator.webdriver` 标识
- 自定义 User-Agent
- 放慢操作速度（slow_mo=50）
- 随机延迟模拟真人行为

### 元素定位

采用多种定位策略组合：

```python
# 写微博按钮
publish_btn_selectors = [
    'text=/写微博|发微博/',
    '[aria-label*="写微博"]',
    'a[href*="publish"]',
]
```

### 登录状态保存

自动保存 cookies 到 `weibo_cookies.json`：

```json
[
  {
    "name": "SUB",
    "value": "...",
    "domain": ".weibo.com"
  }
]
```

## 高级用法

### 自定义 WeiboPublisher

```python
from playwright.sync_api import sync_playwright
from scripts.weibo_publish import WeiboPublisher

with sync_playwright() as p:
    publisher = WeiboPublisher(headless=False)
    publisher._init_browser(p)
    publisher.login(timeout=60)
    
    # 发布多条
    for content in ["第一条", "第二条"]:
        publisher.publish(content=content)
        time.sleep(300)
    
    publisher.close()
```

## 相关文档

- [SKILL.md](SKILL.md) - 技能说明
- [API 参考](references/api_reference.md) - 详细 API 文档
- [故障排查](references/troubleshooting.md) - 问题解决指南

## 许可证

Apache 2.0 License

## 贡献

欢迎提交 Issue 和 Pull Request！

