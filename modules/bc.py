import os
import json
import random
import requests
from datetime import datetime
from zlapi.models import Message, MessageStyle, MultiMsgStyle

des = {
    'version': '1.0.0',
    'credits': 'Kz Khánhh',
    'description': 'Bầu Cua Game'
}

money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

# Initialize money data
if os.path.exists(money_file):
    with open(money_file, "r") as file:
        money_data = json.load(file)
else:
    money_data = {}

# Game items with their emojis
GAME_ITEMS = {
    "bầu": "🍐",
    "cua": "🦀",
    "tôm": "🦞",
    "cá": "🐟",
    "gà": "🐓",
    "nai": "🦌"
}

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def get_money(user_id):
    return money_data.get(user_id, 0)

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

def handle_baucua(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 3:
        usage = "Cách chơi: bc <bầu/cua/tôm/cá/gà/nai> <số tiền>"
        client.replyMessage(Message(text=usage), message_object, thread_id, thread_type)
        return

    bet_type = content[1].lower()
    if bet_type not in GAME_ITEMS:
        client.replyMessage(Message(text="Lựa chọn không hợp lệ. Vui lòng chọn: bầu/cua/tôm/cá/gà/nai"), 
                          message_object, thread_id, thread_type)
        return

    try:
        bet_amount = int(content[2])
    except ValueError:
        client.replyMessage(Message(text="Số tiền cược không hợp lệ!"), 
                          message_object, thread_id, thread_type)
        return

    current_money = get_money(author_id)
    if current_money < bet_amount:
        client.replyMessage(Message(text="Bạn không đủ tiền để đặt cược!"), 
                          message_object, thread_id, thread_type)
        return

    if bet_amount < 100:
        client.replyMessage(Message(text="Số tiền cược tối thiểu là 100!"), 
                          message_object, thread_id, thread_type)
        return

    # Send "rolling" message
    client.replyMessage(Message(text="🎲 Đang lắc..."), message_object, thread_id, thread_type)

    # Generate results
    results = [random.choice(list(GAME_ITEMS.keys())) for _ in range(3)]

    # Count matches
    matches = results.count(bet_type)
    result_emojis = [GAME_ITEMS[item] for item in results]

    # Calculate winnings
    if matches > 0:
        winnings = bet_amount * matches
        add_money(author_id, winnings)
        result_msg = f"Kết quả: {' '.join(result_emojis)}\nChúc mừng! Bạn đã thắng {winnings:,}đ với {matches} {GAME_ITEMS[bet_type]}"
    else:
        subtract_money(author_id, bet_amount)
        result_msg = f"Kết quả: {' '.join(result_emojis)}\nTiếc quá! Bạn đã thua {bet_amount:,}đ"

    # Send final result
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(result_msg), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(result_msg), style="color", color="#cdd6f4", auto_format=False)
    ])
    client.replyMessage(Message(text=result_msg, style=style), message_object, thread_id, thread_type)

def get_szl():
    return {
        'bc': handle_baucua
    }