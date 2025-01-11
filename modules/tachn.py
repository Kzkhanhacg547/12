import os
from zlapi.models import Message
import requests
import json
import urllib.parse

des = {
    'version': "1.0.0",
    'credits': "",
    'description': "Tách nền hình ảnh từ file hoặc URL bằng API remove.bg."
}

REMOVE_BG_API_KEY = "vEB5hDuYwfT3WNs3YAGBuWEL"  # Thay bằng API key của bạn


def handle_tachn_command(message, message_object, thread_id, thread_type, author_id, client):
    if message_object.quote:
        attach = message_object.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
            except json.JSONDecodeError:
                client.sendMessage(
                    Message(text="Dữ liệu không hợp lệ."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            media_url = attach_data.get('hdUrl') or attach_data.get('href')
            if not media_url:
                client.sendMessage(
                    Message(text="Không tìm thấy URL."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            media_url = media_url.replace("\\/", "/")
            media_url = urllib.parse.unquote(media_url)
            result_url = remove_background_from_url(media_url)
            if result_url:
                send_processed_image(client, result_url, thread_id, thread_type)
            else:
                client.sendMessage(
                    Message(text="Không thể tách nền."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
        else:
            client.sendMessage(
                Message(text="Không có tệp nào được reply."),
                thread_id=thread_id,
                thread_type=thread_type
            )
    else:
        if message.startswith('.tachn '):
            url = message[6:].strip()
            if is_valid_image_url(url):
                result_url = remove_background_from_url(url)
                if result_url:
                    send_processed_image(client, result_url, thread_id, thread_type)
                else:
                    client.sendMessage(
                        Message(text="Không thể tách nền."),
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
            else:
                client.sendMessage(
                    Message(text="Vui lòng cung cấp URL ảnh hợp lệ."),
                    thread_id=thread_id,
                    thread_type=thread_type
                )
        else:
            client.sendMessage(
                Message(text="Vui lòng sử dụng lệnh 'tachn' để tách nền hình ảnh."),
                thread_id=thread_id,
                thread_type=thread_type
            )


def remove_background_from_url(image_url):
    api_url = "https://api.remove.bg/v1.0/removebg"
    headers = {"X-Api-Key": REMOVE_BG_API_KEY}
    data = {"image_url": image_url, "size": "auto"}

    try:
        response = requests.post(api_url, headers=headers, data=data, stream=True)
        if response.status_code == 200:
            output_file = "result.png"
            with open(output_file, "wb") as f:
                f.write(response.content)
            return upload_to_catbox(output_file)
        else:
            print(f"Error from remove.bg API: {response.text}")
    except requests.RequestException as e:
        print(f"Lỗi khi gọi remove.bg API: {e}")
    return None


def is_valid_image_url(url):
    try:
        response = requests.head(url)
        content_type = response.headers.get('Content-Type', '')
        return 'image/' in content_type
    except requests.RequestException as e:
        print(f"Lỗi khi kiểm tra URL: {e}")
    return False


def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    files = {'fileToUpload': (os.path.basename(file_path), open(file_path, 'rb'), 'image/png')}
    data = {'reqtype': 'fileupload'}

    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200 and response.text.startswith("http"):
            return response.text
        else:
            print(f"Lỗi khi upload Catbox: {response.text}")
    except requests.RequestException as e:
        print(f"Lỗi khi upload Catbox: {e}")
    return None


def send_processed_image(client, image_url, thread_id, thread_type):
    try:
        client.sendMessage(
            Message(text=f"Hình ảnh đã được xử lý: {image_url}"),
            thread_id=thread_id,
            thread_type=thread_type
        )
    except Exception as e:
        client.sendMessage(
            Message(text=f"Không thể gửi ảnh: {str(e)}"),
            thread_id=thread_id,
            thread_type=thread_type
        )


def get_szl():
    return {
        'tachn': handle_tachn_command
    }