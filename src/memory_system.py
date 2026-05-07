
import json
import os
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class MemoryEntry:
    """记忆条目"""
    content: str
    timestamp: str
    importance: float  # 0-1, 越重要越容易被记住
    category: str  # 事实/情感/偏好/事件
    context: str = ""  # 上下文信息
    access_count: int = 0  # 被访问次数
    last_accessed: str = ""

class CoreMemory:
    """核心记忆系统 - 长期永久记忆"""
    
    def __init__(self, memory_file: str = "data/core_memory.json"):
        self.memory_file = memory_file
        self.memories: Dict[str, List[MemoryEntry]] = {
            'facts': [],      # 事实记忆：用户的基本信息
            'emotions': [],   # 情感记忆：重要的情感时刻
            'preferences': [], # 偏好记忆：用户的喜好厌恶
            'events': [],     # 事件记忆：重要事件
            'habits': [],     # 习惯记忆：用户的行为模式
            'relationships': [] # 关系记忆：用户提到的重要人物
        }
        self.load()
    
    def load(self):
        """加载记忆"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for category, entries in data.items():
                        if category in self.memories:
                            self.memories[category] = [
                                MemoryEntry(**entry) for entry in entries
                            ]
            except Exception as e:
                print(f"加载记忆失败: {e}")
    
    def save(self):
        """保存记忆"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        try:
            data = {}
            for category, entries in self.memories.items():
                data[category] = [asdict(entry) for entry in entries]
            
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存记忆失败: {e}")
    
    def add_memory(self, content: str, category: str = 'facts', 
                   importance: float = 0.5, context: str = ""):
        """添加记忆"""
        if category not in self.memories:
            category = 'facts'
        
        # 检查是否已存在相似记忆
        existing = self._find_similar(content, category)
        if existing:
            # 更新已有记忆的重要性
            existing.importance = min(1.0, existing.importance + 0.1)
            existing.access_count += 1
            existing.last_accessed = datetime.now().isoformat()
            self.save()
            return
        
        entry = MemoryEntry(
            content=content,
            timestamp=datetime.now().isoformat(),
            importance=importance,
            category=category,
            context=context,
            access_count=1,
            last_accessed=datetime.now().isoformat()
        )
        
        self.memories[category].append(entry)
        
        # 如果记忆太多，清理不重要的
        self._cleanup_memories(category)
        self.save()
    
    def _find_similar(self, content: str, category: str) -> Optional[MemoryEntry]:
        """查找相似记忆"""
        for entry in self.memories.get(category, []):
            # 简单相似度检查
            if content in entry.content or entry.content in content:
                return entry
            # 检查关键词重叠
            words1 = set(content.lower().split())
            words2 = set(entry.content.lower().split())
            if len(words1 & words2) / max(len(words1), len(words2)) > 0.7:
                return entry
        return None
    
    def _cleanup_memories(self, category: str, max_memories: int = 50):
        """清理不重要的记忆"""
        memories = self.memories[category]
        if len(memories) <= max_memories:
            return
        
        # 按重要性排序，保留重要的
        memories.sort(key=lambda x: (
            x.importance * 0.4 + 
            min(x.access_count / 10, 1.0) * 0.3 +
            (1 if datetime.now() - datetime.fromisoformat(x.timestamp) < timedelta(days=30) else 0) * 0.3
        ), reverse=True)
        
        self.memories[category] = memories[:max_memories]
    
    def recall(self, query: str, category: Optional[str] = None, 
               limit: int = 5) -> List[MemoryEntry]:
        """回忆相关记忆"""
        results = []
        categories = [category] if category else self.memories.keys()
        
        for cat in categories:
            for entry in self.memories.get(cat, []):
                # 计算相关性分数
                relevance = self._calculate_relevance(query, entry)
                if relevance > 0.3:  # 阈值
                    entry.access_count += 1
                    entry.last_accessed = datetime.now().isoformat()
                    results.append((relevance, entry))
        
        # 按相关性排序
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]
    
    def _calculate_relevance(self, query: str, entry: MemoryEntry) -> float:
        """计算记忆与查询的相关性"""
        query_words = set(query.lower().split())
        content_words = set(entry.content.lower().split())
        
        if not query_words or not content_words:
            return 0.0
        
        # 关键词重叠度
        overlap = len(query_words & content_words) / max(len(query_words), len(content_words))
        
        # 重要性加权
        importance_weight = entry.importance * 0.3
        
        # 时效性加权
        try:
            age = datetime.now() - datetime.fromisoformat(entry.timestamp)
            recency_weight = max(0, 1 - age.days / 365) * 0.2  # 一年内衰减
        except:
            recency_weight = 0
        
        # 访问频率加权
        frequency_weight = min(entry.access_count / 10, 1.0) * 0.2
        
        return overlap * 0.3 + importance_weight + recency_weight + frequency_weight
    
    def get_user_profile(self) -> Dict[str, Any]:
        """获取用户画像"""
        profile = {}
        
        # 基本信息
        facts = self.memories['facts']
        profile['basic_info'] = [entry.content for entry in facts[:10]]
        
        # 情感倾向
        emotions = self.memories['emotions']
        profile['emotional_moments'] = [entry.content for entry in emotions[:5]]
        
        # 偏好
        preferences = self.memories['preferences']
        profile['preferences'] = [entry.content for entry in preferences[:10]]
        
        # 习惯
        habits = self.memories['habits']
        profile['habits'] = [entry.content for entry in habits[:5]]
        
        return profile
    
    def get_memory_summary(self) -> str:
        """获取记忆摘要"""
        summary = []
        total_memories = sum(len(entries) for entries in self.memories.values())
        summary.append(f"共记录 {total_memories} 条记忆")
        
        for category, entries in self.memories.items():
            if entries:
                summary.append(f"  {category}: {len(entries)} 条")
        
        return "\n".join(summary)

