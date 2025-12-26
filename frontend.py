# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - Streamlit 前端
Frontend UI with student and admin modes
"""

import streamlit as st
import requests
import time
from datetime import datetime
from typing import Optional, List, Dict, Any
from config import BACKEND_URL, SYSTEM_NAME, SYSTEM_VERSION, validate_config

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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
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

    /* 学科卡片 */
    .subject-card {
        background: white;
        border-radius: 1.5rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 0.5rem;
    }

    .subject-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .subject-icon {
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }

    .subject-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: #333;
    }

    /* 聊天消息 */
    .chat-message {
        padding: 1rem 1.5rem;
        border-radius: 1.5rem;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease;
    }

    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 20%;
        border-bottom-right-radius: 0.5rem;
    }

    .assistant-message {
        background: white;
        color: #333;
        margin-right: 20%;
        border-bottom-left-radius: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    /* 统计卡片 */
    .stat-card {
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }

    .stat-label {
        color: #666;
        font-size: 0.9rem;
    }

    /* 动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease;
    }

    .slide-in {
        animation: slideIn 0.5s ease;
    }

    /* 模式切换按钮 */
    .mode-switcher {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
    }

    /* 侧边栏样式 */
    .sidebar-section {
        background: black;
        border-radius: 1rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }

    /* 进度条 */
    .progress-bar {
        background: #e0e0e0;
        border-radius: 0.5rem;
        height: 0.5rem;
        overflow: hidden;
    }

    .progress-fill {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 0.5rem;
        transition: width 0.3s ease;
    }

    /* 隐藏 Streamlit 默认元素 */
    #MainMenu {visibility: visible;}
    footer {visibility: visible;}
    header {visibility: visible;}
    </style>
    """, unsafe_allow_html=True)

# API 调用函数

def api_get(endpoint: str) -> Optional[Dict]:
    """GET 请求"""
    try:
        response = requests.get(f"{BACKEND_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API 请求失败: {e}")
        return None

