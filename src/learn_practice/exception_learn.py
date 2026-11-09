"""
Python 异常完全指南
===================
本文件演示 Python 中常用的内置异常及其使用场景
"""

import json
import os


# ==========================================
# 第一部分：基础异常处理示例
# ==========================================

def divide(a, b):
    """安全的除法运算"""
    try:
        result = a / b
    except ZeroDivisionError as e:
        # 异常链：在抛出ValueError时，保留原始的ZeroDivisionError信息
        raise ValueError("除数不能为零") from e
    else:
        print("计算成功！")
        return result
    finally:
        print("无论是否出错，finally都会执行（如关闭资源）")


try:
    print(divide(10, 0))
except ValueError as e:
    print(f"捕获到业务异常: {e}")


# ==========================================
# 第二部分：Python 常用内置异常详解
# ==========================================

print("\n" + "=" * 60)
print("Python 常用内置异常详解")
print("=" * 60)


# 1. AttributeError - 属性错误
print("\n【1】AttributeError - 访问不存在的属性")
try:
    my_list = [1, 2, 3]
    my_list.nonexistent_method()
except AttributeError as e:
    print(f"❌ AttributeError: {e}")


# 2. TypeError - 类型错误
print("\n【2】TypeError - 类型错误")
try:
    result = "hello" + 5
except TypeError as e:
    print(f"❌ TypeError: {e}")

try:
    len(123)
except TypeError as e:
    print(f"❌ TypeError: {e}")


# 3. ValueError - 值错误
print("\n【3】ValueError - 值错误")
try:
    int("not_a_number")
except ValueError as e:
    print(f"❌ ValueError: {e}")

try:
    import math
    math.sqrt(-1)
except ValueError as e:
    print(f"❌ ValueError: {e}")


# 4. KeyError - 键错误
print("\n【4】KeyError - 字典键不存在")
try:
    my_dict = {"name": "Alice", "age": 25}
    print(my_dict["address"])
except KeyError as e:
    print(f"❌ KeyError: {e}")
    print(f"   提示：使用 dict.get('key', default) 避免此错误")


# 5. IndexError - 索引错误
print("\n【5】IndexError - 列表索引越界")
try:
    my_list = [1, 2, 3]
    print(my_list[10])
except IndexError as e:
    print(f"❌ IndexError: {e}")


# 6. FileNotFoundError - 文件未找到
print("\n【6】FileNotFoundError - 文件不存在")
try:
    with open("nonexistent_file.txt", "r") as f:
        content = f.read()
except FileNotFoundError as e:
    print(f"❌ FileNotFoundError: {e}")


# 7. IOError/OSError - IO 错误
print("\n【7】IOError/OSError - IO 操作错误")
try:
    with open("/root/protected_file.txt", "w") as f:
        f.write("test")
except PermissionError as e:
    print(f"❌ PermissionError: {e}")
except OSError as e:
    print(f"❌ OSError: {e}")


# 8. ImportError - 导入错误
print("\n【8】ImportError - 模块导入失败")
try:
    import nonexistent_module
except ImportError as e:
    print(f"❌ ImportError: {e}")


# 9. ModuleNotFoundError - 模块未找到（ImportError 的子类）
print("\n【9】ModuleNotFoundError - 模块未找到")
try:
    from nonexistent_package import something
except ModuleNotFoundError as e:
    print(f"❌ ModuleNotFoundError: {e}")


# 10. NameError - 名称错误
print("\n【10】NameError - 变量未定义")
try:
    print(undefined_variable)
except NameError as e:
    print(f"❌ NameError: {e}")


# 11. SyntaxError - 语法错误（通常在编译时捕获）
print("\n【11】SyntaxError - 语法错误")
try:
    eval("if True print('hello')")  # 缺少冒号
except SyntaxError as e:
    print(f"❌ SyntaxError: {e}")


# 12. IndentationError - 缩进错误（SyntaxError 的子类）
print("\n【12】IndentationError - 缩进错误")
try:
    exec("def test():\nprint('hello')")  # 缺少缩进
