# 测试频率限制的线程安全性
import time
import threading
from adata.common.utils.sunrequests import sun_requests

# 测试域名
TEST_DOMAIN = 'www.baidu.com'
# 每个线程的请求次数
REQUESTS_PER_THREAD = 5
# 线程数量
THREAD_COUNT = 3

# 设置较低的频率限制，以便测试
print(f"设置 {TEST_DOMAIN} 的频率限制为每分钟 5 次")
sun_requests.set_rate_limit(TEST_DOMAIN, 5)

# 线程函数
def test_thread(thread_id):
    print(f"线程 {thread_id} 开始执行")
    for i in range(REQUESTS_PER_THREAD):
        start_time = time.time()
        response = sun_requests.request('get', f'https://{TEST_DOMAIN}')
        end_time = time.time()
        print(f"线程 {thread_id} 请求 {i+1} 完成，状态码: {response.status_code}，耗时: {end_time - start_time:.2f}秒")
        time.sleep(0.1)  # 短暂休息，避免过于密集的请求
    print(f"线程 {thread_id} 执行完成")

# 启动多个线程
print("\n启动多线程测试...")
start_time = time.time()
threads = []

for i in range(THREAD_COUNT):
    t = threading.Thread(target=test_thread, args=(i+1,))
    threads.append(t)
    t.start()

# 等待所有线程完成
for t in threads:
    t.join()

end_time = time.time()
print(f"\n所有线程执行完成，总耗时: {end_time - start_time:.2f}秒")
print(f"总请求次数: {THREAD_COUNT * REQUESTS_PER_THREAD}")
print("如果所有请求都成功完成，且没有线程被长时间阻塞，说明线程安全修复成功。")
print("线程安全测试完成！")
