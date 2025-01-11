import json
import requests
from zlapi.models import Message

# Load API URL from configuration file
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")
print("API Link: ", API_URL)

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Gửi video đa dạng"
}

# Dictionary mapping command types to their configurations
VIDEO_CONFIGS = {
    'vdanime': {
        'message': "Video anime của bạn đây.",
        'endpoint': "/vdanime",
        'data_key': 'data',
        'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
    },
    'vdgirl': {
        'message': "Video gái của bạn đây.",
        'endpoint': "/vdgirl",
        'data_key': 'url',
        'thumbnail': 'https://curly-capybara-4jjp9w9vg6vc57rq-2007.app.github.dev/gaiaodai'

    },
    'vdaodai': {
        'message': "Video gái của bạn đây.",
        'endpoint': "/vdnuaodai",
        'data_key': 'url',
        'thumbnail': 'https://curly-capybara-4jjp9w9vg6vc57rq-2007.app.github.dev/gaiaodai'
    },
    'vdchill': {
        'message': "Video vdchill của bạn đây.",
        'endpoint': "/chill",
        'data_key': 'url',
        'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
    },
    'vdcos': {
        'message': "Video vdcos của bạn đây.",
        'endpoint': "/vdcosplay",
        'data_key': 'data',
        'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
    },
    'vdtamtrang': {
        'message': "Video vdtamtrang của bạn đây.",
        'endpoint': "/tamtrang",
        'data_key': 'url',
        'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
    },
    'vdtrai': {
        'message': "Video của bạn đây.",
        'endpoint': "/vdtrai",
        'data_key': 'url',
        'thumbnail': 'https://files.catbox.moe/gjg8fg.jpeg'
    },
    'vdloli': {
        'message': "Video loli tiktok của bạn đây.",
        'endpoint': "/images/vdloli",
        'data_key': 'url',
        'thumbnail': 'https://curly-capybara-4jjp9w9vg6vc57rq-2007.app.github.dev/gaiaodai'

    }
}

def handle_video_command(command_type, message, message_object, thread_id, thread_type, author_id, client):
    config = VIDEO_CONFIGS[command_type]
    uptime_message = config['message']
    message_to_send = Message(text=uptime_message)

    api_url = f"{API_URL}{config['endpoint']}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        video_url = data.get(config['data_key'], '')
        thumbnail_url = config['thumbnail']
        duration = '1000'

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
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=120000)

def get_szl():
    commands = {}
    for command_type in VIDEO_CONFIGS.keys():
        commands[command_type] = lambda m, mo, tid, tt, aid, c, ct=command_type: handle_video_command(ct, m, mo, tid, tt, aid, c)
    return commands