"""日期工具类

提供日期格式转换、时间戳转换、日期计算、时区处理等功能。
"""

import datetime
import time
from typing import Optional, Union, Tuple


class DateUtils:
    """日期工具类，提供各种日期操作的静态方法"""

    DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    @staticmethod
    def now() -> datetime.datetime:
        """获取当前时间的datetime对象

        Returns:
            datetime.datetime: 当前时间的datetime对象
        """
        return datetime.datetime.now()

    @staticmethod
    def now_str(fmt: str = DEFAULT_FORMAT) -> str:
        """获取当前时间的字符串表示

        Args:
            fmt: 日期格式，默认为'%Y-%m-%d %H:%M:%S'

        Returns:
            str: 当前时间的字符串表示
        """
        return DateUtils.now().strftime(fmt)

    @staticmethod
    def now_timestamp() -> int:
        """获取当前时间的时间戳（秒）

        Returns:
            int: 当前时间的时间戳（秒）
        """
        return int(time.time())

    @staticmethod
    def now_timestamp_ms() -> int:
        """获取当前时间的时间戳（毫秒）

        Returns:
            int: 当前时间的时间戳（毫秒）
        """
        return int(time.time() * 1000)

    @staticmethod
    def str_to_datetime(date_str: str, fmt: str = DEFAULT_FORMAT) -> datetime.datetime:
        """将日期字符串转换为datetime对象

        Args:
            date_str: 日期字符串
            fmt: 日期格式，默认为'%Y-%m-%d %H:%M:%S'

        Returns:
            datetime.datetime: 转换后的datetime对象

        Raises:
            ValueError: 如果日期字符串格式不正确
        """
        return datetime.datetime.strptime(date_str, fmt)

    @staticmethod
    def datetime_to_str(dt: datetime.datetime, fmt: str = DEFAULT_FORMAT) -> str:
        """将datetime对象转换为日期字符串

        Args:
            dt: datetime对象
            fmt: 日期格式，默认为'%Y-%m-%d %H:%M:%S'

        Returns:
            str: 转换后的日期字符串
        """
        return dt.strftime(fmt)

    @staticmethod
    def timestamp_to_datetime(timestamp: Union[int, float]) -> datetime.datetime:
        """将时间戳转换为datetime对象

        Args:
            timestamp: 时间戳（秒）

        Returns:
            datetime.datetime: 转换后的datetime对象
        """
        return datetime.datetime.fromtimestamp(timestamp)

    @staticmethod
    def timestamp_ms_to_datetime(timestamp_ms: Union[int, float]) -> datetime.datetime:
        """将毫秒时间戳转换为datetime对象

        Args:
            timestamp_ms: 时间戳（毫秒）

        Returns:
            datetime.datetime: 转换后的datetime对象
        """
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000)

    @staticmethod
    def datetime_to_timestamp(dt: datetime.datetime) -> int:
        """将datetime对象转换为时间戳（秒）

        Args:
            dt: datetime对象

        Returns:
            int: 转换后的时间戳（秒）
        """
        return int(dt.timestamp())

    @staticmethod
    def datetime_to_timestamp_ms(dt: datetime.datetime) -> int:
        """将datetime对象转换为时间戳（毫秒）

        Args:
            dt: datetime对象

        Returns:
            int: 转换后的时间戳（毫秒）
        """
        return int(dt.timestamp() * 1000)

    @staticmethod
    def str_to_timestamp(date_str: str, fmt: str = DEFAULT_FORMAT) -> int:
        """将日期字符串转换为时间戳（秒）

        Args:
            date_str: 日期字符串
            fmt: 日期格式，默认为'%Y-%m-%d %H:%M:%S'

        Returns:
            int: 转换后的时间戳（秒）

        Raises:
            ValueError: 如果日期字符串格式不正确
        """
        dt = DateUtils.str_to_datetime(date_str, fmt)
        return DateUtils.datetime_to_timestamp(dt)

    @staticmethod
    def timestamp_to_str(timestamp: Union[int, float], fmt: str = DEFAULT_FORMAT) -> str:
        """将时间戳转换为日期字符串

        Args:
            timestamp: 时间戳（秒）
            fmt: 日期格式，默认为'%Y-%m-%d %H:%M:%S'

        Returns:
            str: 转换后的日期字符串
        """
        dt = DateUtils.timestamp_to_datetime(timestamp)
        return DateUtils.datetime_to_str(dt, fmt)

    @staticmethod
    def add_days(dt: datetime.datetime, days: int) -> datetime.datetime:
        """在给定日期上增加或减少天数

        Args:
            dt: 原始datetime对象
            days: 要增加的天数，负数表示减少

        Returns:
            datetime.datetime: 增加或减少天数后的datetime对象
        """
        return dt + datetime.timedelta(days=days)

    @staticmethod
    def add_hours(dt: datetime.datetime, hours: int) -> datetime.datetime:
        """在给定日期上增加或减少小时数

        Args:
            dt: 原始datetime对象
            hours: 要增加的小时数，负数表示减少

        Returns:
            datetime.datetime: 增加或减少小时数后的datetime对象
        """
        return dt + datetime.timedelta(hours=hours)

    @staticmethod
    def add_minutes(dt: datetime.datetime, minutes: int) -> datetime.datetime:
        """在给定日期上增加或减少分钟数

        Args:
            dt: 原始datetime对象
            minutes: 要增加的分钟数，负数表示减少

        Returns:
            datetime.datetime: 增加或减少分钟数后的datetime对象
        """
        return dt + datetime.timedelta(minutes=minutes)

    @staticmethod
    def add_seconds(dt: datetime.datetime, seconds: int) -> datetime.datetime:
        """在给定日期上增加或减少秒数

        Args:
            dt: 原始datetime对象
            seconds: 要增加的秒数，负数表示减少

        Returns:
            datetime.datetime: 增加或减少秒数后的datetime对象
        """
        return dt + datetime.timedelta(seconds=seconds)

    @staticmethod
    def get_date_range(start_date: Union[str, datetime.datetime],
                       end_date: Union[str, datetime.datetime],
                       fmt: str = DATE_FORMAT) -> list:
        """获取两个日期之间的所有日期列表

        Args:
            start_date: 开始日期，可以是字符串或datetime对象
            end_date: 结束日期，可以是字符串或datetime对象
            fmt: 如果输入是字符串，则为日期格式；同时也是输出的日期格式

        Returns:
            list: 日期字符串列表

        Raises:
            ValueError: 如果日期字符串格式不正确
        """
        # 转换输入为datetime对象
        if isinstance(start_date, str):
            start_date = DateUtils.str_to_datetime(start_date, fmt)
        if isinstance(end_date, str):
            end_date = DateUtils.str_to_datetime(end_date, fmt)

        # 确保开始日期不晚于结束日期
        if start_date > end_date:
            start_date, end_date = end_date, start_date

        # 生成日期范围
        date_list = []
        current_date = start_date
        while current_date <= end_date:
            date_list.append(DateUtils.datetime_to_str(current_date, fmt))
            current_date = DateUtils.add_days(current_date, 1)

        return date_list

    @staticmethod
    def get_days_between(start_date: Union[str, datetime.datetime],
                         end_date: Union[str, datetime.datetime],
                         fmt: str = DATE_FORMAT) -> int:
        """计算两个日期之间的天数差

        Args:
            start_date: 开始日期，可以是字符串或datetime对象
            end_date: 结束日期，可以是字符串或datetime对象
            fmt: 如果输入是字符串，则为日期格式

        Returns:
            int: 天数差的绝对值

        Raises:
            ValueError: 如果日期字符串格式不正确
        """
        # 转换输入为datetime对象
        if isinstance(start_date, str):
            start_date = DateUtils.str_to_datetime(start_date, fmt)
        if isinstance(end_date, str):
            end_date = DateUtils.str_to_datetime(end_date, fmt)

        # 计算差值
        delta = end_date - start_date
        return abs(delta.days)

    @staticmethod
    def is_same_day(date1: Union[str, datetime.datetime, int, float],
                    date2: Union[str, datetime.datetime, int, float],
                    fmt: str = DEFAULT_FORMAT) -> bool:
        """判断两个日期是否是同一天

        Args:
            date1: 第一个日期，可以是字符串、datetime对象或时间戳
            date2: 第二个日期，可以是字符串、datetime对象或时间戳
            fmt: 如果输入是字符串，则为日期格式

        Returns:
            bool: 如果是同一天则返回True，否则返回False

        Raises:
            ValueError: 如果日期字符串格式不正确
        """
        # 转换为datetime对象
        dt1 = DateUtils._convert_to_datetime(date1, fmt)
        dt2 = DateUtils._convert_to_datetime(date2, fmt)

        # 比较年、月、日
        return (dt1.year == dt2.year and
                dt1.month == dt2.month and
                dt1.day == dt2.day)

    @staticmethod
    def _convert_to_datetime(date_input: Union[str, datetime.datetime, int, float],
                             fmt: str = DEFAULT_FORMAT) -> datetime.datetime:
        """将各种类型的日期输入转换为datetime对象

        Args:
            date_input: 日期输入，可以是字符串、datetime对象或时间戳
            fmt: 如果输入是字符串，则为日期格式

        Returns:
            datetime.datetime: 转换后的datetime对象

        Raises:
            ValueError: 如果日期字符串格式不正确或输入类型不支持
        """
        if isinstance(date_input, datetime.datetime):
            return date_input
        elif isinstance(date_input, str):
            return DateUtils.str_to_datetime(date_input, fmt)
        elif isinstance(date_input, (int, float)):
            # 判断是秒还是毫秒时间戳
            if date_input > 10000000000:  # 毫秒时间戳通常大于10位数
                return DateUtils.timestamp_ms_to_datetime(date_input)
            else:
                return DateUtils.timestamp_to_datetime(date_input)
        else:
            raise ValueError(f"不支持的日期输入类型: {type(date_input)}")