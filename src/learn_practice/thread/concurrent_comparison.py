"""
并发模型对比演示：多线程 vs 多进程 vs 串行
直观展示不同方式的性能差异
"""

import time
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed


# ==================== 测试任务 ====================

def io_bound_task(task_id):
    """I/O 密集型任务 - 模拟网络请求"""
    time.sleep(0.5)  # 模拟 I/O 等待
    return {"task_id": task_id, "type": "IO", "pid": os.getpid()}


def cpu_bound_task(task_id):
    """CPU 密集型任务 - 大量计算"""
    total = 0
    for i in range(1000000):
        total += i * i
    return {"task_id": task_id, "type": "CPU", "result": total, "pid": os.getpid()}


# ==================== 执行模式 ====================

def run_serial(task_func, task_count, description):
    """串行执行"""
    print(f"\n{'='*60}")
    print(f"{description} - 串行执行")
    print(f"{'='*60}")
    
    start_time = time.time()
    results = [task_func(i) for i in range(task_count)]
    elapsed = time.time() - start_time
    
    print(f"任务数量: {task_count}")
    print(f"总耗时: {elapsed:.2f}秒")
    print(f"平均每个任务: {elapsed/task_count:.3f}秒")
    
    return elapsed, results


def run_threading(task_func, task_count, max_workers, description):
    """多线程执行"""
    print(f"\n{'='*60}")
    print(f"{description} - 多线程执行 ({max_workers}个线程)")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task_func, i) for i in range(task_count)]
        results = [f.result() for f in as_completed(futures)]
    
    elapsed = time.time() - start_time
    
    print(f"任务数量: {task_count}")
    print(f"线程数量: {max_workers}")
    print(f"总耗时: {elapsed:.2f}秒")
    print(f"平均每个任务: {elapsed/task_count:.3f}秒")
    
    return elapsed, results


def run_multiprocessing(task_func, task_count, max_workers, description):
    """多进程执行"""
    print(f"\n{'='*60}")
    print(f"{description} - 多进程执行 ({max_workers}个进程)")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task_func, i) for i in range(task_count)]
        results = [f.result() for f in as_completed(futures)]
    
    elapsed = time.time() - start_time
    
    print(f"任务数量: {task_count}")
    print(f"进程数量: {max_workers}")
    print(f"总耗时: {elapsed:.2f}秒")
    print(f"平均每个任务: {elapsed/task_count:.3f}秒")
    
    return elapsed, results


# ==================== 对比分析 ====================

def compare_io_bound():
    """对比 I/O 密集型任务"""
    print("\n" + "="*70)
    print("📊 I/O 密集型任务对比（模拟网络请求）")
    print("="*70)
    
    task_count = 10
    max_workers = 5
    
    # 串行
    serial_time, _ = run_serial(
        io_bound_task, 
        task_count, 
        "I/O 任务"
    )
    
    # 多线程
    thread_time, thread_results = run_threading(
        io_bound_task, 
        task_count, 
        max_workers,
        "I/O 任务"
    )
    
    # 多进程
    process_time, process_results = run_multiprocessing(
        io_bound_task, 
        task_count, 
        max_workers,
        "I/O 任务"
    )
    
    # 对比结果
    print(f"\n{'='*70}")
    print("📈 I/O 密集型任务 - 性能对比总结")
    print(f"{'='*70}")
    print(f"{'方式':<15} {'耗时':<12} {'加速比':<12} {'评级'}")
    print(f"{'-'*70}")
    print(f"{'串行':<15} {serial_time:<12.2f} {'1.00x':<12} ⭐⭐")
    print(f"{'多线程':<14} {thread_time:<12.2f} {serial_time/thread_time:<12.2f}x ⭐⭐⭐⭐⭐")
    print(f"{'多进程':<14} {process_time:<12.2f} {serial_time/process_time:<12.2f}x ⭐⭐⭐⭐")
    
    print(f"\n💡 结论：I/O 密集型任务最适合使用多线程")
    print(f"   - 多线程加速比: {serial_time/thread_time:.2f}x")
    print(f"   - 多进程也能加速，但开销更大")


