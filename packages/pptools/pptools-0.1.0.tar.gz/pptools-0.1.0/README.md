# PPTools - Python工具集

一个全面的Python工具包，用于自动化测试和日常开发工作。PPTools旨在提供一套简单易用、功能强大的工具集，帮助开发者和测试人员提高工作效率。

## 功能特点

- **日期工具**: 日期格式转换、时间戳转换、日期计算、时区处理
- **Android工具**: ADB命令封装、Logcat日志获取与解析、性能数据采集、应用管理
- **文件操作**: 通用文件读写、YAML配置文件处理、XML解析与生成、Excel文件操作
- **网络工具**: HTTP请求封装、爬虫功能、代理设置、并发请求处理
- **数据库操作**: SQL数据库操作、NoSQL数据库支持、连接池管理、ORM封装
- **系统工具**: 进程管理、端口检测与管理、命令行执行、系统信息获取
- **装饰器**: 重试机制、超时控制、性能计时、日志记录
- **日志模块**: 多级别日志、日志轮转、自定义格式、多目标输出

## 安装

```bash
pip install pptools
```

## 快速开始

```python
from pptools.date import DateUtils
from pptools.file import FileUtils

# 日期工具示例
print(DateUtils.now_str())  # 获取当前时间字符串
print(DateUtils.timestamp_to_str(1609459200))  # 时间戳转字符串

# 文件工具示例
config = FileUtils.read_yaml('config.yaml')  # 读取YAML配置文件
FileUtils.write_excel('data.xlsx', data)  # 写入Excel文件
```

## 详细使用示例

### Android工具

```python
from pptools.android import AdbUtils, AppUtils, LogcatUtils, PerformanceUtils

# 获取设备列表
devices = AdbUtils.get_devices()
print(f"已连接设备: {devices}")

# 安装应用
AppUtils.install_app("path/to/app.apk")

# 获取已安装应用列表
apps = AppUtils.get_installed_apps()
print(f"已安装应用数量: {len(apps)}")

# 获取应用性能数据
memory = PerformanceUtils.get_memory_usage("com.example.app")
print(f"内存使用: {memory['total']} KB")

# 获取日志
LogcatUtils.clear()
logs = LogcatUtils.get_logs(filters="ActivityManager:I *:S", limit=100)
for log in logs:
    print(log)
```

### 日期工具

```python
from pptools.date import DateUtils

# 获取当前时间
now = DateUtils.now_str()
print(f"当前时间: {now}")

# 时间戳转换
timestamp = 1609459200
date_str = DateUtils.timestamp_to_str(timestamp)
print(f"时间戳 {timestamp} 对应的时间: {date_str}")

# 日期计算
tomorrow = DateUtils.add_days(DateUtils.now(), 1)
print(f"明天: {DateUtils.datetime_to_str(tomorrow)}")

# 日期比较
date1 = DateUtils.str_to_datetime("2023-01-01")
date2 = DateUtils.str_to_datetime("2023-01-15")
days = DateUtils.days_between(date1, date2)
print(f"两个日期相差 {days} 天")
```

### 文件操作

```python
from pptools.file import FileUtils

# 读写文本文件
FileUtils.write_text("example.txt", "Hello, World!")
content = FileUtils.read_text("example.txt")
print(f"文件内容: {content}")

# 读写JSON文件
data = {"name": "PPTools", "version": "0.1.0"}
FileUtils.write_json("config.json", data)
config = FileUtils.read_json("config.json")
print(f"配置: {config}")

# 读写YAML文件
yaml_data = {"settings": {"debug": True, "timeout": 30}}
FileUtils.write_yaml("config.yaml", yaml_data)
yaml_config = FileUtils.read_yaml("config.yaml")
print(f"YAML配置: {yaml_config}")

# 读写Excel文件
import pandas as pd
df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
FileUtils.write_excel("data.xlsx", df)
excel_data = FileUtils.read_excel("data.xlsx")
print(excel_data)
```

### 网络工具

```python
from pptools.network import HttpUtils

# 发送GET请求
response = HttpUtils.get("https://api.example.com/data")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.text}")

# 发送POST请求
data = {"username": "test", "password": "password"}
response = HttpUtils.post("https://api.example.com/login", json_data=data)
print(f"登录结果: {response.json()}")

# 下载文件
HttpUtils.download_file("https://example.com/file.zip", "downloaded_file.zip")

# 并发请求
urls = ["https://api.example.com/1", "https://api.example.com/2", "https://api.example.com/3"]
responses = HttpUtils.concurrent_get(urls, max_workers=3)
for url, response in zip(urls, responses):
    print(f"URL: {url}, 状态码: {response.status_code}")
```

### 数据库操作

