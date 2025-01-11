import os
import json
import random
from datetime import datetime
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Module metadata
des = {
    'version': '1.0.0',
    'credits': 'Kz Khánhh',
    'description': 'Game play with anime characters'
}

# Constants
CHARACTERS = {
    'umaru': {'emoji': '🔥', 'image_url': 'https://imgur.com/PJ8xGcA.jpg'},
    'nami': {'emoji': '⚡', 'image_url': 'https://imgur.com/n6TShJP.jpg'},
    'chitanda': {'emoji': '🍙', 'image_url': 'https://imgur.com/tp4Pjo1.jpg'},
    'mirai': {'emoji': '🦞', 'image_url': 'https://imgur.com/mf4EMOx.jpg'},
    'elaina': {'emoji': '🦵', 'image_url': 'https://imgur.com/wYJwU3y.jpg'},
    'mikasa': {'emoji': '🐱', 'image_url': 'https://imgur.com/C0XFKxy.jpg'}
}

MIN_BET = 1000

# File path for money data
money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

def reload_money_data():
    """Reload money data from the JSON file."""
    global money_data
    if os.path.exists(money_file):
        with open(money_file, "r") as file:
            money_data = json.load(file)
    else:
        money_data = {}

# Initialize money data
reload_money_data()

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def get_money(user_id):
    reload_money_data()
    return money_data.get(user_id, 0)

def add_money(user_id, amount):
    reload_money_data()
    if user_id in money_data:
        money_data[user_id] += amount
    else:
        money_data[user_id] = amount
    save_money_data()

def subtract_money(user_id, amount):
    reload_money_data()
    if user_id in money_data:
        money_data[user_id] -= amount
        if money_data[user_id] < 0:
            money_data[user_id] = 0
    save_money_data()

def parse_character(input_char):
    # Map both character names and emojis to internal names
    char_map = {
        'Umaru': 'umaru', '🔥': 'umaru',
        'Nami': 'nami', '⚡': 'nami',
        'Chitanda': 'chitanda', '🍙': 'chitanda',
        'Mirai': 'mirai', '🦞': 'mirai',
        'Elaina': 'elaina', '🦵': 'elaina',
        'Mikasa': 'mikasa', '🐱': 'mikasa'
    }
    return char_map.get(input_char)

def handle_play(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    # Validate command format
    if len(content) != 3:
        usage = "Sử dụng: pl <nhân vật/emoji> <số tiền>\n"
        usage += "Nhân vật: Umaru/Nami/Chitanda/Mirai/Elaina/Mikasa\n"
        usage += "Emoji: 🔥/⚡/🍙/🦞/🦵/🐱\n"
        usage += f"Tiền cược tối thiểu: {MIN_BET} VND"
        client.replyMessage(Message(text=usage), message_object, thread_id, thread_type)
        return

    # Parse bet character and amount
    bet_char = parse_character(content[1])
    try:
        bet_amount = int(content[2])
    except ValueError:
        client.replyMessage(Message(text="Số tiền cược không hợp lệ."), message_object, thread_id, thread_type)
        return

    # Validate character
    if not bet_char:
        client.replyMessage(Message(text="Nhân vật không hợp lệ."), message_object, thread_id, thread_type)
        return

    # Validate bet amount
    if bet_amount < MIN_BET:
        client.replyMessage(Message(text=f"Số tiền cược tối thiểu là {MIN_BET} VND."), message_object, thread_id, thread_type)
        return

    current_money = get_money(author_id)
    if bet_amount > current_money:
        client.replyMessage(Message(text="Bạn không có đủ tiền để đặt cược."), message_object, thread_id, thread_type)
        return

    # Generate results
    results = random.choices(list(CHARACTERS.keys()), k=3)
    result_emojis = [CHARACTERS[char]['emoji'] for char in results]

    # Check if won
    won = bet_char in results

    # Calculate winnings/losses
    if won:
        winnings = bet_amount * 5
        add_money(author_id, winnings)
        result_msg = f"Kết quả: {' | '.join(result_emojis)}\n🌺 Bạn đã thắng và nhận được {winnings} VND!"
    else:
        subtract_money(author_id, bet_amount)
        result_msg = f"Kết quả: {' | '.join(result_emojis)}\n🌺 Bạn đã thua và mất {bet_amount} VND!"

    # Send result message with styling
    style_result = MultiMsgStyle([
        MessageStyle(offset=0, length=len(result_msg), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(result_msg), style="color", color="#a6adc8", auto_format=False)
    ])

    client.replyMessage(Message(text=result_msg, style=style_result), message_object, thread_id, thread_type)

def get_szl():
    return {
        'pl': handle_play
    }
