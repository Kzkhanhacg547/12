import os
import json
import requests
from datetime import datetime
import pytz
from zlapi.models import Message, ZaloAPIException
import random

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Xem bói bài tarot"
}

def get_vietnam_time():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return datetime.now(tz).strftime("%H:%M:%S - %d/%M/%Y")

def load_tarot_data():
    try:
        response = requests.get('https://raw.githubusercontent.com/Kzkhanhacg547/Kz-BOT/refs/heads/main/tarot_data.json')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise Exception(f"Không thể tải dữ liệu tarot: {str(e)}")

def ensure_cache_directory():
    if not os.path.exists('./tarot_cache'):
        os.makedirs('./tarot_cache')

def handle_tarot_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        # Đảm bảo thư mục cache tồn tại
        ensure_cache_directory()

        # Tải dữ liệu tarot
        tarot_data = load_tarot_data()

        # Xử lý tham số đầu vào
        parts = message.split()
        if len(parts) > 1 and parts[1].isdigit():
            card_index = int(parts[1])
            if card_index >= len(tarot_data):
                error_message = Message(text="Số thẻ bài không hợp lệ!")
                client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
                return
        else:
            card_index = random.randint(0, len(tarot_data) - 1)

        # Lấy thông tin lá bài
        card = tarot_data[card_index]

        # Tải và lưu ảnh
        image_filename = f"./tarot_cache/tarot_{int(datetime.now().timestamp())}.jpg"
        response = requests.get(card['image'])
        response.raise_for_status()

        with open(image_filename, 'wb') as f:
            f.write(response.content)

        # Tạo nội dung tin nhắn
        message_text = (
            f"🔮==[ BÓI TAROT ]==🔮\n\n"
            f"🃏 Tên lá bài: {card['name']}\n"
            f"⚜️ Thuộc bộ: {card['suite']}\n"
            f"💭 Mô tả: {card['vi']['description']}\n"
            f"📖 Ý nghĩa: {card['vi']['interpretation']}\n"
            f"🀄 Lá bài ngược: {card['vi']['reversed']}\n\n"
            f"⏰ Thời gian xem: {get_vietnam_time()}"
        )

        # Gửi tin nhắn với ảnh
        client.sendLocalImage(
            image_filename,
            message=Message(text=message_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

        # Dọn dẹp file cache
        os.remove(image_filename)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Lỗi khi tải dữ liệu: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
    except ZaloAPIException as e:
        error_message = Message(text=f"Lỗi Zalo API: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)

def get_szl():
    return {
        'tarot': handle_tarot_command
    }