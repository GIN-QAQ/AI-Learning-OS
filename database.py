# -*- coding: utf-8 -*-
"""
AI 智能学习操作系统 - 数据库模块
In-memory database with preset content
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from models import (
    Question, KnowledgeItem, Session, StudentProgress,
    Subject, QuestionType, GradeLevel, SessionState, SystemLog
)
import uuid

class Database:
    """内存数据库"""

    def __init__(self):
        self.questions: Dict[str, Question] = {}
        self.knowledge: Dict[str, KnowledgeItem] = {}
        self.sessions: Dict[str, Session] = {}
        self.progress: Dict[str, StudentProgress] = {}
        self.logs: List[SystemLog] = []
        self.ai_interactions: int = 0
        
        # 初始化预置数据
        self._init_preset_data()
    
    def _init_preset_data(self):
        """初始化预置的知识点和题目"""

        # 语文 (Chinese)

        # 知识点
        self._add_knowledge(KnowledgeItem(
            subject=Subject.CHINESE,
            topic_id="ch_rhetoric",
            topic_name="修辞手法",
            title="常见修辞手法详解",
            content="""修辞手法是语言表达的艺术技巧，常见的包括：
                        1. 比喻：用相似事物打比方，如"月亮像一个银盘"
                        2. 拟人：把事物人格化，如"春风轻轻抚摸大地"
                        3. 夸张：故意夸大或缩小，如"飞流直下三千尺"
                        4. 排比：结构相同的句子并列，增强气势
                        5. 对偶：字数相等、结构相同的两句对称""",
            key_points=["比喻需要有本体和喻体", "拟人赋予事物人的特征", "夸张要合理不失真"],
            common_mistakes=["混淆比喻和拟人", "把所有形容词都当作夸张"],
            intuition_pumps=["想想事物像什么？是比喻；想想事物会做什么人的动作？是拟人"]
        ))
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.CHINESE,
            topic_id="ch_poetry",
            topic_name="古诗鉴赏",
            title="唐诗宋词鉴赏方法",
            content="""古诗鉴赏的基本步骤：
                        1. 了解作者背景和创作时代
                        2. 理解诗词的字面意思
                        3. 分析意象和意境
                        4. 体会情感和主题
                        5. 欣赏艺术手法和语言特色
                        
                        常见意象含义：月亮-思乡、柳-离别、梅花-高洁、菊花-隐逸""",
            key_points=["意象是寄托情感的具体事物", "意境是整体氛围", "要结合时代背景理解"],
            common_mistakes=["只看字面意思忽略深层含义", "不了解作者导致误解诗意"],
            intuition_pumps=["作者想表达什么情感？用了什么景物来表达？"]
        ))
        
        # 题目
        self._add_question(Question(
            subject=Subject.CHINESE,
            topic_id="ch_rhetoric",
            topic_name="修辞手法",
            question_type=QuestionType.CHOICE,
            difficulty=2,
            content="下列句子使用了什么修辞手法？'春风又绿江南岸'",
            options=["A. 比喻", "B. 拟人", "C. 夸张", "D. 排比"],
            correct_answer="B",
            explanation="'绿'字使春风具有了人的动作（使...变绿），这是拟人手法"
        ))
        
        self._add_question(Question(
            subject=Subject.CHINESE,
            topic_id="ch_rhetoric",
            topic_name="修辞手法",
            question_type=QuestionType.JUDGMENT,
            difficulty=1,
            content="'他的心像一块石头一样硬'这句话使用了拟人手法。",
            correct_answer="错误",
            explanation="这是比喻手法，用石头来比喻心硬，有本体（心）和喻体（石头）"
        ))
        
        self._add_question(Question(
            subject=Subject.CHINESE,
            topic_id="ch_rhetoric",
            topic_name="修辞手法",
            question_type=QuestionType.APPLICATION,
            difficulty=4,
            content="请用比喻和拟人两种修辞手法，分别写一句描写'月光'的句子，并说明为什么这样写能更好地表达情感。",
            correct_answer="开放性答案",
            explanation="比喻示例：月光如水银泻地。拟人示例：月光温柔地亲吻大地。",
            is_transfer=True
        ))
        
        self._add_question(Question(
            subject=Subject.CHINESE,
            topic_id="ch_poetry",
            topic_name="古诗鉴赏",
            question_type=QuestionType.QA,
            difficulty=3,
            content="请分析李白《静夜思》中'床前明月光，疑是地上霜'的意境和情感。",
            correct_answer="诗人用月光如霜的意象，营造清冷孤寂的意境，表达思乡之情",
            explanation="月光本身就是思乡意象，'霜'字增添凄凉感，表达游子思乡"
        ))
        
        # ============================================
        # 数学 (Math)
        # ============================================
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.MATH,
            topic_id="math_quadratic",
            topic_name="一元二次方程",
            title="一元二次方程的解法",
            content="""一元二次方程 ax² + bx + c = 0 (a≠0) 的解法：
                        1. 因式分解法：将方程因式分解为 (x-x₁)(x-x₂)=0
                        2. 配方法：将方程配成完全平方形式
                        3. 公式法：x = (-b ± √(b²-4ac)) / 2a
                        4. 判别式 Δ = b²-4ac：Δ>0 两个不等实根；Δ=0 两个相等实根；Δ<0 无实根""",
            key_points=["公式法是万能方法", "判别式决定根的情况", "a不能为0"],
            common_mistakes=["忘记a≠0的条件", "公式中符号错误", "判别式计算错误"],
            intuition_pumps=["先看能否因式分解，不能就用公式法"]
        ))
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.MATH,
            topic_id="math_function",
            topic_name="函数基础",
            title="函数的概念与性质",
            content="""函数是一种对应关系：
                        1. 定义：对于集合A中的每个元素x，按照某种规则，在集合B中都有唯一确定的元素y与之对应
                        2. 三要素：定义域、值域、对应法则
                        3. 基本性质：单调性、奇偶性、周期性
                        4. 常见函数：一次函数、二次函数、指数函数、对数函数""",
            key_points=["一个x只能对应一个y", "定义域是自变量的取值范围", "值域是函数值的范围"],
            common_mistakes=["把一对多的关系当成函数", "忘记考虑定义域的限制"],
            intuition_pumps=["函数就像自动售货机：投入一个硬币，出来一个固定商品"]
        ))
        
        self._add_question(Question(
            subject=Subject.MATH,
            topic_id="math_quadratic",
            topic_name="一元二次方程",
            question_type=QuestionType.CHOICE,
            difficulty=2,
            content="方程 x² - 5x + 6 = 0 的解是？",
            options=["A. x=2 或 x=3", "B. x=-2 或 x=-3", "C. x=1 或 x=6", "D. x=-1 或 x=-6"],
            correct_answer="A",
            explanation="因式分解：(x-2)(x-3)=0，所以 x=2 或 x=3"
        ))
        
        self._add_question(Question(
            subject=Subject.MATH,
            topic_id="math_quadratic",
            topic_name="一元二次方程",
            question_type=QuestionType.FILL,
            difficulty=3,
            content="方程 2x² + 3x - 2 = 0 的两根之和为____，两根之积为____。",
            correct_answer="-3/2, -1",
            explanation="由韦达定理：x₁+x₂=-b/a=-3/2，x₁x₂=c/a=-2/2=-1"
        ))
        
        self._add_question(Question(
            subject=Subject.MATH,
            topic_id="math_quadratic",
            topic_name="一元二次方程",
            question_type=QuestionType.APPLICATION,
            difficulty=4,
            content="一个矩形的长比宽多3米，面积为40平方米。请建立方程并求出这个矩形的长和宽。",
            correct_answer="设宽为x，则x(x+3)=40，解得x=5，所以宽5米，长8米",
            explanation="这是一元二次方程的实际应用，需要正确建立方程模型",
            is_transfer=True
        ))
        
        self._add_question(Question(
            subject=Subject.MATH,
            topic_id="math_function",
            topic_name="函数基础",
            question_type=QuestionType.JUDGMENT,
            difficulty=2,
            content="y = x² 是一个函数，因为每个x值都对应唯一的y值。",
            correct_answer="正确",
            explanation="对于任意x，x²都有唯一确定的值，满足函数定义"
        ))

        # 英语 (English)

        self._add_knowledge(KnowledgeItem(
            subject=Subject.ENGLISH,
            topic_id="en_tense",
            topic_name="时态",
            title="英语常用时态详解",
            content="""英语时态是表示动作发生时间和状态的语法形式：
                        1. 一般现在时：表示习惯、事实 (I study English every day)
                        2. 一般过去时：表示过去发生的事 (I studied English yesterday)
                        3. 现在进行时：表示正在进行 (I am studying English now)
                        4. 现在完成时：表示过去发生对现在有影响 (I have studied English for 3 years)
                        5. 过去进行时：表示过去某时正在进行 (I was studying when you called)""",
            key_points=["时态由动词形式体现", "注意时间标志词", "完成时强调对现在的影响"],
            common_mistakes=["混淆一般过去时和现在完成时", "第三人称单数忘记加s"],
            intuition_pumps=["看时间词：yesterday用过去时，now用进行时，already用完成时"]
        ))
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.ENGLISH,
            topic_id="en_passive",
            topic_name="被动语态",
            title="被动语态的构成与用法",
            content="""被动语态表示主语是动作的承受者：
                        1. 构成：be + 过去分词
                        2. 一般现在时被动：am/is/are + done
                        3. 一般过去时被动：was/were + done
                        4. 现在完成时被动：have/has been + done
                        5. 使用场景：不知道动作执行者、强调动作承受者、科技文章""",
            key_points=["be动词随时态变化", "过去分词形式不变", "by引出动作执行者"],
            common_mistakes=["be动词和过去分词形式不匹配", "不及物动词无被动语态"],
            intuition_pumps=["主语是'被...的'就用被动语态"]
        ))
        
        self._add_question(Question(
            subject=Subject.ENGLISH,
            topic_id="en_tense",
            topic_name="时态",
            question_type=QuestionType.CHOICE,
            difficulty=2,
            content="I ____ English since I was 10 years old.",
            options=["A. learn", "B. learned", "C. have learned", "D. am learning"],
            correct_answer="C",
            explanation="'since'是现在完成时的标志词，表示从过去开始持续到现在"
        ))
        
        self._add_question(Question(
            subject=Subject.ENGLISH,
            topic_id="en_tense",
            topic_name="时态",
            question_type=QuestionType.FILL,
            difficulty=3,
            content="While I ____(read) a book, my phone ____(ring).",
            correct_answer="was reading, rang",
            explanation="while引导的从句用过去进行时，主句用一般过去时，表示过去进行中被打断"
        ))
        
        self._add_question(Question(
            subject=Subject.ENGLISH,
            topic_id="en_tense",
            topic_name="时态",
            question_type=QuestionType.APPLICATION,
            difficulty=4,
            content="请用三种不同的时态（一般现在时、现在进行时、现在完成时）分别造一个关于'学习编程'的句子，并解释每个时态的用法。",
            correct_answer="开放性答案",
            explanation="例：I learn programming every day.(习惯) I am learning Python now.(正在进行) I have learned three languages.(完成对现在有影响)",
            is_transfer=True
        ))
        
        self._add_question(Question(
            subject=Subject.ENGLISH,
            topic_id="en_passive",
            topic_name="被动语态",
            question_type=QuestionType.JUDGMENT,
            difficulty=2,
            content="The letter was wrote by Tom. 这个句子的被动语态使用正确。",
            correct_answer="错误",
            explanation="write的过去分词是written，不是wrote。正确句子：The letter was written by Tom."
        ))

        # 历史 (History)

        self._add_knowledge(KnowledgeItem(
            subject=Subject.HISTORY,
            topic_id="hist_reform",
            topic_name="改革开放",
            title="中国改革开放历程",
            content="""改革开放是1978年以来中国的基本国策：
                        1. 背景：十年文革结束，经济亟需恢复
                        2. 开始：1978年十一届三中全会
                        3. 内容：对内改革（农村家庭联产承包、城市国企改革）、对外开放（经济特区、沿海开放城市）
                        4. 意义：实现了从计划经济到市场经济的转变，极大提高了人民生活水平
                        5. 关键人物：邓小平""",
            key_points=["1978年是开始时间", "改革从农村开始", "深圳是第一个经济特区"],
            common_mistakes=["混淆改革开放与新中国成立的时间", "不理解市场经济与计划经济的区别"],
            intuition_pumps=["改革=内部调整，开放=对外交流"]
        ))
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.HISTORY,
            topic_id="hist_ancient",
            topic_name="秦朝统一",
            title="秦始皇统一六国",
            content="""秦朝是中国第一个统一的封建王朝：
                        1. 时间：公元前221年
                        2. 人物：秦始皇嬴政
                        3. 统一措施：统一文字（小篆）、统一度量衡、统一货币、修驰道
                        4. 政治制度：废分封、行郡县、设三公九卿
                        5. 历史意义：结束了春秋战国的分裂局面，建立了中央集权制度""",
            key_points=["公元前221年统一", "郡县制取代分封制", "书同文车同轨"],
            common_mistakes=["混淆秦朝与其他朝代的制度", "不理解郡县制的意义"],
            intuition_pumps=["秦始皇的'统一'包括领土统一和制度统一两层含义"]
        ))
        
        self._add_question(Question(
            subject=Subject.HISTORY,
            topic_id="hist_reform",
            topic_name="改革开放",
            question_type=QuestionType.CHOICE,
            difficulty=2,
            content="中国改革开放的开始标志是？",
            options=["A. 1949年新中国成立", "B. 1978年十一届三中全会", "C. 1992年南方谈话", "D. 2001年加入WTO"],
            correct_answer="B",
            explanation="1978年十一届三中全会作出了改革开放的伟大决策"
        ))
        
        self._add_question(Question(
            subject=Subject.HISTORY,
            topic_id="hist_reform",
            topic_name="改革开放",
            question_type=QuestionType.QA,
            difficulty=3,
            content="请简述改革开放初期农村改革的主要内容及其意义。",
            correct_answer="实行家庭联产承包责任制，调动农民积极性，解放农村生产力",
            explanation="家庭联产承包责任制打破了人民公社体制，农民有了生产自主权"
        ))
        
        self._add_question(Question(
            subject=Subject.HISTORY,
            topic_id="hist_reform",
            topic_name="改革开放",
            question_type=QuestionType.APPLICATION,
            difficulty=4,
            content="结合改革开放的历史经验，分析'解放思想'与'经济发展'之间的关系。请举例说明。",
            correct_answer="开放性答案",
            explanation="解放思想是前提，突破旧观念才能推动改革；如突破姓资姓社的争论才有市场经济",
            is_transfer=True
        ))
        
        self._add_question(Question(
            subject=Subject.HISTORY,
            topic_id="hist_ancient",
            topic_name="秦朝统一",
            question_type=QuestionType.JUDGMENT,
            difficulty=2,
            content="秦始皇统一六国后实行分封制，把土地分给功臣。",
            correct_answer="错误",
            explanation="秦始皇废除分封制，实行郡县制，由中央直接管理地方"
        ))

        # 政治 (Politics)
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.POLITICS,
            topic_id="pol_economy",
            topic_name="市场经济",
            title="社会主义市场经济体制",
            content="""社会主义市场经济是中国特色的经济体制：
                        1. 定义：在社会主义条件下发展市场经济
                        2. 特点：坚持公有制主体地位，多种所有制共同发展
                        3. 作用：市场在资源配置中起决定性作用，更好发挥政府作用
                        4. 优势：既发挥市场效率，又体现社会公平
                        5. 发展：从有计划商品经济到社会主义市场经济""",
            key_points=["市场起决定性作用", "公有制为主体", "政府要更好发挥作用"],
            common_mistakes=["认为市场经济就是资本主义", "忽视政府作用"],
            intuition_pumps=["市场是'看不见的手'，政府是'看得见的手'"]
        ))
        
        self._add_knowledge(KnowledgeItem(
            subject=Subject.POLITICS,
            topic_id="pol_citizen",
            topic_name="公民权利",
            title="公民的基本权利与义务",
            content="""我国公民享有广泛的权利，也要履行相应义务：
                        1. 政治权利：选举权和被选举权、政治自由、监督权
                        2. 人身权利：人身自由、人格尊严、住宅不受侵犯
                        3. 社会经济权利：劳动权、休息权、社会保障权
                        4. 基本义务：维护国家统一、遵守宪法法律、依法纳税、服兵役
                        5. 权利与义务的关系：统一的、相辅相成的""",
            key_points=["权利和义务是统一的", "选举权需年满18周岁", "公民权利受法律保护"],
            common_mistakes=["只强调权利忽视义务", "混淆公民与人民的概念"],
            intuition_pumps=["享受权利的同时要履行义务，就像硬币的两面"]
        ))
        
        self._add_question(Question(
            subject=Subject.POLITICS,
            topic_id="pol_economy",
            topic_name="市场经济",
            question_type=QuestionType.CHOICE,
            difficulty=2,
            content="在社会主义市场经济中，资源配置起决定性作用的是？",
            options=["A. 政府", "B. 市场", "C. 企业", "D. 个人"],
            correct_answer="B",
            explanation="党的十八届三中全会明确提出'市场在资源配置中起决定性作用'"
        ))
        
        self._add_question(Question(
            subject=Subject.POLITICS,
            topic_id="pol_economy",
            topic_name="市场经济",
            question_type=QuestionType.QA,
            difficulty=3,
            content="请解释'市场在资源配置中起决定性作用，更好发挥政府作用'的含义。",
            correct_answer="市场通过价格机制调节供需，政府进行宏观调控弥补市场失灵",
            explanation="这是市场与政府关系的核心表述，强调两者的有机结合"
        ))
        
        self._add_question(Question(
            subject=Subject.POLITICS,
            topic_id="pol_economy",
            topic_name="市场经济",
            question_type=QuestionType.APPLICATION,
            difficulty=4,
            content="结合实际案例，分析政府在应对市场失灵（如疫情期间物资短缺）时应该如何发挥作用。",
            correct_answer="开放性答案",
            explanation="政府可采取价格管控、统一调配、增加供给等措施，体现政府的宏观调控作用",
            is_transfer=True
        ))
        
        self._add_question(Question(
            subject=Subject.POLITICS,
            topic_id="pol_citizen",
            topic_name="公民权利",
            question_type=QuestionType.JUDGMENT,
            difficulty=2,
            content="公民只享有权利，不需要履行义务。",
            correct_answer="错误",
            explanation="权利和义务是统一的，公民在享有权利的同时必须履行相应义务"
        ))
        
        # 添加初始日志
        self._add_log("success", "系统初始化完成", {"questions": len(self.questions), "knowledge": len(self.knowledge)})
    
    def _add_knowledge(self, item: KnowledgeItem):
        """添加知识点"""
        self.knowledge[item.id] = item
    
    def _add_question(self, q: Question):
        """添加题目"""
        self.questions[q.id] = q
    
    def _add_log(self, log_type: str, message: str, details: dict = None):
        """添加日志"""
        self.logs.append(SystemLog(
            log_type=log_type,
            message=message,
            details=details
        ))

    # 查询方法
    
    def get_questions_by_subject(self, subject: Subject) -> List[Question]:
        """获取某学科的所有题目"""
        return [q for q in self.questions.values() if q.subject == subject]
    
    def get_questions_by_topic(self, subject: Subject, topic_id: str) -> List[Question]:
        """获取某主题的所有题目"""
        return [q for q in self.questions.values() 
                if q.subject == subject and q.topic_id == topic_id]
    
    def get_transfer_questions(self, subject: Subject, topic_id: str) -> List[Question]:
        """获取迁移测试题目"""
        return [q for q in self.questions.values() 
                if q.subject == subject and q.topic_id == topic_id and q.is_transfer]
    
    def get_knowledge_by_subject(self, subject: Subject) -> List[KnowledgeItem]:
        """获取某学科的所有知识点"""
        return [k for k in self.knowledge.values() if k.subject == subject]
    
    def get_knowledge_by_topic(self, subject: Subject, topic_id: str) -> List[KnowledgeItem]:
        """获取某主题的知识点"""
        return [k for k in self.knowledge.values() 
                if k.subject == subject and k.topic_id == topic_id]
    
    def get_topics_by_subject(self, subject: Subject) -> List[Dict[str, str]]:
        """获取某学科的所有主题"""
        topics = {}
        for k in self.knowledge.values():
            if k.subject == subject:
                topics[k.topic_id] = k.topic_name
        return [{"id": tid, "name": tname} for tid, tname in topics.items()]
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """获取会话"""
        return self.sessions.get(session_id)
    
    def create_session(self, student_id: str, subject: Subject) -> Session:
        """创建会话"""
        session = Session(
            student_id=student_id,
            subject=subject
        )
        self.sessions[session.id] = session
        return session
    
    def update_session(self, session: Session):
        """更新会话"""
        session.updated_at = datetime.now()
        self.sessions[session.id] = session
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计数据"""
        subject_stats = {}
        for subj in Subject:
            questions = self.get_questions_by_subject(subj)
            knowledge = self.get_knowledge_by_subject(subj)
            subject_stats[subj.value] = {
                "questions": len(questions),
                "knowledge": len(knowledge),
                "topics": len(self.get_topics_by_subject(subj))
            }
        
        return {
            "active_students": len(set(s.student_id for s in self.sessions.values())),
            "knowledge_count": len(self.knowledge),
            "question_count": len(self.questions),
            "ai_interactions": self.ai_interactions,
            "average_mastery": 0.65,  # 模拟数据
            "subject_stats": subject_stats
        }
    
    def increment_interactions(self):
        """增加交互次数"""
        self.ai_interactions += 1
    
    def add_question(self, q: Question) -> Question:
        """添加题目（对外接口）"""
        self.questions[q.id] = q
        self._add_log("success", f"添加题目: {q.content[:30]}...", {"subject": q.subject, "type": q.question_type})
        return q
    
    def update_question(self, q: Question) -> Question:
        """更新题目"""
        self.questions[q.id] = q
        self._add_log("info", f"更新题目: {q.id}")
        return q
    
    def delete_question(self, question_id: str) -> bool:
        """删除题目"""
        if question_id in self.questions:
            del self.questions[question_id]
            self._add_log("warning", f"删除题目: {question_id}")
            return True
        return False
    
    def add_knowledge(self, k: KnowledgeItem) -> KnowledgeItem:
        """添加知识点（对外接口）"""
        self.knowledge[k.id] = k
        self._add_log("success", f"添加知识点: {k.title}", {"subject": k.subject})
        return k
    
    def update_knowledge(self, k: KnowledgeItem) -> KnowledgeItem:
        """更新知识点"""
        self.knowledge[k.id] = k
        self._add_log("info", f"更新知识点: {k.id}")
        return k
    
    def delete_knowledge(self, knowledge_id: str) -> bool:
        """删除知识点"""
        if knowledge_id in self.knowledge:
            del self.knowledge[knowledge_id]
            self._add_log("warning", f"删除知识点: {knowledge_id}")
            return True
        return False
    
    def get_recent_logs(self, limit: int = 20) -> List[SystemLog]:
        """获取最近的日志"""
        return sorted(self.logs, key=lambda x: x.timestamp, reverse=True)[:limit]

# 全局数据库实例
db = Database()
