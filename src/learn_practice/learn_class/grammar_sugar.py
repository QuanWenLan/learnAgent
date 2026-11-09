# Python * 和 ** 语法糖完全指南
"""
星号(*)在Python中有多种用途:
1. 数学运算: 乘法、幂运算
2. 序列重复: [1, 2] * 3 → [1, 2, 1, 2, 1, 2]
3. 参数打包/解包: *args, **kwargs
4. 可迭代对象解包: *list, *tuple, *set
5. 字典合并: {**dict1, **dict2}
6. 强制关键字参数: def func(a, *, b)
"""


# ==========================================
# 1. 基础用法: 乘法和重复
# ==========================================
print("=" * 50)
print("1. 基础用法: 乘法和重复")
print("=" * 50)

# 数字乘法
result = 5 * 3
print(f"5 * 3 = {result}")  # 输出: 15

# 字符串重复
stars = "*" * 10
print(f"'*' * 10 = {stars}")  # 输出: **********

# 列表重复
numbers = [1, 2] * 3
print(f"[1, 2] * 3 = {numbers}")  # 输出: [1, 2, 1, 2, 1, 2]


# ==========================================
# 2. *args - 位置参数打包
# ==========================================
print("\n" + "=" * 50)
print("2. *args - 位置参数打包")
print("=" * 50)

def sum_all(*args):
    """接收任意数量的位置参数并求和"""
    print(f"args 类型: {type(args)}")  # tuple
    print(f"args 内容: {args}")
    return sum(args)

# 可以传入任意个参数
print(f"sum_all(1, 2, 3) = {sum_all(1, 2, 3)}")
print(f"sum_all(1, 2, 3, 4, 5) = {sum_all(1, 2, 3, 4, 5)}")
print(f"sum_all() = {sum_all()}")  # 不传参数也可以


def greet(greeting, *names):
    """第一个参数固定，后面可以接任意多个名字"""
    print(f"{greeting}, {' 和 '.join(names)}!")

greet("你好", "张三", "李四", "王五")
# 输出: 你好, 张三 和 李四 和 王五!


# ==========================================
# 3. **kwargs - 关键字参数打包
# ==========================================
print("\n" + "=" * 50)
print("3. **kwargs - 关键字参数打包")
print("=" * 50)

def print_info(**kwargs):
    """接收任意数量的关键字参数"""
    print(f"kwargs 类型: {type(kwargs)}")  # dict
    print(f"kwargs 内容: {kwargs}")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_info(name="盖伦", hp=500, level=10)
print_info(city="北京", country="中国", population=2100)


def create_user(username, **options):
    """必需参数 + 可选的关键字参数"""
    user = {"username": username}
    user.update(options)  # 把额外的选项加入字典
    return user

user = create_user("player1", hp=100, mp=50, level=5)
print(f"\n创建的用户: {user}")


# ==========================================
# 4. 同时使用 *args 和 **kwargs
# ==========================================
print("\n" + "=" * 50)
print("4. 同时使用 *args 和 **kwargs")
print("=" * 50)

def flexible_func(required, *args, **kwargs):
    """
    最灵活的函数签名:
    - required: 必需的位置参数
    - *args: 额外的位置参数
    - **kwargs: 关键字参数
    """
    print(f"必需参数: {required}")
    print(f"额外位置参数: {args}")
    print(f"关键字参数: {kwargs}")

flexible_func("必须的值", 1, 2, 3, name="测试", value=100)


# ==========================================
# 5. * 解包 - 调用函数时展开列表/元组
# ==========================================
print("\n" + "=" * 50)
print("5. * 解包 - 调用函数时展开列表/元组")
print("=" * 50)

def add_three(a, b, c):
    return a + b + c

# 传统方式
result1 = add_three(1, 2, 3)
print(f"add_three(1, 2, 3) = {result1}")

# 使用 * 解包列表
numbers = [10, 20, 30]
result2 = add_three(*numbers)  # 等价于 add_three(10, 20, 30)
print(f"add_three(*[10, 20, 30]) = {result2}")

# 使用 * 解包元组
coords = (100, 200, 300)
result3 = add_three(*coords)
print(f"add_three(*(100, 200, 300)) = {result3}")


# ==========================================
# 6. ** 解包 - 调用函数时展开字典
# ==========================================
print("\n" + "=" * 50)
print("6. ** 解包 - 调用函数时展开字典")
print("=" * 50)

def show_profile(name, age, city):
    print(f"姓名: {name}, 年龄: {age}, 城市: {city}")

# 传统方式
show_profile("张三", 25, "北京")

# 使用 ** 解包字典
person = {"name": "李四", "age": 30, "city": "上海"}
show_profile(**person)  # 等价于 show_profile(name="李四", age=30, city="上海")

# 混合使用
extra_info = {"age": 28, "city": "深圳"}
show_profile("王五", **extra_info)


# ==========================================
# 7. 在可迭代对象中使用 * 解包
# ==========================================
print("\n" + "=" * 50)
print("7. 在可迭代对象中使用 * 解包")
print("=" * 50)

