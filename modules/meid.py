from zlapi import ZaloAPI
from zlapi.models import *
des = {
    'version': "1.0.1",
    'credits': "huang",
    'description': "xem id bản thân."
}
def handle_meid_command(message, message_object, thread_id, thread_type, author_id, client):
    user_id = author_id

    response_message = f"{user_id}"

    message_to_send = Message(text=response_message)

    client.replyMessage(message_to_send, message_object, thread_id, thread_type)
    
def get_szl():
    return {
        'meid': handle_meid_command
    }
