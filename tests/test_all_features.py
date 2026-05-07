
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.chat_engine import ChatEngine
from src.memory_system import MemoryManager, CoreMemory, TemporaryMemory
from src.character_preset import CharacterPresetManager, apply_preset_template
from src.content_moderation import ContentModerator, RiskLevel
from src.ocr_chat_parser import OCRChatParser

def test_basic_chat():
    print("=" * 50)
    print("测试基础聊天功能")
    print("=" * 50)
    
    engine = ChatEngine()
    
    test_inputs = [
        "你好",
        "我想你了",
        "今天好累",
        "晚安",
        "吃饭了吗",
        "我好开心",
        "我心情不好"
    ]
    
    for input_text in test_inputs:
        response = engine.chat(input_text)
        print(f"输入: {input_text}")
        print(f"回复: {response}")
        print()
    
    print("✓ 基础聊天测试通过")
    return True

def test_memory_system():
    print("=" * 50)
    print("测试记忆系统")
    print("=" * 50)
    
    # 测试核心记忆
    core_memory = CoreMemory("data/test_core_memory.json")
    core_memory.add_memory("用户叫小明", "facts", 0.8)
    core_memory.add_memory("用户喜欢吃火锅", "preferences", 0.7)
    core_memory.add_memory("用户今天很开心", "emotions", 0.6)
    
    # 测试记忆召回
    results = core_memory.recall("小明")
    print(f"召回关于'小明'的记忆: {len(results)} 条")
    for r in results:
        print(f"  - {r.content}")
    
    # 测试临时记忆
    temp_memory = TemporaryMemory()
    temp_memory.add_turn("你好", "你好呀")
    temp_memory.add_turn("我叫小明", "好的小明")
    
    context = temp_memory.get_recent_context(2)
    print(f"\n临时记忆上下文:\n{context}")
    
    # 测试记忆管理器
    memory_manager = MemoryManager("data/test_memory")
    memory_manager.process_interaction("我喜欢看电影", "我也喜欢看电影")
    memory_manager.process_interaction("我叫小明", "你好小明")
    
    profile = memory_manager.get_user_profile_summary()
    print(f"\n用户画像:\n{profile}")
    
    print("✓ 记忆系统测试通过")
    return True

def test_character_preset():
    print("=" * 50)
    print("测试人设设定功能")
    print("=" * 50)
    
    manager = CharacterPresetManager("data/test_presets")
    
    # 测试默认人设
    character = manager.get_current_character()
    print(f"默认人设: {character.name}")
    print(f"性格类型: {character.personality_type}")
    
    # 测试预设模板
    print("\n测试预设模板:")
    for template_name in ['tsundere', 'gentle', 'energetic', 'mature']:
        char = apply_preset_template(manager, template_name)
        if char:
            print(f"  ✓ {template_name}: {char.name} - {char.speaking_style}")
    
    # 测试人设描述
    desc = manager.get_character_description()
    print(f"\n人设描述预览:\n{desc[:200]}...")
    
    print("✓ 人设设定测试通过")
    return True

def test_content_moderation():
    print("=" * 50)
    print("测试内容风控系统")
    print("=" * 50)
    
    moderator = ContentModerator()
    
    # 测试安全内容
    safe_text = "今天天气真好，我想去公园散步"
    risk, words, details = moderator.check_text(safe_text)
    print(f"安全文本: '{safe_text}'")
    print(f"  风险等级: {risk.value}")
    
    # 测试敏感内容
    sensitive_text = "色情内容测试"
    risk, words, details = moderator.check_text(sensitive_text)
    print(f"\n敏感文本: '{sensitive_text}'")
    print(f"  风险等级: {risk.value}")
    print(f"  触发词: {words}")
    
    # 测试过滤功能
    filtered = moderator.filter_response("这是色情内容的测试")
    print(f"\n过滤结果: '{filtered}'")
    
    print("✓ 内容风控测试通过")
    return True

def test_ocr_parser():
    print("=" * 50)
    print("测试OCR聊天解析")
    print("=" * 50)
    
    parser = OCRChatParser()
    
    # 测试文本解析
    ocr_text = """
    10:30 小明: 你好呀
    10:31 小红: 你好，今天天气不错
    10:32 小明: 是啊，要不要一起出去玩
    """
    
    messages = parser.parse_ocr_text(ocr_text)
    print(f"解析到 {len(messages)} 条消息:")
    for msg in messages:
        print(f"  [{msg.platform.value}] {msg.sender}: {msg.content}")
    
    # 测试平台检测
    platform = parser.detect_platform("微信聊天内容")
    print(f"\n平台检测: {platform.value}")
    
    print("✓ OCR解析测试通过")
    return True

def test_chat_engine_features():
    print("=" * 50)
    print("测试聊天引擎综合功能")
    print("=" * 50)
    
    engine = ChatEngine()
    
    # 测试风控状态
    status = engine.get_moderation_status()
    print(f"风控状态: {status}")
    
    # 测试人设功能
    print("\n测试人设切换:")
    engine.apply_character_template('tsundere')
    response = engine.chat("你好")
    print(f"傲娇回复: {response}")
    
    engine.apply_character_template('gentle')
    response = engine.chat("你好")
    print(f"温柔回复: {response}")
    
    # 测试记忆功能
    print("\n测试记忆功能:")
    engine.chat("我叫小明")
    engine.chat("我喜欢吃火锅")
    
    profile = engine.get_user_profile()
    print(f"用户画像: {profile}")
    
    print("✓ 聊天引擎综合测试通过")
    return True

def run_all_tests():
    print("\n" + "=" * 60)
    print(" SereneChat 功能测试")
    print("=" * 60 + "\n")
    
    tests = [
        ("基础聊天", test_basic_chat),
        ("记忆系统", test_memory_system),
        ("人设设定", test_character_preset),
        ("内容风控", test_content_moderation),
        ("OCR解析", test_ocr_parser),
        ("聊天引擎", test_chat_engine_features)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"✗ {name} 测试失败: {e}")
            results.append((name, False))
        print()
    
    # 打印测试结果汇总
    print("=" * 60)
    print(" 测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status} - {name}")
    
    print(f"\n  总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n  所有测试通过！")
        return True
    else:
        print(f"\n  有 {total - passed} 个测试失败")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
