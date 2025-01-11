import random
from datetime import datetime
from zlapi.models import Message, ZaloAPIException

des = {
    'version': "1.0.0",
    'credits': "Kz Khánhh",
    'description': "Xem mức độ duyên của bạn với một ai đó"
}

def get_vietnam_time():
    return datetime.now().strftime("%H:%M:%S - %d/%m/%Y")

def handle_xemduyen_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        query = ' '.join(message.split()[1:])  
        if " | " not in query:
            error_message = Message(text="Vui lòng nhập đúng cú pháp: /xemduyen [tên của bạn] | [tên của người đó]")
            client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
            return

        your_name, their_name = query.split(" | ")

      
        duyen = random.randint(0, 100)

        
        current_time = get_vietnam_time()

       
        if duyen >= 80:
            message_text = f"💖 Mức độ duyên giữa {your_name} và {their_name} là: {duyen}%\nChúc mừng! Các bạn có một mối liên kết rất mạnh mẽ.\n⏰ Thời gian: {current_time}\nHãy tận hưởng tình bạn hoặc mối quan hệ tuyệt vời này!"
        elif duyen >= 50:
            message_text = f"😊 Mức độ duyên giữa {your_name} và {their_name} là: {duyen}%\nCác bạn có một mối quan hệ khá tốt, nhưng có thể còn cải thiện thêm!\n⏰ Thời gian: {current_time}\nHãy dành thời gian để hiểu nhau hơn!"
        else:
            message_text = f"😅 Mức độ duyên giữa {your_name} và {their_name} là: {duyen}%\nMối quan hệ này có thể cần thời gian và sự cố gắng nhiều hơn.\n⏰ Thời gian: {current_time}\nĐừng bỏ cuộc, mọi thứ có thể thay đổi theo thời gian!"

        # Gửi tin nhắn
        client.replyMessage(Message(text=message_text), message_object, thread_id=thread_id, thread_type=thread_type)

    except ZaloAPIException as e:
        error_message = Message(text=f"Lỗi Zalo API: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)
    except Exception as e:
        error_message = Message(text=f"Đã xảy ra lỗi: {str(e)}")
        client.replyMessage(error_message, message_object, thread_id=thread_id, thread_type=thread_type)

def get_szl():
    return {
        'xemduyen': handle_xemduyen_command
    }
