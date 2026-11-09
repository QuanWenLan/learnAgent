"""
asyncio 中的线程使用完整教程
展示如何在异步编程环境中正确使用线程，避免阻塞事件循环
"""

import asyncio
import time
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Dict
import random


# ==================== 1. 基础：在 asyncio 中运行阻塞函数 ====================
async def run_blocking_in_thread():
    """使用 run_in_executor 在线程池中运行阻塞函数"""
    print("\n" + "="*60)
    print("1. 基础：在 asyncio 中运行阻塞函数")
    print("="*60)
    
    def blocking_task(name: str, duration: int) -> str:
        """模拟阻塞任务（如同步 I/O、CPU 计算）"""
        print(f"  [线程 {threading.current_thread().name}] 开始: {name}")
        time.sleep(duration)  # 这会阻塞线程，但不会阻塞事件循环
        print(f"  [线程 {threading.current_thread().name}] 完成: {name}")
        return f"{name} 的结果"
    
    loop = asyncio.get_event_loop()
    
    # 在线程池中执行阻塞任务
    start = time.time()
    
    # 提交多个任务到线程池
    futures = [
        loop.run_in_executor(None, blocking_task, f"任务{i}", random.uniform(0.5, 1.5))
        for i in range(5)
    ]
    
    # 等待所有任务完成
    results = await asyncio.gather(*futures)
    
    elapsed = time.time() - start
    print(f"\n  所有任务完成，总耗时: {elapsed:.2f}s")
    for result in results:
        print(f"  结果: {result}")


# ==================== 2. 使用自定义线程池 ====================
async def custom_thread_pool():
    """使用自定义的 ThreadPoolExecutor"""
    print("\n" + "="*60)
    print("2. 使用自定义线程池")
    print("="*60)
    
    def cpu_intensive_task(n: int) -> int:
        """CPU 密集型任务"""
        print(f"  [线程 {threading.current_thread().name}] 计算 {n} 的平方")
        time.sleep(0.5)  # 模拟计算
        return n * n
    
    # 创建自定义线程池（限制线程数量）
    executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="custom_")
    
    loop = asyncio.get_event_loop()
    
    start = time.time()
    
    # 使用自定义线程池执行任务
    tasks = [
        loop.run_in_executor(executor, cpu_intensive_task, i)
        for i in range(10)
    ]
    
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    print(f"\n  计算结果: {results}")
    print(f"  总耗时: {elapsed:.2f}s (串行需要 5s)")
    
    # 关闭线程池
    executor.shutdown()


# ==================== 3. 混合异步和同步代码 ====================
async def mix_async_sync():
    """混合使用异步和同步代码"""
    print("\n" + "="*60)
    print("3. 混合异步和同步代码")
    print("="*60)
    
    def sync_io_operation(file_id: int) -> Dict:
        """模拟同步 I/O 操作（如文件读写、数据库查询）"""
        print(f"  [同步] 读取文件 {file_id}")
        time.sleep(random.uniform(0.3, 0.8))
        return {"file_id": file_id, "data": f"文件{file_id}的内容"}
    
    async def async_process(data: Dict) -> Dict:
        """异步处理数据"""
        print(f"  [异步] 处理文件 {data['file_id']}")
        await asyncio.sleep(0.2)  # 模拟异步处理
        data["processed"] = True
        return data
    
    loop = asyncio.get_event_loop()
    
    # 步骤1: 在线程池中执行同步 I/O
    print("\n  步骤1: 并行读取文件（在线程池中）")
    read_tasks = [
        loop.run_in_executor(None, sync_io_operation, i)
        for i in range(1, 6)
    ]
    file_data_list = await asyncio.gather(*read_tasks)
    
    # 步骤2: 异步处理数据
    print("\n  步骤2: 异步处理数据")
    process_tasks = [
        async_process(data)
        for data in file_data_list
    ]
    results = await asyncio.gather(*process_tasks)
    
    print(f"\n  处理完成，共处理 {len(results)} 个文件")
    for result in results:
        print(f"  文件 {result['file_id']}: {'已处理' if result['processed'] else '未处理'}")


