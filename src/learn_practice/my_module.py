"""
1. __all__ 的作用
在模块中定义 __all__ 列表，可以控制当别人使用 from 模块名 import * 时，哪些函数或类会被导出。这是一种很好的封装习惯。
2. 模块制作、打包与安装
制作模块：本质上就是一个 .py 文件。
打包：通过编写 setup.py 文件，使用 setuptools 将你的模块打包成 .whl 或 .tar.gz 格式。
安装与使用：打包后，可以通过 pip install 你的包文件.whl 进行本地安装，或者上传到 PyPI 供全球开发者使用。
"""

# --- my_module.py ---
__all__ = ['public_func']  # 只允许外部通过 import * 导入 public_func

def public_func():
    return "我是对外公开的函数"

def _private_func():
    return "我是内部使用的私有函数"

# --- 打包用的 setup.py (简略版) ---
# from setuptools import setup
# setup(
#     name="my_module",
#     version="0.1.0",
#     py_modules=["my_module"],
# )