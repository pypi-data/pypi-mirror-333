"""Logcat工具类

提供Logcat日志获取与解析功能。
"""

import re
import subprocess
import threading
import time
from typing import List, Dict, Optional, Union, Tuple, Callable

from .adb_utils import AdbUtils


class LogcatUtils:
    """Logcat工具类，提供日志获取与解析功能"""

    # 日志级别
    VERBOSE = 'V'
    DEBUG = 'D'
    INFO = 'I'
    WARNING = 'W'
    ERROR = 'E'
    FATAL = 'F'

    @staticmethod
    def clear(device: Optional[str] = None) -> bool:
        """清除日志缓冲区

        Args:
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 清除是否成功
        """
        code, _, _ = AdbUtils.shell('logcat -c', device)
        return code == 0

    @staticmethod
    def get_logs(filters: Optional[str] = None, level: str = VERBOSE,
                 limit: Optional[int] = None, device: Optional[str] = None) -> List[str]:
        """获取日志

        Args:
            filters: 日志过滤器，例如 'ActivityManager:I *:S'
            level: 日志级别，默认为VERBOSE
            limit: 限制行数，如果为None则不限制
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            List[str]: 日志行列表
        """
        cmd = 'logcat -d'
        if filters:
            cmd += f' {filters}'
        else:
            cmd += f' *:{level}'

        if limit:
            cmd += f' -t {limit}'

        _, stdout, _ = AdbUtils.shell(cmd, device)
        return stdout.strip().split('\n')

    @staticmethod
    def parse_log_line(line: str) -> Dict[str, str]:
        """解析日志行

        Args:
            line: 日志行

        Returns:
            Dict[str, str]: 解析后的日志信息，包含date, time, pid, tid, level, tag, message等字段
        """
        # 匹配标准格式的日志行
        # 例如: 05-22 11:22:33.444 1234 5678 D TAG: Message
        pattern = r'^(\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}\.\d{3}) +(\d+) +(\d+) +([VDIWEF]) +([^:]+): (.*)$'
        match = re.match(pattern, line)

        if match:
            return {
                'date': match.group(1),
                'time': match.group(2),
                'pid': match.group(3),
                'tid': match.group(4),
                'level': match.group(5),
                'tag': match.group(6).strip(),
                'message': match.group(7)
            }
        return {'raw': line}

    @staticmethod
    def filter_logs_by_tag(logs: List[str], tag: str) -> List[str]:
        """按标签过滤日志

        Args:
            logs: 日志行列表
            tag: 标签

        Returns:
            List[str]: 过滤后的日志行列表
        """
        return [log for log in logs if f' {tag}: ' in log]

    @staticmethod
    def filter_logs_by_level(logs: List[str], level: str) -> List[str]:
        """按级别过滤日志

        Args:
            logs: 日志行列表
            level: 日志级别

        Returns:
            List[str]: 过滤后的日志行列表
        """
        pattern = f' {level} +[^:]+: '
        return [log for log in logs if re.search(pattern, log)]

    @staticmethod
    def filter_logs_by_keyword(logs: List[str], keyword: str) -> List[str]:
        """按关键词过滤日志

        Args:
            logs: 日志行列表
            keyword: 关键词

        Returns:
            List[str]: 过滤后的日志行列表
        """
        return [log for log in logs if keyword in log]

    @staticmethod
    def start_logcat(callback: Callable[[str], None], filters: Optional[str] = None,
                     level: str = VERBOSE, device: Optional[str] = None) -> subprocess.Popen:
        """启动日志监听

        Args:
            callback: 回调函数，接收日志行作为参数
            filters: 日志过滤器，例如 'ActivityManager:I *:S'
            level: 日志级别，默认为VERBOSE
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            subprocess.Popen: 进程对象，可用于停止监听
        """
        if device:
            cmd = f'adb -s {device} logcat'
        else:
            cmd = 'adb logcat'

        if filters:
            cmd += f' {filters}'
        else:
            cmd += f' *:{level}'

        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            bufsize=1,
            universal_newlines=True
        )

        def reader_thread():
            while True:
                # 检查process.stdout是否为None
                if process.stdout:
                    line = process.stdout.readline()
                else:
                    line = None
                if not line:
                    break
                callback(line.strip())

        threading.Thread(target=reader_thread, daemon=True).start()
        return process

    @staticmethod
    def stop_logcat(process: subprocess.Popen) -> None:
        """停止日志监听

        Args:
            process: 进程对象，由start_logcat返回
        """
        if process and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)

    @staticmethod
    def dump_logcat(save_path: str, filters: Optional[str] = None,
                   level: str = VERBOSE, device: Optional[str] = None) -> bool:
        """将日志保存到文件

        Args:
            save_path: 保存路径
            filters: 日志过滤器，例如 'ActivityManager:I *:S'
            level: 日志级别，默认为VERBOSE
            device: 设备序列号，如果为None则使用默认设备

        Returns:
            bool: 保存是否成功
        """
        logs = LogcatUtils.get_logs(filters, level, None, device)
        try:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(logs))
            return True
        except Exception:
            return False

    @staticmethod
    def monitor_logs(tag: str, callback: Callable[[Dict[str, str]], None],
                     timeout: Optional[int] = None, device: Optional[str] = None) -> None:
        """监控特定标签的日志

        Args:
            tag: 标签
            callback: 回调函数，接收解析后的日志信息作为参数
            timeout: 超时时间（秒），如果为None则一直监控
            device: 设备序列号，如果为None则使用默认设备
        """
        filters = f'{tag}:V *:S'
        stop_event = threading.Event()

        def log_callback(line: str):
            log_info = LogcatUtils.parse_log_line(line)
            if 'tag' in log_info and log_info['tag'] == tag:
                callback(log_info)

        process = LogcatUtils.start_logcat(log_callback, filters, LogcatUtils.VERBOSE, device)

        if timeout:
            def timeout_thread():
                time.sleep(timeout)
                stop_event.set()

            threading.Thread(target=timeout_thread, daemon=True).start()

        try:
            stop_event.wait()
        finally:
            LogcatUtils.stop_logcat(process)