# ==================== 4. 生产者-消费者模式（asyncio + 线程）====================
async def producer_consumer_pattern():
    """使用 asyncio 队列和线程实现生产者-消费者"""
    print("\n" + "="*60)
    print("4. 生产者-消费者模式（asyncio + 线程）")
    print("="*60)
    
    queue = asyncio.Queue(maxsize=10)
    
    def sync_producer(item_id: int) -> int:
        """同步生产者（模拟从外部系统获取数据）"""
        print(f"  [线程] 生产项目 {item_id}")
        time.sleep(0.5)
        return item_id
    
    async def async_consumer(consumer_id: int):
        """异步消费者"""
        while True:
            try:
                # 非阻塞获取，超时则退出
                item = await asyncio.wait_for(queue.get(), timeout=2.0)
                print(f"  [协程] 消费者 {consumer_id} 处理项目 {item}")
                await asyncio.sleep(0.3)  # 模拟异步处理
                queue.task_done()
            except asyncio.TimeoutError:
                break
    
    loop = asyncio.get_event_loop()
    
    # 启动消费者
    consumers = [
        asyncio.create_task(async_consumer(i))
        for i in range(3)
    ]
    
    # 在线程池中运行生产者
    print("\n  生产阶段:")
    producer_tasks = [
        loop.run_in_executor(None, sync_producer, i)
        for i in range(10)
    ]
    
    produced_items = await asyncio.gather(*producer_tasks)
    
    # 将生产的项目放入队列
    print("\n  放入队列:")
    for item in produced_items:
        await queue.put(item)
        print(f"  项目 {item} 已入队")
    
    # 等待所有消费者完成
    await asyncio.gather(*consumers, return_exceptions=True)
    
    print(f"\n  所有项目处理完成")


# ==================== 5. 定期任务 + 线程池 ====================
async def periodic_task_with_threadpool():
    """定期执行的任务，部分工作在线程池中完成"""
    print("\n" + "="*60)
    print("5. 定期任务 + 线程池")
    print("="*60)
    
    execution_count = 0
    max_executions = 5
    
    def sync_health_check(service_id: int) -> Dict:
        """同步健康检查（如调用外部 API）"""
        print(f"  [线程] 检查服务 {service_id} 的健康状态")
        time.sleep(0.5)
        status = random.choice(["healthy", "unhealthy"])
        return {"service_id": service_id, "status": status}
    
    async def check_all_services():
        """异步协调多个服务的健康检查"""
        nonlocal execution_count
        execution_count += 1
        
        print(f"\n  --- 第 {execution_count} 次检查 ---")
        
        loop = asyncio.get_event_loop()
        
        # 在线程池中并行检查多个服务
        check_tasks = [
            loop.run_in_executor(None, sync_health_check, service_id)
            for service_id in range(1, 4)
        ]
        
        results = await asyncio.gather(*check_tasks)
        
        for result in results:
            status_icon = "✓" if result["status"] == "healthy" else "✗"
            print(f"  {status_icon} 服务 {result['service_id']}: {result['status']}")
    
    # 定期执行
    for _ in range(max_executions):
        await check_all_services()
        await asyncio.sleep(1)  # 等待 1 秒后再次检查
    
    print(f"\n  总共执行了 {execution_count} 次检查")


# ==================== 6. 错误处理 ====================
async def error_handling_in_threads():
    """在线程池任务中处理错误"""
    print("\n" + "="*60)
    print("6. 错误处理")
    print("="*60)
    
    def risky_task(task_id: int) -> str:
        """可能失败的任务"""
        print(f"  [线程] 执行任务 {task_id}")
        time.sleep(0.5)
        if task_id % 3 == 0:
            raise ValueError(f"任务 {task_id} 执行失败")
        return f"任务 {task_id} 成功"
    
    loop = asyncio.get_event_loop()
    
    # 提交任务
    tasks = [
        loop.run_in_executor(None, risky_task, i)
        for i in range(1, 7)
    ]
    
    # 使用 gather 并收集异常
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    print("\n  执行结果:")
    success_count = 0
    failed_count = 0
    
    for i, result in enumerate(results, 1):
        if isinstance(result, Exception):
            print(f"  ✗ 任务 {i} 失败: {result}")
            failed_count += 1
        else:
            print(f"  ✓ {result}")
            success_count += 1
    
    print(f"\n  统计: 成功 {success_count}, 失败 {failed_count}")


# ==================== 7. 超时控制 ====================
async def timeout_control():
    """为线程池任务设置超时"""
    print("\n" + "="*60)
    print("7. 超时控制")
    print("="*60)
    
    def slow_task(task_id: int, duration: float) -> str:
        """慢速任务"""
        print(f"  [线程] 任务 {task_id} 开始（预计 {duration}s）")
        time.sleep(duration)
        print(f"  [线程] 任务 {task_id} 完成")
        return f"任务 {task_id} 的结果"
    
    loop = asyncio.get_event_loop()
    
    # 任务1: 正常完成
    print("\n  任务1: 正常执行（1s，超时 3s）")
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, slow_task, 1, 1.0),
            timeout=3.0
        )
        print(f"  ✓ {result}")
    except asyncio.TimeoutError:
        print(f"  ✗ 任务超时")
    
    # 任务2: 会超时
    print("\n  任务2: 预期超时（5s，超时 2s）")
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, slow_task, 2, 5.0),
            timeout=2.0
        )
        print(f"  ✓ {result}")
    except asyncio.TimeoutError:
        print(f"  ✗ 任务超时（这是预期的）")
    
    print("\n  注意：超时时，线程中的任务仍在运行，只是 asyncio 不再等待它")


