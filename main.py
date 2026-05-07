
import json
import os
import time
import threading
from datetime import datetime
from src.chat_engine import ChatEngine

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_welcome(config):
    print("=" * 50)
    print(f" 欢迎使用 {config['skill_name']} v{config['version']}")
    print("=" * 50)
    print(f" {config['skill_description']}")
    print("-" * 50)
    print(" 功能特性:")
    for i, feature in enumerate(config['features'], 1):
        print(f"   {i}. {feature}")
    print("-" * 50)
    print(" 支持的聊天记录格式:")
    for fmt in config['supported_chat_formats']:
        print(f"   • {fmt}")
    print("-" * 50)
    print(" 安全提示: 本技能已启用内容风控系统")
    print(" 请勿发送色情、暴力等违规内容")
    print("=" * 50)

def print_menu():
    print("\n[聊天模式]")
    print("直接输入文字 - 与小龙虾聊天")
    print("输入 '导入' - 导入聊天记录文件")
    print("输入 '截图' - 导入聊天截图（OCR识别）")
    print("输入 '人设' - 查看/设置当前人设")
    print("输入 '记忆' - 查看记忆状态")
    print("输入 '画像' - 查看用户画像")
    print("输入 '主动' - 开启/关闭主动消息模式")
    print("输入 '真人' - 开启/关闭真人化回复模式")
    print("输入 '内心' - 查看小龙虾的内心独白")
    print("输入 '情绪' - 查看当前情绪状态")
    print("输入 '保存' - 保存当前对话")
    print("输入 '历史' - 查看聊天历史")
    print("输入 '清空' - 清空聊天记录")
    print("输入 '风控' - 查看风控状态")
    print("输入 '退出' - 退出程序")
    print("-" * 30)

def character_menu(engine):
    """人设菜单"""
    while True:
        print("\n[人设设置]")
        print("1. 查看当前人设")
        print("2. 创建新人设")
        print("3. 应用预设模板")
        print("4. 列出所有人设")
        print("5. 返回主菜单")
        print("-" * 30)
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            print(engine.get_character_info())
        
        elif choice == '2':
            if engine.create_character():
                print("人设创建成功！")
            else:
                print("人设创建失败")
        
        elif choice == '3':
            print("\n可用模板:")
            print("  tsundere - 傲娇型")
            print("  gentle - 温柔型")
            print("  energetic - 活力型")
            print("  mature - 成熟型")
            template = input("请选择模板: ").strip()
            if engine.apply_character_template(template):
                print(f"已应用模板: {template}")
            else:
                print("应用模板失败")
        
        elif choice == '4':
            presets = engine.list_character_presets()
            print("\n已保存的人设:")
            for preset in presets:
                print(f"  • {preset}")
        
        elif choice == '5':
            break

def proactive_message_loop(engine, stop_event, interval=30):
    """主动消息循环 - 在后台运行"""
    while not stop_event.is_set():
        time.sleep(interval)
        
        if stop_event.is_set():
            break
        
        # 检查是否需要发送主动消息
        message = engine.check_proactive_message()
        if message:
            print(f"\n[小龙虾主动消息] {message}")
            print("\n你: ", end="", flush=True)

def main():
    config = load_config()
    engine = ChatEngine()
    
    print_welcome(config)
    
    # 主动消息模式
    proactive_mode = False
    proactive_thread = None
    stop_event = threading.Event()
    
    while True:
        print_menu()
        
        user_input = input("你: ").strip()
        
        if user_input == '退出':
            if proactive_thread:
                stop_event.set()
                proactive_thread.join(timeout=1)
            print("小龙虾: 再见啦，记得常来找我玩哦")
            break
        
        elif user_input == '导入':
            filepath = input("请输入聊天记录文件路径: ").strip()
            if os.path.exists(filepath):
                success = engine.import_chat_history(filepath)
                if success:
                    print(f"小龙虾: 聊天记录导入成功！已学习到 {len(engine.get_chat_history())} 条消息")
                else:
                    print("小龙虾: 导入失败，文件格式可能不支持")
            else:
                print("小龙虾: 文件不存在，请检查路径")
        
        elif user_input == '截图':
            image_path = input("请输入聊天截图路径: ").strip()
            if os.path.exists(image_path):
                success = engine.import_chat_screenshot(image_path)
                if success:
                    print(f"小龙虾: 截图识别成功！")
                else:
                    print("小龙虾: 截图识别失败，请确保安装了OCR库")
                    print("提示: pip install pytesseract pillow")
                    print("同时需要安装Tesseract-OCR引擎")
            else:
                print("小龙虾: 文件不存在，请检查路径")
        
        elif user_input == '人设':
            character_menu(engine)
        
        elif user_input == '记忆':
            status = engine.get_memory_status()
            print("\n记忆状态:")
            print(f"  核心记忆: {status['core_memory']}")
            print(f"  临时记忆轮数: {status['temp_memory_turns']}")
            print(f"  临时记忆上下文: {status['temp_memory_context']}")
        
        elif user_input == '画像':
            profile = engine.get_user_profile()
            print("\n用户画像:")
            print(profile)
        
        elif user_input == '主动':
            proactive_mode = not proactive_mode
            if proactive_mode:
                print("小龙虾: 主动消息模式已开启！我会时不时找你聊天哦~")
                # 启动主动消息线程
                stop_event.clear()
                proactive_thread = threading.Thread(
                    target=proactive_message_loop,
                    args=(engine, stop_event, 30),  # 每30秒检查一次
                    daemon=True
                )
                proactive_thread.start()
            else:
                print("小龙虾: 主动消息模式已关闭")
                if proactive_thread:
                    stop_event.set()
                    proactive_thread.join(timeout=1)
                    proactive_thread = None
        
        elif user_input == '保存':
            filepath = input("请输入保存路径: ").strip()
            engine.save_chat_history(filepath)
            print(f"小龙虾: 聊天记录已保存到 {filepath}")
        
        elif user_input == '历史':
            history = engine.get_chat_history()
            if history:
                print("聊天历史:")
                for i, entry in enumerate(history, 1):
                    print(f"\n{i}.")
                    print(f"  你: {entry['user']}")
                    print(f"  小龙虾: {entry['bot']}")
            else:
                print("小龙虾: 还没有聊天记录呢")
        
        elif user_input == '清空':
            engine.clear_history()
            print("小龙虾: 聊天记录已清空")
        
        elif user_input == '风控':
            status = engine.get_moderation_status()
            print("风控状态:")
            print(f"  违规次数: {status['violation_count']}/{status['max_violations']}")
            print(f"  是否受限: {'是' if status['is_restricted'] else '否'}")

        elif user_input == '真人':
            enabled = engine.toggle_humanized_mode()
            if enabled:
                print("小龙虾: 真人化模式已开启！我会更像真人一样和你聊天")
            else:
                print("小龙虾: 真人化模式已关闭，恢复标准回复模式")

        elif user_input == '内心':
            monologue = engine.get_internal_monologue()
            if monologue:
                print(f"\n[小龙虾的内心独白] {monologue}")
            else:
                print("小龙虾: 我现在没什么特别的想法")

        elif user_input == '情绪':
            status = engine.get_emotion_status()
            print("\n情绪状态:")
            print(f"  当前情绪: {status['emotion']}")
            print(f"  情绪强度: {status['intensity']}")
            print(f"  关系阶段: {status['stage']}")
            print(f"  关系深度: {status['relationship_depth']}")
            print(f"  互动次数: {status['total_interactions']}")

        else:
            response = engine.chat(user_input)
            print(f"小龙虾: {response}")

if __name__ == '__main__':
    main()
