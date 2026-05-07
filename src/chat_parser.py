
import re
import json
from typing import List, Dict, Any, Tuple
import os

class ChatRecord:
    def __init__(self, sender: str, content: str, timestamp: str = ""):
        self.sender = sender
        self.content = content
        self.timestamp = timestamp
    
    def to_dict(self) -> Dict[str, str]:
        return {
            'sender': self.sender,
            'content': self.content,
            'timestamp': self.timestamp
        }

class ChatParser:
    SUPPORTED_FORMATS = ['wechat', 'qq', 'telegram', 'whatsapp', 'plain', 'json']
    
    @classmethod
    def detect_format(cls, content: str) -> str:
        if '微信' in content or 'WeChat' in content or 'MicroMsg' in content:
            return 'wechat'
        elif 'QQ' in content or 'TIM' in content:
            return 'qq'
        elif 'Telegram' in content or 't.me' in content:
            return 'telegram'
        elif 'WhatsApp' in content:
            return 'whatsapp'
        elif cls._is_json(content):
            return 'json'
        else:
            return 'plain'
    
    @classmethod
    def _is_json(cls, content: str) -> bool:
        try:
            json.loads(content)
            return True
        except ValueError:
            return False
    
    @classmethod
    def parse_file(cls, filepath: str) -> List[ChatRecord]:
        _, ext = os.path.splitext(filepath)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        format_type = cls.detect_format(content)
        
        if ext.lower() == '.json':
            return cls.parse_json(content)
        elif format_type == 'wechat':
            return cls.parse_wechat(content)
        elif format_type == 'qq':
            return cls.parse_qq(content)
        elif format_type == 'telegram':
            return cls.parse_telegram(content)
        elif format_type == 'whatsapp':
            return cls.parse_whatsapp(content)
        else:
            return cls.parse_plain(content)
    
    @classmethod
    def parse_json(cls, content: str) -> List[ChatRecord]:
        records = []
        try:
            data = json.loads(content)
            if isinstance(data, list):
                for item in data:
                    if 'sender' in item and 'content' in item:
                        records.append(ChatRecord(
                            sender=item['sender'],
                            content=item['content'],
                            timestamp=item.get('timestamp', '')
                        ))
            elif isinstance(data, dict) and 'messages' in data:
                for item in data['messages']:
                    if 'sender' in item and 'content' in item:
                        records.append(ChatRecord(
                            sender=item['sender'],
                            content=item['content'],
                            timestamp=item.get('timestamp', '')
                        ))
        except Exception:
            pass
        return records
    
    @classmethod
    def parse_wechat(cls, content: str) -> List[ChatRecord]:
        records = []
        lines = content.split('\n')
        current_sender = ''
        current_content = ''
        
        for line in lines:
            line = line.strip()
            
            wechat_pattern = r'^\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+(.+?):\s+(.*)'
            match = re.match(wechat_pattern, line)
            if match:
                if current_sender and current_content:
                    records.append(ChatRecord(current_sender, current_content.strip()))
                current_sender = match.group(2)
                current_content = match.group(3)
            elif current_sender and line:
                current_content += '\n' + line
        
        if current_sender and current_content:
            records.append(ChatRecord(current_sender, current_content.strip()))
        
        return records
    
    @classmethod
    def parse_qq(cls, content: str) -> List[ChatRecord]:
        records = []
        lines = content.split('\n')
        
        qq_pattern = r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(.+?)\s*[说:]+\s*(.*)'
        
        for line in lines:
            line = line.strip()
            match = re.match(qq_pattern, line)
            if match:
                records.append(ChatRecord(
                    sender=match.group(2),
                    content=match.group(3),
                    timestamp=match.group(1)
                ))
        
        return records
    
    @classmethod
    def parse_telegram(cls, content: str) -> List[ChatRecord]:
        records = []
        lines = content.split('\n')
        
        telegram_pattern = r'^(\d{2}\.\d{2}\.\d{4}\s+\d{2}:\d{2})\s+-\s+(.+?):\s+(.*)'
        
        for line in lines:
            line = line.strip()
            match = re.match(telegram_pattern, line)
            if match:
                records.append(ChatRecord(
                    sender=match.group(2),
                    content=match.group(3),
                    timestamp=match.group(1)
                ))
        
        return records
    
    @classmethod
    def parse_whatsapp(cls, content: str) -> List[ChatRecord]:
        records = []
        lines = content.split('\n')
        
        whatsapp_pattern = r'^\[(\d{2}/\d{2}/\d{4},\s+\d{2}:\d{2}:\d{2})\]\s+(.+?):\s+(.*)'
        
        for line in lines:
            line = line.strip()
            match = re.match(whatsapp_pattern, line)
            if match:
                records.append(ChatRecord(
                    sender=match.group(2),
                    content=match.group(3),
                    timestamp=match.group(1)
                ))
        
        return records
    
    @classmethod
    def parse_plain(cls, content: str) -> List[ChatRecord]:
        records = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(':', 1)
            if len(parts) == 2:
                sender = parts[0].strip()
                content = parts[1].strip()
                records.append(ChatRecord(sender, content))
            else:
                records.append(ChatRecord('Unknown', line))
        
        return records
    
    @classmethod
    def analyze_chat_style(cls, records: List[ChatRecord]) -> Dict[str, Any]:
        if not records:
            return {}
        
        sender_stats = {}
        word_counts = []
        avg_lengths = []
        
        for record in records:
            if record.sender not in sender_stats:
                sender_stats[record.sender] = {'count': 0, 'total_length': 0}
            
            sender_stats[record.sender]['count'] += 1
            sender_stats[record.sender]['total_length'] += len(record.content)
            word_counts.append(len(record.content))
            avg_lengths.append(len(record.content))
        
        for sender in sender_stats:
            if sender_stats[sender]['count'] > 0:
                sender_stats[sender]['avg_length'] = sender_stats[sender]['total_length'] / sender_stats[sender]['count']
        
        return {
            'total_messages': len(records),
            'senders': list(sender_stats.keys()),
            'sender_stats': sender_stats,
            'avg_message_length': sum(avg_lengths) / len(avg_lengths) if avg_lengths else 0,
            'most_active_sender': max(sender_stats, key=lambda x: sender_stats[x]['count'], default=None)
        }
