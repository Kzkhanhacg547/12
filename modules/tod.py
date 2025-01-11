import json
import random
from datetime import datetime, timedelta
from zlapi.models import Message, MessageStyle, MultiMsgStyle

# Metadata cho module
des = {
    'version': '1.0.0',
    'credits': 'Kz Khánhh',
    'description': 'Truth or Dare game'
}

# Danh sách câu hỏi thật
truth_questions = [
    "Có coi phim sex bao giờ chưa?",
    "Hôm nay mặc quần xì màu gì?",
    "Có thủ dâm bao giờ chưa ?",
    "Có quan hệ tình dục bao giờ chưa?",
    "Bị ăn sừng bao nhiêu lần rồi?",
    "Bạn đã bao giờ đi tiểu trong bể bơi chưa?",
    "Bạn đã bao giờ trốn học chưa?",
    "Hôm nay mặc áo dzú màu gì?",
    "Bạn đã ngửi quần lót của mình để kiểm tra xem chúng có bị bẩn không?",
    "Nếu bạn có thể hôn ai đó ngay bây giờ bạn sẽ hôn ai?",
    "Điều kinh tởm nhất mà bạn từng say là gì?",
    "Có cởi đồ khi đi ngủ không?",
    "Có chụp ảnh nude hoặc quay video không",
    "Vị trí yêu thích của bạn trên giường là gì?",
    "Bạn thích doggy hay cổ điển",
    "Có coi phim sex bao giờ chưa?","Hôm nay mặc quần xì màu gì?","Có thủ dâm bao giờ chưa ?","Có quan hệ tình dục bao giờ chưa?","Bị ăn sừng bao nhiêu lần rồi?","Bạn đã bao giờ đi tiểu trong bể bơi chưa?","Bạn đã bao giờ trốn học chưa?","Hôm nay mặc áo dzú màu gì?","Bạn đã ngửi quần lót của mình để kiểm tra xem chúng có bị bẩn không?","Nếu bạn có thể hôn ai đó ngay bây giờ bạn sẽ hôn ai?","Điều kinh tởm nhất mà bạn từng say là gì?", "Có cởi đồ khi đi ngủ không?","Có chụp ảnh nude hoặc quay video không", "Vị trí yêu thích của bạn trên giường là gì?","Bạn thích doggy hay cổ điển", "Thích được bắn vào trong hay lên mặt ?","Đã đi đá phò bao giờ chưa","Một tháng thủ dâm mấy lần","Thích cu dài hay ngắn ?","Khi thủ dâm trong đầu nghĩ đến ai ?","Có từng có suy nghĩ quan hệ 18+ với ny không ?","Có thích buscu không?","Thích cu to hay bé","Lông nách có nhiều không","Hay coi web sex nào ?","Thích mặt quần lọt khe hay ren ?","Có hay bị nốn lừng đêm khuya không?","Bạn muốn có bao nhiêu đứa trẻ?","Một sự thật đáng xấu hổ mà tôi nên biết về bạn là gì?","Nụ hôn đầu tiên của bạn như thế nào?","Thích cu dài hay ngắn","Số đo 3 vòng của bạn bao nhiêu","Thích kích thước hay kinh nghiệm trong chuyện xxxx","Ăn cứt mũi bao giờ chưa","Khi thủ dâm nghĩ về ai","Có ý định quan hệ với người yêu bao giờ chưa ?","Cháo lưỡi bao giờ chưa","Có thường xuyên thủ dâm hay không","Có nghiện sex hay không","Nơi yêu thích của bạn để được hôn?","Khoảng thời gian dài nhất khi quan hệ tình dục bạn từng đưa ra là bao nhiêu?","Bạn thích quan hệ tình dục thô bạo hay chậm rãi?","Bạn thích ở trên cùng hay dưới cùng khi quan hệ 18+","Diễn viên phim sex bạn ưa thích là ai?","Bạn thích bạn tình của mình im lặng, hay bạn thích rên rỉ?","Nhổ hoặc nuốt khi quan hệ 18+ ? (BJ)","Bạn còn nhớ nyc không", "Bạn có ý định quay lại với nyc không", "Bạn có bị hôi nách không", "Chia sẽ trải nghiệm lần đầu khi cháo lưỡi với người yêu"
]

