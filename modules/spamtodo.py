import time
from zlapi.models import Message, ThreadType
from config import ADMIN

des = {
    'version': "1.0.2",
    'credits': "Nguyễn Đức Tài", #Kz mod thêm cái |
    'description': "Gửi spam công việc cho người dùng được tag"
}

def handle_spamtodo_command(message, message_object, thread_id, thread_type, author_id, client):
    if author_id in ADMIN:
        client.replyMessage(
            Message(text="Quyền lồn biên giới"),
            message_object, thread_id, thread_type
        )
        return

    # Tách cú pháp mới dựa trên dấu '|'
    parts = message.split('|')
    if len(parts) < 3:
        response_message = "Vui lòng cung cấp đúng cú pháp: spamtodo <uid> | <Nội dung công việc> | <Số lần spam>"
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    tagged_user = parts[0].strip().split(' ', 1)[1]  # Lấy UID từ phần đầu sau "spamtodo"
    content = parts[1].strip()
    try:
        num_repeats = int(parts[2].strip())
    except ValueError:
        response_message = f"Số lần phải là một số nguyên, bạn đã nhập: '{parts[2].strip()}'"
        client.replyMessage(Message(text=response_message), message_object, thread_id, thread_type)
        return

    for _ in range(num_repeats):
        client.sendToDo(
            message_object=message_object,
            content=content,
            assignees=[tagged_user],
            thread_id=tagged_user,
            thread_type=ThreadType.USER,
            due_date=-1,
            description="Soiz"
        )
        time.sleep(0.2)


def get_szl():
    return {
        'spamtodo': handle_spamtodo_command
    }