# ==================== 8. 实际案例：批量 API 调用 ====================
async def batch_api_calls():
    """模拟批量 API 调用（结合同步 SDK 和 asyncio）"""
    print("\n" + "="*60)
    print("8. 实际案例：批量 API 调用")
    print("="*60)
    
    def call_external_api(api_id: int) -> Dict:
        """
        模拟调用外部 API（使用同步 SDK）
        很多第三方库只提供同步接口，需要在线程池中运行
        """
        print(f"  [线程] 调用 API {api_id}")
        time.sleep(random.uniform(0.5, 1.5))  # 模拟网络延迟
        
        # 模拟可能的失败
        if random.random() < 0.2:
            raise ConnectionError(f"API {api_id} 连接失败")
        
        return {
            "api_id": api_id,
            "status": 200,
            "data": f"API {api_id} 的响应数据",
            "timestamp": time.time()
        }
    
    loop = asyncio.get_event_loop()
    
    api_ids = list(range(1, 11))
    
    start_time = time.time()
    
    # 在线程池中并行调用 API
    tasks = [
        loop.run_in_executor(None, call_external_api, api_id)
        for api_id in api_ids
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    elapsed = time.time() - start_time
    
    # 处理结果
    success_results = []
    failed_results = []
    
    for result in results:
        if isinstance(result, Exception):
            failed_results.append(str(result))
        else:
            success_results.append(result)
    
    print(f"\n  执行统计:")
    print(f"  总耗时: {elapsed:.2f}s")
    print(f"  成功: {len(success_results)}")
    print(f"  失败: {len(failed_results)}")
    
    if failed_results:
        print(f"\n  失败的请求:")
        for error in failed_results[:3]:  # 只显示前3个
            print(f"    - {error}")


# ==================== 9. 进程池 vs 线程池 ====================
async def process_pool_vs_thread_pool():
    """对比进程池和线程池的使用"""
    print("\n" + "="*60)
    print("9. 进程池 vs 线程池")
    print("="*60)
    
    def cpu_bound_computation(n: int) -> int:
        """CPU 密集型计算"""
        print(f"  [进程/线程] 计算 {n} 的阶乘")
        result = 1
        for i in range(1, min(n + 1, 1000)):  # 限制计算量
            result *= i
        time.sleep(0.3)  # 模拟更多计算
        return result
    
    def io_bound_operation(file_id: int) -> str:
        """I/O 密集型操作"""
        print(f"  [进程/线程] 读取文件 {file_id}")
        time.sleep(0.5)
        return f"文件 {file_id} 的内容"
    
    loop = asyncio.get_event_loop()
    
    # CPU 密集型：使用进程池
    print("\n  CPU 密集型任务 - 使用进程池:")
    with ProcessPoolExecutor(max_workers=3) as process_executor:
        start = time.time()
        cpu_tasks = [
            loop.run_in_executor(process_executor, cpu_bound_computation, i)
            for i in range(5, 10)
        ]
        cpu_results = await asyncio.gather(*cpu_tasks)
        elapsed = time.time() - start
        print(f"  结果: {[r % 1000 for r in cpu_results]}")  # 只显示最后几位
        print(f"  耗时: {elapsed:.2f}s")
    
    # I/O 密集型：使用线程池
    print("\n  I/O 密集型任务 - 使用线程池:")
    with ThreadPoolExecutor(max_workers=5) as thread_executor:
        start = time.time()
        io_tasks = [
            loop.run_in_executor(thread_executor, io_bound_operation, i)
            for i in range(1, 6)
        ]
        io_results = await asyncio.gather(*io_tasks)
        elapsed = time.time() - start
        print(f"  结果: {io_results}")
        print(f"  耗时: {elapsed:.2f}s")


# ==================== 10. 上下文管理器集成 ====================
async def context_manager_integration():
    """在异步上下文中使用线程安全的资源"""
    print("\n" + "="*60)
    print("10. 上下文管理器集成")
    print("="*60)
    
    class ThreadSafeResource:
        """线程安全资源示例"""
        def __init__(self, name: str):
            self.name = name
            self.lock = threading.Lock()
            self.data = []
        
        def add_data(self, item):
            with self.lock:
                print(f"  [线程 {threading.current_thread().name}] 添加数据: {item}")
                time.sleep(0.2)
                self.data.append(item)
        
        def get_data(self):
            with self.lock:
                return self.data.copy()
    
    resource = ThreadSafeResource("共享资源")
    
    def worker(worker_id: int):
        """工作线程"""
        for i in range(3):
            resource.add_data(f"worker{worker_id}-item{i}")
    
    loop = asyncio.get_event_loop()
    
    # 在线程池中运行多个 worker
    tasks = [
        loop.run_in_executor(None, worker, i)
        for i in range(3)
    ]
    
    await asyncio.gather(*tasks)
    
    # 获取最终数据
    final_data = resource.get_data()
    print(f"\n  最终数据 ({len(final_data)} 项):")
    for item in final_data:
        print(f"    - {item}")


# ==================== 11. 取消任务 ====================
async def task_cancellation():
    """取消正在运行的线程池任务"""
    print("\n" + "="*60)
    print("11. 取消任务")
    print("="*60)
    
    def long_running_task(task_id: int) -> str:
        """长时间运行的任务"""
        print(f"  [线程] 任务 {task_id} 开始")
        for i in range(10):
            time.sleep(0.5)
            print(f"  [线程] 任务 {task_id} 进度: {i+1}/10")
        return f"任务 {task_id} 完成"
    
    loop = asyncio.get_event_loop()
    
    # 启动任务
    task = asyncio.create_task(
        loop.run_in_executor(None, long_running_task, 1)
    )
    
    # 等待 2 秒后取消
    await asyncio.sleep(2)
    print("\n  取消任务...")
    task.cancel()
    
    try:
        await task
    except asyncio.CancelledError:
        print("  ✓ 任务已成功取消")
    
    print("  注意：线程中的函数仍在运行，但 asyncio 不再等待它")


# ==================== 12. 性能对比 ====================
async def performance_comparison():
    """对比不同并发方式的性能"""
    print("\n" + "="*60)
    print("12. 性能对比")
    print("="*60)
    
    def blocking_io_task(task_id: int) -> int:
        """阻塞 I/O 任务"""
        time.sleep(0.5)
        return task_id * 2
    
    async def async_task(task_id: int) -> int:
        """异步任务"""
        await asyncio.sleep(0.5)
        return task_id * 2
    
    task_count = 10
    
    # 方式1: 串行执行
    print(f"\n  方式1: 串行执行 ({task_count} 个任务)")
    start = time.time()
    serial_results = [blocking_io_task(i) for i in range(task_count)]
    serial_time = time.time() - start
    print(f"  耗时: {serial_time:.2f}s")
    
    # 方式2: 线程池
    print(f"\n  方式2: 线程池 ({task_count} 个任务, 5 个工作线程)")
    loop = asyncio.get_event_loop()
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        tasks = [
            loop.run_in_executor(executor, blocking_io_task, i)
            for i in range(task_count)
        ]
        thread_results = await asyncio.gather(*tasks)
    thread_time = time.time() - start
    print(f"  耗时: {thread_time:.2f}s")
    
    # 方式3: 纯异步
    print(f"\n  方式3: 纯异步 ({task_count} 个任务)")
    start = time.time()
    async_tasks = [async_task(i) for i in range(task_count)]
    async_results = await asyncio.gather(*async_tasks)
    async_time = time.time() - start
    print(f"  耗时: {async_time:.2f}s")
    
    print(f"\n  性能对比:")
    print(f"  串行:   {serial_time:.2f}s (基准)")
    print(f"  线程池: {thread_time:.2f}s (提升 {serial_time/thread_time:.2f}x)")
    print(f"  异步:   {async_time:.2f}s (提升 {serial_time/async_time:.2f}x)")
    print(f"\n  结果一致性: {serial_results == list(thread_results) == async_results}")


# ==================== 主函数 ====================
async def main():
    """运行所有示例"""
    print("="*60)
    print("asyncio 中的线程使用完整教程")
    print("="*60)
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    examples = [
        ("基础：在 asyncio 中运行阻塞函数", run_blocking_in_thread),
        ("使用自定义线程池", custom_thread_pool),
        ("混合异步和同步代码", mix_async_sync),
        ("生产者-消费者模式", producer_consumer_pattern),
        ("定期任务 + 线程池", periodic_task_with_threadpool),
        ("错误处理", error_handling_in_threads),
        ("超时控制", timeout_control),
        ("实际案例：批量 API 调用", batch_api_calls),
        ("进程池 vs 线程池", process_pool_vs_thread_pool),
        ("上下文管理器集成", context_manager_integration),
        ("取消任务", task_cancellation),
        ("性能对比", performance_comparison),
    ]
    
    for name, coro_func in examples:
        try:
            await coro_func()
        except Exception as e:
            print(f"\n{name} 执行出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("所有示例执行完毕")
    print(f"结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
