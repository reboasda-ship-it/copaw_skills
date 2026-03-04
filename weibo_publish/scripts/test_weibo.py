#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博发布功能测试脚本
用于验证各项功能是否正常工作
"""
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock


class TestWeiboPublisher(unittest.TestCase):
    """测试 WeiboPublisher 类"""
    
    def setUp(self):
        """测试前准备"""
        # 导入模块
        sys.path.insert(0, str(Path(__file__).parent))
        from weibo_publish import WeiboPublisher
        self.WeiboPublisher = WeiboPublisher
    
    def test_init(self):
        """测试初始化"""
        publisher = self.WeiboPublisher(headless=True, save_cookies=False)
        self.assertTrue(publisher.headless)
        self.assertFalse(publisher.save_cookies)
    
    def test_browser_args(self):
        """测试浏览器参数"""
        publisher = self.WeiboPublisher()
        args = publisher._get_browser_args()
        
        self.assertIn("--disable-blink-features=AutomationControlled", args)
        self.assertIn("--no-sandbox", args)
    
    def test_user_agent(self):
        """测试 User-Agent"""
        publisher = self.WeiboPublisher()
        ua = publisher._get_user_agent()
        
        self.assertIn("Chrome", ua)
        self.assertIn("Mozilla", ua)


class TestWeiboPublishSkill(unittest.TestCase):
    """测试 weibo_publish_skill 函数"""
    
    def setUp(self):
        """测试前准备"""
        sys.path.insert(0, str(Path(__file__).parent))
        from weibo_publish import weibo_publish_skill, MAX_CONTENT_LENGTH, MAX_IMAGES
        self.weibo_publish_skill = weibo_publish_skill
        self.MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
        self.MAX_IMAGES = MAX_IMAGES
    
    def test_content_length_validation(self):
        """测试内容长度校验"""
        # 正常长度
        content = "测试" * 100  # 200 字
        # 这里不实际执行，只测试参数
        
        # 超长内容
        long_content = "测试" * 2000  # 4000 字
        with self.assertRaises(ValueError):
            # Mock playwright 避免实际执行
            with patch('weibo_publish.sync_playwright'):
                self.weibo_publish_skill(content=long_content)
    
    def test_image_count_validation(self):
        """测试图片数量校验"""
        # 创建临时测试文件
        test_images = []
        for i in range(10):
            img_path = f"test_img_{i}.jpg"
            Path(img_path).touch()
            test_images.append(img_path)
        
        try:
            # 超过最大数量
            with self.assertRaises(ValueError):
                with patch('weibo_publish.sync_playwright'):
                    self.weibo_publish_skill(
                        content="测试",
                        image_paths=test_images
                    )
        finally:
            # 清理测试文件
            for img in test_images:
                if os.path.exists(img):
                    os.remove(img)
    
    def test_image_file_exists(self):
        """测试图片文件存在性校验"""
        with self.assertRaises(FileNotFoundError):
            with patch('weibo_publish.sync_playwright'):
                self.weibo_publish_skill(
                    content="测试",
                    image_paths=["non_existent.jpg"]
                )


class TestIntegration(unittest.TestCase):
    """集成测试（需要实际环境）"""
    
    @unittest.skip("需要实际微博账号和浏览器环境")
    def test_real_publish(self):
        """真实发布测试（跳过）"""
        from weibo_publish import weibo_publish_skill
        
        result = weibo_publish_skill(
            content="自动化测试微博 #测试#",
            headless=False,
            login_timeout=120
        )
        
        self.assertTrue(result)


def run_validation_tests():
    """运行验证测试"""
    print("=" * 60)
    print("微博发布功能验证测试")
    print("=" * 60)
    
    # 检查依赖
    print("\n1. 检查依赖...")
    try:
        import playwright
        print("   ✅ Playwright 已安装")
    except ImportError:
        print("   ❌ Playwright 未安装")
        print("   请运行: pip install playwright")
        return False
    
    # 检查 Chromium
    print("\n2. 检查 Chromium...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("   ✅ Chromium 可用")
    except Exception as e:
        print(f"   ❌ Chromium 不可用: {e}")
        print("   请运行: playwright install chromium")
        return False
    
    # 检查脚本文件
    print("\n3. 检查脚本文件...")
    script_path = Path(__file__).parent / "weibo_publish.py"
    if script_path.exists():
        print(f"   ✅ 脚本文件存在: {script_path}")
    else:
        print(f"   ❌ 脚本文件不存在: {script_path}")
        return False
    
    # 运行单元测试
    print("\n4. 运行单元测试...")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestWeiboPublisher))
    suite.addTests(loader.loadTestsFromTestCase(TestWeiboPublishSkill))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"运行测试: {result.testsRun}")
    print(f"成功: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ 所有测试通过！")
        return True
    else:
        print("\n❌ 部分测试失败")
        return False


if __name__ == "__main__":
    # 运行验证测试
    success = run_validation_tests()
    sys.exit(0 if success else 1)

