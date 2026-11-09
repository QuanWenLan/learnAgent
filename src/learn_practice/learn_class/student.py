# __init__方法（类的构造函数）
# 作用：它是类的“初始化”方法。当你创建对象时，Python 会自动调用它。
# 功能：用来给对象“赋初值”（设置初始状态）。

# 理解核心概念：self
"""
为什么要用它？
想象一下，你造了两个学生：张三和李四。当张三调用“自我介绍”这个方法时，self 就代表张三；当李四调用时，self 就代表李四。Python 通过 self 知道你在操作哪一个具体的对象。
怎么用？
在定义方法时，self 必须是第一个参数。
在类内部，通过 self.属性 来访问自己的数据。
注意：你在调用方法时，不需要手动传 self，Python 会自动帮你传。
"""

class Student:
    prop_1: str
    prop_2: int
    name: str

    # 1. 初始化方法：创建对象时自动调用
    def __init__(self, name, age):
        self.name = name  # 实例属性：属于当前对象的特征
        self.age = age
        self.score = 0    # 默认属性：所有学生初始分数都是0

    # 2. 定义方法：描述对象的行为
    def study(self, hours):
        # self 代表当前调用这个方法的学生
        self.score += hours * 10
        print(f"{self.name} 学习了 {hours} 小时，现在的分数是：{self.score}")

    def introduce(self):
        print(f"大家好，我是 {self.name}，今年 {self.age} 岁。")

# --- 下面是使用类的过程 ---

# 3. 创建对象 (实例化)
# 这里的 "张三" 和 18 会自动传给 __init__ 的 name 和 age 参数
stu1 = Student("张三", 18)

# 创建第二个对象
stu2 = Student("李四", 19)

# 4. 访问属性和调用方法
stu1.introduce()  # 输出：大家好，我是 张三，今年 18 岁。
stu2.introduce()  # 输出：大家好，我是 李四，今年 19 岁。

# 不同的对象，状态是独立的
stu1.study(2)     # 张三学习，分数增加
stu2.study(5)     # 李四学习，分数增加

# 查看最终状态
print(f"{stu1.name} 的分数: {stu1.score}") # 输出：张三 的分数: 20
print(f"{stu2.name} 的分数: {stu2.score}") # 输出：李四 的分数: 50