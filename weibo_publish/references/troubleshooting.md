# 故障排查指南

## 常见问题

### 1. 登录失败

#### 问题：扫码后仍然超时

**可能原因:**
- 网络不稳定
- 扫码后未确认
- 微博服务器响应慢

**解决方案:**

```python
# 增加登录超时时间
weibo_publish_skill(
    content="测试",
    login_timeout=120  # 增加到 2 分钟
)
```

#### 问题：提示"登录环境异常"

**可能原因:**
- 被识别为自动化工具
- IP 地址异常
- 账号存在风险

**解决方案:**

1. 使用可视化模式，手动完成验证
2. 更换网络环境
3. 清除 cookies 重新登录

```bash
rm weibo_cookies.json
```

### 2. 发布失败

#### 问题：找不到"写微博"按钮

**可能原因:**
- 微博 UI 更新
- 页面未完全加载
- 元素定位器失效

**解决方案:**

1. 使用可视化模式查看页面状态

```python
weibo_publish_skill(
    content="测试",
    headless=False  # 可视化运行
)
```

2. 检查错误截图，找到正确的元素定位器

3. 修改 `weibo_publish.py` 中的定位器：

```python
publish_btn_selectors = [
    'text=/写微博|发微博/',
    '[aria-label*="写微博"]',
    # 添加新的定位器
    'button.new-publish-btn',
]
```

#### 问题：内容输入失败

**可能原因:**
- 输入框定位失败
- 内容包含特殊字符
- 页面加载未完成

**解决方案:**

1. 增加等待时间

```python
# 在 publish() 方法中增加延迟
time.sleep(2)  # 等待页面加载
```

2. 检查内容是否包含特殊字符

```python
# 清理特殊字符
content = content.replace('\x00', '')
```

#### 问题：图片上传失败

**可能原因:**
- 图片格式不支持
- 图片文件过大
- 上传按钮定位失败

**解决方案:**

1. 检查图片格式和大小

```python
from PIL import Image

# 检查图片
img = Image.open("photo.jpg")
print(f"格式: {img.format}, 大小: {img.size}")

# 压缩图片
if img.size[0] > 2000:
    img.thumbnail((2000, 2000))
    img.save("photo_compressed.jpg", quality=85)
```

2. 跳过图片上传，只发布文字

```python
weibo_publish_skill(
    content="纯文字微博",
    image_paths=None  # 不上传图片
)
```

### 3. 账号安全问题

#### 问题：账号被限制发布

**可能原因:**
- 发布频率过高
- 内容违规
- 账号异常

**解决方案:**

1. 控制发布频率

```python
import time

posts = [...]
for post in posts:
    weibo_publish_skill(**post)
    time.sleep(600)  # 间隔 10 分钟
```

2. 检查内容是否合规

3. 联系微博客服解除限制

#### 问题：需要验证码

**可能原因:**
- 登录环境异常
- 账号存在风险

**解决方案:**

使用可视化模式，手动完成验证码：

```python
weibo_publish_skill(
    content="测试",
    headless=False,  # 可视化模式
    login_timeout=300  # 给足够时间完成验证
)
```

### 4. 性能问题

#### 问题：运行速度慢

**可能原因:**
- 网络延迟
- 页面加载慢
- 等待时间过长

**解决方案:**

1. 使用无头模式（更快）

```python
weibo_publish_skill(
    content="测试",
    headless=True  # 无头模式
)
```

2. 减少不必要的等待时间

```python
# 修改 weibo_publish.py 中的延迟
time.sleep(0.5)  # 从 1 秒减少到 0.5 秒
```

#### 问题：内存占用高

**可能原因:**
- 浏览器未正确关闭
- 多次运行累积

**解决方案:**

1. 确保浏览器正确关闭

```python
try:
    weibo_publish_skill(...)
finally:
    # 确保清理资源
    pass
```

2. 定期重启脚本

### 5. 环境问题

#### 问题：Playwright 未安装

**错误信息:**
```
ModuleNotFoundError: No module named 'playwright'
```

**解决方案:**

```bash
pip install playwright
playwright install chromium
```

#### 问题：Chromium 下载失败

**错误信息:**
```
Failed to download Chromium
```

**解决方案:**

1. 使用国内镜像

```bash
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

2. 手动下载并指定路径

```bash
playwright install chromium --with-deps
```

#### 问题：无图形环境（服务器）

**错误信息:**
```
Error: Failed to launch browser
```

**解决方案:**

1. 安装虚拟显示

```bash
# Ubuntu/Debian
sudo apt-get install xvfb

# 使用 xvfb 运行
xvfb-run python weibo_publish.py
```

2. 使用无头模式

```python
weibo_publish_skill(
    content="测试",
    headless=True
)
```

## 调试技巧

### 1. 启用详细日志

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,  # 改为 DEBUG 级别
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 2. 查看错误截图

脚本会自动保存错误截图：

```bash
ls -lt weibo_*.png | head -5
```

### 3. 使用浏览器开发者工具

在可视化模式下，可以手动打开开发者工具：

```python
# 在 _init_browser 方法中添加
self.context = self.browser.new_context(
    viewport=None,
    user_agent=self._get_user_agent(),
    devtools=True  # 自动打开开发者工具
)
```

### 4. 暂停执行

在关键步骤添加断点：

```python
# 在需要检查的地方添加
import pdb; pdb.set_trace()
```

或使用 input() 暂停：

```python
input("按回车继续...")
```

## 获取帮助

如果以上方法都无法解决问题：

1. 查看完整错误日志
2. 检查错误截图
3. 提供以下信息：
   - Python 版本
   - Playwright 版本
   - 操作系统
   - 错误信息
   - 错误截图

```bash
# 查看版本信息
python --version
pip show playwright
```

