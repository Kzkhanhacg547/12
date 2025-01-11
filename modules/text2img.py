import os
import json
import requests
from datetime import datetime
import pytz
from zlapi.models import Message, ZaloAPIException

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Generate images using Pollinations AI"
}

def ensure_directory():
    if not os.path.exists('./poli'):
        os.makedirs('./poli')

def get_vietnam_time():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    return datetime.now(tz).strftime("%H:%M:%S - %d/%M/%Y")

def handle_poli_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        # Extract query from message
        query = ' '.join(message.split()[1:])  # Remove command name
        if not query:
            error_message = Message(text="Vui lòng nhập nội dung để tạo hình ảnh")
            client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
            return

        # Ensure directory exists
        ensure_directory()

        # Generate unique filename
        filename = f"./poli/poli_{int(datetime.now().timestamp())}.png"

        # Get image from Pollinations API
        start_time = datetime.now()
        image_url = f"https://image.pollinations.ai/prompt/{query}"
        response = requests.get(image_url)
        response.raise_for_status()

        # Save image
        with open(filename, 'wb') as f:
            f.write(response.content)

        # Calculate processing time
        process_time = (datetime.now() - start_time).total_seconds()

        # Create response message
        response_text = (
            f"🎨 Đã tạo ảnh cho từ khóa: {query}\n"
            f"⏰ Thời gian: {get_vietnam_time()}\n"
            f"⏳ Thời gian xử lý: {process_time:.1f} giây"
        )

        # Send message with local image
        client.sendLocalImage(
            filename,
            message=Message(text=response_text),
            thread_id=thread_id,
            thread_type=thread_type
        )

        # Clean up
        os.remove(filename)

    except requests.exceptions.RequestException as e:
        error_message = Message(text=f"Lỗi khi tải ảnh: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
    except ZaloAPIException as e:
        error_message = Message(text=f"Lỗi Zalo API: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)

def get_szl():
    return {
        'poli': handle_poli_command
    }