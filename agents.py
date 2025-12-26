"""
AI 智能学习操作系统 - AI Agent 模块
LangChain-based agents for teaching, assessment, and learning orchestration
"""

from typing import Dict, List, Any, Tuple, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json
import re

from config import API_KEY, API_BASE_URL, MODEL_NAME
from models import (
    Subject, Question, KnowledgeItem, Session,
    GradeLevel, SessionState, QuestionType
)
from database import db

class BaseAgent:
    """基础 Agent 类"""

    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=API_KEY,
            base_url=API_BASE_URL,
            model=MODEL_NAME,
            temperature=0.7,
            max_tokens=2000
        )

    def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        """调用 LLM"""
        try:
            langchain_messages = []
            for msg in messages:
                role = msg.get("role")
                content = msg.get("content", "")
                if role == "system":
                    langchain_messages.append(SystemMessage(content=content))
                elif role == "user":
                    langchain_messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    langchain_messages.append(AIMessage(content=content))

            response = self.llm.invoke(langchain_messages)
            db.increment_interactions()
            return response.content
        except Exception as e:
            return f"AI 服务暂时不可用，请检查配置。错误信息：{str(e)}"


class TeachingAgent(BaseAgent):
    """教学 Agent - 负责启发式教学"""

    SUBJECT_NAMES = {
        Subject.CHINESE: "语文",
        Subject.MATH: "数学",
        Subject.ENGLISH: "英语",
        Subject.HISTORY: "历史",
        Subject.POLITICS: "政治"
    }

    def get_system_prompt(self, subject: Subject, knowledge: List[KnowledgeItem], student_level: GradeLevel = GradeLevel.C) -> str:
        """生成系统提示词，考虑学生水平"""
        subject_name = self.SUBJECT_NAMES.get(subject, getattr(subject, "value", str(subject)))
        
        # 结构化知识库，增加层级关系
        knowledge_text = "## 知识点体系\n"
        topics = {}
        
        # 按主题分组知识点
        for k in knowledge:
            topic = getattr(k, "topic_name", "其他")
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(k)
        
        for topic, items in topics.items():
            knowledge_text += f"### {topic}\n"
            for k in items:
                knowledge_text += f"""
    - **概念**：{k.title}
    - **核心内容**：{k.content}
    - **关键要点**：{', '.join(k.key_points)}
    - **常见误区**：{', '.join(k.common_mistakes)}
"""
        
        # 根据学生水平调整教学策略
        level_adjustments = {
            GradeLevel.C: "从最基础的概念开始讲解，使用最简单的语言和大量例子",
            GradeLevel.B: "可以使用中等难度的讲解，适当引入一些拓展内容",
            GradeLevel.A: "可以深入讲解概念的本质和应用，挑战学生的思维"
        }
        
        return f"""你是一位专业的{subject_name}学科 AI 导师，具有丰富的教学经验。

## 你的教学风格
1. 采用苏格拉底式提问法，通过连续的引导性问题帮助学生自主思考
2. 善于用生动的比喻和贴近生活的实例解释抽象概念
3. 根据学生的理解程度灵活调整教学策略：{level_adjustments.get(student_level, "根据学生反应灵活调整")}
4. 鼓励学生提问，营造积极的学习氛围
5. 对学生的回答给予具体、建设性的反馈

## 当前学科知识库
{knowledge_text}

## 教学原则
1. 先评估学生的基础，再开始针对性教学
2. 从简单到复杂，循序渐进，建立清晰的知识脉络
3. 多用"你觉得呢？""为什么会这样？""如果...会发生什么？"等引导性问题
4. 及时发现并纠正学生的误区，提供具体的改进建议
5. 知识点讲解完毕后，主动提出进行练习以巩固所学

## 响应规则
1. **练习请求**（包含"开始练习"或类似词语）：
   - 输出两道与当前学习内容相关的练习题
   - 考虑学生水平，调整题目难度
   - 格式：
     【今日练习】
     题目1: [描述]（难度：⭐⭐）
     题目2: [描述]（难度：⭐⭐⭐）

2. **提示请求**（包含"给我提示"或类似词语）：
   - 输出三个层次的提示，逐步引导
   - 提示1：激活已有知识
   - 提示2：提供方法指导
   - 提示3：检查关键点
   - 格式：
     【解题提示】
     提示1（知识激活）: 回忆一下...相关的概念
     提示2（方法指导）: 可以尝试使用...方法来解决
     提示3（检查要点）: 注意...关键点，避免...常见错误

3. **总结请求**（包含"知识总结"或类似词语）：
   - 输出结构化总结，建立知识体系
   - 格式：
     【章节总结】
     📖 **核心概念**: [关键概念列表]
     🧠 **重点理解**: [需要深入理解的内容]
     🔗 **知识联系**: [与其他知识点的关联]
     🎯 **应用场景**: [实际应用举例]

4. **普通问题**：
   - 直接回答问题，保持简洁明了
   - 适当引入相关知识点，拓展学生思维

## 输出要求
- 使用与学生水平相适应的语言
- 适当使用 emoji 增加亲和力
- 每次回复聚焦一个核心知识点
- 在合适的时机引入练习题或拓展问题
- 回应学生的时候不要展示思考过程，请直接发送要回应的内容"""

    def teach(self, session: Session, user_message: str, knowledge: List[KnowledgeItem]) -> str:
        """进行教学"""
        system_prompt = self.get_system_prompt(session.subject, knowledge, session.current_grade)

        messages = [{"role": "system", "content": system_prompt}]

        # 添加历史消息：保留最近10条
        for msg in session.messages[-10:]:
            # 只允许三种 role，避免脏数据
            if msg.get("role") in ("system", "user", "assistant"):
                messages.append({"role": msg["role"], "content": msg.get("content", "")})

        messages.append({"role": "user", "content": user_message})

        return self._call_llm(messages)

    def generate_remediation(self, session: Session, topic: str, failures: int, error_type: Optional[str] = None) -> str:
        """生成个性化补救教学内容，基于错误类型和学生水平"""
        knowledge = db.get_knowledge_by_subject(session.subject)
        
        # 获取学生最近的答题历史，用于分析常见错误
        recent_messages = session.messages[-10:]  # 获取最近10条消息
        answer_history = []
        for i in range(len(recent_messages) - 1, -1, -2):  # 倒序查找，每两条消息为一组（用户问+系统答）
            if recent_messages[i].get("role") == "assistant" and "错误类型" in recent_messages[i].get("content", ""):
                if i > 0 and recent_messages[i-1].get("role") == "user":
                    answer_history.append({
                        "question": recent_messages[i-1].get("content", ""),
                        "feedback": recent_messages[i].get("content", "")
                    })
            if len(answer_history) >= 3:  # 最多获取3条最近的答题历史
                break
        
        # 构建错误历史上下文
        error_history_text = ""
        if answer_history:
            error_history_text = "## 学生最近错误历史\n"
            for i, record in enumerate(answer_history, 1):
                error_history_text += f"### 错误 {i}\n"
                error_history_text += f"- 问题：{record['question'][:50]}...\n"
                error_history_text += f"- 反馈：{record['feedback'].split('\n')[0]}\n"
        
        # 定义错误类型对应的教学策略
        error_strategies = {
            "conceptual": "重点解释核心概念，使用直观的比喻和图形化描述",
            "procedural": "分解解题步骤，展示详细的操作流程",
            "factual": "提供记忆技巧，使用联想和重复练习",
            "logical": "培养逻辑思维，使用思维导图和推理训练",
            "misinterpretation": "加强题目理解训练，提升审题能力"
        }
        
        # 根据学生水平调整补救难度
        level_adjustments = {
            GradeLevel.C: "从最基础的概念重新开始，使用最简单的语言和大量生活实例",
            GradeLevel.B: "强化薄弱环节，提供中等难度的练习和指导",
            GradeLevel.A: "挑战思维深度，提供拓展性问题和综合应用训练"
        }
        
        prompt = f"""学生在学习"{topic}"时已经连续失败{failures}次，请生成个性化补救教学内容：

## 学生信息
- 当前水平：{session.current_grade.name}（{session.current_grade.value}）
- 错误类型：{error_type if error_type else '综合型错误'}
{error_history_text if error_history_text else ''}

## 教学策略要求
1. {level_adjustments.get(session.current_grade, '根据学生水平调整难度')}
2. {error_strategies.get(error_type, '采用多样化教学方法')}
3. 重新解释核心概念，避免使用复杂术语
4. 提供3-5个递进式的小步骤练习
5. 给予积极的鼓励和具体的改进建议

## 输出格式
### 🔄 补救学习计划
- **问题诊断**：分析学生的主要问题
- **重新讲解**：用新的方式解释核心概念
- **递进练习**：分步骤的小练习
- **改进建议**：具体的学习方法建议

请生成符合以上要求的补救教学内容："""

        messages = [
            {"role": "system", "content": self.get_system_prompt(session.subject, knowledge, session.current_grade)},
            {"role": "user", "content": prompt}
        ]

        return self._call_llm(messages)

    def generate_hints_for_question(self, session: Session, question: Question, knowledge: List[KnowledgeItem]) -> str:
        """为特定题目生成分层提示，考虑学生水平"""
        options_text = ""
        if getattr(question, "options", None):
            options_text = "\n".join([str(o) for o in question.options])
        
        # 获取相关知识点
        related_knowledge = []
        for k in knowledge:
            if any(keyword in question.content for keyword in k.key_points):
                related_knowledge.append(k)
        
        knowledge_context = ""
        if related_knowledge:
            knowledge_context = "相关知识点：\n" + "\n".join([f"- {k.title}: {', '.join(k.key_points[:2])}" for k in related_knowledge])
        
        prompt = f"""给我提示。

你正在辅导学生解题。学生希望获得提示，但你不能直接给出最终答案或选项字母。

## 题目信息
- 类型：{question.question_type}
- 题目：{question.content}
{"选项：" + options_text if options_text else ""}
{knowledge_context if knowledge_context else ""}

## 学生水平
当前学生水平：{session.current_grade.name}（{session.current_grade.value}）

## 提示要求
- 输出三个层次的提示，逐步引导学生思考
- 提示1：激活学生已有的相关知识
- 提示2：提供具体的解题方法或思路
- 提示3：指出容易出错的关键点或检查方法
- 严格使用格式：

【解题提示】
提示1（知识激活）: ...
提示2（方法指导）: ...
提示3（检查要点）: ...
"""
        messages = [
            {"role": "system", "content": self.get_system_prompt(session.subject, knowledge, session.current_grade)},
            {"role": "user", "content": prompt}
        ]
        return self._call_llm(messages)


