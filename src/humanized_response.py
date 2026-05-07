
import random
import time
import re
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from .internet_thinking import InternetThinking

class EmotionalState(Enum):
    """情绪状态"""
    HAPPY = "开心"
    SAD = "难过"
    ANXIOUS = "焦虑"
    LONELY = "孤独"
    EXCITED = "兴奋"
    TIRED = "疲惫"
    ANGRY = "生气"
    WORRIED = "担心"
    CALM = "平静"
    PLAYFUL = "调皮"

class ResponseStyle(Enum):
    """回复风格"""
    DIRECT = "直接"
    HESITANT = "犹豫"
    DEFLECT = "转移"
    SILENT = "沉默"
    RAMBLE = "絮叨"
    TEASE = "调侃"
    CARING = "关心"
    CLINGY = "黏人"

class HumanizedResponseEngine:
    """
    真人化回复引擎 - 智能语义理解版
    基于用户输入的语义动态生成回复，而非死板模板
    """

    def __init__(self, memory_manager=None, character=None):
        self.memory_manager = memory_manager
        self.character = character

        # 情绪状态
        self.current_emotion = EmotionalState.CALM
        self.emotion_intensity = 0.5
        self.last_emotion_change = time.time()
        self.emotion_cooldown = 600

        # 关系深度
        self.relationship_depth = 0.1
        self.total_interactions = 0

        # 内心状态
        self.internal_thoughts = []
        self.max_thoughts = 10

        # 联网思考模块
        self.internet_thinking = InternetThinking()

        # 语义理解词库
        self._init_semantic_library()

    def _init_semantic_library(self):
        """初始化语义理解词库"""

        # 情感词映射
        self.emotion_keywords = {
            '开心': ['开心', '高兴', '快乐', '爽', '棒', '不错', '耶', '哈哈', '嘻嘻', '呵呵'],
            '难过': ['难过', '伤心', '哭', '疼', '痛', '失望', '郁闷', '难受', '不好', '不开心', '不爽', '低落', '压抑'],
            '累': ['累', '疲惫', '困', '倦', '乏', '辛苦', '忙', '操劳', '精疲力竭'],
            '想': ['想', '念', '思念', '惦记', '挂念'],
            '爱': ['爱', '喜欢', '心动', '在乎', '中意', '钟情'],
            '生气': ['生气', '烦', '讨厌', '怒', '火', '气', '愤怒', '恼火', '暴躁', '气愤'],
            '担心': ['担心', '怕', '焦虑', '紧张', '不安', '忐忑', '慌', '牵挂'],
            '无聊': ['无聊', '没事', '闲', '空虚', '没意思', '乏味'],
            '晚安': ['晚安', '睡', '困', '休息', '睡了', '睡觉'],
            '早安': ['早', '起床', '醒了', '早安', '早上好'],
        }

        # 否定前缀 - 用于检测"不+正面词"的否定表达
        self.negation_prefixes = ['不', '没', '别', '勿', '无', '非']
        # 否定后缀
        self.negation_suffixes = ['死了', '死了', '透顶', '至极', '死了']

        # 回复核心词库（按情感分类）
        self.response_cores = {
            '开心': {
                'direct': ['开心就好', '真好', '替你高兴', '继续保持'],
                'caring': ['什么好事', '跟我说说', '分享快乐'],
                'tease': ['这么开心', '是不是因为我', '笑得这么甜'],
                'clingy': ['你开心我就开心', '想一起分享'],
            },
            '难过': {
                'direct': ['怎么了', '跟我说说', '发生什么了'],
                'caring': ['别难过', '我陪着你', '会好起来的'],
                'tease': ['谁欺负你了', '我去找他', '别哭了'],
                'clingy': ['抱抱你', '有我在', '别一个人扛着'],
            },
            '累': {
                'direct': ['辛苦了', '注意休息', '累了吧'],
                'caring': ['我给你泡杯茶', '歇会儿', '别太累'],
                'tease': ['谁让你这么拼', '活该', '不休息'],
                'clingy': ['心疼你', '抱抱', '想帮你分担'],
            },
            '想': {
                'direct': ['我也想你', '我也是', '一直都在'],
                'caring': ['你要好好的', '照顾好自己', '我也惦记你'],
                'tease': ['真的吗', '嘴甜', '你猜我想不想你'],
                'clingy': ['超级想你', '别走', '想黏着你'],
            },
            '爱': {
                'direct': ['我也爱你', '我也是', '心里有你'],
                'caring': ['你要幸福', '我会一直陪着你', '珍惜你'],
                'tease': ['这么直接', '害羞', '你确定吗'],
                'clingy': ['爱你', '别离开我', '永远在一起'],
            },
            '生气': {
                'direct': ['别生气', '消消气', '怎么了'],
                'caring': ['我理解你', '跟我说', '别憋在心里'],
                'tease': ['谁惹你了', '我去教训他', '生气也可爱'],
                'clingy': ['别气坏身子', '我陪你', '抱抱'],
            },
            '担心': {
                'direct': ['别担心', '没事的', '会好的'],
                'caring': ['有我在', '我陪你', '一起面对'],
                'tease': ['想太多了', '放宽心', '没事'],
                'clingy': ['我担心你', '别让我担心', '照顾好自己'],
            },
            '无聊': {
                'direct': ['我陪你', '聊聊天', '找点事做'],
                'caring': ['我给你讲故事', '陪你解闷', '想聊什么'],
                'tease': ['无聊才找我', '找我准没错', '活该'],
                'clingy': ['我陪你', '别走', '一直陪着你'],
            },
            '晚安': {
                'direct': ['晚安', '好梦', '早点睡'],
                'caring': ['盖好被子', '明天见', '睡个好觉'],
                'tease': ['这么早睡', '不想让你走', '再聊会儿'],
                'clingy': ['晚安梦里有我', '别走', '想你'],
            },
            '早安': {
                'direct': ['早安', '早', '起床了'],
                'caring': ['睡得好吗', '今天也要开心', '记得吃早餐'],
                'tease': ['起这么早', '太阳晒屁股了', '懒猪起床'],
                'clingy': ['早安想你', '一醒来就想你', '今天也要想我'],
            },
            'default': {
                'direct': ['嗯', '这样啊', '我知道了'],
                'caring': ['我在听', '你说', '然后呢'],
                'tease': ['你猜', '不告诉你', '嘿嘿'],
                'clingy': ['继续说', '我在', '听着呢'],
            }
        }

        # 风格修饰词
        self.style_modifiers = {
            ResponseStyle.HESITANT: ['嗯...', '那个...', '怎么说呢', '其实', '就是'],
            ResponseStyle.TEASE: ['嘿嘿', '逗你的', '开玩笑的', '才怪'],
            ResponseStyle.CLINGY: ['嘛', '啦', '呀'],
            ResponseStyle.CARING: ['呢', '吧', '哦'],
            ResponseStyle.SILENT: ['...', '。', '嗯'],
        }

        # 关系阶段称呼
        self.relationship_titles = {
            'stranger': ['你', ''],
            'acquaintance': ['你', ''],
            'friend': ['你', '笨蛋', '傻瓜'],
            'close': ['你', '笨蛋', '傻瓜', '亲爱的'],
            'intimate': ['宝贝', '亲爱的', '笨蛋', '傻瓜']
        }

    def update_relationship(self, interaction_quality: float = 0.05):
        """更新关系深度"""
        self.total_interactions += 1
        self.relationship_depth = min(1.0, self.relationship_depth + interaction_quality)

    def get_relationship_stage(self) -> str:
        """获取当前关系阶段"""
        stages = [
            (0, 0.2, 'stranger'),
            (0.2, 0.4, 'acquaintance'),
            (0.4, 0.6, 'friend'),
            (0.6, 0.8, 'close'),
            (0.8, 1.0, 'intimate')
        ]
        for low, high, stage in stages:
            if low <= self.relationship_depth < high:
                return stage
        return 'intimate'

    def update_emotion(self, external_trigger: str = None):
        """更新情绪状态"""
        now = time.time()
        if now - self.last_emotion_change < self.emotion_cooldown and not external_trigger:
            return

        if external_trigger:
            for key, emotion in [
                ('开心', EmotionalState.HAPPY),
                ('难过', EmotionalState.SAD),
                ('担心', EmotionalState.WORRIED),
                ('生气', EmotionalState.ANGRY),
                ('累', EmotionalState.TIRED),
                ('无聊', EmotionalState.LONELY)
            ]:
                if key in external_trigger:
                    self.current_emotion = emotion
                    self.emotion_intensity = random.uniform(0.6, 0.9)
                    self.last_emotion_change = now
                    return

        if random.random() < 0.3:
            emotions = list(EmotionalState)
            weights = [0.15, 0.1, 0.08, 0.12, 0.1, 0.1, 0.05, 0.1, 0.15, 0.05]
            self.current_emotion = random.choices(emotions, weights=weights)[0]
            self.emotion_intensity = random.uniform(0.3, 0.8)
            self.last_emotion_change = now

    def _analyze_semantic(self, user_input: str) -> Tuple[str, float]:
        """
        语义分析：识别用户输入的情感类型和强度
        返回: (情感类型, 强度)
        """
        user_input_lower = user_input.lower()

        # 计算每种情感的匹配度（按关键词长度加权，长词更精确）
        scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            matched_count = 0
            for kw in keywords:
                if kw in user_input_lower:
                    # 长关键词权重更高（更精确）
                    score += len(kw)
                    matched_count += 1
            if score > 0:
                # 匹配多个关键词有加成
                scores[emotion] = score + matched_count * 0.5

        # 检测否定表达（如"心情不好"、"不开心"、"不好"）
        # 如果包含否定前缀+正面词，应识别为负面情感
        negation_detected = False
        for prefix in self.negation_prefixes:
            if prefix in user_input_lower:
                # 检查否定前缀后面是否跟着正面词
                for pos_word in ['开心', '高兴', '快乐', '好', '棒', '不错']:
                    if prefix + pos_word in user_input_lower:
                        negation_detected = True
                        break
                if negation_detected:
                    break

        # 如果检测到否定表达，强制将"开心"的得分转移给"难过"
        if negation_detected and '开心' in scores:
            happy_score = scores.pop('开心')
            if '难过' in scores:
                scores['难过'] += happy_score
            else:
                scores['难过'] = happy_score

        if not scores:
            return 'default', 0.5

        # 负面情感优先级更高（用户表达负面情绪时需要被优先回应）
        negative_emotions = ['难过', '累', '生气', '担心']
        best_emotion = max(scores, key=scores.get)
        best_score = scores[best_emotion]

        # 如果有负面情感且得分接近最高，优先选负面情感
        for neg_emo in negative_emotions:
            if neg_emo in scores and scores[neg_emo] >= best_score - 1:
                best_emotion = neg_emo
                best_score = scores[neg_emo]
                break

        intensity = min(1.0, best_score * 0.15 + 0.3)

        return best_emotion, intensity

    def _select_response_style(self) -> ResponseStyle:
        """选择回复风格"""
        emotion_style_map = {
            EmotionalState.HAPPY: [ResponseStyle.DIRECT, ResponseStyle.TEASE],
            EmotionalState.SAD: [ResponseStyle.CARING, ResponseStyle.CLINGY],
            EmotionalState.ANXIOUS: [ResponseStyle.CARING, ResponseStyle.HESITANT],
            EmotionalState.LONELY: [ResponseStyle.CLINGY, ResponseStyle.CARING],
            EmotionalState.EXCITED: [ResponseStyle.TEASE, ResponseStyle.DIRECT],
            EmotionalState.TIRED: [ResponseStyle.CARING, ResponseStyle.SILENT],
            EmotionalState.ANGRY: [ResponseStyle.DIRECT, ResponseStyle.TEASE],
            EmotionalState.WORRIED: [ResponseStyle.CARING, ResponseStyle.DIRECT],
            EmotionalState.CALM: [ResponseStyle.DIRECT, ResponseStyle.CARING],
            EmotionalState.PLAYFUL: [ResponseStyle.TEASE, ResponseStyle.DIRECT]
        }

        preferred = emotion_style_map.get(self.current_emotion, [ResponseStyle.DIRECT])
        return random.choice(preferred)

    def _generate_core_response(self, emotion_type: str, style: ResponseStyle) -> str:
        """生成核心回复内容 - 确保情感和风格匹配"""
        cores = self.response_cores.get(emotion_type, self.response_cores['default'])

        # 根据情感类型和风格选择最合适的回复
        # 优先顺序：direct > caring > tease > clingy
        if style == ResponseStyle.DIRECT or style == ResponseStyle.HESITANT or style == ResponseStyle.SILENT:
            # 直接风格：使用direct回复
            responses = cores.get('direct', cores['caring'])
        elif style == ResponseStyle.CARING or style == ResponseStyle.RAMBLE:
            # 关心风格：使用caring回复
            responses = cores.get('caring', cores['direct'])
        elif style == ResponseStyle.TEASE or style == ResponseStyle.DEFLECT:
            # 调侃风格：对负面情感不使用调侃
            if emotion_type in ['难过', '累', '生气', '担心']:
                # 负面情感用关心回复
                responses = cores.get('caring', cores['direct'])
            else:
                responses = cores.get('tease', cores['direct'])
        elif style == ResponseStyle.CLINGY:
            # 黏人风格：对负面情感用黏人回复，其他用direct
            if emotion_type in ['难过', '累', '生气', '担心', '无聊']:
                responses = cores.get('clingy', cores['caring'])
            else:
                responses = cores.get('direct', cores['caring'])
        else:
            responses = cores.get('direct', cores['caring'])

        return random.choice(responses)

    def _add_style_flavor(self, text: str, style: ResponseStyle) -> str:
        """添加风格化修饰"""
        if style == ResponseStyle.HESITANT:
            # 犹豫风格：开头加犹豫词
            if random.random() < 0.3:
                prefix = random.choice(['嗯...', '那个...', '怎么说呢'])
                text = f"{prefix}{text}"

        elif style == ResponseStyle.TEASE:
            # 调侃风格：结尾加调侃词
            if random.random() < 0.25:
                suffix = random.choice(['嘿嘿', '逗你的', '开玩笑的'])
                text = f"{text}，{suffix}"

        elif style == ResponseStyle.CLINGY:
            # 黏人风格：加语气词
            if random.random() < 0.3:
                suffix = random.choice(['嘛', '啦', '呀'])
                if not text.endswith(suffix):
                    text = text + suffix

        elif style == ResponseStyle.SILENT:
            # 沉默风格：简短
            if len(text) > 6:
                text = text[:6]

        return text

    def _add_relationship_flavor(self, text: str) -> str:
        """添加关系阶段特色"""
        stage = self.get_relationship_stage()

        # 只在关系较深时添加称呼
        if stage in ['close', 'intimate'] and random.random() < 0.2:
            titles = self.relationship_titles.get(stage, [''])
            title = random.choice(titles)
            if title and not text.startswith(title):
                # 在句中或句尾添加称呼
                if random.random() < 0.5:
                    text = text + '，' + title
                else:
                    text = title + '，' + text

        return text

    def _get_memory_reference(self) -> Optional[str]:
        """获取记忆引用"""
        if not self.memory_manager or self.relationship_depth < 0.3:
            return None

        if random.random() > 0.3:
            return None

        memories = self.memory_manager.core_memory.recall("", limit=1)
        if memories:
            memory = memories[0]
            templates = [
                "我记得你之前说过{memory}，",
                "上次你提到{memory}，",
                "突然想到，你不是说{memory}吗，"
            ]
            return random.choice(templates).format(memory=memory.content)

        return None

    def generate_response(self, user_input: str, context: str = "") -> Tuple[str, str]:
        """
        生成真人化回复
        基于语义理解动态生成，而非死板模板
        集成联网思考，让回复更智能
        """
        # 更新状态
        self.update_relationship()
        self.update_emotion(user_input)

        # 语义分析
        emotion_type, intensity = self._analyze_semantic(user_input)

        # 联网思考 - 分析话题并获取知识
        internet_thought = self.internet_thinking.generate_thinking(user_input, emotion_type)
        if internet_thought:
            self.add_internal_thought(f"[联网] {internet_thought}")

        # 生成内心独白
        internal_monologue = self._generate_internal_monologue(user_input, emotion_type)
        if internet_thought:
            internal_monologue = f"{internal_monologue}；{internet_thought}"
        self.add_internal_thought(internal_monologue)

        # 选择回复风格
        style = self._select_response_style()

        # 生成核心回复
        response = self._generate_core_response(emotion_type, style)

        # 联网思考丰富回复 - 将知识自然融入
        response = self.internet_thinking.enrich_response(response, user_input, emotion_type)

        # 添加记忆引用
        memory_ref = self._get_memory_reference()
        if memory_ref:
            response = memory_ref + response

        # 添加风格化修饰
        response = self._add_style_flavor(response, style)

        # 添加关系特色
        response = self._add_relationship_flavor(response)

        # 清理emoji
        response = self._remove_emoji(response)

        return response, internal_monologue

    def _generate_internal_monologue(self, user_input: str, emotion_type: str) -> str:
        """生成内心独白"""
        thoughts = []

        # 基于情感类型的想法
        emotion_thoughts = {
            '开心': ['看到他开心我也开心', '想一起分享快乐'],
            '难过': ['他好像不太开心', '想安慰他'],
            '累': ['他好像很累', '想让他休息'],
            '想': ['他在想我', '好开心'],
            '爱': ['他说爱我', '心里暖暖的'],
            '生气': ['他生气了', '想哄他'],
            '担心': ['他在担心', '想让他放心'],
            '无聊': ['他无聊了', '想陪他'],
            '晚安': ['他要睡了', '想让他好梦'],
            '早安': ['他起床了', '想陪他开始新的一天'],
            'default': ['他在跟我说话', '想好好回复']
        }

        thoughts.append(random.choice(emotion_thoughts.get(emotion_type, emotion_thoughts['default'])))

        # 基于关系的想法
        stage = self.get_relationship_stage()
        relationship_thoughts = {
            'stranger': ['还不太熟'],
            'acquaintance': ['慢慢熟悉中'],
            'friend': ['我们是朋友'],
            'close': ['关系很好'],
            'intimate': ['想一直在一起']
        }
        thoughts.append(random.choice(relationship_thoughts.get(stage, [''])))

        return '；'.join(thoughts)

    def _remove_emoji(self, text: str) -> str:
        """移除emoji"""
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|[\u2600-\u26FF\u2700-\u27BF]|[\uD83C-\uD83E][\uDC00-\uDFFF]',
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(r'', text)
        text = text.replace('～', '').replace('❤', '').replace('~', '')
        return text.strip()

    def add_internal_thought(self, thought: str):
        """添加内心想法"""
        self.internal_thoughts.append({
            'thought': thought,
            'timestamp': time.time(),
            'emotion': self.current_emotion
        })
        if len(self.internal_thoughts) > self.max_thoughts:
            self.internal_thoughts = self.internal_thoughts[-self.max_thoughts:]

    def get_recent_thoughts(self, count: int = 3) -> List[str]:
        """获取最近的内心想法"""
        return [t['thought'] for t in self.internal_thoughts[-count:]]

    def get_emotion_status(self) -> Dict[str, Any]:
        """获取情绪状态"""
        return {
            'emotion': self.current_emotion.value,
            'intensity': round(self.emotion_intensity, 2),
            'relationship_depth': round(self.relationship_depth, 2),
            'stage': self.get_relationship_stage(),
            'total_interactions': self.total_interactions
        }