except IndentationError as e:
    print(f"❌ IndentationError: {e}")


# 13. StopIteration - 迭代器停止
print("\n【13】StopIteration - 迭代器耗尽")
try:
    my_iter = iter([1, 2])
    print(next(my_iter))  # 1
    print(next(my_iter))  # 2
    print(next(my_iter))  # 抛出 StopIteration
except StopIteration:
    print("❌ StopIteration: 迭代器已耗尽")


# 14. GeneratorExit - 生成器退出
print("\n【14】GeneratorExit - 生成器关闭")


def my_generator():
    try:
        yield 1
        yield 2
    except GeneratorExit:
        print("   生成器被提前关闭")
        raise


gen = my_generator()
print(next(gen))
gen.close()  # 触发 GeneratorExit


# 15. RuntimeError - 运行时错误
print("\n【15】RuntimeError - 运行时错误")
try:
    raise RuntimeError("这是一个运行时错误")
except RuntimeError as e:
    print(f"❌ RuntimeError: {e}")


# 16. RecursionError - 递归深度超限
print("\n【16】RecursionError - 递归深度超限")
try:
    def infinite_recursion(n):
        return infinite_recursion(n + 1)

    infinite_recursion(0)
except RecursionError as e:
    print(f"❌ RecursionError: {e}")


# 17. MemoryError - 内存不足
print("\n【17】MemoryError - 内存不足")
try:
    # 尝试创建超大列表（可能不会在所有系统上触发）
    huge_list = [0] * (10 ** 10)
except MemoryError as e:
    print(f"❌ MemoryError: {e}")


# 18. AssertionError - 断言失败
print("\n【18】AssertionError - 断言失败")
try:
    x = 5
    assert x > 10, "x 应该大于 10"
except AssertionError as e:
    print(f"❌ AssertionError: {e}")


# 19. NotImplementedError - 方法未实现
print("\n【19】NotImplementedError - 抽象方法未实现")


class BaseClass:
    def abstract_method(self):
        raise NotImplementedError("子类必须实现此方法")


try:
    obj = BaseClass()
    obj.abstract_method()
except NotImplementedError as e:
    print(f"❌ NotImplementedError: {e}")


# 20. UnicodeDecodeError/UnicodeEncodeError - 编码错误
print("\n【20】Unicode 编码错误")
try:
    b"\xff".decode("utf-8")
except UnicodeDecodeError as e:
    print(f"❌ UnicodeDecodeError: {e}")

try:
    "你好".encode("ascii")
except UnicodeEncodeError as e:
    print(f"❌ UnicodeEncodeError: {e}")


# 21. JSONDecodeError - JSON 解析错误
print("\n【21】JSONDecodeError - JSON 格式错误")
try:
    json.loads("{invalid json}")
except json.JSONDecodeError as e:
    print(f"❌ JSONDecodeError: {e}")


# 22. ConnectionError 及其子类 - 网络错误
print("\n【22】ConnectionError - 网络连接错误")
try:
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    sock.connect(("nonexistent.host.com", 80))
except ConnectionError as e:
    print(f"❌ ConnectionError: {e}")
except socket.gaierror as e:
    print(f"❌ socket.gaierror (DNS解析失败): {e}")
except socket.timeout as e:
    print(f"❌ socket.timeout (连接超时): {e}")
finally:
    sock.close()


# ==========================================
# 第三部分：异常继承层次结构
# ==========================================

print("\n" + "=" * 60)
print("异常继承层次结构")
print("=" * 60)

