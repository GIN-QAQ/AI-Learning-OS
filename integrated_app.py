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

# 添加当前目录到Python路径，确保能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入项目模块
from config import SYSTEM_NAME, SYSTEM_VERSION, BACKEND_HOST, BACKEND_PORT, validate_config
from backend import app as fastapi_app
from frontend import (render_header, render_subject_selection, render_learning_interface, 
                     render_admin_dashboard, render_question_management, init_session_state)

# 页面配置
st.set_page_config(
    page_title=SYSTEM_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 启动FastAPI后端服务

def start_backend():
    """启动FastAPI后端服务"""
    uvicorn.run(fastapi_app, host=BACKEND_HOST, port=BACKEND_PORT, log_level="info")

# 检查后端服务是否可用

def check_backend_health():
    """检查后端服务是否可用"""
    try:
        response = requests.get(f"http://{BACKEND_HOST}:{BACKEND_PORT}/api/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# 主函数

def main():
    """主函数"""
    # 初始化会话状态
    init_session_state()
    
    # 渲染页面头部
    render_header()
    
    # 根据当前模式显示不同界面
    if st.session_state.mode == "student":
        if st.session_state.current_subject:
            render_learning_interface()
        else:
            render_subject_selection()
    else:
        # 管理端
        tab1, tab2 = st.tabs(["📊 数据看板", "📝 题目管理"])
        with tab1:
            render_admin_dashboard()
        with tab2:
            render_question_management()

# 启动后端服务

@st.cache_resource
def start_backend_service():
    """启动后端服务并缓存"""
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 等待后端服务启动
    for _ in range(10):
        if check_backend_health():
            st.success(f"✅ 后端服务已启动: http://{BACKEND_HOST}:{BACKEND_PORT}")
            st.success(f"   API 文档: http://{BACKEND_HOST}:{BACKEND_PORT}/docs")
            return True
        time.sleep(1)
    
    st.error("❌ 后端服务启动失败")
    return False

# 执行主程序

if __name__ == "__main__":
    # 启动后端服务
    backend_started = start_backend_service()
    
    # 如果后端服务启动成功，显示主界面
    if backend_started:
        main()
    else:
        st.error("无法启动系统，请检查配置和依赖")
