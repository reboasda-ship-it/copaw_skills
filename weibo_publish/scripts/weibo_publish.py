#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博发布自动化脚本
使用 Playwright 实现微博登录和内容发布
"""
import os
import time
import json
import logging
from pathlib import Path
from typing import List, Optional
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 常量配置
WEIBO_LOGIN_URL = "https://weibo.com/login.php"
WEIBO_HOME_URL = "https://weibo.com/"
COOKIES_FILE = "weibo_cookies.json"
USER_DATA_DIR = os.path.expanduser("~/.copaw/browser_data/weibo_chrome")  # Chrome 用户数据目录
MAX_CONTENT_LENGTH = 2000
MAX_IMAGES = 9


class WeiboPublisher:
    """微博发布器"""
    
    def __init__(self, headless: bool = False, save_cookies: bool = True, use_persistent_context: bool = True):
        """
        初始化微博发布器

        Args:
            headless: 是否无头模式运行
            save_cookies: 是否保存登录状态（已弃用，建议使用 use_persistent_context）
            use_persistent_context: 是否使用持久化上下文（推荐，登录状态永久保存）
        """
        self.headless = headless
        self.save_cookies = save_cookies
        self.use_persistent_context = use_persistent_context
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
    def _get_browser_args(self) -> List[str]:
        """获取浏览器启动参数（反检测配置）"""
        return [
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-web-security",
        ]
    
    def _get_user_agent(self) -> str:
        """获取 User-Agent"""
        return (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    
    def _init_browser(self, playwright):
        """初始化浏览器"""
        logger.info("正在启动浏览器...")

        # 如果使用持久化上下文（推荐）
        if self.use_persistent_context:
            # 确保用户数据目录存在
            os.makedirs(USER_DATA_DIR, exist_ok=True)
            logger.info(f"✅ 使用持久化用户数据目录: {USER_DATA_DIR}")
            logger.info("💡 登录状态将永久保存，下次打开自动登录")

            # 使用持久化上下文启动浏览器（类似 Chrome CDP）
            self.context = playwright.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=self.headless,
                slow_mo=50,
                viewport=None if not self.headless else {"width": 1920, "height": 1080},
                user_agent=self._get_user_agent(),
                args=self._get_browser_args()
            )

            # 移除 webdriver 标识
            self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)

            # 获取或创建页面
            self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
            logger.info("🎉 浏览器启动成功（持久化模式）")

        else:
            # 传统模式：使用 cookies 文件
            logger.info("使用传统 cookies 模式")
            self.browser = playwright.chromium.launch(
                headless=self.headless,
                args=self._get_browser_args(),
                slow_mo=50
            )

            # 创建上下文
            self.context = self.browser.new_context(
                viewport=None if not self.headless else {"width": 1920, "height": 1080},
                user_agent=self._get_user_agent()
            )

            # 移除 webdriver 标识
            self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
            """)

            # 加载已保存的 cookies（如果存在）
            if self.save_cookies and os.path.exists(COOKIES_FILE):
                try:
                    with open(COOKIES_FILE, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                        self.context.add_cookies(cookies)
                        logger.info("已加载保存的登录状态")
                except Exception as e:
                    logger.warning(f"加载 cookies 失败: {e}")

            self.page = self.context.new_page()
            logger.info("浏览器启动成功（cookies 模式）")
    
    def _save_cookies(self):
        """保存 cookies"""
        if not self.save_cookies or not self.context:
            return
        
        try:
            cookies = self.context.cookies()
            with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info("登录状态已保存")
        except Exception as e:
            logger.warning(f"保存 cookies 失败: {e}")
    
    def _take_screenshot(self, name: str = "error"):
        """截图保存"""
        if not self.page:
            return
        
        try:
            timestamp = int(time.time())
            filename = f"weibo_{name}_{timestamp}.png"
            self.page.screenshot(path=filename, full_page=True)
            logger.info(f"截图已保存: {filename}")
        except Exception as e:
            logger.error(f"截图失败: {e}")
    
    def login(self, timeout: int = 60):
        """
        登录微博
        
        Args:
            timeout: 登录超时时间（秒）
        """
        logger.info("正在访问微博登录页...")
        self.page.goto(WEIBO_LOGIN_URL, wait_until="networkidle")
        
        # 检查是否已经登录
        if self.page.url.startswith(WEIBO_HOME_URL):
            logger.info("检测到已登录状态")
            return
        
        logger.info(f"请在 {timeout} 秒内完成扫码登录...")
        
        try:
            # 等待登录完成（跳转到首页）
            self.page.wait_for_url(
                lambda url: url.startswith(WEIBO_HOME_URL),
                timeout=timeout * 1000
            )
            logger.info("✅ 登录成功！")
            time.sleep(2)  # 等待页面完全加载
            
            # 保存登录状态
            self._save_cookies()
            
        except Exception as e:
            self._take_screenshot("login_timeout")
            raise RuntimeError(f"登录超时或失败: {e}")

    def publish(self, content: str, image_paths: Optional[List[str]] = None, return_to_home: bool = True):
        """
        发布微博

        Args:
            content: 微博内容
            image_paths: 图片路径列表
            return_to_home: 发布后是否返回首页（用于连续发布）
        """
        # 校验内容长度
        if len(content) > MAX_CONTENT_LENGTH:
            raise ValueError(f"微博内容不能超过 {MAX_CONTENT_LENGTH} 字！当前 {len(content)} 字")

        # 校验图片
        if image_paths:
            if len(image_paths) > MAX_IMAGES:
                raise ValueError(f"最多只能上传 {MAX_IMAGES} 张图片！")

            for img_path in image_paths:
                if not os.path.exists(img_path):
                    raise FileNotFoundError(f"图片文件不存在: {img_path}")

        try:
            logger.info("正在打开发微博页面...")

            # 如果不在首页，先返回首页
            if not self.page.url.startswith(WEIBO_HOME_URL):
                logger.info("返回首页...")
                self.page.goto(WEIBO_HOME_URL, wait_until="networkidle")
                time.sleep(1)

            # 点击"写微博"按钮
            # 尝试多种可能的定位方式
            publish_btn_selectors = [
                'text=/写微博|发微博/',
                '[aria-label*="写微博"]',
                '[aria-label*="发微博"]',
                'a[href*="publish"]',
            ]

            clicked = False
            for selector in publish_btn_selectors:
                try:
                    self.page.locator(selector).first.click(timeout=3000)
                    clicked = True
                    logger.info("已点击写微博按钮")
                    break
                except:
                    continue

            if not clicked:
                raise RuntimeError("未找到写微博按钮")

            time.sleep(1.5)

            # 输入微博内容
            logger.info("正在输入微博内容...")
            content_box_selectors = [
                'div[contenteditable="true"][role="textbox"]',
                'textarea[placeholder*="微博"]',
                'div.Form_input_2gtXx',
            ]

            content_filled = False
            for selector in content_box_selectors:
                try:
                    content_box = self.page.locator(selector).first
                    content_box.click()
                    time.sleep(0.5)
                    content_box.fill(content)
                    content_filled = True
                    logger.info(f"已输入内容: {content[:50]}...")
                    break
                except:
                    continue

            if not content_filled:
                raise RuntimeError("未找到内容输入框")

            time.sleep(1)

            # 上传图片（如果有）
            if image_paths:
                logger.info(f"正在上传 {len(image_paths)} 张图片...")

                # 查找图片上传按钮
                upload_selectors = [
                    'input[type="file"][accept*="image"]',
                    'input[type="file"]',
                ]

                uploaded = False
                for selector in upload_selectors:
                    try:
                        upload_input = self.page.locator(selector).first
                        # 一次性上传所有图片
                        upload_input.set_input_files(image_paths)
                        uploaded = True
                        logger.info("图片上传中...")
                        break
                    except:
                        continue

                if not uploaded:
                    logger.warning("未找到图片上传按钮，跳过图片上传")
                else:
                    # 等待图片上传完成
                    time.sleep(3)
                    logger.info("图片上传完成")

            # 点击发布按钮
            logger.info("正在发布微博...")
            submit_selectors = [
                'button:has-text("发布")',
                'button[type="submit"]',
                'button.Form_btn_2gtXx',
            ]

            submitted = False
            for selector in submit_selectors:
                try:
                    submit_btn = self.page.locator(selector).first
                    # 确保按钮可点击
                    submit_btn.wait_for(state="visible", timeout=5000)
                    submit_btn.click()
                    submitted = True
                    logger.info("发布按钮已点击")
                    break
                except:
                    continue

            if not submitted:
                raise RuntimeError("未找到发布按钮")

            # 等待发布完成
            time.sleep(3)

            # 验证发布结果
            # 检查是否有成功提示或返回首页
            success_indicators = [
                'text=/发布成功|发送成功/',
                'div[class*="success"]',
            ]

            success = False
            for indicator in success_indicators:
                try:
                    self.page.locator(indicator).first.wait_for(
                        state="visible",
                        timeout=5000
                    )
                    success = True
                    break
                except:
                    continue

            # 如果没有明确的成功提示，检查是否返回首页
            if not success and self.page.url.startswith(WEIBO_HOME_URL):
                success = True

            if success:
                logger.info("✅ 微博发布成功！")
                self._take_screenshot("success")
            else:
                logger.warning("⚠️ 无法确认发布状态，请手动检查")
                self._take_screenshot("unknown_status")

            # 发布后返回首页，准备下一次发布
            if return_to_home:
                logger.info("返回首页...")
                time.sleep(2)  # 等待发布完成
                self.page.goto(WEIBO_HOME_URL, wait_until="networkidle")
                time.sleep(1)

        except Exception as e:
            self._take_screenshot("publish_error")
            raise RuntimeError(f"微博发布失败: {e}")

    def close(self):
        """关闭浏览器"""
        if self.use_persistent_context:
            # 持久化上下文模式：关闭 context
            if self.context:
                self.context.close()
                logger.info("浏览器已关闭（用户数据已保存）")
        else:
            # 传统模式：关闭 browser
            if self.browser:
                self.browser.close()
                logger.info("浏览器已关闭")


def weibo_publish_skill(
    content: str,
    image_paths: Optional[List[str]] = None,
    headless: bool = False,
    login_timeout: int = 60,
    save_cookies: bool = True,
    keep_browser_open: bool = False,
    wait_after_publish: int = 5,
    use_persistent_context: bool = True,
):
    """
    微博发布技能主函数（单条发布）

    Args:
        content: 微博内容（限制 2000 字以内）
        image_paths: 图片路径列表（可选，最多 9 张）
        headless: 是否无头模式运行（False 可视化，True 后台运行）
        login_timeout: 登录超时时间（秒），默认 60 秒
        save_cookies: 是否保存登录状态，默认 True（已弃用，建议使用 use_persistent_context）
        keep_browser_open: 是否保持浏览器打开（默认 False，设为 True 则不自动关闭）
        wait_after_publish: 发布后等待时间（秒），默认 5 秒，方便查看结果
        use_persistent_context: 是否使用持久化上下文（默认 True，推荐！登录状态永久保存）

    Returns:
        bool: 发布是否成功

    Raises:
        ValueError: 参数校验失败
        FileNotFoundError: 图片文件不存在
        RuntimeError: 发布过程出错
    """
    publisher = None

    try:
        with sync_playwright() as p:
            publisher = WeiboPublisher(
                headless=headless,
                save_cookies=save_cookies,
                use_persistent_context=use_persistent_context
            )
            publisher._init_browser(p)

            # 登录
            publisher.login(timeout=login_timeout)

            # 发布
            publisher.publish(content=content, image_paths=image_paths)

            # 发布后等待，方便查看结果
            if wait_after_publish > 0:
                logger.info(f"发布完成，等待 {wait_after_publish} 秒后关闭浏览器...")
                time.sleep(wait_after_publish)

            # 如果设置了保持浏览器打开，则等待用户手动关闭
            if keep_browser_open:
                logger.info("浏览器将保持打开，按 Ctrl+C 或关闭浏览器窗口退出...")
                try:
                    # 无限等待，直到用户手动关闭
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    logger.info("用户中断，正在关闭浏览器...")

            return True

    except Exception as e:
        logger.error(f"执行失败: {e}")
        raise

    finally:
        if publisher and not keep_browser_open:
            publisher.close()


def weibo_batch_publish(
    posts: List[dict],
    headless: bool = False,
    login_timeout: int = 60,
    save_cookies: bool = True,
    interval: int = 300,
    use_persistent_context: bool = True,
):
    """
    批量发布微博（浏览器保持打开，连续发布）

    Args:
        posts: 微博列表，每个元素是包含 content 和 image_paths 的字典
        headless: 是否无头模式运行
        login_timeout: 登录超时时间（秒）
        save_cookies: 是否保存登录状态（已弃用，建议使用 use_persistent_context）
        interval: 每条微博之间的间隔时间（秒），默认 300 秒（5 分钟）
        use_persistent_context: 是否使用持久化上下文（默认 True，推荐！登录状态永久保存）

    Returns:
        dict: 发布结果统计 {"success": 成功数, "failed": 失败数, "total": 总数}

    Example:
        posts = [
            {"content": "第一条微博", "image_paths": None},
            {"content": "第二条微博", "image_paths": ["photo.jpg"]},
        ]
        result = weibo_batch_publish(posts, interval=300)
    """
    publisher = None
    success_count = 0
    failed_count = 0

    try:
        with sync_playwright() as p:
            publisher = WeiboPublisher(
                headless=headless,
                save_cookies=save_cookies,
                use_persistent_context=use_persistent_context
            )
            publisher._init_browser(p)

            # 登录一次
            logger.info("正在登录...")
            publisher.login(timeout=login_timeout)

            # 循环发布每条微博
            total = len(posts)
            for i, post in enumerate(posts, 1):
                content = post.get("content", "")
                image_paths = post.get("image_paths", None)

                logger.info(f"\n{'='*60}")
                logger.info(f"正在发布第 {i}/{total} 条微博...")
                logger.info(f"内容: {content[:50]}...")

                try:
                    # 发布微博（返回首页以便下次发布）
                    publisher.publish(
                        content=content,
                        image_paths=image_paths,
                        return_to_home=True
                    )
                    success_count += 1
                    logger.info(f"✅ 第 {i} 条发布成功")

                except Exception as e:
                    failed_count += 1
                    logger.error(f"❌ 第 {i} 条发布失败: {e}")
                    # 发布失败后尝试返回首页
                    try:
                        publisher.page.goto(WEIBO_HOME_URL, wait_until="networkidle")
                        time.sleep(1)
                    except:
                        pass

                # 如果不是最后一条，等待间隔时间
                if i < total:
                    logger.info(f"等待 {interval} 秒后发布下一条...")
                    time.sleep(interval)

            # 显示统计结果
            logger.info(f"\n{'='*60}")
            logger.info("批量发布完成！")
            logger.info(f"总计: {total} 条")
            logger.info(f"成功: {success_count} 条")
            logger.info(f"失败: {failed_count} 条")
            logger.info(f"{'='*60}\n")

            # 发布完成后等待 5 秒再关闭
            logger.info("等待 5 秒后关闭浏览器...")
            time.sleep(5)

            return {
                "success": success_count,
                "failed": failed_count,
                "total": total
            }

    except Exception as e:
        logger.error(f"批量发布失败: {e}")
        raise

    finally:
        if publisher:
            publisher.close()


# 命令行入口
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="微博发布自动化工具")
    parser.add_argument("content", help="微博内容")
    parser.add_argument(
        "-i", "--images",
        nargs="+",
        help="图片路径（可多个）"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="无头模式运行"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="登录超时时间（秒）"
    )
    parser.add_argument(
        "--no-save-cookies",
        action="store_true",
        help="不保存登录状态"
    )
    parser.add_argument(
        "--keep-open",
        action="store_true",
        help="发布后保持浏览器打开（不自动关闭）"
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=5,
        help="发布后等待时间（秒），默认 5 秒"
    )

    args = parser.parse_args()

    try:
        weibo_publish_skill(
            content=args.content,
            image_paths=args.images,
            headless=args.headless,
            login_timeout=args.timeout,
            save_cookies=not args.no_save_cookies,
            keep_browser_open=args.keep_open,
            wait_after_publish=args.wait,
        )
        print("\n✅ 发布成功！")
    except Exception as e:
        print(f"\n❌ 发布失败: {e}")
        exit(1)

