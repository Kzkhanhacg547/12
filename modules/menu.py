import os
import random
from zlapi.models import Message, MultiMsgStyle, MessageStyle
import importlib

# Bảng màu hacker vibes
colors = [
    "00FF00", "33FF33", "66FF66", "99FF99", "00FFFF", "33FFFF", "FF00FF", "CC00FF", 
    "FF3300", "FF6600", "FF9900", "FFFF00", "FFFFFF", "000000"
]

# Kích thước ngẫu nhiên
sizes = ["12", "14", "16", "18", "20", "22"]

# Icon trang trí
icons = [
    "⚡", "🔥", "💻", "🔒", "🛠️", "📡", "✨", "💥", "🌀", "📀", "🎯"
]

des = {
    'version': "2.0.0",
    'credits': "Quốc Khánh x Nguyễn Đức Tài",
    'description': "Xem toàn bộ lệnh hiện có của bot với giao diện hacker"
}

def get_all_khanhdzzl():
    khanhdzzl = {}

    for module_name in os.listdir('modules'):
        if module_name.endswith('.py') and module_name != '__init__.py':
            module_path = f'modules.{module_name[:-3]}'
            module = importlib.import_module(module_path)

            if hasattr(module, 'get_szl'):
                module_khanhdzzl = module.get_szl()
                khanhdzzl.update(module_khanhdzzl)

    command_names = list(khanhdzzl.keys())
    return command_names

def handle_menu_command(message, message_object, thread_id, thread_type, author_id, client):
    command_names = get_all_khanhdzzl()

    total_khanhdzzl = len(command_names)
    numbered_khanhdzzl = [f"{random.choice(icons)} {i+1}. {name}" for i, name in enumerate(command_names)]

    header = "🌐 [Z MENU] 🌐\n"
    footer = "\n🚀 *Sẵn sàng hoạt động!* 🚀"
    menu_message = (
        f"{header}💡 Tổng số lệnh: {total_khanhdzzl}\n\n"
        + "\n".join(numbered_khanhdzzl)
        + footer
    )

    msg_length = len(menu_message)
    random_color = random.choice(colors)
    random_size = random.choice(sizes)

    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(header), style="color", color="FF0000", auto_format=False),
        MessageStyle(offset=0, length=len(header), style="bold", auto_format=False),
        MessageStyle(offset=len(header), length=msg_length - len(header), style="color", color=random_color, auto_format=False),
        MessageStyle(offset=0, length=msg_length, style="size", size=random_size, auto_format=True)
    ])

    message_to_send = Message(text=menu_message, style=style)
    client.replyMessage(message_to_send, message_object, thread_id, thread_type)

def get_szl():
    return {
        'menu': handle_menu_command
    }
