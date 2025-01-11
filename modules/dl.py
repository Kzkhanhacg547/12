import yt_dlp as youtube_dl
import json
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from threading import Thread
import re
import os
des = {
    'version': "1.0.2",
    'credits': "",
    'description': "Download YTB"
}

link = 'https://soundcloud.com/zkun/sets/t-n-c-c-i-l-ng?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing'
def download_soundcloud(link):
    # Các tùy chọn cho yt-dlp
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'extract_flat': False,
        }

    # Sử dụng yt_dlp để trích xuất thông tin
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            # print(info_dict)
            if 'entries' in info_dict:
                entries= info_dict['entries'][0]
            else:
                entries =info_dict
        url_mp3=''
        for format in entries['formats']:
            if format['ext'] == 'mp3' and format['protocol']=='http':
                # print(format)
                url_mp3=f"{format['url']}"
                # print(f"MP3 URL: {format['url']}")
        result = {
                "success": True,
                "data": {
                    "url": url_mp3,
                    "description": entries.get('description'),
                    "title": entries.get('title'),
                    "thumbnail": entries['thumbnail'],
                    # "thumbnail": [thumb for thumb in entries['thumbnail'] if thumb['id'] in ['original']],
                }
        }
        return result
    except Exception as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}

# print(download_soundcloud(link))
# def sendRemoteVoice(self, voiceUrl, thread_id, thread_type, fileSize=None, ttl=0):
def download_from_youtube(link):
    try:
        # Thiết lập tùy chọn cho yt-dlp
        ydl_opts = {
            'quiet': True,
            'noplaylist': False,
            'format': 'bestaudio/best',
            'get_formats': True,
        }

        # Tạo đối tượng YoutubeDL và lấy thông tin video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'Unknown Title')
            print(f"Đang xử lý video: {title}")

            # Lấy các định dạng video và âm thanh
            video_formats = []
            # audio_formats = []
            for format_info in info_dict.get('formats', []):
                format_url = format_info.get('url')
                if format_info.get('acodec') != 'none' and format_info.get('vcodec') != 'none':
                    # print(format_info,"\n")
                    resolution = format_info.get('resolution', None)
                    if resolution:
                        width, height = resolution.split('x')  # Tách độ phân giải thành width và height
                    else:
                        width = height = None 
                    video_formats.append({
                        'url': format_url,
                        'quality': format_info.get('height', None),
                        'width':width,
                        'height':height,
                        'type_download': 'video',
                        'type': format_info.get('acodec'),
                        'extension': format_info.get('ext')
                    })
                # if format_info.get('acodec') != 'none' and format_info.get('vcodec') == 'none' and format_info.get('ext')=='m4a':
                #     audio_formats.append({
                #         'url': format_url,
                #         'quality': format_info.get('height', None),
                #         'type_download': 'audio',
                #         'type': format_info.get('acodec'),
                #         'extension': format_info.get('ext')
                #     })

            # Trả về kết quả dưới dạng từ điển (dict)
            result = {
                "success": True,
                "data": {
                    "url": link,
                    "source": "youtube",
                    "author": info_dict.get('uploader', 'Unknown Author'),
                    "title": title,
                    "thumbnail": info_dict.get('thumbnail', ''),
                    "duration": info_dict.get('duration', 0),
                    "medias": video_formats,
                }
            }
            return result

    except youtube_dl.utils.DownloadError as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}
    except Exception as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}



def download_from_tiktok(link):
    try:
        # Thiết lập tùy chọn cho yt-dlp
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'format': 'bestvideo+bestaudio/best',
            'get_formats': True,
        }

        # Tạo đối tượng YoutubeDL và lấy thông tin video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'Unknown Title')
            print(f"Đang xử lý video: {title}")

            # Lấy các định dạng video
            video_formats = []
            for format_info in info_dict.get('formats', []):
                format_url = format_info.get('url')
                
                resolution = format_info.get('resolution', None)
                if resolution:
                    width, height = resolution.split('x')  # Tách độ phân giải thành width và height
                else:
                    width = height = None 
                if format_info.get('vcodec') != 'none' and 'cookies' not in format_info and format_info.get('vcodec')=='h264':  # Chỉ lấy video formats
                    # print(format_info, "\n")
                    video_formats.append({
                        'url': format_url,
                        'quality': format_info.get('height', None),
                        'width':width,
                        'height':height,
                        'type_download': 'video',
                        'extension': format_info.get('ext'),
                    })

            # Trả về kết quả dưới dạng từ điển (dict)
            result = {
                "success": True,
                "data": {
                    "url": link,
                    "source": "tiktok",
                    "author": info_dict.get('uploader', 'Unknown Author'),
                    "title": title,
                    "thumbnail": info_dict.get('thumbnail', ''),
                    "duration": info_dict.get('duration', 0),
                    "medias": video_formats,
                }
            }
            return result

    except youtube_dl.utils.DownloadError as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}
    except Exception as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}

