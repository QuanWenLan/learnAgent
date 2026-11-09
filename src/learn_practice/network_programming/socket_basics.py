"""
Socket 网络编程基础教程 - 第一阶段
从零开始理解 TCP/UDP、Socket 编程和 HTTP 协议本质
"""

import socket
import threading
import time
from typing import Tuple


# ==================== 1. Socket 基础概念 ====================
def socket_basics():
    """
    Socket 是什么？
    
    Socket = IP地址 + 端口号
    类比：IP地址是大楼地址，端口号是房间号
    
    常见端口：
    - 80: HTTP
    - 443: HTTPS
    - 3306: MySQL
    - 6379: Redis
    - 9092: Kafka
    """
    print("\n" + "="*60)
    print("1. Socket 基础概念")
    print("="*60)
    
    # 获取本机信息
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"  主机名: {hostname}")
    print(f"  本地IP: {local_ip}")
    print(f"  localhost: {socket.gethostbyname('localhost')}")
    
    # Socket 类型
    print("\n  Socket 类型:")
    print(f"  - SOCK_STREAM (TCP): 可靠、有序、面向连接")
    print(f"  - SOCK_DGRAM (UDP): 快速、不可靠、无连接")
    print(f"  - SOCK_RAW (原始): 直接访问网络层")


# ==================== 2. TCP Socket 服务端 ====================
def tcp_server_basic():
    """
    最简单的 TCP 服务端
    
    流程：
    1. 创建 Socket
    2. 绑定地址和端口
    3. 监听连接
    4. 接受连接
    5. 收发数据
    6. 关闭连接
    """
    print("\n" + "="*60)
    print("2. TCP Socket 服务端（基础版）")
    print("="*60)
    
    def handle_client(client_socket: socket.socket, address: Tuple[str, int]):
        """处理客户端连接"""
        print(f"  [新连接] {address}")
        
        try:
            # 接收数据（阻塞）
            data = client_socket.recv(1024)
            if data:
                message = data.decode('utf-8')
                print(f"  [收到] 来自 {address}: {message}")
                
                # 发送响应
                response = f"服务器收到: {message}"
                client_socket.send(response.encode('utf-8'))
                print(f"  [发送] 到 {address}: {response}")
        except Exception as e:
            print(f"  [错误] 处理客户端失败: {e}")
        finally:
            client_socket.close()
            print(f"  [关闭] 连接 {address}")
    
    # 创建 TCP Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 设置选项：允许端口复用（避免重启时 Address already in use）
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # 绑定地址和端口
    host = '127.0.0.1'
    port = 9999
    server_socket.bind((host, port))
    
    # 开始监听（ backlog=5 表示最多等待5个连接）
    server_socket.listen(5)
    print(f"  服务器启动，监听 {host}:{port}")
    print(f"  提示：运行 tcp_client_basic() 来测试")
    
    try:
        while True:
            # 接受连接（阻塞，直到有客户端连接）
            client_socket, address = server_socket.accept()
            
            # 为每个客户端创建一个线程（简单但不够高效）
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\n  服务器关闭")
    finally:
        server_socket.close()


# ==================== 3. TCP Socket 客户端 ====================
def tcp_client_basic():
    """
    TCP 客户端
    
    流程：
    1. 创建 Socket
    2. 连接服务器
    3. 发送数据
    4. 接收响应
    5. 关闭连接
    """
    print("\n" + "="*60)
    print("3. TCP Socket 客户端（基础版）")
    print("="*60)
    
    # 创建 TCP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # 连接服务器
        host = '127.0.0.1'
        port = 9999
        print(f"  正在连接 {host}:{port}...")
        client_socket.connect((host, port))
        print(f"  ✓ 连接成功")
        
        # 发送数据
        message = "Hello, Server!"
        client_socket.send(message.encode('utf-8'))
        print(f"  [发送] {message}")
        
        # 接收响应（阻塞，直到收到数据或连接关闭）
        response = client_socket.recv(1024)
        print(f"  [收到] {response.decode('utf-8')}")
        
    except ConnectionRefusedError:
        print(f"  ✗ 连接失败：服务器未启动")
        print(f"  提示：先运行 tcp_server_basic()")
    except Exception as e:
        print(f"  ✗ 错误: {e}")
    finally:
        client_socket.close()
        print(f"  [关闭] 客户端连接")


