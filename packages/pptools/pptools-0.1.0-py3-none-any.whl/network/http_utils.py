"""HTTP工具类

提供HTTP请求封装、爬虫功能、代理设置、并发请求处理等功能。
"""

import json
import requests
from typing import Dict, List, Optional, Union, Any
from concurrent.futures import ThreadPoolExecutor


class HttpUtils:
    """HTTP工具类，提供各种HTTP请求操作的静态方法"""

    @staticmethod
    def get(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, 
            timeout: int = 30, verify: bool = True, proxies: Optional[Dict] = None) -> requests.Response:
        """发送GET请求

        Args:
            url: 请求URL
            params: 请求参数
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            requests.Response: 响应对象

        Raises:
            requests.RequestException: 如果请求失败
        """
        return requests.get(
            url, 
            params=params, 
            headers=headers, 
            timeout=timeout, 
            verify=verify, 
            proxies=proxies
        )

    @staticmethod
    def post(url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
             headers: Optional[Dict] = None, timeout: int = 30, verify: bool = True, 
             proxies: Optional[Dict] = None) -> requests.Response:
        """发送POST请求

        Args:
            url: 请求URL
            data: 表单数据
            json_data: JSON数据
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            requests.Response: 响应对象

        Raises:
            requests.RequestException: 如果请求失败
        """
        return requests.post(
            url, 
            data=data, 
            json=json_data, 
            headers=headers, 
            timeout=timeout, 
            verify=verify, 
            proxies=proxies
        )

    @staticmethod
    def put(url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
            headers: Optional[Dict] = None, timeout: int = 30, verify: bool = True, 
            proxies: Optional[Dict] = None) -> requests.Response:
        """发送PUT请求

        Args:
            url: 请求URL
            data: 表单数据
            json_data: JSON数据
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            requests.Response: 响应对象

        Raises:
            requests.RequestException: 如果请求失败
        """
        return requests.put(
            url, 
            data=data, 
            json=json_data, 
            headers=headers, 
            timeout=timeout, 
            verify=verify, 
            proxies=proxies
        )

    @staticmethod
    def delete(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, 
               timeout: int = 30, verify: bool = True, proxies: Optional[Dict] = None) -> requests.Response:
        """发送DELETE请求

        Args:
            url: 请求URL
            params: 请求参数
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            requests.Response: 响应对象

        Raises:
            requests.RequestException: 如果请求失败
        """
        return requests.delete(
            url, 
            params=params, 
            headers=headers, 
            timeout=timeout, 
            verify=verify, 
            proxies=proxies
        )

    @staticmethod
    def get_json(url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None, 
                 timeout: int = 30, verify: bool = True, proxies: Optional[Dict] = None) -> Dict:
        """发送GET请求并返回JSON数据

        Args:
            url: 请求URL
            params: 请求参数
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            Dict: JSON数据

        Raises:
            requests.RequestException: 如果请求失败
            json.JSONDecodeError: 如果响应不是有效的JSON
        """
        response = HttpUtils.get(url, params, headers, timeout, verify, proxies)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def post_json(url: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, 
                  headers: Optional[Dict] = None, timeout: int = 30, verify: bool = True, 
                  proxies: Optional[Dict] = None) -> Dict:
        """发送POST请求并返回JSON数据

        Args:
            url: 请求URL
            data: 表单数据
            json_data: JSON数据
            headers: 请求头
            timeout: 超时时间，单位为秒
            verify: 是否验证SSL证书
            proxies: 代理设置，格式为 {'http': 'http://user:pass@host:port', 'https': 'https://user:pass@host:port'}

        Returns:
            Dict: JSON数据

        Raises:
            requests.RequestException: 如果请求失败
            json.JSONDecodeError: 如果响应不是有效的JSON
        """
        response = HttpUtils.post(url, data, json_data, headers, timeout, verify, proxies)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def download_file(url: str, file_path: str, chunk_size: int = 8192, 
                      headers: Optional[Dict] = None, proxies: Optional[Dict] = None) -> bool:
        """下载文件

        Args:
            url: 文件URL
            file_path: 保存路径
            chunk_size: 块大小，单位为字节
            headers: 请求头
            proxies: 代理设置

        Returns:
            bool: 下载是否成功
        """
        try:
            import os
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            with requests.get(url, headers=headers, proxies=proxies, stream=True) as response:
                response.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
            return True
        except Exception:
            return False

    @staticmethod
    def concurrent_requests(urls: List[str], method: str = 'get', max_workers: int = 5, 
                           **kwargs) -> List[requests.Response]:
        """并发发送请求

        Args:
            urls: URL列表
            method: 请求方法，支持'get'、'post'、'put'、'delete'
            max_workers: 最大并发数
            **kwargs: 请求参数，与requests库参数一致

        Returns:
            List[requests.Response]: 响应对象列表
        """
        method_map = {
            'get': requests.get,
            'post': requests.post,
            'put': requests.put,
            'delete': requests.delete
        }
        request_method = method_map.get(method.lower(), requests.get)
        
        def fetch_url(url):
            try:
                return request_method(url, **kwargs)
            except Exception as e:
                return e
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            responses = list(executor.map(fetch_url, urls))
            # 过滤掉异常结果，只返回成功的Response对象
            return [r for r in responses if isinstance(r, requests.Response)]
