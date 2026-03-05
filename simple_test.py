# 简单测试频率限制功能
import time
from adata.common.utils.sunrequests import sun_requests

print("开始测试频率限制功能...")

# 测试默认频率限制
print("\n测试默认频率限制（每分钟30次）...")
start = time.time()

for i in range(5):
    response = sun_requests.request('get', 'https://www.baidu.com')
    print(f"请求 {i+1} 成功，状态码: {response.status_code}")
    time.sleep(0.5)

end = time.time()
print(f"5次请求耗时: {end - start:.2f}秒")

# 测试自定义频率限制
print("\n测试自定义频率限制（每分钟5次）...")
sun_requests.set_rate_limit('www.baidu.com', 5)

start = time.time()

for i in range(10):
    response = sun_requests.request('get', 'https://www.baidu.com')
    print(f"请求 {i+1} 成功，状态码: {response.status_code}")

end = time.time()
print(f"10次请求耗时: {end - start:.2f}秒")
print("测试完成！")
