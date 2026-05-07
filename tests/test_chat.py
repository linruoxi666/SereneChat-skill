
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.chat_engine import ChatEngine
from src.chat_parser import ChatParser

def test_personality():
    print("测试人格模块...")
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
    
    print("人格模块测试完成")

def test_chat_parser():
    print("\n测试聊天记录解析...")
    
    test_content = """
[2024-01-15 10:30:00] 小明: 你好呀
[2024-01-15 10:31:00] 小红: 你好，今天天气不错
[2024-01-15 10:32:00] 小明: 是啊，要不要一起出去玩
"""
    
    records = ChatParser.parse_wechat(test_content)
    print(f"解析到 {len(records)} 条消息")
    for record in records:
        print(f"{record.sender}: {record.content}")
    
    print("聊天记录解析测试完成")

def test_import_functionality():
    print("\n测试聊天记录导入...")
    
    test_file = os.path.join(os.path.dirname(__file__), 'test_chat.txt')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("""
[2024-01-15 10:30:00] 用户: 嗨，在吗
[2024-01-15 10:31:00] 用户: 今天过得怎么样
[2024-01-15 10:32:00] 用户: 想和你聊聊天
""")
    
    engine = ChatEngine()
    success = engine.import_chat_history(test_file)
    
    if success:
        print(f"导入成功，共 {len(engine.get_chat_history())} 条消息")
        for entry in engine.get_chat_history():
            print(f"用户: {entry['user']}")
            print(f"小龙虾: {entry['bot']}")
            print()
    else:
        print("导入失败")
    
    os.remove(test_file)
    print("聊天记录导入测试完成")

if __name__ == '__main__':
    test_personality()
    test_chat_parser()
    test_import_functionality()
    print("\n所有测试完成！")