class AssessmentAgent(BaseAgent):
    """评估 Agent - 负责学生回答的深度评估"""

    def evaluate_answer(
        self,
        question: Question,
        student_answer: str,
        session: Session
    ) -> Tuple[bool, GradeLevel, str, Optional[str]]:
        """评估学生回答，增加错误类型分析"""

        # 增加错误类型分类
        error_types = {
            "conceptual": "概念理解错误",
            "procedural": "解题步骤错误",
            "factual": "事实记忆错误",
            "logical": "逻辑推理错误",
            "misinterpretation": "题目理解错误"
        }

        prompt = f"""请评估学生对以下问题的回答：

## 问题信息
- 类型：{question.question_type}
- 题目：{question.content}
- 正确答案：{question.correct_answer}
- 解析：{question.explanation}
{"- 选项：" + str(question.options) if question.options else ""}

## 学生回答
{student_answer}

## 评估要求
请从以下几个维度评估并给出等级：
1. 答案正确性
2. 理解深度
3. 表达清晰度
4. 思维过程完整性

## 输出格式（请严格按照此格式输出JSON）
{{
    "is_correct": true/false,
    "grade": "A/B/C",
    "feedback": "对学生的反馈",
    "explanation": "详细解释为什么这样评分",
    "error_type": "{list(error_types.keys())[0]}/null",
    "error_description": "错误类型描述/null",
    "improvement_suggestion": "具体的改进建议"
}}

等级标准：
- A级：完全正确，理解深刻，表达清晰
- B级：基本正确，但有小错误或理解不够深入
- C级：理解有误，需要重新学习"""

        messages = [
            {"role": "system", "content": "你是一位严谨但友善的评估专家，擅长分析学生的学习情况。请用JSON格式输出评估结果，确保包含所有要求的字段。"},
            {"role": "user", "content": prompt}
        ]

        response = self._call_llm(messages)

        # 增强JSON解析的鲁棒性
        try:
            # 提取JSON部分
            import json
            import re
            
            # 尝试匹配JSON对象
            json_pattern = r'\{[\s\S]*?\}'
            matches = re.findall(json_pattern, response)
            
            for match in matches:
                try:
                    result = json.loads(match)
                    # 验证必要字段
                    if all(key in result for key in ["is_correct", "grade", "feedback"]):
                        is_correct = bool(result.get("is_correct", False))
                        grade_str = str(result.get("grade", "C")).strip().upper()
                        grade = GradeLevel(grade_str) if grade_str in ["A", "B", "C"] else GradeLevel.C
                        feedback = str(result.get("feedback", "评估完成"))
                        error_type = result.get("error_type")  # 提取错误类型键
                        
                        # 增强反馈内容
                        if not is_correct:
                            error_desc = result.get("error_description")
                            improvement = result.get("improvement_suggestion")
                            
                            if error_type and error_desc:
                                feedback += f"\n\n📌 错误类型：{error_desc}"
                            if improvement:
                                feedback += f"\n\n💡 改进建议：{improvement}"
                        
                        return is_correct, grade, feedback, error_type
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            print(f"JSON解析错误: {e}")

        # JSON解析失败则简化评估
        is_correct = self._simple_check(question, student_answer)
        grade = GradeLevel.A if is_correct else GradeLevel.C
        return is_correct, grade, response, None

    def _simple_check(self, question: Question, answer: str) -> bool:
        """简单答案检查"""
        correct = str(question.correct_answer).lower().strip()
        student = str(answer).lower().strip()

        if question.question_type == QuestionType.CHOICE:
            return correct in student or student in correct

        if question.question_type == QuestionType.JUDGMENT:
            correct_keywords = ["正确", "对", "true", "yes", "√"]
            wrong_keywords = ["错误", "错", "false", "no", "×"]
            if correct in correct_keywords:
                return any(k in student for k in correct_keywords)
            return any(k in student for k in wrong_keywords)

        # 问答/填空：关键词命中率
        keywords = [k for k in correct.split() if k]
        if not keywords:
            return False
        matches = sum(1 for k in keywords if k in student)
        return matches >= len(keywords) * 0.5

    def generate_feedback(self, question: Question, is_correct: bool, grade: GradeLevel) -> str:
        """生成反馈"""
        if is_correct:
            if grade == GradeLevel.A:
                return f"🎉 太棒了！你完全理解了这个知识点！\n\n📝 解析：{question.explanation}"
            return f"✅ 答对了！但还可以理解得更深入。\n\n📝 解析：{question.explanation}"
        return f"❌ 这道题做错了，没关系，让我们一起分析一下。\n\n✨ 正确答案：{question.correct_answer}\n📝 解析：{question.explanation}"


