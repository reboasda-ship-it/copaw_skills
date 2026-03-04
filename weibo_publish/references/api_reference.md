# 微博发布 API 参考文档

## 核心函数

### weibo_publish_skill()

主函数，用于发布微博。

**函数签名:**

```python
def weibo_publish_skill(
    content: str,
    image_paths: Optional[List[str]] = None,
    headless: bool = False,
    login_timeout: int = 60,
    save_cookies: bool = True,
    keep_browser_open: bool = False,
    wait_after_publish: int = 5,
) -> bool
```

**参数说明:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `content` | str | 是 | - | 微博内容，限制 2000 字以内 |
| `image_paths` | List[str] | 否 | None | 图片路径列表，最多 9 张 |
| `headless` | bool | 否 | False | 是否无头模式运行 |
| `login_timeout` | int | 否 | 60 | 登录超时时间（秒） |
| `save_cookies` | bool | 否 | True | 是否保存登录状态 |
| `keep_browser_open` | bool | 否 | False | 是否保持浏览器打开（不自动关闭） |
| `wait_after_publish` | int | 否 | 5 | 发布后等待时间（秒），方便查看结果 |

**返回值:**

- `bool`: 发布成功返回 True

**异常:**

- `ValueError`: 参数校验失败（内容过长、图片过多等）
- `FileNotFoundError`: 图片文件不存在
- `RuntimeError`: 发布过程出错（登录失败、元素定位失败等）

**示例:**

```python
# 发布纯文字微博
weibo_publish_skill(
    content="这是一条测试微博 #Python#"
)

# 发布带图片的微博
weibo_publish_skill(
    content="分享美图 #摄影#",
    image_paths=["photo1.jpg", "photo2.jpg"]
)

# 无头模式运行
weibo_publish_skill(
    content="后台发布",
    headless=True
)

# 保持浏览器打开，方便查看结果
weibo_publish_skill(
    content="测试微博",
    keep_browser_open=True  # 不自动关闭，按 Ctrl+C 退出
)

# 自定义等待时间
weibo_publish_skill(
    content="测试微博",
    wait_after_publish=10  # 发布后等待 10 秒再关闭
)
```

## WeiboPublisher 类

高级用户可以直接使用 `WeiboPublisher` 类进行更精细的控制。

### 初始化

```python
publisher = WeiboPublisher(headless=False, save_cookies=True)
```

### 方法

#### login(timeout: int = 60)

登录微博。

**参数:**
- `timeout`: 登录超时时间（秒）

**示例:**

```python
publisher.login(timeout=120)  # 等待 2 分钟
```

#### publish(content: str, image_paths: Optional[List[str]] = None)

发布微博。

**参数:**
- `content`: 微博内容
- `image_paths`: 图片路径列表

**示例:**

```python
publisher.publish(
    content="测试内容",
    image_paths=["img1.jpg"]
)
```

#### close()

关闭浏览器。

**示例:**

```python
publisher.close()
```

### 完整示例

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    publisher = WeiboPublisher(headless=False)
    publisher._init_browser(p)
    
    # 登录
    publisher.login(timeout=60)
    
    # 发布多条微博
    posts = [
        {"content": "第一条", "image_paths": ["1.jpg"]},
        {"content": "第二条", "image_paths": None},
    ]
    
    for post in posts:
        publisher.publish(**post)
        time.sleep(300)  # 间隔 5 分钟
    
    publisher.close()
```

## 配置文件

### cookies 文件

登录状态保存在 `weibo_cookies.json` 文件中。

**位置:** 脚本运行目录

**格式:** JSON 数组

**示例:**

```json
[
  {
    "name": "SUB",
    "value": "...",
    "domain": ".weibo.com",
    "path": "/",
    "expires": 1234567890,
    "httpOnly": true,
    "secure": true,
    "sameSite": "Lax"
  }
]
```

**清除登录状态:**

```bash
rm weibo_cookies.json
```

## 元素定位器

脚本使用多种定位策略以提高稳定性。如果微博 UI 更新导致定位失败，可以修改以下定位器：

### 写微博按钮

```python
publish_btn_selectors = [
    'text=/写微博|发微博/',
    '[aria-label*="写微博"]',
    '[aria-label*="发微博"]',
    'a[href*="publish"]',
]
```

### 内容输入框

```python
content_box_selectors = [
    'div[contenteditable="true"][role="textbox"]',
    'textarea[placeholder*="微博"]',
    'div.Form_input_2gtXx',
]
```

### 图片上传

```python
upload_selectors = [
    'input[type="file"][accept*="image"]',
    'input[type="file"]',
]
```

### 发布按钮

```python
submit_selectors = [
    'button:has-text("发布")',
    'button[type="submit"]',
    'button.Form_btn_2gtXx',
]
```

## 反检测配置

### 浏览器参数

```python
browser_args = [
    "--disable-blink-features=AutomationControlled",
    "--start-maximized",
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-web-security",
]
```

### JavaScript 注入

```javascript
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
});
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
});
```

### User-Agent

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36
```

## 常量配置

```python
WEIBO_LOGIN_URL = "https://weibo.com/login.php"
WEIBO_HOME_URL = "https://weibo.com/"
COOKIES_FILE = "weibo_cookies.json"
MAX_CONTENT_LENGTH = 2000  # 微博最大字数
MAX_IMAGES = 9  # 最多图片数量
```

