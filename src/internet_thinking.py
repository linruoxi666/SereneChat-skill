
import random
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class InternetThinking:
    """
    联网思考模块 - 模拟小龙虾的"上网搜索"能力
    根据用户输入的话题，结合知识库生成更智能的回复
    """

    def __init__(self):
        self._init_knowledge_base()
        self._init_topic_patterns()

    def _init_knowledge_base(self):
        """初始化知识库 - 模拟网络知识"""
        self.knowledge_base = {
            '天气': {
                'facts': [
                    '今天天气不错的话适合出去走走',
                    '下雨天记得带伞，别淋湿了',
                    '天气冷的话多穿点衣服',
                    '大热天记得多喝水',
                ],
                'suggestions': [
                    '要不要出去走走',
                    '记得看天气预报',
                    '注意保暖',
                    '多喝水',
                ]
            },
            '美食': {
                'facts': [
                    '火锅是很多人喜欢的',
                    '奶茶最近很火',
                    '烧烤适合朋友聚会',
                    '寿司比较清淡健康',
                ],
                'suggestions': [
                    '一起去吃吧',
                    '我知道一家不错的店',
                    '要不吃点好的',
                    '自己做也行',
                ]
            },
            '电影': {
                'facts': [
                    '最近有几部新片上映',
                    '经典电影值得反复看',
                    '悬疑片比较烧脑',
                    '爱情片适合情侣看',
                ],
                'suggestions': [
                    '一起看吧',
                    '推荐你看一部',
                    '周末去看',
                    '在家看也行',
                ]
            },
            '音乐': {
                'facts': [
                    '听音乐能放松心情',
                    '老歌越听越有味道',
                    '轻音乐适合工作时听',
                    '摇滚适合发泄情绪',
                ],
                'suggestions': [
                    '分享一首歌给你',
                    '一起听吧',
                    '推荐个歌手',
                    '听歌放松一下',
                ]
            },
            '游戏': {
                'facts': [
                    '适度游戏有益放松',
                    '手游比较方便',
                    '单机游戏剧情好',
                    '联机游戏可以一起玩',
                ],
                'suggestions': [
                    '一起玩吧',
                    '推荐一个游戏',
                    '别玩太久',
                    '休息一下眼睛',
                ]
            },
            '工作': {
                'facts': [
                    '工作再忙也要注意休息',
                    '效率比时长更重要',
                    '适当摸鱼有助于效率',
                    '加班太多对身体不好',
                ],
                'suggestions': [
                    '别太累了',
                    '注意休息',
                    '效率优先',
                    '该下班就下班',
                ]
            },
            '学习': {
                'facts': [
                    '学习要劳逸结合',
                    '专注力比时间重要',
                    '适当休息效果更好',
                    '兴趣是最好的老师',
                ],
                'suggestions': [
                    '加油',
                    '注意休息',
                    '有不懂的可以问我',
                    '慢慢来',
                ]
            },
            '健康': {
                'facts': [
                    '早睡早起身体好',
                    '多喝水对身体好',
                    '运动能增强免疫力',
                    '心情好身体才好',
                ],
                'suggestions': [
                    '注意休息',
                    '多运动',
                    '保持好心情',
                    '定期体检',
                ]
            },
            '旅行': {
                'facts': [
                    '旅行能放松心情',
                    '提前做好攻略',
                    '淡季出行更划算',
                    '注意安全',
                ],
                'suggestions': [
                    '一起去吧',
                    '推荐个地方',
                    '做好攻略',
                    '拍照片给我',
                ]
            },
            '宠物': {
                'facts': [
                    '养宠物能缓解压力',
                    '猫猫比较独立',
                    '狗狗比较粘人',
                    '养宠物需要责任心',
                ],
                'suggestions': [
                    '好可爱',
                    '我也想养',
                    '多陪陪它',
                    '注意卫生',
                ]
            },
            '科技': {
                'facts': [
                    'AI发展很快',
                    '新手机功能越来越强',
                    '智能家居很方便',
                    '科技改变生活',
                ],
                'suggestions': [
                    '试试新功能',
                    '了解一下',
                    '科技让生活更好',
                    '别过度依赖',
                ]
            },
            '节日': {
                'facts': [
                    '节日要有仪式感',
                    '送礼物要用心',
                    '陪伴是最好的礼物',
                    '节日美食不能少',
                ],
                'suggestions': [
                    '节日快乐',
                    '一起庆祝',
                    '送你个礼物',
                    '吃顿好的',
                ]
            },
        }

        # 通用知识（当没有匹配到具体话题时使用）
        self.general_knowledge = [
            '最近网上说这个挺火的',
            '我看到一个有趣的观点',
            '有人说这个很有道理',
            '网上讨论这个的很多',
        ]

    def _init_topic_patterns(self):
        """初始化话题匹配模式"""
        self.topic_patterns = {
            '天气': ['天气', '下雨', '晴天', '阴天', '冷', '热', '温度', '气温', '下雪', '刮风', '雾霾'],
            '美食': ['吃', '饭', '菜', '火锅', '烧烤', '奶茶', '寿司', '美食', '好吃', '饿', '餐厅', '外卖'],
            '电影': ['电影', '看片', '追剧', '影院', '票房', '演员', '导演', '剧情'],
            '音乐': ['歌', '音乐', '听', '唱', '歌手', '乐队', '专辑', '旋律', '歌词'],
            '游戏': ['游戏', '玩', '打', '通关', '段位', '队友', '挂机', '氪金', '手游', '网游'],
            '工作': ['工作', '上班', '加班', '老板', '同事', '项目', '客户', '开会', ' deadline', '任务'],
            '学习': ['学习', '考试', '复习', '作业', '论文', '课程', '专业', '学校', '老师', '成绩'],
            '健康': ['健康', '生病', '感冒', '发烧', '医院', '医生', '药', '锻炼', '运动', '减肥'],
            '旅行': ['旅行', '旅游', '出去玩', '景点', '酒店', '机票', '攻略', '度假', '风景'],
            '宠物': ['猫', '狗', '宠物', '萌宠', '铲屎官', '撸猫', '遛狗', '猫粮', '狗粮'],
            '科技': ['手机', '电脑', 'APP', '软件', '科技', 'AI', '智能', '数码', '新品', '发布会'],
            '节日': ['节日', '过年', '生日', '圣诞', '情人节', '礼物', '庆祝', '放假', '假期'],
        }

    def analyze_topic(self, user_input: str) -> Tuple[Optional[str], float]:
        """
        分析用户输入的话题
        返回: (话题类型, 匹配度)
        """
        user_input_lower = user_input.lower()
        best_topic = None
        best_score = 0

        for topic, patterns in self.topic_patterns.items():
            score = sum(2 for pattern in patterns if pattern in user_input_lower)
            if score > best_score:
                best_score = score
                best_topic = topic

        # 计算匹配度
        confidence = min(1.0, best_score * 0.2) if best_score > 0 else 0

        return best_topic, confidence

    def get_knowledge(self, topic: str) -> Optional[Dict[str, List[str]]]:
        """获取某个话题的知识"""
        return self.knowledge_base.get(topic)

    def generate_thinking(self, user_input: str, emotion_type: str) -> str:
        """
        生成"联网思考"内容
        模拟小龙虾上网搜索后形成的想法
        """
        topic, confidence = self.analyze_topic(user_input)

        if not topic or confidence < 0.3:
            # 没有明确话题，返回空思考
            return ""

        knowledge = self.get_knowledge(topic)
        if not knowledge:
            return ""

        # 根据情感类型选择不同的思考方向
        thoughts = []

        # 添加一个事实
        fact = random.choice(knowledge['facts'])
        thoughts.append(fact)

        # 根据情感添加建议
        if emotion_type in ['难过', '累', '生气', '担心']:
            # 负面情绪：提供安慰性建议
            suggestion = random.choice(knowledge['suggestions'])
            thoughts.append(f"我想{suggestion}")
        elif emotion_type in ['开心', '爱', '想']:
            # 正面情绪：分享快乐
            suggestion = random.choice(knowledge['suggestions'])
            thoughts.append(f"可以{suggestion}")
        else:
            # 中性：简单提及
            pass

        return "；".join(thoughts)

    def enrich_response(self, base_response: str, user_input: str, emotion_type: str) -> str:
        """
        用联网思考的结果丰富回复
        将知识自然融入回复中
        """
        # 如果基础回复太短或太简单，不添加知识（避免突兀）
        if len(base_response) <= 3 or base_response in ['嗯', '啊', '哦', '好', '行', '你说', '这样啊', '我知道了']:
            return base_response

        topic, confidence = self.analyze_topic(user_input)

        if not topic or confidence < 0.5:
            # 匹配度不够，不添加知识
            return base_response

        # 日常问候类话题不添加知识（避免生硬）
        if topic in ['美食'] and any(word in user_input for word in ['吃饭', '吃了', '饿', '喝']):
            # 用户问"吃饭了吗"这类日常问候，不塞知识
            if '吗' in user_input or '了' in user_input:
                return base_response

        knowledge = self.get_knowledge(topic)
        if not knowledge:
            return base_response

        # 决定是否添加知识（不是每次都加，保持自然）
        if random.random() > 0.5:
            return base_response

        # 选择一个相关知识片段
        fact = random.choice(knowledge['facts'])

        # 将知识自然融入回复
        enrichments = [
            f"{base_response}，{fact}",
            f"{base_response}。对了，{fact}",
        ]

        return random.choice(enrichments)

    def get_topic_suggestion(self, user_input: str) -> Optional[str]:
        """
        根据话题给出建议
        用于主动消息或话题引导
        """
        topic, confidence = self.analyze_topic(user_input)

        if not topic or confidence < 0.3:
            return None

        knowledge = self.get_knowledge(topic)
        if not knowledge:
            return None

        return random.choice(knowledge['suggestions'])
