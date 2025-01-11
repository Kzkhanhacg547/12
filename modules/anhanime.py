import json
import requests
from zlapi.models import Message
import os

# Load API URL từ file cấu hình
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")
print("API Link: ", API_URL)

des = {
    'version': "1.0.0",
    'credits': "Nguyễn Phi Hoàng",
    'description': "Gửi ảnh anime từ API"
}

def handle_anhgai_command(message, message_object, thread_id, thread_type, author_id, client):
    message_to_send = Message(text="Dưới đây là ảnh anime của bạn!")

    # URL endpoint để lấy ảnh anime
    api_url = f"{API_URL}/anime"
    try:
        # Header để mô phỏng trình duyệt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Gửi yêu cầu GET tới API
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        # Parse kết quả từ API
        data = response.json()
        image_url = data.get('url', None)

        if not image_url:
            raise ValueError("Không tìm thấy URL ảnh trong phản hồi từ API.")

        # Tải ảnh từ URL
        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()

        # Lưu ảnh tạm thời
        image_path = 'temp_image.jpeg'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        # Gửi ảnh qua client
        client.sendLocalImage(
            image_path, 
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1200,
            height=1600
        )

        # Xoá ảnh sau khi gửi
        os.remove(image_path)

    except requests.exceptions.RequestException as e:
        # Lỗi khi gọi API
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)
    except Exception as e:
        # Các lỗi khác
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)

def get_szl():
    return {
        'anhanime': handle_anhgai_command
    }
