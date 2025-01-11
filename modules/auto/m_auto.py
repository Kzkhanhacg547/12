# Mẫu lệnh auto (đặt trong thư mục /modules/auto/example_auto.py)
import time
import threading
from zlapi.models import Message, ThreadType
from zlapi._message import Mention

def start_auto(client):
    while True:
        try:
            # Logic của lệnh tự động ở đây
            print("Auto command is running...")
            # Ví dụ: Gửi tin nhắn tự động sau mỗi 1 giờ
            # thread_id = "your_thread_id"
            # client.send(Message(text="Auto message"), thread_id, ThreadType.GROUP)

            # Delay 1 giờ
            time.sleep(1800)
        except Exception as e:
            print(f"Error in auto command: {e}")
            time.sleep(10)  # Delay ngắn nếu có lỗi