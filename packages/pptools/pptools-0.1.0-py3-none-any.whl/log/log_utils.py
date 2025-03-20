"""日志工具类

提供多级别日志、日志轮转、自定义格式、多目标输出等功能。
"""

import os
import logging
import logging.handlers
from typing import Dict, List, Optional, Union


class LogUtils:
    """日志工具类，提供各种日志操作的静态方法"""

    # 日志级别映射
    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    @staticmethod
    def get_logger(name: str, level: Union[str, int] = 'info') -> logging.Logger:
        """获取日志记录器

        Args:
            name: 日志记录器名称
            level: 日志级别，可以是字符串('debug', 'info', 'warning', 'error', 'critical')或整数

        Returns:
            logging.Logger: 日志记录器
        """
        logger = logging.getLogger(name)
        
        # 设置日志级别
        if isinstance(level, str):
            level = LogUtils.LEVELS.get(level.lower(), logging.INFO)
        logger.setLevel(level)
        
        # 如果没有处理器，添加一个控制台处理器
        if not logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(console_handler)
        
        return logger

    @staticmethod
    def add_file_handler(logger: logging.Logger, file_path: str, level: Union[str, int] = 'info',
                         max_bytes: int = 10485760, backup_count: int = 5,
                         encoding: str = 'utf-8', formatter: Optional[str] = None) -> logging.Logger:
        """添加文件处理器

        Args:
            logger: 日志记录器
            file_path: 日志文件路径
            level: 日志级别，可以是字符串('debug', 'info', 'warning', 'error', 'critical')或整数
            max_bytes: 单个日志文件最大字节数，默认为10MB
            backup_count: 备份文件数量，默认为5
            encoding: 文件编码，默认为utf-8
            formatter: 日志格式字符串，如果为None则使用默认格式

        Returns:
            logging.Logger: 更新后的日志记录器
        """
        # 确保日志目录存在
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # 设置日志级别
        if isinstance(level, str):
            level = LogUtils.LEVELS.get(level.lower(), logging.INFO)
        
        # 创建文件处理器
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=encoding
        )
        file_handler.setLevel(level)
        
        # 设置格式化器
        if formatter is None:
            formatter = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        file_handler.setFormatter(logging.Formatter(formatter))
        
        # 添加处理器
        logger.addHandler(file_handler)
        
        return logger

    @staticmethod
    def add_time_rotating_handler(logger: logging.Logger, file_path: str, level: Union[str, int] = 'info',
                                 when: str = 'D', interval: int = 1, backup_count: int = 30,
                                 encoding: str = 'utf-8', formatter: Optional[str] = None) -> logging.Logger:
        """添加时间轮转文件处理器

        Args:
            logger: 日志记录器
            file_path: 日志文件路径
            level: 日志级别，可以是字符串('debug', 'info', 'warning', 'error', 'critical')或整数
            when: 轮转时间单位，'S'秒, 'M'分钟, 'H'小时, 'D'天, 'W'星期, 'midnight'午夜
            interval: 轮转时间间隔，默认为1
            backup_count: 备份文件数量，默认为30
            encoding: 文件编码，默认为utf-8
            formatter: 日志格式字符串，如果为None则使用默认格式

        Returns:
            logging.Logger: 更新后的日志记录器
        """
        # 确保日志目录存在
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        
        # 设置日志级别
        if isinstance(level, str):
            level = LogUtils.LEVELS.get(level.lower(), logging.INFO)
        
        # 创建时间轮转文件处理器
        time_handler = logging.handlers.TimedRotatingFileHandler(
            file_path,
            when=when,
            interval=interval,
            backupCount=backup_count,
            encoding=encoding
        )
        time_handler.setLevel(level)
        
        # 设置格式化器
        if formatter is None:
            formatter = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        time_handler.setFormatter(logging.Formatter(formatter))
        
        # 添加处理器
        logger.addHandler(time_handler)
        
        return logger

    @staticmethod
    def set_log_level(logger: logging.Logger, level: Union[str, int]) -> None:
        """设置日志级别

        Args:
            logger: 日志记录器
            level: 日志级别，可以是字符串('debug', 'info', 'warning', 'error', 'critical')或整数
        """
        if isinstance(level, str):
            level = LogUtils.LEVELS.get(level.lower(), logging.INFO)
        logger.setLevel(level)

    @staticmethod
    def create_custom_logger(name: str, config: Dict) -> logging.Logger:
        """创建自定义日志记录器

        Args:
            name: 日志记录器名称
            config: 配置字典，包含以下可选字段：
                - level: 日志级别
                - console: 是否输出到控制台
                - file: 文件输出配置，包含path, level, max_bytes, backup_count等字段
                - time_file: 时间轮转文件配置，包含path, level, when, interval, backup_count等字段

        Returns:
            logging.Logger: 自定义日志记录器
        """
        # 创建日志记录器
        logger = logging.getLogger(name)
        logger.setLevel(LogUtils.LEVELS.get(config.get('level', 'info').lower(), logging.INFO))
        
        # 清除现有处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 添加控制台处理器
        if config.get('console', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter(
                config.get('console_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            ))
            logger.addHandler(console_handler)
        
        # 添加文件处理器
        file_config = config.get('file')
        if file_config and 'path' in file_config:
            LogUtils.add_file_handler(
                logger,
                file_config['path'],
                file_config.get('level', 'info'),
                file_config.get('max_bytes', 10485760),
                file_config.get('backup_count', 5),
                file_config.get('encoding', 'utf-8'),
                file_config.get('format')
            )
        
        # 添加时间轮转文件处理器
        time_file_config = config.get('time_file')
        if time_file_config and 'path' in time_file_config:
            LogUtils.add_time_rotating_handler(
                logger,
                time_file_config['path'],
                time_file_config.get('level', 'info'),
                time_file_config.get('when', 'D'),
                time_file_config.get('interval', 1),
                time_file_config.get('backup_count', 30),
                time_file_config.get('encoding', 'utf-8'),
                time_file_config.get('format')
            )
        
        return logger