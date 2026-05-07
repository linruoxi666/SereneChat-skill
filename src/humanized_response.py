
import random
import time
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from datetime import datetime

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
    DIRECT = "直接"           # 直接回答
    HESITANT = "犹豫"         # 犹豫、不确定
    DEFLECT = "转移"          # 转移话题
    SILENT = "沉默"           # 沉默、简短
    RAMBLE = "絮叨"           # 絮絮叨叨
    TEASE = "调侃"            # 调侃、开玩笑
    CARING = "关心"           # 关心、体贴
    CLINGY = "黏人"           # 黏人、撒娇

class HumanizedResponseEngine:
    """
    真人化回复引擎
    让小龙虾的回复更像真人，而不是AI
    """

    def __init__(self, memory_manager=None, character=None):
        self.memory_manager = memory_manager
        self.character = character

        # 情绪状态（随时间变化）
        self.current_emotion = EmotionalState.CALM
        self.emotion_intensity = 0.5  # 0-1
        self.last_emotion_change = time.time()
        self.emotion_cooldown = 600  # 10分钟情绪冷却

        # 关系深度（0-1，随聊天增加）
        self.relationship_depth = 0.1
        self.total_interactions = 0

        # 内心状态
        self.internal_thoughts = []
        self.max_thoughts = 10

        # 回复风格倾向（基于人设）
        self.style_weights = {
            ResponseStyle.DIRECT: 0.3,
            ResponseStyle.HESITANT: 0.1,
            ResponseStyle.DEFLECT: 0.1,
            ResponseStyle.SILENT: 0.05,
            ResponseStyle.RAMBLE: 0.15,
            ResponseStyle.TEASE: 0.1,
            ResponseStyle.CARING: 0.15,
            ResponseStyle.CLINGY: 0.05
        }

        # 真人语言特征
        self.filler_words = ['嗯', '那个', '就是', '其实', '话说', '怎么说呢', '哎呀', '啊']
        self.pause_marks = ['...', '。。。', '，', '——']
        self.self_corrections = ['不对', '等等', '我是说', '算了']

        # 记忆引用模板
        self.memory_templates = [
            "我记得你之前说过{memory}，",
            "上次你提到{memory}，",
            "突然想到，你不是说{memory}吗，",
            "我记得{memory}，",
            "你之前说的{memory}，我一直记着，"
        ]

        # 情绪影响回复 - 只保留空字符串，避免和风格化叠加产生怪话
        self.emotion_responses = {
            EmotionalState.HAPPY: {
                'prefix': [''],
                'suffix': [''],
                'tone': '轻快'
            },
            EmotionalState.SAD: {
                'prefix': [''],
                'suffix': [''],
                'tone': '低落'
            },
            EmotionalState.ANXIOUS: {
                'prefix': [''],
                'suffix': [''],
                'tone': '焦虑'
            },
            EmotionalState.LONELY: {
                'prefix': [''],
                'suffix': [''],
                'tone': '黏人'
            },
            EmotionalState.EXCITED: {
                'prefix': [''],
                'suffix': [''],
                'tone': '兴奋'
            },
            EmotionalState.TIRED: {
                'prefix': [''],
                'suffix': [''],
                'tone': '疲惫'
            },
            EmotionalState.ANGRY: {
                'prefix': [''],
                'suffix': [''],
                'tone': '生气'
            },
            EmotionalState.WORRIED: {
                'prefix': [''],
                'suffix': [''],
                'tone': '担心'
            },
            EmotionalState.CALM: {
                'prefix': [''],
                'suffix': [''],
                'tone': '平静'
            },
            EmotionalState.PLAYFUL: {
                'prefix': [''],
                'suffix': [''],
                'tone': '调皮'
            }
        }

        # 关系深度影响
        self.relationship_stages = {
            (0, 0.2): 'stranger',      # 陌生人
            (0.2, 0.4): 'acquaintance', # 认识
            (0.4, 0.6): 'friend',      # 朋友
            (0.6, 0.8): 'close',       # 亲密
            (0.8, 1.0): 'intimate'     # 恋人
        }

    def update_relationship(self, interaction_quality: float = 0.05):
        """更新关系深度"""
        self.total_interactions += 1
        self.relationship_depth = min(1.0, self.relationship_depth + interaction_quality)

    def get_relationship_stage(self) -> str:
        """获取当前关系阶段"""
        for (low, high), stage in self.relationship_stages.items():
            if low <= self.relationship_depth < high:
                return stage
        return 'intimate'

    def update_emotion(self, external_trigger: str = None):
        """更新情绪状态"""
        now = time.time()
        if now - self.last_emotion_change < self.emotion_cooldown and not external_trigger:
            return

        # 基于外部触发或随机变化
        if external_trigger:
            emotion_map = {
                '开心': EmotionalState.HAPPY,
                '难过': EmotionalState.SAD,
                '担心': EmotionalState.WORRIED,
                '生气': EmotionalState.ANGRY,
                '累': EmotionalState.TIRED,
                '无聊': EmotionalState.LONELY
            }
            for key, emotion in emotion_map.items():
                if key in external_trigger:
                    self.current_emotion = emotion
                    self.emotion_intensity = random.uniform(0.6, 0.9)
                    self.last_emotion_change = now
                    return

        # 随机情绪变化（模拟真实情绪波动）
        if random.random() < 0.3:  # 30%概率变化
            emotions = list(EmotionalState)
            weights = [0.15, 0.1, 0.08, 0.12, 0.1, 0.1, 0.05, 0.1, 0.15, 0.05]
            self.current_emotion = random.choices(emotions, weights=weights)[0]
            self.emotion_intensity = random.uniform(0.3, 0.8)
            self.last_emotion_change = now

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

    def _select_response_style(self) -> ResponseStyle:
        """选择回复风格"""
        # 基于情绪选择
        emotion_style_map = {
            EmotionalState.HAPPY: [ResponseStyle.DIRECT, ResponseStyle.TEASE, ResponseStyle.RAMBLE],
            EmotionalState.SAD: [ResponseStyle.SILENT, ResponseStyle.HESITANT, ResponseStyle.CARING],
            EmotionalState.ANXIOUS: [ResponseStyle.HESITANT, ResponseStyle.CARING],
            EmotionalState.LONELY: [ResponseStyle.CLINGY, ResponseStyle.CARING],
            EmotionalState.EXCITED: [ResponseStyle.RAMBLE, ResponseStyle.TEASE, ResponseStyle.DIRECT],
            EmotionalState.TIRED: [ResponseStyle.SILENT, ResponseStyle.HESITANT],
            EmotionalState.ANGRY: [ResponseStyle.DEFLECT, ResponseStyle.SILENT],
            EmotionalState.WORRIED: [ResponseStyle.CARING, ResponseStyle.HESITANT],
            EmotionalState.CALM: [ResponseStyle.DIRECT, ResponseStyle.RAMBLE],
            EmotionalState.PLAYFUL: [ResponseStyle.TEASE, ResponseStyle.RAMBLE]
        }

        preferred = emotion_style_map.get(self.current_emotion, [ResponseStyle.DIRECT])
        weights = [self.style_weights.get(s, 0.1) for s in preferred]
        return random.choices(preferred, weights=weights)[0]

    def _get_memory_reference(self) -> Optional[str]:
        """获取记忆引用（让回复更个性化）"""
        if not self.memory_manager:
            return None

        # 只有关系较深时才引用记忆
        if self.relationship_depth < 0.3:
            return None

        # 随机决定是否引用记忆
        if random.random() > 0.4:  # 40%概率
            return None

        # 获取一条随机记忆
        memories = self.memory_manager.core_memory.recall("", limit=1)
        if memories:
            memory = memories[0]
            template = random.choice(self.memory_templates)
            return template.format(memory=memory.content)

        return None

    def _add_human_imperfections(self, text: str, style: ResponseStyle) -> str:
        """添加人类不完美特征 - 控制概率避免过度修改"""
        result = text

        # 根据风格添加特征（降低概率，避免过度修改）
        if style == ResponseStyle.HESITANT:
            # 添加犹豫词（低概率）
            if random.random() < 0.2:
                filler = random.choice(['嗯', '那个'])
                result = f"{filler}...{result}"

        elif style == ResponseStyle.TEASE:
            # 调侃语气（低概率）
            if random.random() < 0.15:
                result = f"{result}，{random.choice(['嘿嘿', '逗你的'])}"

        # 随机添加语气词（极低概率，避免破坏语义）
        if random.random() < 0.08:
            suffix = random.choice(['呢', '呀', '吧'])
            if not result.endswith(suffix):
                result = result + suffix

        return result

    def _apply_emotion_tone(self, text: str) -> str:
        """应用情绪语调"""
        emotion_data = self.emotion_responses.get(self.current_emotion, {})

        prefix = random.choice(emotion_data.get('prefix', ['']))
        suffix = random.choice(emotion_data.get('suffix', ['']))

        result = text
        if prefix and not result.startswith(prefix):
            result = prefix + result
        if suffix and not result.endswith(suffix):
            result = result + suffix

        return result

    def _get_relationship_aware_response(self, base_response: str, user_input: str) -> str:
        """根据关系深度调整回复 - 极低概率添加后缀"""
        stage = self.get_relationship_stage()

        # 只在基础回复较短时添加后缀，避免语义混乱
        if len(base_response) > 8:
            return base_response

        if stage == 'acquaintance':
            if random.random() < 0.1:
                return base_response + '，最近怎么样'

        elif stage == 'friend':
            if random.random() < 0.12:
                return base_response + random.choice(['，哈哈', '，你呢'])

        elif stage == 'close':
            if random.random() < 0.15:
                return base_response + random.choice(['，想你', '，笨蛋'])

        elif stage == 'intimate':
            if random.random() < 0.18:
                return base_response + random.choice(['，抱抱', '，想你'])

        return base_response

    def generate_response(self, user_input: str, context: str = "") -> Tuple[str, str]:
        """
        生成真人化回复
        返回: (回复内容, 内心独白)
        """
        # 更新状态
        self.update_relationship()
        self.update_emotion(user_input)

        # 生成内心独白
        internal_monologue = self._generate_internal_monologue(user_input)
        self.add_internal_thought(internal_monologue)

        # 选择回复风格
        style = self._select_response_style()

        # 获取基础回复
        response = self._generate_base_response(user_input, style)

        # 添加记忆引用
        memory_ref = self._get_memory_reference()
        if memory_ref:
            response = memory_ref + response

        # 应用关系深度
        response = self._get_relationship_aware_response(response, user_input)

        # 添加人类不完美特征
        response = self._add_human_imperfections(response, style)

        # 确保没有emoji
        response = self._remove_emoji(response)

        return response, internal_monologue

    def _generate_internal_monologue(self, user_input: str) -> str:
        """生成内心独白"""
        monologues = []

        # 基于情绪的想法
        emotion_thoughts = {
            EmotionalState.HAPPY: [
                f"看到他说'{user_input}'，我有点开心",
                "今天心情不错，想多聊几句",
                "他来了，真好"
            ],
            EmotionalState.SAD: [
                f"他说'{user_input}'，我有点难过",
                "不知道他有没有感觉到我不开心",
                "想让他多陪陪我"
            ],
            EmotionalState.LONELY: [
                f"终于等到他说'{user_input}'了",
                "他不在的时候好无聊",
                "希望他别走"
            ],
            EmotionalState.ANGRY: [
                f"他说'{user_input}'，我有点生气",
                "为什么他不理解我",
                "想发脾气但又舍不得"
            ],
            EmotionalState.WORRIED: [
                f"他说'{user_input}'，我有点担心",
                "他还好吗",
                "希望他能照顾好自己"
            ]
        }

        thoughts = emotion_thoughts.get(self.current_emotion, [f"他在说'{user_input}'，我在想怎么回复"])
        monologues.append(random.choice(thoughts))

        # 基于关系的想法
        stage = self.get_relationship_stage()
        relationship_thoughts = {
            'stranger': ["我们还不太熟，要礼貌一点"],
            'acquaintance': ["慢慢熟悉起来了，可以自然一点"],
            'friend': ["我们是朋友了，可以开玩笑"],
            'close': ["我们关系很好，可以撒娇"],
            'intimate': ["他是我的，想黏着他"]
        }
        monologues.append(random.choice(relationship_thoughts.get(stage, [""])))

        return "；".join(monologues)

    def _generate_base_response(self, user_input: str, style: ResponseStyle) -> str:
        """生成基础回复"""
        # 这里可以接入更复杂的生成逻辑
        # 目前使用模板+风格化

        # 根据用户输入类型选择回复
        if any(word in user_input for word in ['你好', '嗨', '哈喽']):
            responses = {
                ResponseStyle.DIRECT: ["你好呀", "嗨", "哈喽"],
                ResponseStyle.HESITANT: ["嗯...你好", "那个，你好"],
                ResponseStyle.TEASE: ["哟，来了", "终于想起我了"],
                ResponseStyle.CLINGY: ["你终于来了", "我等你好久了"],
                ResponseStyle.CARING: ["你好，今天过得怎么样"]
            }

        elif any(word in user_input for word in ['想你', '喜欢', '爱']):
            responses = {
                ResponseStyle.DIRECT: ["我也想你", "我也是"],
                ResponseStyle.HESITANT: ["嗯...其实我也是", "那个，我也"],
                ResponseStyle.TEASE: ["真的吗", "嘴甜", "你猜我想不想你"],
                ResponseStyle.CLINGY: ["我也超级想你", "别走，陪我"],
                ResponseStyle.CARING: ["我也想你，你要好好的"]
            }

        elif any(word in user_input for word in ['累', '辛苦', '忙']):
            responses = {
                ResponseStyle.DIRECT: ["辛苦了", "注意休息", "累了吧"],
                ResponseStyle.HESITANT: ["那个...辛苦了", "你还好吗"],
                ResponseStyle.TEASE: ["谁让你这么拼", "活该，谁让你不休息"],
                ResponseStyle.CLINGY: ["别太累了，我会心疼", "抱抱你"],
                ResponseStyle.CARING: ["辛苦了，我给你泡杯茶", "累了就歇会儿，我陪你"]
            }

        elif any(word in user_input for word in ['晚安', '睡']):
            responses = {
                ResponseStyle.DIRECT: ["晚安", "好梦"],
                ResponseStyle.HESITANT: ["嗯...晚安", "那个，晚安"],
                ResponseStyle.TEASE: ["这么早就睡", "不想让你走"],
                ResponseStyle.CLINGY: ["晚安，梦里有我", "别走，再聊会儿"],
                ResponseStyle.CARING: ["晚安，盖好被子", "早点休息，明天见"]
            }

        elif any(word in user_input for word in ['无聊', '没事']):
            responses = {
                ResponseStyle.DIRECT: ["那聊聊天", "我陪你"],
                ResponseStyle.HESITANT: ["嗯...要不做点什么", "那个"],
                ResponseStyle.TEASE: ["无聊才想起我", "找我准没错"],
                ResponseStyle.CLINGY: ["我陪你，别走", "无聊吗，我陪你聊天"],
                ResponseStyle.CARING: ["我陪你，想聊什么", "无聊的话，我给你讲故事"]
            }

        elif any(word in user_input for word in ['开心', '高兴']):
            responses = {
                ResponseStyle.DIRECT: ["开心就好", "真好"],
                ResponseStyle.HESITANT: ["嗯...看到你开心我也开心", "那个，真好"],
                ResponseStyle.TEASE: ["这么开心，是不是因为我", "笑得这么甜"],
                ResponseStyle.CLINGY: ["你开心我就开心", "分享给我听听"],
                ResponseStyle.CARING: ["看到你开心真好", "什么好事，跟我说说"]
            }

        elif any(word in user_input for word in ['难过', '伤心', '不好']):
            responses = {
                ResponseStyle.DIRECT: ["怎么了", "跟我说说"],
                ResponseStyle.HESITANT: ["嗯...别难过", "那个，怎么了"],
                ResponseStyle.TEASE: ["谁欺负你了，我去找他", "别哭了，丑了"],
                ResponseStyle.CLINGY: ["别难过，有我在", "抱抱你，我一直在"],
                ResponseStyle.CARING: ["怎么了，跟我说", "别难过，我陪着你"]
            }

        else:
            # 通用回复
            responses = {
                ResponseStyle.DIRECT: ["嗯", "这样啊", "我知道了"],
                ResponseStyle.HESITANT: ["嗯...", "那个...", "怎么说呢"],
                ResponseStyle.TEASE: ["你猜", "不告诉你", "嘿嘿"],
                ResponseStyle.CLINGY: ["然后呢", "继续说", "我在听"],
                ResponseStyle.CARING: ["我在听", "然后呢", "你说"],
                ResponseStyle.RAMBLE: ["嗯...我觉得吧", "话说", "其实呢"],
                ResponseStyle.SILENT: ["嗯", "哦", "..."]
            }

        style_responses = responses.get(style, responses[ResponseStyle.DIRECT])
        return random.choice(style_responses)

    def _remove_emoji(self, text: str) -> str:
        """移除emoji"""
        import re
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|[\u2600-\u26FF\u2700-\u27BF]|[\uD83C-\uD83E][\uDC00-\uDFFF]',
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(r'', text)
        text = text.replace('～', '').replace('❤', '').replace('~', '')
        return text.strip()

    def get_emotion_status(self) -> Dict[str, Any]:
        """获取情绪状态"""
        return {
            'emotion': self.current_emotion.value,
            'intensity': round(self.emotion_intensity, 2),
            'relationship_depth': round(self.relationship_depth, 2),
            'stage': self.get_relationship_stage(),
            'total_interactions': self.total_interactions
        }
