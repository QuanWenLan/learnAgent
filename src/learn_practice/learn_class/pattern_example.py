# 单例模式

class Database:
    __instance = None # 用于存储唯一的实例

    def __new__(cls, *args, **kwargs):
        # 如果没有实例，就创建一个；如果有，就返回现有的
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, url):
        self.url = url

# 测试
db1 = Database("mysql://localhost")
db2 = Database("mysql://192.168.1.1")

print(db1 is db2) # 输出：True (它们是同一个对象！)
# 注意：虽然对象相同，但 __init__ 可能会被多次调用，实际开发中需配合标志位防止重复初始化


# 工厂模式
class Dog:
    def bark(self): return "汪汪"

class Cat:
    def bark(self): return "喵喵"

# 简单工厂
class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        else:
            return None

# 使用
animal = AnimalFactory.create_animal("dog")
print(animal.bark()) # 输出：汪汪

# ============== 愤怒的小鸟 ==============


import random


# --- 目标类 ---
class Pig:
    def __init__(self, hp):
        self.hp = hp

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            print("🐷 猪被击败了！")
        else:
            print(f"🐷 猪还剩 {self.hp} 点血")


# --- 鸟类基类 ---
class Bird:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.__damage = 10  # 私有属性：基础攻击力

    # 普通攻击
    def hit(self, pig):
        print(f"🐦 {self.color}色的{self.name} 撞击了猪！")
        pig.take_damage(self.__damage)

    # 技能方法（留给子类重写 - 多态）
    def skill(self, pig):
        print(f"✨ {self.name} 没有特殊技能，只能普攻。")
        self.hit(pig)


# --- 红鸟 (无特殊技能，血量高) ---
class RedBird(Bird):
    def __init__(self):
        super().__init__("小红", "红")
        # 这里可以修改私有属性，或者增加新属性
        self._Bird__damage = 15  # 强制访问私有属性（不推荐，仅作演示）


# --- 黄鸟 (加速技能，伤害翻倍) ---
class YellowBird(Bird):
    def __init__(self):
        super().__init__("小黄", "黄")
        self.speed_boost = True

    def skill(self, pig):
        if self.speed_boost:
            print(f"⚡ {self.name} 发动了加速技能！伤害翻倍！")
            pig.take_damage(20)  # 特殊伤害逻辑
        else:
            self.hit(pig)


# --- 黑鸟 (爆炸技能，范围伤害) ---
class BlackBird(Bird):
    def __init__(self):
        super().__init__("小黑", "黑")

    def skill(self, pig):
        damage = random.randint(50, 100)
        print(f"💥 BOOM! {self.name} 爆炸了！造成 {damage} 点巨额伤害！")
        pig.take_damage(damage)


# --- 游戏主逻辑 ---
def play_game():
    print("--- 🎮 愤怒的小鸟：文字版 ---")
    target_pig = Pig(100)  # 创建一只100血的猪

    # 创建鸟的列表
    birds = [RedBird(), YellowBird(), BlackBird()]

    # 模拟发射鸟
    for bird in birds:
        print(f"\n准备发射：{bird.name}")
        if bird.name == "小黑":
            bird.skill(target_pig)  # 使用技能
        elif bird.name == "小黄":
            bird.skill(target_pig)
        else:
            bird.hit(target_pig)  # 普通攻击

        if target_pig.hp == 0:
            print("🏆 游戏胜利！")
            break


play_game()

"""
封装：用 __ 保护数据，用方法操作数据。
继承：class A(B):，避免重复代码。
多态：不同的鸟调用 skill() 方法，效果完全不同。
设计模式：
单例：重写 __new__，保证只有一个数据库连接。
工厂：用函数返回不同的对象实例。
"""