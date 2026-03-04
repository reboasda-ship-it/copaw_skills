#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博发布示例脚本
演示各种使用场景
"""
import time
from weibo_publish import weibo_publish_skill, weibo_batch_publish


def example_1_simple_text():
    """示例 1: 发布纯文字微博"""
    print("\n=== 示例 1: 发布纯文字微博 ===")

    weibo_publish_skill(
        content="这是一条测试微博，使用 Python + Playwright 自动发布 #Python自动化#",
        headless=False,  # 可视化运行
        wait_after_publish=10  # 发布后等待 10 秒再关闭
    )


def example_2_with_images():
    """示例 2: 发布带图片的微博"""
    print("\n=== 示例 2: 发布带图片的微博 ===")
    
    # 准备图片路径
    image_paths = [
        "photo1.jpg",
        "photo2.jpg",
    ]
    
    weibo_publish_skill(
        content="分享两张美图 #摄影# #风景#",
        image_paths=image_paths,
        headless=False
    )


def example_3_batch_publish():
    """示例 3: 批量发布多条微博"""
    print("\n=== 示例 3: 批量发布 ===")
    
    posts = [
        {
            "content": "第一条微博：早安！新的一天开始了 #早安#",
            "image_paths": None
        },
        {
            "content": "第二条微博：分享一张图片",
            "image_paths": ["photo1.jpg"]
        },
        {
            "content": "第三条微博：今天天气不错 #天气#",
            "image_paths": None
        },
    ]
    
    for i, post in enumerate(posts, 1):
        print(f"\n正在发布第 {i}/{len(posts)} 条...")
        
        try:
            weibo_publish_skill(**post)
            print(f"✅ 第 {i} 条发布成功")
        except Exception as e:
            print(f"❌ 第 {i} 条发布失败: {e}")
        
        # 间隔 5 分钟，避免频繁发布
        if i < len(posts):
            print("等待 5 分钟后发布下一条...")
            time.sleep(300)


def example_4_scheduled_publish():
    """示例 4: 定时发布（配合 CoPaw cron）"""
    print("\n=== 示例 4: 定时发布配置 ===")
    
    # 这是一个配置示例，实际使用时通过 copaw cron 命令创建
    cron_config = """
    # 每天早上 9:00 发布早安微博
    copaw cron create \\
      --type agent \\
      --name "每日早安微博" \\
      --cron "0 9 * * *" \\
      --channel console \\
      --target-user "system" \\
      --target-session "default" \\
      --text "使用 weibo_publish 技能发布：早安，新的一天开始了！#早安#"
    
    # 每周一 10:00 发布周报
    copaw cron create \\
      --type agent \\
      --name "每周周报" \\
      --cron "0 10 * * 1" \\
      --channel console \\
      --target-user "system" \\
      --target-session "default" \\
      --text "使用 weibo_publish 技能发布本周工作总结"
    """
    
    print(cron_config)


def example_5_headless_mode():
    """示例 5: 无头模式运行（后台）"""
    print("\n=== 示例 5: 无头模式运行 ===")
    
    weibo_publish_skill(
        content="后台自动发布的微博 #自动化#",
        headless=True,  # 无头模式
        save_cookies=True  # 保存登录状态
    )


def example_6_error_handling():
    """示例 6: 错误处理"""
    print("\n=== 示例 6: 错误处理 ===")
    
    try:
        # 尝试发布超长内容
        long_content = "测试" * 1000  # 超过 2000 字
        weibo_publish_skill(content=long_content)
        
    except ValueError as e:
        print(f"参数错误: {e}")
    
    except FileNotFoundError as e:
        print(f"文件不存在: {e}")
    
    except RuntimeError as e:
        print(f"运行时错误: {e}")
        print("请查看错误截图进行排查")
    
    except Exception as e:
        print(f"未知错误: {e}")


def example_7_with_cookies():
    """示例 7: 使用保存的登录状态"""
    print("\n=== 示例 7: 使用保存的登录状态 ===")

    # 首次运行会要求登录并保存 cookies
    weibo_publish_skill(
        content="首次登录，保存状态",
        save_cookies=True
    )

    # 后续运行会自动使用保存的 cookies，无需重新登录
    weibo_publish_skill(
        content="使用已保存的登录状态",
        save_cookies=True
    )


def example_8_keep_browser_open():
    """示例 8: 保持浏览器打开"""
    print("\n=== 示例 8: 保持浏览器打开 ===")

    weibo_publish_skill(
        content="测试微博，浏览器将保持打开",
        headless=False,
        keep_browser_open=True  # 不自动关闭，按 Ctrl+C 退出
    )


def example_9_custom_wait():
    """示例 9: 自定义等待时间"""
    print("\n=== 示例 9: 自定义等待时间 ===")

    weibo_publish_skill(
        content="测试微博，等待 15 秒后关闭",
        headless=False,
        wait_after_publish=15  # 等待 15 秒
    )


def example_10_batch_publish():
    """示例 10: 批量连续发布（推荐）✨"""
    print("\n=== 示例 10: 批量连续发布 ===")

    # 准备多条微博
    posts = [
        {"content": "第一条测试微博 #Python#", "image_paths": None},
        {"content": "第二条测试微博 #自动化#", "image_paths": None},
        {"content": "第三条测试微博 #Playwright#", "image_paths": None},
    ]

    print(f"准备发布 {len(posts)} 条微博...")
    print("浏览器只会打开一次，连续发布所有微博")

    # 批量发布
    result = weibo_batch_publish(
        posts=posts,
        headless=False,  # 可视化运行
        interval=60  # 演示用，间隔 1 分钟（实际使用建议 300 秒）
    )

    print(f"\n发布完成！")
    print(f"  成功: {result['success']} 条")
    print(f"  失败: {result['failed']} 条")
    print(f"  总计: {result['total']} 条")


def example_11_batch_with_images():
    """示例 11: 批量发布带图片的微博"""
    print("\n=== 示例 11: 批量发布带图片 ===")

    posts = [
        {
            "content": "分享美图 1 #摄影#",
            "image_paths": ["photo1.jpg"] if os.path.exists("photo1.jpg") else None
        },
        {
            "content": "分享美图 2 #摄影#",
            "image_paths": ["photo2.jpg"] if os.path.exists("photo2.jpg") else None
        },
    ]

    result = weibo_batch_publish(
        posts=posts,
        headless=False,
        interval=180  # 间隔 3 分钟
    )

    print(f"发布结果: {result}")


import os


def main():
    """主函数"""
    print("微博发布示例脚本")
    print("=" * 50)

    # 选择要运行的示例
    examples = {
        "1": ("发布纯文字微博", example_1_simple_text),
        "2": ("发布带图片的微博", example_2_with_images),
        "3": ("批量发布（旧方式）", example_3_batch_publish),
        "4": ("定时发布配置", example_4_scheduled_publish),
        "5": ("无头模式运行", example_5_headless_mode),
        "6": ("错误处理", example_6_error_handling),
        "7": ("使用保存的登录状态", example_7_with_cookies),
        "8": ("保持浏览器打开", example_8_keep_browser_open),
        "9": ("自定义等待时间", example_9_custom_wait),
        "10": ("✨ 批量连续发布（推荐）", example_10_batch_publish),
        "11": ("批量发布带图片", example_11_batch_with_images),
    }

    print("\n可用示例:")
    for key, (desc, _) in examples.items():
        print(f"  {key}. {desc}")

    choice = input("\n请选择示例编号 (1-11): ").strip()

    if choice in examples:
        desc, func = examples[choice]
        print(f"\n运行示例: {desc}")
        func()
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()

