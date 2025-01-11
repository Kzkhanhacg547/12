import os
import json
import random
from datetime import datetime, timedelta
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Metadata
des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Được ăn cả, ngã thì đứng lên, còn thở là còn gỡ. Đầu tư sinh lời"
}

# File path for money data
money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

# Initialize money data
def load_money_data():
    if os.path.exists(money_file):
        with open(money_file, "r") as file:
            return json.load(file)
    return {}

def save_money_data(data):
    with open(money_file, "w") as file:
        json.dump(data, file)

def get_money(user_id):
    money_data = load_money_data()  # Always reload the data
    return money_data.get(user_id, 0)

def set_money(user_id, amount):
    money_data = load_money_data()  # Always reload the data
    money_data[user_id] = amount
    save_money_data(money_data)

def check_money(user_id):
    """Kiểm tra và cập nhật số tiền người chơi."""
    user_money = get_money(user_id)

    # Kiểm tra xem người chơi có đủ tiền lớn hơn 10 để chơi
    if user_money < 10:
        set_money(user_id, max(user_money, 10))  # Đảm bảo không có số tiền dưới 10

def get_lucky():
    lucky_numbers = ['5', '21', '34', '43', '55', '78', '87', '66', '98', '9', 
                     '11', '17', '26', '30', '48', '59', '66', '70', '82', '93']
    return random.choice(lucky_numbers)

def get_lucky_number():
    return random.randint(1, 99)

def handle_pl(message, message_object, thread_id, thread_type, author_id, client):
    # Kiểm tra và cập nhật tiền trước khi bắt đầu chơi
    check_money(author_id)

    # Kiểm tra nếu người chơi có đủ tiền để tham gia (tối thiểu là 10)
    user_money = get_money(author_id)
    if user_money < 10:
        client.replyMessage(
            Message(text="Số tiền của bạn không đủ để chơi, hãy kiếm thêm tiền!"),
            message_object, thread_id, thread_type
        )
        return

    # Increase win chance by modifying the lucky number match logic
    lucky_number = get_lucky()
    player_number = str(get_lucky_number())

    # Winning chance: slightly higher
    if player_number == lucky_number or random.random() < 0.15:  # 15% chance of win (increase odds)
        # Win - multiply money by 10
        new_money = user_money * 10
        set_money(author_id, new_money)
        result_message = (
            f"Số may mắn: {lucky_number}\n"
            f"Số của bạn: {player_number}\n\n"
            f"Chúc mừng bạn đã thắng và nhận thưởng gấp 10 lần\n"
            f"Số tiền hiện tại: {new_money}"
        )
    else:
        # Lose - add small penalty
        new_money = max(user_money - 10, 10)  # Ensure at least 10 money
        set_money(author_id, new_money)
        result_message = (
            f"Số may mắn: {lucky_number}\n"
            f"Số của bạn: {player_number}\n\n"
            f"Chia buồn bạn đã thua. Số tiền hiện tại: {new_money}"
        )

    # Apply message styling
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(result_message), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(result_message), style="color", color="#cdd6f4", auto_format=False)
    ])

    # Send result message
    client.replyMessage(
        Message(text=result_message, style=style),
        message_object, thread_id, thread_type
    )

def get_szl():
    return {
        'cado': handle_pl,
    }
