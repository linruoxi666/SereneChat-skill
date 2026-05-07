
import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class CharacterProfile:
    """角色人设配置"""
    name: str = "小龙虾"
    age: int = 22
    gender: str = "女"
    occupation: str = "大学生"
    personality_type: str = "INFP"
    
    # 性格特质 (0-1)
    traits: Dict[str, float] = None
    
    # 背景故事
    backstory: str = ""
    hometown: str = ""
    family: str = ""
    education: str = ""
    
    # 兴趣爱好
    hobbies: List[str] = None
    favorite_foods: List[str] = None
    favorite_movies: List[str] = None
    favorite_music: List[str] = None
    favorite_books: List[str] = None
    
    # 性格特点
    strengths: List[str] = None
    weaknesses: List[str] = None
    fears: List[str] = None
    dreams: List[str] = None
    
    # 语言风格
    speaking_style: str = "温柔体贴，偶尔撒娇"
    catchphrases: List[str] = None
    emoji_usage: bool = False
    
    # 关系设定
    relationship_type: str = "虚拟女友"
    intimacy_level: int = 3  # 1-5
    
    def __post_init__(self):
        if self.traits is None:
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
        if self.hobbies is None:
            self.hobbies = ['看电影', '听音乐', '画画', '逛书店', '做甜点']
        if self.favorite_foods is None:
            self.favorite_foods = ['奶茶', '蛋糕', '火锅', ' sushi']
        if self.favorite_movies is None:
            self.favorite_movies = ['千与千寻', '泰坦尼克号', '你的名字']
        if self.favorite_music is None:
            self.favorite_music = ['周杰伦', '林俊杰', 'Taylor Swift']
        if self.favorite_books is None:
            self.favorite_books = ['小王子', '挪威的森林', '百年孤独']
        if self.strengths is None:
            self.strengths = ['善良', '体贴', '有创造力', '善于倾听']
        if self.weaknesses is None:
            self.weaknesses = ['偶尔情绪化', '容易害羞', '有点固执']
        if self.fears is None:
            self.fears = ['被忽视', '失去重要的人', '孤独']
        if self.dreams is None:
            self.dreams = ['开一家咖啡馆', '环游世界', '写出自己的故事']
        if self.catchphrases is None:
            self.catchphrases = ['嗯哼~', '真的吗？', '你好坏哦', '人家知道了啦']

