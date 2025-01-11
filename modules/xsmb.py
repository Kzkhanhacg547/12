import os
import json
import random
from datetime import datetime
from zlapi.models import Message, MessageStyle, MultiMsgStyle

des = {
    'version': '1.0.0',
    'credits': 'Gwen',
    'description': 'Xổ Số Miền Bắc Game'
}

money_file = os.path.join(os.path.dirname(__file__), "cache/money_data.json")

# Load money data
if os.path.exists(money_file):
    with open(money_file, "r") as file:
        money_data = json.load(file)
else:
    money_data = {}

VALID_TYPES = {
    'lo': 2,
    'xien2': 2,
    '3cang': 1,
    '4cang': 1,
    'xien3': 3,
    'xien4': 4
}

MULTIPLIERS = {
    'lo': 3,
    'xien2': 5,
    '3cang': 70,
    'xien3': 100,
    'xien4': 200
}

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def get_money(user_id):
    return money_data.get(str(user_id), 0)

def add_money(user_id, amount):
    user_id = str(user_id)
    if user_id in money_data:
        money_data[user_id] += amount
    else:
        money_data[user_id] = amount
    save_money_data()

def subtract_money(user_id, amount):
    user_id = str(user_id)
    if user_id in money_data:
        money_data[user_id] -= amount
        if money_data[user_id] < 0:
            money_data[user_id] = 0
    save_money_data()

def generate_results():
    return {
        'db': random.randint(10000, 99999),
        'g1': random.randint(10000, 99999),
        'g2': [random.randint(10000, 99999) for _ in range(2)],
        'g3': [random.randint(10000, 99999) for _ in range(6)],
        'g4': [random.randint(1000, 9999) for _ in range(4)],
        'g5': [random.randint(1000, 9999) for _ in range(6)],
        'g6': [random.randint(100, 999) for _ in range(3)],
        'g7': [random.randint(10, 99) for _ in range(4)]
    }

def format_results(results):
    return f"""🎯 Đặc Biệt: {results['db']}
🥇 Giải 1: {results['g1']}
🥈 Giải 2: {' '.join(map(str, results['g2']))}
🥉 Giải 3: {' '.join(map(str, results['g3']))}
🏅 Giải 4: {' '.join(map(str, results['g4']))}
🎖️ Giải 5: {' '.join(map(str, results['g5']))}
🎗️ Giải 6: {' '.join(map(str, results['g6']))}
🎫 Giải 7: {' '.join(map(str, results['g7']))}"""

def check_win(bet_type, numbers, results):
    all_results = set(map(str, [
        results['db'], results['g1'],
        *results['g2'], *results['g3'], *results['g4'],
        *results['g5'], *results['g6'], *results['g7']
    ]))

    if bet_type in ['lo', 'xien2']:
        return all(any(str(res).endswith(str(num)) for res in all_results) for num in numbers)
    elif bet_type in ['3cang', '4cang']:
        return str(numbers[0]) in all_results
    elif bet_type in ['xien3', 'xien4']:
        return all(any(str(num) in str(res) for res in all_results) for num in numbers)
    return False

def handle_xsmb(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()

    if len(content) < 4:
        usage = "Cách chơi: xsmb <loại> <số> <tiền cược>\nLoại: lo, xien2, 3cang, 4cang, xien3, xien4"
        client.replyMessage(Message(text=usage), message_object, thread_id, thread_type)
        return

    bet_type = content[1].lower()
    if bet_type not in VALID_TYPES:
        client.replyMessage(
            Message(text=f"⚠️ Loại đánh không hợp lệ. Các loại: {', '.join(VALID_TYPES.keys())}"),
            message_object, thread_id, thread_type
        )
        return

    try:
        numbers = [int(num) for num in content[2].split(',')]
        bet_amount = int(content[3])
    except ValueError:
        client.replyMessage(
            Message(text="⚠️ Số đánh hoặc tiền cược không hợp lệ!"),
            message_object, thread_id, thread_type
        )
        return

    if len(numbers) != VALID_TYPES[bet_type]:
        client.replyMessage(
            Message(text=f"⚠️ {bet_type} phải đánh đúng {VALID_TYPES[bet_type]} số."),
            message_object, thread_id, thread_type
        )
        return

    current_money = get_money(author_id)
    if current_money < bet_amount:
        client.replyMessage(
            Message(text="⚠️ Bạn không đủ tiền để đặt cược!"),
            message_object, thread_id, thread_type
        )
        return

    # Confirm bet
    client.replyMessage(
        Message(text=f"🎲 Bạn đã đánh {bet_type.upper()} với số: {', '.join(map(str, numbers))} và số tiền {bet_amount:,}đ\nKết quả sẽ có sau 30 giây!"),
        message_object, thread_id, thread_type
    )

    # Generate results after 30 seconds
    import time
    time.sleep(30)

    results = generate_results()
    formatted_results = format_results(results)

    # Check win and calculate reward
    if check_win(bet_type, numbers, results):
        winnings = bet_amount * MULTIPLIERS[bet_type]
        add_money(author_id, winnings)
        summary = f"🎉 Chúc mừng! Bạn đã thắng {winnings:,}đ!"
    else:
        subtract_money(author_id, bet_amount)
        summary = f"😢 Rất tiếc, bạn đã thua {bet_amount:,}đ!"

    # Send final result
    result_msg = f"✨ KẾT QUẢ XỔ SỐ MIỀN BẮC ✨\n\n{formatted_results}\n\n{summary}"
    style = MultiMsgStyle([
        MessageStyle(offset=0, length=len(result_msg), style="font", size="13", auto_format=False),
        MessageStyle(offset=0, length=len(result_msg), style="color", color="#cdd6f4", auto_format=False)
    ])
    client.replyMessage(Message(text=result_msg, style=style), message_object, thread_id, thread_type)

def get_szl():
    return {
        'xsmb': handle_xsmb
    }