"""
BaseException
 ├── SystemExit              # sys.exit() 抛出
 ├── KeyboardInterrupt       # Ctrl+C 中断
 ├── GeneratorExit           # 生成器关闭
 └── Exception               # 所有常规异常的基类
      ├── AttributeError
      ├── EOFError
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── NameError
      ├── OSError
      │    ├── FileNotFoundError
      │    ├── PermissionError
      │    └── TimeoutError
      ├── RuntimeError
      │    ├── RecursionError
      │    └── NotImplementedError
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         └── UnicodeEncodeError
      ├── ArithmeticError
      │    ├── ZeroDivisionError
      │    ├── OverflowError
      │    └── FloatingPointError
      ├── AssertionError
      ├── BufferError
      ├── MemoryError
      └── Warning            # 警告的基类
           ├── DeprecationWarning
           ├── FutureWarning
           └── UserWarning
"""

print("""
异常继承树（简化版）:
├── BaseException
│    ├── SystemExit          # 系统退出
│    ├── KeyboardInterrupt   # 用户中断 (Ctrl+C)
│    └── Exception           # ⭐ 我们主要处理的异常
│         ├── ArithmeticError
│         │    └── ZeroDivisionError
│         ├── AttributeError
│         ├── EOFError
│         ├── ImportError → ModuleNotFoundError
│         ├── LookupError
│         │    ├── IndexError
│         │    └── KeyError
│         ├── NameError
│         ├── OSError
│         │    ├── FileNotFoundError
│         │    ├── PermissionError
│         │    └── TimeoutError
│         ├── RuntimeError → RecursionError
│         ├── StopIteration
│         ├── SyntaxError → IndentationError
│         ├── TypeError
│         ├── ValueError → UnicodeError
│         ├── AssertionError
│         ├── MemoryError
│         └── NotImplementedError
""")


# ==========================================
# 第四部分：自定义异常
# ==========================================

print("\n" + "=" * 60)
print("自定义异常")
print("=" * 60)


class AppError(Exception):
    """应用基础异常类"""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.message = message
        self.code = code


class ConfigError(AppError):
    """配置相关异常"""
    pass


class DatabaseError(AppError):
    """数据库相关异常"""
    pass


class BusinessError(AppError):
    """业务逻辑异常"""
    pass


class ValidationError(AppError):
    """数据验证异常"""
    pass


# 测试自定义异常
try:
    raise ConfigError("配置文件格式错误", code="CFG_001")
except AppError as e:
    print(f"✅ 捕获自定义异常: {type(e).__name__}")
    print(f"   消息: {e.message}")
    print(f"   代码: {e.code}")


# ==========================================
# 第五部分：实际应用场景
# ==========================================

print("\n" + "=" * 60)
print("实际应用场景")
print("=" * 60)


