import os
import json
from datetime import datetime, timedelta
import random
import requests
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Load settings
with open('setting.json', 'r') as config_file:
    config = json.load(config_file)

API_URL = config.get("API", "")

# Metadata for the module
des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Taixiu Game"
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

# Initialize cooldown data
cooldown_data = {}

# Job definitions
jobs = {
    "1": {"name": "làm ngành", "reward_range": (500000, 700000)},
    "2": {"name": "làm ôsin", "reward_range": (15000, 25000)},
    "3": {"name": "làm điếm", "reward_range": (700000, 900000)},
    "4": {"name": "bán máu", "reward_range": (300000, 500000)},
    "5": {"name": "làm thợ sửa chữa", "reward_range": (100000, 200000)},
    "6": {"name": "làm phục vụ quán ăn", "reward_range": (20000, 40000)},
    "7": {"name": "dạy kèm", "reward_range": (40000, 60000)},
    "8": {"name": "làm bảo vệ", "reward_range": (50000, 90000)},
    "9": {"name": "làm tài xế", "reward_range": (100000, 150000)},
    "10": {"name": "làm nhà báo", "reward_range": (200000, 300000)},
}

def save_money_data():
    with open(money_file, "w") as file:
        json.dump(money_data, file)

def update_money_data():
    global money_data
    money_data = load_money_data()

def add_money(user_id, amount):
    update_money_data()
    money_data[user_id] = money_data.get(user_id, 0) + amount
    save_money_data()

def subtract_money(user_id, amount):
    update_money_data()
    if user_id in money_data:
        money_data[user_id] = max(0, money_data[user_id] - amount)
    save_money_data()

def get_money(user_id):
    update_money_data()
    return money_data.get(user_id, 0)

def check_cooldown(author_id, job_id):
    if author_id in cooldown_data:
        if job_id in cooldown_data[author_id]:
            return datetime.now() < cooldown_data[author_id][job_id]
    return False

def update_cooldown(author_id, job_id):
    if author_id not in cooldown_data:
        cooldown_data[author_id] = {}
    cooldown_data[author_id][job_id] = datetime.now() + timedelta(seconds=60)

def get_random_reward(job_id):
    if job_id in jobs:
        min_reward, max_reward = jobs[job_id]['reward_range']
        return random.randint(min_reward, max_reward)
    return 0

def handle_check_money(message, message_object, thread_id, thread_type, author_id, client):
    user_money = get_money(author_id)
    reply_message = f"💳 • Money Current: {user_money} VND."
    style_checkmoney = MultiMsgStyle([
        MessageStyle(offset=0, length=10, style="font", size="12", auto_format=False),
        MessageStyle(offset=10, length=len(reply_message.encode()) - 10, style="font", size="13", auto_format=False),
        MessageStyle(offset=10, length=len(reply_message.encode()) - 10, style="color", color="#cdd6f4", auto_format=False),
        MessageStyle(offset=11, length=len(reply_message.split(": ")[1].strip()), style="color", color="#a6adc8", auto_format=False)
    ])
    client.replyMessage(Message(text=reply_message, style=style_checkmoney), message_object, thread_id, thread_type)

def handle_set_money(message, message_object, thread_id, thread_type, author_id, client):
    if author_id != "8697905534842942934":
        client.replyMessage(Message(text="Bạn không có quyền sử dụng lệnh này."), message_object, thread_id, thread_type)
        return

    content = message.strip().split()
    if len(content) < 3 or not message_object.mentions:
        client.replyMessage(Message(text="Cú pháp không đúng. Vui lòng sử dụng: !setmoney @người_dùng <số tiền>"), message_object, thread_id, thread_type)
        return

    mentioned_user = message_object.mentions[0]
    user_id = mentioned_user['uid']
    try:
        amount_str = content[-1].replace(",", "").replace(".", "")
        amount = int(amount_str)
        add_money(user_id, amount)
        reply_message = f"• Added amount {amount} VND for user id: {user_id}."
        style_setmoney = MultiMsgStyle([
            MessageStyle(offset=0, length=10, style="font", size="12", auto_format=False),
            MessageStyle(offset=10, length=len(reply_message.encode()) - 10, style="font", size="13", auto_format=False)
        ])
        client.replyMessage(Message(text=reply_message, style=style_setmoney), message_object, thread_id, thread_type)
    except ValueError:
        client.replyMessage(Message(text="Số tiền không hợp lệ. Vui lòng nhập một số."), message_object, thread_id, thread_type)

