import os
import unittest
from unittest.mock import patch, MagicMock
from android.adb_utils import AdbUtils


class TestAdbUtils(unittest.TestCase):
    """测试AdbUtils类的功能"""

    @patch('android.adb_utils.subprocess.Popen')
    def test_run_cmd(self, mock_popen):
        """测试run_cmd方法"""
        # 设置模拟对象的行为
        process_mock = MagicMock()
        process_mock.returncode = 0
        process_mock.communicate.return_value = ('output', 'error')
        mock_popen.return_value = process_mock

        # 执行测试
        code, stdout, stderr = AdbUtils.run_cmd('test command')

        # 验证结果
        mock_popen.assert_called_once_with(
            'test command',
            shell=True,
            stdout=-1,
            stderr=-1,
            encoding='utf-8'
        )
        self.assertEqual(code, 0)
        self.assertEqual(stdout, 'output')
        self.assertEqual(stderr, 'error')

    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_get_devices(self, mock_run_cmd):
        """测试get_devices方法"""
        # 设置模拟对象的行为
        mock_run_cmd.return_value = (0, 'List of devices attached\ndevice1\tdevice\ndevice2\tdevice\n', '')

        # 执行测试
        devices = AdbUtils.get_devices()

        # 验证结果
        mock_run_cmd.assert_called_once_with('adb devices')
        self.assertEqual(devices, ['device1', 'device2'])

    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_shell(self, mock_run_cmd):
        """测试shell方法"""
        # 设置模拟对象的行为
        mock_run_cmd.return_value = (0, 'output', 'error')

        # 执行测试 - 无设备参数
        result = AdbUtils.shell('test command')
        mock_run_cmd.assert_called_with('adb shell test command', 30)
        self.assertEqual(result, (0, 'output', 'error'))

        # 执行测试 - 有设备参数
        result = AdbUtils.shell('test command', 'device1')
        mock_run_cmd.assert_called_with('adb -s device1 shell test command', 30)
        self.assertEqual(result, (0, 'output', 'error'))

    @patch('android.adb_utils.os.path.exists')
    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_install(self, mock_run_cmd, mock_exists):
        """测试install方法"""
        # 设置模拟对象的行为
        mock_exists.return_value = True
        mock_run_cmd.return_value = (0, 'Success', '')

        # 执行测试 - 无设备参数
        result = AdbUtils.install('/path/to/app.apk')
        mock_run_cmd.assert_called_with('adb install -r "/path/to/app.apk"', 60)
        self.assertTrue(result)

        # 执行测试 - 有设备参数
        result = AdbUtils.install('/path/to/app.apk', 'device1')
        mock_run_cmd.assert_called_with('adb -s device1 install -r "/path/to/app.apk"', 60)
        self.assertTrue(result)

        # 测试文件不存在的情况
        mock_exists.return_value = False
        result = AdbUtils.install('/path/to/app.apk')
        self.assertFalse(result)

    @patch('android.adb_utils.AdbUtils.run_cmd')
    def test_uninstall(self, mock_run_cmd):
        """测试uninstall方法"""
        # 设置模拟对象的行为
        mock_run_cmd.return_value = (0, 'Success', '')

        # 执行测试 - 无设备参数
        result = AdbUtils.uninstall('com.example.app')
        mock_run_cmd.assert_called_with('adb uninstall com.example.app', 30)
        self.assertTrue(result)

        # 执行测试 - 有设备参数
        result = AdbUtils.uninstall('com.example.app', 'device1')
        mock_run_cmd.assert_called_with('adb -s device1 uninstall com.example.app', 30)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()