# Danh sách thử thách
dare_challenges = [
    "nhắn vs Ny là I love you 3000 :3","Thách đú trend vs 1 người bạn quen qua face","Qua Lượt","Để Avt đôi với 1 người lạ","Nhắn Tin Yêu Với 1 người bất kỳ","Tỏ tình cr hoặc 1 ng bất kỳ","Nói 1 sự thật","show ảnh của 1 người bạn đẹp nhất","cà khịa 1 đứa trong gr","Bốc phốt 1 đứa trong group","Hôn 1 đứa trong group bằng lệnh #kiss [ tag nó vô ]","Hãy nói ra 1 câu nói khiến bạn buồn nhất","Điều bây giờ bạn muốn nhất là gì","Hãy nói xấu 1 đứa bạn","hãy kể 1 việc bạn từng làm khiến mn kinh ngạc :c","Thứ Khiến bạn vui nhất là gì","Hãy kể 1 lần chơi ngu của em 😏","Bạn thấy trong group này ai xinh nhất ","bạn giỏi môn gì nhất","Hãy tạo 1 câu thơ tỏ tình cả group 💁‍♂️","hãy sử dụng tính chất môn bạn giỏi nhất để tỏ tình gr","Vào FaceBook Của Admin Bão Like", "Nhắn Tỏ Tình Với Admin", "Ghi Âm Hát Một Bài Nhạc Bất Kì", "Ghi Âm Với Nội Dung Là Yêu Admin Nhất", "Để hình admin làm avt 1 days", "Voice Rên 10s", "Quay video và nói yêu admin rất nhiều", "Ăn một thìa cà phê gia vị bất kì trong bếp", "Gửi một tấm ảnh lúc bé của bạn", "Gửi một tấm ảnh dìm của bạn", "Quay video và nói một câu bất kì với cái lưỡi lè ra trong lúc nói", "Đăng một trạng thái dài dòng, vô nghĩa trên Facebook.", "Bắt chước một ngôi sao YouTube cho đến khi một người chơi khác đoán được bạn đang thể hiện vai diễn của ai.", "Gọi cho một người bạn, giả vờ đó là sinh nhật của họ và hát cho họ nghe Chúc mừng sinh nhật", "Quay video thè lưỡi và sủa 3 tiếng", "Chụp một tấm hình với gương mặt gợi cảm", "Voice một đoạn sau đây và gửi vào box: Dùng giọng văn hay nhất đọc câu sau: Hừ, do anh hết á! Cũng không dỗ người ta gì hết (｡•ˇ‸ˇ•｡) Người ta muốn khóc quá nè, đấm bể ngực mấy người, đồ xấu xa!! (￣^￣)ゞđấm bể ngực mấy người! Đáng ghét!! Muốn ôm ôm ~~~ huhuhu… hừm, đồ xấu xa, đánh chết mấy người luôn!!", "Gọi cho admin và một câu ngọt ngào", "Nhắn tin cho nyc bảo quay lại", "Tự vã vào mặt 3 cái", "Ghi âm một câu em nhớ anh cho admin", "Nhắn tin cho bạn thân và bảo là tao đang nứng uwu","Đặt ngôn ngữ điện thoại di động của bạn thành tiếng Trung","Đi bằng bốn chân và hành động như một con chó cho đến lượt tiếp theo của bạn","Hôn người bạn cùng giới ngồi cạnh, bất kể vị trí nào đều được.","Gởi tin nhắn cho người bạn bất kỳ: Đi ỉa chung hong? Tui đem giấy rồi nè.","Gửi cho người bạn cùng giới thân thiết nhất một tin nhắn: “Tôi thật sự thích cậu lâu lắm rồi, chờ đó tôi đến ngay! Thật! Không phải giỡn chơi đâu.”","Chat sex với một người bất kì trong list bạn bè 5 phút","Lấy quần đội lên đầu và chụp hình lại gửi vào đây", "Hãy tự dơ cánh tay lên và ngửi nách của bạn", "Hãy nhắn cho người yêu cũ một câu gạ tình và cap lại màn hình gửi vào group này", "Nhắn vs Ny là I love you 3000 :3",
    "Thách đú trend vs 1 người bạn quen qua face",
    "Qua Lượt",
    "Để Avt đôi với 1 người lạ",
    "Nhắn Tin Yêu Với 1 người bất kỳ",
    "Tỏ tình cr hoặc 1 ng bất kỳ",
    "Nói 1 sự thật",
    "Show ảnh của 1 người bạn đẹp nhất",
    "Cà khịa 1 đứa trong gr",
    "Bốc phốt 1 đứa trong group",
    "Hôn 1 đứa trong group",
    "Hãy nói ra 1 câu nói khiến bạn buồn nhất",
    "Điều bây giờ bạn muốn nhất là gì",
    "Hãy nói xấu 1 đứa bạn",
    "Hãy kể 1 việc bạn từng làm khiến mn kinh ngạc"
]

