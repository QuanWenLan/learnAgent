import sys  # 引入 sys 模块

num = {1, 2, 3, 4}
num2 = [x * 2 for x in num]
print(num2)

for x in num2:
    if x <= 2:
        print(x, "小于等于2")
    elif x <= 4:
        print(x, "小于等于4")
    elif x <= 6:
        print(x, "小于等于6")
    else:
        print(x, "大于6")

num3 = [x for x in num2 if x / 3 > 1]
print(num3)

tempList = [1, 2, 3, 4]
it = iter(tempList)  # 创建迭代器对象

for x in it:
    print(x, end=" ")

it = iter(tempList)  # 创建迭代器对象，只能用一次
while True:
    try:
        print(next(it))
    except StopIteration:
        sys.exit()
