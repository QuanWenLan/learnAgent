"""
浅拷贝 (copy.copy() 或 list.copy())：创建一个新的对象，但内部的子对象（如嵌套的列表、字典）依然是引用原来的。修改嵌套对象会影响原数据。
深拷贝 (copy.deepcopy())：完全克隆一个全新的对象，包括内部所有的嵌套对象。新旧数据完全独立。

使用建议
扁平数据结构 → 浅拷贝就够了
嵌套数据结构 → 必须用深拷贝
配置管理 → 总是用深拷贝
性能敏感 → 评估是否真的需要拷贝
不确定时 → 用深拷贝更安全
"""

"""
Python 浅拷贝 vs 深拷贝完全指南
================================
理解 Python 中的对象引用、浅拷贝和深拷贝
"""

import copy


# ==========================================
# 第一部分：基础概念 - Python 的对象引用
# ==========================================

print("=" * 60)
print("【1】Python 的对象引用机制")
print("=" * 60)

# Python 中变量是对象的引用（指针）
a = [1, 2, 3]
b = a  # b 和 a 指向同一个对象

print(f"a = {a}")
print(f"b = {b}")
print(f"a is b: {a is b}")  # True，指向同一对象
print(f"id(a): {id(a)}")
print(f"id(b): {id(b)}")

# 修改 b 会影响 a
b.append(4)
print(f"\n修改 b 后:")
print(f"a = {a}")  # [1, 2, 3, 4] - a 也被影响了！
print(f"b = {b}")


# ==========================================
# 第二部分：浅拷贝（Shallow Copy）
# ==========================================

print("\n" + "=" * 60)
print("【2】浅拷贝（Shallow Copy）")
print("=" * 60)

# 创建浅拷贝的三种方式
original = [1, 2, [3, 4]]

# 方式1: 使用 copy 模块
shallow_copy1 = copy.copy(original)

# 方式2: 使用列表的 copy() 方法
shallow_copy2 = original.copy()

# 方式3: 使用切片
shallow_copy3 = original[:]

print(f"原始列表: {original}")
print(f"浅拷贝1: {shallow_copy1}")
print(f"浅拷贝2: {shallow_copy2}")
print(f"浅拷贝3: {shallow_copy3}")

print(f"\n是否是同一对象:")
print(f"original is shallow_copy1: {original is shallow_copy1}")  # False

# ⚠️ 浅拷贝的问题：只拷贝第一层
print(f"\n⚠️ 浅拷贝的陷阱:")
print(f"original[2] is shallow_copy1[2]: {original[2] is shallow_copy1[2]}")  # True!

# 修改嵌套列表会影响原对象
shallow_copy1[2].append(5)
print(f"\n修改浅拷贝的嵌套列表后:")
print(f"原始列表: {original}")        # [1, 2, [3, 4, 5]] - 被影响了！
print(f"浅拷贝1: {shallow_copy1}")    # [1, 2, [3, 4, 5]]


# ==========================================
# 第三部分：深拷贝（Deep Copy）
# ==========================================

print("\n" + "=" * 60)
print("【3】深拷贝（Deep Copy）")
print("=" * 60)

original = [1, 2, [3, 4]]
deep_copy = copy.deepcopy(original)

print(f"原始列表: {original}")
print(f"深拷贝: {deep_copy}")
print(f"original is deep_copy: {original is deep_copy}")  # False

# ✅ 深拷贝的优势：递归拷贝所有层级
print(f"\n✅ 深拷贝的安全性:")
print(f"original[2] is deep_copy[2]: {original[2] is deep_copy[2]}")  # False!

# 修改深拷贝不会影响原对象
deep_copy[2].append(5)
print(f"\n修改深拷贝的嵌套列表后:")
print(f"原始列表: {original}")      # [1, 2, [3, 4]] - 不受影响！
print(f"深拷贝: {deep_copy}")       # [1, 2, [3, 4, 5]]


# ==========================================
# 第四部分：可视化对比
# ==========================================

print("\n" + "=" * 60)
print("【4】浅拷贝 vs 深拷贝对比图")
print("=" * 60)

print("""
原始对象:     [1, 2, [3, 4]]
              │    │    │
              │    │    └─→ 嵌套列表对象 A

浅拷贝:       [1, 2, [3, 4]]
              │    │    │
              │    │    └─→ 嵌套列表对象 A (同一个！)
              
⚠️ 修改嵌套列表会影响原对象

────────────────────────────────────────

原始对象:     [1, 2, [3, 4]]
              │    │    │
              │    │    └─→ 嵌套列表对象 A

深拷贝:       [1, 2, [3, 4]]
              │    │    │
              │    │    └─→ 嵌套列表对象 B (全新的！)
              
✅ 修改嵌套列表不会影响原对象
""")


# ==========================================
# 第五部分：实际应用场景
# ==========================================

print("\n" + "=" * 60)
print("【5】实际应用场景")
print("=" * 60)


# 场景1: 字典配置管理
print("\n【场景1】字典配置管理")
print("-" * 40)

