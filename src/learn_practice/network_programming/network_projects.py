"""
网络编程实战项目 - 第二阶段
通过实际项目深化理解：聊天服务器、HTTP 服务、性能对比
"""

import asyncio
import socket
import threading
import time
import json
from typing import Dict, List, Set
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field


# ==================== 项目1：聊天服务器（三个版本对比）====================

@dataclass
class ChatMessage:
    """聊天消息数据结构"""
    sender: str
    content: str
    timestamp: float = field(default_factory=time.time)
    
    def to_json(self) -> str:
        return json.dumps({
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp
        })
    
    @classmethod
    def from_json(cls, json_str: str) -> 'ChatMessage':
        data = json.loads(json_str)
        return cls(**data)


# --- 版本1：使用 threading + Socket（阻塞 IO）---
class ThreadedChatServer:
    """
    版本1：基于线程的聊天服务器
    
    特点：
    - 每个客户端一个线程
    - 代码简单直观
    - 并发能力有限（线程切换开销）
    - 适合 < 100 个并发连接
    """
    
    def __init__(self, host='127.0.0.1', port=12000):
        self.host = host
        self.port = port
        self.clients: Dict[str, socket.socket] = {}
        self.lock = threading.Lock()
        self.server_socket = None
    
    def start(self):
        """启动服务器"""
        print("\n" + "="*60)
        print("聊天服务器 v1: Threading + Socket")
        print("="*60)
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(50)
        
        print(f"  服务器启动: {self.host}:{self.port}")
        print(f"  最大并发: ~50 个客户端")
        
        try:
            while True:
                client_socket, address = self.server_socket.accept()
                client_id = f"{address[0]}:{address[1]}"
                
                # 为每个客户端创建线程
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, client_id),
                    daemon=True
                )
                thread.start()
                print(f"  [新连接] {client_id} (活跃: {len(self.clients)})")
        
        except KeyboardInterrupt:
            print("\n  服务器关闭")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket: socket.socket, client_id: str):
        """处理单个客户端"""
        with self.lock:
            self.clients[client_id] = client_socket
        
        try:
            # 发送欢迎消息
            welcome = ChatMessage(
                sender="系统",
                content=f"欢迎 {client_id} 加入聊天室！"
            )
            self.broadcast(welcome.to_json(), exclude=client_id)
            
            # 接收消息
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                if message:
                    chat_msg = ChatMessage(sender=client_id, content=message)
                    print(f"  [{client_id}] {message}")
                    
                    # 广播给其他人
                    self.broadcast(chat_msg.to_json(), exclude=client_id)
        
        except Exception as e:
            print(f"  [错误] {client_id}: {e}")
        finally:
            self.remove_client(client_id)
            client_socket.close()
    
    def broadcast(self, message: str, exclude: str = None):
        """广播消息"""
        with self.lock:
            for client_id, client_socket in list(self.clients.items()):
                if client_id != exclude:
                    try:
                        client_socket.send(message.encode('utf-8') + b'\n')
                    except:
                        self.remove_client(client_id)
    
    def remove_client(self, client_id: str):
        """移除客户端"""
        with self.lock:
            if client_id in self.clients:
                del self.clients[client_id]
                print(f"  [断开] {client_id} (活跃: {len(self.clients)})")
                
                # 通知其他人
                leave_msg = ChatMessage(
                    sender="系统",
                    content=f"{client_id} 离开了聊天室"
                )
                # 注意：这里不能再调用 broadcast，避免死锁
                for cid, csock in list(self.clients.items()):
                    try:
                        csock.send(leave_msg.to_json().encode('utf-8') + b'\n')
                    except:
                        pass
    
    def shutdown(self):
        """关闭服务器"""
        if self.server_socket:
            self.server_socket.close()