def download_from_facebook(link):
    try:
        # Thiết lập tùy chọn cho yt-dlp
        ydl_opts = {
            'quiet': True,
            'noplaylist': True,
            'format': 'bestvideo+bestaudio/best',
            'get_formats': True,
        }

        # Tạo đối tượng YoutubeDL và lấy thông tin video
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'Unknown Title')
            print(f"Đang xử lý video: {title}")

            # Lấy các định dạng video
            video_formats = []
            for format_info in info_dict.get('formats', []):
                format_url = format_info.get('url')

                # resolution = format_info.get('resolution', None)
                # if resolution:
                #     width, height = resolution.split('x')  # Tách độ phân giải thành width và height
                # else:
                #     width = height = None
                
                if format_info.get('vcodec') != 'none' and 'manifest_url' not in format_info:  
                    # print(format_info, "\n")
                    video_formats.append({
                        'url': format_url,
                        'quality': format_info.get('height', None),
                        # 'width': width,
                        # 'height': height,
                        'type_download': 'video',
                        'extension': format_info.get('ext'),
                    })

            # Trả về kết quả dưới dạng từ điển (dict)
            result = {
                "success": True,
                "data": {
                    "url": link,
                    "source": "facebook",
                    "author": info_dict.get('uploader', 'Unknown Author'),
                    "title": title,
                    "thumbnail": info_dict.get('thumbnail', ''),
                    "duration": info_dict.get('duration', 0),
                    "medias": video_formats,
                }
            }
            return result

    except youtube_dl.utils.DownloadError as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}
    except Exception as e:
        print(str(e))
        return {"success": False, "error": f"➜ Đã xảy ra lỗi gì đó 🤧"}
def detect_platform(link):
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*'
    tiktok_regex = r'(https?://)?(www\.)?(tiktok\.com|vt\.tiktok\.com)/.*'
    facebook_regex = r'(https?://)?(www\.)?(facebook|fb)(\.com|\.watch)?/.*'
    soundcloud_regex = r'(https?://)?(www\.)?(soundcloud\.com|on\.soundcloud\.com)/.*'

    if re.match(youtube_regex, link):
        return "youtube"
    elif re.match(tiktok_regex, link):
        return "tiktok"
    elif re.match(facebook_regex, link):
        return "facebook"
    elif re.match(soundcloud_regex, link):
        return "soundcloud"
    else:
        return None