```python
from pptools.database import DbUtils

# SQLite操作
conn = DbUtils.sqlite_connect("example.db")
DbUtils.sqlite_execute(conn, "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
DbUtils.sqlite_execute(conn, "INSERT INTO users (name, age) VALUES (?, ?)", ("张三", 30))
users = DbUtils.sqlite_query(conn, "SELECT * FROM users")
print(f"用户列表: {users}")

# MongoDB操作
mongo_db = DbUtils.mongodb_connect("mongodb://localhost:27017", "example")
user_id = DbUtils.mongodb_insert(mongo_db, "users", {"name": "李四", "age": 25})
users = DbUtils.mongodb_find(mongo_db, "users", {"age": {"$gt": 20}})
print(f"MongoDB用户列表: {users}")

# Redis操作
redis_conn = DbUtils.redis_connect()
DbUtils.redis_set(redis_conn, "user:1", "张三")
name = DbUtils.redis_get(redis_conn, "user:1")
print(f"Redis中的用户名: {name}")
```

### 系统工具

```python
from pptools.system import SystemUtils

# 获取系统信息
os_info = SystemUtils.get_os_info()
print(f"操作系统: {os_info['system']} {os_info['release']}")

# 执行命令
code, stdout, stderr = SystemUtils.run_command("echo Hello, World!")
print(f"命令输出: {stdout}")

# 查找可用端口
port = SystemUtils.find_free_port(start_port=8000)
print(f"可用端口: {port}")

# 获取系统资源使用情况
resources = SystemUtils.get_system_resources()
print(f"CPU使用率: {resources['cpu_percent']}%")
print(f"内存使用: {resources['memory']['used_gb']} GB / {resources['memory']['total_gb']} GB")
```

### 装饰器

```python
from pptools.decorator import DecoratorUtils
import logging

# 重试装饰器
@DecoratorUtils.retry(max_attempts=3, delay=1, exceptions=(ConnectionError,))
def fetch_data():
    # 模拟可能失败的网络请求
    import random
    if random.random() < 0.7:
        raise ConnectionError("连接失败")
    return "数据获取成功"

# 性能计时装饰器
@DecoratorUtils.timer()
def process_data():
    import time
    time.sleep(1.5)  # 模拟耗时操作
    return "处理完成"

# 日志装饰器
logger = logging.getLogger("example")
@DecoratorUtils.log(logger=logger)
def calculate(a, b):
    return a + b

# 缓存装饰器
@DecoratorUtils.cache()
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试装饰器
print(fetch_data())
print(process_data())
print(calculate(10, 20))
print(fibonacci(30))  # 使用缓存会大大提高性能
```

### 日志工具

```python
from pptools.log import LogUtils

# 创建基本日志记录器
logger = LogUtils.get_logger("example", level="debug")
logger.debug("这是一条调试日志")
logger.info("这是一条信息日志")
logger.warning("这是一条警告日志")

# 添加文件处理器
LogUtils.add_file_handler(logger, "logs/app.log", level="info")
logger.info("这条日志会同时输出到控制台和文件")

# 添加时间轮转文件处理器
LogUtils.add_time_rotating_handler(logger, "logs/app_daily.log", when="D")
logger.info("这条日志会输出到按天轮转的日志文件")

# 创建自定义日志记录器
config = {
    "level": "info",
    "console": True,
    "file": {
        "path": "logs/custom.log",
        "level": "warning",
        "max_bytes": 5 * 1024 * 1024,  # 5MB
        "backup_count": 3
    },
    "time_file": {
        "path": "logs/custom_daily.log",
        "when": "midnight",
        "backup_count": 7
    }
}
custom_logger = LogUtils.create_custom_logger("custom", config)
custom_logger.info("这是一条自定义日志")
```

## 上传到PyPI的步骤

如果您想将此包上传到PyPI，请按照以下步骤操作：

### 1. 准备必要文件

确保您的项目结构包含以下文件：

- `setup.py`: 包含包的元数据和依赖信息
- `pyproject.toml`: 指定构建系统要求
- `README.md`: 项目说明文档
- `LICENSE`: 许可证文件

### 2. 更新版本号

在 `pptools/__init__.py` 中更新版本号：

```python
__version__ = '0.1.0'  # 更改为您要发布的版本
```

### 3. 更新setup.py

确保 `setup.py` 中的信息是最新的，特别是：

```python
setup(
    name="pptools",
    version="0.1.0",  # 与__init__.py中的版本一致
    author="Your Name",
    author_email="your.email@example.com",
    description="一个全面的Python工具包，用于自动化测试和日常开发工作",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://gitee.com/dyliujun/pptools.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "pyyaml",
        "pandas",
        "openpyxl",
        "psutil",
        "adbutils",
    ],
    extras_require={
        "database": ["pymongo", "pymysql", "redis"],
        "dev": ["pytest", "black", "isort", "mypy", "flake8", "build", "twine"]
    }
)
```

### 4. 安装构建和上传工具

```bash
pip install build twine
```

### 5. 构建分发包

```bash
python -m build
```

这将在 `dist/` 目录下创建源代码分发包（.tar.gz）和轮子分发包（.whl）。

### 6. 上传到测试PyPI（