import os
import unittest
from unittest.mock import patch, MagicMock
from android.adb_utils import AdbUtils


class TestAdbUtilsExtended(unittest.TestCase):
    """AdbUtils类的扩展测试"""

    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_push(self, mock_run_cmd):
        """测试push方法"""
        # 设置模拟对象的行为
        mock_run_cmd.return_value = (0, 'Success', '')

        # 模拟文件存在
        with patch('android.adb_utils.os.path.exists', return_value=True):
            # 执行测试 - 无设备参数
            result = AdbUtils.push('/local/path', '/remote/path')
            mock_run_cmd.assert_called_with('adb push "/local/path" "/remote/path"', 60)
            self.assertTrue(result)

            # 执行测试 - 有设备参数
            result = AdbUtils.push('/local/path', '/remote/path', 'device1')
            mock_run_cmd.assert_called_with('adb -s device1 push "/local/path" "/remote/path"', 60)
            self.assertTrue(result)

        # 模拟文件不存在
        with patch('android.adb_utils.os.path.exists', return_value=False):
            result = AdbUtils.push('/local/path', '/remote/path')
            self.assertFalse(result)

    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_pull(self, mock_run_cmd):
        """测试pull方法"""
        # 设置模拟对象的行为
        mock_run_cmd.return_value = (0, 'Success', '')

        # 执行测试 - 无设备参数
        result = AdbUtils.pull('/remote/path', '/local/path')
        mock_run_cmd.assert_called_with('adb pull "/remote/path" "/local/path"', 60)
        self.assertTrue(result)

        # 执行测试 - 有设备参数
        result = AdbUtils.pull('/remote/path', '/local/path', 'device1')
        mock_run_cmd.assert_called_with('adb -s device1 pull "/remote/path" "/local/path"', 60)
        self.assertTrue(result)

    @patch('android.adb_utils.AdbUtils.shell')
    def test_get_prop(self, mock_shell):
        """测试get_prop方法"""
        # 设置模拟对象的行为
        mock_shell.return_value = (0, 'property_value', '')

        # 执行测试 - 无设备参数
        result = AdbUtils.get_prop('property_name')
        mock_shell.assert_called_with('getprop property_name', None)
        self.assertEqual(result, 'property_value')

        # 执行测试 - 有设备参数
        result = AdbUtils.get_prop('property_name', 'device1')
        mock_shell.assert_called_with('getprop property_name', 'device1')
        self.assertEqual(result, 'property_value')

    @patch('android.adb_utils.AdbUtils.get_prop')
    @patch('android.adb_utils.AdbUtils.get_devices')
    def test_get_device_info(self, mock_get_devices, mock_get_prop):
        """测试get_device_info方法"""
        # 设置模拟对象的行为
        mock_get_prop.side_effect = lambda prop, device=None: {
            'ro.product.brand': 'TestBrand',
            'ro.product.model': 'TestModel',
            'ro.build.version.release': '11',
            'ro.build.version.sdk': '30'
        }[prop]
        mock_get_devices.return_value = ['device1']

        # 执行测试 - 无设备参数
        result = AdbUtils.get_device_info()
        self.assertEqual(result['brand'], 'TestBrand')
        self.assertEqual(result['model'], 'TestModel')
        self.assertEqual(result['android_version'], '11')
        self.assertEqual(result['sdk_version'], '30')
        self.assertEqual(result['serial'], 'device1')

        # 执行测试 - 有设备参数
        result = AdbUtils.get_device_info('device2')
        self.assertEqual(result['serial'], 'device2')

    @patch('android.adb_utils.AdbUtils.shell')
    def test_is_screen_on(self, mock_shell):
        """测试is_screen_on方法"""
        # 设置模拟对象的行为 - 屏幕点亮
        mock_shell.return_value = (0, 'Display Power: state=ON', '')
        result = AdbUtils.is_screen_on()
        self.assertTrue(result)

        # 设置模拟对象的行为 - 屏幕关闭
        mock_shell.return_value = (0, 'Display Power: state=OFF', '')
        result = AdbUtils.is_screen_on()
        self.assertFalse(result)

    @patch('android.adb_utils.AdbUtils.is_screen_on')
    @patch('android.adb_utils.AdbUtils.shell')
    def test_screen_on(self, mock_shell, mock_is_screen_on):
        """测试screen_on方法"""
        # 设置模拟对象的行为 - 屏幕已点亮
        mock_is_screen_on.return_value = True
        AdbUtils.screen_on()
        mock_shell.assert_not_called()

        # 设置模拟对象的行为 - 屏幕未点亮
        mock_is_screen_on.return_value = False
        mock_shell.reset_mock()
        AdbUtils.screen_on()
        mock_shell.assert_called_with('input keyevent 26', None)

    @patch('android.adb_utils.AdbUtils.is_screen_on')
    @patch('android.adb_utils.AdbUtils.shell')
    def test_screen_off(self, mock_shell, mock_is_screen_on):
        """测试screen_off方法"""
        # 设置模拟对象的行为 - 屏幕已关闭
        mock_is_screen_on.return_value = False
        AdbUtils.screen_off()
        mock_shell.assert_not_called()

        # 设置模拟对象的行为 - 屏幕未关闭
        mock_is_screen_on.return_value = True
        mock_shell.reset_mock()
        AdbUtils.screen_off()
        mock_shell.assert_called_with('input keyevent 26', None)


if __name__ == '__main__':
    unittest.main()