# ==================== 4. UDP Socket 示例 ====================
def udp_example():
    """
    UDP Socket 示例
    
    UDP vs TCP:
    - UDP: 发出去就不管了，不保证到达
    - TCP: 确保数据完整到达，但速度慢
    
    适用场景：
    - UDP: 视频直播、DNS查询、在线游戏
    - TCP: 网页浏览、文件传输、邮件
    """
    print("\n" + "="*60)
    print("4. UDP Socket 示例")
    print("="*60)
    
    def udp_server():
        """UDP 服务端"""
        print("\n  [UDP 服务器] 启动...")
        
        # 创建 UDP Socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('127.0.0.1', 10000))
        
        print(f"  [UDP 服务器] 监听 127.0.0.1:10000")
        
        try:
            # 接收数据（不需要 accept，UDP 是无连接的）
            data, address = server_socket.recvfrom(1024)
            message = data.decode('utf-8')
            print(f"  [UDP 服务器] 收到来自 {address}: {message}")
            
            # 发送响应
            response = f"UDP 服务器收到: {message}"
            server_socket.sendto(response.encode('utf-8'), address)
            print(f"  [UDP 服务器] 发送响应到 {address}")
        finally:
            server_socket.close()
    
    def udp_client():
        """UDP 客户端"""
        print("\n  [UDP 客户端] 启动...")
        
        # 创建 UDP Socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # 设置超时（UDP 可能丢包，需要超时机制）
        client_socket.settimeout(3.0)
        
        try:
            # 发送数据（不需要 connect，直接指定目标地址）
            message = "Hello, UDP Server!"
            server_address = ('127.0.0.1', 10000)
            client_socket.sendto(message.encode('utf-8'), server_address)
            print(f"  [UDP 客户端] 发送: {message}")
            
            # 接收响应
            data, address = client_socket.recvfrom(1024)
            print(f"  [UDP 客户端] 收到: {data.decode('utf-8')}")
        except socket.timeout:
            print(f"  [UDP 客户端] 超时，服务器可能未启动")
        finally:
            client_socket.close()
    
    # 注意：UDP 示例需要手动分别运行服务端和客户端
    print("  提示：UDP 是无连接的，可以分别运行服务端和客户端")
    print("  先在一个终端运行 udp_server()，再在另一个终端运行 udp_client()")


# ==================== 5. 用 Socket 实现 HTTP 客户端 ====================
def http_client_with_socket():
    """
    用原生 Socket 实现 HTTP 客户端
    
    这就是 requests 库底层做的事情！
    
    HTTP 请求格式：
    GET / HTTP/1.1
    Host: www.baidu.com
    [空行]
    
    HTTP 响应格式：
    HTTP/1.1 200 OK
    Content-Type: text/html
    [空行]
    <html>...</html>
    """
    print("\n" + "="*60)
    print("5. 用 Socket 实现 HTTP 客户端")
    print("="*60)
    
    def simple_http_get(host: str, path: str = "/", port: int = 80) -> str:
        """
        简单的 HTTP GET 请求
        
        Args:
            host: 域名或IP
            path: 路径
            port: 端口（默认80）
        """
        # 创建 TCP Socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # 设置超时
            sock.settimeout(5.0)
            
            # 连接服务器
            print(f"  连接到 {host}:{port}...")
            sock.connect((host, port))
            print(f"  ✓ TCP 连接建立（三次握手完成）")
            
            # 构造 HTTP 请求
            request = f"GET {path} HTTP/1.1\r\n"
            request += f"Host: {host}\r\n"
            request += "Connection: close\r\n"  # 告诉服务器发送完就关闭连接
            request += "\r\n"  # 空行，表示请求头结束
            
            # 发送请求
            sock.send(request.encode('utf-8'))
            print(f"  [发送] HTTP 请求")
            
            # 接收响应
            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            return response.decode('utf-8', errors='ignore')
        
        except socket.timeout:
            return "错误：连接超时"
        except Exception as e:
            return f"错误：{e}"
        finally:
            sock.close()
            print(f"  [关闭] TCP 连接（四次挥手）")
    
    # 测试1：访问百度
    print("\n  测试1: GET http://www.baidu.com/")
    response = simple_http_get("www.baidu.com", "/", 80)
    
    # 只显示响应头和前200个字符的响应体
    lines = response.split('\r\n')
    print(f"  响应状态行: {lines[0]}")
    print(f"  响应头:")
    for line in lines[1:]:
        if line == "":  # 空行，表示响应头结束
            break
        print(f"    {line}")
    
    # 找到响应体
    body_start = response.find('\r\n\r\n')
    if body_start != -1:
        body = response[body_start + 4:body_start + 204]
        print(f"  响应体（前200字符）: {body[:200]}...")