default_config = {
    "database": {
        "host": "localhost",
        "port": 3306,
        "options": {"timeout": 30, "retry": 3}
    },
    "cache": {
        "enabled": True,
        "ttl": 3600
    }
}

# ❌ 错误：直接赋值
user_config1 = default_config
user_config1["database"]["host"] = "remote_server"
print(f"❌ 直接赋值后，默认配置被污染:")
print(f"   default_config['database']['host'] = {default_config['database']['host']}")

# 恢复
default_config["database"]["host"] = "localhost"

# ❌ 浅拷贝：嵌套字典仍然共享
user_config2 = copy.copy(default_config)
user_config2["database"]["host"] = "remote_server"
print(f"\n❌ 浅拷贝后，嵌套字典仍被污染:")
print(f"   default_config['database']['host'] = {default_config['database']['host']}")

# 恢复
default_config["database"]["host"] = "localhost"

# ✅ 深拷贝：完全独立
user_config3 = copy.deepcopy(default_config)
user_config3["database"]["host"] = "remote_server"
print(f"\n✅ 深拷贝后，默认配置安全:")
print(f"   default_config['database']['host'] = {default_config['database']['host']}")
print(f"   user_config3['database']['host'] = {user_config3['database']['host']}")


# 场景2: 游戏角色状态保存
print("\n【场景2】游戏角色状态保存")
print("-" * 40)

class GameState:
    def __init__(self, player_name, inventory, skills):
        self.player_name = player_name
        self.inventory = inventory  # 背包物品
        self.skills = skills        # 技能列表

    def __repr__(self):
        return f"GameState({self.player_name}, {self.inventory}, {self.skills})"

# 创建游戏状态
original_state = GameState("勇者", ["剑", "盾牌", "药水"], ["火球术", "治疗术"])

# ❌ 浅拷贝：修改背包会影响原状态
saved_state_shallow = copy.copy(original_state)
saved_state_shallow.inventory.append("宝藏")
print(f"❌ 浅拷贝保存:")
print(f"   原始状态: {original_state}")
print(f"   保存状态: {saved_state_shallow}")

# 恢复
original_state.inventory.remove("宝藏")

# ✅ 深拷贝：完全独立的存档
saved_state_deep = copy.deepcopy(original_state)
saved_state_deep.inventory.append("宝藏")
saved_state_deep.skills.append("传送术")
print(f"\n✅ 深拷贝保存:")
print(f"   原始状态: {original_state}")
print(f"   保存状态: {saved_state_deep}")


# 场景3: 函数参数保护
print("\n【场景3】函数参数保护")
print("-" * 40)

def process_data_bad(data):
    """❌ 不好的做法：直接修改传入的参数"""
    data.append("processed")
    return data

def process_data_good(data):
    """✅ 好的做法：先拷贝再处理"""
    data_copy = copy.deepcopy(data)
    data_copy.append("processed")
    return data_copy

original_data = [1, 2, 3, {"nested": "value"}]

# 测试不好的做法
result_bad = process_data_bad(copy.deepcopy(original_data))
print(f"原始数据可能被修改（如果没拷贝的话）")

# 测试好的做法
result_good = process_data_good(original_data)
print(f"✅ 原始数据保持不变: {original_data}")
print(f"   处理结果: {result_good}")


# 场景4: 缓存系统
print("\n【场景4】缓存系统")
print("-" * 40)

class CacheSystem:
    def __init__(self):
        self.cache = {}

    def set(self, key, value):
        # 深拷贝存储，防止外部修改影响缓存
        self.cache[key] = copy.deepcopy(value)

    def get(self, key):
        # 深拷贝返回，防止外部修改影响缓存
        if key in self.cache:
            return copy.deepcopy(self.cache[key])
        return None

cache = CacheSystem()
original_data = {"users": [{"name": "张三", "age": 25}]}

cache.set("users", original_data)

# 修改原始数据
original_data["users"][0]["age"] = 30

# 从缓存获取的数据不受影响
cached_data = cache.get("users")
print(f"✅ 缓存数据保持原样:")
print(f"   原始数据: {original_data}")
print(f"   缓存数据: {cached_data}")


# ==========================================
# 第六部分：性能对比
# ==========================================

print("\n" + "=" * 60)
print("【6】性能对比")
print("=" * 60)


# 创建大型数据结构
large_list = [[i for i in range(100)] for _ in range(100)]

# 更精确的性能测试
import time

# 测试浅拷贝性能
start = time.perf_counter()
for _ in range(1000):
    _ = copy.copy(large_list)
shallow_time = time.perf_counter() - start

# 测试深拷贝性能
start = time.perf_counter()
for _ in range(1000):
    _ = copy.deepcopy(large_list)
deep_time = time.perf_counter() - start

print(f"浅拷贝 1000 次耗时: {shallow_time:.6f} 秒")
print(f"深拷贝 1000 次耗时: {deep_time:.6f} 秒")

if shallow_time > 0:
    print(f"深拷贝比浅拷贝慢: {deep_time / shallow_time:.2f} 倍")
print(f"\n💡 提示：深拷贝更慢，因为要递归复制所有嵌套对象")


