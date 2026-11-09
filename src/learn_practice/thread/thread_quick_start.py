"""
多线程快速入门 - 5分钟上手
最常用、最实用的多线程示例
"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# ==================== 示例1：最简单的多线程 ====================
def simple_threading():
    """最简单的多线程使用"""
    print("\n【示例1】最简单的多线程")
    
    def task(name, seconds):
        print(f"  开始任务: {name}")
        time.sleep(seconds)
        print(f"  完成任务: {name}")
        return f"{name} 的结果"
    
    # 创建线程池（3个工作线程）
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务
        future1 = executor.submit(task, "任务A", 2)
        future2 = executor.submit(task, "任务B", 1)
        future3 = executor.submit(task, "任务C", 1.5)
        
        # 获取结果
        print(f"  {future1.result()}")
        print(f"  {future2.result()}")
        print(f"  {future3.result()}")


# ==================== 示例2：批量处理任务 ====================
def batch_processing():
    """批量处理任务的典型用法"""
    print("\n【示例2】批量处理任务")
    
    def process_item(item_id):
        """处理单个项目"""
        time.sleep(0.5)  # 模拟处理时间
        return item_id * 2
    
    items = list(range(1, 11))  # 10个项目
    
    start_time = time.time()
    
    # 使用 map 批量处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(process_item, items))
    
    elapsed = time.time() - start_time
    
    print(f"  处理结果: {results}")
    print(f"  总耗时: {elapsed:.2f}秒")
    print(f"  如果串行执行需要: {len(items) * 0.5:.2f}秒")
    print(f"  加速比: {len(items) * 0.5 / elapsed:.2f}x")


# ==================== 示例3：按完成顺序获取结果 ====================
def as_completed_example():
    """按任务完成顺序获取结果"""
    print("\n【示例3】按完成顺序获取结果")
    
    def download(url_id):
        """模拟下载"""
        import random
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
        return {"url_id": url_id, "time": round(delay, 2)}
    
    urls = list(range(1, 6))
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 提交所有任务
        future_to_url = {
            executor.submit(download, url_id): url_id 
            for url_id in urls
        }
        
        # 按完成顺序处理结果
        print("  下载完成情况:")
        for future in as_completed(future_to_url):
            result = future.result()
            print(f"    URL {result['url_id']} 下载完成 (耗时 {result['time']}s)")


# ==================== 示例4：实际应用场景 - 批量API调用 ====================
def api_calls_simulation():
    """模拟批量API调用"""
    print("\n【示例4】批量API调用模拟")
    
    def call_api(api_id):
        """模拟API调用"""
        time.sleep(0.8)  # 模拟网络延迟
        return {
            "api_id": api_id,
            "status": 200,
            "data": f"API {api_id} 的响应数据"
        }
    
    api_ids = list(range(1, 8))
    
    start_time = time.time()
    
    success_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_api = {
            executor.submit(call_api, api_id): api_id 
            for api_id in api_ids
        }
        
        for future in as_completed(future_to_api):
            api_id = future_to_api[future]
            try:
                result = future.result()
                print(f"  ✓ API {api_id} 调用成功: {result['status']}")
                success_count += 1
            except Exception as e:
                print(f"  ✗ API {api_id} 调用失败: {e}")
                failed_count += 1
    
    elapsed = time.time() - start_time
    
    print(f"\n  统计: 成功 {success_count}, 失败 {failed_count}")
    print(f"  总耗时: {elapsed:.2f}秒")


# ==================== 示例5：带错误处理的线程池 ====================
def error_handling():
    """带错误处理的线程池"""
    print("\n【示例5】带错误处理")
    
    def risky_task(task_id):
        """可能失败的任务"""
        time.sleep(0.5)
        if task_id % 3 == 0:
            raise ValueError(f"任务 {task_id} 执行失败")
        return f"任务 {task_id} 成功"
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [
            executor.submit(risky_task, i) 
            for i in range(1, 7)
        ]
        
        for future in futures:
            try:
                result = future.result()
                print(f"  ✓ {result}")
            except Exception as e:
                print(f"  ✗ {e}")


# ==================== 示例6：对比串行和并行性能 ====================
def performance_comparison():
    """对比串行和并行性能"""
    print("\n【示例6】性能对比：串行 vs 并行")
    
    def io_task(task_id):
        """I/O 密集型任务"""
        time.sleep(0.5)
        return task_id ** 2
    
    task_count = 10
    
    # 串行执行
    start = time.time()
    serial_results = [io_task(i) for i in range(task_count)]
    serial_time = time.time() - start
    
    # 并行执行
    start = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        parallel_results = list(executor.map(io_task, range(task_count)))
    parallel_time = time.time() - start
    
    print(f"  任务数量: {task_count}")
    print(f"  串行耗时: {serial_time:.2f}秒")
    print(f"  并行耗时: {parallel_time:.2f}秒")
    print(f"  性能提升: {serial_time / parallel_time:.2f}x")
    print(f"  结果一致: {serial_results == parallel_results}")


# ==================== 示例7：生产者-消费者模式 ====================
def producer_consumer():
    """经典的生产者-消费者模式"""
    print("\n【示例7】生产者-消费者模式")
    
    import queue
    
    q = queue.Queue(maxsize=20)
    
    def producer(item_count):
        """生产者"""
        for i in range(item_count):
            q.put(i)
            print(f"  生产: {i}")
            time.sleep(0.2)
        q.put(None)  # 结束信号
    
    def consumer():
        """消费者"""
        while True:
            item = q.get()
            if item is None:
                break
            print(f"  消费: {item}")
            time.sleep(0.4)
            q.task_done()
    
    # 启动生产者和消费者
    producer_thread = threading.Thread(target=producer, args=(10,))
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    print("  所有任务完成")


# ==================== 主函数 ====================
if __name__ == "__main__":
    print("="*60)
    print("多线程快速入门 - 5分钟上手")
    print("="*60)
    
    # 运行所有示例
    examples = [
        simple_threading,
        batch_processing,
        as_completed_example,
        api_calls_simulation,
        error_handling,
        performance_comparison,
        # producer_consumer,  # 这个示例需要 import threading，单独演示
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"示例出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("学习建议:")
    print("  1. 从示例1开始，理解基本概念")
    print("  2. 重点掌握示例2和3（最常用）")
    print("  3. 实际应用参考示例4和5")
    print("  4. 完整教程查看 thread_learn.py")
    print("  5. 理论指南查看 THREAD_TUTORIAL.md")
    print("="*60)
