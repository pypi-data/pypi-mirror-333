"""应用工具类

提供应用安装、卸载、启动、停止等管理功能。
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Union

from .adb_utils import AdbUtils


class AppUtils:
    """应用工具类，提供应用管理功能"""

    @staticmethod
    def install_app(apk_path: str, device: Optional[str] = None) -> bool:
        """安装应用

        Args:
            apk_path: APK文件路径
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 安装是否成功
        """
        return AdbUtils.install(apk_path, device)

    @staticmethod
    def uninstall_app(package_name: str, device: Optional[str] = None) -> bool:
        """卸载应用

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 卸载是否成功
        """
        return AdbUtils.uninstall(package_name, device)

    @staticmethod
    def start_app(package_name: str, activity: Optional[str] = None, device: Optional[str] = None) -> bool:
        """启动应用

        Args:
            package_name: 应用包名
            activity: 启动的Activity，如果为None则启动主Activity
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 启动是否成功
        """
        if activity:
            cmd = f'am start -n {package_name}/{activity}'
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

    @staticmethod
    def clear_app_data(package_name: str, device: Optional[str] = None) -> bool:
        """清除应用数据

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 清除是否成功
        """
        cmd = f'pm clear {package_name}'
        code, _, _ = AdbUtils.shell(cmd, device)
        return code == 0

    @staticmethod
    def get_app_version(package_name: str, device: Optional[str] = None) -> str:
        """获取应用版本

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            str: 应用版本号
        """
        cmd = f'dumpsys package {package_name} | grep versionName'
        _, stdout, _ = AdbUtils.shell(cmd, device)
        match = re.search(r'versionName=([^\s]+)', stdout)
        if match:
            return match.group(1)
        return ''

    @staticmethod
    def get_app_pid(package_name: str, device: Optional[str] = None) -> int:
        """获取应用进程ID

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            int: 进程ID，如果应用未运行则返回0
        """
        cmd = f'ps -A | grep {package_name}'
        _, stdout, _ = AdbUtils.shell(cmd, device)
        if stdout.strip():
            try:
                return int(stdout.strip().split()[1])
            except (IndexError, ValueError):
                pass
        return 0

    @staticmethod
    def is_app_running(package_name: str, device: Optional[str] = None) -> bool:
        """检查应用是否正在运行

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 应用是否正在运行
        """
        return AppUtils.get_app_pid(package_name, device) > 0

    @staticmethod
    def get_installed_apps(device: Optional[str] = None) -> List[str]:
        """获取已安装的应用列表

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            List[str]: 应用包名列表
        """
        cmd = 'pm list packages'
        _, stdout, _ = AdbUtils.shell(cmd, device)
        packages = []
        for line in stdout.strip().split('\n'):
            if line.startswith('package:'):
                packages.append(line[8:].strip())
        return packages

    @staticmethod
    def get_app_info(package_name: str, device: Optional[str] = None) -> Dict[str, str]:
        """获取应用信息

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Dict[str, str]: 应用信息，包含version(版本)、first_install_time(首次安装时间)等字段
        """
        cmd = f'dumpsys package {package_name}'
        _, stdout, _ = AdbUtils.shell(cmd, device)
        
        info = {
            'package_name': package_name,
            'version': '',
            'version_code': '',
            'first_install_time': '',
            'last_update_time': '',
            'installer': ''
        }
        
        version_match = re.search(r'versionName=([^\s]+)', stdout)
        if version_match:
            info['version'] = version_match.group(1)
            
        version_code_match = re.search(r'versionCode=([\d]+)', stdout)
        if version_code_match:
            info['version_code'] = version_code_match.group(1)
            
        first_install_match = re.search(r'firstInstallTime=([^\s]+)', stdout)
        if first_install_match:
            info['first_install_time'] = first_install_match.group(1)
            
        last_update_match = re.search(r'lastUpdateTime=([^\s]+)', stdout)
        if last_update_match:
            info['last_update_time'] = last_update_match.group(1)
            
        installer_match = re.search(r'installerPackageName=([^\s]+)', stdout)
        if installer_match:
            info['installer'] = installer_match.group(1)
            
        return info

    @staticmethod
    def grant_permission(package_name: str, permission: str, device: Optional[str] = None) -> bool:
        """授予应用权限

        Args:
            package_name: 应用包名
            permission: 权限名称，例如 android.permission.CAMERA
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 授权是否成功
        """
        cmd = f'pm grant {package_name} {permission}'
        code, _, _ = AdbUtils.shell(cmd, device)
        return code == 0

    @staticmethod
    def revoke_permission(package_name: str, permission: str, device: Optional[str] = None) -> bool:
        """撤销应用权限

        Args:
            package_name: 应用包名
            permission: 权限名称，例如 android.permission.CAMERA
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 撤销是否成功
        """
        cmd = f'pm revoke {package_name} {permission}'
        code, _, _ = AdbUtils.shell(cmd, device)
        return code == 0