# Lưu trữ cooldown cho người chơi
cooldowns = {}

def check_cooldown(user_id):
    """Kiểm tra cooldown của người chơi"""
    if user_id in cooldowns:
        if datetime.now() < cooldowns[user_id]:
            return True
    return False

def set_cooldown(user_id, seconds=300):  # 5 phút cooldown
    """Thiết lập cooldown cho người chơi"""
    cooldowns[user_id] = datetime.now() + timedelta(seconds=seconds)

def create_styled_message(text, primary_color="#cdd6f4"):
    """Tạo tin nhắn với style được định dạng"""
    return Message(
        text=text,
        style=MultiMsgStyle([
            MessageStyle(offset=0, length=len(text), style="font", size="13", auto_format=False),
            MessageStyle(offset=0, length=len(text), style="color", color=primary_color, auto_format=False)
        ])
    )

def handle_tod(message, message_object, thread_id, thread_type, author_id, client):
    """Xử lý lệnh TOD"""
    # Kiểm tra cooldown
    if check_cooldown(author_id):
        remaining_time = (cooldowns[author_id] - datetime.now()).seconds
        response = f"⏳ Vui lòng đợi {remaining_time} giây nữa để sử dụng lại lệnh này."
        client.replyMessage(create_styled_message(response), message_object, thread_id, thread_type)
        return

    content = message.strip().split()

    if len(content) != 2:
        guide = """Cách dùng: 
tod 1: Chơi thử thách (Dare)
tod 2: Chơi sự thật (Truth)

🎮 Hãy chọn một trong hai lựa chọn trên!"""
        client.replyMessage(create_styled_message(guide), message_object, thread_id, thread_type)
        return

    choice = content[1]

    if choice == "1":
        challenge = random.choice(dare_challenges)
        response = f"🎲 DARE: {challenge}"
        client.replyMessage(create_styled_message(response), message_object, thread_id, thread_type)
        set_cooldown(author_id)
    elif choice == "2":
        truth = random.choice(truth_questions)
        response = f"🎯 TRUTH: {truth}"
        client.replyMessage(create_styled_message(response), message_object, thread_id, thread_type)
        set_cooldown(author_id)
    else:
        client.replyMessage(create_styled_message("❌ Lựa chọn không hợp lệ! Sử dụng 'tod 1' hoặc 'tod 2'"), message_object, thread_id, thread_type)

def get_szl():
    """Trả về dictionary các lệnh"""
    return {
        'tod': handle_tod
    }