# --- 版本2：使用 asyncio（非阻塞 IO）---
class AsyncChatServer:
    """
    版本2：基于 asyncio 的聊天服务器
    
    特点：
    - 单线程处理所有连接
    - 高并发能力（上万连接）
    - 代码稍复杂
    - 适合 I/O 密集型高并发场景
    """
    
    def __init__(self, host='127.0.0.1', port=12001):
        self.host = host
        self.port = port
        self.clients: Dict[str, asyncio.StreamWriter] = {}
    
    async def start(self):
        """启动服务器"""
        print("\n" + "="*60)
        print("聊天服务器 v2: asyncio")
        print("="*60)
        
        server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port
        )
        
        print(f"  服务器启动: {self.host}:{self.port}")
        print(f"  最大并发: 理论无限制（受内存限制）")
        
        async with server:
            await server.serve_forever()
    
    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """处理单个客户端"""
        address = writer.get_extra_info('peername')
        client_id = f"{address[0]}:{address[1]}"
        
        print(f"  [新连接] {client_id} (活跃: {len(self.clients)})")
        
        # 注册客户端
        self.clients[client_id] = writer
        
        try:
            # 发送欢迎消息
            welcome = ChatMessage(
                sender="系统",
                content=f"欢迎 {client_id} 加入聊天室！（异步版）"
            )
            await self.broadcast(welcome.to_json(), exclude=client_id)
            
            # 接收消息
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                if message:
                    chat_msg = ChatMessage(sender=client_id, content=message)
                    print(f"  [{client_id}] {message}")
                    
                    # 广播给其他人
                    await self.broadcast(chat_msg.to_json(), exclude=client_id)
        
        except Exception as e:
            print(f"  [错误] {client_id}: {e}")
        finally:
            await self.remove_client(client_id)
            writer.close()
            await writer.wait_closed()
    
    async def broadcast(self, message: str, exclude: str = None):
        """广播消息"""
        data = (message + '\n').encode('utf-8')
        
        tasks = []
        for client_id, writer in list(self.clients.items()):
            if client_id != exclude:
                try:
                    writer.write(data)
                    tasks.append(writer.drain())
                except:
                    await self.remove_client(client_id)
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def remove_client(self, client_id: str):
        """移除客户端"""
        if client_id in self.clients:
            del self.clients[client_id]
            print(f"  [断开] {client_id} (活跃: {len(self.clients)})")
            
            # 通知其他人
            leave_msg = ChatMessage(
                sender="系统",
                content=f"{client_id} 离开了聊天室"
            )
            await self.broadcast(leave_msg.to_json())


