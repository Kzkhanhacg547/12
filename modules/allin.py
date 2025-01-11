import os
import json
import random
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Metadata
des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Được ăn cả, ngã về không"
}

# File path for money data
money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

# Initialize money data
def load_money_data():
    if os.path.exists(money_file):
        with open(money_file, "r") as file:
            return json.load(file)
    return {}

money_data = load_money_data()

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def get_money(user_id):
    return money_data.get(user_id, 0)

def set_money(user_id, amount):
    money_data[user_id] = amount
    save_money_data()

def check_money(user_id):
    """Kiểm tra và cập nhật số tiền người chơi."""
    user_money = get_money(user_id)

    # Đảm bảo người chơi có tiền tối thiểu (ví dụ: 50 để chơi lần đầu)
    if user_money < 50:
        set_money(user_id, max(user_money, 50))

def get_lucky():
    lucky_numbers = ['5', '21', '34', '43', '55', '78', '87', '66', '98', '9', 
                     '11', '17', '26', '30', '48', '59', '66', '70', '82', '93']
    return random.choice(lucky_numbers)

def get_lucky_number():
    return random.randint(1, 99)

def handle_all_or_nothing(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra và cập nhật tiền trước khi bắt đầu chơi
    check_money(author_id)

    # Kiểm tra nếu người chơi có đủ tiền để tham gia (tối thiểu là 50)
    user_money = get_money(author_id)
    if user_money < 50:
        client.replyMessage(
            Message(text="Số tiền của bạn không đủ để chơi, hãy kiếm thêm tiền!"),
            message_object, thread_id, thread_type
        )
        return

    # Xác định số may mắn và số của người chơi
    lucky_number = get_lucky()
    player_number = str(get_lucky_number())

    if player_number == lucky_number or random.random() < 0.15:  # 15% cơ hội thắng
        # Thắng - nhân tiền lên 10 lần
        new_money = user_money * 10
        set_money(author_id, new_money)
        result_message = (
            f"Số may mắn: {lucky_number}\n"
            f"Số của bạn: {player_number}\n\n"
            f"Chúc mừng bạn đã thắng và nhận thưởng gấp 10 lần!\n"
            f"Số tiền hiện tại: {new_money}"
        )
    else:
        # Thua - mất hết tiền
        set_money(author_id, 0)
        result_message = (
            f"Số may mắn: {lucky_number}\n"
            f"Số của bạn: {player_number}\n\n"
            f"Chia buồn, bạn đã thua và mất hết tiền. Hãy thử lại sau!"
        )

    # Áp dụng phong cách cho tin nhắn
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(result_message), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(result_message), style="color", color="#f38ba8", auto_format=False)
    ])

    # Gửi tin nhắn kết quả
    client.replyMessage(
        Message(text=result_message, style=style),
        message_object, thread_id, thread_type
    )

def get_szl():
    return {
        'allin': handle_all_or_nothing,
    }
