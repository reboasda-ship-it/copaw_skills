# 快速入门指南

## 5 分钟上手微博发布

### 第 1 步：安装依赖

```bash
# 安装 Playwright
pip install playwright

# 下载 Chromium 浏览器
playwright install chromium
```

**国内用户加速下载：**

```bash
# 使用国内镜像
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

### 第 2 步：准备脚本

进入技能目录：

```bash
cd src/copaw/agents/skills/weibo_publish/scripts
```

### 第 3 步：发布第一条微博

**方式 1：使用 Python 脚本**

```python
from weibo_publish import weibo_publish_skill

# 发布纯文字微博
weibo_publish_skill(
    content="我的第一条自动发布的微博 #Python自动化#",
    headless=False  # 可视化运行，方便观察
)
```

**方式 2：使用命令行**

```bash
python weibo_publish.py "我的第一条自动发布的微博 #Python自动化#"
```

### 第 4 步：完成登录

脚本运行后会自动打开浏览器，显示微博登录页面：

1. 使用手机微博 APP 扫描二维码
2. 在手机上确认登录
3. 等待浏览器自动跳转到首页

**提示：** 首次登录后会自动保存登录状态，下次运行无需重新登录。

### 第 5 步：等待发布完成

脚本会自动：

1. 点击"写微博"按钮
2. 输入微博内容
3. 点击"发布"按钮
4. 验证发布结果

看到 `✅ 微博发布成功！` 即表示发布完成。

## 进阶使用

### 发布带图片的微博

```python
weibo_publish_skill(
    content="分享美图 #摄影#",
    image_paths=["photo1.jpg", "photo2.jpg"]
)
```

### 保持浏览器打开（推荐用于调试）

```python
# 发布后不自动关闭浏览器，方便查看结果
weibo_publish_skill(
    content="测试微博",
    keep_browser_open=True  # 浏览器保持打开，按 Ctrl+C 退出
)
```

### 自定义等待时间

```python
# 发布后等待 10 秒再关闭浏览器
weibo_publish_skill(
    content="测试微博",
    wait_after_publish=10  # 等待 10 秒
)
```

### 批量发布

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

### 无头模式（后台运行）

```python
weibo_publish_skill(
    content="后台自动发布",
    headless=True  # 不显示浏览器窗口
)
```

### 定时发布

使用 CoPaw 的 cron 功能：

```bash
# 每天早上 9:00 发布早安微博
copaw cron create \
  --type agent \
  --name "每日早安" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user "system" \
  --target-session "default" \
  --text "使用 weibo_publish 技能发布：早安，新的一天开始了！#早安#"
```

## 常见问题

### Q1: 登录超时怎么办？

**A:** 增加登录超时时间：

```python
weibo_publish_skill(
    content="测试",
    login_timeout=120  # 增加到 2 分钟
)
```

### Q2: 如何清除登录状态？

**A:** 删除 cookies 文件：

```bash
rm weibo_cookies.json
```

### Q3: 发布失败怎么办？

**A:** 查看错误截图：

```bash
ls -lt weibo_*.png | head -1
```

使用可视化模式观察：

```python
weibo_publish_skill(
    content="测试",
    headless=False  # 可视化运行
)
```

### Q4: 如何避免账号被限制？

**A:** 控制发布频率：

- 每次发布间隔至少 5 分钟
- 每天发布不超过 20 条
- 内容不要完全重复
- 避免深夜发布

### Q5: 支持哪些图片格式？

**A:** 支持常见格式：

- JPG/JPEG
- PNG
- GIF
- 单张图片不超过 5MB
- 最多 9 张图片

## 测试验证

运行测试脚本验证功能：

```bash
python test_weibo.py
```

## 下一步

- 查看 [API 参考](api_reference.md) 了解详细参数
- 查看 [故障排查](troubleshooting.md) 解决问题
- 查看 [示例脚本](../scripts/example.py) 学习更多用法

## 获取帮助

如果遇到问题：

1. 查看错误截图
2. 阅读故障排查指南
3. 检查日志输出
4. 提交 Issue

## 最佳实践

### ✅ 推荐做法

- 首次使用可视化模式（`headless=False`）
- 保存登录状态（`save_cookies=True`）
- 控制发布频率（间隔 5 分钟以上）
- 定期检查错误截图
- 使用定时任务自动化发布

### ❌ 避免做法

- 频繁发布（每分钟多条）
- 发布违规内容
- 在公共环境保存登录状态
- 使用相同内容重复发布
- 忽略错误信息

## 安全提示

⚠️ **重要提醒：**

1. **保护账号安全**：不要在公共环境使用
2. **保护 cookies**：`weibo_cookies.json` 包含登录信息，不要分享
3. **遵守规则**：确保内容符合微博社区规范
4. **控制频率**：避免被识别为机器人
5. **备份数据**：定期备份重要内容

## 许可证

本技能基于 Apache 2.0 许可证开源。

