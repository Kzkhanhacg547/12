import json
import requests
from zlapi.models import Message

# Load API URL từ file cấu hình
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")
print("API Link: ", API_URL)

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Gửi video ngẫu nhiên"
}

# Cấu hình cho API video ngẫu nhiên
RANDOM_VIDEO_CONFIG = {
    'message': "🌟====𝐓𝐡ô𝐧𝐠 𝐓𝐢𝐧 𝐀𝐝𝐦𝐢𝐧====🌟\n👀 Tên: 𝐁ù𝐢 𝐕ă𝐧 𝐊𝐡á𝐧𝐡\n👤 Giới tính: 𝐍𝐚𝐦\n🙄 Sinh ngày: 𝟏𝟎/𝟏𝟏/𝟐𝟎𝟎𝟕\n💫 Chiều cao × cân nặng: 𝟏𝐦𝟕 × 𝟕𝟐𝐤𝐠\n😎 Quê quán: 𝐇ả𝐢 𝐃ươ𝐧𝐠\n🤔 Nơi ở: 𝐆𝐢𝐚 𝐋𝐚𝐢\n🌸 Cung: 𝐁ọ 𝐂ạ𝐩\n🌸 Tính cách: Quen Lâu Là Biết ❤️\n📱 Facebook: https://fb.me/kzkhanh547\n[ ✰ ]=== [  𝐊𝐳 𝐁𝐨𝐭𝐭 ] ===[ ✰ ]\n",
    'endpoint': "/ad",
    'data_key': 'url',
    'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
}

def kzkhanhh(message, message_object, thread_id, thread_type, author_id, client):
    config = RANDOM_VIDEO_CONFIG
    message_to_send = Message(text=config['message'])
    client.send(message_to_send, thread_id, thread_type)

    api_url = f"{API_URL}{config['endpoint']}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        # Gọi API để lấy video
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        video_url = data.get(config['data_key'], '')
        thumbnail_url = config['thumbnail']
        duration = '1000'

        # Gửi video
        client.sendRemoteVideo(
            video_url,
            thumbnail_url,
            duration=duration,
            message=None,
            thread_id=thread_id,
            thread_type=thread_type,
            ttl=120000,
            width=1080,
            height=1920
        )

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"❌ Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.send(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"❌ Đã xảy ra lỗi: {str(e)}")
        client.send(error_message, thread_id, thread_type)


def get_szl():
    return {
        'kzkhanhh': kzkhanhh 
    }
