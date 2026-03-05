# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""
import time
from adata.common.utils import requests

# 测试默认频率限制（每分钟30次）
def test_default_rate_limit():
    print("测试默认频率限制（每分钟30次）...")
    start_time = time.time()
    count = 0
    
    # 尝试在短时间内发送40次请求
    for i in range(40):
        try:
            # 使用同一个域名进行测试
            response = requests.request('get', 'https://www.baidu.com')
            count += 1
            print(f"请求 {count} 成功，状态码: {response.status_code}")
        except Exception as e:
            print(f"请求 {count+1} 失败: {e}")
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"测试完成，共发送 {count} 次请求，耗时 {elapsed:.2f} 秒")
    print(f"平均请求间隔: {elapsed/count:.2f} 秒")
    print()

# 测试自定义频率限制
def test_custom_rate_limit():
    print("测试自定义频率限制（每分钟5次）...")
    # 设置百度域名的频率限制为每分钟5次
    requests.set_rate_limit('www.baidu.com', 5)
    
    start_time = time.time()
    count = 0
    
    # 尝试在短时间内发送10次请求
    for i in range(10):
        try:
            response = requests.request('get', 'https://www.baidu.com')
            count += 1
            print(f"请求 {count} 成功，状态码: {response.status_code}")
        except Exception as e:
            print(f"请求 {count+1} 失败: {e}")
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"测试完成，共发送 {count} 次请求，耗时 {elapsed:.2f} 秒")
    print(f"平均请求间隔: {elapsed/count:.2f} 秒")
    print()

if __name__ == '__main__':
    test_default_rate_limit()
    test_custom_rate_limit()
