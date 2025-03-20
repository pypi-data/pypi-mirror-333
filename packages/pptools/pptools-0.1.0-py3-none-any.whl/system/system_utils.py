"""系统工具类

提供进程管理、端口检测与管理、命令行执行、系统信息获取等功能。
"""

import os
import sys
import socket
import platform
import subprocess
import psutil
from typing import Dict, List, Optional, Tuple, Union

try:
    import psutil
    _has_psutil = True
except ImportError:
    _has_psutil = False


class SystemUtils:
    """系统工具类，提供各种系统操作的静态方法"""

    @staticmethod
    def get_os_info() -> Dict[str, str]:
        """获取操作系统信息

        Returns:
            Dict[str, str]: 操作系统信息，包含system(系统名称)、release(发行版本)、version(系统版本)等字段
        """
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'platform': platform.platform(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }

    @staticmethod
    def get_python_info() -> Dict[str, str]:
        """获取Python解释器信息

        Returns:
            Dict[str, str]: Python解释器信息，包含version(版本)、implementation(实现)等字段
        """
        return {
            'version': platform.python_version(),
            'implementation': platform.python_implementation(),
            'compiler': platform.python_compiler(),
            'build': platform.python_build()[1],
            'executable': sys.executable
        }

    @staticmethod
    def run_command(cmd: str, shell: bool = True, timeout: Optional[int] = None) -> Tuple[int, str, str]:
        """执行命令行命令

        Args:
            cmd: 要执行的命令
            shell: 是否使用shell执行，默认为True
            timeout: 超时时间（秒），默认为None（不超时）

        Returns:
            Tuple[int, str, str]: 返回码、标准输出、标准错误

        Raises:
            subprocess.TimeoutExpired: 如果命令执行超时
            subprocess.SubprocessError: 如果命令执行失败
        """
        process = subprocess.Popen(
            cmd,
            shell=shell,
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
    def is_port_in_use(port: int, host: str = '127.0.0.1') -> bool:
        """检查端口是否被占用

        Args:
            port: 端口号
            host: 主机地址，默认为127.0.0.1

        Returns:
            bool: 端口是否被占用
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return False
            except socket.error:
                return True

    @staticmethod
    def find_free_port(start_port: int = 8000, host: str = '127.0.0.1') -> int:
        """查找可用端口

        Args:
            start_port: 起始端口号，默认为8000
            host: 主机地址，默认为127.0.0.1

        Returns:
            int: 可用端口号
        """
        port = start_port
        while SystemUtils.is_port_in_use(port, host):
            port += 1
        return port

    @staticmethod
    def get_process_list() -> List[Dict[str, Union[int, str]]]:
        """获取进程列表

        Returns:
            List[Dict[str, Union[int, str]]]: 进程列表，每个进程包含pid(进程ID)、name(进程名)、status(状态)等字段

        Raises:
            ImportError: 如果未安装psutil
        """
        if not _has_psutil:
            raise ImportError("获取进程列表需要安装psutil库")

        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status', 'username', 'memory_info']):
            try:
                pinfo = proc.info
                pinfo['memory_mb'] = round(pinfo.get('memory_info', {}).get('rss', 0) / (1024 * 1024), 2)
                processes.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    @staticmethod
    def kill_process(pid: int) -> bool:
        """终止进程

        Args:
            pid: 进程ID

        Returns:
            bool: 是否成功终止进程

        Raises:
            ImportError: 如果未安装psutil
        """
        if not _has_psutil:
            raise ImportError("终止进程需要安装psutil库")

        try:
            process = psutil.Process(pid)
            process.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    @staticmethod
    def get_system_resources() -> Dict[str, Union[float, Dict]]:
        """获取系统资源使用情况

        Returns:
            Dict[str, Union[float, Dict]]: 系统资源使用情况，包含cpu_percent(CPU使用率)、memory(内存使用情况)、disk(磁盘使用情况)等字段

        Raises:
            ImportError: 如果未安装psutil
        """
        if not _has_psutil:
            raise ImportError("获取系统资源使用情况需要安装psutil库")

        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_info = {
            'total_gb': round(memory.total / (1024 ** 3), 2),
            'available_gb': round(memory.available / (1024 ** 3), 2),
            'used_gb': round(memory.used / (1024 ** 3), 2),
            'percent': memory.percent
        }

        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        disk_info = {
            'total_gb': round(disk.total / (1024 ** 3), 2),
            'used_gb': round(disk.used / (1024 ** 3), 2),
            'free_gb': round(disk.free / (1024 ** 3), 2),
            'percent': disk.percent
        }

        return {
            'cpu_percent': cpu_percent,
            'memory': memory_info,
            'disk': disk_info
        }

    @staticmethod
    def get_network_info() -> Dict[str, Dict]:
        """获取网络信息

        Returns:
            Dict[str, Dict]: 网络信息，包含各网络接口的地址信息

        Raises:
            ImportError: 如果未安装psutil
        """
        if not _has_psutil:
            raise ImportError("获取网络信息需要安装psutil库")

        # 将psutil.net_if_addrs()返回的snicaddr对象转换为字典格式
        net_if_addrs = psutil.net_if_addrs()
        result = {}
        for interface, addrs in net_if_addrs.items():
            result[interface] = {
                i: {
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast,
                    'ptp': addr.ptp,
                    'family': addr.family
                } for i, addr in enumerate(addrs)
            }
        return result

    @staticmethod
    def get_environment_variables() -> Dict[str, str]:
        """获取环境变量

        Returns:
            Dict[str, str]: 环境变量字典
        """
        return dict(os.environ)