"""
Python 内置高效函数完全指南
============================
掌握 Python 内置函数，写出更简洁、高效的代码
"""


# ==========================================
# 第一部分：函数式编程三剑客
# ==========================================

print("=" * 60)
print("【1】map() - 映射函数")
print("=" * 60)

# 案例1: 批量转换数据类型
numbers = ["1", "2", "3", "4", "5"]
int_numbers = list(map(int, numbers))
print(f"字符串转整数: {int_numbers}")

# 案例2: 批量处理数据
names = ["alice", "bob", "charlie"]
capitalized = list(map(str.capitalize, names))
print(f"首字母大写: {capitalized}")

# 案例3: 使用 lambda 表达式
squares = list(map(lambda x: x ** 2, range(10)))
print(f"平方数: {squares}")

# 案例4: 多个可迭代对象
list1 = [1, 2, 3]
list2 = [10, 20, 30]
summed = list(map(lambda x, y: x + y, list1, list2))
print(f"对应元素相加: {summed}")

# 对比：列表推导式（更 Pythonic）
squares_v2 = [x ** 2 for x in range(10)]
print(f"列表推导式等价写法: {squares_v2}")


print("\n" + "=" * 60)
print("【2】filter() - 过滤函数")
print("=" * 60)

# 案例1: 过滤偶数
numbers = range(20)
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"偶数: {evens}")

# 案例2: 过滤空值
data = ["hello", "", "world", None, "python", "", "java"]
filtered = list(filter(None, data))  # None 作为函数会过滤掉假值
print(f"过滤空值: {filtered}")

# 案例3: 过滤字典中的特定项
students = [
    {"name": "张三", "score": 85},
    {"name": "李四", "score": 92},
    {"name": "王五", "score": 78},
    {"name": "赵六", "score": 95},
]
excellent = list(filter(lambda s: s["score"] >= 90, students))
print(f"优秀学生: {[s['name'] for s in excellent]}")

# 对比：列表推导式（更常用）
evens_v2 = [x for x in range(20) if x % 2 == 0]
print(f"列表推导式等价写法: {evens_v2}")


print("\n" + "=" * 60)
print("【3】reduce() - 归约函数")
print("=" * 60)

from functools import reduce

# 案例1: 求和
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda x, y: x + y, numbers)
print(f"求和: {total}")

# 案例2: 求乘积
product = reduce(lambda x, y: x * y, numbers)
print(f"乘积: {product}")

# 案例3: 找最大值
max_value = reduce(lambda x, y: x if x > y else y, numbers)
print(f"最大值: {max_value}")

# 案例4: 合并字典
dict_list = [{"a": 1}, {"b": 2}, {"c": 3}]
merged = reduce(lambda x, y: {**x, **y}, dict_list)
print(f"合并字典: {merged}")

# 案例5: 字符串拼接
words = ["Hello", "World", "Python"]
sentence = reduce(lambda x, y: f"{x} {y}", words)
print(f"字符串拼接: {sentence}")

# 💡 提示：简单场景用内置函数更高效
print(f"\n💡 求和推荐用 sum(): {sum(numbers)}")
print(f"💡 最大值推荐用 max(): {max(numbers)}")


# ==========================================
# 第二部分：排序相关函数
# ==========================================

print("\n" + "=" * 60)
print("【4】sorted() - 排序函数")
print("=" * 60)

# 案例1: 基本排序
numbers = [5, 2, 8, 1, 9, 3]
sorted_nums = sorted(numbers)
print(f"升序: {sorted_nums}")
print(f"原列表不变: {numbers}")

# 案例2: 降序排序
sorted_desc = sorted(numbers, reverse=True)
print(f"降序: {sorted_desc}")

# 案例3: 按绝对值排序
mixed = [-5, 3, -1, 8, -2]
sorted_abs = sorted(mixed, key=abs)
print(f"按绝对值排序: {sorted_abs}")

# 案例4: 字符串按长度排序
words = ["python", "java", "c", "javascript", "go"]
sorted_by_len = sorted(words, key=len)
print(f"按长度排序: {sorted_by_len}")

# 案例5: 字典列表排序
students = [
    {"name": "张三", "score": 85, "age": 20},
    {"name": "李四", "score": 92, "age": 19},
    {"name": "王五", "score": 78, "age": 21},
]

# 按分数排序
by_score = sorted(students, key=lambda s: s["score"], reverse=True)
print(f"按分数排序: {[s['name'] for s in by_score]}")

