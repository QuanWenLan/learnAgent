"""
Python 多线程编程完整教程
涵盖：线程基础、线程同步、线程池、生产者-消费者模式等
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import random


# ==================== 1. 基础线程创建 ====================
def basic_thread_example():
    """基础线程创建示例"""
    print("\n" + "="*50)
    print("1. 基础线程创建")
    print("="*50)
    
    def worker(name: str, duration: int):
        """工作函数"""
        print(f"线程 {name} 开始运行，持续 {duration} 秒")
        time.sleep(duration)
        print(f"线程 {name} 完成")
    
    # 方式1：直接创建线程
    thread1 = threading.Thread(target=worker, args=("Thread-1", 2))
    thread2 = threading.Thread(target=worker, args=("Thread-2", 3))
    
    # 启动线程
    thread1.start()
    thread2.start()
    
    # 等待线程完成
    thread1.join()
    thread2.join()
    
    print("所有线程已完成")


# ==================== 2. 使用类创建线程 ====================
class MyThread(threading.Thread):
    """通过继承 Thread 类创建线程"""
    
    def __init__(self, name: str, duration: int):
        super().__init__()
        self.name = name
        self.duration = duration
        self.result = None
    
    def run(self):
        """线程执行的方法"""
        print(f"自定义线程 {self.name} 开始运行")
        time.sleep(self.duration)
        self.result = f"{self.name} 的结果"
        print(f"自定义线程 {self.name} 完成")


def class_thread_example():
    """使用类创建线程示例"""
    print("\n" + "="*50)
    print("2. 使用类创建线程")
    print("="*50)
    
    threads = [
        MyThread("ClassThread-1", 1),
        MyThread("ClassThread-2", 2),
        MyThread("ClassThread-3", 1.5)
    ]
    
    # 启动所有线程
    for thread in threads:
        thread.start()
    
    # 等待所有线程完成并获取结果
    for thread in threads:
        thread.join()
        print(f"{thread.name}: {thread.result}")


# ==================== 3. 线程同步 - Lock ====================
def lock_example():
    """使用 Lock 进行线程同步"""
    print("\n" + "="*50)
    print("3. 线程同步 - Lock")
    print("="*50)
    
    counter = 0
    lock = threading.Lock()
    
    def increment():
        nonlocal counter
        for _ in range(100000):
            with lock:  # 自动获取和释放锁
                counter += 1
    
    threads = []
    for _ in range(5):
        t = threading.Thread(target=increment)
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"最终计数值: {counter} (期望值: 500000)")


# ==================== 4. 线程同步 - RLock（可重入锁）====================
def rlock_example():
    """使用 RLock 可重入锁"""
    print("\n" + "="*50)
    print("4. 线程同步 - RLock（可重入锁）")
    print("="*50)
    
    rlock = threading.RLock()
    
    def recursive_function(n: int):
        """递归函数，需要可重入锁"""
        with rlock:
            if n <= 0:
                return 0
            print(f"递归层级: {n}")
            time.sleep(0.1)
            return n + recursive_function(n - 1)
    
    result = recursive_function(5)
    print(f"递归结果: {result}")


# ==================== 5. 线程同步 - Condition ====================
def condition_example():
    """使用 Condition 进行线程间通信"""
    print("\n" + "="*50)
    print("5. 线程同步 - Condition")
    print("="*50)
    
    condition = threading.Condition()
    items = []
    
    def producer():
        """生产者"""
        for i in range(5):
            with condition:
                item = f"item-{i}"
                items.append(item)
                print(f"生产: {item}")
                condition.notify()  # 通知消费者
                time.sleep(0.5)
    
    def consumer():
        """消费者"""
        for _ in range(5):
            with condition:
                while not items:
                    condition.wait()  # 等待生产者通知
                item = items.pop(0)
                print(f"消费: {item}")
                time.sleep(1)
    
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    consumer_thread.start()
    producer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()


# ==================== 6. 线程同步 - Event ====================
def event_example():
    """使用 Event 进行线程间信号传递"""
    print("\n" + "="*50)
    print("6. 线程同步 - Event")
    print("="*50)
    
    event = threading.Event()
    
    def waiter():
        """等待事件"""
        print("Waiter: 等待事件触发...")
        event.wait()  # 阻塞直到事件被设置
        print("Waiter: 事件已触发，继续执行")
    
    def setter():
        """设置事件"""
        time.sleep(2)
        print("Setter: 触发事件")
        event.set()
    
    waiter_thread = threading.Thread(target=waiter)
    setter_thread = threading.Thread(target=setter)
    
    waiter_thread.start()
    setter_thread.start()
    
    waiter_thread.join()
    setter_thread.join()


# ==================== 7. 线程同步 - Semaphore ====================
def semaphore_example():
    """使用 Semaphore 控制并发数量"""
    print("\n" + "="*50)
    print("7. 线程同步 - Semaphore")
    print("="*50)
    
    semaphore = threading.Semaphore(3)  # 最多允许3个线程同时访问
    
    def worker(worker_id: int):
        with semaphore:
            print(f"Worker {worker_id} 开始工作")
            time.sleep(random.uniform(0.5, 2))
            print(f"Worker {worker_id} 完成工作")
    
    threads = []
    for i in range(10):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print("所有 Worker 完成")


# ==================== 8. 线程安全队列 ====================
def queue_example():
    """使用 queue.Queue 实现线程安全队列"""
    print("\n" + "="*50)
    print("8. 线程安全队列")
    print("="*50)
    
    q = queue.Queue(maxsize=10)
    
    def producer():
        """生产者"""
        for i in range(10):
            item = f"item-{i}"
            q.put(item)
            print(f"生产: {item}, 队列大小: {q.qsize()}")
            time.sleep(0.3)
    
    def consumer():
        """消费者"""
        while True:
            try:
                item = q.get(timeout=5)  # 超时退出
                print(f"消费: {item}, 队列大小: {q.qsize()}")
                q.task_done()
                time.sleep(0.5)
            except queue.Empty:
                break
    
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()


# ==================== 9. 线程池基础使用 ====================
def thread_pool_basic():
    """线程池基础使用"""
    print("\n" + "="*50)
    print("9. 线程池基础使用")
    print("="*50)
    
    def task(n: int) -> int:
        """任务函数"""
        time.sleep(0.5)
        return n * n
    
    # 创建线程池，最大5个线程
    with ThreadPoolExecutor(max_workers=5) as executor:
        # 提交任务
        futures = [executor.submit(task, i) for i in range(10)]
        
        # 获取结果
        for future in futures:
            result = future.result()
            print(f"结果: {result}")


# ==================== 10. 线程池 - map 方法 ====================
def thread_pool_map():
    """线程池使用 map 方法"""
    print("\n" + "="*50)
    print("10. 线程池 - map 方法")
    print("="*50)
    
    def task(n: int) -> int:
        time.sleep(0.3)
        return n * n
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(task, range(10))
        
        for i, result in enumerate(results):
            print(f"task({i}) = {result}")


# ==================== 11. 线程池 - as_completed ====================
def thread_pool_as_completed():
    """线程池使用 as_completed 按完成顺序获取结果"""
    print("\n" + "="*50)
    print("11. 线程池 - as_completed")
    print("="*50)
    
    def task(n: int) -> tuple:
        sleep_time = random.uniform(0.5, 2)
        time.sleep(sleep_time)
        return (n, n * n, sleep_time)
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(task, i): i for i in range(10)}
        
        for future in as_completed(futures):
            original_num, result, sleep_time = future.result()
            print(f"任务 {original_num} 完成（耗时 {sleep_time:.2f}s）: {result}")


# ==================== 12. 实际案例：批量下载模拟 ====================
def batch_download_simulation():
    """模拟批量下载任务"""
    print("\n" + "="*50)
    print("12. 实际案例：批量下载模拟")
    print("="*50)
    
    def download_file(file_id: int) -> Dict:
        """模拟下载文件"""
        download_time = random.uniform(0.5, 2)
        time.sleep(download_time)
        return {
            "file_id": file_id,
            "status": "success",
            "download_time": round(download_time, 2),
            "size": random.randint(1000, 10000)
        }
    
    file_ids = list(range(1, 11))
    results = []
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {
            executor.submit(download_file, file_id): file_id 
            for file_id in file_ids
        }
        
        for future in as_completed(future_to_file):
            file_id = future_to_file[future]
            try:
                result = future.result()
                results.append(result)
                print(f"文件 {file_id} 下载完成: {result['size']} bytes "
                      f"(耗时 {result['download_time']}s)")
            except Exception as e:
                print(f"文件 {file_id} 下载失败: {e}")
    
    end_time = time.time()
    
    print(f"\n总耗时: {end_time - start_time:.2f}s")
    print(f"成功下载: {len(results)} 个文件")


# ==================== 13. 实际案例：并行数据处理 ====================
def parallel_data_processing():
    """并行数据处理示例"""
    print("\n" + "="*50)
    print("13. 实际案例：并行数据处理")
    print("="*50)
    
    def process_data_chunk(data: List[int]) -> Dict:
        """处理数据块"""
        time.sleep(0.5)
        return {
            "sum": sum(data),
            "avg": sum(data) / len(data),
            "max": max(data),
            "min": min(data),
            "count": len(data)
        }
    
    # 生成测试数据
    data = list(range(1, 1001))
    chunk_size = 100
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(process_data_chunk, chunk) 
            for chunk in chunks
        ]
        
        partial_results = [f.result() for f in futures]
    
    # 合并结果
    total_sum = sum(r["sum"] for r in partial_results)
    total_count = sum(r["count"] for r in partial_results)
    overall_avg = total_sum / total_count
    overall_max = max(r["max"] for r in partial_results)
    overall_min = min(r["min"] for r in partial_results)
    
    end_time = time.time()
    
    print(f"数据处理完成:")
    print(f"  总和: {total_sum}")
    print(f"  平均值: {overall_avg:.2f}")
    print(f"  最大值: {overall_max}")
    print(f"  最小值: {overall_min}")
    print(f"  总数量: {total_count}")
    print(f"  耗时: {end_time - start_time:.2f}s")


# ==================== 14. 守护线程 ====================
def daemon_thread_example():
    """守护线程示例"""
    print("\n" + "="*50)
    print("14. 守护线程")
    print("="*50)
    
    def background_worker():
        """后台工作线程"""
        count = 0
        while True:
            count += 1
            print(f"后台工作: {count}")
            time.sleep(1)
    
    # 创建守护线程
    daemon = threading.Thread(target=background_worker, daemon=True)
    daemon.start()
    
    # 主线程等待3秒后退出，守护线程会自动终止
    time.sleep(3)
    print("主线程即将退出，守护线程将自动终止")


# ==================== 15. 线程局部变量 ====================
def thread_local_example():
    """线程局部变量示例"""
    print("\n" + "="*50)
    print("15. 线程局部变量")
    print("="*50)
    
    # 创建线程局部存储
    local_data = threading.local()
    
    def worker(worker_id: int):
        # 每个线程有独立的 value
        local_data.value = worker_id
        time.sleep(random.uniform(0.5, 1.5))
        print(f"Worker {worker_id}: value = {local_data.value}")
    
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()


# ==================== 主函数 ====================
def main():
    """运行所有示例"""
    print("Python 多线程编程完整教程")
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))
    
    # 依次运行各个示例
    examples = [
        ("基础线程创建", basic_thread_example),
        ("类创建线程", class_thread_example),
        ("Lock 同步", lock_example),
        ("RLock 可重入锁", rlock_example),
        ("Condition 条件变量", condition_example),
        ("Event 事件", event_example),
        ("Semaphore 信号量", semaphore_example),
        ("线程安全队列", queue_example),
        ("线程池基础", thread_pool_basic),
        ("线程池 map", thread_pool_map),
        ("线程池 as_completed", thread_pool_as_completed),
        ("批量下载模拟", batch_download_simulation),
        ("并行数据处理", parallel_data_processing),
        ("守护线程", daemon_thread_example),
        ("线程局部变量", thread_local_example),
    ]
    
    for name, func in examples:
        try:
            func()
        except Exception as e:
            print(f"\n{name} 执行出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*50)
    print("所有示例执行完毕")
    print("结束时间:", time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
