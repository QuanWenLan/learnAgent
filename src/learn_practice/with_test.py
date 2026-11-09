file = open('../../example.txt', 'r', encoding='utf-8')
try:
    content = file.read()
    # 按换行符分割内容
    lines = content.splitlines()

    # 打印每一行数据
    for i, line in enumerate(lines, 1):
        print(f"第{i}行数据: {line}")
finally:
    file.close()

'''
容易忘记关闭资源：如果没有 try-finally 块，可能会忘记调用 close()
代码冗长：简单的文件操作需要多行代码
异常处理复杂：需要手动处理可能出现的异常
'''

# with expression [as variable]:
#     # 代码块

'''
expression 返回一个支持上下文管理协议的对象
as variable 是可选的，用于将表达式结果赋值给变量
代码块执行完毕后，自动调用清理方法
'''

with open('../../example.txt', 'r', encoding='utf-8') as file:
    # 按换行符分割内容
    lines = content.splitlines()

    # 打印每一行数据
    for i, line in enumerate(lines, 1):
        print(f"第{i}行数据: {line}")
# 文件已自动关闭

# 同时打开多个文件
with open('../../example.txt', 'r', encoding='utf-8') as infile, open('../../output.txt', 'w', encoding='utf-8') as outfile:
    content = infile.read()
    outfile.write(content.upper())