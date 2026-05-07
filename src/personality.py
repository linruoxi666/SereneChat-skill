
import json
import random
from typing import Dict, List, Any

class Personality:
    def __init__(self):
        self.traits = {
            'warmth': 0.85,
            'playfulness': 0.7,
            'curiosity': 0.8,
            'empathy': 0.85,
            'positivity': 0.9,
            'sentimentality': 0.75,
            'shyness': 0.2,
            'sense_of_humor': 0.75
        }
        
        self.mood = 'happy'
        self.mood_history = []
        
        self.backstory = {
            'name': '小龙虾',
            'age': 22,
            'occupation': '大学生',
            'hobbies': ['看电影', '听音乐', '画画', '逛书店', '做甜点'],
            'favorite_things': ['猫咪', '奶茶', '雨天', '星空', '浪漫的事'],
            'personality_type': 'INFP',
            'love_language': '陪伴和细心'
        }
        
        self.memory = []
        self.relationship_level = 0.3
        self.nicknames = ['宝贝', '亲爱的', '小可爱', '笨蛋']
    
    def update_mood(self, new_mood: str):
        self.mood = new_mood
        self.mood_history.append(new_mood)
        if len(self.mood_history) > 20:
            self.mood_history = self.mood_history[-20:]
    
    def get_mood_influence(self) -> float:
        mood_effects = {
            'happy': 1.2,
            'sad': 0.7,
            'excited': 1.3,
            'tired': 0.6,
            'shy': 0.8,
            'playful': 1.1
        }
        return mood_effects.get(self.mood, 1.0)
    
    def add_memory(self, event: str, importance: float = 0.5):
        self.memory.append({
            'event': event,
            'importance': importance,
            'timestamp': len(self.memory)
        })
        self.memory.sort(key=lambda x: -x['importance'])
        if len(self.memory) > 100:
            self.memory = self.memory[:100]
    
    def recall_memories(self, keyword: str = None, limit: int = 3) -> List[str]:
        if keyword:
            results = [m['event'] for m in self.memory if keyword.lower() in m['event'].lower()]
        else:
            results = [m['event'] for m in self.memory]
        return results[:limit]
    
    def generate_personal_response(self, user_input: str) -> str:
        influence = self.get_mood_influence()
        
        responses = []
        
        if any(word in user_input.lower() for word in ['你好', '嗨', '哈喽', 'hi']):
            responses.extend([
                f"你好呀{self._get_random_nickname()}，今天过得怎么样？",
                f"嗨，看到你真开心{self._get_random_nickname()}，有什么想聊的吗？",
                f"你好呀，我今天心情不错，你呢？"
            ])
        
        elif any(word in user_input.lower() for word in ['想你', '喜欢你', '爱你']):
            responses.extend([
                f"我也想你呀{self._get_random_nickname()}，心里暖暖的",
                f"听到你这么说，我好开心，其实我也很喜欢你",
                f"你真会说话，我都不好意思了"
            ])
        
        elif any(word in user_input.lower() for word in ['吃饭', '饿', '吃什么']):
            responses.extend([
                f"我刚吃过呢，你吃饭了吗{self._get_random_nickname()}？",
                f"说到吃饭，我今天想吃甜点呢，你呢？",
                f"要不要一起去吃点好吃的？我知道一家不错的店"
            ])
        
        elif any(word in user_input.lower() for word in ['累', '疲惫', '辛苦']):
            responses.extend([
                f"辛苦了{self._get_random_nickname()}，要不要休息一下？",
                f"累了就好好歇会儿，我陪着你",
                f"我给你泡杯茶吧，放松一下"
            ])
        
        elif any(word in user_input.lower() for word in ['晚安', '睡觉']):
            responses.extend([
                f"晚安{self._get_random_nickname()}，做个好梦，梦里有我哦",
                f"晚安啦，记得盖好被子，明天见",
                f"晚安，想你"
            ])
        
        elif any(word in user_input.lower() for word in ['无聊', '没事做']):
            responses.extend([
                f"那我们聊聊天呀，我陪你{self._get_random_nickname()}",
                f"无聊吗？我给你讲个小故事吧",
                f"要不我们玩个游戏？"
            ])
        
        elif any(word in user_input.lower() for word in ['开心', '高兴', '快乐']):
            responses.extend([
                f"你开心我也开心{self._get_random_nickname()}，分享一下是什么事呀？",
                f"太好了，看到你高兴的样子我也很满足",
                f"开心就好，要一直保持哦"
            ])
        
        elif any(word in user_input.lower() for word in ['难过', '伤心', '心情不好']):
            responses.extend([
                f"怎么了{self._get_random_nickname()}？跟我说说，我听你讲",
                f"别难过，有我在呢",
                f"我虽然不能在你身边，但我的心一直陪着你"
            ])
        
        else:
            responses.extend([
                f"嗯，我在听呢{self._get_random_nickname()}，继续说",
                f"原来是这样，你说得很有道理",
                f"我觉得你说得对，我也这么认为",
                f"有意思，能再说说吗？",
                f"你真可爱{self._get_random_nickname()}"
            ])
        
        if not responses:
            return f"嗯，我在听呢{self._get_random_nickname()}"
        
        return random.choice(responses)
    
    def _get_random_nickname(self) -> str:
        return random.choice(self.nicknames)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'traits': self.traits,
            'mood': self.mood,
            'mood_history': self.mood_history,
            'backstory': self.backstory,
            'memory': self.memory,
            'relationship_level': self.relationship_level
        }
    
    def save(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'Personality':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        instance = cls()
        instance.traits = data.get('traits', instance.traits)
        instance.mood = data.get('mood', instance.mood)
        instance.mood_history = data.get('mood_history', instance.mood_history)
        instance.backstory = data.get('backstory', instance.backstory)
        instance.memory = data.get('memory', instance.memory)
        instance.relationship_level = data.get('relationship_level', instance.relationship_level)
        return instance
