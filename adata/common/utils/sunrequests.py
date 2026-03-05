# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
"""

import threading
import time
from urllib.parse import urlparse

import requests


class SunProxy(object):
    _data = {}
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SunProxy, "_instance"):
            with SunProxy._instance_lock:
                if not hasattr(SunProxy, "_instance"):
                    SunProxy._instance = object.__new__(cls)
        return SunProxy._instance

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def delete(cls, key):
        if key in cls._data:
            del cls._data[key]


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self._rate_limit = {}
        self._rate_limit_default = 30  # 默认每分钟30次请求
        self._rate_limit_lock = threading.Lock()

    def set_rate_limit(self, domain, limit):
        """
        设置域名的请求频率限制
        :param domain: 域名
        :param limit: 每分钟请求次数限制
        """
        with self._rate_limit_lock:
            self._rate_limit[domain] = {
                'limit': limit,
                'count': 0,
                'reset_time': time.time() + 60
            }

    def _check_rate_limit(self, url):
        """
        检查请求频率限制
        :param url: 请求URL
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        wait_time = 0
        
        # 第一次获取锁，检查频率限制并计算等待时间
        with self._rate_limit_lock:
            now = time.time()
            if domain not in self._rate_limit:
                self._rate_limit[domain] = {
                    'limit': self._rate_limit_default,
                    'count': 0,
                    'reset_time': now + 60
                }
            
            rate_info = self._rate_limit[domain]
            
            # 检查是否需要重置计数
            if now >= rate_info['reset_time']:
                rate_info['count'] = 0
                rate_info['reset_time'] = now + 60
            
            # 检查是否超过限制
            if rate_info['count'] >= rate_info['limit']:
                # 计算需要等待的时间
                wait_time = rate_info['reset_time'] - now
        
        # 释放锁后执行等待，避免阻塞其他线程
        if wait_time > 0:
            time.sleep(wait_time)
        
        # 等待完成后，重新获取锁并重置计数和增加计数
        with self._rate_limit_lock:
            now = time.time()
            rate_info = self._rate_limit[domain]
            
            # 再次检查是否需要重置计数（可能在等待期间已经过期）
            if now >= rate_info['reset_time']:
                rate_info['count'] = 0
                rate_info['reset_time'] = now + 60
            else:
                # 重置计数（因为之前超过了限制）
                rate_info['count'] = 0
                rate_info['reset_time'] = now + 60
            
            # 增加计数
            rate_info['count'] += 1

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
        # 1. 检查频率限制
        self._check_rate_limit(url)
        # 2. 获取设置代理
        proxies = self.__get_proxies(proxies)
        # 3. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(retry_wait_time / 1000)
            if i == times - 1:
                return res
        return res

    def __get_proxies(self, proxies):
        """
        获取代理配置
        """
        if proxies is None:
            proxies = {}
        is_proxy = SunProxy.get('is_proxy')
        ip = SunProxy.get('ip')
        proxy_url = SunProxy.get('proxy_url')
        if not ip and is_proxy and proxy_url:
            # 对代理URL也应用频率限制
            self._check_rate_limit(proxy_url)
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