# ==========================================
# 第七部分：特殊情况的处理
# ==========================================

print("\n" + "=" * 60)
print("【7】特殊情况处理")
print("=" * 60)


# 情况1: 不可变对象不需要拷贝
print("\n【情况1】不可变对象")
print("-" * 40)

immutable = (1, 2, 3)  # 元组是不可变的
shallow = copy.copy(immutable)
deep = copy.deepcopy(immutable)

print(f"元组的浅拷贝和深拷贝:")
print(f"immutable is shallow: {immutable is shallow}")  # True - Python 优化
print(f"immutable is deep: {immutable is deep}")        # True - Python 优化
print(f"💡 不可变对象不需要拷贝，Python 会优化")


# 情况2: 自定义类的拷贝
print("\n【情况2】自定义类的拷贝控制")
print("-" * 40)

class CustomClass:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __copy__(self):
        """自定义浅拷贝逻辑"""
        print(f"   执行自定义浅拷贝: {self.name}")
        return CustomClass(self.name, copy.copy(self.data))

    def __deepcopy__(self, memo):
        """自定义深拷贝逻辑"""
        print(f"   执行自定义深拷贝: {self.name}")
        return CustomClass(self.name, copy.deepcopy(self.data, memo))

obj = CustomClass("测试对象", [1, 2, [3, 4]])
print("浅拷贝:")
obj_shallow = copy.copy(obj)

print("\n深拷贝:")
obj_deep = copy.deepcopy(obj)


# 情况3: 循环引用的处理
print("\n【情况3】循环引用")
print("-" * 40)

a = []
b = [a]
a.append(b)  # 循环引用: a -> b -> a

print(f"创建了循环引用结构")
try:
    # deepcopy 可以处理循环引用
    a_deep = copy.deepcopy(a)
    print(f"✅ 深拷贝成功处理循环引用")
except Exception as e:
    print(f"❌ 深拷贝失败: {e}")


# ==========================================
# 第八部分：选择指南
# ==========================================

print("\n" + "=" * 60)
print("【8】如何选择：浅拷贝 vs 深拷贝")
print("=" * 60)

print("""
📋 决策指南:

┌──────────────────┬────────────┬────────────┐
│ 场景             │ 浅拷贝     │ 深拷贝     │
├──────────────────┼────────────┼────────────┤
│ 扁平列表/字典    │ ✅ 推荐    │ ⚠️ 过度    │
│ 嵌套数据结构     │ ❌ 危险    │ ✅ 推荐    │
│ 包含不可变对象   │ ✅ 足够    │ ✅ 安全    │
│ 性能敏感         │ ✅ 快速    │ ❌ 较慢    │
│ 需要完全隔离     │ ❌ 不够    │ ✅ 必须    │
│ 配置管理         │ ❌ 危险    │ ✅ 推荐    │
│ 简单数据传递     │ ✅ 足够    │ ⚠️ 过度    │
└──────────────────┴────────────┴────────────┘

💡 经验法则:
1. 如果数据只有一层 → 用浅拷贝或切片
2. 如果数据有嵌套 → 用深拷贝
3. 如果不确定 → 用深拷贝更安全
4. 如果性能关键 → 评估是否真的需要拷贝

常用拷贝方式速查:
- 列表: list.copy(), lst[:], copy.copy(lst)
- 字典: dict.copy(), copy.copy(dct)
- 通用: copy.copy(obj), copy.deepcopy(obj)
""")


# ==========================================
# 第九部分：常见错误和陷阱
# ==========================================

print("\n" + "=" * 60)
print("【9】常见错误和陷阱")
print("=" * 60)


# 陷阱1: 以为切片是深拷贝
print("\n【陷阱1】切片不是深拷贝")
print("-" * 40)

original = [[1, 2], [3, 4]]
sliced = original[:]

print(f"original[0] is sliced[0]: {original[0] is sliced[0]}")  # True!
sliced[0].append(3)
print(f"❌ 修改切片影响了原列表: {original}")


# 陷阱2: 字典的 copy() 也是浅拷贝
print("\n【陷阱2】dict.copy() 是浅拷贝")
print("-" * 40)

original = {"nested": {"key": "value"}}
copied = original.copy()

print(f"original['nested'] is copied['nested']: {original['nested'] is copied['nested']}")  # True!
copied["nested"]["key"] = "modified"
print(f"❌ 修改拷贝影响了原字典: {original}")


# 陷阱3: 忘记拷贝可变默认参数
print("\n【陷阱3】可变默认参数")
print("-" * 40)

def bad_append(item, lst=[]):  # ❌ 危险的可变默认参数
    lst.append(item)
    return lst

def good_append(item, lst=None):  # ✅ 安全的写法
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(f"bad_append(1): {bad_append(1)}")
print(f"bad_append(2): {bad_append(2)}")  # [1, 2] - 意外行为！

print(f"\ngood_append(1): {good_append(1)}")
print(f"good_append(2): {good_append(2)}")  # [2] - 符合预期


print("\n✅ 所有拷贝示例执行完毕!")