# ==================== 6. Socket 选项和配置 ====================
def socket_options():
    """
    常用的 Socket 选项
    
    这些选项影响连接的行为
    """
    print("\n" + "="*60)
    print("6. Socket 选项和配置")
    print("="*60)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # 1. SO_REUSEADDR: 允许重用地址（开发时很有用）
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("  ✓ SO_REUSEADDR: 允许端口复用")
    
    # 2. SO_KEEPALIVE: 启用 TCP 保活机制
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    print("  ✓ SO_KEEPALIVE: 启用 TCP 保活（检测死连接）")
    
    # 3. SO_TIMEOUT: 设置超时
    sock.settimeout(5.0)
    print("  ✓ SO_TIMEOUT: 设置超时为 5 秒")
    
    # 4. TCP_NODELAY: 禁用 Nagle 算法（减少延迟）
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    print("  ✓ TCP_NODELAY: 禁用 Nagle 算法（适合实时应用）")
    
    # 5. SO_SNDBUF/SO_RCVBUF: 设置缓冲区大小
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)  # 64KB
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
    print("  ✓ SO_SNDBUF/SO_RCVBUF: 设置发送/接收缓冲区为 64KB")
    
    sock.close()
    
    print("\n  实际应用场景:")
    print("  - Web 服务器: SO_REUSEADDR（快速重启）")
    print("  - 即时通讯: TCP_NODELAY（降低延迟）")
    print("  - 长连接服务: SO_KEEPALIVE（检测断线）")
    print("  - 所有网络程序: SO_TIMEOUT（防止永久阻塞）")


# ==================== 7. 粘包问题及解决方案 ====================
def sticky_packet_problem():
    """
    TCP 粘包问题
    
    TCP 是流式协议，没有"消息边界"的概念
    发送方发送两次，接收方可能一次收到，也可能分多次收到
    
    解决方案：
    1. 固定长度
    2. 特殊分隔符
    3. 长度前缀（最常用）
    """
    print("\n" + "="*60)
    print("7. TCP 粘包问题及解决方案")
    print("="*60)
    
    print("\n  问题演示:")
    print("  发送方: send('Hello') + send('World')")
    print("  接收方可能收到: 'HelloWorld' 或 'Hel' + 'loWorld'")
    
    print("\n  解决方案1: 长度前缀（推荐）")
    print("  格式: [4字节长度][数据]")
    print("  例如: [0005][Hello][0005][World]")
    
    def send_with_length(sock: socket.socket, message: str):
        """发送带长度前缀的消息"""
        # 编码消息
        data = message.encode('utf-8')
        # 发送长度（4字节，大端序）
        length = len(data)
        sock.sendall(length.to_bytes(4, byteorder='big'))
        # 发送数据
        sock.sendall(data)
        print(f"  [发送] 长度={length}, 消息={message}")
    
    def recv_with_length(sock: socket.socket) -> str:
        """接收带长度前缀的消息"""
        # 接收长度（4字节）
        length_bytes = sock.recv(4)
        if len(length_bytes) < 4:
            raise ConnectionError("连接关闭")
        
        length = int.from_bytes(length_bytes, byteorder='big')
        
        # 接收数据
        data = b""
        while len(data) < length:
            chunk = sock.recv(min(4096, length - len(data)))
            if not chunk:
                raise ConnectionError("连接关闭")
            data += chunk
        
        message = data.decode('utf-8')
        print(f"  [接收] 长度={length}, 消息={message}")
        return message
    
    print("\n  这种方案被广泛应用于:")
    print("  - Protocol Buffers")
    print("  - MessagePack")
    print("  - Kafka 协议")
    print("  - Redis 协议")


