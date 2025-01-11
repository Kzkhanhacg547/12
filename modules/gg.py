from zlapi.models import Message
import requests
from bs4 import BeautifulSoup
import re

# Metadata for the module
des = {
    'version': "1.0.0",
    'credits': "Kz Khánh",
    'description': "Google Search Bot Module by Kz Khánhh"
}

def handle_google_search_command(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 2:
        error_message = Message(text="Vui lòng nhập câu hỏi tìm kiếm.")
        client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=20000)
        return

    query = ' '.join(content[1:])

    def search_google(query):
        """Perform a Google search and return the first few results."""
        try:
            url = f'https://www.google.com/search?q={requests.utils.quote(query)}'
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            results = []
            for g in soup.find_all('div', class_='tF2Cxc'):
                title = g.find('h3').text if g.find('h3') else 'Không có tiêu đề'
                description = g.find('span', class_='aCOpRe').text if g.find('span', class_='aCOpRe') else 'Không có mô tả'
                link = g.find('a')['href'] if g.find('a') else 'Không có đường dẫn'
                results.append({
                    "title": title,
                    "description": description,
                    "url": link
                })
                if len(results) >= 3:
                    break
            return results
        except Exception as e:
            print(f"Lỗi khi tìm kiếm Google: {e}")
            return []

    results = search_google(query)

    if not results:
        error_message = Message(text=f"Không tìm thấy kết quả nào cho: {query}")
        client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=20000)
        return

    msg = f"===== KẾT QUẢ TÌM KIẾM GOOGLE =====\n\n"
    msg += f"🔎 Bạn đã tìm: {query}\n\n"
    msg += "==========================\n\n"

    for i, result in enumerate(results, 1):
        msg += f"■ Tiêu đề: {result['title']}\n"
        msg += f"📝 Mô tả: {result['description']}\n"
        msg += f"🔗 Đường dẫn: {result['url']}\n"
        msg += "\n==========================\n\n"

    client.replyMessage(Message(text=msg), message_object, thread_id, thread_type, ttl=20000)

def get_szl():
    return {
        'gg': handle_google_search_command
    }
