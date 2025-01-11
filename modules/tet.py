import json
import requests
from zlapi.models import Message

des = {
    'version': "1.0.2",
    'credits': "Kz Khánhh",
    'description': "Gửi audio MP3"
}

def handle_audio_command(message, message_object, thread_id, thread_type, author_id, client):
    uptime_message = "Audio MP3 của bạn đây."
    message_to_send = Message(text=uptime_message)

    # Load API URL from configuration file
    with open('setting.json', 'r') as config_file:
        config = json.load(config_file)
    API_URL = config.get("API", "")

    api_url = f"{API_URL}/tet2"  # Adjust endpoint as needed
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        audio_url = data.get('url', '')

        # Send the audio using sendRemoteVoice instead of sendRemoteVideo
        client.sendRemoteVoice(
            audio_url,
            thread_id=thread_id,
            thread_type=thread_type,
            ttl=120000
        )

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)

def get_szl():
    return {
        'tet': handle_audio_command  # Changed command name from 'vdtet' to 'audio'
    }