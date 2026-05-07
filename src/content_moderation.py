
import re
from typing import List, Dict, Tuple, Optional
from enum import Enum

class RiskLevel(Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ContentModerator:
    """内容风控系统 - 防止色情、暴力等违规内容"""
    
    def __init__(self):
        self._init_sensitive_words()
        self._init_patterns()
        self.risk_threshold = {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 3,
            RiskLevel.HIGH: 5,
            RiskLevel.CRITICAL: 8
        }
    
    def _init_sensitive_words(self):
        """初始化敏感词库"""
        # 色情相关敏感词
        self.sexual_words = [
            '色情', '做爱', '性交', '性器官', '裸体', '裸照', '裸聊',
            '约炮', '嫖娼', '卖淫', '强奸', '乱伦', 'SM', '性虐',
            '性服务', '性交易', '性暗示', '性诱惑', '性挑逗',
            '淫秽', '猥亵', '性骚扰', '性侵犯', '性暴力',
            'av', 'porn', 'sex', 'nude', 'naked', 'xxx',
            '成人影片', '色情片', '毛片', '黄片', '三级片',
            '性高潮', '性快感', '性幻想', '性癖好', '性变态',
            '性奴', '性玩具', '性用品', '性药', '催情',
            '包养', '二奶', '小三', '情妇', '情夫',
            '一夜情', '婚外情', '通奸', '偷情', '出轨',
            '性开放', '性自由', '性解放', '性革命',
            '性知识', '性教育', '性健康', '性科学',
            '性心理', '性取向', '性认同', '性表达',
            '性权利', '性平等', '性尊重', '性同意',
            '性安全', '性保护', '性预防', '性治疗',
            '性咨询', '性辅导', '性支持', '性帮助'
        ]
        
        # 暴力相关敏感词
        self.violence_words = [
            '杀人', '抢劫', '绑架', '爆炸', '恐怖袭击',
            '暴力', '殴打', '伤害', '虐待', '折磨',
            '血腥', '残忍', '冷酷', '无情', '恶毒',
            '报复', '仇恨', '歧视', '偏见', '排斥',
            '武器', '枪支', '弹药', '炸弹', '刀具'
        ]
        
        # 毒品相关敏感词
        self.drug_words = [
            '毒品', '吸毒', '贩毒', '制毒', '运毒',
            '大麻', '冰毒', '海洛因', '可卡因', '摇头丸',
            '兴奋剂', '致幻剂', '麻醉剂', '精神药品',
            '毒瘾', '戒毒', '禁毒', '缉毒', '扫毒'
        ]
        
        # 赌博相关敏感词
        self.gambling_words = [
            '赌博', '赌场', '赌钱', '赌球', '赌马',
            '彩票', '博彩', '六合彩', '赌局', '赌注',
            '赌徒', '赌棍', '赌鬼', '赌神', '赌圣',
            '网络赌博', '线上赌博', '地下赌博', '非法赌博'
        ]
        
        # 政治敏感词
        self.political_words = [
            '反动', '颠覆', '分裂', '独立', '自治',
            '暴乱', '动乱', '骚乱', '游行', '示威',
            '抗议', '罢工', '罢课', '罢市', '集会',
            '邪教', '非法组织', '恐怖组织', '极端组织'
        ]
        
        # 诈骗相关敏感词
        self.fraud_words = [
            '诈骗', '欺骗', '欺诈', '骗子', '骗局',
            '传销', '直销', '洗脑', '忽悠', '套路',
            '钓鱼', '木马', '病毒', '黑客', '盗号',
            '洗钱', '黑钱', '赃款', '非法所得', '不正当利益'
        ]
        
        # 合并所有敏感词
        self.all_sensitive_words = (
            self.sexual_words + 
            self.violence_words + 
            self.drug_words + 
            self.gambling_words + 
            self.political_words + 
            self.fraud_words
        )
    
    def _init_patterns(self):
        """初始化正则表达式模式"""
        # 色情内容模式
        self.sexual_patterns = [
            r'(?:发|给|看|有|要).*?(?:图|照片|视频|片).*?(?:吗|么|不|没)',
            r'(?:裸|露|脱|穿).*?(?:照|图|视频|体)',
            r'(?:约|找|想|要).*?(?:炮|友|妹|女|男)',
            r'(?:性|色|黄).*?(?:服务|交易|暗示|诱惑)',
            r'(?:成人|色情|av|porn).*?(?:影片|片|视频|内容)',
            r'(?:包|养|陪|睡).*?(?:夜|晚|天|月|年)',
            r'(?:一|两|几|多).*?(?:夜|次|回|晚).*?(?:情|性|约)',
        ]
        
        # 诱导性内容模式
        self.seductive_patterns = [
            r'(?:来|去|到).*?(?:我家|你那里|酒店|宾馆|房间)',
            r'(?:一|两|几|多).*?(?:个人|一起|单独|私下)',
            r'(?:晚上|深夜|凌晨|半夜).*?(?:见|约|聊|玩)',
            r'(?:秘密|隐私|私密|私人).*?(?:话题|事情|内容|照片)',
            r'(?:不要|别|不能).*?(?:告诉|说|讲|透露).*?(?:别人|其他人|任何人)',
        ]
        
        # 联系方式模式
        self.contact_patterns = [
            r'(?:加|扫|关注|联系).*?(?:微信|QQ|qq|电话|手机|邮箱)',
            r'(?:微信|QQ|qq|电话|手机|邮箱).*?(?:号|号码|地址|联系)',
            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            r'1[3-9]\d{9}',
            r'[qQ][qQ]\s*[：:]\s*\d{5,11}',
        ]
    
    def check_text(self, text: str) -> Tuple[RiskLevel, List[str], Dict[str, any]]:
        """
        检查文本内容风险
        返回: (风险等级, 触发的敏感词列表, 详细信息)
        """
        if not text or not isinstance(text, str):
            return RiskLevel.SAFE, [], {}
        
        text_lower = text.lower()
        triggered_words = []
        risk_score = 0
        details = {
            'sexual_count': 0,
            'violence_count': 0,
            'drug_count': 0,
            'gambling_count': 0,
            'political_count': 0,
            'fraud_count': 0,
            'pattern_matches': []
        }
        
        # 检查敏感词
        for word in self.all_sensitive_words:
            if word in text or word in text_lower:
                triggered_words.append(word)
                
                # 分类统计
                if word in self.sexual_words:
                    details['sexual_count'] += 1
                    risk_score += 2
                elif word in self.violence_words:
                    details['violence_count'] += 1
                    risk_score += 2
                elif word in self.drug_words:
                    details['drug_count'] += 1
                    risk_score += 3
                elif word in self.gambling_words:
                    details['gambling_count'] += 1
                    risk_score += 2
                elif word in self.political_words:
                    details['political_count'] += 1
                    risk_score += 3
                elif word in self.fraud_words:
                    details['fraud_count'] += 1
                    risk_score += 2
        
        # 检查模式匹配
        for pattern in self.sexual_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                details['pattern_matches'].extend(matches)
                risk_score += len(matches) * 2
        
        for pattern in self.seductive_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                details['pattern_matches'].extend(matches)
                risk_score += len(matches) * 1
        
        # 确定风险等级
        risk_level = self._calculate_risk_level(risk_score)
        
        return risk_level, triggered_words, details
    
    def _calculate_risk_level(self, score: int) -> RiskLevel:
        """根据分数计算风险等级"""
        if score >= self.risk_threshold[RiskLevel.CRITICAL]:
            return RiskLevel.CRITICAL
        elif score >= self.risk_threshold[RiskLevel.HIGH]:
            return RiskLevel.HIGH
        elif score >= self.risk_threshold[RiskLevel.MEDIUM]:
            return RiskLevel.MEDIUM
        elif score >= self.risk_threshold[RiskLevel.LOW]:
            return RiskLevel.LOW
        else:
            return RiskLevel.SAFE
    
    def is_safe(self, text: str) -> bool:
        """检查文本是否安全"""
        risk_level, _, _ = self.check_text(text)
        return risk_level in [RiskLevel.SAFE, RiskLevel.LOW]
    
    def get_warning_message(self, risk_level: RiskLevel) -> str:
        """根据风险等级返回警告信息"""
        warnings = {
            RiskLevel.SAFE: "",
            RiskLevel.LOW: "请注意言辞，保持友好交流。",
            RiskLevel.MEDIUM: "检测到不当内容，请遵守社区规范。",
            RiskLevel.HIGH: "内容涉及敏感话题，已被记录。请立即停止此类话题。",
            RiskLevel.CRITICAL: "严重违规！内容已被拦截并记录。多次违规将封禁账号。"
        }
        return warnings.get(risk_level, "")
    
    def filter_response(self, text: str, replace_char: str = "*") -> str:
        """过滤响应中的敏感词"""
        if not text:
            return text
        
        filtered_text = text
        risk_level, triggered_words, _ = self.check_text(text)
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            # 高风险内容，完全替换
            for word in triggered_words:
                filtered_text = filtered_text.replace(word, replace_char * len(word))
                filtered_text = filtered_text.replace(word.lower(), replace_char * len(word))
        elif risk_level == RiskLevel.MEDIUM:
            # 中风险内容，部分替换
            for word in triggered_words:
                if len(word) > 2:
                    # 保留首尾字符，中间替换
                    masked = word[0] + replace_char * (len(word) - 2) + word[-1]
                    filtered_text = filtered_text.replace(word, masked)
                    filtered_text = filtered_text.replace(word.lower(), masked)
        
        return filtered_text
    
    def check_conversation(self, messages: List[str]) -> Dict[str, any]:
        """检查整个对话的风险情况"""
        results = []
        total_risk_score = 0
        max_risk_level = RiskLevel.SAFE
        
        for i, message in enumerate(messages):
            risk_level, triggered_words, details = self.check_text(message)
            
            results.append({
                'message_index': i,
                'message_preview': message[:50] + '...' if len(message) > 50 else message,
                'risk_level': risk_level.value,
                'triggered_words': triggered_words,
                'details': details
            })
            
            # 计算总分
            score = self._risk_level_to_score(risk_level)
            total_risk_score += score
            
            if self._risk_level_to_score(risk_level) > self._risk_level_to_score(max_risk_level):
                max_risk_level = risk_level
        
        return {
            'total_messages': len(messages),
            'total_risk_score': total_risk_score,
            'average_risk_score': total_risk_score / len(messages) if messages else 0,
            'max_risk_level': max_risk_level.value,
            'message_results': results,
            'is_safe': max_risk_level in [RiskLevel.SAFE, RiskLevel.LOW]
        }
    
    def _risk_level_to_score(self, risk_level: RiskLevel) -> int:
        """风险等级转分数"""
        scores = {
            RiskLevel.SAFE: 0,
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 3,
            RiskLevel.HIGH: 5,
            RiskLevel.CRITICAL: 8
        }
        return scores.get(risk_level, 0)
    
    def add_custom_words(self, words: List[str], category: str = "custom"):
        """添加自定义敏感词"""
        if category == "sexual":
            self.sexual_words.extend(words)
        elif category == "violence":
            self.violence_words.extend(words)
        elif category == "drug":
            self.drug_words.extend(words)
        elif category == "gambling":
            self.gambling_words.extend(words)
        elif category == "political":
            self.political_words.extend(words)
        elif category == "fraud":
            self.fraud_words.extend(words)
        else:
            # 添加到自定义分类
            if not hasattr(self, 'custom_words'):
                self.custom_words = []
            self.custom_words.extend(words)
            self.all_sensitive_words.extend(words)
            return
        
        self.all_sensitive_words.extend(words)
    
    def remove_words(self, words: List[str]):
        """移除敏感词"""
        for word in words:
            if word in self.all_sensitive_words:
                self.all_sensitive_words.remove(word)
            if word in self.sexual_words:
                self.sexual_words.remove(word)
            if word in self.violence_words:
                self.violence_words.remove(word)
            if word in self.drug_words:
                self.drug_words.remove(word)
            if word in self.gambling_words:
                self.gambling_words.remove(word)
            if word in self.political_words:
                self.political_words.remove(word)
            if word in self.fraud_words:
                self.fraud_words.remove(word)