def api_post(endpoint: str, data: Dict) -> Optional[Dict]:
    """POST 请求"""
    try:
        response = requests.post(f"{BACKEND_URL}{endpoint}", json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API 请求失败: {e}")
        return None

def api_put(endpoint: str, data: Dict) -> Optional[Dict]:
    """PUT 请求"""
    try:
        response = requests.put(f"{BACKEND_URL}{endpoint}", json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API 请求失败: {e}")
        return None

def api_delete(endpoint: str) -> bool:
    """DELETE 请求"""
    try:
        response = requests.delete(f"{BACKEND_URL}{endpoint}", timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"API 请求失败: {e}")
        return False

# 初始化 Session State
def init_session_state():
    """初始化会话状态"""
    if "mode" not in st.session_state:
        st.session_state.mode = "student"  # student 或 admin
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = None
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "mastery_level" not in st.session_state:
        st.session_state.mastery_level = 0

# 页面头部
def render_header():
    """渲染页面头部"""
    st.markdown(f"""
    <div class="fade-in" style="text-align: center; padding: 1rem;">
        <h1 class="main-title">🎓 {SYSTEM_NAME}</h1>
        <p class="subtitle">{SYSTEM_VERSION} | 智能学习，因材施教</p>
    </div>
    """, unsafe_allow_html=True)

    # 模式切换
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mode_cols = st.columns(2)
        with mode_cols[0]:
            if st.button("👨‍🎓 学生端", use_container_width=True,
                         type="primary" if st.session_state.mode == "student" else "secondary"):
                st.session_state.mode = "student"
                st.session_state.current_subject = None
                st.session_state.session_id = None
                st.session_state.messages = []
                st.rerun()
        with mode_cols[1]:
            if st.button("👨‍💼 管理端", use_container_width=True,
                         type="primary" if st.session_state.mode == "admin" else "secondary"):
                st.session_state.mode = "admin"
                st.rerun()

    st.markdown("---")

# 学生端 - 学科选择
def render_subject_selection():
    """渲染学科选择页面"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.markdown("### 📚 选择学习科目")
    st.markdown("点击下方卡片，开始你的智能学习之旅")
    st.markdown("")

    subjects = [
        {"id": "chinese", "name": "语文", "icon": "📖", "desc": "阅读理解、写作技巧、古诗词鉴赏"},
        {"id": "math", "name": "数学", "icon": "📐", "desc": "代数方程、函数图像、几何证明"},
        {"id": "english", "name": "英语", "icon": "🌍", "desc": "语法时态、阅读写作、口语表达"},
        {"id": "history", "name": "历史", "icon": "🏛️", "desc": "中国历史、世界历史、历史分析"},
        {"id": "politics", "name": "政治", "icon": "⚖️", "desc": "政治理论、经济常识、时事分析"},
    ]

    cols = st.columns(5)
    for i, subj in enumerate(subjects):
        with cols[i]:
            with st.container():
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 3rem;">{subj['icon']}</div>
                    <div style="font-weight: bold; font-size: 1.2rem; margin: 0.5rem 0;">{subj['name']}</div>
                    <div style="color: #666; font-size: 0.8rem;">{subj['desc']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"开始学习", key=f"subj_{subj['id']}", use_container_width=True):
                    # 创建会话
                    result = api_post("/api/sessions", {
                        "student_id": "streamlit_user",
                        "subject": subj['id']
                    })
                    if result:
                        st.session_state.current_subject = subj['id']
                        st.session_state.session_id = result['session_id']
                        st.session_state.messages = [
                            {"role": "assistant", "content": result['welcome_message']}
                        ]
                        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# 学生端 - 学习对话界面
def render_learning_interface():
    """渲染学习对话界面"""

    # 侧边栏 - 学习状态
    with st.sidebar:
        st.markdown("### 📊 学习状态")

        # 返回按钮
        if st.button("← 返回选择科目", use_container_width=True):
            st.session_state.current_subject = None
            st.session_state.session_id = None
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")

        # 当前科目
        subject_names = {
            "chinese": "📖 语文", "math": "📐 数学", "english": "🌍 英语",
            "history": "🏛️ 历史", "politics": "⚖️ 政治"
        }
        st.markdown(f"**当前科目：** {subject_names.get(st.session_state.current_subject, '未知')}")

        # 掌握度进度条
        st.markdown("**掌握度**")
        progress = st.session_state.mastery_level / 100
        st.progress(progress)
        st.markdown(f"当前等级: **{get_grade_display(progress)}**")

        st.markdown("---")

        # 直觉泵/提示
        st.markdown("### 💡 学习提示")
        tips = get_learning_tips(st.session_state.current_subject)
        for tip in tips:
            st.info(tip)

        st.markdown("---")

        # 常见误区
        st.markdown("### ⚠️ 常见误区")
        mistakes = get_common_mistakes(st.session_state.current_subject)
        for mistake in mistakes:
            st.warning(mistake)

    # 主内容区 - 对话界面
    st.markdown("### 💬 AI 导师对话")

    # 消息容器
    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                with st.chat_message("user", avatar="👨‍🎓"):
                    st.markdown(msg["content"])
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(msg["content"])

    # 输入区
    if prompt := st.chat_input("输入你的问题或回答..."):
        # 添加用户消息
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 发送到后端
        with st.spinner("AI 导师思考中..."):
            result = api_post("/api/chat", {
                "session_id": st.session_state.session_id,
                "message": prompt,
                "student_id": "streamlit_user"
            })

        if result:
            # 添加助手回复
            st.session_state.messages.append({
                "role": "assistant",
                "content": result['response']
            })

            # 更新掌握度
            if result.get('grade') == 'A':
                st.session_state.mastery_level = min(100, st.session_state.mastery_level + 20)
            elif result.get('grade') == 'B':
                st.session_state.mastery_level = min(100, st.session_state.mastery_level + 10)

            # 检查是否掌握
            if result.get('mastered'):
                st.balloons()

            st.rerun()

    # 快捷操作按钮
    st.markdown("---")
    cols = st.columns(4)
    with cols[0]:
        if st.button("📝 开始练习", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "我想做一些练习题"})
            result = api_post("/api/chat", {
                "session_id": st.session_state.session_id,
                "message": "我想做一些练习题",
                "student_id": "streamlit_user"
            })
            if result:
                st.session_state.messages.append({"role": "assistant", "content": result['response']})
                st.rerun()

    with cols[1]:
        if st.button("💡 给我提示", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "给我一些提示"})
            result = api_post("/api/chat", {
                "session_id": st.session_state.session_id,
                "message": "给我一些提示",
                "student_id": "streamlit_user"
            })
            if result:
                st.session_state.messages.append({"role": "assistant", "content": result['response']})
                st.rerun()

    with cols[2]:
        if st.button("📖 知识总结", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "请帮我总结一下今天学习的内容"})
            result = api_post("/api/chat", {
                "session_id": st.session_state.session_id,
                "message": "请帮我总结一下今天学习的内容",
                "student_id": "streamlit_user"
            })
            if result:
                st.session_state.messages.append({"role": "assistant", "content": result['response']})
                st.rerun()

    with cols[3]:
        if st.button("🔄 清空对话", use_container_width=True):
            # 重新创建会话
            result = api_post("/api/sessions", {
                "student_id": "streamlit_user",
                "subject": st.session_state.current_subject
            })
            if result:
                st.session_state.session_id = result['session_id']
                st.session_state.messages = [
                    {"role": "assistant", "content": result['welcome_message']}
                ]
                st.rerun()


def get_grade_display(progress: float) -> str:
    """获取等级显示"""
    if progress >= 0.85:
        return "A 🌟 优秀"
    elif progress >= 0.6:
        return "B 👍 良好"
    else:
        return "C 📚 学习中"


def get_learning_tips(subject: str) -> List[str]:
    """获取学习提示"""
    tips = {
        "chinese": ["多读多写是提高语文的关键", "理解文章要先了解作者背景"],
        "math": ["先理解概念再做题", "画图可以帮助理解几何问题"],
        "english": ["每天背诵10个单词", "多听英语培养语感"],
        "history": ["用时间线梳理历史事件", "理解历史要看因果关系"],
        "politics": ["结合时事理解理论", "注意概念之间的联系"],
    }
    return tips.get(subject, ["认真学习，持之以恒"])


def get_common_mistakes(subject: str) -> List[str]:
    """获取常见误区"""
    mistakes = {
        "chinese": ["混淆比喻和拟人"],
        "math": ["公式符号使用错误"],
        "english": ["时态使用混乱"],
        "history": ["时间点记忆混淆"],
        "politics": ["概念理解表面化"],
    }
    return mistakes.get(subject, ["粗心大意"])


# ============================================
# 管理端 - 数据看板
# ============================================

def render_admin_dashboard():
    """渲染管理端数据看板"""
    st.markdown("### 📊 数据看板")

    # 获取统计数据
    stats = api_get("/api/admin/stats")

    if stats:
        # 核心指标
        cols = st.columns(4)
        metrics = [
            ("👥 活跃学生", stats.get('active_students', 0), "人"),
            ("📚 知识库条目", stats.get('knowledge_count', 0), "条"),
            ("🤖 AI 交互次数", stats.get('ai_interactions', 0), "次"),
            ("📈 平均掌握度", f"{stats.get('average_mastery', 0) * 100:.1f}", "%"),
        ]

        for i, (label, value, unit) in enumerate(metrics):
            with cols[i]:
                st.metric(label=label, value=f"{value}{unit}")

        st.markdown("---")

        # 学科统计
        st.markdown("### 📊 各学科数据")
        subject_stats = stats.get('subject_stats', {})

        subject_names = {
            "chinese": "语文", "math": "数学", "english": "英语",
            "history": "历史", "politics": "政治"
        }

        cols = st.columns(5)
        for i, (subj_id, subj_name) in enumerate(subject_names.items()):
            with cols[i]:
                subj_data = subject_stats.get(subj_id, {})
                st.markdown(f"**{subj_name}**")
                st.write(f"📝 题目: {subj_data.get('questions', 0)}")
                st.write(f"📖 知识点: {subj_data.get('knowledge', 0)}")
                st.write(f"🗂️ 主题: {subj_data.get('topics', 0)}")

# 管理端 - 题目管理

def render_question_management():
    """渲染题目管理"""
    st.markdown("### 📝 题目管理")

    tab1, tab2 = st.tabs(["题目列表", "添加题目"])

    with tab1:
        # 过滤器
        cols = st.columns(4)
        with cols[0]:
            filter_subject = st.selectbox(
                "学科",
                ["全部", "chinese", "math", "english", "history", "politics"],
                format_func=lambda x: {"全部": "全部", "chinese": "语文", "math": "数学",
                                       "english": "英语", "history": "历史", "politics": "政治"}.get(x, x)
            )
        with cols[1]:
            filter_type = st.selectbox(
                "题型",
                ["全部", "choice", "judgment", "qa", "fill", "application"],
                format_func=lambda x: {"全部": "全部", "choice": "选择题", "judgment": "判断题",
                                       "qa": "问答题", "fill": "填空题", "application": "应用题"}.get(x, x)
            )
        with cols[2]:
            filter_difficulty = st.selectbox("难度", ["全部", "1", "2", "3", "4", "5"])

        # 获取题目
        endpoint = "/api/questions"
        params = []
        if filter_subject != "全部":
            params.append(f"subject={filter_subject}")
        if filter_type != "全部":
            params.append(f"question_type={filter_type}")
        if filter_difficulty != "全部":
            params.append(f"difficulty={filter_difficulty}")

        if params:
            endpoint += "?" + "&".join(params)

        questions = api_get(endpoint) or []

        st.markdown(f"共 **{len(questions)}** 道题目")

        for q in questions:
            with st.expander(f"📝 {q['content'][:50]}..." if len(
                    q.get('content', '')) > 50 else f"📝 {q.get('content', '无内容')}"):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"**学科:** {q.get('topic_name', '未知')}")
                    st.write(f"**题型:** {q.get('question_type', '未知')}")
                    st.write(f"**难度:** {'⭐' * q.get('difficulty', 1)}")
                    st.write(f"**题目:** {q.get('content', '')}")
                    if q.get('options'):
                        st.write(f"**选项:** {', '.join(q.get('options', []))}")
                    st.write(f"**答案:** {q.get('correct_answer', '')}")
                    st.write(f"**解析:** {q.get('explanation', '')}")
                with cols[1]:
                    if st.button("🗑️ 删除", key=f"del_q_{q['id']}"):
                        if api_delete(f"/api/questions/{q['id']}"):
                            st.success("删除成功")
                            st.rerun()

    with tab2:
        with st.form("add_question_form"):
            st.markdown("#### 添加新题目")

            cols = st.columns(2)
            with cols[0]:
                new_subject = st.selectbox(
                    "学科 *",
                    ["chinese", "math", "english", "history", "politics"],
                    format_func=lambda x: {"chinese": "语文", "math": "数学",
                                           "english": "英语", "history": "历史", "politics": "政治"}.get(x, x),
                    key="new_q_subject"
                )
            with cols[1]:
                new_type = st.selectbox(
                    "题型 *",
                    ["choice", "judgment", "qa", "fill", "application"],
                    format_func=lambda x: {"choice": "选择题", "judgment": "判断题",
                                           "qa": "问答题", "fill": "填空题", "application": "应用题"}.get(x, x),
                    key="new_q_type"
                )

            cols = st.columns(3)
            with cols[0]:
                new_topic_id = st.text_input("主题 ID *", key="new_q_topic_id")
            with cols[1]:
                new_topic_name = st.text_input("主题名称 *", key="new_q_topic_name")
            with cols[2]:
                new_difficulty = st.slider("难度 *", 1, 5, 3, key="new_q_difficulty")

            new_content = st.text_area("题目内容 *", key="new_q_content")

            new_options = st.text_input("选项（用逗号分隔，如：A. 选项1, B. 选项2）", key="new_q_options")
            new_answer = st.text_input("正确答案 *", key="new_q_answer")
            new_explanation = st.text_area("解析 *", key="new_q_explanation")
            new_is_transfer = st.checkbox("迁移测试题", key="new_q_transfer")

            submitted = st.form_submit_button("添加题目", use_container_width=True)

            if submitted:
                if new_topic_id and new_topic_name and new_content and new_answer:
                    options = [o.strip() for o in new_options.split(",")] if new_options else None

                    result = api_post("/api/questions", {
                        "subject": new_subject,
                        "topic_id": new_topic_id,
                        "topic_name": new_topic_name,
                        "question_type": new_type,
                        "difficulty": new_difficulty,
                        "content": new_content,
                        "options": options,
                        "correct_answer": new_answer,
                        "explanation": new_explanation,
                        "is_transfer": new_is_transfer
                    })

                    if result:
                        st.success("✅ 题目添加成功！")
                        st.rerun()
                else:
                    st.error("请填写所有必填字段（带 * 的项）")

# 管理端 - 知识库管理

def render_knowledge_management():
    """渲染知识库管理"""
    st.markdown("### 📚 知识库管理")

    tab1, tab2 = st.tabs(["知识点列表", "添加知识点"])

    with tab1:
        # 过滤器
        cols = st.columns(2)
        with cols[0]:
            filter_subject = st.selectbox(
                "学科筛选",
                ["全部", "chinese", "math", "english", "history", "politics"],
                format_func=lambda x: {"全部": "全部", "chinese": "语文", "math": "数学",
                                       "english": "英语", "history": "历史", "politics": "政治"}.get(x, x),
                key="knowledge_filter_subject"
            )

        # 获取知识点
        endpoint = "/api/knowledge"
        if filter_subject != "全部":
            endpoint += f"?subject={filter_subject}"

        knowledge_items = api_get(endpoint) or []

        st.markdown(f"共 **{len(knowledge_items)}** 条知识点")

        for k in knowledge_items:
            with st.expander(f"📖 {k.get('title', '无标题')}"):
                cols = st.columns([3, 1])
                with cols[0]:
                    st.write(f"**主题:** {k.get('topic_name', '未知')}")
                    st.write(f"**内容:** {k.get('content', '')[:200]}...")
                    st.write(f"**要点:** {', '.join(k.get('key_points', []))}")
                    st.write(f"**常见误区:** {', '.join(k.get('common_mistakes', []))}")
                    st.write(f"**标签:** {', '.join(k.get('tags', []))}")
                with cols[1]:
                    if st.button("🗑️ 删除", key=f"del_k_{k['id']}"):
                        if api_delete(f"/api/knowledge/{k['id']}"):
                            st.success("删除成功")
                            st.rerun()

    with tab2:
        with st.form("add_knowledge_form"):
            st.markdown("#### 添加新知识点")

            cols = st.columns(2)
            with cols[0]:
                new_subject = st.selectbox(
                    "学科 *",
                    ["chinese", "math", "english", "history", "politics"],
                    format_func=lambda x: {"chinese": "语文", "math": "数学",
                                           "english": "英语", "history": "历史", "politics": "政治"}.get(x, x),
                    key="new_k_subject"
                )
            with cols[1]:
                new_source_type = st.selectbox(
                    "来源类型",
                    ["text", "pdf", "link"],
                    format_func=lambda x: {"text": "文本", "pdf": "PDF", "link": "链接"}.get(x, x),
                    key="new_k_source"
                )

            cols = st.columns(2)
            with cols[0]:
                new_topic_id = st.text_input("主题 ID *", key="new_k_topic_id")
            with cols[1]:
                new_topic_name = st.text_input("主题名称 *", key="new_k_topic_name")

            new_title = st.text_input("标题 *", key="new_k_title")
            new_content = st.text_area("内容 *", height=150, key="new_k_content")

            new_key_points = st.text_input("要点（用逗号分隔）", key="new_k_points")
            new_mistakes = st.text_input("常见误区（用逗号分隔）", key="new_k_mistakes")
            new_intuition = st.text_input("直觉泵/提示（用逗号分隔）", key="new_k_intuition")
            new_tags = st.text_input("标签（用逗号分隔）", key="new_k_tags")
            new_source_url = st.text_input("来源 URL（可选）", key="new_k_url")

            submitted = st.form_submit_button("添加知识点", use_container_width=True)

            if submitted:
                if new_topic_id and new_topic_name and new_title and new_content:
                    result = api_post("/api/knowledge", {
                        "subject": new_subject,
                        "topic_id": new_topic_id,
                        "topic_name": new_topic_name,
                        "title": new_title,
                        "content": new_content,
                        "key_points": [p.strip() for p in new_key_points.split(",") if p.strip()],
                        "common_mistakes": [m.strip() for m in new_mistakes.split(",") if m.strip()],
                        "intuition_pumps": [i.strip() for i in new_intuition.split(",") if i.strip()],
                        "tags": [t.strip() for t in new_tags.split(",") if t.strip()],
                        "source_type": new_source_type,
                        "source_url": new_source_url if new_source_url else None
                    })

                    if result:
                        st.success("✅ 知识点添加成功！")
                        st.rerun()
                else:
                    st.error("请填写所有必填字段（带 * 的项）")

# 管理端 - 系统日志

def render_system_logs():
    """渲染系统日志"""
    st.markdown("### 📋 系统日志")

    logs = api_get("/api/admin/logs?limit=50") or []

    if not logs:
        st.info("暂无日志记录")
        return

    for log in logs:
        timestamp = log.get('timestamp', '')[:19]
        log_type = log.get('log_type', 'info')
        message = log.get('message', '')

        icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}.get(log_type, "📝")

        if log_type == "error":
            st.error(f"{icon} [{timestamp}] {message}")
        elif log_type == "warning":
            st.warning(f"{icon} [{timestamp}] {message}")
        elif log_type == "success":
            st.success(f"{icon} [{timestamp}] {message}")
        else:
            st.info(f"{icon} [{timestamp}] {message}")

# 主应用
def main():
    """主函数"""
    load_custom_css()
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
        # 管理端侧边栏
        with st.sidebar:
            st.markdown("### 🔧 管理功能")
            admin_page = st.radio(
                "选择功能",
                ["数据看板", "题目管理", "知识库管理", "系统日志"],
                label_visibility="collapsed"
            )

        # 管理端内容
        with st.container():
            if admin_page == "数据看板":
                render_admin_dashboard()
            elif admin_page == "题目管理":
                render_question_management()
            elif admin_page == "知识库管理":
                render_knowledge_management()
            elif admin_page == "系统日志":
                render_system_logs()

if __name__ == "__main__":
    main()