# ==================== 8. 实战：简单的聊天室 ====================
def simple_chat_room():
    """
    简单的聊天室
    
    功能：
    - 多个客户端可以连接
    - 一个客户端发送消息，其他客户端都能收到
    - 使用 threading 处理多客户端
    """
    print("\n" + "="*60)
    print("8. 实战：简单的聊天室")
    print("="*60)
    
    # 存储所有客户端连接
    clients = []
    clients_lock = threading.Lock()
    
    def broadcast(message: str, sender_sock: socket.socket = None):
        """广播消息给所有客户端"""
        with clients_lock:
            for client in clients:
                if client != sender_sock:  # 不发给发送者自己
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        pass  # 客户端可能已断开
    
    def handle_client_chat(client_socket: socket.socket, address: Tuple[str, int]):
        """处理聊天客户端"""
        print(f"  [聊天室] {address} 加入")
        
        # 添加到客户端列表
        with clients_lock:
            clients.append(client_socket)
        
        # 通知其他人
        broadcast(f"[系统] {address} 加入了聊天室\n")
        
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                print(f"  [聊天室] {address}: {message}")
                
                # 广播给其他人
                broadcast(f"[{address}] {message}\n", sender_sock=client_socket)
        except Exception as e:
            print(f"  [聊天室] {address} 错误: {e}")
        finally:
            # 移除客户端
            with clients_lock:
                if client_socket in clients:
                    clients.remove(client_socket)
            client_socket.close()
            broadcast(f"[系统] {address} 离开了聊天室\n")
            print(f"  [聊天室] {address} 离开")
    
    def chat_server():
        """聊天室服务器"""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('127.0.0.1', 11000))
        server_socket.listen(10)
        
        print(f"  聊天室服务器启动: 127.0.0.1:11000")
        print(f"  提示：用 telnet 127.0.0.1 11000 连接测试")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                thread = threading.Thread(
                    target=handle_client_chat,
                    args=(client_socket, address)
                )
                thread.daemon = True
                thread.start()
        finally:
            server_socket.close()
    
    print("\n  使用方法:")
    print("  1. 在一个终端运行: chat_server()")
    print("  2. 打开多个终端，运行: telnet 127.0.0.1 11000")
    print("  3. 在一个窗口输入消息，其他窗口会收到")


# ==================== 主函数 ====================
def main():
    """运行所有示例"""
    print("="*60)
    print("Socket 网络编程基础教程 - 第一阶段")
    print("="*60)
    
    examples = [
        ("Socket 基础概念", socket_basics),
        ("Socket 选项和配置", socket_options),
        ("TCP 粘包问题", sticky_packet_problem),
        ("HTTP 客户端实现", http_client_with_socket),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n{name} 执行出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("交互式示例（需要手动运行）:")
    print("  1. TCP 服务端: tcp_server_basic()")
    print("  2. TCP 客户端: tcp_client_basic()")
    print("  3. UDP 示例: udp_example()")
    print("  4. 聊天室: simple_chat_room()")
    print("="*60)
    
    print("\n学习建议:")
    print("  1. 先阅读代码，理解每个步骤的作用")
    print("  2. 运行 tcp_server_basic()，然后用 telnet 测试")
    print("  3. 修改代码，尝试不同的 Socket 选项")
    print("  4. 理解 TCP vs UDP 的区别")
    print("  5. 掌握 HTTP 协议的文本格式")


if __name__ == "__main__":
    main()
