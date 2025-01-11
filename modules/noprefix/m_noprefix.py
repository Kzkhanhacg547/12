# Mẫu lệnh noprefix (đặt trong thư mục /modules/noprefix/example_noprefix.py)
from zlapi.models import Message, ThreadType
from zlapi._message import Mention

des = {
    'version': '1.0',
    'credits': 'Your Name',
    'description': 'Mô tả về chức năng của lệnh noprefix'
}

def get_szl():
    return {
        'trigger_word': handle_noprefix  # từ khoá kích hoạt lệnh
    }

def handle_noprefix(message, message_object, thread_id, thread_type, author_id, client):
    # Xử lý logic của lệnh noprefix ở đây
    response = "Đây là phản hồi từ lệnh noprefix"
    client.send(Message(text=response), thread_id, thread_type)
