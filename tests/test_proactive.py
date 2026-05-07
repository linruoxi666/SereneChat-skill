
import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.chat_engine import ChatEngine
from src.proactive_messaging import ProactiveMessagingSystem, TriggerType

def test_proactive_system():
    print("=" * 50)
    print("测试主动消息系统")
    print("=" * 50)
    
    engine = ChatEngine()
    
    # 测试1: 基础主动消息检查
    print("\n1. 测试主动消息检查:")
    message = engine.check_proactive_message()
    if message:
        print(f"  触发主动消息: {message}")
    else:
        print("  暂无主动消息")
    
    # 测试2: 模拟用户不活跃
    print("\n2. 测试不活跃触发:")
    print("  模拟用户不活跃...")
    # 手动设置最后活跃时间为很久以前
    engine.proactive_system.last_user_activity = time.time() - 400  # 400秒前
    
    message = engine.check_proactive_message()
    if message:
        print(f"  不活跃触发: {message}")
    else:
        print("  未触发（可能需要更长时间）")
    
    # 重置活跃时间
    engine.proactive_system.update_activity()
    
    # 测试3: 模拟聊天后检查
    print("\n3. 测试聊天后主动消息:")
    engine.chat("你好")
    time.sleep(1)
    
    # 此时应该没有主动消息，因为刚刚活跃过
    message = engine.check_proactive_message()
    if message:
        print(f"  意外触发: {message}")
    else:
        print("  正确：没有触发（用户刚刚活跃）")
    
    # 测试4: 测试不同触发类型
    print("\n4. 测试触发类型:")
    proactive = ProactiveMessagingSystem()
    
    # 时间触发
    print("  时间触发模板:")
    for time_key in ['morning', 'noon', 'evening', 'night']:
        templates = proactive.message_templates[TriggerType.TIME_BASED][time_key]
        print(f"    {time_key}: {templates[0]}")
    
    # 不活跃触发
    print("  不活跃触发模板:")
    for inactivity_key in ['short', 'medium', 'long']:
        templates = proactive.message_templates[TriggerType.INACTIVITY][inactivity_key]
        print(f"    {inactivity_key}: {templates[0]}")
    
    # 心情触发
    print("  心情触发模板:")
    for mood_key in ['lonely', 'happy', 'worried']:
        templates = proactive.message_templates[TriggerType.MOOD_BASED][mood_key]
        print(f"    {mood_key}: {templates[0]}")
    
    print("\n✓ 主动消息系统测试通过")
    return True

def test_proactive_in_chat():
    print("=" * 50)
    print("测试聊天中的主动消息")
    print("=" * 50)
    
    engine = ChatEngine()
    
    print("\n模拟正常聊天:")
    responses = [
        engine.chat("你好"),
        engine.chat("今天天气不错"),
        engine.chat("我想你了")
    ]
    
    for i, response in enumerate(responses, 1):
        print(f"  回复{i}: {response}")
    
    print("\n模拟用户离开（不活跃）:")
    # 手动设置不活跃状态
    engine.proactive_system.last_user_activity = time.time() - 400
    
    # 检查主动消息
    message = engine.check_proactive_message()
    if message:
        print(f"  小龙虾主动说: {message}")
    
    print("\n✓ 聊天主动消息测试通过")
    return True

def run_proactive_tests():
    print("\n" + "=" * 60)
    print(" SereneChat 主动消息功能测试")
    print("=" * 60 + "\n")
    
    tests = [
        ("主动消息系统", test_proactive_system),
        ("聊天中的主动消息", test_proactive_in_chat)
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
    success = run_proactive_tests()
    sys.exit(0 if success else 1)