# 多条件排序：先按分数降序，再按年龄升序
by_multi = sorted(students, key=lambda s: (-s["score"], s["age"]))
print(f"多条件排序: {[(s['name'], s['score'], s['age']) for s in by_multi]}")

# 案例6: 使用 operator 模块（更高效）
from operator import itemgetter, attrgetter

by_score_v2 = sorted(students, key=itemgetter("score"), reverse=True)
print(f"使用 itemgetter: {[s['name'] for s in by_score_v2]}")


print("\n" + "=" * 60)
print("【5】enumerate() - 枚举函数")
print("=" * 60)

# 案例1: 遍历列表获取索引
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"  [{index}] {fruit}")

# 案例2: 自定义起始索引
for index, fruit in enumerate(fruits, start=1):
    print(f"  {index}. {fruit}")

# 案例3: 创建索引字典
index_dict = {fruit: idx for idx, fruit in enumerate(fruits)}
print(f"索引字典: {index_dict}")

# 案例4: 查找所有匹配项的位置
text = "hello world hello python hello"
positions = [idx for idx, word in enumerate(text.split()) if word == "hello"]
print(f"'hello' 出现的位置: {positions}")


print("\n" + "=" * 60)
print("【6】zip() - 压缩函数")
print("=" * 60)

# 案例1: 合并多个列表
names = ["张三", "李四", "王五"]
ages = [20, 21, 22]
scores = [85, 92, 78]

for name, age, score in zip(names, ages, scores):
    print(f"  {name}: {age}岁, {score}分")

# 案例2: 创建字典
student_dict = dict(zip(names, scores))
print(f"姓名-分数字典: {student_dict}")

# 案例3: 解压（反向操作）
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
numbers, letters = zip(*pairs)
print(f"解压后: numbers={numbers}, letters={letters}")

# 案例4: 矩阵转置
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = list(zip(*matrix))
print(f"矩阵转置: {transposed}")

# 案例5: 找出每组的最小值
list1 = [5, 10, 15]
list2 = [3, 12, 8]
list3 = [7, 9, 20]
mins = [min(values) for values in zip(list1, list2, list3)]
print(f"每组最小值: {mins}")


# ==========================================
# 第三部分：聚合函数
# ==========================================

print("\n" + "=" * 60)
print("【7】常用聚合函数")
print("=" * 60)

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# sum() - 求和
print(f"sum({numbers}) = {sum(numbers)}")

# max() / min() - 最大/最小值
print(f"max({numbers}) = {max(numbers)}")
print(f"min({numbers}) = {min(numbers)}")

# 带 key 参数
words = ["python", "java", "javascript", "go"]
print(f"最长的单词: {max(words, key=len)}")
print(f"最短的单词: {min(words, key=len)}")

# len() - 长度
print(f"len({numbers}) = {len(numbers)}")

# all() / any() - 全部/任意
bool_list = [True, True, False, True]
print(f"all({bool_list}) = {all(bool_list)}")  # False
print(f"any({bool_list}) = {any(bool_list)}")  # True

# 实际案例：检查所有学生是否及格
students_scores = [85, 92, 78, 60, 95]
all_passed = all(score >= 60 for score in students_scores)
print(f"所有学生都及格了吗？ {all_passed}")

has_excellent = any(score >= 90 for score in students_scores)
print(f"有优秀学生吗？ {has_excellent}")


# ==========================================
# 第四部分：范围与迭代
# ==========================================

print("\n" + "=" * 60)
print("【8】range() - 范围函数")
print("=" * 60)

# 案例1: 基本用法
print(f"range(5): {list(range(5))}")
print(f"range(2, 8): {list(range(2, 8))}")
print(f"range(0, 10, 2): {list(range(0, 10, 2))}")

# 案例2: 倒序
print(f"range(10, 0, -1): {list(range(10, 0, -1))}")

# 案例3: 生成索引
items = ["a", "b", "c", "d"]
for i in range(len(items)):
    print(f"  items[{i}] = {items[i]}")

# 💡 更好的方式：用 enumerate
print("\n💡 推荐用 enumerate:")
for i, item in enumerate(items):
    print(f"  items[{i}] = {item}")


print("\n" + "=" * 60)
print("【9】iter() 和 next() - 迭代器")
print("=" * 60)

# 案例1: 手动迭代
my_list = [1, 2, 3]
my_iter = iter(my_list)
print(f"next(): {next(my_iter)}")
print(f"next(): {next(my_iter)}")
print(f"next(): {next(my_iter)}")