class LearningAgent(BaseAgent):
    """学习 Agent - 核心调度，协调教学和评估"""

    def __init__(self):
        super().__init__()
        self.teaching_agent = TeachingAgent()
        self.assessment_agent = AssessmentAgent()

        # 关键修复：缓存“当前题目”，避免评估阶段拿错题
        # 不依赖 Session 模型增加字段
        self._current_question_by_session: Dict[str, Question] = {}

    def get_welcome_message(self, subject: Subject) -> str:
        """获取欢迎消息"""
        subject_names = {
            Subject.CHINESE: "语文",
            Subject.MATH: "数学",
            Subject.ENGLISH: "英语",
            Subject.HISTORY: "历史",
            Subject.POLITICS: "政治"
        }
        subject_name = subject_names.get(subject, getattr(subject, "value", str(subject)))

        topics = db.get_topics_by_subject(subject)
        topic_list = "\n".join([f"  • {t.get('name')}" for t in topics])

        return f"""👋 欢迎来到 {subject_name} 学习空间！

我是你的 AI 学习导师，将陪伴你一起学习和进步。

📚 当前可学习的主题：
{topic_list}

💡 你可以：
1. 直接告诉我你想学习什么
2. 问我任何关于 {subject_name} 的问题
3. 让我给你出题练习

准备好了吗？让我们开始学习之旅！🚀"""

    def process_message(self, session: Session, user_message: str) -> Dict[str, Any]:
        """处理用户消息 - 核心调度逻辑"""

        result: Dict[str, Any] = {
            "response": "",
            "state": session.state,
            "grade": session.current_grade,
            "is_question": False,
            "question": None,
            "mastered": False
        }

        knowledge = db.get_knowledge_by_subject(session.subject)

        # 记录用户消息
        session.messages.append({"role": "user", "content": user_message})

        # 状态机调度
        if session.state == SessionState.LEARNING:
            result = self._handle_learning(session, user_message, knowledge)
        elif session.state == SessionState.ASSESSING:
            result = self._handle_assessment(session, user_message, knowledge)
        elif session.state == SessionState.TRANSFER_TEST:
            result = self._handle_transfer_test(session, user_message, knowledge)
        elif session.state == SessionState.REMEDIATION:
            result = self._handle_remediation(session, user_message, knowledge)

        # 记录助手回复
        session.messages.append({"role": "assistant", "content": result["response"]})

        # 更新会话
        session.state = result["state"]
        session.current_grade = result["grade"]

        # db 持久化如果失败，不让它把 /api/chat 直接打成 500（真实错误建议在 FastAPI 层打印）
        try:
            db.update_session(session)
        except Exception:
            # 这里吞掉异常，让接口仍能返回（避免用户看到“提示=500”）
            pass

        return result

    def _wants_practice(self, message: str) -> bool:
        keywords = ["练习", "做题", "测试", "出题", "考考我", "quiz", "test", "practice"]
        m = (message or "").lower()
        return any(k in m for k in keywords)

    def _wants_hint(self, message: str) -> bool:
        # 在答题态/迁移测试态识别“提示”，不要当作答案去评估
        m = (message or "").lower()
        keywords = ["给我提示", "提示", "hint", "给点提示", "来点提示", "不会", "思路", "怎么做"]
        return any(k in m for k in keywords)

    def _handle_learning(
        self,
        session: Session,
        user_message: str,
        knowledge: List[KnowledgeItem]
    ) -> Dict[str, Any]:
        """处理学习状态"""

        if self._wants_practice(user_message):
            return self._start_assessment(session)

        # 关键修复：topic id 匹配时强转为 str，避免 `int in str` TypeError 引发 500
        topics = db.get_topics_by_subject(session.subject)
        msg = user_message or ""
        for topic in topics:
            topic_name = str(topic.get("name", ""))
            topic_id = str(topic.get("id", ""))  # 强转
            if (topic_name and topic_name in msg) or (topic_id and topic_id in msg):
                session.topic_id = topic.get("id")
                break

        response = self.teaching_agent.teach(session, user_message, knowledge)

        return {
            "response": response,
            "state": SessionState.LEARNING,
            "grade": session.current_grade,
            "is_question": False,
            "question": None,
            "mastered": False
        }

    def _remember_current_question(self, session: Session, question: Question) -> None:
        sid = getattr(session, "id", None)
        if sid:
            self._current_question_by_session[sid] = question

    def _get_current_question(self, session: Session, want_transfer: Optional[bool] = None) -> Optional[Question]:
        sid = getattr(session, "id", None)
        if not sid:
            return None
        q = self._current_question_by_session.get(sid)
        if not q:
            return None
        if want_transfer is None:
            return q
        if bool(getattr(q, "is_transfer", False)) == bool(want_transfer):
            return q
        return None

    def _start_assessment(self, session: Session) -> Dict[str, Any]:
        """开始评估"""

        if session.topic_id:
            questions = db.get_questions_by_topic(session.subject, session.topic_id)
        else:
            questions = db.get_questions_by_subject(session.subject)

        # 过滤掉迁移测试题
        questions = [q for q in questions if not getattr(q, "is_transfer", False)]

        if not questions:
            return {
                "response": "📚 当前主题暂无练习题，让我们继续学习吧！",
                "state": SessionState.LEARNING,
                "grade": session.current_grade,
                "is_question": False,
                "question": None,
                "mastered": False
            }

        import random
        question = random.choice(questions)
        self._remember_current_question(session, question)

        question_text = self._format_question(question)

        return {
            "response": f"📝 好的，让我们来做一道练习题！\n\n{question_text}\n\n请输入你的答案（需要提示就说“给我提示”）：",
            "state": SessionState.ASSESSING,
            "grade": session.current_grade,
            "is_question": True,
            "question": question,
            "mastered": False
        }

    def _format_question(self, question: Question) -> str:
        type_names = {
            QuestionType.CHOICE: "选择题",
            QuestionType.JUDGMENT: "判断题",
            QuestionType.QA: "问答题",
            QuestionType.FILL: "填空题",
            QuestionType.APPLICATION: "应用题"
        }

        difficulty = getattr(question, "difficulty", 1) or 1
        text = f"【{type_names.get(question.question_type, '题目')}】难度：{'⭐' * int(difficulty)}\n\n"
        text += f"{question.content}\n"

        if getattr(question, "options", None):
            text += "\n"
            for opt in question.options:
                text += f"{opt}\n"

        return text

    def _handle_assessment(
        self,
        session: Session,
        user_message: str,
        knowledge: List[KnowledgeItem]
    ) -> Dict[str, Any]:
        """处理评估状态"""

        # 关键修复：拿到“刚刚出的那道题”，而不是题库第一题
        question = self._get_current_question(session, want_transfer=False)

        if not question:
            return {
                "response": "未找到当前题目，我们重新开始一题练习吧。回复“出题/练习”即可。",
                "state": SessionState.LEARNING,
                "grade": session.current_grade,
                "is_question": False,
                "question": None,
                "mastered": False
            }

        # 关键修复：答题态支持“给我提示”，不要当作答案评估
        if self._wants_hint(user_message):
            hints = self.teaching_agent.generate_hints_for_question(session, question, knowledge)
            return {
                "response": f"{hints}\n\n你可以继续作答：",
                "state": SessionState.ASSESSING,
                "grade": session.current_grade,
                "is_question": True,
                "question": question,
                "mastered": False
            }

        is_correct, grade, feedback, error_type = self.assessment_agent.evaluate_answer(question, user_message, session)
        session.current_grade = grade

        if is_correct:
            session.consecutive_failures = 0
            if grade == GradeLevel.A:
                return self._start_transfer_test(session, feedback)
            return {
                "response": f"{feedback}\n\n继续努力！你想继续学习还是做更多练习？",
                "state": SessionState.LEARNING,
                "grade": grade,
                "is_question": False,
                "question": None,
                "mastered": False
            }

        # 答错
        session.consecutive_failures += 1

        if session.consecutive_failures >= 3:
            remediation = self.teaching_agent.generate_remediation(
                session,
                getattr(question, "topic_name", "当前主题"),
                session.consecutive_failures,
                error_type
            )
            return {
                "response": f"{feedback}\n\n---\n\n🔄 让我换一种方式来帮助你理解：\n\n{remediation}",
                "state": SessionState.REMEDIATION,
                "grade": GradeLevel.C,
                "is_question": False,
                "question": None,
                "mastered": False
            }

        # 仍然留在答题态，方便“给我提示/继续作答”
        return {
            "response": f"{feedback}\n\n别灰心！你可以继续作答，或者说“给我提示”。",
            "state": SessionState.ASSESSING,
            "grade": grade,
            "is_question": True,
            "question": question,
            "mastered": False
        }

    def _start_transfer_test(self, session: Session, prev_feedback: str) -> Dict[str, Any]:
        """开始迁移测试"""

        if session.topic_id:
            transfer_questions = db.get_transfer_questions(session.subject, session.topic_id)
        else:
            transfer_questions = [q for q in db.get_questions_by_subject(session.subject) if getattr(q, "is_transfer", False)]

        if not transfer_questions:
            return {
                "response": f"{prev_feedback}\n\n🎊 太棒了！你已经掌握了这个知识点！\n\n想要学习其他内容吗？",
                "state": SessionState.MASTERED,
                "grade": GradeLevel.A,
                "is_question": False,
                "question": None,
                "mastered": True
            }

        import random
        question = random.choice(transfer_questions)
        self._remember_current_question(session, question)

        question_text = self._format_question(question)

        return {
            "response": f"{prev_feedback}\n\n---\n\n🚀 **迁移测试**\n\n你对基础知识掌握得很好！现在挑战一道应用题，看看你能否举一反三：\n\n{question_text}\n\n请认真思考后作答（需要提示就说“给我提示”）：",
            "state": SessionState.TRANSFER_TEST,
            "grade": GradeLevel.A,
            "is_question": True,
            "question": question,
            "mastered": False
        }

    def _handle_transfer_test(
        self,
        session: Session,
        user_message: str,
        knowledge: List[KnowledgeItem]
    ) -> Dict[str, Any]:
        """处理迁移测试"""

        question = self._get_current_question(session, want_transfer=True)
        if not question:
            return {
                "response": "未找到迁移测试题目，我们先回到学习吧。",
                "state": SessionState.LEARNING,
                "grade": session.current_grade,
                "is_question": False,
                "question": None,
                "mastered": False
            }

        if self._wants_hint(user_message):
            hints = self.teaching_agent.generate_hints_for_question(session, question, knowledge)
            return {
                "response": f"{hints}\n\n你可以继续作答：",
                "state": SessionState.TRANSFER_TEST,
                "grade": session.current_grade,
                "is_question": True,
                "question": question,
                "mastered": False
            }

        is_correct, grade, feedback = self.assessment_agent.evaluate_answer(question, user_message, session)

        if is_correct or grade in [GradeLevel.A, GradeLevel.B]:
            return {
                "response": f"🎊 **恭喜！迁移测试通过！**\n\n{feedback}\n\n✅ 你已经真正掌握了这个知识点！\n\n想继续学习其他内容吗？",
                "state": SessionState.MASTERED,
                "grade": GradeLevel.A,
                "is_question": False,
                "question": None,
                "mastered": True
            }

        return {
            "response": f"{feedback}\n\n迁移测试未通过，没关系！我们回顾一下基础知识再挑战。\n\n你想我从哪部分开始讲？",
            "state": SessionState.LEARNING,
            "grade": GradeLevel.B,
            "is_question": False,
            "question": None,
            "mastered": False
        }

    def _handle_remediation(
        self,
        session: Session,
        user_message: str,
        knowledge: List[KnowledgeItem]
    ) -> Dict[str, Any]:
        """处理补救教学"""

        session.consecutive_failures = 0
        response = self.teaching_agent.teach(session, user_message, knowledge)

        return {
            "response": response,
            "state": SessionState.LEARNING,
            "grade": GradeLevel.C,
            "is_question": False,
            "question": None,
            "mastered": False
        }


# 创建全局 Agent 实例
learning_agent = LearningAgent()
teaching_agent = TeachingAgent()
assessment_agent = AssessmentAgent()
