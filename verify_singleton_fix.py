# 验证 SunProxy 单例模式修复
from adata.common.utils.sunrequests import SunProxy

print("验证 SunProxy 单例模式修复...")

# 创建两个 SunProxy 实例
proxy1 = SunProxy()
proxy2 = SunProxy()

# 检查是否是同一个实例
print(f"proxy1 和 proxy2 是否是同一个实例: {proxy1 is proxy2}")
print(f"proxy1 id: {id(proxy1)}")
print(f"proxy2 id: {id(proxy2)}")

# 测试设置和获取值
proxy1.set('test_key', 'test_value')
print(f"通过 proxy1 设置值，通过 proxy2 获取值: {proxy2.get('test_key')}")

# 测试删除值
proxy2.delete('test_key')
print(f"通过 proxy2 删除值，通过 proxy1 获取值: {proxy1.get('test_key')}")

print("单例模式验证完成！")