# 案例2: 带默认值
my_iter = iter([1])
print(f"next(默认值): {next(my_iter, '无更多元素')}")
print(f"next(默认值): {next(my_iter, '无更多元素')}")

# 案例3: 无限迭代器
from itertools import count, cycle, repeat

counter = count(start=10, step=2)
print(f"\n无限计数器: {[next(counter) for _ in range(5)]}")

cycler = cycle(['A', 'B', 'C'])
print(f"循环器: {[next(cycler) for _ in range(7)]}")

repeater = repeat('Hello', 3)
print(f"重复器: {list(repeater)}")


# ==========================================
# 第五部分：类型转换函数
# ==========================================

print("\n" + "=" * 60)
print("【10】类型转换函数")
print("=" * 60)

# int(), float(), str(), bool()
print(f"int('42') = {int('42')}")
print(f"float('3.14') = {float('3.14')}")
print(f"str(123) = '{str(123)}'")
print(f"bool(1) = {bool(1)}, bool(0) = {bool(0)}")

# list(), tuple(), set(), dict()
print(f"\nlist((1,2,3)) = {list((1, 2, 3))}")
print(f"tuple([1,2,3]) = {tuple([1, 2, 3])}")
print(f"set([1,1,2,2,3]) = {set([1, 1, 2, 2, 3])}")
print(f"dict([('a',1), ('b',2)]) = {dict([('a', 1), ('b', 2)])}")

# bytes(), bytearray()
print(f"\nbytes('hello', 'utf-8') = {bytes('hello', 'utf-8')}")

# chr(), ord()
print(f"\nchr(65) = '{chr(65)}'")
print(f"ord('A') = {ord('A')}")

# hex(), oct(), bin()
num = 255
print(f"\nhex({num}) = {hex(num)}")
print(f"oct({num}) = {oct(num)}")
print(f"bin({num}) = {bin(num)}")


# ==========================================
# 第六部分：高级内置函数
# ==========================================

print("\n" + "=" * 60)
print("【11】any() 和 all() 的高级用法")
print("=" * 60)

# 案例1: 验证表单数据
form_data = {
    "username": "john",
    "email": "john@example.com",
    "password": "secret123",
}

# 检查所有字段都不为空
is_valid = all(value for value in form_data.values())
print(f"表单有效: {is_valid}")

# 案例2: 检查是否有敏感词
comments = ["很好", "不错", "这个垃圾产品", "一般般"]
bad_words = ["垃圾", "骗子", "假货"]
has_bad_word = any(word in comment for comment in comments for word in bad_words)
print(f"包含敏感词: {has_bad_word}")

# 案例3: 矩阵检查（所有行长度相同）
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
row_length = len(matrix[0])
is_regular = all(len(row) == row_length for row in matrix)
print(f"矩阵规则: {is_regular}")


print("\n" + "=" * 60)
print("【12】callable() - 检查可调用性")
print("=" * 60)

def my_func():
    pass

class MyClass:
    def __call__(self):
        return "Called!"

print(f"callable(my_func): {callable(my_func)}")
print(f"callable(MyClass): {callable(MyClass)}")
print(f"callable(lambda: None): {callable(lambda: None)}")
print(f"callable(42): {callable(42)}")

obj = MyClass()
print(f"callable(obj): {callable(obj)}")  # 实现了 __call__


print("\n" + "=" * 60)
print("【13】isinstance() 和 issubclass() - 类型检查")
print("=" * 60)

# isinstance() - 检查实例
print(f"isinstance(42, int): {isinstance(42, int)}")
print(f"isinstance('hello', str): {isinstance('hello', str)}")
print(f"isinstance([1,2], (list, tuple)): {isinstance([1, 2], (list, tuple))}")

# issubclass() - 检查子类
class Animal:
    pass

class Dog(Animal):
    pass

print(f"\nissubclass(Dog, Animal): {issubclass(Dog, Animal)}")
print(f"issubclass(Dog, Dog): {issubclass(Dog, Dog)}")


print("\n" + "=" * 60)
print("【14】vars(), dir(), help() -  introspection")
print("=" * 60)

# vars() - 查看对象的属性字典
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person = Person("张三", 25)
print(f"vars(person): {vars(person)}")

# dir() - 查看对象的所有属性和方法
print(f"\ndir(person) 前10个: {dir(person)[:10]}")

# help() - 查看帮助文档（注释掉，避免阻塞）
# help(str.upper)


