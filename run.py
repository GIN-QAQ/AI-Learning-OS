# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 一键启动脚本
仅支持: python run.py 启动 | 适配 Streamlit 部署
彻底解决重复打开页面问题
"""

import subprocess
import sys
import time
import os
import threading
import webbrowser
import socket
from config import BACKEND_HOST, BACKEND_PORT, SYSTEM_NAME, SYSTEM_VERSION, validate_config

# 全局控制：确保浏览器只打开一次（本地模式）
BROWSER_OPENED = False
BROWSER_LOCK = threading.Lock()

# 部署环境检测：判断是否在 Streamlit 云/服务器部署
def is_deployed_environment():
    """判断是否在 Streamlit 部署环境（云/服务器）"""
    return (
        "STREAMLIT_SERVER_PORT" in os.environ or  # Streamlit 部署会自动设置该环境变量
        "STREAMLIT_CLOUD" in os.environ or        # Streamlit Cloud 特有变量
        os.environ.get("SERVER_SOFTWARE") is not None or  # 服务器环境
        not sys.stdout.isatty()  # 非终端环境（部署时通常无终端）
    )

def print_banner():
    """打印启动横幅"""
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
        # 部署环境下不阻塞，直接继续
        if is_deployed_environment():
            print("📢 部署环境下自动继续启动...")
            return True
        # 本地环境询问用户
        while True:
            choice = input("是否继续启动？(y/n): ").strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("请输入 y 或 n")
    print("✅ 配置检查通过")
    return True

def is_port_in_use(host, port):
    """检查端口是否被占用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def wait_for_service(host, port, timeout=30, interval=1):
    """等待服务启动"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(host, port):
            return True
        time.sleep(interval)
        if int(time.time() - start_time) % 5 == 0 and not is_deployed_environment():
            print(f"⏳ 等待服务启动中（{int(time.time() - start_time)}/{timeout}秒）...")
    return False

def start_backend():
    """启动后端服务（适配部署环境）"""
    print("\n🚀 启动后端服务...")
    
    # 部署环境下：使用 Streamlit 分配的端口（避免冲突）
    if is_deployed_environment():
        backend_port = int(os.environ.get("BACKEND_PORT", BACKEND_PORT))
        backend_host = os.environ.get("BACKEND_HOST", BACKEND_HOST)
    else:
        backend_port = BACKEND_PORT
        backend_host = BACKEND_HOST

    # 本地环境检查端口占用，部署环境跳过（由平台管理）
    if not is_deployed_environment() and is_port_in_use(backend_host, backend_port):
        print(f"⚠️  后端端口 {backend_port} 已被占用，使用已有服务")
        return None
    
    try:
        # 部署环境下后端以无头模式运行，日志重定向
        process_kwargs = {
            "args": [sys.executable, "backend.py"],
            "stdout": subprocess.PIPE if is_deployed_environment() else subprocess.PIPE,
            "stderr": subprocess.PIPE if is_deployed_environment() else subprocess.PIPE,
            "text": True
        }
        if is_deployed_environment():
            process_kwargs["stdout"] = subprocess.DEVNULL
            process_kwargs["stderr"] = subprocess.DEVNULL

        process = subprocess.Popen(**process_kwargs)

        if not wait_for_service(backend_host, backend_port):
            if not is_deployed_environment():
                stderr = process.stderr.read()
                print(f"❌ 后端服务启动失败:\n{stderr}")
            process.terminate()
            return None

        print(f"✅ 后端服务已启动: http://{backend_host}:{backend_port}")
        if not is_deployed_environment():
            print(f"   API 文档: http://{backend_host}:{backend_port}/docs")
        return process
    except Exception as e:
        print(f"❌ 启动后端时发生错误: {str(e)}")
        return None

def safe_open_browser(url):
    """本地环境安全打开浏览器（仅打开一次）"""
    global BROWSER_OPENED
    with BROWSER_LOCK:
        if BROWSER_OPENED or is_deployed_environment():
            return
        if not is_port_in_use(url.split(":")[1].split("/")[0], int(url.split(":")[2].split("/")[0])):
            return
        try:
            # 强制使用新标签页打开，避免重复
            webbrowser.get().open_new_tab(url)
            BROWSER_OPENED = True
            print(f"🌐 已打开浏览器: {url}")
        except:
            print(f"🔗 请手动访问: {url}")

def start_frontend():
    """启动前端服务（核心：彻底禁用自动打开浏览器）"""
    print("\n🚀 启动前端服务...")

    # 部署环境下使用平台分配的端口，本地固定8501
    if is_deployed_environment():
        frontend_port = int(os.environ.get("STREAMLIT_SERVER_PORT", 8501))
        headless = True
    else:
        frontend_port = 8501
        headless = True

    # 本地环境检查端口占用
    if not is_deployed_environment() and is_port_in_use("localhost", frontend_port):
        print(f"⚠️  前端端口 {frontend_port} 已被占用，使用已有服务")
        return None, f"http://localhost:{frontend_port}"

    # Streamlit 启动参数（核心：禁用所有自动打开行为）
    streamlit_args = [
        sys.executable, "-m", "streamlit", "run", "frontend.py",
        "--server.headless", str(headless).lower(),          # 无头模式
        "--browser.gatherUsageStats", "false",               # 禁用统计
        "--server.runOnSave", "false",                       # 禁用自动重载
        "--browser.openBrowser", "false",                    # 核心：禁用自动打开浏览器
        "--server.port", str(frontend_port),                 # 指定端口
        "--server.address", "0.0.0.0" if is_deployed_environment() else "localhost",  # 部署时允许外部访问
    ]

    try:
        # 部署环境下重定向日志，避免干扰
        process_kwargs = {
            "args": streamlit_args,
            "text": True
        }
        if is_deployed_environment():
            process_kwargs["stdout"] = subprocess.DEVNULL
            process_kwargs["stderr"] = subprocess.DEVNULL
        else:
            process_kwargs["stdout"] = subprocess.PIPE
            process_kwargs["stderr"] = subprocess.PIPE

        process = subprocess.Popen(**process_kwargs)

        # 等待前端启动（部署环境跳过超时检查）
        if not is_deployed_environment():
            if not wait_for_service("localhost", frontend_port):
                stderr = process.stderr.read()
                print(f"❌ 前端服务启动失败:\n{stderr}")
                process.terminate()
                return None, ""
        else:
            time.sleep(5)  # 部署环境简单等待

        # 构建访问地址
        if is_deployed_environment():
            frontend_url = f"https://{os.environ.get('STREAMLIT_APP_NAME', 'localhost')}.streamlit.app"
        else:
            frontend_url = f"http://localhost:{frontend_port}"

        print(f"✅ 前端服务已启动: {frontend_url}")
        return process, frontend_url
    except Exception as e:
        print(f"❌ 启动前端时发生错误: {str(e)}")
        return None, ""

def main():
    """主函数：仅支持 python run.py 启动"""
    print_banner()

    # 基础检查
    if not check_dependencies() or not check_config():
        sys.exit(1)

    print("\n" + "=" * 70)

    # 1. 启动后端
    backend_process = start_backend()

    # 2. 启动前端
    frontend_process, frontend_url = start_frontend()
    if not frontend_process and not is_deployed_environment():
        if backend_process:
            backend_process.terminate()
        sys.exit(1)

    # 3. 输出启动信息
    print("\n" + "=" * 70)
    if is_deployed_environment():
        print(f"""
