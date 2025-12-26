# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 一键启动脚本
One-click startup script for both backend and frontend
"""

import subprocess
import sys
import time
import os
import threading
import webbrowser
import socket  # 新增：用于服务健康检查
from config import BACKEND_HOST, BACKEND_PORT, SYSTEM_NAME, SYSTEM_VERSION, validate_config

def print_banner():
    """打印启动横幅（去掉框线，保持排版）"""
    # 用等号分隔线+居中对齐替代框线，保持内容结构
    banner = f"""
                {"=" * 70}
                {"AI 智能辅助学习系统 (Intelligent Learning OS)":^70}
                {SYSTEM_VERSION:^70}
                {"让学习更智能，让成长更高效":^70}
                {"=" * 70}
                📚 支持学科: 语文 | 数学 | 英语 | 历史 | 政治
                🤖 AI 功能: 智能教学 | 深度评估 | 迁移测试 | 补救教学
                📝 题目类型: 选择题 | 判断题 | 问答题 | 填空题 | 应用题
                {"=" * 70}
                """
    print(banner)


def check_dependencies():
    """检查依赖是否安装"""
    print("📦 检查依赖...")

    required = ['fastapi', 'uvicorn', 'streamlit', 'langchain', 'langchain_openai', 'requests', 'pydantic']
    missing = []

    for package in required:
        try:
            # 处理安装名与导入名差异（如langchain-openai -> langchain_openai）
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)

    if missing:
        print(f"❌ 缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False

    print("✅ 依赖检查通过")
    return True


def check_config():
    """检查配置并允许用户选择是否继续"""
    print("🔧 检查配置...")

    if not validate_config():
        print("⚠️  配置不完整（如API_KEY缺失），可能导致部分功能无法使用")
        while True:
            choice = input("是否继续启动？(y/n): ").strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("请输入 y 或 n")

    print("✅ 配置检查通过")
    return True


def wait_for_service(host, port, timeout=30, interval=1):
    """等待服务启动（替代固定sleep）"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(interval)
            if int(time.time() - start_time) % 5 == 0:  # 每5秒提示一次
                print(f"⏳ 等待服务启动中（{int(time.time() - start_time)}/{timeout}秒）...")
    return False


def start_backend():
    """启动后端服务并检查健康状态"""
    print("\n🚀 启动后端服务...")
    try:
        process = subprocess.Popen(
            [sys.executable, "backend.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True  # 文本模式便于读取输出
        )

        # 等待服务启动
        if not wait_for_service(BACKEND_HOST, BACKEND_PORT):
            stderr = process.stderr.read()
            print(f"❌ 后端服务启动失败:\n{stderr}")
            process.terminate()
            return None

        print(f"✅ 后端服务已启动: http://{BACKEND_HOST}:{BACKEND_PORT}")
        print(f"   API 文档: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
        return process
    except Exception as e:
        print(f"❌ 启动后端时发生错误: {str(e)}")
        return None


def start_frontend():
    """启动前端服务并检查健康状态"""
    print("\n🚀 启动前端服务...")
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", "frontend.py",
             "--server.headless", "true",
             "--browser.gatherUsageStats", "false"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待前端启动
        if not wait_for_service("localhost", 8501):
            stderr = process.stderr.read()
            print(f"❌ 前端服务启动失败:\n{stderr}")
            process.terminate()
            return None

        print("✅ 前端服务已启动: http://localhost:8501")
        return process
    except Exception as e:
        print(f"❌ 启动前端时发生错误: {str(e)}")
        return None


def open_browser():
    """打开浏览器（服务确认启动后调用）"""
    webbrowser.open("http://localhost:8501")
    print("🌐 已自动打开浏览器，如未打开请手动访问: http://localhost:8501")


def main():
    """主函数"""
    print_banner()

    # 依赖检查（不通过则退出）
    if not check_dependencies():
        sys.exit(1)

    # 配置检查（用户选择不继续则退出）
    if not check_config():
        sys.exit(1)

    print("\n" + "=" * 70)

    # 启动后端服务
    backend_process = start_backend()
    if not backend_process:
        sys.exit(1)

    # 启动前端服务
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        sys.exit(1)

    print("\n" + "=" * 70)
    print("""
🎉 系统启动成功！

📱 访问地址:
   • 前端界面: http://localhost:8501
   • API 文档: http://localhost:8000/docs

💡 使用说明:
   1. 学生端: 选择科目 → 与 AI 导师对话 → 做练习 → 掌握知识
   2. 管理端: 查看数据 → 管理题目 → 管理知识库

⚠️  按 Ctrl+C 停止服务
    """)

    # 打开浏览器（服务已确认启动，无需延迟）
    threading.Thread(target=open_browser, daemon=True).start()

    # 保持运行并处理退出
    try:
        # 等待前端进程结束（前端通常是用户交互主入口）
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 正在关闭服务...")
        # 确保所有子进程都被终止
        frontend_process.terminate()
        backend_process.terminate()
        # 等待进程退出
        frontend_process.wait(timeout=5)
        backend_process.wait(timeout=5)
        print("✅ 服务已关闭，再见！")
    finally:
        # 清理残留进程
        if frontend_process.poll() is None:
            frontend_process.kill()
        if backend_process.poll() is None:
            backend_process.kill()

if __name__ == "__main__":
    main()