# ==========================================
# 第七部分：实用技巧组合
# ==========================================

print("\n" + "=" * 60)
print("【15】实战技巧组合")
print("=" * 60)

# 技巧1: map + filter 组合
numbers = range(1, 21)
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(f"偶数的平方: {result}")

# 更 Pythonic 的写法
result_v2 = [x ** 2 for x in numbers if x % 2 == 0]
print(f"列表推导式: {result_v2}")

# 技巧2: zip + dict 创建映射
keys = ["name", "age", "city"]
values = ["Alice", 25, "Beijing"]
person = dict(zip(keys, values))
print(f"\n快速创建字典: {person}")

# 技巧3: enumerate + dict 反转字典
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(f"反转字典: {reversed_dict}")

# 技巧4: sorted + zip 并行排序
names = ["张三", "李四", "王五"]
scores = [85, 92, 78]
sorted_pairs = sorted(zip(scores, names), reverse=True)
print(f"\n并行排序: {[(name, score) for score, name in sorted_pairs]}")

# 技巧5: reduce + map 数据处理
from functools import reduce

data = ["1", "2", "3", "4", "5"]
total = reduce(lambda x, y: x + y, map(int, data))
print(f"字符串列表求和: {total}")

# 技巧6: any + generator 短路评估
import time

def slow_check(n):
    time.sleep(0.1)
    return n > 100

start = time.time()
# 一旦找到 True 就停止
result = any(slow_check(n) for n in [1, 2, 3, 200, 5, 6])
elapsed = time.time() - start
print(f"\n短路评估耗时: {elapsed:.2f}秒 (而非 0.6秒)")


# ==========================================
# 第八部分：性能对比
# ==========================================

print("\n" + "=" * 60)
print("【16】性能对比：内置函数 vs 手动实现")
print("=" * 60)

import time

# 测试数据
large_list = list(range(10000))

# 对比1: sum() vs 循环
start = time.time()
total1 = sum(large_list)
time_sum = time.time() - start

start = time.time()
total2 = 0
for num in large_list:
    total2 += num
time_loop = time.time() - start

print(f"sum() 耗时: {time_sum:.6f}秒")
print(f"循环耗时: {time_loop:.6f}秒")
print(f"内置函数快 {time_loop / time_sum:.2f} 倍")

# 对比2: map() vs 列表推导式 vs 循环
def square(x):
    return x ** 2

start = time.time()
result1 = list(map(square, large_list))
time_map = time.time() - start

start = time.time()
result2 = [x ** 2 for x in large_list]
time_comprehension = time.time() - start

start = time.time()
result3 = []
for x in large_list:
    result3.append(x ** 2)
time_append = time.time() - start

print(f"\nmap() 耗时: {time_map:.6f}秒")
print(f"列表推导式耗时: {time_comprehension:.6f}秒")
print(f"循环 append 耗时: {time_append:.6f}秒")
print(f"最快的是: {'map()' if time_map < time_comprehension else '列表推导式'}")


# ==========================================
# 第九部分：最佳实践总结
# ==========================================

print("\n" + "=" * 60)
print("【17】最佳实践总结")
print("=" * 60)

print("""
📋 内置函数使用指南:

✅ 推荐使用场景:
┌──────────────┬─────────────────────────────┐
│ 函数         │ 典型用途                     │
├──────────────┼─────────────────────────────┤
│ map()        │ 批量转换数据                 │
│ filter()     │ 过滤数据（复杂条件）         │
│ sorted()     │ 自定义排序                   │
│ enumerate()  │ 需要索引的遍历               │
│ zip()        │ 并行迭代多个序列             │
│ sum/max/min  │ 聚合计算                     │
│ any/all      │ 布尔判断                     │
│ reduce()     │ 累积操作（需 from functools）│
└──────────────┴─────────────────────────────┘

💡 经验法则:
1. 优先使用内置函数 - 更快、更简洁
2. 简单场景用列表推导式 - 更 Pythonic
3. 复杂转换用 map/filter - 更清晰
4. 需要索引时用 enumerate - 更优雅
5. 并行迭代用 zip - 更安全
6. 避免过度嵌套 - 可读性优先

⚠️ 注意事项:
- map/filter 返回迭代器，需要 list() 转换
- reduce 需要从 functools 导入
- sorted 不修改原列表，list.sort() 修改原列表
- zip 以最短的为准，可用 itertools.zip_longest 补齐
""")

print("\n✅ 所有内置函数示例执行完毕!")
