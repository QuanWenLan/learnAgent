import time

# 获取当前时间戳（秒数，浮点数）
timestamp = time.time()
print(f"当前时间戳: {timestamp}")  # 例如: 1723792835.123456

# 获取当前时间的struct_time对象
local_time = time.localtime()
print(f"本地时间: {local_time}")
# 输出: time.struct_time(tm_year=2025, tm_mon=8, tm_mday=15, tm_hour=14, tm_min=20, tm_sec=35, tm_wday=3, tm_yday=227, tm_isdst=0)

# 获取UTC时间
utc_time = time.gmtime()
print(f"UTC时间: {utc_time}")

# 时间戳 → 可读字符串
# 将时间戳格式化为字符串
formatted_time = time.ctime(time.time())
print(f"格式化时间: {formatted_time}")  # Thu Aug 15 14:20:35 2025

# 自定义格式
formatted_custom = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"自定义格式: {formatted_custom}")  # 2025-08-15 14:20:35

# 字符串 → 时间戳
# 将字符串解析为struct_time
time_str = "2025-08-15 14:30:00"
struct_time = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
print(f"解析后的时间: {struct_time}")

# 转换为时间戳
timestamp_from_str = time.mktime(struct_time)
print(f"对应时间戳: {timestamp_from_str}")

# 各种时间格式
formats = {
    "日期": time.strftime("%Y-%m-%d", time.localtime()),
    "时间": time.strftime("%H:%M:%S", time.localtime()),
    "日期时间": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "周几": time.strftime("%A", time.localtime()),  # Thursday
    "简写周几": time.strftime("%a", time.localtime()),  # Thu
    "月份": time.strftime("%B", time.localtime()),  # August
    "简写月份": time.strftime("%b", time.localtime()),  # Aug
    "年中的第几天": time.strftime("%j", time.localtime()),  # 227
    "12小时制": time.strftime("%I:%M:%S %p", time.localtime()),  # 02:20:35 PM
}

for key, value in formats.items():
    print(f"{key}: {value}")

print("开始执行...")
time.sleep(2.5)  # 休眠2.5秒
print("2.5秒后继续执行...")

# 精确到纳秒的睡眠（Python 3.11+）
time.sleep(0.001)  # 休眠1毫秒

# 测量代码执行时间
start_time = time.time()

# 模拟耗时操作
sum_result = 0
for i in range(1000000):
    sum_result += i

end_time = time.time()
execution_time = end_time - start_time
print(f"代码执行时间: {execution_time:.6f} 秒")

# 使用 perf_counter（更精确）
start = time.perf_counter()

# 执行代码
time.sleep(0.1)

end = time.perf_counter()
print(f"精确执行时间: {end - start:.6f} 秒")


# 计算时间差
def time_difference(start_time_param, end_time_param):
    """计算两个时间戳之间的差值"""
    diff = end_time_param - start_time_param
    hours = diff // 3600
    minutes = (diff % 3600) // 60
    seconds = diff % 60
    return hours, minutes, seconds


start = time.time()
time.sleep(3.75)  # 休眠3.75秒
end = time.time()

h, m, s = time_difference(start, end)
print(f"时间差: {h}小时 {m}分钟 {s:.2f}秒")