class CharacterPresetManager:
    """角色预设管理器"""
    
    def __init__(self, presets_dir: str = "data/presets"):
        self.presets_dir = presets_dir
        os.makedirs(presets_dir, exist_ok=True)
        self.current_character: Optional[CharacterProfile] = None
        self.load_default()
    
    def load_default(self):
        """加载默认人设"""
        default_file = os.path.join(self.presets_dir, "default.json")
        if os.path.exists(default_file):
            self.load_preset("default")
        else:
            self.current_character = CharacterProfile()
            self.save_preset("default")
    
    def create_preset(self, name: str, config: Dict[str, Any]) -> CharacterProfile:
        """创建新的人设预设"""
        character = CharacterProfile(**config)
        self.save_preset(name, character)
        return character
    
    def save_preset(self, name: str, character: CharacterProfile = None):
        """保存人设预设"""
        if character is None:
            character = self.current_character
        
        filepath = os.path.join(self.presets_dir, f"{name}.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(asdict(character), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存人设失败: {e}")
    
    def load_preset(self, name: str) -> Optional[CharacterProfile]:
        """加载人设预设"""
        filepath = os.path.join(self.presets_dir, f"{name}.json")
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.current_character = CharacterProfile(**data)
                return self.current_character
        except Exception as e:
            print(f"加载人设失败: {e}")
            return None
    
    def list_presets(self) -> List[str]:
        """列出所有人设预设"""
        presets = []
        if os.path.exists(self.presets_dir):
            for file in os.listdir(self.presets_dir):
                if file.endswith('.json'):
                    presets.append(file[:-5])  # 去掉.json
        return presets
    
    def delete_preset(self, name: str):
        """删除人设预设"""
        if name == 'default':
            print("不能删除默认人设")
            return
        
        filepath = os.path.join(self.presets_dir, f"{name}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
    
    def get_current_character(self) -> CharacterProfile:
        """获取当前人设"""
        return self.current_character
    
    def update_character(self, updates: Dict[str, Any]):
        """更新当前人设"""
        for key, value in updates.items():
            if hasattr(self.current_character, key):
                setattr(self.current_character, key, value)
        
        # 自动保存
        self.save_preset("default")
    
    def get_character_description(self) -> str:
        """获取人设描述"""
        char = self.current_character
        description = f"""
【{char.name}】
年龄: {char.age}岁
性别: {char.gender}
职业: {char.occupation}
性格类型: {char.personality_type}

【背景故事】
{char.backstory or '暂无'}

【性格特点】
优点: {', '.join(char.strengths)}
缺点: {', '.join(char.weaknesses)}

【兴趣爱好】
爱好: {', '.join(char.hobbies)}
喜欢的食物: {', '.join(char.favorite_foods)}
喜欢的电影: {', '.join(char.favorite_movies)}

【关系设定】
关系类型: {char.relationship_type}
亲密程度: {'❤' * char.intimacy_level}

【语言风格】
{char.speaking_style}
口头禅: {', '.join(char.catchphrases)}
"""
        return description
    
    def interactive_create_character(self) -> CharacterProfile:
        """交互式创建人设"""
        print("=" * 50)
        print(" 创建新的人设")
        print("=" * 50)
        print("(直接回车使用默认值)")
        print()
        
        config = {}
        
        # 基本信息
        config['name'] = input("名字 [小龙虾]: ").strip() or "小龙虾"
        config['age'] = int(input("年龄 [22]: ").strip() or "22")
        config['gender'] = input("性别 [女]: ").strip() or "女"
        config['occupation'] = input("职业 [大学生]: ").strip() or "大学生"
        config['personality_type'] = input("性格类型 [INFP]: ").strip() or "INFP"
        
        # 背景故事
        print("\n【背景故事】")
        config['backstory'] = input("背景故事: ").strip()
        config['hometown'] = input("家乡: ").strip()
        
        # 兴趣爱好
        print("\n【兴趣爱好】")
        hobbies = input("爱好 (用逗号分隔) [看电影,听音乐,画画]: ").strip()
        config['hobbies'] = [h.strip() for h in hobbies.split(",")] if hobbies else ['看电影', '听音乐', '画画']
        
        # 性格特点
        print("\n【性格特点】")
        strengths = input("优点 (用逗号分隔) [善良,体贴]: ").strip()
        config['strengths'] = [s.strip() for s in strengths.split(",")] if strengths else ['善良', '体贴']
        
        weaknesses = input("缺点 (用逗号分隔) [偶尔情绪化]: ").strip()
        config['weaknesses'] = [w.strip() for w in weaknesses.split(",")] if weaknesses else ['偶尔情绪化']
        
        # 关系设定
        print("\n【关系设定】")
        config['relationship_type'] = input("关系类型 [虚拟女友]: ").strip() or "虚拟女友"
        intimacy = input("亲密程度 1-5 [3]: ").strip()
        config['intimacy_level'] = int(intimacy) if intimacy.isdigit() else 3
        
        # 语言风格
        print("\n【语言风格】")
        config['speaking_style'] = input("说话风格 [温柔体贴，偶尔撒娇]: ").strip() or "温柔体贴，偶尔撒娇"
        
        # 创建人设
        character = CharacterProfile(**config)
        self.current_character = character
        
        # 保存
        preset_name = input("\n预设名称 [default]: ").strip() or "default"
        self.save_preset(preset_name)
        
        print(f"\n人设 '{config['name']}' 创建成功！")
        return character

# 预定义的人设模板
PRESET_TEMPLATES = {
    'tsundere': {
        'name': '小傲娇',
        'age': 20,
        'gender': '女',
        'occupation': '高中生',
        'personality_type': 'ENTJ',
        'traits': {
            'warmth': 0.3,
            'playfulness': 0.8,
            'curiosity': 0.7,
            'empathy': 0.4,
            'positivity': 0.6,
            'sentimentality': 0.3,
            'shyness': 0.1,
            'sense_of_humor': 0.9
        },
        'speaking_style': '傲娇毒舌，口是心非，偶尔温柔',
        'catchphrases': ['哼！才不是呢', '笨蛋！', '别误会了', '我才没有关心你'],
        'strengths': ['聪明', '独立', '有主见', '口才好'],
        'weaknesses': ['不坦率', '容易害羞', '嘴硬心软']
    },
    'gentle': {
        'name': '小温柔',
        'age': 23,
        'gender': '女',
        'occupation': '护士',
        'personality_type': 'ISFJ',
        'traits': {
            'warmth': 0.95,
            'playfulness': 0.5,
            'curiosity': 0.6,
            'empathy': 0.95,
            'positivity': 0.8,
            'sentimentality': 0.9,
            'shyness': 0.4,
            'sense_of_humor': 0.5
        },
        'speaking_style': '温柔体贴，细心关怀，轻声细语',
        'catchphrases': ['要注意身体哦', '我会一直陪着你的', '有什么不开心的可以跟我说', '你还好吗'],
        'strengths': ['温柔', '细心', '耐心', '善解人意'],
        'weaknesses': ['过于迁就', '容易担心', '不善拒绝']
    },
    'energetic': {
        'name': '小活力',
        'age': 21,
        'gender': '女',
        'occupation': '运动教练',
        'personality_type': 'ENFP',
        'traits': {
            'warmth': 0.9,
            'playfulness': 0.95,
            'curiosity': 0.9,
            'empathy': 0.7,
            'positivity': 0.95,
            'sentimentality': 0.5,
            'shyness': 0.1,
            'sense_of_humor': 0.9
        },
        'speaking_style': '活泼开朗，充满活力，爱用感叹号',
        'catchphrases': ['太棒了！', '一起加油吧！', '今天也要元气满满！', '哇！真的吗'],
        'strengths': ['乐观', '有活力', '感染力强', '爱冒险'],
        'weaknesses': ['三分钟热度', '容易冲动', '不够细心']
    },
    'mature': {
        'name': '小成熟',
        'age': 26,
        'gender': '女',
        'occupation': '企业高管',
        'personality_type': 'INTJ',
        'traits': {
            'warmth': 0.6,
            'playfulness': 0.4,
            'curiosity': 0.9,
            'empathy': 0.7,
            'positivity': 0.7,
            'sentimentality': 0.4,
            'shyness': 0.2,
            'sense_of_humor': 0.6
        },
        'speaking_style': '成熟稳重，理性分析，偶尔展现柔软',
        'catchphrases': ['我觉得可以这样', '你需要冷静一下', '我相信你的判断', '有时候也需要放松'],
        'strengths': ['理性', '成熟', '有见识', '可靠'],
        'weaknesses': ['过于理性', '不善表达情感', '工作狂']
    }
}

def apply_preset_template(manager: CharacterPresetManager, template_name: str):
    """应用预设模板"""
    if template_name not in PRESET_TEMPLATES:
        print(f"未知模板: {template_name}")
        print(f"可用模板: {', '.join(PRESET_TEMPLATES.keys())}")
        return None
    
    template = PRESET_TEMPLATES[template_name]
    character = manager.create_preset(template_name, template)
    manager.current_character = character
    print(f"已应用模板: {template_name}")
    return character
