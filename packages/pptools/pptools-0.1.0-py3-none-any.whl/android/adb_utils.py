"""ADB工具类

提供ADB命令的封装，方便与Android设备进行交互。
"""

import os
import re
import subprocess
from typing import List, Dict, Optional, Union, Tuple


class AdbUtils:
    """ADB工具类，提供ADB命令的封装"""

    @staticmethod
    def run_cmd(cmd: str, timeout: int = 30) -> Tuple[int, str, str]:
        """执行ADB命令

        Args:
            cmd: ADB命令
            timeout: 超时时间，单位为秒

        Returns:
            Tuple[int, str, str]: 返回码、标准输出、标准错误
        """
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8'
        )
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            return process.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            process.kill()
            return -1, '', f'Command timed out after {timeout} seconds'

    @staticmethod
    def get_devices() -> List[str]:
        """获取已连接的设备列表

        Returns:
            List[str]: 设备序列号列表
        """
        _, stdout, _ = AdbUtils.run_cmd('adb devices')
        devices = []
        for line in stdout.strip().split('\n')[1:]:
            if line.strip():
                device = line.split('\t')[0].strip()
                if device:
                    devices.append(device)
        return devices

    @staticmethod
    def shell(cmd: str, device: Optional[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
        """执行ADB Shell命令

        Args:
            cmd: Shell命令
            device: 设备序列号，如果为None则使用默认设备
            timeout: 超时时间，单位为秒

        Returns:
            Tuple[int, str, str]: 返回码、标准输出、标准错误
        """
        if device:
            adb_cmd = f'adb -s {device} shell {cmd}'
        else:
            adb_cmd = f'adb shell {cmd}'
        return AdbUtils.run_cmd(adb_cmd, timeout)

    @staticmethod
    def install(apk_path: str, device: Optional[str] = None, timeout: int = 60) -> bool:
        """安装APK

        Args:
            apk_path: APK文件路径
            device: 设备序列号，如果为None则使用默认设备
            timeout: 超时时间，单位为秒

        Returns:
            bool: 安装是否成功
        """
        if not os.path.exists(apk_path):
            return False

        if device:
            cmd = f'adb -s {device} install -r "{apk_path}"'
        else:
            cmd = f'adb install -r "{apk_path}"'

        code, stdout, _ = AdbUtils.run_cmd(cmd, timeout)
        return code == 0 and ('Success' in stdout or '成功' in stdout)

    @staticmethod
    def uninstall(package_name: str, device: Optional[str] = None, timeout: int = 30) -> bool:
        """卸载应用

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备
            timeout: 超时时间，单位为秒

        Returns:
            bool: 卸载是否成功
        """
        if device:
            cmd = f'adb -s {device} uninstall {package_name}'
        else:
            cmd = f'adb uninstall {package_name}'

        code, stdout, _ = AdbUtils.run_cmd(cmd, timeout)
        return code == 0 and ('Success' in stdout or '成功' in stdout)

    @staticmethod
    def push(local_path: str, remote_path: str, device: Optional[str] = None, timeout: int = 60) -> bool:
        """推送文件到设备

        Args:
            local_path: 本地文件路径
            remote_path: 设备上的目标路径
            device: 设备序列号，如果为None则使用默认设备
            timeout: 超时时间，单位为秒

        Returns:
            bool: 推送是否成功
        """
        if not os.path.exists(local_path):
            return False

        if device:
            cmd = f'adb -s {device} push "{local_path}" "{remote_path}"'
        else:
            cmd = f'adb push "{local_path}" "{remote_path}"'

        code, _, _ = AdbUtils.run_cmd(cmd, timeout)
        return code == 0

    @staticmethod
    def pull(remote_path: str, local_path: str, device: Optional[str] = None, timeout: int = 60) -> bool:
        """从设备拉取文件

        Args:
            remote_path: 设备上的文件路径
            local_path: 本地目标路径
            device: 设备序列号，如果为None则使用默认设备
            timeout: 超时时间，单位为秒

        Returns:
            bool: 拉取是否成功
        """
        if device:
            cmd = f'adb -s {device} pull "{remote_path}" "{local_path}"'
        else:
            cmd = f'adb pull "{remote_path}" "{local_path}"'

        code, _, _ = AdbUtils.run_cmd(cmd, timeout)
        return code == 0

    @staticmethod
    def get_prop(prop: str, device: Optional[str] = None) -> str:
        """获取设备属性

        Args:
            prop: 属性名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            str: 属性值
        """
        _, stdout, _ = AdbUtils.shell(f'getprop {prop}', device)
        return stdout.strip()

    @staticmethod
    def get_device_info(device: Optional[str] = None) -> Dict[str, str]:
        """获取设备信息

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Dict[str, str]: 设备信息字典
        """
        info = {}
        info['brand'] = AdbUtils.get_prop('ro.product.brand', device)
        info['model'] = AdbUtils.get_prop('ro.product.model', device)
        info['android_version'] = AdbUtils.get_prop('ro.build.version.release', device)
        info['sdk_version'] = AdbUtils.get_prop('ro.build.version.sdk', device)
        info['serial'] = device if device else AdbUtils.get_devices()[0] if AdbUtils.get_devices() else ''
        return info

    @staticmethod
    def is_screen_on(device: Optional[str] = None) -> bool:
        """检查屏幕是否点亮

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 屏幕是否点亮
        """
        _, stdout, _ = AdbUtils.shell('dumpsys power | grep "Display Power"', device)
        return 'state=ON' in stdout or 'ON' in stdout

    @staticmethod
    def screen_on(device: Optional[str] = None) -> None:
        """点亮屏幕

        Args:
            device: 设备序列号，如果为None则使用默认设备
        """
        if not AdbUtils.is_screen_on(device):
            AdbUtils.shell('input keyevent 26', device)  # KEYCODE_POWER

    @staticmethod
    def screen_off(device: Optional[str] = None) -> None:
        """关闭屏幕

        Args:
            device: 设备序列号，如果为None则使用默认设备
        """
        if AdbUtils.is_screen_on(device):
            AdbUtils.shell('input keyevent 26', device)  # KEYCODE_POWER

    @staticmethod
    def unlock_screen(device: Optional[str] = None) -> None:
        """解锁屏幕

        Args:
            device: 设备序列号，如果为None则使用默认设备
        """
        AdbUtils.screen_on(device)
        AdbUtils.shell('input keyevent 82', device)  # KEYCODE_MENU

    @staticmethod
    def input_text(text: str, device: Optional[str] = None) -> None:
        """输入文本

        Args:
            text: 要输入的文本
            device: 设备序列号，如果为None则使用默认设备
        """
        AdbUtils.shell(f'input text "{text}"', device)

    @staticmethod
    def input_keyevent(keycode: int, device: Optional[str] = None) -> None:
        """输入按键事件

        Args:
            keycode: 按键代码
            device: 设备序列号，如果为None则使用默认设备
        """
        AdbUtils.shell(f'input keyevent {keycode}', device)

    @staticmethod
    def input_tap(x: int, y: int, device: Optional[str] = None) -> None:
        """模拟点击

        Args:
            x: 横坐标
            y: 纵坐标
            device: 设备序列号，如果为None则使用默认设备
        """
        AdbUtils.shell(f'input tap {x} {y}', device)

    @staticmethod
    def input_swipe(x1: int, y1: int, x2: int, y2: int, duration: int = 500, device: Optional[str] = None) -> None:
        """模拟滑动

        Args:
            x1: 起始点横坐标
            y1: 起始点纵坐标
            x2: 结束点横坐标
            y2: 结束点纵坐标
            duration: 持续时间，单位为毫秒
            device: 设备序列号，如果为None则使用默认设备
        """
        AdbUtils.shell(f'input swipe {x1} {y1} {x2} {y2} {duration}', device)

    @staticmethod
    def get_screen_resolution(device: Optional[str] = None) -> Tuple[int, int]:
        """获取屏幕分辨率

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Tuple[int, int]: 宽度和高度
        """
        _, stdout, _ = AdbUtils.shell('wm size', device)
        match = re.search(r'Physical size: (\d+)x(\d+)', stdout)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 0, 0

    @staticmethod
    def get_screen_density(device: Optional[str] = None) -> int:
        """获取屏幕密度

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            int: 屏幕密度
        """
        _, stdout, _ = AdbUtils.shell('wm density', device)
        match = re.search(r'Physical density: (\d+)', stdout)
        if match:
            return int(match.group(1))
        return 0

    @staticmethod
    def take_screenshot(save_path: str, device: Optional[str] = None) -> bool:
        """截图

        Args:
            save_path: 保存路径
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 截图是否成功
        """
        temp_path = '/sdcard/screenshot.png'
        AdbUtils.shell(f'screencap -p {temp_path}', device)
        result = AdbUtils.pull(temp_path, save_path, device)
        AdbUtils.shell(f'rm {temp_path}', device)
        return result

    @staticmethod
    def start_app(package_name: str, activity_name: Optional[str] = None, device: Optional[str] = None) -> bool:
        """启动应用

        Args:
            package_name: 应用包名
            activity_name: 活动名称，如果为None则启动主活动
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 启动是否成功
        """
        if activity_name:
            cmd = f'am start -n {package_name}/{activity_name}'
        else:
            cmd = f'monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
        code, _, _ = AdbUtils.shell(cmd, device)
        return code == 0

    @staticmethod
    def stop_app(package_name: str, device: Optional[str] = None) -> bool:
        """停止应用

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 停止是否成功
        """
        cmd = f'am force-stop {package_name}'
        code, _, _ = AdbUtils.shell(cmd, device)
        return code == 0