🎉 系统部署成功！
📱 访问地址: {frontend_url}
💡 部署环境下无本地浏览器打开，直接访问上方地址即可
⚠️  关闭终端即可停止服务
        """)
    else:
        print(f"""
🎉 系统启动成功！
📱 访问地址:
   • 前端界面: {frontend_url}
   • API 文档: http://{BACKEND_HOST}:{BACKEND_PORT}/docs
💡 使用说明:
   1. 学生端: 选择科目 → 与 AI 导师对话 → 做练习 → 掌握知识
   2. 管理端: 查看数据 → 管理题目 → 管理知识库
⚠️  按 Ctrl+C 停止服务
        """)
        # 本地环境延迟打开浏览器（仅一次）
        threading.Thread(target=lambda: (time.sleep(2), safe_open_browser(frontend_url)), daemon=True).start()

    # 4. 进程管理（保持运行）
    try:
        # 部署环境下阻塞主线程，本地等待前端进程
        if is_deployed_environment():
            while True:
                time.sleep(3600)  # 部署环境持续运行
        else:
            if frontend_process:
                frontend_process.wait()
    except KeyboardInterrupt:
        print("\n\n👋 正在关闭服务...")
        # 清理进程
        if frontend_process:
            frontend_process.terminate()
            frontend_process.wait(timeout=5)
        if backend_process:
            backend_process.terminate()
            backend_process.wait(timeout=5)
        print("✅ 服务已关闭，再见！")

if __name__ == "__main__":
    # 强制检查启动方式：仅允许 python run.py
    if "streamlit" in sys.argv[0] or any("--streamlit" in arg for arg in sys.argv):
        print("❌ 禁止使用 streamlit run 启动！")
        print("✅ 请使用: python run.py 启动")
        sys.exit(1)
    main()
