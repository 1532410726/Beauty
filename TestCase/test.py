from datetime import datetime

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))  # 输出：2025-06-20 14:30:45
print(int(datetime.now().timestamp()))  #输出当前时间戳

a = 0.1
b = 0.2
print(a+b)