# 批量连续发布功能说明

## ✨ 新功能：连续发布

从 v1.2.0 开始，新增了 `weibo_batch_publish()` 函数，支持**浏览器保持打开，连续发布多条微博**，大幅提升批量发布效率。

## 🆚 新旧方式对比

### 旧方式（不推荐）

```python
# ❌ 每次都重新打开关闭浏览器
for post in posts:
    weibo_publish_skill(**post)  # 打开浏览器 → 登录 → 发布 → 关闭
    time.sleep(300)
```

**缺点：**
- 每条微博都要重新打开浏览器（慢）
- 每条微博都要重新登录（不稳定）
- 频繁操作容易被检测为异常

### 新方式（推荐）✅

```python
# ✅ 浏览器只打开一次，连续发布
result = weibo_batch_publish(posts, interval=300)
# 打开浏览器 → 登录一次 → 发布所有微博 → 关闭
```

**优点：**
- 浏览器只打开一次（快）
- 只需登录一次（稳定）
- 减少操作次数，更像真人行为

## 📖 使用方法

### 基本用法

```python
from weibo_publish import weibo_batch_publish

# 准备微博列表
posts = [
    {"content": "第一条微博", "image_paths": None},
    {"content": "第二条微博", "image_paths": ["photo.jpg"]},
    {"content": "第三条微博", "image_paths": ["p1.jpg", "p2.jpg"]},
]

# 批量发布
result = weibo_batch_publish(
    posts=posts,
    headless=False,  # 可视化运行
    interval=300  # 每条间隔 5 分钟（300 秒）
)

# 查看结果
print(f"成功: {result['success']} 条")
print(f"失败: {result['failed']} 条")
print(f"总计: {result['total']} 条")
```

### 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `posts` | List[dict] | 是 | - | 微博列表，每个元素包含 `content` 和 `image_paths` |
| `headless` | bool | 否 | False | 是否无头模式运行 |
| `login_timeout` | int | 否 | 60 | 登录超时时间（秒） |
| `save_cookies` | bool | 否 | True | 是否保存登录状态 |
| `interval` | int | 否 | 300 | 每条微博之间的间隔时间（秒） |

### 返回值

```python
{
    "success": 2,  # 成功发布的数量
    "failed": 1,   # 失败的数量
    "total": 3     # 总数
}
```

## 💡 使用示例

### 示例 1: 发布纯文字微博

```python
posts = [
    {"content": "早安 ☀️ #早安#"},
    {"content": "午安 🌤️ #午安#"},
    {"content": "晚安 🌙 #晚安#"},
]

result = weibo_batch_publish(posts, interval=180)  # 间隔 3 分钟
```

### 示例 2: 发布带图片的微博

```python
posts = [
    {
        "content": "分享美食 #美食#",
        "image_paths": ["food1.jpg", "food2.jpg"]
    },
    {
        "content": "分享风景 #旅行#",
        "image_paths": ["scenery.jpg"]
    },
]

result = weibo_batch_publish(posts, interval=300)
```

### 示例 3: 混合发布

```python
posts = [
    {"content": "纯文字微博"},
    {"content": "带图片的微博", "image_paths": ["photo.jpg"]},
    {"content": "多图微博", "image_paths": ["p1.jpg", "p2.jpg", "p3.jpg"]},
]

result = weibo_batch_publish(posts, headless=False, interval=300)
```

### 示例 4: 后台批量发布

```python
# 无头模式，适合服务器运行
result = weibo_batch_publish(
    posts=posts,
    headless=True,  # 后台运行
    interval=600  # 间隔 10 分钟
)
```

## ⚙️ 工作流程

```
1. 打开浏览器
   ↓
2. 登录微博（扫码或使用保存的 cookies）
   ↓
3. 循环发布每条微博：
   - 点击"写微博"
   - 输入内容
   - 上传图片（如果有）
   - 点击发布
   - 返回首页
   - 等待间隔时间
   ↓
4. 所有微博发布完成
   ↓
5. 关闭浏览器
```

## ⚠️ 注意事项

### 1. 间隔时间建议

- **最小间隔**: 建议不少于 3 分钟（180 秒）
- **推荐间隔**: 5-10 分钟（300-600 秒）
- **原因**: 避免被微博检测为机器人，导致账号被限制

### 2. 发布数量建议

- **每次批量**: 建议不超过 10 条
- **每天总量**: 建议不超过 30 条
- **原因**: 模拟真人行为，避免触发风控

### 3. 错误处理

- 如果某条微博发布失败，会自动跳过，继续发布下一条
- 失败的微博会记录在返回结果的 `failed` 字段中
- 建议检查返回结果，手动补发失败的微博

### 4. 中断恢复

- 如果批量发布过程中被中断（Ctrl+C），已发布的微博不会回滚
- 建议记录已发布的位置，下次从未发布的位置继续

## 🔧 高级用法

### 动态生成微博内容

```python
from datetime import datetime

# 动态生成微博
posts = []
for i in range(5):
    posts.append({
        "content": f"第 {i+1} 条自动微博 - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "image_paths": None
    })

result = weibo_batch_publish(posts, interval=300)
```

### 从文件读取微博内容

```python
import json

# 从 JSON 文件读取
with open("posts.json", "r", encoding="utf-8") as f:
    posts = json.load(f)

result = weibo_batch_publish(posts, interval=300)
```

`posts.json` 示例：
```json
[
    {"content": "第一条微博", "image_paths": null},
    {"content": "第二条微博", "image_paths": ["photo.jpg"]},
    {"content": "第三条微博", "image_paths": ["p1.jpg", "p2.jpg"]}
]
```

## 📊 性能对比

假设发布 10 条微博：

| 方式 | 浏览器打开次数 | 登录次数 | 总耗时（估算） |
|------|----------------|----------|----------------|
| 旧方式 | 10 次 | 10 次 | ~15 分钟 |
| 新方式 | 1 次 | 1 次 | ~5 分钟 |

**效率提升**: 约 **3 倍**

## 🐛 故障排查

### 问题 1: 发布失败率高

**可能原因**: 间隔时间太短
**解决方案**: 增加 `interval` 参数，建议 300 秒以上

### 问题 2: 登录失败

**可能原因**: cookies 过期
**解决方案**: 删除 `weibo_cookies.json`，重新扫码登录

### 问题 3: 浏览器崩溃

**可能原因**: 内存不足
**解决方案**: 减少批量发布数量，分批发布

