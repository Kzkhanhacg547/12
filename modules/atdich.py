import json
import requests
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import wordnet
from zlapi.models import Message

# Thông tin module
des = {
    'version': "1.0.0",
    'credits': "Claude Assistant",
    'description': "Tự động dịch tin nhắn sang tiếng Việt"
}

def download_nltk_data():
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')

# Tải dữ liệu NLTK khi khởi động
download_nltk_data()

class AutoTranslateCommand:
    def __init__(self):
        self.auto_translate_enabled = {}  # Lưu trạng thái theo từng thread_id
        self.translator = GoogleTranslator(source='auto', target='vi')

    def get_word_types(self, word):
        """Xác định thể loại của từ."""
        synsets = wordnet.synsets(word)
        if not synsets:
            return {}

        pos_meanings = {}
        pos_map = {
            'n': 'danh từ',
            'v': 'động từ',
            'a': 'tính từ',
            'r': 'trạng từ',
            's': 'tính từ'
        }

        for syn in synsets:
            pos = syn.pos()
            pos_name = pos_map.get(pos, pos)
            if pos_name not in pos_meanings:
                pos_meanings[pos_name] = []

            meaning = self.translator.translate(syn.definition())
            if meaning not in pos_meanings[pos_name]:
                pos_meanings[pos_name].append(meaning)

        return pos_meanings

    def translate_single_word(self, word):
        """Dịch một từ đơn và xác định thể loại."""
        translated = self.translator.translate(word)
        pos_meanings = self.get_word_types(word)

        if not pos_meanings:
            return f"{word}: {translated}"

        response = f"{word}:\n"
        for pos, meanings in pos_meanings.items():
            response += f"• {pos}: {', '.join(meanings)}\n"
        return response

    def translate_sentence(self, text):
        """Dịch một câu hoặc đoạn văn."""
        translated = self.translator.translate(text)
        if text != translated:
            return f"Dịch: {translated}"
        return None

    def check_admin_permission(self, client, thread_id, author_id):
        """Kiểm tra quyền admin an toàn hơn."""
        try:
            group_info = client.fetchGroupInfo(thread_id)
            if group_info and thread_id in group_info:
                thread_info = group_info[thread_id]
                if 'adminIds' in thread_info and 'creatorId' in thread_info:
                    admin_ids = thread_info['adminIds']
                    creator_id = thread_info['creatorId']
                    if author_id in admin_ids and author_id != creator_id:
                        return False
            return True
        except Exception:
            # Nếu không lấy được thông tin nhóm, cho phép thực hiện lệnh
            return True

    def autodich(self, message, message_object, thread_id, thread_type, author_id, client):
        """Xử lý lệnh autodich."""
        # Tách command từ message
        parts = message.strip().split()
        if len(parts) < 2:
            client.send(
                Message(text="❌ Sử dụng: autodich [on/off]"),
                thread_id,
                thread_type
            )
            return

        command = parts[1].lower()

        try:
            # Kiểm tra quyền admin
            if not self.check_admin_permission(client, thread_id, author_id):
                client.send(
                    Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                    thread_id,
                    thread_type
                )
                return

            # Xử lý command
            if command == "on":
                self.auto_translate_enabled[thread_id] = True
                client.send(
                    Message(text="🤭 Tự động dịch đã được bật."),
                    thread_id,
                    thread_type
                )
            elif command == "off":
                self.auto_translate_enabled[thread_id] = False
                client.send(
                    Message(text="🤭 Tự động dịch đã được tắt."),
                    thread_id,
                    thread_type
                )
            else:
                client.send(
                    Message(text="❌ Lệnh không hợp lệ. Sử dụng: autodich [on/off]"),
                    thread_id,
                    thread_type
                )

        except Exception as e:
            client.send(
                Message(text=f"❌ Lỗi: {str(e)}"),
                thread_id,
                thread_type
            )

    def handle_message(self, message, message_object, thread_id, thread_type, author_id, client):
        """Xử lý tin nhắn khi chế độ tự động dịch được bật."""
        if not self.auto_translate_enabled.get(thread_id, False) or author_id == client.uid:
            return

        try:
            text = message.strip()
            words = text.split()

            # Xử lý dịch thuật
            if len(words) == 1:
                response = self.translate_single_word(text)
            else:
                response = self.translate_sentence(text)

            if response:
                client.send(
                    Message(text=response),
                    thread_id,
                    thread_type
                )

        except Exception as e:
            client.send(
                Message(text=f"🌸 Lỗi khi dịch: {str(e)}"),
                thread_id,
                thread_type
            )

# Khởi tạo instance của AutoTranslateCommand
auto_translate = AutoTranslateCommand()

def get_szl():
    return {
        'autodich': auto_translate.autodich,
        'handle_message': auto_translate.handle_message
    }