import os
import random
import re
import time
import requests
from zlapi import *
from zlapi.models import *
from bs4 import BeautifulSoup
from fake_useragent import UserAgent 

des = {
    'version': "1.x.x",
    'credits': "Bản quyền con cặc",
    'description': "Thịnh"
}

def handle_nhac_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="𝑽𝒖𝒊 𝒍𝒐𝒏𝒈 𝒏𝒉𝒂𝒑 𝒕𝒆𝒏 𝒃𝒂𝒊 𝒉𝒂𝒕, 𝑽𝑫: 𝒏𝒉𝒂𝒄 𝑶𝒃𝒊𝒕𝒐 - 𝑩𝒖𝒐𝒏 𝑯𝒂𝒚 𝑽𝒖𝒊 ᕦ😉ᕤ")
        client.replyMessage(error_message, message_object, thread_id, thread_type,ttl=60000)
        return

    tenbaihat = ' '.join(content[1:]) 

    def get_client_id():
        """Lấy client ID từ SoundCloud và lưu vào tệp nếu chưa có."""
        client_id_file = 'client_id.txt'
        if os.path.exists(client_id_file):
            with open(client_id_file, 'r') as file:
                client_id = file.read().strip()
                if client_id:
                    return client_id

        try:
            res = requests.get('https://soundcloud.com/', headers=get_headers())
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            script_tags = soup.find_all('script', {'crossorigin': True})
            urls = [tag.get('src') for tag in script_tags if tag.get('src') and tag.get('src').startswith('https')]
            if not urls:
                raise Exception('Không tìm thấy URL script')
            
            res = requests.get(urls[-1], headers=get_headers())
            res.raise_for_status()
            client_id = res.text.split(',client_id:"')[1].split('"')[0]

            # Lưu client_id vào tệp
            with open(client_id_file, 'w') as file:
                file.write(client_id)

            # Gửi thông báo khi lấy được client_id thành công

            return client_id
        except Exception as e:
            print(f"Không thể lấy client ID: {e}")
            error_message = Message(text="Không thể lấy client ID. Vui lòng thử lại.")
            client.sendMessage(error_message, thread_id, thread_type)
            return None

    def wait_for_client_id():
        """Đợi cho đến khi lấy được client ID từ SoundCloud."""
        while True:
            client_id = get_client_id()
            if client_id:
                return client_id
            print("Đang chờ client ID...")
            time.sleep(0)  # Đợi 5 giây trước khi thử lại

    def get_headers():
        """Tạo tiêu đề ngẫu nhiên cho yêu cầu HTTP."""
        user_agent = UserAgent()
        headers = {
            "User-Agent": user_agent.random,
            "Accept-Language": random.choice([
                "en-US,en;q=0.9",
                "fr-FR,fr;q=0.9",
                "es-ES,es;q=0.9",
                "de-DE,de;q=0.9",
                "zh-CN,zh;q=0.9"
            ]),
            "Referer": 'https://soundcloud.com/',
            "Upgrade-Insecure-Requests": "1"
        }
        return headers

    def search_song(query):
        """Tìm kiếm bài hát trên SoundCloud và trả về URL, tiêu đề và ảnh bìa của bài hát đầu tiên tìm thấy."""
        try:
            link_url = 'https://soundcloud.com'
            headers = get_headers()
            search_url = f'https://m.soundcloud.com/search?q={requests.utils.quote(query)}'
            messagesend = Message(text="𝑫𝒂𝒏𝒈 𝒕𝒊𝒎 𝒌𝒊𝒆𝒎 𝒏𝒉𝒂𝒄 𝒃𝒂𝒏 𝒚𝒆𝒖 𝒄𝒂𝒖 𝒅𝒆 𝒈𝒖𝒊 𝒍𝒆𝒏. 𝑪𝒉𝒖𝒄 𝒃𝒂𝒏 𝒏𝒈𝒉𝒆 𝒏𝒉𝒂𝒄 𝒗𝒖𝒊 𝒗𝒆♡")
            client.replyMessage(messagesend, message_object, thread_id, thread_type,ttl=20000)
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            url_pattern = re.compile(r'^/[^/]+/[^/]+$')
            for element in soup.select('div > ul > li > div'):
                a_tag = element.select_one('a')
                if a_tag and a_tag.has_attr('href'):
                    relative_url = a_tag['href']
                    if url_pattern.match(relative_url):
                        title = a_tag.get('aria-label', '')
                        url = link_url + relative_url
                        img_tag = element.select_one('img')
                        if img_tag and img_tag.has_attr('src'):
                            cover_url = img_tag['src']
                        else:
                            cover_url = None 
                    
                        return url, title, cover_url
            return None, None, None
        except Exception as e:
            print(f"Lỗi khi tìm kiếm bài hát: {e}")
            return None, None, None

    def download(link):
        """Lấy và in ra URL âm thanh từ SoundCloud."""
        try:
            client_id = wait_for_client_id()  # Đợi cho đến khi lấy được client_id
            if not client_id:
                return None
            headers = get_headers()
            api_url = f'https://api-v2.soundcloud.com/resolve?url={link}&client_id={client_id}'
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            progressive_url = next((t['url'] for t in data.get('media', {}).get('transcodings', []) if t['format']['protocol'] == 'progressive'), None)
            if not progressive_url:
                raise Exception('Không tìm thấy URL âm thanh')
            response = requests.get(f'{progressive_url}?client_id={client_id}&track_authorization={data.get("track_authorization")}', headers=headers)
            response.raise_for_status()
            url = response.json().get('url')
            return url
        except Exception as e:
            print(f"Lỗi khi tải âm thanh: {e}")
            return None

    def save_file_to_cache(url, filename):
        """Tải và lưu file vào thư mục con cache."""
        try:
            response = requests.get(url, headers=get_headers())
            response.raise_for_status()
            cache_dir = os.path.join(os.path.dirname(__file__), 'cache')
            os.makedirs(cache_dir, exist_ok=True)
            file_path = os.path.join(cache_dir, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            print(f"Tải file thành công! Đã lưu tại {file_path}")
            return file_path
        except Exception as e:
            print(f"Lỗi khi tải file: {e}")
            return None

    def upload_to_uguu(file_path):
        """Tải lên tệp tới Uguu.se và trả về URL."""
        url = "https://uguu.se/upload"
        try:
            with open(file_path, 'rb') as file:
                files = {'files[]': (os.path.basename(file_path), file)}
                response = requests.post(url, files=files, headers=get_headers())
                response.raise_for_status()
            response_text = response.text
            if "https:" in response_text:
                start = response_text.find("https:")
                end = response_text.find(" ", start)
                if end == -1:
                    end = len(response_text)
                url = response_text[start:end]
                return url.replace("\\", "")  
            else:
                return "Không tìm thấy URL trong phản hồi."
        except Exception as e:
            print(f"Lỗi khi tải lên: {e}")
            return None

    def delete_file(file_path):
        """Xóa tệp sau khi sử dụng."""
        try:
            os.remove(file_path)
            print(f"Đã xóa tệp: {file_path}")
        except Exception as e:
            print(f"Lỗi khi xóa tệp: {e}")

    if tenbaihat:
        print(f"Tên bài hát tìm thấy: {tenbaihat}")
        link, title, cover = search_song(tenbaihat)
        if link:
            print(f"URL bài hát tìm thấy: {link}")
            mp3_file = save_file_to_cache(download(link), 'downloaded_file.mp3')
            if mp3_file:
                upload_response = upload_to_uguu(mp3_file)
                ulrp = upload_response.replace('"', '').replace(',', '')
                try:
                    cover_response = requests.get(cover)
                    open(cover.rsplit("/", 1)[-1], "wb").write(cover_response.content)
                except:
                    pass
                
                if upload_response:
                    messagesend = Message(text=f"𝑇𝑒𝑛 𝑏𝑎𝑖 ℎ𝑎𝑡:🔸{title}🔹")
                    [
                        client.sendLocalImage(cover.rsplit("/", 1)[-1], thread_id, thread_type, message=messagesend, width=240, height=240,ttl=120000)
                        if cover_response.status_code == 200 else
                        client.replyMessage(messagesend, message_object, thread_id, thread_type)
                    ]
                    
                    client.sendRemoteVoice(voiceUrl=ulrp, thread_id=thread_id, thread_type=thread_type,ttl=120000)
                    delete_file(mp3_file)
                    delete_file(cover.rsplit("/", 1)[-1])
                else:
                    print("Không thể tải lên Uguu.se.")
            else:
                print("Không thể tải file âm thanh.")
        else:
            print("Không tìm thấy bài hát.")
    else:
        print("Tên bài hát không được bỏ trống.")
        
def get_szl():
    return {
        'nhac': handle_nhac_command
    }

