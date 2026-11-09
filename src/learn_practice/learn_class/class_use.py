from learn_practice.learn_class.student import Student
# from learn_practice.my_module import *   _private_func() 导入不了
from learn_practice.my_module import public_func, _private_func  # 这样才可以

def print_student_param(student: Student):
    print(student.name, student.age)
    pass

def test_import():
    """测试 my_module 的导包功能"""
    print("=" * 50)
    print("测试 my_module 导包")
    print("=" * 50)

    # 1. 测试导入公开函数
    print("\n1. 调用公开函数:")
    result = public_func()
    print(f"   {result}")

    # 2. 测试导入私有函数（虽然可以导入，但不推荐）
    print("\n2. 调用私有函数（不推荐）:")
    result = _private_func()
    print(f"   {result}")

    # 3. 测试 import * （只会导入 __all__ 中定义的）
    print("\n3. 测试 from my_module import *:")
    from learn_practice import my_module

    # 查看模块中所有公开的属性和函数
    print(f"   模块中的公开成员: {[name for name in dir(my_module) if not name.startswith('_')]}")
    print(f"   __all__ 定义的内容: {my_module.__all__}")

if __name__ == "__main__":
    new_student = Student("小王", 18)
    print_student_param(new_student)
