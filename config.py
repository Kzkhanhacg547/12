IMEI = "b03d7492-c38d-4fe6-b5d4-a9c1285fff11-7675d59b5e84e0a878ee6f0a97f9056f"
SESSION_COOKIES = {"_ga":"GA1.2.1782749144.1735464586","__zi":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","__zi-legacy":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","ozi":"2000.UelfvS0R1PqpcVIltHyTt6UL_Rp0HqkNRP3zly55JDzabVhnmK97scAKz_ur.1","_zlang":"vn","app.event.zalo.me":"2456638497330600094","_gid":"GA1.2.1671209458.1736448389","zpsid":"axzF.421600670.9.Hdq_aReYvsWaFyPnjYBdQCzHbLo84z5OYXJGM175rZxOX7V2kxkdwTqYvsW","zpw_sek":"Clbq.421600670.a0.w6Pl2WVyMggPuNkp9lnQgdpUFy4bndZPQAznnpM60iHDbXJ9LvLltLEBRi9WmMU8UbUzcr6U_3gj_S7gXfjQgW"}
API_KEY = "api_key"
SECRET_KEY = "secret_key"
PREFIX = "!"
ADMIN = "968896132353789689"





import re
import os
import json
SETTING_FILE= "setting.json"
#Không chỉnh sửa nếu bạn không có kinh nghiệm
def read_settings():
    """Đọc toàn bộ nội dung từ file JSON."""
    try:
        with open(SETTING_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_settings(settings):
    """Ghi toàn bộ nội dung vào file JSON."""
    with open(SETTING_FILE, 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)


def is_admin(author_id):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    if author_id in admin_bot:
        return True
    else:
        return False
def get_user_name_by_id(bot,author_id):
    try:
        user = bot.fetchUserInfo(author_id).changed_profiles[author_id].displayName
        return user
    except:
        return "Unknown User"

def handle_bot_admin(bot):
    settings = read_settings()
    admin_bot = settings.get("admin_bot", [])
    if bot.uid not in admin_bot:
        admin_bot.append(bot.uid)
        settings['admin_bot'] = admin_bot
        write_settings(settings)
        print(f"Đã thêm 👑{get_user_name_by_id(bot, bot.uid)} 🆔 {bot.uid} cho lần đầu tiên khởi động vào danh sách Admin 🤖BOT ✅")

settings= read_settings()
ADMIN = [settings.get("admin_bot", [])]