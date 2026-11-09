# Fibonacci series: 斐波纳契数列
# 两个元素的总和确定了下一个数
a, b = 0, 1
while b < 10:
    print(b)
    # a, b = b, a+b  # 多变量并行赋值，是原子操作，会先计算所有右侧表达式再赋值。而分开写会改变程序逻辑
    temp = a
    a = b
    b = temp + b

n = 100

totalSum = 0
counter = 1
while counter <= n:
    totalSum = totalSum + counter
    counter += 1

print("1 到 %d 之和为: %d" % (n, totalSum))

# 如果 while 后面的条件语句为 false 时，则执行 else 的语句块
count = 0
while count < 5:
    print(count, " 小于 5")
    count = count + 1
else:
    print(count, " 大于或等于 5")

sites = ["Baidu", "Google","Runoob","Taobao"]
for site in sites:
    print(site)

word = 'runoob'
for letter in word:
    print(letter)
else:
    print("循环结束")