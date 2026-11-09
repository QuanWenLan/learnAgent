# 元组
user = 1, 2, 3
print(user)
print(type(user))

# 字典
tinydict = {'name': 'runoob', 'likes': 123, 'url': 'www.runoob.com'}
print(tinydict)
print(type(tinydict), len(tinydict), "tinydict['name']:", tinydict['name'], sep=" | ")
print(f"类型: {type(tinydict)} | 长度: {len(tinydict)} | name值: {tinydict['name']}")
# 使用get方法避免KeyError
name_value = tinydict.get('name', 'Key not found')
print(type(tinydict), len(tinydict), f"name: {name_value}", sep=" | ")

# 集合
set1 = {3, 1, 4, 2, 5}  # 直接使用大括号创建集合
set2 = set([4, 5, 6, 7])  # 使用 set() 函数从列表创建集合
set2.add(8)
print(set1, set2, set1.intersection(set2), set1, sep=" | ")
set1.pop()
print(set1, set1.isdisjoint(set2), set1.symmetric_difference(set2))
my_set = {3, 1, 4, 2, 5}
# 方法1：转换为列表后排序
sorted_list = sorted(my_set)
print(sorted_list)  # [1, 2, 3, 4, 5]

# 方法2：使用sorted()函数（返回列表）
sorted_list_desc = sorted(my_set, reverse=True)
print(sorted_list_desc)  # [5, 4, 3, 2, 1]

# 列表
# 示例：一个包含多种类型的列表
my_list = [1, "hello", 3.14, True, [1, 2, 3]]
colors = ["red", "green", "blue", "yellow"]

# 正向索引（从0开始）
print(colors[0])   # "red"
print(colors[2])   # "blue"

# 负向索引（从-1开始，表示末尾）
print(colors[-1])  # "yellow"

# 切片（左闭右开）
print(colors[1:3])    # ["green", "blue"]
print(colors[:2])     # ["red", "green"]
print(colors[2:])     # ["blue", "yellow"]
print(colors[::-1])   # 反转列表 → ["yellow", "blue", "green", "red"]

nums = [10, 20, 30]

# 修改单个元素
nums[0] = 100        # → [100, 20, 30]

# 修改切片
nums[1:] = [200, 300]  # → [100, 200, 300]

# 添加元素
nums.append(400)       # 末尾添加 → [100, 200, 300, 400]
nums.insert(1, 150)    # 在索引1插入 → [100, 150, 200, 300, 400]

# 删除元素
del nums[0]            # 删除索引0 → [150, 200, 300, 400]
nums.remove(200)       # 删除第一个值为200的元素 → [150, 300, 400]
last = nums.pop()      # 弹出最后一个元素（并返回）→ last=400, nums=[150, 300]

a = [1, 2]
b = [3, 4]

# 拼接（+）→ 创建新列表
c = a + b              # [1, 2, 3, 4]

# 重复（*）
d = [0] * 3            # [0, 0, 0]
e = [1, 2] * 2         # [1, 2, 1, 2]

# 注意：+= 是原地修改
a += b                 # a 变成 [1, 2, 3, 4]，不创建新对象（高效！）