class TemporaryMemory:
    """临时记忆系统 - 短期上下文记忆"""
    
    def __init__(self, max_turns: int = 20):
        self.conversation_history: List[Dict[str, str]] = []
        self.current_context: Dict[str, Any] = {}
        self.max_turns = max_turns
    
    def add_turn(self, user_input: str, bot_response: str, 
                 metadata: Optional[Dict] = None):
        """添加一轮对话"""
        turn = {
            'user': user_input,
            'bot': bot_response,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        
        self.conversation_history.append(turn)
        
        # 保持最近N轮
        if len(self.conversation_history) > self.max_turns:
            self.conversation_history = self.conversation_history[-self.max_turns:]
    
    def get_recent_context(self, turns: int = 5) -> str:
        """获取最近的对话上下文"""
        recent = self.conversation_history[-turns:]
        context = []
        for turn in recent:
            context.append(f"用户: {turn['user']}")
            context.append(f"小龙虾: {turn['bot']}")
        return "\n".join(context)
    
    def get_current_topic(self) -> Optional[str]:
        """获取当前话题"""
        if not self.conversation_history:
            return None
        
        # 简单提取最后一轮的话题
        last_turn = self.conversation_history[-1]
        return last_turn['user'][:50]
    
    def update_context(self, key: str, value: Any):
        """更新上下文信息"""
        self.current_context[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_context(self, key: str) -> Optional[Any]:
        """获取上下文信息"""
        if key in self.current_context:
            return self.current_context[key]['value']
        return None
    
    def clear(self):
        """清空临时记忆"""
        self.conversation_history.clear()
        self.current_context.clear()
    
    def extract_important_info(self) -> List[Dict[str, Any]]:
        """从对话中提取重要信息用于长期记忆"""
        important_info = []
        
        for turn in self.conversation_history:
            user_input = turn['user']
            
            # 提取事实信息
            if any(keyword in user_input for keyword in ['我叫', '我是', '我来自', '我工作', '我喜欢', '我讨厌']):
                important_info.append({
                    'content': user_input,
                    'category': 'facts' if '我叫' in user_input or '我是' in user_input else 'preferences',
                    'importance': 0.8
                })
            
            # 提取情感信息
            if any(keyword in user_input for keyword in ['开心', '难过', '生气', '感动', '惊喜']):
                important_info.append({
                    'content': user_input,
                    'category': 'emotions',
                    'importance': 0.7
                })
            
            # 提取事件信息
            if any(keyword in user_input for keyword in ['今天', '昨天', '明天', '上周', '下周']):
                important_info.append({
                    'content': user_input,
                    'category': 'events',
                    'importance': 0.6
                })
        
        return important_info

class MemoryManager:
    """记忆管理器 - 统一管理核心记忆和临时记忆"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.core_memory = CoreMemory(os.path.join(data_dir, "core_memory.json"))
        self.temp_memory = TemporaryMemory()
        
        # 记忆提取间隔（每N轮对话提取一次）
        self.extraction_interval = 5
        self.turns_since_extraction = 0
    
    def process_interaction(self, user_input: str, bot_response: str):
        """处理一次交互"""
        # 添加到临时记忆
        self.temp_memory.add_turn(user_input, bot_response)
        
        # 定期提取重要信息到核心记忆
        self.turns_since_extraction += 1
        if self.turns_since_extraction >= self.extraction_interval:
            self._extract_to_core_memory()
            self.turns_since_extraction = 0
    
    def _extract_to_core_memory(self):
        """将临时记忆中的重要信息提取到核心记忆"""
        important_info = self.temp_memory.extract_important_info()
        
        for info in important_info:
            self.core_memory.add_memory(
                content=info['content'],
                category=info['category'],
                importance=info['importance'],
                context=self.temp_memory.get_recent_context(3)
            )
    
    def get_relevant_memories(self, query: str) -> Tuple[List[MemoryEntry], str]:
        """获取相关记忆（核心+临时）"""
        # 从核心记忆中召回
        core_results = self.core_memory.recall(query, limit=3)
        
        # 从临时记忆中获取上下文
        temp_context = self.temp_memory.get_recent_context(3)
        
        return core_results, temp_context
    
    def get_enriched_context(self, user_input: str) -> str:
        """获取增强的上下文（包含相关记忆）"""
        # 获取相关记忆
        relevant_memories, recent_context = self.get_relevant_memories(user_input)
        
        context_parts = []
        
        # 添加相关长期记忆
        if relevant_memories:
            context_parts.append("【我记得】")
            for memory in relevant_memories:
                context_parts.append(f"- {memory.content}")
            context_parts.append("")
        
        # 添加近期对话
        if recent_context:
            context_parts.append("【近期对话】")
            context_parts.append(recent_context)
        
        return "\n".join(context_parts)
    
    def get_user_profile_summary(self) -> str:
        """获取用户画像摘要"""
        profile = self.core_memory.get_user_profile()
        
        summary = []
        if profile['basic_info']:
            summary.append("关于你：" + "；".join(profile['basic_info'][:3]))
        
        if profile['preferences']:
            summary.append("你的喜好：" + "；".join(profile['preferences'][:3]))
        
        if profile['habits']:
            summary.append("你的习惯：" + "；".join(profile['habits'][:2]))
        
        return "\n".join(summary) if summary else "还没有足够的记忆"
    
    def clear_temp_memory(self):
        """清空临时记忆"""
        self.temp_memory.clear()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """获取记忆统计"""
        return {
            'core_memory': self.core_memory.get_memory_summary(),
            'temp_memory_turns': len(self.temp_memory.conversation_history),
            'temp_memory_context': len(self.temp_memory.current_context)
        }
