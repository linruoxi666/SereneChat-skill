
import re
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ChatPlatform(Enum):
    WECHAT = "wechat"
    QQ = "qq"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    UNKNOWN = "unknown"

@dataclass
class ChatMessage:
    sender: str
    content: str
    timestamp: str = ""
    platform: ChatPlatform = ChatPlatform.UNKNOWN
    is_user: bool = True

class OCRChatParser:
    """OCR聊天截图解析器 - 支持识别聊天截图中的文字内容"""
    
    def __init__(self):
        self.platform_patterns = {
            ChatPlatform.WECHAT: {
                'time_pattern': r'(\d{1,2}:\d{2})',
                'sender_pattern': r'([\u4e00-\u9fa5\w\s]+?)(?:\s+|$)',
                'message_indicators': ['微信', 'WeChat', '朋友圈', '公众号'],
                'bubble_indicators': ['对方正在输入', '语音', '图片', '视频']
            },
            ChatPlatform.QQ: {
                'time_pattern': r'(\d{1,2}:\d{2}:\d{2})',
                'sender_pattern': r'([\u4e00-\u9fa5\w\s]+?)(?:\s+|$)',
                'message_indicators': ['QQ', 'TIM', 'QQ空间', '群'],
                'bubble_indicators': ['戳一戳', '闪照', '厘米秀']
            },
            ChatPlatform.TELEGRAM: {
                'time_pattern': r'(\d{1,2}:\d{2})',
                'sender_pattern': r'([\w\s]+?)(?:\s+|$)',
                'message_indicators': ['Telegram', 'TG', 'Channel', 'Bot'],
                'bubble_indicators': ['Forwarded', 'Reply', 'Edit']
            },
            ChatPlatform.WHATSAPP: {
                'time_pattern': r'(\d{1,2}:\d{2})',
                'sender_pattern': r'([\w\s]+?)(?:\s+|$)',
                'message_indicators': ['WhatsApp', 'WA', 'Status', 'Call'],
                'bubble_indicators': ['Voice', 'Forwarded', 'Document']
            }
        }
    
    def detect_platform(self, ocr_text: str) -> ChatPlatform:
        """根据OCR文本检测聊天平台"""
        text_lower = ocr_text.lower()
        
        for platform, patterns in self.platform_patterns.items():
            for indicator in patterns['message_indicators']:
                if indicator.lower() in text_lower:
                    return platform
        
        # 根据特征判断
        if any(keyword in ocr_text for keyword in ['微信', 'WeChat', '朋友圈']):
            return ChatPlatform.WECHAT
        elif any(keyword in ocr_text for keyword in ['QQ', 'TIM']):
            return ChatPlatform.QQ
        elif any(keyword in ocr_text for keyword in ['Telegram', 'TG']):
            return ChatPlatform.TELEGRAM
        elif any(keyword in ocr_text for keyword in ['WhatsApp', 'WA']):
            return ChatPlatform.WHATSAPP
        
        return ChatPlatform.UNKNOWN
    
    def parse_ocr_text(self, ocr_text: str) -> List[ChatMessage]:
        """解析OCR识别的聊天文本"""
        platform = self.detect_platform(ocr_text)
        messages = []
        
        lines = ocr_text.split('\n')
        current_sender = ""
        current_content = ""
        current_time = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 尝试匹配时间
            time_match = re.search(r'(\d{1,2}:\d{2}(?::\d{2})?)', line)
            if time_match:
                current_time = time_match.group(1)
            
            # 尝试匹配发送者和消息内容
            # 常见格式: "发送者: 消息内容" 或 "发送者 消息内容"
            sender_message_match = re.match(r'^([\u4e00-\u9fa5\w\s]+?)[\s:：]+(.+)$', line)
            
            if sender_message_match:
                # 保存之前的消息
                if current_sender and current_content:
                    messages.append(ChatMessage(
                        sender=current_sender,
                        content=current_content.strip(),
                        timestamp=current_time,
                        platform=platform
                    ))
                
                current_sender = sender_message_match.group(1).strip()
                current_content = sender_message_match.group(2).strip()
            else:
                # 可能是消息的续行
                if current_sender:
                    current_content += " " + line
        
        # 保存最后一条消息
        if current_sender and current_content:
            messages.append(ChatMessage(
                sender=current_sender,
                content=current_content.strip(),
                timestamp=current_time,
                platform=platform
            ))
        
        return messages
    
    def parse_wechat_screenshot(self, ocr_text: str) -> List[ChatMessage]:
        """专门解析微信聊天截图"""
        messages = []
        lines = ocr_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 微信格式: "发送者名称 消息内容" 或 "发送者名称: 消息内容"
            # 也可能有时间前缀: "10:30 发送者: 消息"
            wechat_pattern = r'(?:\d{1,2}:\d{2}\s+)?([\u4e00-\u9fa5\w\s]+?)[\s:：]+(.+)'
            match = re.match(wechat_pattern, line)
            
            if match:
                sender = match.group(1).strip()
                content = match.group(2).strip()
                
                # 过滤系统消息
                if sender in ['对方正在输入...', '微信团队', '']:
                    continue
                
                messages.append(ChatMessage(
                    sender=sender,
                    content=content,
                    platform=ChatPlatform.WECHAT
                ))
        
        return messages
    
    def parse_qq_screenshot(self, ocr_text: str) -> List[ChatMessage]:
        """专门解析QQ聊天截图"""
        messages = []
        lines = ocr_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # QQ格式: "发送者 消息内容" 或 "[时间] 发送者: 消息"
            qq_pattern = r'(?:\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s+)?([\u4e00-\u9fa5\w\s]+?)[\s:：]+(.+)'
            match = re.match(qq_pattern, line)
            
            if match:
                sender = match.group(1).strip()
                content = match.group(2).strip()
                
                # 过滤系统消息
                if sender in ['QQ团队', '系统消息', '']:
                    continue
                
                messages.append(ChatMessage(
                    sender=sender,
                    content=content,
                    platform=ChatPlatform.QQ
                ))
        
        return messages
    
    def extract_chat_from_image(self, image_path: str) -> List[ChatMessage]:
        """从图片中提取聊天内容（需要OCR库支持）"""
        try:
            # 尝试使用pytesseract进行OCR
            import pytesseract
            from PIL import Image
            
            image = Image.open(image_path)
            ocr_text = pytesseract.image_to_string(image, lang='chi_sim+eng')
            
            return self.parse_ocr_text(ocr_text)
        
        except ImportError:
            print("警告: 未安装OCR库。请安装: pip install pytesseract pillow")
            print("同时需要安装Tesseract-OCR引擎")
            return []
        except Exception as e:
            print(f"OCR识别失败: {e}")
            return []
    
    def format_for_training(self, messages: List[ChatMessage], bot_name: str = "小龙虾") -> List[Dict[str, str]]:
        """将解析的消息格式化为训练数据"""
        formatted_data = []
        
        for msg in messages:
            formatted_data.append({
                'sender': msg.sender,
                'content': msg.content,
                'timestamp': msg.timestamp,
                'platform': msg.platform.value,
                'is_bot': msg.sender == bot_name
            })
        
        return formatted_data
    
    def analyze_chat_pattern(self, messages: List[ChatMessage]) -> Dict[str, Any]:
        """分析聊天模式"""
        if not messages:
            return {}
        
        senders = {}
        total_messages = len(messages)
        
        for msg in messages:
            if msg.sender not in senders:
                senders[msg.sender] = {
                    'message_count': 0,
                    'total_length': 0,
                    'messages': []
                }
            
            senders[msg.sender]['message_count'] += 1
            senders[msg.sender]['total_length'] += len(msg.content)
            senders[msg.sender]['messages'].append(msg.content)
        
        # 计算平均消息长度
        for sender in senders:
            if senders[sender]['message_count'] > 0:
                senders[sender]['avg_length'] = (
                    senders[sender]['total_length'] / senders[sender]['message_count']
                )
        
        return {
            'total_messages': total_messages,
            'unique_senders': len(senders),
            'sender_stats': senders,
            'platform': messages[0].platform.value if messages else 'unknown'
        }
