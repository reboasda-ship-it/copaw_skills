# 持久化登录功能说明

## ⭐ 新功能：持久化登录

从 v1.3.0 开始，微博发布技能支持**持久化登录**功能，使用 Chrome 用户数据目录保存登录状态，实现**登录一次，永久有效**！

## 🆚 与 Chrome CDP 版本对比

### Chrome CDP 版本的优势

Chrome CDP 版本使用真实 Chrome 浏览器的用户数据，登录状态非常持久。

### Playwright 持久化版本的优势

现在 Playwright 版本也支持持久化用户数据了！

| 特性 | Chrome CDP 版本 | Playwright 持久化版本 |
|------|-----------------|----------------------|
| 登录持久性 | ✅ 永久有效 | ✅ 永久有效 |
| 浏览器类型 | 真实 Chrome | Chromium |
| 批量发布 | ❓ 未知 | ✅ 支持 |
| 连续发布 | ❓ 未知 | ✅ 支持 |
| 反检测 | ✅ 好 | ✅ 好 |
| 文档完整性 | ⚠️ 一般 | ✅ 完整 |

## 🔧 工作原理

### 传统 Cookies 模式（旧）

```
每次运行:
1. 启动浏览器
2. 加载 cookies 文件
3. 访问微博
4. 可能需要重新登录（cookies 过期）
```

**问题：** Cookies 容易过期，需要频繁重新登录

### 持久化上下文模式（新）⭐

```
每次运行:
1. 启动浏览器（使用固定的用户数据目录）
2. 自动加载所有登录信息（cookies、localStorage、session 等）
3. 访问微博
4. 已经登录！无需任何操作
```

**优势：** 
- 登录状态永久保存
- 包含所有浏览器数据（不仅是 cookies）
- 就像使用自己的 Chrome 浏览器一样

## 📁 用户数据存储位置

```
~/.copaw/browser_data/weibo_chrome/
```

这个目录包含：
- Cookies
- LocalStorage
- SessionStorage
- IndexedDB
- 浏览器缓存
- 等等...

## 💡 使用方法

### 方法 1：默认使用（推荐）

```python
from weibo_publish import weibo_publish_skill

# 默认就是持久化模式，无需额外配置
weibo_publish_skill(content="测试微博")
```

第一次运行时会提示：
```
✅ 使用持久化用户数据目录: ~/.copaw/browser_data/weibo_chrome
💡 登录状态将永久保存，下次打开自动登录
```

### 方法 2：显式指定

```python
weibo_publish_skill(
    content="测试微博",
    use_persistent_context=True  # 明确使用持久化模式（默认值）
)
```

### 方法 3：禁用持久化（使用旧的 cookies 模式）

```python
weibo_publish_skill(
    content="测试微博",
    use_persistent_context=False  # 使用传统 cookies 模式
)
```

## 🚀 首次使用流程

### 第 1 次运行

```python
weibo_publish_skill(content="第一条微博")
```

**会发生什么：**
1. 创建用户数据目录 `~/.copaw/browser_data/weibo_chrome/`
2. 打开浏览器
3. 显示微博登录页面
4. **你需要扫码登录**
5. 登录成功后，所有数据自动保存到用户数据目录
6. 发布微博
7. 关闭浏览器

### 第 2 次及以后运行

```python
weibo_publish_skill(content="第二条微博")
```

**会发生什么：**
1. 使用已有的用户数据目录
2. 打开浏览器
3. **自动已登录！** 无需扫码
4. 直接发布微博
5. 关闭浏览器

## 🎯 批量发布也支持

```python
from weibo_publish import weibo_batch_publish

posts = [
    {"content": "第一条微博"},
    {"content": "第二条微博"},
    {"content": "第三条微博"},
]

# 默认使用持久化模式
result = weibo_batch_publish(posts, interval=300)
```

**优势：**
- 第一次运行：登录一次，发布所有微博
- 以后运行：无需登录，直接发布所有微博

## 🔄 重新登录

如果需要重新登录（例如换账号），删除用户数据目录即可：

```bash
rm -rf ~/.copaw/browser_data/weibo_chrome
```

下次运行时会重新创建，并要求重新登录。

## ⚙️ 高级配置

### 自定义用户数据目录

如果你想使用不同的目录，可以修改 `weibo_publish.py` 中的常量：

```python
USER_DATA_DIR = os.path.expanduser("~/.copaw/browser_data/weibo_chrome")
```

改为：

```python
USER_DATA_DIR = os.path.expanduser("~/my_custom_path/weibo_data")
```

### 多账号支持

如果需要支持多个微博账号，可以为每个账号创建不同的用户数据目录：

```python
# 账号 1
USER_DATA_DIR = "~/.copaw/browser_data/weibo_account1"

# 账号 2
USER_DATA_DIR = "~/.copaw/browser_data/weibo_account2"
```

## 📊 对比总结

| 模式 | 登录持久性 | 使用便捷性 | 推荐度 |
|------|-----------|-----------|--------|
| 持久化上下文 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ 强烈推荐 |
| Cookies 文件 | ⭐⭐⭐ | ⭐⭐⭐ | ⚠️ 不推荐 |

## 🎊 总结

持久化登录功能让 Playwright 版本的登录体验**媲美 Chrome CDP 版本**：

- ✅ 登录一次，永久有效
- ✅ 无需频繁扫码
- ✅ 更稳定、更方便
- ✅ 默认启用，无需配置

现在你可以像使用 Chrome CDP 版本一样，享受持久化登录的便利了！🚀

