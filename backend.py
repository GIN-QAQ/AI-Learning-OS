"""
AI 智能学习操作系统 - FastAPI 后端
Backend API server with RESTful endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uvicorn
import traceback

from config import BACKEND_HOST, BACKEND_PORT, SYSTEM_NAME, SYSTEM_VERSION
from models import (
    Subject, Question, KnowledgeItem, Session,
    QuestionType, GradeLevel, SessionState,
    ChatRequest, ChatResponse,
    CreateSessionRequest, CreateSessionResponse,
    QuestionCreateRequest, KnowledgeCreateRequest,
    DashboardStats, SystemLog
)
from database import db
from agents import learning_agent

app = FastAPI(
    title=SYSTEM_NAME,
    description="AI 辅助学习系统 API",
    version=SYSTEM_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "sessions": "/api/sessions",
            "questions": "/api/questions",
            "knowledge": "/api/knowledge"
        }
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/sessions", response_model=CreateSessionResponse)
async def create_session(request: CreateSessionRequest):
    session = db.create_session(request.student_id, request.subject)
    welcome = learning_agent.get_welcome_message(request.subject)

    session.messages.append({"role": "assistant", "content": welcome})

    # 防止 DB 持久化异常把接口打挂
    try:
        db.update_session(session)
    except Exception as e:
        print("[create_session] db.update_session failed:", repr(e))
        print(traceback.format_exc())

    return CreateSessionResponse(
        session_id=session.id,
        subject=request.subject,
        welcome_message=welcome
    )

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    session = db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # 关键：捕获 agents 层的真实异常，否则前端只能看到“500 API请求失败”
    try:
        result = learning_agent.process_message(session, request.message)
    except Exception as e:
        print("[/api/chat] process_message failed:", repr(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

    # 这里让 Pydantic 自行把 Enum/Model 做校验与序列化
    try:
        return ChatResponse(
            session_id=session.id,
            response=result["response"],
            state=result["state"],
            grade=result["grade"],
            is_question=result["is_question"],
            question=result.get("question"),
            mastered=result["mastered"]
        )
    except Exception as e:
        # 如果 response_model 校验失败，这里能打印出原因（否则也是 500）
        print("[/api/chat] ChatResponse validation/build failed:", repr(e))
        print("result keys:", list(result.keys()))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"ChatResponse build error: {str(e)}")

@app.get("/api/sessions/{session_id}/messages")
async def get_messages(session_id: str):
    session = db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"messages": session.messages}

@app.get("/api/questions", response_model=List[Question])
async def list_questions(
    subject: Optional[Subject] = None,
    topic_id: Optional[str] = None,
    difficulty: Optional[int] = None,
    question_type: Optional[QuestionType] = None
):
    questions = list(db.questions.values())

    if subject:
        questions = [q for q in questions if q.subject == subject]
    if topic_id:
        questions = [q for q in questions if q.topic_id == topic_id]
    if difficulty:
        questions = [q for q in questions if q.difficulty == difficulty]
    if question_type:
        questions = [q for q in questions if q.question_type == question_type]

    return questions

@app.get("/api/questions/{question_id}", response_model=Question)
async def get_question(question_id: str):
    question = db.questions.get(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@app.post("/api/questions", response_model=Question)
async def create_question(request: QuestionCreateRequest):
    question = Question(
        subject=request.subject,
        topic_id=request.topic_id,
        topic_name=request.topic_name,
        question_type=request.question_type,
        difficulty=request.difficulty,
        content=request.content,
        options=request.options,
        correct_answer=request.correct_answer,
        explanation=request.explanation,
        is_transfer=request.is_transfer
    )
    return db.add_question(question)

@app.put("/api/questions/{question_id}", response_model=Question)
async def update_question(question_id: str, request: QuestionCreateRequest):
    if question_id not in db.questions:
        raise HTTPException(status_code=404, detail="Question not found")

    question = Question(
        id=question_id,
        subject=request.subject,
        topic_id=request.topic_id,
        topic_name=request.topic_name,
        question_type=request.question_type,
        difficulty=request.difficulty,
        content=request.content,
        options=request.options,
        correct_answer=request.correct_answer,
        explanation=request.explanation,
        is_transfer=request.is_transfer
    )
    return db.update_question(question)

@app.delete("/api/questions/{question_id}")
async def delete_question(question_id: str):
    if not db.delete_question(question_id):
        raise HTTPException(status_code=404, detail="Question not found")
    return {"status": "deleted", "id": question_id}

@app.get("/api/knowledge", response_model=List[KnowledgeItem])
async def list_knowledge(
    subject: Optional[Subject] = None,
    topic_id: Optional[str] = None,
    tag: Optional[str] = None
):
    items = list(db.knowledge.values())

    if subject:
        items = [k for k in items if k.subject == subject]
    if topic_id:
        items = [k for k in items if k.topic_id == topic_id]
    if tag:
        items = [k for k in items if tag in k.tags]

    return items

@app.get("/api/knowledge/{knowledge_id}", response_model=KnowledgeItem)
async def get_knowledge(knowledge_id: str):
    item = db.knowledge.get(knowledge_id)
    if not item:
        raise HTTPException(status_code=404, detail="Knowledge item not found")
    return item

@app.post("/api/knowledge", response_model=KnowledgeItem)
async def create_knowledge(request: KnowledgeCreateRequest):
    item = KnowledgeItem(
        subject=request.subject,
        topic_id=request.topic_id,
        topic_name=request.topic_name,
        title=request.title,
        content=request.content,
        key_points=request.key_points,
        common_mistakes=request.common_mistakes,
        intuition_pumps=request.intuition_pumps,
        source_type=request.source_type,
        source_url=request.source_url,
        tags=request.tags
    )
    return db.add_knowledge(item)

@app.put("/api/knowledge/{knowledge_id}", response_model=KnowledgeItem)
async def update_knowledge(knowledge_id: str, request: KnowledgeCreateRequest):
    if knowledge_id not in db.knowledge:
        raise HTTPException(status_code=404, detail="Knowledge item not found")

    item = KnowledgeItem(
        id=knowledge_id,
        subject=request.subject,
        topic_id=request.topic_id,
        topic_name=request.topic_name,
        title=request.title,
        content=request.content,
        key_points=request.key_points,
        common_mistakes=request.common_mistakes,
        intuition_pumps=request.intuition_pumps,
        source_type=request.source_type,
        source_url=request.source_url,
        tags=request.tags
    )
    return db.update_knowledge(item)

@app.delete("/api/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: str):
    if not db.delete_knowledge(knowledge_id):
        raise HTTPException(status_code=404, detail="Knowledge item not found")
    return {"status": "deleted", "id": knowledge_id}

@app.get("/api/subjects")
async def list_subjects():
    subject_info = {
        Subject.CHINESE: {"name": "语文", "icon": "📖", "color": "#ef4444"},
        Subject.MATH: {"name": "数学", "icon": "📐", "color": "#3b82f6"},
        Subject.ENGLISH: {"name": "英语", "icon": "🌍", "color": "#22c55e"},
        Subject.HISTORY: {"name": "历史", "icon": "🏛️", "color": "#f59e0b"},
        Subject.POLITICS: {"name": "政治", "icon": "⚖️", "color": "#8b5cf6"}
    }

    result = []
    for subj, info in subject_info.items():
        stats = db.get_stats()["subject_stats"].get(subj.value, {})
        result.append({
            "id": subj.value,
            "name": info["name"],
            "icon": info["icon"],
            "color": info["color"],
            "question_count": stats.get("questions", 0),
            "knowledge_count": stats.get("knowledge", 0)
        })

    return result

@app.get("/api/subjects/{subject}/topics")
async def list_topics(subject: Subject):
    return db.get_topics_by_subject(subject)

@app.get("/api/admin/stats", response_model=DashboardStats)
async def get_stats():
    stats = db.get_stats()
    return DashboardStats(**stats)

@app.get("/api/admin/logs", response_model=List[SystemLog])
async def get_logs(limit: int = 20):
    return db.get_recent_logs(limit)

def start_server():
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              {SYSTEM_NAME}                                   ║
║                     {SYSTEM_VERSION}                         ║
║                                                              ║
║   后端服务启动中...                                             ║
║   API 文档: http://{BACKEND_HOST}:{BACKEND_PORT}/docs         ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    uvicorn.run(app, host=BACKEND_HOST, port=BACKEND_PORT)

if __name__ == "__main__":
    start_server()
