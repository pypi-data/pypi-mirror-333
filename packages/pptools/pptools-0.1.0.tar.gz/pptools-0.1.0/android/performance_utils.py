"""性能工具类

提供CPU、内存、电量等性能数据采集功能。
"""

import re
import time
from typing import Dict, List, Optional, Tuple, Union

from .adb_utils import AdbUtils


class PerformanceUtils:
    """性能工具类，提供性能数据采集功能"""

    @staticmethod
    def get_cpu_usage(package_name: str, device: Optional[str] = None) -> float:
        """获取应用CPU使用率

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            float: CPU使用率，取值范围0-100
        """
        # 获取应用进程ID
        _, stdout, _ = AdbUtils.shell(f'ps -A | grep {package_name}', device)
        if not stdout.strip():
            return 0.0

        pid = stdout.strip().split()[1]
        # 获取CPU使用率
        _, stdout, _ = AdbUtils.shell(f'top -p {pid} -n 1', device)
        for line in stdout.strip().split('\n'):
            if package_name in line:
                # 解析CPU使用率
                parts = line.strip().split()
                for i, part in enumerate(parts):
                    if '%' in part and i > 0:
                        return float(part.replace('%', ''))
        return 0.0

    @staticmethod
    def get_memory_usage(package_name: str, device: Optional[str] = None) -> Dict[str, int]:
        """获取应用内存使用情况

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Dict[str, int]: 内存使用情况，包含total(总内存)、native(原生内存)、dalvik(虚拟机内存)等字段，单位为KB
        """
        _, stdout, _ = AdbUtils.shell(f'dumpsys meminfo {package_name}', device)
        result = {
            'total': 0,
            'native': 0,
            'dalvik': 0,
            'code': 0,
            'stack': 0,
            'graphics': 0
        }

        # 解析内存信息
        total_pattern = r'TOTAL\s+([\d,]+)'
        native_pattern = r'Native Heap\s+([\d,]+)'
        dalvik_pattern = r'Dalvik Heap\s+([\d,]+)'
        code_pattern = r'Code\s+([\d,]+)'
        stack_pattern = r'Stack\s+([\d,]+)'
        graphics_pattern = r'Graphics\s+([\d,]+)'

        total_match = re.search(total_pattern, stdout)
        if total_match:
            result['total'] = int(total_match.group(1).replace(',', ''))

        native_match = re.search(native_pattern, stdout)
        if native_match:
            result['native'] = int(native_match.group(1).replace(',', ''))

        dalvik_match = re.search(dalvik_pattern, stdout)
        if dalvik_match:
            result['dalvik'] = int(dalvik_match.group(1).replace(',', ''))

        code_match = re.search(code_pattern, stdout)
        if code_match:
            result['code'] = int(code_match.group(1).replace(',', ''))

        stack_match = re.search(stack_pattern, stdout)
        if stack_match:
            result['stack'] = int(stack_match.group(1).replace(',', ''))

        graphics_match = re.search(graphics_pattern, stdout)
        if graphics_match:
            result['graphics'] = int(graphics_match.group(1).replace(',', ''))

        return result

    @staticmethod
    def get_battery_info(device: Optional[str] = None) -> Dict[str, Union[int, str]]:
        """获取电池信息

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Dict[str, Union[int, str]]: 电池信息，包含level(电量)、temperature(温度)、status(状态)等字段
        """
        _, stdout, _ = AdbUtils.shell('dumpsys battery', device)
        result = {
            'level': 0,
            'temperature': 0,
            'status': '',
            'health': '',
            'plugged': ''
        }

        # 解析电池信息
        for line in stdout.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'level':
                    result['level'] = int(value)
                elif key == 'temperature':
                    result['temperature'] = int(value) / 10.0  # 转换为摄氏度
                elif key == 'status':
                    status_map = {
                        '1': '未知',
                        '2': '充电中',
                        '3': '放电中',
                        '4': '未充电',
                        '5': '充满'
                    }
                    result['status'] = status_map.get(value, value)
                elif key == 'health':
                    health_map = {
                        '1': '未知',
                        '2': '良好',
                        '3': '过热',
                        '4': '损坏',
                        '5': '过压',
                        '6': '未知故障',
                        '7': '冷却'
                    }
                    result['health'] = health_map.get(value, value)
                elif key == 'plugged':
                    plugged_map = {
                        '0': '未插入',
                        '1': 'AC充电',
                        '2': 'USB充电',
                        '4': '无线充电'
                    }
                    result['plugged'] = plugged_map.get(value, value)

        return result

    @staticmethod
    def get_fps(package_name: str, duration: int = 5, device: Optional[str] = None) -> float:
        """获取应用帧率

        Args:
            package_name: 应用包名
            duration: 采集持续时间，单位为秒
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            float: 帧率
        """
        # 清除旧数据
        AdbUtils.shell('dumpsys gfxinfo {} reset'.format(package_name), device)
        
        # 等待采集数据
        time.sleep(duration)
        
        # 获取帧率数据
        _, stdout, _ = AdbUtils.shell('dumpsys gfxinfo {}'.format(package_name), device)
        
        # 解析帧率数据
        frame_count = 0
        jank_count = 0
        is_data_section = False
        
        for line in stdout.strip().split('\n'):
            if 'Janky frames' in line:
                match = re.search(r'(\d+) frames rendered', line)
                if match:
                    frame_count = int(match.group(1))
                match = re.search(r'(\d+) janky frames', line)
                if match:
                    jank_count = int(match.group(1))
                break
        
        if frame_count > 0:
            return frame_count / duration
        return 0.0

    @staticmethod
    def get_network_stats(package_name: str, device: Optional[str] = None) -> Dict[str, int]:
        """获取应用网络流量统计

        Args:
            package_name: 应用包名
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            Dict[str, int]: 网络流量统计，包含rx_bytes(接收字节数)、tx_bytes(发送字节数)等字段
        """
        # 获取应用的UID
        _, stdout, _ = AdbUtils.shell(f'dumpsys package {package_name} | grep userId=', device)
        uid_match = re.search(r'userId=(\d+)', stdout)
        if not uid_match:
            return {'rx_bytes': 0, 'tx_bytes': 0}
        
        uid = uid_match.group(1)
        
        # 获取网络流量统计
        _, stdout, _ = AdbUtils.shell(f'cat /proc/net/xt_qtaguid/stats | grep {uid}', device)
        
        rx_bytes = 0
        tx_bytes = 0
        
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 6:
                    rx_bytes += int(parts[5])
                    tx_bytes += int(parts[7])
        
        return {
            'rx_bytes': rx_bytes,
            'tx_bytes': tx_bytes
        }

    @staticmethod
    def monitor_performance(package_name: str, interval: int = 1, count: int = 10, 
                           device: Optional[str] = None) -> List[Dict[str, Union[float, Dict]]]:
        """监控应用性能

        Args:
            package_name: 应用包名
            interval: 采集间隔，单位为秒
            count: 采集次数
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            List[Dict[str, Union[float, Dict]]]: 性能数据列表，每个元素包含timestamp(时间戳)、cpu(CPU使用率)、memory(内存使用情况)等字段
        """
        result = []
        
        for _ in range(count):
            data = {
                'timestamp': time.time(),
                'cpu': PerformanceUtils.get_cpu_usage(package_name, device),
                'memory': PerformanceUtils.get_memory_usage(package_name, device),
                'battery': PerformanceUtils.get_battery_info(device)
            }
            result.append(data)
            
            if _ < count - 1:  # 最后一次采集后不需要等待
                time.sleep(interval)
        
        return result