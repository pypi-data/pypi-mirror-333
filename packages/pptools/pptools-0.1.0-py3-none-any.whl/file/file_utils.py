"""文件工具类

提供通用文件读写、YAML配置文件处理、XML解析与生成、Excel文件操作等功能。
"""

import os
import json
import yaml
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Union

try:
    import pandas as pd
    import openpyxl
    _has_excel = True
except ImportError:
    _has_excel = False


class FileUtils:
    """文件工具类，提供各种文件操作的静态方法"""

    @staticmethod
    def read_text(file_path: str, encoding: str = 'utf-8') -> str:
        """读取文本文件

        Args:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8

        Returns:
            str: 文件内容

        Raises:
            FileNotFoundError: 如果文件不存在
            IOError: 如果读取文件时发生错误
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()

    @staticmethod
    def write_text(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """写入文本文件

        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码，默认为utf-8

        Returns:
            bool: 写入是否成功

        Raises:
            IOError: 如果写入文件时发生错误
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            return True
        except Exception:
            return False

    @staticmethod
    def read_json(file_path: str, encoding: str = 'utf-8') -> Dict:
        """读取JSON文件

        Args:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8

        Returns:
            Dict: JSON数据

        Raises:
            FileNotFoundError: 如果文件不存在
            json.JSONDecodeError: 如果JSON格式不正确
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)

    @staticmethod
    def write_json(file_path: str, data: Dict, encoding: str = 'utf-8', indent: int = 4) -> bool:
        """写入JSON文件

        Args:
            file_path: 文件路径
            data: JSON数据
            encoding: 文件编码，默认为utf-8
            indent: 缩进空格数，默认为4

        Returns:
            bool: 写入是否成功

        Raises:
            IOError: 如果写入文件时发生错误
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except Exception:
            return False

    @staticmethod
    def read_yaml(file_path: str, encoding: str = 'utf-8') -> Dict:
        """读取YAML文件

        Args:
            file_path: 文件路径
            encoding: 文件编码，默认为utf-8

        Returns:
            Dict: YAML数据

        Raises:
            FileNotFoundError: 如果文件不存在
            yaml.YAMLError: 如果YAML格式不正确
        """
        with open(file_path, 'r', encoding=encoding) as f:
            return yaml.safe_load(f)

    @staticmethod
    def write_yaml(file_path: str, data: Dict, encoding: str = 'utf-8') -> bool:
        """写入YAML文件

        Args:
            file_path: 文件路径
            data: YAML数据
            encoding: 文件编码，默认为utf-8

        Returns:
            bool: 写入是否成功

        Raises:
            IOError: 如果写入文件时发生错误
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding=encoding) as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
            return True
        except Exception:
            return False

    @staticmethod
    def read_xml(file_path: str) -> ET.Element:
        """读取XML文件

        Args:
            file_path: 文件路径

        Returns:
            ET.Element: XML根元素

        Raises:
            FileNotFoundError: 如果文件不存在
            ET.ParseError: 如果XML格式不正确
        """
        tree = ET.parse(file_path)
        return tree.getroot()

    @staticmethod
    def write_xml(file_path: str, root: ET.Element, encoding: str = 'utf-8') -> bool:
        """写入XML文件

        Args:
            file_path: 文件路径
            root: XML根元素
            encoding: 文件编码，默认为utf-8

        Returns:
            bool: 写入是否成功

        Raises:
            IOError: 如果写入文件时发生错误
        """
        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            tree = ET.ElementTree(root)
            tree.write(file_path, encoding=encoding, xml_declaration=True)
            return True
        except Exception:
            return False

    @staticmethod
    def read_excel(file_path: str, sheet_name: Optional[Union[str, int]] = 0) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """读取Excel文件

        Args:
            file_path: 文件路径
            sheet_name: 工作表名称或索引，默认为0（第一个工作表）
                        如果为None，则返回所有工作表的字典

        Returns:
            Union[pd.DataFrame, Dict[str, pd.DataFrame]]: Excel数据

        Raises:
            FileNotFoundError: 如果文件不存在
            ImportError: 如果未安装pandas或openpyxl
        """
        if not _has_excel:
            raise ImportError("读取Excel文件需要安装pandas和openpyxl库")
        return pd.read_excel(file_path, sheet_name=sheet_name)

    @staticmethod
    def write_excel(file_path: str, data: Union[pd.DataFrame, Dict[str, pd.DataFrame]], index: bool = False) -> bool:
        """写入Excel文件

        Args:
            file_path: 文件路径
            data: Excel数据，可以是DataFrame或者{sheet_name: DataFrame}字典
            index: 是否写入索引，默认为False

        Returns:
            bool: 写入是否成功

        Raises:
            ImportError: 如果未安装pandas或openpyxl
            IOError: 如果写入文件时发生错误
        """
        if not _has_excel:
            raise ImportError("写入Excel文件需要安装pandas和openpyxl库")

        try:
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            if isinstance(data, dict):
                with pd.ExcelWriter(file_path) as writer:
                    for sheet_name, df in data.items():
                        df.to_excel(writer, sheet_name=sheet_name, index=index)
            else:
                data.to_excel(file_path, index=index)
            return True
        except Exception:
            return False