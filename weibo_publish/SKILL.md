---
name: weibo_publish
description: 使用 Playwright 自动化登录微博并发布内容（支持文字、图片），适用于定时发布、批量发布等场景。支持扫码登录和账号密码登录。
metadata:
  {
    "copaw":
      {
        "emoji": "📱",
        "requires": {
          "python_packages": ["playwright"],
          "system_commands": ["playwright install chromium"]
        }
      }
  }
---

# 微博发布自动化技能

使用 Playwright 实现微博自动登录和内容发布，支持文字和图片发布。

## 功能特性

- ✅ 自动登录微博（扫码登录/账号密码登录）
- ⭐ **持久化登录** - **新功能！** 使用 Chrome 用户数据目录，登录一次永久有效（类似 Chrome CDP）
- ✅ 发布纯文字微博
- ✅ 发布带图片的微博（支持单张或多张）
- ✅ 批量连续发布 - 浏览器保持打开，连续发布多条微博
- ✅ 反检测配置，避免被识别为自动化工具
- ✅ 完善的错误处理和日志记录
- ✅ 自动截图保存错误现场

## 使用前准备

### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

### 2. 准备微博账号

- 确保有可用的微博账号
- 建议使用扫码登录（更稳定，不易触发风控）

## 使用方式

### 基础用法

使用 `scripts/weibo_publish.py` 脚本发布微博：

```python
from scripts.weibo_publish import weibo_publish_skill

# 发布纯文字微博
weibo_publish_skill(
    content="这是一条测试微博 #Python自动化#",
    headless=False  # 可视化运行，方便调试
)

# 发布带图片的微博
weibo_publish_skill(
    content="分享一张图片 #摄影#",
    image_paths=["photo1.jpg", "photo2.jpg"],
    headless=False
)
```

### 参数说明

- `content` (str, 必填): 微博内容，限制 2000 字以内
- `image_paths` (list, 可选): 图片路径列表，支持最多 9 张图片
- `headless` (bool, 可选): 是否无头模式运行，默认 False（可视化）
- `login_timeout` (int, 可选): 登录超时时间（秒），默认 60 秒
- `save_cookies` (bool, 可选): 是否保存登录状态，默认 True
- `keep_browser_open` (bool, 可选): 是否保持浏览器打开，默认 False（自动关闭）
- `wait_after_publish` (int, 可选): 发布后等待时间（秒），默认 5 秒

### 高级用法

#### 1. 保持浏览器打开（推荐用于调试）

发布后不自动关闭浏览器，方便查看发布结果：

```python
weibo_publish_skill(
    content="测试微博，查看发布效果",
    keep_browser_open=True  # 浏览器保持打开，按 Ctrl+C 退出
)
```

#### 2. 自定义等待时间

发布后等待指定时间再关闭浏览器：

```python
weibo_publish_skill(
    content="测试微博",
    wait_after_publish=10  # 等待 10 秒后关闭
)
```

#### 3. 使用保存的登录状态

首次登录成功后，会自动保存 cookies，下次运行时可跳过登录：

```python
weibo_publish_skill(
    content="使用已保存的登录状态发布",
    save_cookies=True  # 使用保存的 cookies
)
```

#### 2. 定时发布

结合 CoPaw 的 cron 功能实现定时发布：

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
```

#### 3. 批量发布

```python
posts = [
    {"content": "第一条微博", "image_paths": ["img1.jpg"]},
    {"content": "第二条微博", "image_paths": ["img2.jpg"]},
    {"content": "第三条微博", "image_paths": None}
]

for post in posts:
    weibo_publish_skill(**post)
    time.sleep(300)  # 间隔 5 分钟，避免频繁发布被限制
```

## 注意事项

### ⚠️ 重要提醒

1. **频率控制**: 不要频繁发布，建议每次发布间隔至少 5 分钟，避免账号被风控
2. **内容合规**: 确保发布内容符合微博社区规范
3. **图片格式**: 支持 jpg、png、gif 等常见格式，单张图片不超过 5MB
4. **登录方式**: 优先使用扫码登录，账号密码登录可能触发验证码
5. **网络环境**: 确保网络稳定，能正常访问微博

### 🔧 故障排查

如果发布失败，检查以下几点：

1. **查看错误截图**: 脚本会自动保存错误截图到当前目录
2. **检查元素定位**: 微博 UI 可能更新，需要调整元素定位器
3. **清除 cookies**: 删除 `weibo_cookies.json` 重新登录
4. **使用可视化模式**: 设置 `headless=False` 观察执行过程

## 技术实现

### 反检测机制

- 移除 `navigator.webdriver` 标识
- 自定义 User-Agent
- 放慢操作速度，模拟真人行为
- 随机延迟，避免机械化操作

### 元素定位策略

采用多种定位策略组合，提高稳定性：

- XPath 模糊匹配，适配 UI 变化
- 等待元素可见后再操作
- 超时控制，防止卡死

## 相关文档

- `references/api_reference.md` - 详细 API 文档
- `references/troubleshooting.md` - 故障排查指南
- `scripts/weibo_publish.py` - 核心实现脚本
- `scripts/weibo_login.py` - 登录模块
- `scripts/weibo_utils.py` - 工具函数

## 示例场景

1. **个人博主**: 定时发布内容，保持账号活跃度
2. **营销推广**: 批量发布产品信息
3. **新闻媒体**: 自动同步新闻到微博
4. **数据采集**: 发布后获取互动数据

## 许可证

本技能基于 Apache 2.0 许可证开源。

