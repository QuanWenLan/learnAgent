"""
网络编程教程快速启动脚本

运行此脚本查看所有可用的示例和项目
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))


def print_menu():
    """打印菜单"""
    print("\n" + "="*70)
    print("Python 网络编程教程 - 快速启动")
    print("="*70)
    
    print("\n📚 第一阶段：Socket 基础")
    print("-" * 70)
    print("1. socket_basics.py - Socket 基础教程")
    print("   包含：TCP/UDP、HTTP 客户端、粘包问题、聊天室等")
    print("   运行: python socket_basics.py")
    
    print("\n🔧 补充主题")
    print("-" * 70)
    print("2. asyncio_thread_usage.py - asyncio 中的线程使用")
    print("   包含：run_in_executor、混合异步同步、错误处理等")
    print("   运行: python asyncio_thread_usage.py")
    
    print("\n🚀 第二阶段：实战项目")
    print("-" * 70)
    print("3. network_projects.py - 完整实战项目")
    print("   包含：聊天服务器、HTTP 服务器、性能对比、连接池")
    print("   运行: python network_projects.py")
    
    print("\n📖 学习文档")
    print("-" * 70)
    print("4. README.md - 快速入门指南")
    print("5. NETWORK_LEARNING_GUIDE.md - 详细学习指南（推荐先读）")
    
    print("\n" + "="*70)
    print("💡 建议学习顺序:")
    print("="*70)
    print("1️⃣  先阅读 README.md 了解整体结构")
    print("2️⃣  阅读 NETWORK_LEARNING_GUIDE.md 制定学习计划")
    print("3️⃣  运行 socket_basics.py 学习基础知识")
    print("4️⃣  动手实验 TCP/UDP 示例")
    print("5️⃣  实现聊天室项目")
    print("6️⃣  运行 network_projects.py 进行实战")
    print("7️⃣  根据需要学习 asyncio_thread_usage.py")
    print("="*70)


def quick_demo():
    """快速演示"""
    print("\n" + "="*70)
    print("快速演示 - 性能对比")
    print("="*70)
    
    try:
        from network_projects import PerformanceComparison
        
        perf = PerformanceComparison()
        perf.run_comparison()
        
    except Exception as e:
        print(f"\n演示出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "demo":
            quick_demo()
        elif command == "socket":
            from socket_basics import main
            main()
        elif command == "asyncio":
            import asyncio
            from asyncio_thread_usage import main
            asyncio.run(main())
        elif command == "projects":
            from network_projects import main
            main()
        else:
            print(f"未知命令: {command}")
            print_menu()
    else:
        print_menu()
        
        # 询问是否运行快速演示
        print("\n是否运行快速性能对比演示？(y/n): ", end="")
        try:
            choice = input().strip().lower()
            if choice == 'y':
                quick_demo()
        except:
            pass
