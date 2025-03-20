"""数据库工具类

提供SQL数据库操作、NoSQL数据库支持、连接池管理、ORM封装等功能。
"""

import sqlite3
import pymysql
import pymongo
import redis
from typing import Any, Dict, List, Optional, Union, Tuple

try:
    import pymysql
    _has_mysql = True
except ImportError:
    _has_mysql = False

try:
    import pymongo
    _has_mongodb = True
except ImportError:
    _has_mongodb = False

try:
    import redis
    _has_redis = True
except ImportError:
    _has_redis = False


class DbUtils:
    """数据库工具类，提供各种数据库操作的静态方法"""

    @staticmethod
    def sqlite_connect(db_path: str) -> sqlite3.Connection:
        """连接SQLite数据库

        Args:
            db_path: 数据库文件路径

        Returns:
            sqlite3.Connection: 数据库连接对象

        Raises:
            sqlite3.Error: 如果连接失败
        """
        return sqlite3.connect(db_path)

    @staticmethod
    def sqlite_execute(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> sqlite3.Cursor:
        """执行SQLite SQL语句

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params: SQL参数

        Returns:
            sqlite3.Cursor: 游标对象

        Raises:
            sqlite3.Error: 如果执行失败
        """
        if params:
            return conn.execute(sql, params)
        return conn.execute(sql)

    @staticmethod
    def sqlite_execute_many(conn: sqlite3.Connection, sql: str, params_list: List[Tuple]) -> sqlite3.Cursor:
        """执行SQLite批量SQL语句

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params_list: SQL参数列表

        Returns:
            sqlite3.Cursor: 游标对象

        Raises:
            sqlite3.Error: 如果执行失败
        """
        return conn.executemany(sql, params_list)

    @staticmethod
    def sqlite_query(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """执行SQLite查询语句

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params: SQL参数

        Returns:
            List[Tuple]: 查询结果

        Raises:
            sqlite3.Error: 如果查询失败
        """
        cursor = DbUtils.sqlite_execute(conn, sql, params)
        return cursor.fetchall()

    @staticmethod
    def sqlite_query_one(conn: sqlite3.Connection, sql: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        """执行SQLite查询语句，返回第一条结果

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params: SQL参数

        Returns:
            Optional[Tuple]: 查询结果，如果没有结果则返回None

        Raises:
            sqlite3.Error: 如果查询失败
        """
        cursor = DbUtils.sqlite_execute(conn, sql, params)
        return cursor.fetchone()

    @staticmethod
    def mysql_connect(host: str, user: str, password: str, database: str, port: int = 3306) -> Any:
        """连接MySQL数据库

        Args:
            host: 主机地址
            user: 用户名
            password: 密码
            database: 数据库名
            port: 端口号，默认为3306

        Returns:
            pymysql.Connection: 数据库连接对象

        Raises:
            ImportError: 如果未安装pymysql
            pymysql.Error: 如果连接失败
        """
        if not _has_mysql:
            raise ImportError("连接MySQL数据库需要安装pymysql库")
        return pymysql.connect(host=host, user=user, password=password, database=database, port=port)

    @staticmethod
    def mysql_execute(conn: Any, sql: str, params: Optional[Tuple] = None) -> Any:
        """执行MySQL SQL语句

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params: SQL参数

        Returns:
            pymysql.Cursor: 游标对象

        Raises:
            pymysql.Error: 如果执行失败
        """
        with conn.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            conn.commit()
            return cursor

    @staticmethod
    def mysql_query(conn: Any, sql: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """执行MySQL查询语句

        Args:
            conn: 数据库连接对象
            sql: SQL语句
            params: SQL参数

        Returns:
            List[Tuple]: 查询结果

        Raises:
            pymysql.Error: 如果查询失败
        """
        with conn.cursor() as cursor:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchall()

    @staticmethod
    def mongodb_connect(uri: str, database: str) -> Any:
        """连接MongoDB数据库

        Args:
            uri: MongoDB连接URI
            database: 数据库名

        Returns:
            pymongo.Database: 数据库对象

        Raises:
            ImportError: 如果未安装pymongo
            pymongo.errors.ConnectionError: 如果连接失败
        """
        if not _has_mongodb:
            raise ImportError("连接MongoDB数据库需要安装pymongo库")
        client = pymongo.MongoClient(uri)
        return client[database]

    @staticmethod
    def mongodb_insert(db: Any, collection: str, document: Dict) -> str:
        """插入MongoDB文档

        Args:
            db: 数据库对象
            collection: 集合名
            document: 文档数据

        Returns:
            str: 插入的文档ID

        Raises:
            pymongo.errors.PyMongoError: 如果插入失败
        """
        result = db[collection].insert_one(document)
        return str(result.inserted_id)

    @staticmethod
    def mongodb_find(db: Any, collection: str, query: Dict, projection: Optional[Dict] = None) -> List[Dict]:
        """查询MongoDB文档

        Args:
            db: 数据库对象
            collection: 集合名
            query: 查询条件
            projection: 投影条件，指定返回的字段

        Returns:
            List[Dict]: 查询结果

        Raises:
            pymongo.errors.PyMongoError: 如果查询失败
        """
        cursor = db[collection].find(query, projection)
        return list(cursor)

    @staticmethod
    def redis_connect(host: str = 'localhost', port: int = 6379, db: int = 0, password: Optional[str] = None) -> Any:
        """连接Redis数据库

        Args:
            host: 主机地址，默认为localhost
            port: 端口号，默认为6379
            db: 数据库索引，默认为0
            password: 密码，默认为None

        Returns:
            redis.Redis: Redis连接对象

        Raises:
            ImportError: 如果未安装redis
            redis.RedisError: 如果连接失败
        """
        if not _has_redis:
            raise ImportError("连接Redis数据库需要安装redis库")
        return redis.Redis(host=host, port=port, db=db, password=password)

    @staticmethod
    def redis_set(conn: Any, key: str, value: str, ex: Optional[int] = None) -> bool:
        """设置Redis键值

        Args:
            conn: Redis连接对象
            key: 键
            value: 值
            ex: 过期时间（秒），默认为None（不过期）

        Returns:
            bool: 设置是否成功

        Raises:
            redis.RedisError: 如果设置失败
        """
        return conn.set(key, value, ex=ex)

    @staticmethod
    def redis_get(conn: Any, key: str) -> Optional[str]:
        """获取Redis键值

        Args:
            conn: Redis连接对象
            key: 键

        Returns:
            Optional[str]: 值，如果键不存在则返回None

        Raises:
            redis.RedisError: 如果获取失败
        """
        value = conn.get(key)
        return value.decode('utf-8') if value else None