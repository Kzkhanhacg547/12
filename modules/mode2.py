from zlapi.models import Message
import requests
import random
import pyshorteners
import urllib.parse

des = {
    'version': '1.0',
    'credits': 'Your Name',
    'description': 'Các lệnh hỗ trợ bot Zalo'
}

def get_szl():
    return {
        'capcutvd': handle_capcutvd_command,
        'ifcc': handle_ifcc_command,
        'catbot': handle_catbot_command,
        'link': handle_link_command,
        'dlfb': handle_dlfb_command
    }

def handle_capcutvd_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()
    if len(content) < 2:
        error_message = Message(text="❌ Vui lòng nhập từ khóa tìm kiếm video CapCut.")
        client.send(error_message, thread_id, thread_type)
        return

    keyword = " ".join(content[1:]).strip()

    try:
        encoded_keyword = urllib.parse.quote(keyword)
        api_url = f'https://subhatde.id.vn/capcut/search?keyword={encoded_keyword}'
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        if not data:
            raise KeyError("Không có video nào được tìm thấy cho từ khóa này.")

        video = random.choice(data)
        title = video.get('title', 'Không có tiêu đề')
        short_title = video.get('short_title', 'Không có tên ngắn')
        views = video.get('play_amount', 0)
        likes = video.get('like_count', 0)
        comments = video.get('comment_count', 0)
        author = video.get('author', {})
        author_name = author.get('name', 'Không có tác giả')
        author_id = author.get('unique_id', 'Không có tác giả ID')
        video_url = video.get('video_url', 'Không có video URL')

        thumbnail_url = "https://files.catbox.moe/ksg81k.jpg"
        duration = 1000

        quote = f"{title} ({short_title})\n" \
                f"   - Lượt xem: {views}\n" \
                f"   - Lượt thích: {likes}\n" \
                f"   - Lượt bình luận: {comments}\n" \
                f"   - Tác giả: {author_name} (@{author_id})\n" \
                f"   - Link video: {video_url}"

        message_to_send = Message(text=f"🤭 {quote}")
        client.sendRemoteVideo(
            video_url,
            thumbnail_url,
            duration=duration,
            message=message_to_send,
            thread_id=thread_id,
            thread_type=thread_type,
            width=1080,
            height=1920,
            ttl=120000
        )

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"❌ Đã xảy ra lỗi khi gọi API: {str(e)}")
        client.send(error_message, thread_id, thread_type)
    except KeyError as e:
        error_message = Message(text=f"❌ Dữ liệu từ API không đúng cấu trúc: {str(e)}")
        client.send(error_message, thread_id, thread_type)
    except Exception as e:
        error_message = Message(text=f"❌ Đã xảy ra lỗi không xác định: {str(e)}")
        client.send(error_message, thread_id, thread_type)

def handle_ifcc_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ")
    if len(parts) < 2:
        client.send(Message(text="❌ Vui lòng cung cấp URL."), thread_id, thread_type)
        return

    url = parts[1]
    api_url = f"https://subhatde.id.vn/capcut/info?url={url}"

    try:
        response = requests.get(api_url)
        data = response.json()
        user = data.get("user", {})
        user_info = (
            f"👤 Tên: {user.get('name', 'N/A')}\n"
            f"🎤 Mô tả: {user.get('description', 'Không có mô tả')}\n"
            f"🔗 Profile: https://www.tiktok.com/@{user.get('public_id')}"
        )

        client.send(Message(text=user_info), thread_id, thread_type)
    except Exception as e:
        client.send(Message(text=f"❌ Lỗi: {str(e)}"), thread_id, thread_type)

def handle_catbot_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ", 1)
    if len(parts) < 2:
        client.send(Message(text="❌ Vui lòng cung cấp URL."), thread_id, thread_type)
        return

    long_url = parts[1].strip()
    try:
        short_url = pyshorteners.Shortener().tinyurl.short(long_url)
        client.send(Message(text=f"🔗 Link rút gọn: {short_url}"), thread_id, thread_type)
    except Exception as e:
        client.send(Message(text=f"❌ Lỗi: {str(e)}"), thread_id, thread_type)

def handle_link_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ", 1)
    if len(parts) < 2:
        client.send(Message(text="❌ Vui lòng cung cấp URL."), thread_id, thread_type)
        return

    long_url = parts[1].strip()
    api_url = f'https://link4m.co/api-shorten/v2?api=66f43a0fb711e46de04d8c14&url={long_url}'

    try:
        response = requests.get(api_url)
        data = response.json()
        if data["status"] == "success":
            short_url = data["shortenedUrl"]
            client.send(Message(text=f"🔗 Link rút gọn: {short_url}"), thread_id, thread_type)
        else:
            client.send(Message(text="❌ Lỗi khi rút gọn URL."), thread_id, thread_type)
    except Exception as e:
        client.send(Message(text=f"❌ Lỗi: {str(e)}"), thread_id, thread_type)

def handle_dlfb_command(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ")
    if len(parts) < 2:
        client.send(Message(text="❌ Vui lòng cung cấp URL video."), thread_id, thread_type)
        return

    url = parts[1]
    api_url = f"https://subhatde.id.vn/fb/download?url={url}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            client.send(Message(text="✅ Video đã được tải."), thread_id, thread_type)
        else:
            client.send(Message(text="❌ Không thể tải video."), thread_id, thread_type)
    except Exception as e:
        client.send(Message(text=f"❌ Lỗi: {str(e)}"), thread_id, thread_type)
