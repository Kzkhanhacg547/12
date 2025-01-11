from config import PREFIX
from zlapi.models import Message
import json
import requests

# Metadata
des = {
    'version': "1.0.5",
    'credits': "",
    'description': "check prefix and fetch thinh API"
}

# Load settings
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")

def prf():
    """Get prefix from settings"""
    with open('setting.json', 'r') as f:
        return json.load(f).get('prefix')

def checkprefix(message, message_object, thread_id, thread_type, author_id, client):
    """Check and display the current prefix"""
    current_prefix = prf()
    formatted_message = f"""
- 𝐏𝐫𝐞𝐟𝐢𝐱: `{current_prefix}`
    """
    gui = Message(text=formatted_message)
    client.replyMessage(gui, message_object, thread_id, thread_type)

def fetch_thinh():
    """Fetch 'thinh' from API"""
    try:
        response = requests.get(f"{API_URL}/thinh")
        if response.status_code == 200:
            data = response.json()
            thinh_message = f"""
💌 𝐂𝐚̂𝐮 𝐭𝐡𝐢́𝐧𝐡 𝐡𝐨̂𝐦 𝐧𝐚𝐲:
- 🌹 `{data.get('url', 'Không có dữ liệu')}`
- ✨𝐍𝐠𝐮𝐨̂̀𝐧: {data.get('author', 'Ẩn danh')}
            """
            return thinh_message
        else:
            return "⚠️ Không thể lấy câu thính từ API. Vui lòng kiểm tra URL hoặc kết nối."
    except Exception as e:
        return f"❌ Đã xảy ra lỗi: {str(e)}"

def show_thinh(message, message_object, thread_id, thread_type, author_id, client):
    """Display a 'thinh' message"""
    thinh_content = fetch_thinh()
    gui = Message(text=thinh_content)
    client.replyMessage(gui, message_object, thread_id, thread_type)

def get_szl():
    """Register commands"""
    return {
        'prefix': checkprefix,
        'thính': show_thinh
    }
