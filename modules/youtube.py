from zlapi.models import Message
from config import PREFIX
import requests
import urllib.parse
from youtube_search import YoutubeSearch 
import json

des = {
    'version': "1.9.2",
    'credits': "Nguyễn Phi Hoàng",
    'description': "𝕋𝕚̀𝕞 𝕜𝕚𝕖̂́𝕞 𝕧𝕚𝕕𝕖𝕠 𝕥𝕣𝕖̂𝕟 𝕐𝕠𝕦𝕋𝕦𝕓𝕖"
}

def translate_time(publish_time):
    translations = {
        'day': 'ngày', 'days': 'ngày',
        'hour': 'giờ', 'hours': 'giờ',
        'minute': 'phút', 'minutes': 'phút',
        'second': 'giây', 'seconds': 'giây',
        'week': 'tuần', 'weeks': 'tuần',
        'month': 'tháng', 'months': 'tháng',
        'year': 'năm', 'years': 'năm',
        'ago': 'trước'
    }
    for eng, viet in translations.items():
        publish_time = publish_time.replace(eng, viet)
    return publish_time

def translate_views(views):
    views = views.replace('views', 'lượt xem')
    return views

def handle_ytb_command(message, message_object, thread_id, thread_type, author_id, client):
    text = message.split()

    if len(text) < 2:
        error_message = Message(text="Vui lòng nhập từ khóa để tìm kiếm video trên YouTube.")
        client.sendMessage(error_message, thread_id, thread_type)
        return

    query = " ".join(text[1:])

    results = YoutubeSearch(query, max_results=5).to_json()
    data = json.loads(results)

    if not data['videos']:
        no_result_message = Message(text=f"Không tìm thấy kết quả cho từ khóa: {query}")
        client.sendMessage(no_result_message, thread_id, thread_type)
        return

    message_to_send = ""
    for idx, video in enumerate(data['videos'], 1):
        translated_time = translate_time(video['publish_time'])
        translated_views = translate_views(video['views'])
        message_to_send += (
            f"{idx}. \n"
            f"• Tên kênh: {video['channel']}\n"
            f"• Tiêu đề: {video['title']}\n"
            f"• Lượt xem: {translated_views}\n"
            f"• Thời gian đã up video: {translated_time}\n"
            f"• Thời lượng video: {video['duration']}\n"
            f"• Link: https://www.youtube.com{video['url_suffix']}\n\n"
        )

        gui = f"{message_to_send}\nĐể xem video vui lòng coppy link video cần xem và dùng lệnh {PREFIX}down <link video>"

    client.replyMessage(
        Message(text=gui),
        message_object,
        thread_id,
        thread_type,ttl=120000
    )

def get_szl():
    return {
        'ytb': handle_ytb_command
    }