# 场景1：读取配置文件
def read_config(filepath):
    """读取 JSON 配置文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise ConfigError(f"配置文件不存在: {filepath}", code="CFG_002") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"配置文件格式错误: {filepath}", code="CFG_003") from e
    except PermissionError as e:
        raise ConfigError(f"无权限读取配置文件: {filepath}", code="CFG_004") from e


# 场景2：数据库操作
class MockDB:
    """模拟数据库"""

    def execute(self, sql, data):
        if "error" in sql.lower():
            raise Exception("SQL 执行失败")
        return {"id": 1, **data}

    def close(self):
        print("   数据库连接已关闭")


db = MockDB()


def save_user(user_data):
    """保存用户到数据库"""
    try:
        result = db.execute("INSERT INTO users ...", user_data)
        return result
    except Exception as e:
        raise BusinessError("用户保存失败", code="DB_001") from e
    finally:
        db.close()


try:
    user = save_user({"name": "张三", "email": "zhangsan@example.com"})
    print(f"✅ 用户保存成功: {user}")
except BusinessError as e:
    print(f"❌ 业务异常: {e.message} (代码: {e.code})")


# 场景3：数据验证
def validate_email(email):
    """验证邮箱格式"""
    if not email or "@" not in email:
        raise ValidationError(f"无效的邮箱地址: {email}", code="VAL_001")
    return True


try:
    validate_email("invalid-email")
except ValidationError as e:
    print(f"❌ 验证失败: {e.message} (代码: {e.code})")


# 场景4：多重异常捕获
def process_data(data):
    """处理数据，可能抛出多种异常"""
    try:
        if not isinstance(data, dict):
            raise TypeError("数据必须是字典类型")

        value = data["value"]

        if not isinstance(value, (int, float)):
            raise ValueError("值必须是数字")

        result = 100 / value
        return result

    except TypeError as e:
        print(f"   类型错误: {e}")
        return None
    except ValueError as e:
        print(f"   值错误: {e}")
        return None
    except KeyError as e:
        print(f"   键缺失: {e}")
        return None
    except ZeroDivisionError as e:
        print(f"   除零错误: {e}")
        return None


print("\n数据处理测试:")
print(f"process_data({{'value': 10}}) = {process_data({'value': 10})}")
print(f"process_data({{'value': 0}}) = {process_data({'value': 0})}")
print(f"process_data({{'value': 'abc'}}) = {process_data({'value': 'abc'})}")
print(f"process_data({{'other': 10}}) = {process_data({'other': 10})}")
print(f"process_data('not a dict') = {process_data('not a dict')}")


# 场景5：使用 else 和 finally
def safe_divide(a, b):
    """安全除法，展示完整的 try-except-else-finally"""
    try:
        result = a / b
    except ZeroDivisionError:
        print("   捕获到除零错误")
        return None
    except TypeError:
        print("   捕获到类型错误")
        return None
    else:
        # 只有在没有异常时才执行
        print(f"   计算成功: {a} / {b} = {result}")
        return result
    finally:
        # 无论如何都执行
        print("   清理资源")


print("\n安全除法测试:")
safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "2")


# ==========================================
# 第六部分：最佳实践总结
# ==========================================

print("\n" + "=" * 60)
print("异常处理最佳实践")
print("=" * 60)

print("""
✅ 推荐做法:
1. 精确捕获异常 - 避免使用裸 except
   ❌ try: ... except: ...
   ✅ try: ... except ValueError: ...

2. 使用异常链 - 保留原始错误信息
   ✅ raise NewError("msg") from original_error

3. 自定义异常 - 建立异常层次结构
   class AppError(Exception): ...
   class BusinessError(AppError): ...

4. 资源清理 - 使用 finally 或 context manager
   ✅ with open(file) as f: ...
   ✅ try: ... finally: cleanup()

5. 不要静默吞掉异常
   ❌ except: pass
   ✅ except: logger.error(...)

6. 区分可恢复和不可恢复错误
   - 可恢复: 重试、降级、默认值
   - 不可恢复: 记录日志、向上抛出

7. 使用 else 子句
   - try: 可能出错的代码
   - except: 异常处理
   - else: 正常执行的业务逻辑
   - finally: 清理工作

8. 记录异常上下文
   ✅ logging.exception("详细错误信息")
   - 自动包含堆栈跟踪

常见异常速查表:
┌─────────────────────┬──────────────────────────┐
│ 异常类型             │ 触发场景                  │
├─────────────────────┼──────────────────────────┤
│ TypeError           │ 类型不匹配                │
│ ValueError          │ 值不正确                  │
│ KeyError            │ 字典键不存在              │
│ IndexError          │ 列表索引越界              │
│ AttributeError      │ 属性/方法不存在           │
│ FileNotFoundError   │ 文件不存在                │
│ PermissionError     │ 权限不足                  │
│ ImportError         │ 模块导入失败              │
│ NameError           │ 变量未定义                │
│ ZeroDivisionError   │ 除以零                    │
│ AssertionError      │ 断言失败                  │
│ StopIteration       │ 迭代器耗尽                │
│ RuntimeError        │ 运行时错误                │
│ RecursionError      │ 递归深度超限              │
│ MemoryError         │ 内存不足                  │
│ NotImplementedError │ 方法未实现                │
│ JSONDecodeError     │ JSON 解析失败             │
│ ConnectionError     │ 网络连接失败              │
└─────────────────────┴──────────────────────────┘
""")

print("\n✅ 所有异常示例执行完毕!")
