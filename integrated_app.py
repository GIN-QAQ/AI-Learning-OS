# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 集成版
Integrated version for Streamlit Cloud Deployment
"""

import streamlit as st
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import threading
import time
import requests
import sys
import os
import socket

# 添加当前目录到Python路径，确保能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入项目模块
from config import SYSTEM_NAME, SYSTEM_VERSION, BACKEND_HOST, BACKEND_PORT, validate_config
from backend import app as fastapi_app
from frontend import (render_header, render_subject_selection, render_learning_interface, 
                     render_admin_dashboard, render_question_management, render_knowledge_management,
                     render_system_logs, init_session_state, load_custom_css)

# 页面配置
st.set_page_config(
    page_title=SYSTEM_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 禁用Streamlit开发者工具和调试信息
st.session_state['debug_mode'] = False

# 隐藏Streamlit调试信息和开发者工具
css = '''
/* 隐藏调试工具栏和调试信息 */
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stToolbarActions"] { display: none !important; }
footer { visibility: hidden !important; }
.stApp > header { display: none !important; }
*[data-testid*="debug"], *[data-testid*="tool"] { display: none !important; }
[data-testid="stAppViewBlockContainer"] { padding-left: 1rem !important; max-width: 100% !important; }
'''
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# 加载自定义CSS
load_custom_css()

# 启动FastAPI后端服务
def start_backend():
    """启动FastAPI后端服务"""
    uvicorn.run(fastapi_app, host=BACKEND_HOST, port=BACKEND_PORT, log_level="info")

# 检查后端服务是否可用
def wait_for_service(host, port, timeout=30, interval=1):
    """等待服务启动(替代固定sleep)"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                return True
        except (ConnectionRefusedError, OSError):
            time.sleep(interval)
    return False

def check_backend_health():
    """检查后端服务是否可用"""
    try:
        response = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def start_backend_service():
    """启动后端服务并返回启动状态"""
    # 检查后端服务是否已经在运行
    if check_backend_health():
        return True
    
    # 启动后端服务
    try:
        # 使用线程启动后端服务
        backend_thread = threading.Thread(target=start_backend, daemon=True)
        backend_thread.start()
        
        # 等待服务启动
        return wait_for_service(BACKEND_HOST, BACKEND_PORT)
    except Exception as e:
        st.error(f"启动后端服务时出错: {str(e)}")
        return False

# 主界面函数
def main():
    """主界面函数"""
    # 初始化会话状态
    init_session_state()
    
    # 渲染头部
    render_header()
    
    # 根据模式渲染内容
    if st.session_state.mode == "student":
        if st.session_state.current_subject is None:
            render_subject_selection()
        else:
            render_learning_interface()
    
    else:  # admin mode
        # 渲染管理功能
        tab1, tab2, tab3, tab4 = st.tabs(["📊 数据看板", "📝 题目管理", "📚 知识库管理", "📋 系统日志"])
        
        with tab1:
            render_admin_dashboard()
        
        with tab2:
            render_question_management()
        
        with tab3:
            render_knowledge_management()
        
        with tab4:
            render_system_logs()

# 执行主程序
def run_app():
    """运行应用程序"""
    # 检查配置
    if not validate_config():
        st.warning("⚠️ 配置不完整(如API_KEY缺失)，可能导致部分功能无法使用")
    
    # 启动后端服务
    backend_started = start_backend_service()
    
    # 如果后端服务启动成功，显示主界面
    if backend_started:
        main()
    else:
        st.error("无法启动系统，请检查配置和依赖")

if __name__ == "__main__":
    run_app()
