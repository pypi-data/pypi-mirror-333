import os
import unittest
from unittest.mock import patch, MagicMock
from android.adb_utils import AdbUtils


class TestAdbUtilsAdvanced(unittest.TestCase):
    """AdbUtils类的高级功能测试"""

    @patch('android.adb_utils.AdbUtils.shell')
    def test_unlock_screen(self, mock_shell):
        """测试unlock_screen方法"""
        # 设置模拟对象的行为
        with patch('android.adb_utils.AdbUtils.screen_on') as mock_screen_on:
            # 执行测试 - 无设备参数
            AdbUtils.unlock_screen()
            mock_screen_on.assert_called_once_with(None)
            mock_shell.assert_called_with('input keyevent 82', None)

            # 执行测试 - 有设备参数
            mock_screen_on.reset_mock()
            mock_shell.reset_mock()
            AdbUtils.unlock_screen('device1')
            mock_screen_on.assert_called_once_with('device1')
            mock_shell.assert_called_with('input keyevent 82', 'device1')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_input_text(self, mock_shell):
        """测试input_text方法"""
        # 执行测试 - 无设备参数
        AdbUtils.input_text('test text')
        mock_shell.assert_called_with('input text "test text"', None)

        # 执行测试 - 有设备参数
        AdbUtils.input_text('test text', 'device1')
        mock_shell.assert_called_with('input text "test text"', 'device1')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_input_keyevent(self, mock_shell):
        """测试input_keyevent方法"""
        # 执行测试 - 无设备参数
        AdbUtils.input_keyevent(4)  # KEYCODE_BACK
        mock_shell.assert_called_with('input keyevent 4', None)

        # 执行测试 - 有设备参数
        AdbUtils.input_keyevent(4, 'device1')
        mock_shell.assert_called_with('input keyevent 4', 'device1')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_input_tap(self, mock_shell):
        """测试input_tap方法"""
        # 执行测试 - 无设备参数
        AdbUtils.input_tap(100, 200)
        mock_shell.assert_called_with('input tap 100 200', None)

        # 执行测试 - 有设备参数
        AdbUtils.input_tap(100, 200, 'device1')
        mock_shell.assert_called_with('input tap 100 200', 'device1')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_input_swipe(self, mock_shell):
        """测试input_swipe方法"""
        # 执行测试 - 无设备参数，默认持续时间
        AdbUtils.input_swipe(100, 200, 300, 400)
        mock_shell.assert_called_with('input swipe 100 200 300 400 500', None)

        # 执行测试 - 有设备参数，自定义持续时间
        AdbUtils.input_swipe(100, 200, 300, 400, 1000, 'device1')
        mock_shell.assert_called_with('input swipe 100 200 300 400 1000', 'device1')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_get_screen_resolution(self, mock_shell):
        """测试get_screen_resolution方法"""
        # 设置模拟对象的行为
        mock_shell.return_value = (0, 'Physical size: 1080x2340', '')

        # 执行测试 - 无设备参数
        width, height = AdbUtils.get_screen_resolution()
        mock_shell.assert_called_with('wm size', None)
        self.assertEqual(width, 1080)
        self.assertEqual(height, 2340)

        # 执行测试 - 有设备参数
        width, height = AdbUtils.get_screen_resolution('device1')
        mock_shell.assert_called_with('wm size', 'device1')
        self.assertEqual(width, 1080)
        self.assertEqual(height, 2340)

        # 测试无法获取分辨率的情况
        mock_shell.return_value = (0, 'Invalid output', '')
        width, height = AdbUtils.get_screen_resolution()
        self.assertEqual(width, 0)
        self.assertEqual(height, 0)

    @patch('android.adb_utils.AdbUtils.shell')
    def test_get_screen_density(self, mock_shell):
        """测试get_screen_density方法"""
        # 设置模拟对象的行为
        mock_shell.return_value = (0, 'Physical density: 480', '')

        # 执行测试 - 无设备参数
        density = AdbUtils.get_screen_density()
        mock_shell.assert_called_with('wm density', None)
        self.assertEqual(density, 480)

        # 执行测试 - 有设备参数
        density = AdbUtils.get_screen_density('device1')
        mock_shell.assert_called_with('wm density', 'device1')
        self.assertEqual(density, 480)

        # 测试无法获取密度的情况
        mock_shell.return_value = (0, 'Invalid output', '')
        density = AdbUtils.get_screen_density()
        self.assertEqual(density, 0)

    @patch('android.adb_utils.AdbUtils.pull')
    @patch('android.adb_utils.AdbUtils.shell')
    def test_take_screenshot(self, mock_shell, mock_pull):
        """测试take_screenshot方法"""
        # 设置模拟对象的行为
        mock_pull.return_value = True

        # 执行测试 - 无设备参数
        result = AdbUtils.take_screenshot('/path/to/save.png')
        mock_shell.assert_any_call('screencap -p /sdcard/screenshot.png', None)
        mock_pull.assert_called_with('/sdcard/screenshot.png', '/path/to/save.png', None)
        mock_shell.assert_called_with('rm /sdcard/screenshot.png', None)
        self.assertTrue(result)

        # 执行测试 - 有设备参数
        mock_shell.reset_mock()
        mock_pull.reset_mock()
        result = AdbUtils.take_screenshot('/path/to/save.png', 'device1')
        mock_shell.assert_any_call('screencap -p /sdcard/screenshot.png', 'device1')
        mock_pull.assert_called_with('/sdcard/screenshot.png', '/path/to/save.png', 'device1')
        mock_shell.assert_called_with('rm /sdcard/screenshot.png', 'device1')
        self.assertTrue(result)

    @patch('android.adb_utils.AdbUtils.shell')
    def test_start_app(self, mock_shell):
        """测试start_app方法"""
        # 设置模拟对象的行为
        mock_shell.return_value = (0, 'Success', '')

        # 执行测试 - 无活动名称，无设备参数
        result = AdbUtils.start_app('com.example.app')
        mock_shell.assert_called_with('monkey -p com.example.app -c android.intent.category.LAUNCHER 1', None)
        self.assertTrue(result)

        # 执行测试 - 有活动名称，有设备参数
        result = AdbUtils.start_app('com.example.app', 'com.example.app.MainActivity', 'device1')
        mock_shell.assert_called_with('am start -n com.example.app/com.example.app.MainActivity', 'device1')
        self.assertTrue(result)

    @patch('android.adb_utils.AdbUtils.shell')
    def test_stop_app(self, mock_shell):
        """测试stop_app方法"""
        # 设置模拟对象的行为
        mock_shell.return_value = (0, 'Success', '')

        # 执行测试 - 无设备参数
        result = AdbUtils.stop_app('com.example.app')
        mock_shell.assert_called_with('am force-stop com.example.app', None)
        self.assertTrue(result)

        # 执行测试 - 有设备参数
        result = AdbUtils.stop_app('com.example.app', 'device1')
        mock_shell.assert_called_with('am force-stop com.example.app', 'device1')
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()