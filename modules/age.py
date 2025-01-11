import os
import json
from datetime import datetime, timedelta
import random
from zlapi.models import Message, MessageStyle, MultiMsgStyle

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Kiểm tra tuổi dựa trên ngày sinh"
}

def calculate_age(birth_date):
    today = datetime.now()
    birth_date = datetime.strptime(birth_date, "%d/%m/%Y")
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

def handle_check_age(message, message_object, thread_id, thread_type, author_id, client):
    content = message.strip().split()
    if len(content) != 2:
        client.replyMessage(Message(text="Cú pháp không đúng. Vui lòng nhập: !age <ngày/tháng/năm sinh>"), message_object, thread_id, thread_type)
        return

    try:
        birth_date = content[1]
        age = calculate_age(birth_date)
        today = datetime.now()
        birth_date = datetime.strptime(birth_date, "%d/%m/%Y")

        if today.month > birth_date.month or (today.month == birth_date.month and today.day >= birth_date.day):
            msg = f"Năm nay bạn {age + 1} tuổi."
        else:
            months_left = birth_date.month - today.month if birth_date.month > today.month else 12 - (today.month - birth_date.month)
            days_left = (birth_date - datetime(today.year, today.month, today.day)).days % 30
            msg = f"Năm nay bạn {age} tuổi. Còn {months_left} tháng {days_left} ngày nữa là bạn tròn {age + 1} tuổi."

        style = MultiMsgStyle([
            MessageStyle(offset=0, length=len(msg), style="font", size="13", auto_format=False),
            MessageStyle(offset=0, length=len(msg), style="color", color="#cdd6f4", auto_format=False)
        ])
        client.replyMessage(Message(text=msg, style=style), message_object, thread_id, thread_type)
    except ValueError:
        client.replyMessage(Message(text="Ngày tháng năm sinh không hợp lệ. Vui lòng nhập đúng định dạng DD/MM/YYYY"), message_object, thread_id, thread_type)


def get_szl():
    return {
        'age': handle_check_age
    }