def handle_work(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()
    if len(content) != 2 or content[1] not in jobs:
        job_options = "\n".join([f"{k}: {v['name']}" for k, v in jobs.items()])
        client.replyMessage(Message(text=f"Vui lòng chọn một công việc:\n{job_options}"), message_object, thread_id, thread_type)
        return

    job_id = content[1]
    if check_cooldown(author_id, job_id):
        client.replyMessage(Message(text="Bạn phải chờ 60 giây để làm công việc này lại."), message_object, thread_id, thread_type)
        return

    update_cooldown(author_id, job_id)
    job_name = jobs[job_id]['name']
    job_reward = get_random_reward(job_id)
    add_money(author_id, job_reward)
    reply_message = f"• bạn đã {job_name} và nhận được {job_reward} VND."
    style_lamviec = MultiMsgStyle([
        MessageStyle(offset=0, length=10, style="font", size="12", auto_format=False),
        MessageStyle(offset=10, length=len(reply_message.encode()) - 10, style="font", size="13", auto_format=False)
    ])
    client.replyMessage(Message(text=reply_message, style=style_lamviec), message_object, thread_id, thread_type)





def handle_taixiu(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()
    if len(content) < 3:  # Kiểm tra đủ 3 phần: lệnh, loại cược (tài/xỉu), số tiền
        client.replyMessage(Message(text="Cú pháp không hợp lệ. Vui lòng sử dụng cú pháp: tx <tài/xỉu> <tiền>"), message_object, thread_id, thread_type)
        return

    bet_type = content[1].strip().lower()  # Chuẩn hóa loại cược
    if bet_type not in ['tài', 'xỉu']:  # Kiểm tra loại cược hợp lệ
        client.replyMessage(Message(text="Loại cược không hợp lệ. Vui lòng chọn 'tài' hoặc 'xỉu'."), message_object, thread_id, thread_type)
        return

    try:
        bet_amount = int(content[2])  # Lấy số tiền cược
    except ValueError:
        client.replyMessage(Message(text="Số tiền cược không hợp lệ. Vui lòng nhập một số."), message_object, thread_id, thread_type)
        return

    current_money = get_money(author_id)  # Lấy số tiền hiện tại của người chơi
    if current_money < 1000:
        client.replyMessage(Message(text="Bạn cần ít nhất 1000 VND để chơi tài xỉu."), message_object, thread_id, thread_type)
        return

    if bet_amount < 1000:
        client.replyMessage(Message(text="Số tiền cược tối thiểu là 1000 VND."), message_object, thread_id, thread_type)
        return

    if bet_amount > current_money:
        client.replyMessage(Message(text="Bạn không có đủ tiền để đặt cược."), message_object, thread_id, thread_type)
        return

    try:
        response = requests.get(f"{API_URL}/game/taixiu")
        if response.status_code == 200:
            data = response.json()
            total = data.get("total", None)
            result = data.get("result", "").strip().lower()  # Chuẩn hóa kết quả từ API

            if total is None or result not in ['tài', 'xỉu']:
                client.replyMessage(Message(text="Dữ liệu API không hợp lệ."), message_object, thread_id, thread_type)
                return

            # So sánh kết quả cược của người chơi với kết quả API
            if bet_type == result:
                add_money(author_id, bet_amount)
                content = f"Tổng điểm: {total}, Kết quả: {result.capitalize()}. Bạn đã thắng cược {bet_amount}!"
            else:
                subtract_money(author_id, bet_amount)
                content = f"Tổng điểm: {total}, Kết quả: {result.capitalize()}. Bạn đã thua cược {bet_amount}."

            # Gửi tin nhắn nội dung thắng/thua
            client.replyMessage(Message(text=content), message_object, thread_id, thread_type)


    except Exception as e:
        client.replyMessage(Message(text=f"Unexpected error: {e}"), message_object, thread_id, thread_type)



def get_szl():
    return {
        'checkmoney': handle_check_money,
        'setmoney': handle_set_money,
        'lamviec': handle_work,
        'tx': handle_taixiu
    }