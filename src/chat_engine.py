
import random
import re
import os
from typing import List, Dict, Any, Optional
from .personality import Personality
from .chat_parser import ChatRecord, ChatParser
from .ocr_chat_parser import OCRChatParser, ChatPlatform
from .content_moderation import ContentModerator, RiskLevel
from .memory_system import MemoryManager
from .character_preset import CharacterPresetManager, apply_preset_template
from .proactive_messaging import ProactiveMessagingSystem
from .humanized_response import HumanizedResponseEngine

class ChatEngine:
    def __init__(self):
        self.personality = Personality()
        self.chat_history = []
        self.context_window = 10
        self.last_input = ""
        self.last_response = ""
        self.ocr_parser = OCRChatParser()
        self.moderator = ContentModerator()
        self.violation_count = 0
        self.max_violations = 3

        # 新增：记忆系统
        self.memory_manager = MemoryManager()

        # 新增：人设管理
        self.character_manager = CharacterPresetManager()
        self.current_character = self.character_manager.get_current_character()

        # 新增：主动消息系统
        self.proactive_system = ProactiveMessagingSystem(
            memory_manager=self.memory_manager,
            character=self.current_character
        )

        # 新增：真人化回复引擎
        self.humanized_engine = HumanizedResponseEngine(
            memory_manager=self.memory_manager,
            character=self.current_character
        )

        # 是否启用真人化模式
        self.humanized_mode = True
    
    def chat(self, user_input: str) -> str:
        self.last_input = user_input
        
        # 内容风控检查
        risk_level, triggered_words, details = self.moderator.check_text(user_input)
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            self.violation_count += 1
            warning = self.moderator.get_warning_message(risk_level)
            
            if self.violation_count >= self.max_violations:
                return "由于多次违规，你已被临时禁言。请反思自己的行为。"
            
            return f"{warning} (违规次数: {self.violation_count}/{self.max_violations})"
        
        elif risk_level == RiskLevel.MEDIUM:
            warning = self.moderator.get_warning_message(risk_level)
        
        # 获取增强的上下文（包含记忆）
        enriched_context = self.memory_manager.get_enriched_context(user_input)

        context = self._build_context()

        # 使用真人化回复引擎生成回复
        if self.humanized_mode:
            response, internal_monologue = self.humanized_engine.generate_response(user_input, context)
        else:
            response = self._generate_response(user_input, context, enriched_context)
            internal_monologue = ""

        # 检查生成的回复是否安全
        response_risk, _, _ = self.moderator.check_text(response)
        if response_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            response = "这个话题不太合适呢，我们聊点别的吧。"
        elif response_risk == RiskLevel.MEDIUM:
            response = self.moderator.filter_response(response)

        # 保存到记忆系统
        self.memory_manager.process_interaction(user_input, response)

        # 更新用户活跃时间
        self.proactive_system.update_activity()

        self.chat_history.append({
            'user': user_input,
            'bot': response
        })
        
        if len(self.chat_history) > 50:
            self.chat_history = self.chat_history[-50:]
        
        self.last_response = response
        return response
    
    def check_proactive_message(self) -> Optional[str]:
        """检查是否需要发送主动消息"""
        message = self.proactive_system.check_triggers()
        if message:
            return message.content
        return None
    
    def get_proactive_message(self) -> str:
        """获取主动消息（用于定时调用）"""
        return self.proactive_system.generate_proactive_message()
    
    def _build_context(self) -> str:
        context = ""
        for i, entry in enumerate(reversed(self.chat_history[-self.context_window:])):
            context = f"用户: {entry['user']}\n小龙虾: {entry['bot']}\n" + context
        return context
    
    def _generate_response(self, user_input: str, context: str, enriched_context: str = "") -> str:
        # 使用人设信息生成回复
        character = self.current_character
        
        # 基于人设的个性化回复
        if any(word in user_input.lower() for word in ['你好', '嗨', '哈喽', 'hi']):
            return self._generate_greeting(character)
        
        elif any(word in user_input.lower() for word in ['想你', '喜欢你', '爱你']):
            return self._generate_affection_response(character)
        
        elif any(word in user_input.lower() for word in ['吃饭', '饿', '吃什么']):
            return self._generate_food_response(character)
        
        elif any(word in user_input.lower() for word in ['累', '疲惫', '辛苦']):
            return self._generate_comfort_response(character)
        
        elif any(word in user_input.lower() for word in ['晚安', '睡觉']):
            return self._generate_goodnight_response(character)
        
        elif any(word in user_input.lower() for word in ['无聊', '没事做']):
            return self._generate_boredom_response(character)
        
        elif any(word in user_input.lower() for word in ['开心', '高兴', '快乐']):
            return self._generate_happy_response(character)
        
        elif any(word in user_input.lower() for word in ['难过', '伤心', '心情不好']):
            return self._generate_sad_response(character)
        
        else:
            # 使用默认人格回复
            personal_response = self.personality.generate_personal_response(user_input)
            
            if self._contains_emoji(personal_response):
                personal_response = self._remove_emoji(personal_response)
            
            return personal_response
    
    def _generate_greeting(self, character) -> str:
        """生成问候回复"""
        responses = [
            f"你好呀{self._get_random_nickname(character)}，今天过得怎么样？",
            f"嗨，看到你真开心{self._get_random_nickname(character)}，有什么想聊的吗？",
            f"你好呀，我今天心情不错，你呢？"
        ]
        return random.choice(responses)
    
    def _generate_affection_response(self, character) -> str:
        """生成情感回复"""
        responses = [
            f"我也想你呀{self._get_random_nickname(character)}，心里暖暖的",
            f"听到你这么说，我好开心，其实我也很喜欢你",
            f"你真会说话，我都不好意思了"
        ]
        return random.choice(responses)
    
    def _generate_food_response(self, character) -> str:
        """生成食物相关回复"""
        favorite_food = random.choice(character.favorite_foods) if character.favorite_foods else "好吃的"
        responses = [
            f"我刚吃过呢，你吃饭了吗{self._get_random_nickname(character)}？",
            f"说到吃饭，我今天想吃{favorite_food}呢，你呢？",
            f"要不要一起去吃点好吃的？我知道一家不错的店"
        ]
        return random.choice(responses)
    
    def _generate_comfort_response(self, character) -> str:
        """生成安慰回复"""
        responses = [
            f"辛苦了{self._get_random_nickname(character)}，要不要休息一下？",
            f"累了就好好歇会儿，我陪着你",
            f"我给你泡杯茶吧，放松一下"
        ]
        return random.choice(responses)
    
    def _generate_goodnight_response(self, character) -> str:
        """生成晚安回复"""
        responses = [
            f"晚安{self._get_random_nickname(character)}，做个好梦，梦里有我哦",
            f"晚安啦，记得盖好被子，明天见",
            f"晚安，想你"
        ]
        return random.choice(responses)
    
    def _generate_boredom_response(self, character) -> str:
        """生成无聊回复"""
        hobby = random.choice(character.hobbies) if character.hobbies else "聊天"
        responses = [
            f"那我们聊聊天呀，我陪你{self._get_random_nickname(character)}",
            f"无聊吗？我给你讲个小故事吧",
            f"要不我们一起{hobby}？"
        ]
        return random.choice(responses)
    
    def _generate_happy_response(self, character) -> str:
        """生成开心回复"""
        responses = [
            f"你开心我也开心{self._get_random_nickname(character)}，分享一下是什么事呀？",
            f"太好了，看到你高兴的样子我也很满足",
            f"开心就好，要一直保持哦"
        ]
        return random.choice(responses)
    
    def _generate_sad_response(self, character) -> str:
        """生成难过回复"""
        responses = [
            f"怎么了{self._get_random_nickname(character)}？跟我说说，我听你讲",
            f"别难过，有我在呢",
            f"我虽然不能在你身边，但我的心一直陪着你"
        ]
        return random.choice(responses)
    
    def _get_random_nickname(self, character) -> str:
        """获取随机昵称"""
        nicknames = ['宝贝', '亲爱的', '小可爱', '笨蛋']
        return random.choice(nicknames)
    
    def _contains_emoji(self, text: str) -> bool:
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|[\u2600-\u26FF\u2700-\u27BF]|[\uD83C-\uD83E][\uDC00-\uDFFF]',
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(text)) or any(c in text for c in ['^', '*', '▽', '❤', '～'])
    
    def _remove_emoji(self, text: str) -> str:
        emoji_pattern = re.compile(
            r'[\U00010000-\U0010ffff]|[\u2600-\u26FF\u2700-\u27BF]|[\uD83C-\uD83E][\uDC00-\uDFFF]',
            flags=re.UNICODE
        )
        text = emoji_pattern.sub(r'', text)
        ascii_emoji_pattern = re.compile(r'\(\*[\^▽\*]+\*\)')
        text = ascii_emoji_pattern.sub(r'', text)
        text = text.replace('～', '')
        text = text.replace('❤', '')
        text = text.replace('~', '')
        return text.strip()
    
    def import_chat_history(self, filepath: str) -> bool:
        try:
            records = ChatParser.parse_file(filepath)
            style_info = ChatParser.analyze_chat_style(records)

            for record in records:
                if record.sender != '小龙虾':
                    self.chat_history.append({
                        'user': record.content,
                        'bot': self._generate_response(record.content, "", "")
                    })

            # 根据导入的聊天记录设置关系深度（用户数据优先）
            if style_info:
                msg_count = style_info.get('total_messages', 0)
                # 基于聊天记录数量计算关系深度
                imported_depth = min(1.0, 0.3 + (msg_count / 100) * 0.7)
                # 同步到真人化引擎
                self.humanized_engine.relationship_depth = imported_depth
                self.humanized_engine.total_interactions = msg_count
                # 同步到人格系统
                self.personality.relationship_level = imported_depth

            return True
        except Exception:
            return False
    
    def import_chat_screenshot(self, image_path: str) -> bool:
        """导入聊天截图（OCR识别）"""
        try:
            if not os.path.exists(image_path):
                print(f"文件不存在: {image_path}")
                return False
            
            _, ext = os.path.splitext(image_path)
            if ext.lower() not in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                print(f"不支持的图片格式: {ext}")
                return False
            
            messages = self.ocr_parser.extract_chat_from_image(image_path)
            
            if not messages:
                print("未能从图片中识别到聊天内容")
                return False
            
            analysis = self.ocr_parser.analyze_chat_pattern(messages)
            print(f"识别到 {analysis['total_messages']} 条消息，来自 {analysis['unique_senders']} 个发送者")
            print(f"平台: {analysis['platform']}")
            
            for msg in messages:
                self.chat_history.append({
                    'user': msg.content,
                    'bot': self._generate_response(msg.content, "", "")
                })

            # 根据导入的截图聊天记录设置关系深度（用户数据优先）
            msg_count = analysis['total_messages']
            imported_depth = min(1.0, 0.3 + (msg_count / 100) * 0.7)
            self.humanized_engine.relationship_depth = imported_depth
            self.humanized_engine.total_interactions = msg_count
            self.personality.relationship_level = imported_depth

            return True
        
        except Exception as e:
            print(f"导入截图失败: {e}")
            return False
    
    def import_ocr_text(self, ocr_text: str) -> bool:
        """导入OCR识别后的文本"""
        try:
            messages = self.ocr_parser.parse_ocr_text(ocr_text)
            
            if not messages:
                print("未能从文本中解析到聊天内容")
                return False
            
            for msg in messages:
                self.chat_history.append({
                    'user': msg.content,
                    'bot': self._generate_response(msg.content, "", "")
                })
            
            return True
        except Exception as e:
            print(f"导入OCR文本失败: {e}")
            return False
    
    # 新增：人设相关功能
    def set_character(self, preset_name: str) -> bool:
        """设置当前人设"""
        character = self.character_manager.load_preset(preset_name)
        if character:
            self.current_character = character
            # 同步到真人化引擎
            self.humanized_engine.character = character
            return True
        return False

    def create_character(self) -> bool:
        """交互式创建人设"""
        try:
            character = self.character_manager.interactive_create_character()
            self.current_character = character
            # 同步到真人化引擎
            self.humanized_engine.character = character
            return True
        except Exception as e:
            print(f"创建人设失败: {e}")
            return False

    def apply_character_template(self, template_name: str) -> bool:
        """应用人设模板"""
        character = apply_preset_template(self.character_manager, template_name)
        if character:
            self.current_character = character
            # 同步到真人化引擎
            self.humanized_engine.character = character
            return True
        return False
    
    def get_character_info(self) -> str:
        """获取当前人设信息"""
        return self.character_manager.get_character_description()
    
    def list_character_presets(self) -> List[str]:
        """列出所有人设预设"""
        return self.character_manager.list_presets()
    
    # 新增：记忆相关功能
    def get_memory_status(self) -> str:
        """获取记忆状态"""
        return self.memory_manager.get_memory_stats()
    
    def get_user_profile(self) -> str:
        """获取用户画像"""
        return self.memory_manager.get_user_profile_summary()
    
    def recall_memories(self, query: str) -> List[Any]:
        """回忆相关记忆"""
        return self.memory_manager.core_memory.recall(query)
    
    def get_chat_history(self) -> List[Dict[str, str]]:
        return self.chat_history
    
    def save_chat_history(self, filepath: str):
        import json
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history, f, ensure_ascii=False, indent=2)
    
    def load_chat_history(self, filepath: str):
        import json
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.chat_history = json.load(f)
            return True
        except Exception:
            return False
    
    def clear_history(self):
        self.chat_history = []
        self.violation_count = 0
        self.memory_manager.clear_temp_memory()
    
    def update_personality(self, updates: Dict[str, Any]):
        if 'mood' in updates:
            self.personality.update_mood(updates['mood'])
        if 'relationship_level' in updates:
            self.personality.relationship_level = updates['relationship_level']
        if 'add_memory' in updates:
            self.personality.add_memory(updates['add_memory'])
    
    def get_moderation_status(self) -> Dict[str, Any]:
        """获取风控状态"""
        return {
            'violation_count': self.violation_count,
            'max_violations': self.max_violations,
            'is_restricted': self.violation_count >= self.max_violations
        }

    def toggle_humanized_mode(self) -> bool:
        """切换真人化模式"""
        self.humanized_mode = not self.humanized_mode
        return self.humanized_mode

    def get_emotion_status(self) -> Dict[str, Any]:
        """获取情绪状态"""
        return self.humanized_engine.get_emotion_status()

    def get_internal_monologue(self) -> str:
        """获取最近的内心独白"""
        thoughts = self.humanized_engine.get_recent_thoughts(3)
        return "；".join(thoughts) if thoughts else ""
