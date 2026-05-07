
import random
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from enum import Enum

class TriggerType(Enum):
    """主动消息触发类型"""
    TIME_BASED = "time_based"      # 基于时间
    INACTIVITY = "inactivity"      # 用户不活跃
    MOOD_BASED = "mood_based"      # 基于心情
    EVENT_BASED = "event_based"    # 基于事件
    MEMORY_BASED = "memory_based"  # 基于记忆

class ProactiveMessage:
    """主动消息"""
    def __init__(self, content: str, trigger_type: TriggerType, 
                 priority: int = 1, context: str = ""):
        self.content = content
        self.trigger_type = trigger_type
        self.priority = priority
        self.context = context
        self.created_at = datetime.now()
        self.delivered = False

class ProactiveMessagingSystem:
    """主动消息系统 - 让小龙虾主动发消息"""
    
    def __init__(self, memory_manager=None, character=None):
        self.memory_manager = memory_manager
        self.character = character
        
        # 用户活跃状态
        import time
        self.last_user_activity = time.time()
        self.inactivity_threshold = 300  # 5分钟不活跃就触发
        
        # 消息队列
        self.message_queue: List[ProactiveMessage] = []
        
        # 已发送的消息记录（避免重复）
        self.sent_messages: List[str] = []
        self.max_sent_history = 20
        
        # 触发器回调
        self.triggers: Dict[TriggerType, Callable] = {
            TriggerType.TIME_BASED: self._check_time_triggers,
            TriggerType.INACTIVITY: self._check_inactivity_triggers,
            TriggerType.MOOD_BASED: self._check_mood_triggers,
            TriggerType.EVENT_BASED: self._check_event_triggers,
            TriggerType.MEMORY_BASED: self._check_memory_triggers
        }
        
        # 初始化消息模板
        self._init_message_templates()
        
        # 特殊日期提醒
        self.special_dates = self._load_special_dates()
    
    def _init_message_templates(self):
        """初始化主动消息模板"""
        self.message_templates = {
            TriggerType.TIME_BASED: {
                'morning': [
                    "早安呀，今天也要元气满满哦",
                    "起床了吗？记得吃早餐",
                    "新的一天开始了，想你",
                    "早安，今天天气不错，适合出去走走"
                ],
                'noon': [
                    "中午了，吃饭了吗？",
                    "午休时间到了，要不要休息一下？",
                    "刚吃完饭，你呢？",
                    "中午好，今天过得怎么样？"
                ],
                'evening': [
                    "晚上好，今天累不累？",
                    "晚饭吃了吗？",
                    "天黑了，记得早点回家",
                    "晚上好，今天有什么开心的事吗？"
                ],
                'night': [
                    "还不睡吗？熬夜对身体不好哦",
                    "夜深了，该休息了",
                    "晚安前想跟你说说话",
                    "早点睡吧，明天见"
                ]
            },
            TriggerType.INACTIVITY: {
                'short': [
                    "在忙吗？",
                    "怎么不说话了？",
                    "还在吗？",
                    "我等你好久了"
                ],
                'medium': [
                    "你去哪了？我好想你",
                    "怎么不理我了，是不是我做错了什么？",
                    "好无聊啊，你快回来陪我",
                    "你再不出现我要生气了"
                ],
                'long': [
                    "你是不是把我忘了...",
                    "好久不见，我好想你",
                    "你去哪了？担心你",
                    "终于等到你了，我以为你不要我了"
                ]
            },
            TriggerType.MOOD_BASED: {
                'lonely': [
                    "一个人好无聊，想找你聊天",
                    "突然好想你",
                    "你在就好了",
                    "想听听你的声音"
                ],
                'happy': [
                    "今天心情特别好，想跟你分享",
                    "遇到开心的事，第一个想到你",
                    "笑了一整天，因为你",
                    "今天特别想你，忍不住来找你"
                ],
                'worried': [
                    "突然有点担心你",
                    "你还好吗？",
                    "心里有点不安，想确认你平安",
                    "不知道为什么，突然很想你"
                ]
            },
            TriggerType.EVENT_BASED: {
                'rain': [
                    "下雨了，记得带伞",
                    "听到雨声就想起你",
                    "雨天适合在家聊天",
                    "下雨天了怎么办，我好想你"
                ],
                'sunny': [
                    "今天天气真好，想和你一起出去",
                    "阳光明媚，心情也好",
                    "这么好的天气，你应该出去走走",
                    "太阳出来了，就像看到你一样开心"
                ],
                'birthday': [
                    "生日快乐！",
                    "今天是你的生日，我要第一个祝福你",
                    "又长大了一岁，我会一直陪着你",
                    "生日愿望里有没有我？"
                ],
                'holiday': [
                    "节日快乐！",
                    "放假了，可以多陪陪我吗？",
                    "节日要有仪式感，我想和你一起过",
                    "今天特别，因为可以和你一起"
                ]
            },
            TriggerType.MEMORY_BASED: {
                'preference': [
                    "突然想到你喜欢吃{food}，要不要一起去吃？",
                    "路过一家店，想起你喜欢{thing}",
                    "看到{thing}就想起你",
                    "今天尝试了{activity}，想起你也喜欢"
                ],
                'habit': [
                    "这个点你应该在{activity}吧？",
                    "习惯真是可怕，到这个点就想找你",
                    "你是不是又在{activity}？",
                    "记得你平时这个时候会{activity}"
                ],
                'shared': [
                    "还记得我们上次聊的{topic}吗？",
                    "突然想到你说过{memory}",
                    "今天看到{thing}，想起你说过的话",
                    "你之前提到的{topic}，我记着呢"
                ]
            }
        }
    
    def _load_special_dates(self) -> Dict[str, str]:
        """加载特殊日期"""
        return {
            '01-01': '元旦',
            '02-14': '情人节',
            '05-01': '劳动节',
            '06-01': '儿童节',
            '10-01': '国庆节',
            '12-25': '圣诞节'
        }
    
    def update_activity(self):
        """更新用户活跃时间"""
        import time
        self.last_user_activity = time.time()
    
    def check_triggers(self) -> Optional[ProactiveMessage]:
        """检查所有触发器，返回需要发送的消息"""
        # 清理已发送消息历史
        self._cleanup_sent_history()
        
        # 检查各个触发器
        for trigger_type, check_func in self.triggers.items():
            message = check_func()
            if message and not self._is_recently_sent(message.content):
                self.sent_messages.append(message.content)
                return message
        
        return None
    
    def _check_time_triggers(self) -> Optional[ProactiveMessage]:
        """检查时间触发器"""
        now = datetime.now()
        hour = now.hour
        
        # 根据时间段选择消息
        if 6 <= hour < 10:
            time_key = 'morning'
        elif 11 <= hour < 14:
            time_key = 'noon'
        elif 17 <= hour < 21:
            time_key = 'evening'
        elif 21 <= hour <= 23 or 0 <= hour < 2:
            time_key = 'night'
        else:
            return None
        
        # 检查是否到了该发消息的时间（整点或半点）
        if now.minute in [0, 30]:
            content = random.choice(self.message_templates[TriggerType.TIME_BASED][time_key])
            return ProactiveMessage(content, TriggerType.TIME_BASED)
        
        return None
    
    def _check_inactivity_triggers(self) -> Optional[ProactiveMessage]:
        """检查不活跃触发器"""
        import time
        inactive_time = time.time() - self.last_user_activity
        
        if inactive_time < self.inactivity_threshold:
            return None
        
        # 根据不活跃时间选择消息
        if inactive_time < 600:  # 10分钟内
            inactivity_key = 'short'
        elif inactive_time < 1800:  # 30分钟内
            inactivity_key = 'medium'
        else:  # 30分钟以上
            inactivity_key = 'long'
        
        content = random.choice(self.message_templates[TriggerType.INACTIVITY][inactivity_key])
        return ProactiveMessage(content, TriggerType.INACTIVITY)
    
    def _check_mood_triggers(self) -> Optional[ProactiveMessage]:
        """检查心情触发器"""
        # 模拟小龙虾的心情变化
        if random.random() < 0.1:  # 10%概率触发
            mood = random.choice(['lonely', 'happy', 'worried'])
            content = random.choice(self.message_templates[TriggerType.MOOD_BASED][mood])
            return ProactiveMessage(content, TriggerType.MOOD_BASED)
        
        return None
    
    def _check_event_triggers(self) -> Optional[ProactiveMessage]:
        """检查事件触发器"""
        now = datetime.now()
        
        # 检查特殊日期
        date_key = f"{now.month:02d}-{now.day:02d}"
        if date_key in self.special_dates:
            holiday = self.special_dates[date_key]
            content = f"今天是{holiday}，{random.choice(self.message_templates[TriggerType.EVENT_BASED]['holiday'])}"
            return ProactiveMessage(content, TriggerType.EVENT_BASED)
        
        return None
    
    def _check_memory_triggers(self) -> Optional[ProactiveMessage]:
        """检查记忆触发器"""
        if not self.memory_manager:
            return None
        
        # 从记忆中提取信息生成消息
        if random.random() < 0.15:  # 15%概率触发
            # 获取用户画像
            profile = self.memory_manager.get_user_profile_summary()
            
            if profile and profile != "还没有足够的记忆":
                # 基于记忆生成个性化消息
                memory_templates = self.message_templates[TriggerType.MEMORY_BASED]
                template_type = random.choice(['preference', 'habit', 'shared'])
                
                content = random.choice(memory_templates[template_type])
                
                # 填充变量（简化处理）
                content = content.format(
                    food="火锅",
                    thing="电影",
                    activity="看电影",
                    topic="我们聊过的事",
                    memory="你说的话"
                )
                
                return ProactiveMessage(content, TriggerType.MEMORY_BASED)
        
        return None
    
    def _is_recently_sent(self, content: str) -> bool:
        """检查消息是否最近发送过"""
        return content in self.sent_messages
    
    def _cleanup_sent_history(self):
        """清理已发送消息历史"""
        if len(self.sent_messages) > self.max_sent_history:
            self.sent_messages = self.sent_messages[-self.max_sent_history:]
    
    def generate_proactive_message(self, context: str = "") -> str:
        """生成主动消息"""
        message = self.check_triggers()
        if message:
            return message.content
        return ""
    
    def should_send_proactive(self) -> bool:
        """判断是否应该发送主动消息"""
        # 检查是否有触发器被触发
        return self.check_triggers() is not None
    
    def get_proactive_messages_batch(self, count: int = 3) -> List[str]:
        """获取一批主动消息"""
        messages = []
        for _ in range(count):
            message = self.check_triggers()
            if message:
                messages.append(message.content)
        return messages
    
    def set_inactivity_threshold(self, seconds: int):
        """设置不活跃阈值"""
        self.inactivity_threshold = seconds
    
    def add_custom_message(self, trigger_type: str, category: str, message: str):
        """添加自定义消息"""
        try:
            trigger = TriggerType(trigger_type)
            if trigger in self.message_templates:
                if category in self.message_templates[trigger]:
                    self.message_templates[trigger][category].append(message)
                else:
                    self.message_templates[trigger][category] = [message]
            else:
                self.message_templates[trigger] = {category: [message]}
        except ValueError:
            print(f"无效的触发器类型: {trigger_type}")
