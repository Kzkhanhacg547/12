from zlapi.models import Message
import json
import urllib.parse
import os
import requests
import yt_dlp

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Trích xuất âm thanh từ video và cung cấp link tải"
}

def download_audio(video_url):
    """Download audio from video URL using yt-dlp"""
    try:
        output_file = 'audio_output.mp3'
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': output_file.replace('.mp3', ''),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        return output_file
    except Exception as e:
        print(f"Lỗi tải audio: {str(e)}")
        return None

def upload_to_host(file_name):
    """Upload file to hosting service"""
    try:
        with open(file_name, 'rb') as file:
            files = {'files[]': file}
            response = requests.post('https://uguu.se/upload', files=files).json()
            if response['success']:
                return response['files'][0]['url']
            return False
    except Exception as e:
        print(f"Lỗi upload: {e}")
        return False

def send_audio_and_link(audio_url, thread_id, thread_type, client, file_size):
    """Send both audio file and download link"""
    # Gửi file âm thanh
    client.sendRemoteVoice(audio_url, thread_id, thread_type, fileSize=file_size)

    # Gửi link download
    download_message = Message(text=f"🎵 Link tải MP3: {audio_url}")
    client.send(download_message, thread_id, thread_type)

def handle_getaudio_command(message, message_object, thread_id, thread_type, author_id, client):
    """Handle the getaudio command"""
    if message_object.quote:
        attach = message_object.quote.attach
        if attach:
            try:
                attach_data = json.loads(attach)
                video_url = attach_data.get('hdUrl') or attach_data.get('href')

                if video_url:
                    # Thông báo đang xử lý
                    client.send(Message(text="⏳ Đang xử lý video..."), thread_id, thread_type)

                    # Download audio from video
                    audio_file = download_audio(video_url)

                    if audio_file and os.path.exists(audio_file):
                        # Upload audio to host
                        audio_url = upload_to_host(audio_file)

                        if audio_url:
                            # Send audio file and download link
                            file_size = os.path.getsize(audio_file)
                            send_audio_and_link(audio_url, thread_id, thread_type, client, file_size)

                            # Cleanup
                            os.remove(audio_file)
                        else:
                            send_error_message(thread_id, thread_type, client, "Không thể tải audio lên host.")
                    else:
                        send_error_message(thread_id, thread_type, client, "Không thể tải xuống audio từ video.")
                else:
                    send_error_message(thread_id, thread_type, client)
            except json.JSONDecodeError as e:
                print(f"Lỗi phân tích JSON: {str(e)}")
                send_error_message(thread_id, thread_type, client)
        else:
            send_error_message(thread_id, thread_type, client)
    else:
        send_error_message(thread_id, thread_type, client)

def send_error_message(thread_id, thread_type, client, error_message="Vui lòng reply video cần trích xuất âm thanh."):
    """Send error message to chat"""
    if hasattr(client, 'send'):
        client.send(Message(text=error_message), thread_id, thread_type)
    else:
        print("Client không hỗ trợ gửi tin nhắn.")

def get_szl():
    return {
        'getaudio': handle_getaudio_command
    }