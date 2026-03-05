# 测试频率限制修复
import time
from adata.common.utils.sunrequests import sun_requests

print("测试频率限制修复...")

# 设置一个较低的频率限制，以便快速测试
print("\n设置百度域名的频率限制为每分钟2次...")
sun_requests.set_rate_limit('www.baidu.com', 2)

print("\n开始测试请求...")
start_time = time.time()

# 发送3次请求，应该会在第3次请求时触发频率限制
for i in range(3):
    print(f"\n发送第 {i+1} 次请求...")
    request_start = time.time()
    response = sun_requests.request('get', 'https://www.baidu.com')
    request_end = time.time()
    print(f"请求 {i+1} 完成，状态码: {response.status_code}，耗时: {request_end - request_start:.2f}秒")

end_time = time.time()
print(f"\n测试完成，总耗时: {end_time - start_time:.2f}秒")
print("如果第3次请求耗时明显长于前两次，说明频率限制生效。")
print("修复验证完成！")
