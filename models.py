# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 数据模型
Pydantic models for data validation and serialization
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from enum import Enum
import uuid

# 枚举类型
class Subject(str, Enum):
    """学科枚举"""
    CHINESE = "chinese"      # 语文
    MATH = "math"            # 数学
    ENGLISH = "english"      # 英语
    HISTORY = "history"      # 历史
    POLITICS = "politics"    # 政治

class QuestionType(str, Enum):
    """题目类型"""
    CHOICE = "choice"        # 选择题
    JUDGMENT = "judgment"    # 判断题
    QA = "qa"                # 问答题
    FILL = "fill"            # 填空题
    APPLICATION = "application"  # 应用题（迁移测试）

class GradeLevel(str, Enum):
    """理解等级"""
    A = "A"  # 深度理解，可进行迁移测试
    B = "B"  # 基本理解，需要更多练习
    C = "C"  # 理解不足，需要重新学习

class SessionState(str, Enum):
    """会话状态"""
    LEARNING = "learning"           # 学习中
    ASSESSING = "assessing"         # 评估中
    TRANSFER_TEST = "transfer_test" # 迁移测试
    MASTERED = "mastered"           # 已掌握
    REMEDIATION = "remediation"     # 补救教学

# 基础模型
class Question(BaseModel):
    """题目模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: Subject
    topic_id: str
    topic_name: str
    question_type: QuestionType
    difficulty: int = Field(ge=1, le=5, description="难度1-5")
    content: str
    options: Optional[List[str]] = None  # 选择题选项
    correct_answer: str
    explanation: str
    is_transfer: bool = False  # 是否为迁移测试题
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class KnowledgeItem(BaseModel):
    """知识点模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    subject: Subject
    topic_id: str
    topic_name: str
    title: str
    content: str
    key_points: List[str] = []
    common_mistakes: List[str] = []  # 常见误区
    intuition_pumps: List[str] = []  # 直觉泵/提示
    source_type: Literal["text", "pdf", "link"] = "text"
    source_url: Optional[str] = None
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class StudentProgress(BaseModel):
    """学生进度模型"""
    student_id: str
    subject: Subject
    topic_id: str
    current_grade: GradeLevel = GradeLevel.C
    attempt_count: int = 0
    correct_count: int = 0
    mastered: bool = False
    transfer_passed: bool = False
    last_activity: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

class Session(BaseModel):
    """学习会话模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str
    subject: Subject
    topic_id: Optional[str] = None
    state: SessionState = SessionState.LEARNING
    current_grade: GradeLevel = GradeLevel.C
    consecutive_failures: int = 0
    messages: List[Dict[str, str]] = []
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    class Config:
        use_enum_values = True

# API 请求/响应模型
class ChatRequest(BaseModel):
    """聊天请求"""
    session_id: str
    message: str
    student_id: str = "default_student"

class ChatResponse(BaseModel):
    """聊天响应"""
    session_id: str
    response: str
    state: SessionState
    grade: Optional[GradeLevel] = None
    is_question: bool = False
    question: Optional[Question] = None
    mastered: bool = False

class CreateSessionRequest(BaseModel):
    """创建会话请求"""
    student_id: str = "default_student"
    subject: Subject

class CreateSessionResponse(BaseModel):
    """创建会话响应"""
    session_id: str
    subject: Subject
    welcome_message: str

class QuestionCreateRequest(BaseModel):
    """创建题目请求"""
    subject: Subject
    topic_id: str
    topic_name: str
    question_type: QuestionType
    difficulty: int = Field(ge=1, le=5)
    content: str
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    is_transfer: bool = False

class KnowledgeCreateRequest(BaseModel):
    """创建知识点请求"""
    subject: Subject
    topic_id: str
    topic_name: str
    title: str
    content: str
    key_points: List[str] = []
    common_mistakes: List[str] = []
    intuition_pumps: List[str] = []
    source_type: Literal["text", "pdf", "link"] = "text"
    source_url: Optional[str] = None
    tags: List[str] = []

class DashboardStats(BaseModel):
    """管理端数据统计"""
    active_students: int
    knowledge_count: int
    question_count: int
    ai_interactions: int
    average_mastery: float
    subject_stats: Dict[str, Dict[str, Any]]

class SystemLog(BaseModel):
    """系统日志"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.now)
    log_type: Literal["info", "warning", "error", "success"]
    message: str
    details: Optional[Dict[str, Any]] = None

class AnswerSubmission(BaseModel):
    """答案提交"""
    session_id: str
    question_id: str
    answer: str
    student_id: str = "default_student"

class AnswerResult(BaseModel):
    """答案评估结果"""
    is_correct: bool
    grade: GradeLevel
    feedback: str
    explanation: str
    next_action: str
    mastered: bool = False