# ==================== 项目2：简易 HTTP 服务器 ====================
class SimpleHTTPServer:
    """
    从零实现 HTTP 服务器
    
    理解：
    - HTTP 请求/响应格式
    - URL 路由
    - 静态文件服务
    - JSON API
    """
    
    def __init__(self, host='127.0.0.1', port=13000):
        self.host = host
        self.port = port
        self.routes: Dict[str, callable] = {}
    
    def route(self, path: str):
        """装饰器：注册路由"""
        def decorator(func: callable):
            self.routes[path] = func
            return func
        return decorator
    
    def start(self):
        """启动 HTTP 服务器"""
        print("\n" + "="*60)
        print("简易 HTTP 服务器")
        print("="*60)
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(10)
        
        print(f"  服务器启动: http://{self.host}:{self.port}")
        print(f"  已注册路由: {list(self.routes.keys())}")
        print(f"  测试: curl http://{self.host}:{self.port}/hello")
        
        try:
            while True:
                client_socket, address = server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_request,
                    args=(client_socket, address),
                    daemon=True
                )
                thread.start()
        finally:
            server_socket.close()
    
    def handle_request(self, client_socket: socket.socket, address):
        """处理 HTTP 请求"""
        try:
            # 接收请求
            request_data = client_socket.recv(4096).decode('utf-8')
            if not request_data:
                return
            
            # 解析请求行
            lines = request_data.split('\r\n')
            request_line = lines[0]
            method, path, version = request_line.split(' ')
            
            print(f"  [{method}] {path} from {address}")
            
            # 查找路由
            if path in self.routes:
                handler = self.routes[path]
                status, headers, body = handler()
            else:
                status = "404 Not Found"
                headers = {"Content-Type": "text/plain"}
                body = "404 Not Found"
            
            # 构造响应
            response = f"HTTP/1.1 {status}\r\n"
            for key, value in headers.items():
                response += f"{key}: {value}\r\n"
            response += "\r\n"
            response += body
            
            # 发送响应
            client_socket.send(response.encode('utf-8'))
        
        except Exception as e:
            print(f"  [错误] 处理请求失败: {e}")
        finally:
            client_socket.close()
    
    def run_demo(self):
        """运行演示"""
        # 注册路由
        @self.route("/hello")
        def hello():
            return (
                "200 OK",
                {"Content-Type": "text/plain"},
                "Hello, World!"
            )
        
        @self.route("/json")
        def json_api():
            data = {
                "message": "Hello from JSON API",
                "timestamp": time.time(),
                "server": "SimpleHTTPServer"
            }
            return (
                "200 OK",
                {"Content-Type": "application/json"},
                json.dumps(data, indent=2)
            )
        
        @self.route("/time")
        def get_time():
            return (
                "200 OK",
                {"Content-Type": "text/plain"},
                f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        
        # 启动服务器
        self.start()


# ==================== 项目3：性能对比实验 ====================
class PerformanceComparison:
    """
    对比不同并发模型的性能
    
    测试场景：
    - 模拟 I/O 密集型任务（网络请求、数据库查询）
    - 不同并发数量下的表现
    """
    
    def __init__(self):
        self.results = []
    
    def io_task(self, task_id: int, delay: float = 0.1) -> dict:
        """模拟 I/O 任务"""
        time.sleep(delay)  # 模拟网络延迟
        return {
            "task_id": task_id,
            "completed_at": time.time(),
            "thread": threading.current_thread().name
        }
    
    async def async_io_task(self, task_id: int, delay: float = 0.1) -> dict:
        """模拟异步 I/O 任务"""
        await asyncio.sleep(delay)
        return {
            "task_id": task_id,
            "completed_at": time.time(),
            "coroutine": f"async_task_{task_id}"
        }
    
    def test_threading(self, task_count: int = 100, workers: int = 10):
        """测试多线程性能"""
        print(f"\n  测试: 多线程 ({task_count} 任务, {workers} 线程)")
        
        start = time.time()
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(self.io_task, i, 0.1)
                for i in range(task_count)
            ]
            results = [f.result() for f in futures]
        
        elapsed = time.time() - start
        
        print(f"    耗时: {elapsed:.2f}s")
        print(f"    吞吐量: {task_count/elapsed:.2f} 任务/秒")
        
        return {
            "model": "threading",
            "task_count": task_count,
            "workers": workers,
            "elapsed": elapsed,
            "throughput": task_count / elapsed
        }
    
    async def test_asyncio(self, task_count: int = 100):
        """测试 asyncio 性能"""
        print(f"\n  测试: asyncio ({task_count} 任务)")
        
        start = time.time()
        
        tasks = [
            self.async_io_task(i, 0.1)
            for i in range(task_count)
        ]
        results = await asyncio.gather(*tasks)
        
        elapsed = time.time() - start
        
        print(f"    耗时: {elapsed:.2f}s")
        print(f"    吞吐量: {task_count/elapsed:.2f} 任务/秒")
        
        return {
            "model": "asyncio",
            "task_count": task_count,
            "workers": 1,  # 单线程
            "elapsed": elapsed,
            "throughput": task_count / elapsed
        }
    
    def test_serial(self, task_count: int = 100):
        """测试串行执行（基准）"""
        print(f"\n  测试: 串行执行 ({task_count} 任务)")
        
        start = time.time()
        
        results = [self.io_task(i, 0.1) for i in range(task_count)]
        
        elapsed = time.time() - start
        
        print(f"    耗时: {elapsed:.2f}s")
        print(f"    吞吐量: {task_count/elapsed:.2f} 任务/秒")
        
        return {
            "model": "serial",
            "task_count": task_count,
            "workers": 1,
            "elapsed": elapsed,
            "throughput": task_count / elapsed
        }
    
    def run_comparison(self):
        """运行完整对比"""
        print("\n" + "="*60)
        print("性能对比实验")
        print("="*60)
        
        task_count = 100
        
        # 测试1: 串行
        serial_result = self.test_serial(task_count)
        
        # 测试2: 多线程
        thread_result = self.test_threading(task_count, workers=10)
        
        # 测试3: asyncio
        async_result = asyncio.run(self.test_asyncio(task_count))
        
        # 汇总结果
        print("\n" + "-"*60)
        print("结果汇总:")
        print("-"*60)
        print(f"{'模型':<15} {'任务数':<10} {'并发数':<10} {'耗时(s)':<10} {'吞吐量':<15}")
        print("-"*60)
        
        for result in [serial_result, thread_result, async_result]:
            print(
                f"{result['model']:<15} "
                f"{result['task_count']:<10} "
                f"{result['workers']:<10} "
                f"{result['elapsed']:<10.2f} "
                f"{result['throughput']:<15.2f}"
            )
        
        print("-"*60)
        print(f"\n结论:")
        print(f"  - 多线程比串行快 {serial_result['elapsed']/thread_result['elapsed']:.2f}x")
        print(f"  - asyncio 比串行快 {serial_result['elapsed']/async_result['elapsed']:.2f}x")
        print(f"  - asyncio vs 多线程: {'asyncio 更快' if async_result['elapsed'] < thread_result['elapsed'] else '多线程更快'}")


