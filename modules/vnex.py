import requests
from bs4 import BeautifulSoup
from zlapi.models import Message

# Metadata for the module
des = {
    'version': "1.0.2",
    'credits': "Quốc Khánh",
    'description': "VNExpress News Module"
}

def handle_vnex_command(message, message_object, thread_id, thread_type, author_id, client):
    """Handles the VNExpress news command"""
    url = "https://vnexpress.net/tin-tuc-24h"

    def fetch_latest_news():
        """Fetch the latest news from VNExpress"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            news_items = []
            articles = soup.find_all('article', class_='item-news', limit=3)  # Fetch top 3 news items

            for article in articles:
                title = article.find('h3', class_='title-news').text.strip() if article.find('h3', class_='title-news') else "Không có tiêu đề"
                link = article.find('a')['href'] if article.find('a') else "Không có đường dẫn"
                description = article.find('p', class_='description').text.strip() if article.find('p', class_='description') else "Không có mô tả"
                time = article.find('span', class_='time-ago').text.strip() if article.find('span', class_='time-ago') else "Không có thời gian"

                news_items.append({
                    "time": time,
                    "title": title,
                    "description": description,
                    "url": link
                })

            return news_items
        except Exception as e:
            print(f"Lỗi khi lấy tin tức: {e}")
            return []

    news_items = fetch_latest_news()

    if not news_items:
        error_message = Message(text="Không tìm thấy tin tức mới.")
        client.replyMessage(error_message, message_object, thread_id, thread_type, ttl=20000)
        return

    # Constructing the response message
    msg = "===== TIN TỨC MỚI NHẤT TỪ VNEXPRESS =====\n\n"
    for i, item in enumerate(news_items, 1):
        msg += f"🔔 Tin {i}:\n"
        msg += f"🕒 Thời gian: {item['time']}\n"
        msg += f"📌 Tiêu đề: {item['title']}\n"
        msg += f"📝 Mô tả: {item['description']}\n"
        msg += f"🔗 Đường dẫn: {item['url']}\n"
        msg += "-------------------------\n\n"

    client.replyMessage(Message(text=msg), message_object, thread_id, thread_type, ttl=20000)

def get_szl():
    return {
        'vnex': handle_vnex_command
    }
