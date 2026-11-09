# 类的多态性
"""
1. 封装
概念：把数据（属性）和操作数据（方法）捆绑在一起，并对外隐藏内部实现的细节。
私有属性/方法：在 Python 中，在变量名或方法名前加两个下划线 __（例如 __money），就把它变成了私有的。外部无法直接访问，只能在类内部访问。
作用：保护数据安全，防止外部随意修改。
2. 继承
概念：子类继承父类，自动拥有父类的属性和方法。
单继承：class Dog(Animal):
多继承：class Dog(Animal, Pet):（Python 支持一个儿子认多个爹）。
作用：代码复用，避免重复造轮子。
3. 多态
概念：不同的子类对象，调用相同的方法，产生不同的执行结果。
核心：父类引用指向子类对象。
作用：增加代码的灵活性。
4. 特殊方法与属性分类
__new__：真正的构造函数，负责创建实例（在 __init__ 之前执行）。
__del__：析构函数，当对象被销毁（内存回收）时自动调用。
类属性 vs 实例属性：
类属性：所有对象共享（如“物种”）。
实例属性：每个对象独有（如“名字”）。
类方法 (@classmethod) vs 静态方法 (@staticmethod)：
类方法：操作类属性，第一个参数是 cls。
静态方法：与类无关的纯功能函数，不需要 self 或 cls。
"""

class Hero:
    # 类属性：所有英雄共享
    game_version = "1.0.0"
    hero_count = 0  # 记录英雄总数

    # __new__：真正的构造函数，负责创建实例（在 __init__ 之前执行）
    """
    1. *args (Positional Arguments)
    作用：接收任意数量的位置参数，并将它们打包成一个元组(tuple)
    使用场景：当你不确定调用者会传入多少个位置参数时
    2. **kwargs (Keyword Arguments)
    作用：接收任意数量的关键字参数，并将它们打包成一个字典(dict)
    使用场景：当你不确定调用者会传入多少个命名参数时
    
    1. * (单个星号) - 位置参数解包
    在函数定义时(打包):
    def func(*args):
    # * 把多个位置参数"打包"成一个元组
    print(args)

    func(1, 2, 3)  # args = (1, 2, 3)
    
    在函数调用时(解包):
    def func(a, b, c):
    print(a, b, c)

    numbers = [1, 2, 3]
    func(*numbers)  # 等价于 func(1, 2, 3), * 把列表"解开"成独立参数

    """
    def __new__(cls, *args, **kwargs):
        print("在 __init__ 之前执行，创建英雄对象...", args, type(args), kwargs, type(kwargs))
        return super().__new__(cls)

    def __init__(self, name, hp):
        # 实例属性：每个英雄独有
        self.name = name
        self._hp = hp  # 受保护的属性（单下划线），建议不要直接访问
        self.__weapon = "拳头"  # 私有属性（双下划线），外部无法访问
        Hero.hero_count += 1

    # 私有方法：只能在类内部调用
    def __attack(self):
        print(f"{self.name} 使用 {self.__weapon} 攻击！")

    # 公共方法：对外暴露的接口
    def fight(self):
        # 内部可以调用私有方法
        self.__attack()

    # 析构方法 析构函数，当对象被销毁（内存回收）时自动调用
    def __del__(self):
        print(f"{self.name} 退出了战场...")

    # 类方法：修饰器 @classmethod，操作类属性，第一个参数是 cls。
    @classmethod
    def get_hero_count(cls):
        print(f"当前版本 {cls.game_version} 共有 {cls.hero_count} 位英雄")

    # 静态方法：修饰器 @staticmethod，不需要 cls 或 self，
    @staticmethod
    def show_tips():
        print("提示：请按 W 键移动")


# --- 继承与多态演示 ---

class Warrior(Hero):  # 继承 Hero
    def __init__(self, name, hp, shield):
        super().__init__(name, hp)  # 调用父类初始化
        self.shield = shield

    # 多态：重写父类方法
    def fight(self):
        print(f"战士 {self.name} 举起了盾牌防御并反击！")


class Mage(Hero):  # 继承 Hero
    def fight(self):
        print(f"法师 {self.name} 释放了火球术！")


# --- 使用 ---
w1 = Warrior("盖伦", 500, "铁盾")
m1 = Mage("瑞兹", 300)

w1.fight()  # 输出：战士 盖伦 举起了盾牌防御并反击！
m1.fight()  # 输出：法师 瑞兹 释放了火球术！

# 访问私有属性会报错 (m1.__weapon)，体现了封装
Hero.get_hero_count()  # 类方法调用
Hero.show_tips()  # 静态方法调用