# ==================== 项目4：TCP 连接池实现 ====================
class TCPConnectionPool:
    """
    TCP 连接池
    
    为什么需要连接池？
    - TCP 三次握手有开销（~1ms）
    - 频繁创建/销毁连接浪费资源
    - 连接池复用连接，提升性能
    
    应用场景：
    - 数据库连接池（MySQL, Redis）
    - HTTP 连接池（requests.Session）
    - RPC 连接池
    """
    
    def __init__(self, host: str, port: int, max_connections: int = 10):
        self.host = host
        self.port = port
        self.max_connections = max_connections
        self.pool: List[socket.socket] = []
        self.lock = threading.Lock()
        self.created_count = 0
    
    def get_connection(self) -> socket.socket:
        """从连接池获取连接"""
        with self.lock:
            if self.pool:
                # 复用已有连接
                conn = self.pool.pop()
                print(f"  [连接池] 复用连接 (池中剩余: {len(self.pool)})")
                return conn
            elif self.created_count < self.max_connections:
                # 创建新连接
                self.created_count += 1
                conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conn.connect((self.host, self.port))
                print(f"  [连接池] 创建新连接 #{self.created_count}")
                return conn
            else:
                raise Exception("连接池已满")
    
    def release_connection(self, conn: socket.socket):
        """释放连接回连接池"""
        with self.lock:
            if len(self.pool) < self.max_connections:
                self.pool.append(conn)
                print(f"  [连接池] 释放连接 (池中数量: {len(self.pool)})")
            else:
                conn.close()
                print(f"  [连接池] 连接池满，关闭连接")
    
    def close_all(self):
        """关闭所有连接"""
        with self.lock:
            for conn in self.pool:
                conn.close()
            self.pool.clear()
            print(f"  [连接池] 关闭所有连接")
    
    def demo(self):
        """演示连接池使用"""
        print("\n" + "="*60)
        print("TCP 连接池演示")
        print("="*60)
        
        # 注意：这个演示需要一个真实的服务器
        # 这里只是展示连接池的使用模式
        
        print("\n  连接池的优势:")
        print("  1. 减少 TCP 握手次数")
        print("  2. 降低延迟（复用连接）")
        print("  3. 控制并发连接数")
        print("  4. 避免资源泄漏")
        
        print("\n  实际应用:")
        print("  - requests.Session() 就是 HTTP 连接池")
        print("  - SQLAlchemy 的数据库连接池")
        print("  - Redis 客户端的连接池")
        
        print("\n  使用示例:")
        print("""
        pool = TCPConnectionPool('localhost', 3306, max_connections=10)
        
        # 获取连接
        conn = pool.get_connection()
        try:
            # 使用连接
            conn.send(query)
            result = conn.recv(4096)
        finally:
            # 释放连接（放回池中）
            pool.release_connection(conn)
        """)


# ==================== 主函数 ====================
def main():
    """运行所有项目"""
    print("="*60)
    print("网络编程实战项目 - 第二阶段")
    print("="*60)
    
    print("\n可用项目:")
    print("  1. 聊天服务器（两个版本）")
    print("     - ThreadedChatServer: 线程版")
    print("     - AsyncChatServer: asyncio 版")
    print("")
    print("  2. 简易 HTTP 服务器")
    print("     - SimpleHTTPServer")
    print("")
    print("  3. 性能对比实验")
    print("     - PerformanceComparison")
    print("")
    print("  4. TCP 连接池")
    print("     - TCPConnectionPool")
    
    print("\n" + "="*60)
    print("推荐学习顺序:")
    print("="*60)
    print("  1. 先运行性能对比，直观感受差异")
    perf = PerformanceComparison()
    perf.run_comparison()
    
    print("\n  2. 理解连接池的概念")
    pool = TCPConnectionPool('example.com', 80)
    pool.demo()
    
    print("\n  3. 启动 HTTP 服务器（在新终端测试）")
    print("     运行: SimpleHTTPServer().run_demo()")
    
    print("\n  4. 启动聊天服务器")
    print("     线程版: ThreadedChatServer().start()")
    print("     异步版: asyncio.run(AsyncChatServer().start())")
    
    print("\n" + "="*60)
    print("学习要点:")
    print("="*60)
    print("  ✓ 理解阻塞 IO vs 非阻塞 IO")
    print("  ✓ 掌握 threading 和 asyncio 的适用场景")
    print("  ✓ 学会用 Socket 实现 HTTP 协议")
    print("  ✓ 理解连接池的价值和实现原理")
    print("  ✓ 能够根据业务需求选择合适的并发模型")


if __name__ == "__main__":
    main()