def handle_download_command(message, message_object, thread_id, thread_type, author_id, bot):
    def send_download_response():
        try:
            parts = message.split()
            if len(parts) < 2:
                response = (
                    "🎉 Chào mừng đến với menu ⬇️ Downloader! ⚙️\n"
                    "   ➜ /dl [link]: 🎬 Tải video từ link\n"
                    "🆘 Hỗ trợ Download các video từ 🌀 Facebook, ▶️ Youtube\n"
                    "🤖 bot luôn sẵn sàng phục vụ bạn! 🌸"
                )
                bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                return
            else:
                link = parts[1]

                # Kiểm tra nền tảng
                platform = detect_platform(link)

                # Gửi thông báo chờ
                response = f"➜ 🌀 Đang xử lý, vui lòng chờ ⌛"
                bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)

                # Gọi hàm xử lý theo nền tảng
                if platform == "youtube":
                    result = download_from_youtube(link)
                    
                    if result['success']:
                        medias = result['data']['medias']
                        
                        # Lấy video có chất lượng tốt nhất
                        chosen_media = max([media for media in medias if media['type_download'] == 'video'], key=lambda x: x['quality'])
                        
                        if chosen_media:
                            # Gửi video tải về
                            bot.sendRemoteVideo(videoUrl=chosen_media['url'], thumbnailUrl=result['data']['thumbnail'], duration=result['data']['duration'],  thread_id=thread_id,  thread_type=thread_type,width=int(chosen_media['width']),
                                height=int(chosen_media['height']),  message=Message(text=result['data']['title']))
                            # bot.sendRemoteVideo(videoUrl=chosen_media['url'], thumbnailUrl=result['data']['thumbnail'], duration=result['data']['duration'],  thread_id=thread_id,  thread_type=thread_type, width=640, height=360)
                            response = f"➜ Tải thành công ✅"
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                        else:
                            response = "⚠️ Không tìm thấy video tải xuống phù hợp."
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)

                elif platform == "tiktok":
                    result = download_from_tiktok(link)
                    if result['success']:
                        medias = result['data']['medias']
                        chosen_media = max([media for media in medias if media['type_download'] == 'video'], key=lambda x: x['quality'])
                        if chosen_media:
                            bot.sendRemoteVideo(
                                videoUrl=chosen_media['url'],
                                thumbnailUrl=result['data']['thumbnail'],
                                duration=result['data']['duration'],
                                thread_id=thread_id,
                                thread_type=thread_type,
                                width=int(chosen_media['width']),
                                height=int(chosen_media['height']),
                                message=Message(text=result['data']['title'])
                            )
                            response = f"➜ Tải thành công ✅"
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                        else:
                            response = "⚠️ Không tìm thấy video tải xuống phù hợp."
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                elif platform == "soundcloud":
                    result = download_soundcloud(link)
                    if result['success']:
                        medias = result['data']
                        # bot.sendLocalGif(gifPath=medias['thumbnail'], thumbnailUrl=medias['thumbnail'], thread_id=thread_id, thread_type=thread_type, gifName="vrxx.gif", width=500, height=500, ttl=0)
                        print(medias['thumbnail'])
                        print(medias)
                        bot.sendLink(linkUrl=medias['thumbnail'], title=f"➜ 🎸 {medias['title']}\n➜ 🎶 {medias['description']}", thread_id=thread_id, thread_type=thread_type, thumbnailUrl=medias['thumbnail'], domainUrl=None, desc=None, message=None, ttl=0)
                        bot.sendRemoteVoice( voiceUrl=medias['url'], thread_id=thread_id, thread_type=thread_type )
                        
                        response = f"➜ Tải thành công ✅"
                        # bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                    else:
                        response = "➜ ⚠️ Không tìm thấy video tải xuống phù hợp 🤧"
                            # bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                    if response:
                        bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                elif platform=='facebook':
                    result = download_from_facebook(link)
                    if result['success']:
                        medias = result['data']['medias']
                        
                        # Lấy video có chất lượng tốt nhất
                        chosen_media = max([media for media in medias if media['type_download'] == 'video'], key=lambda x: x['quality'] or 0)
                        
                        if chosen_media:
                            bot.sendRemoteVideo(
                                videoUrl=chosen_media['url'],
                                thumbnailUrl=result['data']['thumbnail'],
                                duration=result['data']['duration'],
                                thread_id=thread_id,
                                thread_type=thread_type,
                                width=1280,  # Thêm chiều rộng (mặc định 640 nếu không có)
                                height=720,  # Thêm chiều cao (mặc định 360 nếu không có)
                                message=Message(text=result['data']['title'])
                            )
                            response = f"➜ Tải thành công ✅"
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                        else:
                            response = "⚠️ Không tìm thấy video tải xuống phù hợp."
                            bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                    else:
                        response = "⚠️ Không thể tải video từ Facebook."
                        bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)
                else:
                    response = f"➜ Link không hợp lệ hoặc không được hỗ trợ 🤧"
                    bot.replyMessage(Message(text=f"{response}"), message_object, thread_id=thread_id, thread_type=thread_type)

        except Exception as e:
            print(f"Error: {e}")
            bot.replyMessage(Message(text="➜ Đã xảy ra lỗi gì đó 🤧"), message_object, thread_id=thread_id, thread_type=thread_type)

    thread = Thread(target=send_download_response)
    thread.start()
    
def get_szl():
    return {
        'dl': handle_download_command
    }