# 合并列表
list1 = [1, 2, 3]
list2 = [4, 5, 6]
merged = [*list1, *list2]
print(f"[*{list1}, *{list2}] = {merged}")

# 合并元组
tuple1 = (10, 20)
tuple2 = (30, 40)
merged_tuple = (*tuple1, *tuple2)
print(f"(*{tuple1}, *{tuple2}) = {merged_tuple}")

# 合并集合
set1 = {1, 2, 3}
set2 = {3, 4, 5}
merged_set = {*set1, *set2}
print(f"{{*{set1}, *{set2}}} = {merged_set}")

# 在中间插入元素
first, *middle, last = [1, 2, 3, 4, 5, 6]
print(f"first={first}, middle={middle}, last={last}")

# 只取第一个和最后一个
head, *tail = [10, 20, 30, 40, 50]
print(f"head={head}, tail={tail}")


# ==========================================
# 8. ** 合并字典
# ==========================================
print("\n" + "=" * 50)
print("8. ** 合并字典")
print("=" * 50)

dict1 = {"name": "盖伦", "hp": 500}
dict2 = {"level": 10, "weapon": "剑"}

# 传统写法
# 方法1: update() - 经典写法，兼容所有版本
merged1 = dict1.copy()
merged1.update(dict2)
print(f"update(): {merged1}")

# 方法2: dict() 构造函数 - 简洁但不够直观
merged2 = dict(dict1, **dict2)
print(f"dict(): {merged2}")

# Python 3.5+ 使用 ** 合并字典
merged_dict = {**dict1, **dict2}
print(f"{{**dict1, **dict2}} = {merged_dict}")

# 如果有重复键，后面的会覆盖前面的
dict3 = {"name": "瑞兹", "mp": 300}
merged_dict2 = {**dict1, **dict3}
print(f"有重复键时: {merged_dict2}")  # name 被覆盖为 "瑞兹"

# Python 3.9+ 可以使用 | 运算符
# merged_dict3 = dict1 | dict2


# ==========================================
# 9. 强制关键字参数 (Keyword-only arguments)
# ==========================================
print("\n" + "=" * 50)
print("9. 强制关键字参数")
print("=" * 50)

def create_hero(name, *, hp, mp):
    """
    * 后面的参数必须使用关键字形式传递
    这样可以提高代码可读性
    """
    return {"name": name, "hp": hp, "mp": mp}

# ✅ 正确用法
hero = create_hero("亚索", hp=400, mp=200)
print(f"英雄信息: {hero}")

# ❌ 错误用法（会报错）:
# hero = create_hero("亚索", 400, 200)  # TypeError!


def process_data(data, *, debug=False, verbose=True):
    """配置参数必须用关键字传递，避免混淆"""
    print(f"处理数据: {data}")
    print(f"调试模式: {debug}, 详细输出: {verbose}")

process_data([1, 2, 3], debug=True, verbose=False)


# ==========================================
# 10. 实际应用场景
# ==========================================
print("\n" + "=" * 50)
print("10. 实际应用场景")
print("=" * 50)

# 场景1: 装饰器中转发参数
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"调用函数: {func.__name__}")
        print(f"位置参数: {args}")
        print(f"关键字参数: {kwargs}")
        result = func(*args, **kwargs)  # 转发所有参数
        print(f"返回值: {result}")
        return result
    return wrapper

@my_decorator
def multiply(x, y):
    return x * y

multiply(5, 3)
# multiply(10, 20, extra="test")  # 注意: 这里会报错，因为 multiply 只接受2个参数


# 场景2: 类继承中的参数转发
class BaseClass:
    def __init__(self, name, **kwargs):
        self.name = name
        self.extra = kwargs
        print(f"BaseClass 初始化: name={name}, extra={kwargs}")

class DerivedClass(BaseClass):
    def __init__(self, name, age, **kwargs):
        super().__init__(name, **kwargs)  # 转发额外的关键字参数
        self.age = age
        print(f"DerivedClass 初始化: age={age}")

obj = DerivedClass("测试对象", 25, hp=100, mp=50)


# 场景3: 日志记录
def log_message(level, *messages, timestamp=None):
    """记录多条消息"""
    if timestamp is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] [{level}]")
    for msg in messages:
        print(f"  - {msg}")

log_message("INFO", "系统启动", "加载配置", "连接数据库")


# ==========================================
# 11. 常见错误和注意事项
# ==========================================
print("\n" + "=" * 50)
print("11. 常见错误和注意事项")
print("=" * 50)

# 错误1: *args 必须在普通参数之后
# def bad_func(*args, normal_param):  # ❌ 错误!
#     pass

def good_func(normal_param, *args):  # ✅ 正确
    pass

# 错误2: **kwargs 必须在最后
# def bad_func2(**kwargs, *args):  # ❌ 错误!
#     pass

def good_func2(*args, **kwargs):  # ✅ 正确
    pass

# 错误3: 解包时参数数量要匹配
def add_two(a, b):
    return a + b

# add_two(*[1, 2, 3])  # ❌ TypeError: 太多参数

# 注意: * 只能用于可迭代对象
# ** 只能用于字典或映射类型

print("\n✅ 所有示例执行完毕!")
