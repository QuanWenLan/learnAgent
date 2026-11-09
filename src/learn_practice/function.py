def change(a):
    print(id(a))  # 指向的是同一个对象
    a = 10
    print(id(a))  # 一个新对象


a = 1
print(id(a))
change(a)


# 可写函数说明
def change_me(list):
    # "修改传入的列表"
    list.append([1, 2, 3, 4])
    print(f"函数内取值: {list}，地址：{id(list)}")
    return


# 调用changeme函数
mylist = [10, 20, 30]
change_me(mylist)
print(f"函数外取值: {mylist}，地址：{id(mylist)}")


# 不需要使用指定顺序
def print_info(name, age):
    # "打印任何传入的字符串"
    print("名字: ", name)
    print("年龄: ", age)
    return


# 调用printinfo函数
print_info(age=50, name="runoob")


# 默认参数 age = 35
def print_info2(name, age=35):
    # "打印任何传入的字符串"
    print("名字: ", name)
    print("年龄: ", age)
    return


# 调用printinfo函数
print_info2(age=50, name="runoob")
print("------------------------")
print_info2(name="runoob")

# 可变参数
'''
def functionname([formal_args,] *var_args_tuple ):
   "函数_文档字符串"
   function_suite
   return [expression]
'''


def print_info3(arg1, *vartuple):
    # "打印任何传入的参数"
    print("输出: ")
    print(arg1)
    print(vartuple)


# 调用printinfo 函数
print_info3(70, 60, 50)

# lambda 函数是匿名的，它们没有函数名称，只能通过赋值给变量或作为参数传递给其他函数来使用。
f = lambda: "Hello, world!"
print(f())  # 输出: Hello, world!

x = lambda a, b: a * b
print(x(5, 6))

x2 = lambda a, b, c : a + b + c
print(x2(5, 6, 2))

numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)  # 输出: [1, 4, 9, 16, 25]

numbers = [1, 2, 3, 4, 5, 6, 7, 8]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # 输出：[2, 4, 6, 8]