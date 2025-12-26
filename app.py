# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - Streamlit 云部署版本
Streamlit Cloud Deployment Version
"""

import streamlit as st
from config import SYSTEM_NAME, SYSTEM_VERSION, validate_config
import sys
import os

# 添加当前目录到Python路径，确保能正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 页面配置
st.set_page_config(
    page_title=SYSTEM_NAME,
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS 样式
def load_custom_css():
    st.markdown("""
    <style>
    /* 全局样式 */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }

    /* 毛玻璃容器 */
    .glass-container {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 2.5rem;
        padding: 2rem;
        margin: 1rem auto;
        max-width: 1400px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* 标题样式 */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    /* 功能卡片 */
    .feature-card {
        background: white;
        border-radius: 1.5rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        margin: 0.5rem;
    }

    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .feature-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .feature-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
    }

    /* 动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# 打印启动横幅

def print_banner():
    """打印启动横幅"""
    st.markdown(f"""
    <div class="fade-in">
        <h1 class="main-title">🎓 {SYSTEM_NAME}</h1>
        <p class="subtitle">{SYSTEM_VERSION} | 智能学习，因材施教</p>
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="color: #666;">让学习更智能，让成长更高效</p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
                <span>📚 支持学科: 语文 | 数学 | 英语 | 历史 | 政治</span>
                <span>🤖 AI 功能: 智能教学 | 深度评估 | 迁移测试 | 补救教学</span>
                <span>📝 题目类型: 选择题 | 判断题 | 问答题 | 填空题 | 应用题</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 检查配置

def check_config():
    """检查配置"""
    st.markdown("### 🔧 配置检查")
    
    if validate_config():
        st.success("✅ 配置检查通过")
        return True
    else:
        st.warning("⚠️ 配置不完整（如API_KEY缺失），可能导致部分功能无法使用")
        return False

# 主界面

def main():
    """主函数"""
    load_custom_css()
    print_banner()
    
    # 配置检查
    check_config()
    
    st.markdown("---")
    
    # 系统功能介绍
    st.markdown("### 🎯 系统功能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👨‍🎓</div>
            <div class="feature-name">学生端</div>
            <p style="color: #666; margin-top: 0.5rem;">
                选择科目 → 与 AI 导师对话 → 做练习 → 掌握知识
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👨‍💼</div>
            <div class="feature-name">管理端</div>
            <p style="color: #666; margin-top: 0.5rem;">
                查看数据 → 管理题目 → 管理知识库
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-name">三级评估</div>
            <p style="color: #666; margin-top: 0.5rem;">
                A/B/C 三个理解等级，科学评估学习效果
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 系统访问信息
    st.markdown("### 📱 访问信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-container">
            <h3 style="text-align: center; color: #667eea;">🎓 学生学习界面</h3>
            <p style="text-align: center; margin-top: 1rem;">
                点击下方按钮进入学生端学习界面
            </p>
            if st.button("进入学习界面", use_container_width=True, type="primary"):
                # 直接跳转到学习界面
                st.switch_page("frontend.py")
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-container">
            <h3 style="text-align: center; color: #667eea;">📖 API 文档</h3>
            <p style="text-align: center; margin-top: 1rem;">
                查看系统 API 文档
            </p>
            if st.button("查看 API 文档", use_container_width=True, type="secondary"):
                # 在新标签页打开 API 文档
                import webbrowser
                webbrowser.open("http://localhost:8000/docs")
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 使用说明
    st.markdown("### 💡 使用说明")
    
    with st.expander("学生端使用指南"):
        st.markdown("""
        1. **学科选择**：进入系统后，选择想要学习的科目
        2. **AI 导师对话**：与 AI 导师进行自然语言对话，采用苏格拉底式提问引导学习
        3. **评估系统**：输入"练习"、"做题"等触发练习模式，系统自动出题并评估回答
        4. **迁移测试**：A级后自动触发应用题测试，验证学生能否举一反三
        5. **补救机制**：连续失败3次触发补救教学，AI 自动切换教学策略
        """
        )
    
    with st.expander("管理端使用指南"):
        st.markdown("""
        1. **数据看板**：查看活跃学生数、知识库条目数、AI 交互次数等统计信息
        2. **题目管理**：按学科、题型、难度筛选题目，支持增删改查
        3. **知识库管理**：上传知识点，关联学科和标签，设置要点和常见误区
        4. **系统日志**：实时查看系统动态，记录知识库更新、系统操作等
        """
        )

# 执行主函数

if __name__ == "__main__":
    main()
