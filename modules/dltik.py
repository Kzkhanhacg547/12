from zlapi.models import Message
import requests
import os

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Tải video, images tiktok"
}

def handle_tiktok_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập một đường link TikTok hợp lệ.")
        client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=60000)
        return

    video_link = content[1].strip()

    if not video_link.startswith("https://"):
        error_message = Message(text="Vui lòng nhập một đường link TikTok hợp lệ (bắt đầu bằng https://).")
        client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=60000)
        return

    api_url = f'https://www.tikwm.com/api/?url={video_link}'

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.6 Mobile/15E148 Safari/604.1'
        }

        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if 'data' not in data or 'play' not in data['data']:
            error_message = Message(text=f"Không thể lấy được link video từ API cho {video_link}.")
            client.sendMessage(error_message, thread_id, thread_type, ttl=60000)
            return

        videoUrl = data['data']['play']
        titlevd = data['data']['title']
        sendtitle = f"title: {titlevd}"
        messagesend = Message(text=sendtitle)

        # Download and send images if available
        image_urls = data['data'].get('images', [])
        if image_urls:
            image_paths = []
            for idx, img_url in enumerate(image_urls):
                image_path = f"temp_image_{idx}.jpg"
                with open(image_path, 'wb') as img_file:
                    img_file.write(requests.get(img_url, headers=headers).content)
                image_paths.append(image_path)

            client.sendMultiLocalImage(image_paths, thread_id, thread_type, message=messagesend, ttl=60000)

            for image_path in image_paths:
                if os.path.exists(image_path):
                    os.remove(image_path)

        thumbnailUrl = data['data']['cover'] or 'https://files.catbox.moe/gjg8fg.jpeg'
        duration = '1000'
        client.sendRemoteVideo(
            videoUrl,
            thumbnailUrl,
            duration=duration,
            message=messagesend,
            thread_id=thread_id,
            thread_type=thread_type,
            ttl=60000,
            width=1200,
            height=1600
        )

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=60000)
    except KeyError as e:
        error_message = Message(text=f"Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=60000)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi không xác định: {str(e)}")
        client.sendMessage(error_message, thread_id, thread_type, ttl=60000)

def get_szl():
    return {
        'dltik': handle_tiktok_command
    }
