import os
import json
import random
from datetime import datetime, timedelta
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Metadata cho module
des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Tung xu game - Ngửa/Xấp"
}

# Đường dẫn đến file money_data.json
MONEY_FILE = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

# Khởi tạo dữ liệu cooldown
cooldown_data = {}
COOLDOWN_TIME = 10  # Thời gian cooldown 10 giây

def load_money_data():
    """Load dữ liệu tiền từ file json"""
    try:
        if os.path.exists(MONEY_FILE):
            with open(MONEY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading money data: {e}")
        return {}

def save_money_data(data):
    """Lưu dữ liệu tiền vào file json"""
    try:
        os.makedirs(os.path.dirname(MONEY_FILE), exist_ok=True)
        with open(MONEY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving money data: {e}")

def get_user_money(user_id):
    """Lấy số tiền hiện tại của user"""
    data = load_money_data()
    return int(data.get(str(user_id), 0))

def update_user_money(user_id, amount, operation='add'):
    """Cập nhật số tiền của user
    operation: 'add' để cộng tiền, 'subtract' để trừ tiền
    """
    data = load_money_data()
    user_id = str(user_id)
    current_money = int(data.get(user_id, 0))

    if operation == 'add':
        data[user_id] = current_money + amount
    elif operation == 'subtract':
        data[user_id] = max(0, current_money - amount)

    save_money_data(data)
    return data[user_id]

def check_cooldown(user_id):
    """Kiểm tra cooldown của user"""
    if user_id in cooldown_data:
        if datetime.now() < cooldown_data[user_id]:
            remaining = (cooldown_data[user_id] - datetime.now()).seconds
            return True, remaining
    return False, 0

def set_cooldown(user_id):
    """Set cooldown cho user"""
    cooldown_data[user_id] = datetime.now() + timedelta(seconds=COOLDOWN_TIME)

def format_money(amount):
    """Format số tiền với dấu phẩy"""
    return "{:,}".format(amount)

def handle_tungxu(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh tung xu"""
    # Kiểm tra cooldown
    is_cooldown, remaining = check_cooldown(author_id)
    if is_cooldown:
        reply = f"⏰ Vui lòng đợi {remaining} giây nữa để tiếp tục tung xu."
        client.replyMessage(Message(text=reply), message_object, thread_id, thread_type)
        return

    # Phân tích nội dung tin nhắn
    content = message.strip().split()
    if len(content) < 3:
        reply = "📌 Cách dùng: tungxu [n/x] [số tiền]\n- n (ngửa)\n- x (xấp)"
        client.replyMessage(Message(text=reply), message_object, thread_id, thread_type)
        return

    # Xác định loại cược và số tiền
    bet_type = content[1].lower()
    try:
        bet_amount = int(content[2])
    except ValueError:
        client.replyMessage(Message(text="❌ Số tiền cược không hợp lệ!"), message_object, thread_id, thread_type)
        return

    # Kiểm tra loại cược
    if bet_type not in ['n', 'x', 'ngửa', 'xấp']:
        client.replyMessage(Message(text="❌ Chỉ chấp nhận cược 'n' (ngửa) hoặc 'x' (xấp)!"), message_object, thread_id, thread_type)
        return

    # Chuẩn hóa loại cược
    bet_type = 0 if bet_type in ['n', 'ngửa'] else 1

    # Kiểm tra số tiền cược
    current_money = get_user_money(author_id)
    if bet_amount < 10000:
        client.replyMessage(Message(text="❌ Số tiền cược tối thiểu là 10,000 VND!"), message_object, thread_id, thread_type)
        return

    if bet_amount > current_money:
        client.replyMessage(Message(text=f"❌ Bạn không đủ tiền! Hiện tại bạn chỉ có {format_money(current_money)} VND"), message_object, thread_id, thread_type)
        return

    # Tung đồng xu
    result = random.randint(0, 1)  # 0: ngửa, 1: xấp
    result_text = 'ngửa' if result == 0 else 'xấp'

    # Xử lý kết quả
    if bet_type == result:
        # Thắng
        winnings = bet_amount * 2
        update_user_money(author_id, winnings, 'add')
        reply = f"""🎲 Kết quả: {result_text.upper()}
💰 Chúc mừng! Bạn đã thắng {format_money(winnings)} VND
💵 Số dư hiện tại: {format_money(get_user_money(author_id))} VND"""
    else:
        # Thua
        update_user_money(author_id, bet_amount, 'subtract')
        reply = f"""🎲 Kết quả: {result_text.upper()}
💸 Tiếc quá! Bạn đã thua {format_money(bet_amount)} VND
💵 Số dư hiện tại: {format_money(get_user_money(author_id))} VND"""

    # Style cho tin nhắn
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(reply), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(reply), style="color", color="#cdd6f4", auto_format=False)
    ])

    # Gửi kết quả
    client.replyMessage(Message(text=reply, style=style), message_object, thread_id, thread_type)

    # Set cooldown
    set_cooldown(author_id)

# Thêm vào get_szl()
def get_szl():
    return {
        'tungxu': handle_tungxu
    }