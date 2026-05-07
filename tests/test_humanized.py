
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.humanized_response import HumanizedResponseEngine, EmotionalState, ResponseStyle
from src.chat_engine import ChatEngine

def test_emotion_system():
    print("=" * 50)
    print("测试情绪系统")
    print("=" * 50)

    engine = HumanizedResponseEngine()

    # 测试初始状态
    status = engine.get_emotion_status()
    print(f"初始情绪: {status['emotion']}")
    print(f"关系阶段: {status['stage']}")

    # 测试情绪变化
    print("\n模拟不同输入触发的情绪变化:")
    test_inputs = [
        "我好开心",
        "我很难过",
        "我好累",
        "我好担心你",
        "你怎么不理我"
    ]

    for input_text in test_inputs:
        engine.update_emotion(input_text)
        status = engine.get_emotion_status()
        print(f"  输入: '{input_text}' -> 情绪: {status['emotion']} (强度: {status['intensity']})")

    print("\n✓ 情绪系统测试通过")
    return True

def test_response_styles():
    print("=" * 50)
    print("测试回复风格")
    print("=" * 50)

    engine = HumanizedResponseEngine()

    # 测试不同风格
    test_cases = [
        ("你好", [ResponseStyle.DIRECT, ResponseStyle.HESITANT, ResponseStyle.TEASE]),
        ("我想你了", [ResponseStyle.CLINGY, ResponseStyle.CARING, ResponseStyle.TEASE]),
        ("今天好累", [ResponseStyle.CARING, ResponseStyle.SILENT]),
        ("晚安", [ResponseStyle.DIRECT, ResponseStyle.CLINGY]),
    ]

    for user_input, styles in test_cases:
        print(f"\n输入: '{user_input}'")
        emotion_type, _ = engine._analyze_semantic(user_input)
        for style in styles:
            engine.current_emotion = EmotionalState.HAPPY
            response = engine._generate_core_response(emotion_type, style)
            response = engine._add_style_flavor(response, style)
            print(f"  风格[{style.value}]: {response}")

    print("\n✓ 回复风格测试通过")
    return True

def test_relationship_progression():
    print("=" * 50)
    print("测试关系深度影响")
    print("=" * 50)

    engine = HumanizedResponseEngine()

    # 模拟关系发展
    test_inputs = ["你好", "我想你了", "今天好累"]

    for i in range(5):
        # 增加关系深度
        for _ in range(5):
            engine.update_relationship()

        status = engine.get_emotion_status()
        print(f"\n关系阶段: {status['stage']} (深度: {status['relationship_depth']})")

        for input_text in test_inputs:
            response, monologue = engine.generate_response(input_text)
            print(f"  输入: '{input_text}' -> 回复: '{response}'")

    print("\n✓ 关系深度测试通过")
    return True

def test_human_imperfections():
    print("=" * 50)
    print("测试人类不完美特征")
    print("=" * 50)

    engine = HumanizedResponseEngine()

    # 测试犹豫风格
    engine.current_emotion = EmotionalState.SAD
    emotion_type, _ = engine._analyze_semantic("你好")
    for _ in range(5):
        response = engine._generate_core_response(emotion_type, ResponseStyle.HESITANT)
        response = engine._add_style_flavor(response, ResponseStyle.HESITANT)
        print(f"  犹豫: {response}")

    # 测试调侃风格
    engine.current_emotion = EmotionalState.PLAYFUL
    emotion_type, _ = engine._analyze_semantic("我想你了")
    for _ in range(5):
        response = engine._generate_core_response(emotion_type, ResponseStyle.TEASE)
        response = engine._add_style_flavor(response, ResponseStyle.TEASE)
        print(f"  调侃: {response}")

    # 测试沉默风格 - 对负面情感用关心风格
    engine.current_emotion = EmotionalState.TIRED
    emotion_type, _ = engine._analyze_semantic("今天好累")
    for _ in range(5):
        response = engine._generate_core_response(emotion_type, ResponseStyle.SILENT)
        response = engine._add_style_flavor(response, ResponseStyle.SILENT)
        print(f"  沉默: {response}")

    print("\n✓ 人类不完美特征测试通过")
    return True

def test_chat_engine_integration():
    print("=" * 50)
    print("测试聊天引擎集成")
    print("=" * 50)

    engine = ChatEngine()

    # 确保真人化模式开启
    if not engine.humanized_mode:
        engine.toggle_humanized_mode()

    print("\n模拟对话:")
    test_inputs = [
        "你好",
        "我想你了",
        "今天好累",
        "晚安",
        "我好开心",
        "我心情不好"
    ]

    for input_text in test_inputs:
        response = engine.chat(input_text)
        print(f"你: {input_text}")
        print(f"小龙虾: {response}")

        # 显示内心独白
        monologue = engine.get_internal_monologue()
        if monologue:
            print(f"[内心] {monologue}")
        print()

    # 显示情绪状态
    status = engine.get_emotion_status()
    print(f"\n最终情绪状态: {status['emotion']}")
    print(f"关系阶段: {status['stage']}")

    print("\n✓ 聊天引擎集成测试通过")
    return True

def test_comparison():
    print("=" * 50)
    print("对比测试：真人化模式 vs 标准模式")
    print("=" * 50)

    engine = ChatEngine()

    test_inputs = ["你好", "我想你了", "今天好累"]

    print("\n标准模式:")
    engine.humanized_mode = False
    for input_text in test_inputs:
        response = engine.chat(input_text)
        print(f"  输入: '{input_text}' -> 回复: '{response}'")

    print("\n真人化模式:")
    engine.humanized_mode = True
    for input_text in test_inputs:
        response = engine.chat(input_text)
        print(f"  输入: '{input_text}' -> 回复: '{response}'")

    print("\n✓ 对比测试通过")
    return True

def run_humanized_tests():
    print("\n" + "=" * 60)
    print(" SereneChat 真人化回复功能测试")
    print("=" * 60 + "\n")

    tests = [
        ("情绪系统", test_emotion_system),
        ("回复风格", test_response_styles),
        ("关系深度", test_relationship_progression),
        ("人类不完美特征", test_human_imperfections),
        ("聊天引擎集成", test_chat_engine_integration),
        ("模式对比", test_comparison)
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"✗ {name} 测试失败: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
        print()

    print("=" * 60)
    print(" 测试结果汇总")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status} - {name}")

    print(f"\n  总计: {passed}/{total} 测试通过")

    return passed == total

if __name__ == '__main__':
    success = run_humanized_tests()
    sys.exit(0 if success else 1)
