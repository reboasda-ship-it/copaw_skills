# 🐾 CoPaw Skills 技能库

> 为 [CoPaw](https://github.com/copaw) 打造的实用自动化技能合集，让 AI Agent 拥有更强大的能力。

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![CoPaw](https://img.shields.io/badge/CoPaw-Skills-green.svg)](https://github.com/copaw)

---

## 📖 项目简介

**CoPaw Skills** 是一个专为 CoPaw AI Agent 平台设计的技能扩展库。CoPaw 是一个强大的 AI Agent 框架，通过加载不同的 **Skill**，Agent 可以执行各种自动化任务。

本仓库提供开箱即用的技能模块，覆盖社交媒体自动化、内容发布、数据采集等场景，帮助你快速扩展 AI Agent 的能力边界。

---

## 🗂️ 技能列表

| 技能 | 描述 | 状态 |
|------|------|------|
| 📱 [weibo_publish](./weibo_publish/) | 微博自动登录 & 内容发布（支持图片、定时、批量） | ✅ 已发布 |
| 🔜 更多技能 | 持续更新中... | 🚧 开发中 |

---

## 📱 weibo_publish — 微博自动发布

使用 Playwright 实现微博自动化登录和内容发布，支持文字、图片、定时、批量发布。

### ✨ 功能特性

- ✅ **自动登录** — 支持扫码登录，登录状态持久化，一次登录永久有效
- ✅ **文字发布** — 支持最多 2000 字的文字内容
- ✅ **图片发布** — 支持最多 9 张图片（jpg / png / gif）
- ✅ **批量连续发布** — 浏览器保持打开，连续发布多条微博，效率提升 3 倍
- ✅ **定时发布** — 配合 CoPaw cron 实现定时任务
- ✅ **反检测机制** — 自动规避微博的自动化检测
- ✅ **完善的错误处理** — 自动截图保存错误现场，便于排查

### 🚀 快速开始

#### 1. 安装依赖

```bash
pip install playwright
playwright install chromium
```

#### 2. 发布微博

```python
from weibo_publish.scripts.weibo_publish import weibo_publish_skill, weibo_batch_publish

# 发布纯文字微博
weibo_publish_skill(content="早安！新的一天开始了 🌞 #早安#")

# 发布带图片的微博
weibo_publish_skill(
    content="分享今天的美食 #美食#",
    image_paths=["food1.jpg", "food2.jpg"]
)

# ⭐ 批量连续发布（推荐，浏览器只打开一次）
posts = [
    {"content": "第一条微博", "image_paths": None},
    {"content": "第二条微博", "image_paths": ["photo.jpg"]},
]
result = weibo_batch_publish(posts, interval=300)
```

#### 3. 命令行使用

```bash
# 发布纯文字
python weibo_publish/scripts/weibo_publish.py "测试微博内容"

# 发布带图片
python weibo_publish/scripts/weibo_publish.py "测试微博" -i photo1.jpg photo2.jpg

# 无头模式（后台运行）
python weibo_publish/scripts/weibo_publish.py "测试微博" --headless
```

#### 4. 定时发布（配合 CoPaw cron）

```bash
# 每天早上 9:00 自动发布早安微博
copaw cron create \
  --type agent \
  --name "每日早安" \
  --cron "0 9 * * *" \
  --channel console \
  --target-user "system" \
  --target-session "default" \
  --text "使用 weibo_publish 技能发布：早安，新的一天开始了！#早安#"
```

### 📋 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|--------|------|
| `content` | str | ✅ | — | 微博内容（最多 2000 字） |
| `image_paths` | List[str] | ❌ | None | 图片路径列表（最多 9 张） |
| `headless` | bool | ❌ | False | 是否无头模式运行 |
| `login_timeout` | int | ❌ | 60 | 登录超时时间（秒） |
| `save_cookies` | bool | ❌ | True | 是否保存登录状态 |
| `keep_browser_open` | bool | ❌ | False | 发布后是否保持浏览器打开 |
| `wait_after_publish` | int | ❌ | 5 | 发布后等待时间（秒） |

### 📁 文件结构

```
weibo_publish/
├── SKILL.md                    # CoPaw 技能配置文件
├── README.md                   # 技能详细文档
├── scripts/
│   ├── weibo_publish.py        # 核心发布脚本
│   ├── example.py              # 使用示例
│   └── test_weibo.py           # 测试脚本
└── references/
    ├── api_reference.md        # API 参考文档
    └── troubleshooting.md      # 故障排查指南
```

> 📚 详细文档请查看 [weibo_publish/README.md](./weibo_publish/README.md)

---

## ⚠️ 注意事项

1. **频率控制** — 建议每次发布间隔至少 5 分钟，避免触发风控
2. **内容合规** — 确保内容符合微博社区规范
3. **账号安全** — 不要在公共环境保存登录状态（cookies 文件）
4. **网络环境** — 确保网络稳定，能正常访问微博

---

## 🤝 加入交流群

欢迎加入 CoPaw Skills 交流群，一起分享技能、交流经验、共同打造更强大的 AI Agent！

> 📲 **扫描下方二维码，添加微信好友，备注「CoPaw」即可拉入群**

<div align="center">
  <img src="./assets/wechat_qr.png" alt="微信二维码" width="280" />
</div>

**群内你可以：**
- 💡 分享自己开发的 CoPaw 技能
- 🐛 反馈 Bug，共同改进
- 🚀 获取最新技能更新通知
- 🤖 探讨 AI Agent 自动化玩法

---

## 🛠️ 贡献指南

欢迎贡献新的技能或改进现有技能！

1. Fork 本仓库
2. 创建你的技能目录（参考 `weibo_publish/` 结构）
3. 在技能目录下添加 `SKILL.md`（CoPaw 技能配置文件）
4. 提交 Pull Request

---

## 📄 许可证

本项目基于 [Apache 2.0 License](LICENSE) 开源。
