import os
import json
import random
from datetime import datetime, timedelta
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Metadata
des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Chẵn Lẻ Game" 
}

# File paths
money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")
cooldown_file = os.path.join(os.path.dirname(__file__), "cache/cooldown_data.json")

# Initialize money data
if os.path.exists(money_file):
    with open(money_file, "r") as file:
        money_data = json.load(file)
else:
    money_data = {}

# Initialize cooldown data
if os.path.exists(cooldown_file):
    with open(cooldown_file, "r") as file:
        cooldown_data = json.load(file)
else:
    cooldown_data = {}

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def save_cooldown_data():
    with open(cooldown_file, "w") as file:
        json.dump(cooldown_data, file)

def add_money(user_id, amount):
    if user_id in money_data:
        money_data[user_id] += amount
    else:
        money_data[user_id] = amount
    save_money_data()

def subtract_money(user_id, amount):
    if user_id in money_data:
        money_data[user_id] -= amount
        if money_data[user_id] < 0:
            money_data[user_id] = 0
    save_money_data()

def get_money(user_id):
    return money_data.get(user_id, 0)

def check_cooldown(user_id):
    if user_id in cooldown_data:
        last_play = datetime.fromtimestamp(cooldown_data[user_id])
        if datetime.now() - last_play < timedelta(seconds=30):
            return True
    return False

def update_cooldown(user_id):
    cooldown_data[user_id] = datetime.now().timestamp()
    save_cooldown_data()

def handle_chanle(message, message_object, thread_id, thread_type, author_id, client):
    # Check cooldown
    if check_cooldown(author_id):
        client.replyMessage(
            Message(text="⏰ Vui lòng đợi 30 giây giữa mỗi lần chơi."),
            message_object, thread_id, thread_type
        )
        return

    content = message.strip().split()
    if len(content) < 3:
        client.replyMessage(
            Message(text="📌 Cú pháp: cl <chẵn/lẻ> <tiền>"),
            message_object, thread_id, thread_type
        )
        return

    bet_type = content[1].strip().lower()
    if bet_type not in ['chẵn', 'lẻ']:
        client.replyMessage(
            Message(text="❌ Chọn 'chẵn' hoặc 'lẻ'."),
            message_object, thread_id, thread_type
        )
        return

    try:
        bet_amount = int(content[2])
    except ValueError:
        client.replyMessage(
            Message(text="❌ Số tiền không hợp lệ."),
            message_object, thread_id, thread_type
        )
        return

    current_money = get_money(author_id)
    if current_money < 1000:
        client.replyMessage(
            Message(text="💰 Bạn cần ít nhất 1000 VND để chơi."),
            message_object, thread_id, thread_type
        )
        return

    if bet_amount < 1000:
        client.replyMessage(
            Message(text="💰 Cược tối thiểu 1000 VND."),
            message_object, thread_id, thread_type
        )
        return

    if bet_amount > current_money:
        client.replyMessage(
            Message(text="❌ Không đủ tiền để cược."),
            message_object, thread_id, thread_type
        )
        return

    # Update cooldown
    update_cooldown(author_id)

    # Generate result
    result_number = random.randint(0, 9)
    result_type = "chẵn" if result_number % 2 == 0 else "lẻ"

    # Handle win/lose
    if bet_type == result_type:
        add_money(author_id, bet_amount)
        reply_text = f"""🎲 Kết quả: {result_number}
💰 Chúc mừng! +{bet_amount:,} VND
💵 Số dư: {get_money(author_id):,} VND"""
    else:
        subtract_money(author_id, bet_amount)
        reply_text = f"""🎲 Kết quả: {result_number}
💸 Tiếc quá! -{bet_amount:,} VND
💵 Số dư: {get_money(author_id):,} VND"""

    # Send result
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(reply_text), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(reply_text), style="color", color="#cdd6f4", auto_format=False)
    ])
    client.replyMessage(Message(text=reply_text, style=style), message_object, thread_id, thread_type)

def get_szl():
    return {
        'cl': handle_chanle
    }