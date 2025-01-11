# modules/canva_commands.py
import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from zlapi.models import Message, ThreadType
from zlapi._message import Mention

des = {
    'version': '1.0',
    'credits': 'Your Name',
    'description': 'Các lệnh xử lý ảnh và video như canva, thư pháp, tìm kiếm video TikTok'
}

def get_szl():
    return {
        'canva': handle_canva,
        'thuphap': handle_thuphap,
        'ttsr': handle_ttsr
    }

def handle_canva(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ", 1)
    if len(parts) < 2:
        client.send(
            Message(text="⚠️ Vui lòng cung cấp nội dung cần vẽ lên ảnh!"),
            thread_id,
            thread_type
        )
        return

    text_to_draw = parts[1]

    # Kiểm tra thư mục canva
    canva_folder = 'canva'
    image_files = [f for f in os.listdir(canva_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]
    if not image_files:
        client.send(
            Message(text="⚠️ Không tìm thấy ảnh trong thư mục 'canva'."),
            thread_id,
            thread_type
        )
        return

    # Kiểm tra thư mục font
    font_folder = 'font'
    font_files = [f for f in os.listdir(font_folder) if f.endswith('.ttf')]
    if not font_files:
        client.send(
            Message(text="⚠️ Không tìm thấy font trong thư mục 'font'."),
            thread_id,
            thread_type
        )
        return

    try:
        # Xử lý ảnh
        selected_image = random.choice(image_files)
        selected_font = random.choice(font_files)
        image_path = os.path.join(canva_folder, selected_image)
        font_path = os.path.join(font_folder, selected_font)

        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, 500)

        # Tính toán vị trí text
        bbox = draw.textbbox((0, 0), text_to_draw, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        width, height = image.size
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # Vẽ text
        random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        draw.text(position, text_to_draw, font=font, fill=random_color)

        # Lưu và gửi ảnh
        output_path = "output_image.png"
        image.save(output_path)
        client.sendLocalImage(output_path, thread_id=thread_id, thread_type=thread_type)
        os.remove(output_path)

    except Exception as e:
        client.send(
            Message(text=f"⚠️ Đã xảy ra lỗi khi xử lý ảnh: {str(e)}"),
            thread_id,
            thread_type
        )

def handle_thuphap(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 4:
        client.send(
            Message(text="💬 Vui lòng nhập 3 tên để vẽ thư pháp (sử dụng lệnh #thuphap name)."),
            thread_id,
            thread_type
        )
        return

    name_1, name_2, name_3 = content[1:4]
    api_url = f"https://api.ntmdz.online/thuphap?id=1&sodong=3&dong_1={name_1}&dong_2={name_2}&dong_3={name_3}"

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            image_path = 'thuphap_image.jpeg'
            with open(image_path, 'wb') as f:
                f.write(response.content)

            success_message = f"💬 Thư pháp với các tên: {name_1}, {name_2}, {name_3} đã được vẽ thành công!"
            client.sendLocalImage(
                image_path,
                message=Message(text=success_message),
                thread_id=thread_id,
                thread_type=thread_type
            )
            os.remove(image_path)
        else:
            client.send(
                Message(text="❌ Đã xảy ra lỗi khi vẽ thư pháp. Vui lòng thử lại."),
                thread_id,
                thread_type
            )
    except Exception as e:
        client.send(
            Message(text=f"❌ Đã xảy ra lỗi: {str(e)}"),
            thread_id,
            thread_type
        )

def handle_ttsr(message, message_object, thread_id, thread_type, author_id, client):
    parts = message.split(" ")
    if len(parts) <= 1:
        client.send(
            Message(text="⚠️ Vui lòng cung cấp tên tìm kiếm sau lệnh !ttsr"),
            thread_id,
            thread_type
        )
        return

    search_name = parts[1]
    api_url = f'https://subhatde.id.vn/tiktok/searchvideo?keywords={search_name}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if data["code"] == 0 and data['data']['videos']:
            video = data['data']['videos'][0]
            video_url = video['play']
            video_cover = video['cover']
            title = video['title']

            # Tải và gửi thumbnail
            temp_image_path = download_image(video_cover)
            if temp_image_path:
                client.sendLocalImage(temp_image_path, thread_id, thread_type)
                os.remove(temp_image_path)

            # Gửi video
            client.sendRemoteVideo(
                video_url,
                'https://files.catbox.moe/ksg81k.jpg',
                duration=100,
                message=Message(text=f"🎥 Video tìm kiếm: {title}"),
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920
            )
        else:
            client.send(
                Message(text="💢 Không tìm thấy video phù hợp với từ khóa."),
                thread_id,
                thread_type
            )

    except Exception as e:
        client.send(
            Message(text=f"🚦 Có lỗi xảy ra trong quá trình tìm kiếm video: {str(e)}"),
            thread_id,
            thread_type
        )

def download_image(image_url):
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        temp_image_path = "temp_image.jpg"
        with open(temp_image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return temp_image_path
    except:
        return None