def compare_cpu_bound():
    """对比 CPU 密集型任务"""
    print("\n" + "="*70)
    print("📊 CPU 密集型任务对比（大量计算）")
    print("="*70)
    
    task_count = 8
    max_workers = 4
    
    # 串行
    serial_time, _ = run_serial(
        cpu_bound_task, 
        task_count, 
        "CPU 任务"
    )
    
    # 多线程
    thread_time, thread_results = run_threading(
        cpu_bound_task, 
        task_count, 
        max_workers,
        "CPU 任务"
    )
    
    # 多进程
    process_time, process_results = run_multiprocessing(
        cpu_bound_task, 
        task_count, 
        max_workers,
        "CPU 任务"
    )
    
    # 对比结果
    print(f"\n{'='*70}")
    print("📈 CPU 密集型任务 - 性能对比总结")
    print(f"{'='*70}")
    print(f"{'方式':<15} {'耗时':<12} {'加速比':<12} {'评级'}")
    print(f"{'-'*70}")
    print(f"{'串行':<15} {serial_time:<12.2f} {'1.00x':<12} ⭐⭐")
    print(f"{'多线程':<14} {thread_time:<12.2f} {serial_time/thread_time:<12.2f}x ⭐⭐ (受GIL限制)")
    print(f"{'多进程':<14} {process_time:<12.2f} {serial_time/process_time:<12.2f}x ⭐⭐⭐⭐⭐")
    
    print(f"\n💡 结论：CPU 密集型任务最适合使用多进程")
    print(f"   - 多线程几乎无加速（受 GIL 限制）")
    print(f"   - 多进程加速比: {serial_time/process_time:.2f}x")


def show_comparison_table():
    """显示综合对比表"""
    print("\n" + "="*70)
    print("📋 并发模型综合对比表")
    print("="*70)
    
    table = """
┌──────────────┬──────────────┬──────────────┬──────────────┐
│     特性      │   串行执行    │   多线程      │   多进程      │
├──────────────┼──────────────┼──────────────┼──────────────┤
│ 创建开销      │     无       │     小       │     大       │
│ 切换开销      │     无       │     小       │     大       │
│ 内存占用      │     小       │     中       │     大       │
│ 数据共享      │    简单      │    较简单    │    复杂      │
│ I/O密集型    │     慢       │   非常快 ⚡  │     快       │
│ CPU密集型    │     慢       │     慢       │   非常快 ⚡  │
│ 稳定性        │     高       │     中       │     高       │
│ 调试难度      │    简单      │    较难      │    较难      │
│ 适用场景      │   简单任务   │  I/O密集任务 │ CPU密集任务  │
└──────────────┴──────────────┴──────────────┴──────────────┘

选择建议：
✅ I/O 密集型（网络、文件、数据库） → 多线程
✅ CPU 密集型（计算、处理） → 多进程
✅ 超高并发（>1000连接） → 协程 (asyncio)
✅ 简单任务、顺序依赖 → 串行
    """
    print(table)


# ==================== 主函数 ====================

def main():
    print("="*70)
    print("并发模型对比演示")
    print("多线程 vs 多进程 vs 串行")
    print("="*70)
    print(f"CPU 核心数: {os.cpu_count()}")
    print(f"当前进程 ID: {os.getpid()}")
    
    # 对比 I/O 密集型
    compare_io_bound()
    
    # 对比 CPU 密集型
    compare_cpu_bound()
    
    # 显示对比表
    show_comparison_table()
    
    print("\n" + "="*70)
    print("🎯 学习要点")
    print("="*70)
    print("""
1. I/O 密集型任务：
   - 多线程 >> 多进程 > 串行
   - 原因：I/O 等待时线程可以切换

2. CPU 密集型任务：
   - 多进程 >> 串行 ≈ 多线程
   - 原因：GIL 限制多线程并行执行

3. 实际应用中：
   - Web 服务、爬虫 → 多线程
   - 数据处理、计算 → 多进程
   - 高并发服务器 → asyncio
   
4. 线程池/进程池大小：
   - I/O 密集：CPU核心数 * 2 + 1
   - CPU 密集：CPU核心数
   - 通过压测找到最佳值
    """)
    
    print("\n" + "="*70)
    print("演示完成！")
    print("="*70)


if __name__ == "__main__":
    main()
