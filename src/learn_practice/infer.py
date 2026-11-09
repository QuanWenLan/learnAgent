# 推导式 Comprehensions
# 列表推导式
"""
[表达式 for 变量 in 列表]
[out_exp_res for out_exp in input_list]

或者

[表达式 for 变量 in 列表 if 条件]
[out_exp_res for out_exp in input_list if condition]
"""
# 基本过滤
# 过滤出偶数
numbers = [1, 2, 3, 4, 5, 6]
evens = [x for x in numbers if x % 2 == 0]  # 筛选满足条件的元素（不改变元素值）
print(evens)  # 输出: [2, 4, 6]

# 带条件转换
# 将正数转为平方，负数保持不变
nums = [-2, -1, 0, 1, 2]
processed = [x ** 2 if x > 0 else x for x in nums]  # 对每个元素 x 进行条件判断，返回不同的值（改变元素值）
print(processed)  # 输出: [-2, -1, 0, 1, 4]

# 嵌套循环（扁平化矩阵）
matrix = [[1, 2], [3, 4], [5, 6]]
flatten = [num for row in matrix for num in row]
print(flatten)  # 输出: [1, 2, 3, 4, 5, 6]

# 多条件筛选
# 筛选能被2或3整除的数
nums = range(20)
filtered = [x for x in nums if x % 2 == 0 or x % 3 == 0]
print(filtered)  # 输出: [0, 2, 3, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18]

# 字典推导式
"""
{ key_expr: value_expr for value in collection }

或

{ key_expr: value_expr for value in collection if condition }
"""
# 键值互换
original = {'a': 1, 'b': 2}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # 输出: {1: 'a', 2: 'b'}

# 只保留值大于0的项
scores = {'Alice': 85, 'Bob': -1, 'Charlie': 90}
passed = {k: v for k, v in scores.items() if v > 0}
print(passed)  # 输出: {'Alice': 85, 'Charlie': 90}

# 集合推导式
'''
{ expression for item in Sequence }
或
{ expression for item in Sequence if conditional }
'''
setnew = {i ** 2 for i in (1, 2, 3)}  # 输出: {1, 4, 9}

# 元组推导式
'''
(expression for item in Sequence )
或
(expression for item in Sequence if conditional )
'''
a = (x for x in range(1, 10))
print(a)  # 输出: <generator object <genexpr> at 0x000001F95CADC040>
print(tuple(a))
