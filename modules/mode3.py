from zlapi.models import Message, ThreadType
from zlapi._message import Mention
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import wordnet

des = {
    'version': '1.0',
    'credits': 'ChatBot Developer',
    'description': 'Dịch văn bản tự động và quản lý chế độ tự động dịch'
}

def get_szl():
    return {
        'autodich': handle_autodich_command,
        '': handle_translate_message
    }

def handle_autodich_command(message, message_object, thread_id, thread_type, author_id, client):
    try:
        group_info = client.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            client.send(
                Message(text="🚦Lệnh bất khả thi với thí chủ."),
                thread_id,
                thread_type
            )
            return

        parts = message.split(" ")
        if len(parts) < 2:
            client.send(
                Message(text="🚦 Vui lòng nhập 'on' hoặc 'off' để bật/tắt tự động dịch."),
                thread_id,
                thread_type
            )
            return

        command = parts[1].lower()
        if command == "on":
            client.auto_translate_enabled = True
            client.send(
                Message(text="🤭 Tự động dịch đã được bật."),
                thread_id,
                thread_type
            )
        elif command == "off":
            client.auto_translate_enabled = False
            client.send(
                Message(text="🤭 Tự động dịch đã được tắt."),
                thread_id,
                thread_type
            )
        else:
            client.send(
                Message(text="🚦 Lệnh không hợp lệ. Vui lòng sử dụng 'on' hoặc 'off'."),
                thread_id,
                thread_type
            )
    except Exception as e:
        client.send(
            Message(text=f"❌ Lỗi: {str(e)}"),
            thread_id,
            thread_type
        )

def handle_translate_message(message, message_object, thread_id, thread_type, author_id, client):
    if author_id == client.uid:
        return

    try:
        message_content = ' '.join(message.split()[1:])
        if not message_content:
            client.send(
                Message(text="🚦 Vui lòng nhập nội dung cần dịch."),
                thread_id,
                thread_type
            )
            return

        words = message_content.strip().split()
        translator = GoogleTranslator(source='auto', target='vi')

        # Nếu là một từ đơn, dịch kèm theo thể loại
        if len(words) == 1:
            word = words[0]
            translated = translator.translate(word)

            try:
                # Tải wordnet nếu cần
                try:
                    synsets = wordnet.synsets(word)
                except LookupError:
                    nltk.download('wordnet')
                    synsets = wordnet.synsets(word)

                if synsets:
                    # Tạo dictionary để lưu các nghĩa theo thể loại
                    pos_meanings = {}
                    for syn in synsets:
                        pos = syn.pos()
                        pos_name = {
                            'n': 'danh từ',
                            'v': 'động từ',
                            'a': 'tính từ',
                            'r': 'trạng từ',
                            's': 'tính từ'
                        }.get(pos, pos)

                        if pos_name not in pos_meanings:
                            pos_meanings[pos_name] = []
                        if translated not in pos_meanings[pos_name]:
                            pos_meanings[pos_name].append(translated)

                    # Tạo chuỗi phản hồi
                    response = f"{word}: \n"
                    for pos, meanings in pos_meanings.items():
                        response += f"• {pos}: {', '.join(meanings)}\n"
                else:
                    response = f"{word}: {translated}"

            except Exception as e:
                response = f"{word}: {translated}"

        # Nếu là câu, chỉ dịch nghĩa
        else:
            translated = translator.translate(message_content)
            if message_content != translated:
                response = f"Dịch: {translated}"
            else:
                return

        client.send(Message(text=response), thread_id, thread_type)

    except Exception as e:
        client.send(
            Message(text=f"🌸 Lỗi khi dịch: {str(e)}"),
            thread_id,
            thread_type
        )