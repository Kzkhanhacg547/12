import json
import requests
from zlapi.models import Message
import os

# Tải cấu hình API từ file
CONFIG_FILE = 'setting.json'
def load_config():
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)

config = load_config()
API_URL = config.get("API", "")

print(f"\u2728 API Link by Kz Khánhh: {API_URL} \u2728")

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Hệ thống gửi ảnh anime độc quyền by Kz Khánhh!"
}

def handle_anhgai_command(message, message_object, thread_id, thread_type, author_id, client):
    message_to_send = Message(text="\u2728 BOT CUTE xin gửi bạn ảnh girl dưới đây! \u2728")

    api_url = f"{API_URL}/girl"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Kz-Khanhh-Custom-Header': 'AnimeImageRequest'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        image_url = data.get('url')

        if not image_url:
            raise ValueError("\u274c API không cung cấp URL ảnh!")

        image_response = requests.get(image_url, headers=headers)
        image_response.raise_for_status()

        image_path = 'temp_image_kz_khanhh.jpeg'
        with open(image_path, 'wb') as f:
            f.write(image_response.content)

        client.sendLocalImage(
            image_path, 
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1200,
            height=1600
        )

        os.remove(image_path)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"\u274c Lỗi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)
    except Exception as e:
        error_message = Message(text=f"\u274c Lỗi khác: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)


def get_szl():
    return {
        'girl': handle_anhgai_command
    }