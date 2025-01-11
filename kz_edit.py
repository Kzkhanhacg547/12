import os
import random
import threading
import pyshorteners
from googletrans import Translator
from deep_translator import GoogleTranslator
import qrcode
import requests
import urllib
import os
from datetime import timedelta

import subprocess
from zlapi.models import Message, Mention, MessageStyle, MultiMsgStyle
from zlapi import ZaloAPI
import threading
import sys

from gtts import gTTS
from io import BytesIO
from PIL import Image
import json
import time
import os

from datetime import datetime
import json
import urllib.parse
import requests
from PIL import Image
from zlapi import ZaloAPI
from zlapi.models import Message
from io import BytesIO
import io
import threading
from removebg import RemoveBg
import hashlib
import requests
from zlapi.models import Message
from zlapi import ZaloAPI
import threading 

from zlapi import ZaloAPI
from zlapi.models import Message
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

class Honhattruong(ZaloAPI):
    def __init__(self, api_key, secret_key, imei, session_cookies):
        super().__init__(api_key, secret_key, imei=imei, session_cookies=session_cookies)
        self.rmbg = RemoveBg(api_key, "error.log")
        self.rmbg = RemoveBg("TuW7DFuDstmHn1fRRkvSD3CK", "error.log")
        self.start_time = time.time()
        self.last_sent = None  
        self.selection_timer = {}
        self.reply_images = []
        self.user_selection_status = {}
        self.search_results = []  
        self.next_step = {}
        self.last_sms_times = {}
        self.autodl_enabled = False
        self.last_search_name = None
        self.auto_translate_enabled = False

    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"\033[32m{message} \033[39m|\033[31m {author_id} \033[39m|\033[33m {thread_id}\033[0m\n")
        if not isinstance(message, str):
            return
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        self.anti_all(message_object, thread_id, author_id)
        if isinstance(message, str):
            threading.Thread(
                target=self.handle_mention_command,
                args=(message, message_object, thread_id, thread_type)
            ).start()
        if content.startswith("/scl"):
            threading.Thread(target=self.handle_scl_command, args=(message, message_object, thread_id, thread_type)).start()
        if isinstance(message, str) and message.startswith("stk"):
            mentions = message_object.mentions if hasattr(message_object, 'mentions') else []
            if mentions:
                mentioned_user_id = mentions[0]['uid']
                user_info = self.fetchUserInfo(mentioned_user_id)
                if user_info and mentioned_user_id in user_info.changed_profiles:
                    avatar_url = user_info.changed_profiles[mentioned_user_id].avatar
                    self.create_sticker(avatar_url, message_object, thread_id, thread_type)

        if isinstance(content, str) and content.startswith("dlfb"):
            threading.Thread(target=self.handle_dlfb_command, args=(content, message_object, thread_id, thread_type)).start()
        if isinstance(message, str) and message.startswith("sms"):
            threading.Thread(
                target=self.handle_sms_command,
                args=(message, message_object, thread_id, thread_type, author_id)
            ).start()
        if content.startswith("nhac"):
            threading.Thread(target=self.handle_getvoice_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        if isinstance(message, str) and message.startswith("link"):
            threading.Thread(
                target=self.handle_link_command,
                args=(message, message_object, thread_id, thread_type)
            ).start()
        if isinstance(message, str) and message.startswith("catbot"):
            threading.Thread(
                target=self.handle_catbot_command,
                args=(message, message_object, thread_id, thread_type)
            ).start()
        if isinstance(message, str) and message.startswith("qr"):
            threading.Thread(
                target=self.handle_qr_command,
                args=(message, message_object, thread_id, thread_type)
            ).start()
        if content.startswith("autodl"):
                threading.Thread(target=self.handle_autodl_command, args=(author_id, message, message_object, thread_id, thread_type)).start()
        elif self.autodl_enabled and self.is_tiktok_url(content):
                threading.Thread(target=self.handle_tiktok_download, args=(content, message_object, thread_id, thread_type)).start()
        if content.startswith("st"):
                threading.Thread( target=self.handle_stk_command, args=(message, message_object, thread_id, thread_type)).start()
        if content.startswith("gif"):
                threading.Thread(target=self.handle_gif_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        elif content.startswith("taogif"):
                threading.Thread(target=self.handle_taogif_command, args=(message, message_object, thread_id, thread_type)).start()
        if content.startswith("sr"):
            threading.Thread(target=self.handle_sr_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        elif author_id in self.next_step and self.next_step[author_id] == 'wait_select':
            threading.Thread(target=self.handle_selection, args=(message, message_object, thread_id, thread_type, author_id)).start()

        if content.startswith("~gif"):
            self.handle_gif_command(content, message_object, thread_id, thread_type, author_id)
        if isinstance(content, str) and content.startswith("sos"):
            threading.Thread(target=self.handle_sos, args=(thread_id, thread_type, message_object, author_id)).start()
        elif isinstance(content, str) and content.startswith("unlock"):
            threading.Thread(target=self.handle_unlock, args=(thread_id, thread_type, message_object, author_id)).start()
        if isinstance(message, str) and message.startswith("info"):
            user_id = author_id
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            user_info = self.fetchUserInfo(user_id) or {}
            user_data = user_info.get('changed_profiles', {}).get(user_id, {})
            canvas_path = self.create_canvas(user_data)
            if os.path.exists(canvas_path):
                self.sendLocalImage(
                    canvas_path,
                    message=None,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1600,
                    height=1039,
                    ttl=240000
                )
                os.remove(canvas_path)
        if message.startswith("add"):
            self.process_add_command(author_id, message, message_object, thread_id, thread_type)

        if isinstance(content, str) and content.startswith("ifcc"):
            threading.Thread(target=self.handle_ifcc_command, args=(message, message_object, thread_id, thread_type)).start()

        content = message.strip().split()

        if len(content) >= 2 and content[0] == "autodich":
            threading.Thread(target=self.handle_autodich_command, args=(content[1], message_object, thread_id, thread_type, author_id)).start()

        if self.auto_translate_enabled:
            threading.Thread(target=self.handle_translate_message, args=(message, message_object, thread_id, thread_type, author_id)).start()

        if message.startswith("dich"):
            threading.Thread(target=self.handle_translate_command, args=(message, message_object, thread_id, thread_type, author_id)).start()

        content = message.strip().split()
        if len(content) >= 2 and content[0] == "srcc":
            threading.Thread(target=self.handle_capcutvd_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        if isinstance(content, str) and content.startswith("thinh"):
            threading.Thread(target=self.handle_thinh_command, args=(message_object, thread_id, thread_type)).start()
        if isinstance(content, str) and content.startswith("ura"):
            threading.Thread(target=self.handle_ura_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("voice"):
            threading.Thread(target=self.handle_voice_command, args=(message, message_object, thread_id, thread_type)).start()

        if message.startswith("tiengmenu"):
            threading.Thread(target=self.handle_languages_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("share "):
            threading.Thread(target=self.handle_share_command, args=(message, message_object, thread_id, thread_type)).start()
        elif message.strip() == "sharemenu":
            threading.Thread(target=self.handle_sharemenu_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("rs"):
            threading.Thread(target=self.handle_restart, args=(message, message_object, thread_id, thread_type, author_id)).start()

        if message.startswith("mrk"):
            threading.Thread(target=self.handle_mrk_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("sophan"):
            threading.Thread(target=self.handle_sophan_command, args=(message, message_object, thread_id, thread_type, author_id)).start()

        if message.startswith("cardif"):
            threading.Thread(target=self.handle_cardif_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("bnc2"):
            threading.Thread(target=self.handle_bnc2_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("bnc1"):
            threading.Thread(target=self.handle_bnc1_command, args=(message, message_object, thread_id, thread_type)).start()

        if message.startswith("anhbia"):
            threading.Thread(target=self.handle_anhbia_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("fk"):
            threading.Thread(target=self.handle_fk_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("giangsinh"):
            threading.Thread(target=self.handle_giangsinh_command, args=(message, message_object, thread_id, thread_type)).start()

        if message.startswith("danhthiep"):
            threading.Thread(target=self.handle_danhthiep_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("wibu"):
            threading.Thread(target=self.handle_wibu_command, args=(message, message_object, thread_id, thread_type)).start()

        if message.startswith("blink"):
            threading.Thread(target=self.handle_blink_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("if3"):
            threading.Thread(target=self.handle_infov3_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("if2"):
            threading.Thread(target=self.handle_infov2_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("if1"):
            threading.Thread(target=self.handle_infov1_command, args=(message, message_object, thread_id, thread_type)).start()

        if message.startswith("dlyt"):
            threading.Thread(target=self.handle_dlyt2_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("srp"):
            threading.Thread(target=self.handle_srp_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("uptime"):
            threading.Thread(target=self.handle_uptime_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("ttsr"):
            threading.Thread(target=self.handle_ttsr_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("thuphap"):
            threading.Thread(target=self.handle_thuphap_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        if message.startswith("6mui"): threading.Thread(target=self.handle_6mui_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("anhloli"): threading.Thread(target=self.handle_anhloli_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("anhanime"): threading.Thread(target=self.handle_anhanime_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("anhcos"):
            threading.Thread(
                target=self.handle_gaicos_command,
                args=(message_object, thread_id, thread_type)
            ).start()
        if message.startswith("dltw"):
            threading.Thread(target=self.handle_dltw_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("gaicos"): threading.Thread(target=self.handle_gaicos_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("vdgai"): threading.Thread(target=self.handle_vdgai_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("meme"): threading.Thread(target=self.handle_meme_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("menuv2"):
            threading.Thread(target=self.handle_menu, args=(thread_id, thread_type)).start()
        elif message.startswith("anhgai"):
            threading.Thread(target=self.handle_anhgai_command, args=(thread_id, thread_type)).start()
        if message.startswith("vdchill"): threading.Thread(target=self.handle_vdchill_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("vdtet"):
            threading.Thread(target=self.handle_vdtet_command, args=(message_object, thread_id, thread_type)).start()
        if message.startswith("dltt"):
            threading.Thread(target=self.handle_dltt_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("dlcc"):
            threading.Thread(target=self.handle_dlcc_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("rsyt"):
            threading.Thread(target=self.handle_dlyt_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("canva"):
            threading.Thread(target=self.handle_canva_command, args=(message, message_object, thread_id, thread_type)).start()
        if message.startswith("todo"):
            threading.Thread(target=self.handle_todo_command, args=(message, message_object, thread_id, thread_type, author_id)).start()
        elif message.startswith("add"):
            threading.Thread(target=self.handle_add_command, args=(message_object, thread_id, thread_type, author_id)).start()
        elif message.startswith("revo"):
            threading.Thread(target=self.handle_revo_command, args=(message_object, thread_id, thread_type, author_id)).start()


    def handle_menu(self, thread_id):
        menu_text = """
      __/°°°°°°°°°°°°°°°°°°°°°°°°°°°\🏔
      🗺𝑀𝐸𝑁𝑈 𝑉2🗾
        🌸 #anhgai: Gửi ảnh ngẫu nhiên từ danh sách URL.
        🌸 #gaicos: ảnh gái cospay.
        🌸 #anhanime: ảnh anime.
        🌸 #anhloli: ảnh loli.
        🌸 #6mui:  ảnh sáu múi.
        🌸 #meme: ảnh meme.
        🌸 #vdgai: video gái.
        🌸 #gaicos: video gái cót pờ lay. 
        🌸 #vdchill: video chill. 
        🌸 #vdtet: video tết. 
        🌸 #dltt url: tải video tiktok. 
        🌸 #dltw url: tải video tiktok.
        🌸 #dlcc url: tải video capcup. 
        🌸 #rsyt name: tìm kiếm video. 
        🌸 #canva name: tạo ảnh với name. 
        🌸 #thuphap : tạo ảnh thư pháp. 
        🌸 #ttsr name : tiềm kiếm vd titkok. 
        🌸 #dlyt url :tải video Youtube. 
        🌸 #srp name : tìm kiếm nhạc spo. 
        🌸 #uptime : xem tgian hoạt động bot. 
        🌸 #add : thêm id spam todo gr. 
        🌸 #revo : xoá id spam todo. 
        🌸 #todo sl nd : spam gr. 
        🌸 #if2 name id sbn : ảnh info v2. 
        🌸 #if3  : ảnh info v3. 
        🌸 #if1  : ảnh info v1. 
        🌸 #blink id demay  : ảnh blink. 
        🌸 #wibu id name name  : ảnh blink. 
        🌸 #danhthiep text1, text2  : danh thiếp. 
        🌸 #giangsinh name  : ảnh giáng sinh. 
        🌸 #fk[text1] [text2] [text3] [text4] [urlimg  : fkccc. 
        🌸 #anhbia   : tạo ảnh bài. 
        🌸 #bnc1   : tạo ảnh banner.
        🌸 #bnc2   : tạo ảnh banner. 
        🌸 #cardif  : tạo card info người dùng. 
        🌸 #sophan name : xem số phận tương lai. 
        🌸 #mrk : tạo ảnh marketing. 
        🌸 !rs : khởi động lại bot. 
        🌸 #share name : share code. 
        🌸 #sharemenu : menu share. 
        🌸 #tiengmenu : menu tiếng. 
        🌸 #voice tiếng text: gửi vocie. 
        🌸 #ura: gửi ảnh gì cx đếch biết
        🌸 #thinh: gửi thính với video,ảnh
        🌸 #srcc name: tiềm kiếm vd capcup 
        🌸 #dich tiếng nội dung: dịch từ cái
        🌸 #autodich on/off : auto dịch 
        🌸 #ifcc url  : info capcup 
        🌸 #sos : cấm tv chat
        🌸 #unlock  : mở chat 
        🌸 gif  : reply ảnh tạo gif
        🌸 taogif  : tạo gif tu reply ảnh
        🌸 #sr name  : tìm kiếm video tiktok cực múp
        🌸 .st reply ảnh tạo stk xoá nền
        🌸 #autodl on/off  : auto dl tiktok khi gửi link
        🌸 #qr nd  : tạo ảnh qr code 
        🌸 #catbot url  : tạo link ảnh  
        🌸 #link url  : tạo link rút gọn link4m
        🌸 #info  : xem info
        🌸 #sms sdt  : spam call & sms. 
        🌸 #dlfb  urrl  : tải video fb. 
        🌸 #stk  @tagname  : tạo stick từ avatar metion. 
        🌸 #nhac  : reply vào video 
        🌸 #scl url  : downloads nhạc 

. 

        """

        image_path = self.get_random_image_from_folder('anh')

        try:
            if image_path:
                self.sendLocalImage(
                    image_path, thread_id=thread_id, thread_type=thread_type, 
                    width=2560, height=2560, message=Message(text=menu_text), ttl=30000
                )
            else:
                self.replyMessage(
                    Message(text="💢 Không tìm thấy ảnh trong thư mục 'anh'."),
                    thread_id, thread_type, ttl=30000
                )
        except Exception as e:
            self.replyMessage(
                Message(text=f"🚦 Có lỗi xảy ra: {e}"),
                thread_id, thread_type, ttl=30000
            )
    def get_random_image_from_folder(self, folder_path='anh'):
        try:
            image_files = [file for file in os.listdir(folder_path) if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            return os.path.join(folder_path, random.choice(image_files)) if image_files else None
        except Exception as e:
            print(f"Error getting random image: {e}")
            return None
    def download_images(self, image_urls):
        images = []
        for url in image_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content)).convert("RGBA")
                    images.append(img)
            except:
                pass
        return images


    def handle_anhgai_command(self, thread_id, thread_type):
        file_path = "anhgai.txt"
        valid_extensions = (".jpg", ".jpeg", ".png")
        try:
            if not os.path.exists(file_path):
                self.sendMessage(Message(text="💢 File 'anhgai.txt' không tồn tại."), thread_id, thread_type)
                return
            with open(file_path, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file if line.strip().lower().endswith(valid_extensions)]

            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'anhgai.txt'."), thread_id, thread_type)
                return
            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)
            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"), thread_id, thread_type)
                return
            temp_image_path = "temp_anhgai_image.jpg"
            with open(temp_image_path, "wb") as temp_file:
                for chunk in response.iter_content(1024):
                    temp_file.write(chunk)
            self.sendLocalImage(temp_image_path, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            self.sendMessage(Message(text="🌸 Ảnh gái đã được gửi!"), thread_id, thread_type)
            os.remove(temp_image_path)
        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {e}"), thread_id, thread_type)

    def handle_gaicos_command(self, message_object, thread_id, thread_type):
        file_path = "cos.txt"
        valid_extensions = (".jpg", ".jpeg", ".png")
        try:
            if not os.path.exists(file_path):
                self.sendMessage(
                    Message(text="💢 File 'cos.txt' không tồn tại."),
                    thread_id, thread_type
                )
                return
            with open(file_path, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file if line.strip() and line.strip().lower().endswith(valid_extensions)]
            if not urls:
                self.sendMessage(
                    Message(text="🤧 Không tìm thấy URL hợp lệ trong 'cos.txt'."),
                    thread_id, thread_type
                )
                return
            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)
            if response.status_code != 200:
                self.sendMessage(
                    Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"),
                    thread_id, thread_type
                )
                return
            temp_image_path = "temp_cos_image.jpg"
            with open(temp_image_path, "wb") as temp_file:
                for chunk in response.iter_content(1024):
                    temp_file.write(chunk)
            self.sendLocalImage(temp_image_path, thread_id, thread_type)
            os.remove(temp_image_path)
            self.sendMessage(
                Message(text="🌸 Ảnh gái cosplay đã được gửi!"),
                thread_id, thread_type
            )
        except Exception as e:
            self.sendMessage(
                Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"),
                thread_id, thread_type
            )
    def handle_anhanime_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("anime.txt", "r", encoding="utf-8") if line.strip() and line.strip().lower().endswith(('.jpg', '.jpeg', '.png'))]
            if not urls: self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'anime.txt'."), thread_id, thread_type); return
            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)
            if response.status_code != 200: self.sendMessage(Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"), thread_id, thread_type); return
            with open("temp_anime_image.jpg", "wb") as temp_file: [temp_file.write(chunk) for chunk in response.iter_content(1024)]
            self.sendLocalImage("temp_anime_image.jpg", thread_id, thread_type); os.remove("temp_anime_image.jpg")
            self.sendMessage(Message(text="🌸 Ảnh anime đã được gửi!"), thread_id, thread_type)
        except Exception as e: self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_anhloli_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("loli.txt", "r", encoding="utf-8") if line.strip() and line.strip().lower().endswith(('.jpg', '.jpeg', '.png'))]
            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'loli.txt'."), thread_id, thread_type)
                return
            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)
            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"), thread_id, thread_type)
                return
            with open("temp_loli_image.jpg", "wb") as temp_file:
                for chunk in response.iter_content(1024):
                    temp_file.write(chunk)
            self.sendLocalImage("temp_loli_image.jpg", thread_id, thread_type)
            os.remove("temp_loli_image.jpg")
            self.sendMessage(Message(text="?? Ảnh loli đã được gửi!"), thread_id, thread_type)

        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_6mui_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("6mui.txt", "r", encoding="utf-8") if line.strip() and line.strip().lower().endswith(('.jpg', '.jpeg', '.png'))]
            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong '6mui.txt'."), thread_id, thread_type)
                return

            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)

            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"), thread_id, thread_type)
                return

            with open("temp_6mui_image.jpg", "wb") as temp_file:
                for chunk in response.iter_content(1024):
                    temp_file.write(chunk)

            self.sendLocalImage("temp_6mui_image.jpg", thread_id, thread_type)
            os.remove("temp_6mui_image.jpg")

            self.sendMessage(Message(text="🌸 Ảnh 6 múi đã được gửi!"), thread_id, thread_type)

        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_meme_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("meme.txt", "r", encoding="utf-8") if line.strip() and line.strip().lower().endswith(('.jpg', '.jpeg', '.png'))]
            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'mem.txt'."), thread_id, thread_type)
                return

            random_url = random.choice(urls)
            response = requests.get(random_url, stream=True)

            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải ảnh từ URL: {random_url}"), thread_id, thread_type)
                return

            with open("temp_meme_image.jpg", "wb") as temp_file:
                for chunk in response.iter_content(1024):
                    temp_file.write(chunk)

            self.sendLocalImage("temp_meme_image.jpg", thread_id, thread_type)
            os.remove("temp_meme_image.jpg")

            self.sendMessage(Message(text="🌸 Ảnh meme đã được gửi!"), thread_id, thread_type)

        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_vdgai_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("vdgai.txt", "r", encoding="utf-8") if line.strip()]
            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'vdgai.txt'."), thread_id, thread_type)
                return

            random_video_url = random.choice(urls)
            response = requests.get(random_video_url, stream=True)

            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải video từ URL: {random_video_url}"), thread_id, thread_type)
                return

            random_message = "🌸 Đây là video gái ngẫu nhiên!"
            thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'
            duration = 1000  

            message_to_send = Message(text=random_message)

            self.sendRemoteVideo(
                random_video_url,
                thumbnail_url,
                duration=duration,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )

        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_gaicos_command(self, message_object, thread_id, thread_type):
        try:
            urls = [line.strip() for line in open("gaicos.txt", "r", encoding="utf-8") if line.strip()]
            if not urls:
                self.sendMessage(Message(text="🤧 Không tìm thấy URL hợp lệ trong 'gaicos.txt'."), thread_id, thread_type)
                return

            random_video_url = random.choice(urls)
            response = requests.get(random_video_url, stream=True)

            if response.status_code != 200:
                self.sendMessage(Message(text=f"🤭 Không thể tải video từ URL: {random_video_url}"), thread_id, thread_type)
                return

            random_message = "🌸 Đây là video gái ngẫu nhiên!"
            thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'
            duration = 1000

            message_to_send = Message(text=random_message)

            self.sendRemoteVideo(
                random_video_url,
                thumbnail_url,
                duration=duration,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )

        except Exception as e:
            self.sendMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), thread_id, thread_type)
    def handle_vdchill_command(self, message_object, thread_id, thread_type):
        file_path = "chill.txt"
        try:
            if not os.path.exists(file_path):
                error_message = Message(text="❌ File 'chill.txt' không tồn tại.")
                self.sendMessage(error_message, thread_id, thread_type)
                return

            with open(file_path, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file.readlines() if line.strip()]

            if not urls:
                error_message = Message(text="❌ File 'chill.txt' không chứa URL nào.")
                self.sendMessage(error_message, thread_id, thread_type)
                return

            random_video_url = random.choice(urls)
            self.sendRemoteVideo(
                random_video_url,
                "https://files.catbox.moe/ksg81k.jpg", 
                duration=1000,
                message=Message(text="🎥 Video chill từ danh sách!"),
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )
        except Exception as e:
            error_message = Message(text=f"⚠️ Đã xảy ra lỗi khi gửi video: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_vdtet_command(self, message_object, thread_id, thread_type):
        url = "https://raw.githubusercontent.com/trannguyen-shiniuem/trannguyen-shiniuem/refs/heads/main/videotet.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
                random_video_url = random.choice(data)
                self.sendRemoteVideo(
                    random_video_url,
                    "https://files.catbox.moe/ksg81k.jpg",
                    duration=1000, 
                    message=Message(text="🎥 Video Tết từ danh sách!"),
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1080,
                    height=1920,
                    ttl=120000
                )
            else:
                error_message = Message(text="💢 Không tìm thấy URL video trong tệp JSON.")
                self.sendMessage(error_message, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"🥱 Đã xảy ra lỗi khi tải tệp JSON: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"🥱 Đã xảy ra lỗi khi gửi video: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_dltt_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ", 1)
        if len(parts) < 2:
            self.replyMessage(
                Message(text="🚦 Bạn chưa nhập URL video TikTok. Vui lòng nhập lại theo cú pháp: !dltt <URL> ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        video_url = parts[1]
        try:
            api_url = f'https://subhatde.id.vn/tiktok/downloadvideo?url={video_url}'
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data['code'] != 0:
                self.replyMessage(
                    Message(text="💢 Không tìm thấy video hoặc URL không hợp lệ. Vui lòng thử lại!"),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            video_data = data['data']
            video_title = video_data.get('title', 'Không có tiêu đề')
            video_play_url = video_data.get('play', '')
            video_cover = video_data.get('cover', '')
            if not video_play_url:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            send_title = f"📺Tiêu đề Video: {video_title}\n💖Số lượt thích: {video_data.get('digg_count', 0)}\n↪️Số lượt chia sẻ: {video_data.get('share_count', 0)}\n💬Số bình luận: {video_data.get('comment_count', 0)}\n📌Link Video: {video_url}"
            messagesend = Message(text=send_title)
            thumbnail_url = video_cover if video_cover else 'https://files.catbox.moe/34xdgb.jpeg'
            duration = video_data.get('duration', 60)
            self.sendRemoteVideo(
                video_play_url,
                thumbnail_url,
                duration=duration,
                message=messagesend,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600,
                ttl=30000
            )
        except Exception as e:
            self.replyMessage(
                Message(text="🚦 Có lỗi xảy ra trong quá trình tải video. Vui lòng thử lại!"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=300000
            )
    def handle_dltw_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")

        if len(parts) <= 1:  
            self.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp URL sau lệnh !dltw"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        api_url = f'https://subhatde.id.vn/tw/download?url={parts[1]}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if data.get("type") == "video":
                video_url = data['media'][0]
                title = data.get("title", "Video từ Twitter")
                message_to_send = Message(text=f"🎥 {title}")
                thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'
                duration = 1000

                self.sendRemoteVideo(
                    video_url,
                    thumbnail_url,
                    duration=duration,
                    message=message_to_send,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    #srp 3107
                    ttl=120000
                )
            else:
                self.replyMessage(
                    Message(text="💢 Không có video hoặc không thể tải video từ URL cung cấp."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )

        except requests.exceptions.RequestException as e:
            self.replyMessage(
                Message(text=f"🚦 Có lỗi xảy ra trong quá trình tải video: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
    def handle_dlcc_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")
        if len(parts) <= 1:
            self.replyMessage(Message(text="⚠️ Vui lòng cung cấp URL sau lệnh !dlcc"), message_object, thread_id, thread_type)
            return

        url = parts[1]
        api_url = f'https://subhatde.id.vn/capcut/download?url={url}'

        try:
            data = requests.get(api_url).json()
            video_url = data.get("video_url")
            if not video_url:
                self.replyMessage(Message(text="⚠️ Không thể tải video từ URL cung cấp."), message_object, thread_id, thread_type)
                return

            message_to_send = Message(
                text=f"🎥 {data.get('title', 'Video từ CapCut')}\n"
                     f"🔗 URL: {url}\n"
                     f"📝 Title: {data.get('short_title', '')}\n"
                     f"⏳ Duration: {data.get('duration', 0) // 1000}s\n"
                     f"👍 Likes: {data.get('like_count', 0)}\n"
                     f"💬 Comments: {data.get('comment_count', 0)}\n"
                     f"👤 Author: {data.get('author', {}).get('name', 'Unknown')}"
            )

            self.replyMessage(message_to_send, message_object, thread_id, thread_type)

            self.sendRemoteVideo(
                video_url, 'https://files.catbox.moe/ksg81k.jpg',
                duration=data.get('duration', 0) // 1000, message=message_to_send,
                thread_id=thread_id, thread_type=thread_type, width=1080, height=1920, ttl=120000
            )

        except requests.exceptions.RequestException:
            self.replyMessage(Message(text="🚦 Lỗi tải video."), message_object, thread_id, thread_type)


    def handle_dlyt_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")
        if len(parts) <= 1:
            self.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp tên tìm kiếm sau lệnh !dlyt"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        query = " ".join(parts[1:])
        api_url = f'https://subhatde.id.vn/youtube?q={query}'

        try:
            data = requests.get(api_url).json()

            if "results" not in data or len(data["results"]) == 0:
                self.replyMessage(
                    Message(text="⚠️ Không tìm thấy kết quả cho từ khóa bạn nhập."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=300000
                )
                return

            video_info = data["results"][0]["video"]
            title = video_info.get("title", "Không có tiêu đề")
            url = video_info.get("url", "")
            duration = video_info.get("duration", "Không có thông tin")
            views = video_info.get("views", "Không có thông tin")
            thumbnail_src = video_info.get("thumbnail_src", "")
            upload_date = video_info.get("upload_date", "Không có thông tin")
            uploader_name = data["results"][0]["uploader"].get("username", "Không có thông tin")
            uploader_url = data["results"][0]["uploader"].get("url", "")

            message_to_send = Message(text=f"🎥 **{title}**\n"
                                          f"🔗 URL: {url}\n"
                                          f"⏳ Duration: {duration}\n"
                                          f"👀 Views: {views}\n"
                                          f"📅 Uploaded: {upload_date}\n"
                                          f"👤 Uploader: {uploader_name} ({uploader_url})")

            self.replyMessage(
                message_to_send,
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=300000
            )

            if thumbnail_src:
                img_data = requests.get(thumbnail_src).content
                with open("thumbnail.jpg", "wb") as handler:
                    handler.write(img_data)

                self.sendLocalImage("thumbnail.jpg", thread_id=thread_id, thread_type=thread_type, ttl=30000)

            video_url = video_info.get("url", "")
            thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'

            self.sendRemoteVideo(
                video_url,
                thumbnail_url,
                duration=100,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )

        except requests.exceptions.RequestException as e:
            self.replyMessage(
                Message(text=f"🚦 Có lỗi xảy ra khi tìm kiếm video: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=300000
            )
    def handle_canva_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ", 1)
        if len(parts) < 2:
            self.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp nội dung cần vẽ lên ảnh!"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        text_to_draw = parts[1]

        canva_folder = 'canva'
        image_files = [f for f in os.listdir(canva_folder) if f.endswith(('png', 'jpg', 'jpeg', 'bmp'))]
        if not image_files:
            self.replyMessage(
                Message(text="⚠️ Không tìm thấy ảnh trong thư mục 'canva'."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        selected_image = random.choice(image_files)
        image_path = os.path.join(canva_folder, selected_image)

        font_folder = 'font'
        font_files = [f for f in os.listdir(font_folder) if f.endswith('.ttf')]
        if not font_files:
            self.replyMessage(
                Message(text="⚠️ Không tìm thấy font trong thư mục 'font'."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        selected_font = random.choice(font_files)
        font_path = os.path.join(font_folder, selected_font)

        try:
            image = Image.open(image_path)
            draw = ImageDraw.Draw(image)

            font = ImageFont.truetype(font_path, 500)
            bbox = draw.textbbox((0, 0), text_to_draw, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            width, height = image.size
            position = ((width - text_width) // 2, (height - text_height) // 2)

            random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            draw.text(position, text_to_draw, font=font, fill=random_color)

            img_filename = "output_image.png"
            image.save(img_filename)

            self.sendLocalImage(img_filename, thread_id=thread_id, thread_type=thread_type, ttl=30000)

            os.remove(img_filename)

        except Exception as e:
            self.replyMessage(
                Message(text=f"⚠️ Đã xảy ra lỗi khi xử lý ảnh: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
    def handle_thuphap_command(self, message, message_object, thread_id, thread_type, author_id):
        content = message.strip().split()

        if len(content) < 4:
            error_message = Message(text="💬 Vui lòng nhập 3 tên để vẽ thư pháp (sử dụng lệnh #thuphap name).")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        name_1 = content[1]
        name_2 = content[2]
        name_3 = content[3]

        api_url = f"https://api.ntmdz.online/thuphap?id=1&sodong=3&dong_1={name_1}&dong_2={name_2}&dong_3={name_3}"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                image_path = 'thuphap_image.jpeg'
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                success_message = f"💬 Thư pháp với các tên: {name_1}, {name_2}, {name_3} đã được vẽ thành công!"
                message_to_send = Message(text=success_message)
                self.sendLocalImage(
                    image_path, 
                    message=message_to_send,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )

                os.remove(image_path)

            else:
                error_message = Message(text="❌ Đã xảy ra lỗi khi vẽ thư pháp. Vui lòng thử lại.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌ Đã xảy ra lỗi khi gọi API: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"❌ Đã xảy ra lỗi: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_ttsr_command(self, message, message_object, thread_id, thread_type):
      parts = message.split(" ")

      if len(parts) <= 1:  
          self.replyMessage(
              Message(text="⚠️ Vui lòng cung cấp tên tìm kiếm sau lệnh !ttsr"),
              message_object,
              thread_id=thread_id,
              thread_type=thread_type,
              ttl=30000
          )
          return

      search_name = parts[1]
      api_url = f'https://subhatde.id.vn/tiktok/searchvideo?keywords={search_name}'

      try:
          response = requests.get(api_url)
          response.raise_for_status()
          data = response.json()

          if data["code"] == 0:

              if data['data']['videos']:
                  video = data['data']['videos'][0]
                  video_url = video['play']
                  video_cover = video['cover']
                  title = video['title']
                  music_url = video['music_info']['play']
                  thumbnail_url = video['music_info']['cover']

                  message_to_send = Message(text=f"🎥 Video tìm kiếm: {title}")


                  thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'
                  temp_image_path = self.download_image(video_cover)
                  self.sendLocalImage(temp_image_path, thread_id, thread_type)

                  self.sendRemoteVideo(
                      video_url,
                      thumbnail_url,
                      duration=100,
                      message=message_to_send,
                      thread_id=thread_id,
                      thread_type=thread_type,
                      width=1080,
                      height=1920,
                      ttl=120000
                  )

                  if os.path.exists(temp_image_path):
                      os.remove(temp_image_path)
              else:
                  self.replyMessage(
                      Message(text="💢 Không tìm thấy video phù hợp với từ khóa."),
                      message_object,
                      thread_id=thread_id,
                      thread_type=thread_type,
                      ttl=30000
                  )

          else:
              self.replyMessage(
                  Message(text="💢 Không tìm thấy video phù hợp với từ khóa."),
                  message_object,
                  thread_id=thread_id,
                  thread_type=thread_type,
                  ttl=30000
              )

      except requests.exceptions.RequestException as e:
          self.replyMessage(
              Message(text=f"🚦 Có lỗi xảy ra trong quá trình tìm kiếm video: {str(e)}"),
              message_object,
              thread_id=thread_id,
              thread_type=thread_type,
              ttl=30000
          )


    def download_image(self, image_url):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            temp_image_path = "temp_image.jpg"
            with open(temp_image_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            return temp_image_path
        except requests.exceptions.RequestException as e:
            return None
    def handle_dlyt2_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")

        if len(parts) <= 1:  
            self.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp URL YouTube sau lệnh !dlyt"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        video_url = parts[1]
        api_url = f'https://subhatde.id.vn/youtube/download?url={video_url}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            video_id = data.get('id')
            video_title = data.get('title', 'Không có tiêu đề')
            video_duration = data.get('duration', '00:00:00')
            video_url = data.get('url', '')

            if not video_url:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            message_to_send = Message(text=f"🎥 Tiêu đề: {video_title}\n⏱️ Thời gian: {video_duration}")
            self.sendRemoteVideo(
                video_url,
                "https://files.catbox.moe/ksg81k.jpg",  
                duration=1000,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )
        except requests.exceptions.RequestException as e:
            self.replyMessage(
                Message(text=f"🚦 Có lỗi xảy ra trong quá trình tải video: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
    def handle_srp_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")

        if len(parts) <= 1:  
            self.replyMessage(
                Message(text="⚠️ Vui lòng cung cấp tên bài hát sau lệnh #srp"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        song_name = parts[1]
        api_url = f'https://subhatde.id.vn/spotify?q={song_name}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list) and data:
                data = data[0]
            else:
                self.replyMessage(
                    Message(text="💢 Không tìm thấy bài hát hoặc URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            thumbnail_url = data.get('thumbnail', '')
            song_title = data.get('title', 'Không có tiêu đề')
            update_date = data.get('update', 'Không có ngày cập nhật')
            duration = data.get('duration', '00:00')
            popularity = data.get('popularity', 'Chưa có thông tin')
            preview_url = data.get('preview', '')
            spotify_url = data.get('url', '')

            if not preview_url:
                self.replyMessage(
                    Message(text="💢 Không thể tìm thấy bài hát hoặc URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            message_to_send = Message(
                text=f"🎶 Bài hát: {song_title}\n📅 Cập nhật: {update_date}\n⏳ Thời gian: {duration}\n🔥 Độ phổ biến: {popularity}\n🎧 Nghe trước: {preview_url}\n🔗 Link Spotify: {spotify_url}"
            )

            thumbnail_url = 'https://files.catbox.moe/ksg81k.jpg'
            self.sendRemoteVideo(
                preview_url,
                thumbnail_url,
                duration=100,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080, height=1920, ttl=120000
            )
        except requests.exceptions.RequestException as e:
            self.replyMessage(
                Message(text=f"🚦 Có lỗi xảy ra trong quá trình tìm kiếm bài hát: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
    def handle_uptime_command(self, message, message_object, thread_id, thread_type):
        try:
            current_time = datetime.now()
            uptime_seconds = time.time() - self.start_time
            uptime = str(timedelta(seconds=int(uptime_seconds)))

            uptime_str = f"Bot đã hoạt động được {uptime}"

            color_rgb = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            upt_dir = "upt"
            images = [img for img in os.listdir(upt_dir) if img.endswith(".jpg")]
            if not images:
                self.replyMessage(
                    Message(text="❌ Không tìm thấy ảnh trong thư mục upt."),
                    message_object, thread_id, thread_type
                )
                return
            image_path = os.path.join(upt_dir, random.choice(images))
            img = Image.open(image_path)
            draw = ImageDraw.Draw(img)

            font_dir = "font"
            fonts = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]
            if not fonts:
                self.replyMessage(
                    Message(text="❌ Không tìm thấy font trong thư mục font."),
                    message_object, thread_id, thread_type
                )
                return
            font_path = os.path.join(font_dir, random.choice(fonts))
            font = ImageFont.truetype(font_path, 60)

            bbox = draw.textbbox((0, 0), uptime_str, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_position = ((img.width - text_width) // 2, (img.height - text_height) // 2)

            draw.text(text_position, uptime_str, font=font, fill=color_rgb)

            output_path = os.path.join(upt_dir, f"uptime_{int(time.time())}.jpg")
            img.save(output_path)

            self.sendLocalImage(
                output_path, 
                message=Message(text="🌟 Uptime đã được hiển thị!"), 
                thread_id=thread_id, thread_type=thread_type, width=800, height=180, ttl=30000
            )

            os.remove(output_path)

        except Exception as e:
            self.replyMessage(
                Message(text=f"⚠️ Đã xảy ra lỗi: {str(e)}"), 
                message_object, thread_id, thread_type
            )

    def handle_todo_command(self, message, message_object, thread_id, thread_type, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return
        try:
            with open("todo.json", "r") as f:
                todo_data = json.load(f)
            group_id = str(thread_id)
            if group_id not in todo_data:
                return self.replyMessage(Message(text="🚦 Nhóm này chưa được duyệt todo!"), message_object, thread_id, thread_type)
        except FileNotFoundError:
            return self.replyMessage(Message(text="🚦 File todo.json không tìm thấy!"), message_object, thread_id, thread_type)

        parts = message.split(" ")
        if len(parts) < 3 or not parts[1].isdigit():
            return self.replyMessage(Message(text="💢 Vui lòng nhập đúng lệnh: #todo số_lần [nội dung]"), message_object, thread_id, thread_type)

        spam_count = int(parts[1])
        content = " ".join(parts[2:])

        try:
            data = self.fetchGroupInfo(groupId=str(thread_id))
            members = data['gridInfoMap'][str(thread_id)]['memVerList']
            member_ids = [mem.split('_')[0] for mem in members]

            for user_id in member_ids:
                user_name = self.fetchUserInfo(user_id).changed_profiles[user_id].displayName
                for _ in range(spam_count):
                    self.sendToDo(message_object, content, [user_id], thread_id, thread_type, -1, "Nhiệm vụ được giao tự động qua bot.")
                self.replyMessage(Message(text=f"🌸 Đã giao {spam_count} nhiệm vụ với nội dung '{content}' cho {user_name}."), message_object, thread_id, thread_type, ttl=1000)
        except Exception as e:
            self.replyMessage(Message(text=f"🤧 Lỗi khi gửi nhiệm vụ cho người dùng: {e}"), message_object, thread_id, thread_type)

    def handle_add_command(self, message_object, thread_id, thread_type, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return
        group_id = thread_id
        data = self.fetchGroupInfo(groupId=group_id)
        members = data['gridInfoMap'][str(group_id)]['memVerList']
        member_ids = {}
        for mem in members:
            user_id = mem.split('_')[0]
            user_name = mem.split('_')[1]
            member_ids[user_id] = user_name

        try:
            with open("todo.json", "r") as f:
                todo_data = json.load(f)
        except FileNotFoundError:
            todo_data = {}

        todo_data[group_id] = member_ids
        with open("todo.json", "w") as f:
            json.dump(todo_data, f)

        self.replyMessage(Message(text="🌸 Đã thêm ID nhóm vào todo.json!"), message_object, thread_id, thread_type)

    def handle_revo_command(self, message_object, thread_id, thread_type, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return
        group_id = thread_id
        try:
            with open("todo.json", "r") as f:
                todo_data = json.load(f)
            if group_id in todo_data:
                del todo_data[group_id]
                with open("todo.json", "w") as f:
                    json.dump(todo_data, f)
                self.replyMessage(Message(text="🌸 Đã xóa ID nhóm khỏi todo.json!"), message_object, thread_id, thread_type)
            else:
                self.replyMessage(Message(text="🚦 Nhóm này không tồn tại trong todo.json!"), message_object, thread_id, thread_type)
        except FileNotFoundError:
            self.replyMessage(Message(text="🚦 File todo.json không tìm thấy!"), message_object, thread_id, thread_type)

    def handle_infov2_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")  

        if len(content) < 4:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: name, id và subname.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return


        name = content[1].strip(' ]')
        fb_id = content[2].strip(' ]')
        subname = content[3].strip(' ]')

        api_url = f"https://api.ntmdz.online/fbcover/v2?name={name}&id={fb_id}&subname={subname}"
        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return
            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), f"{name}_{fb_id}_{subname}_fbcover.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                image_width, image_height = 3300, 1180  

                message_to_send = Message(text=f"🌸 Ảnh info đã được gửi! Thông tin của '{name}' với ID '{fb_id}' và Subname '{subname}' đã được tải lên.")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=image_width, height=image_height, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌ API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌ Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️ Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_infov3_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")  


        if len(content) < 8:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: name, birthday, love, location, hometown, follow, gender và uid.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return


        name = content[1].strip(' ]')
        birthday = content[2].strip(' ]')
        love = content[3].strip(' ]')
        location = content[4].strip(' ]')
        hometown = content[5].strip(' ]')
        follow = content[6].strip(' ]')
        gender = content[7].strip(' ]')
        uid = content[8].strip(' ]')

        api_url = f"https://api.ntmdz.online/fbcover/v3?name={name}&birthday={birthday}&love={love}&location={location}&hometown={hometown}&follow={follow}&gender={gender}&uid={uid}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return
            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), f"{name}_fbcover_v3.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                image_width, image_height = 3300, 1180  

                message_to_send = Message(text=f"🌸 Ảnh info đã được gửi! Thông tin của '{name}' đã được tải lên.")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=image_width, height=image_height, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌ API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌ Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️ Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_infov1_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")  

        if len(content) < 8:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: name, uid, address, email, subname, sdt, và color.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return


        name = content[1].strip(' ]')
        uid = content[2].strip(' ]')
        address = content[3].strip(' ]')
        email = content[4].strip(' ]')
        subname = content[5].strip(' ]')
        sdt = content[6].strip(' ]')
        color = content[7].strip(' ]')

        api_url = f"https://subhatde.id.vn/fbcover/v1?name={name}&uid={uid}&address={address}&email={email}&subname={subname}&sdt={sdt}&color={color}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return
            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), f"{name}_fbcover_v1.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text=f"🌸🥱 Thông tin của '{name}' đã được tải lên thành công! 💢😺")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type,width=3300,height=1180,ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_blink_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")  

        if len(content) < 3:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: id và delay.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return


        ids = content[1].strip(' ]')
        delay = content[2].strip(' ]')
        api_url = f"https://subhatde.id.vn/blink?id={ids}&delay={delay}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), "blink_image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text=f"🌸🥱 Ảnh blink đã được tải lên thành công! 💢😺")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type,width=3300,height=1180, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_wibu_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")
        if len(content) < 4:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: id, chu_nen, chu_ky.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        ids = content[1].strip(' ]')
        chu_nen = content[2].strip(' ]')
        chu_ky = content[3].strip(' ]')

        api_url = f"https://subhatde.id.vn/canvas/avatarwibu?id={ids}&chu_nen={chu_nen}&chu_ky={chu_ky}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), "wibu_image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text="🌸🥱 Ảnh Wibu đã được tạo thành công! 💢😺")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_danhthiep_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")
        if len(content) < 3:
            error_message = Message(text="❌ Vui lòng nhập đủ các thông tin: text1 và text2.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        text1 = content[1].strip(' ]')
        text2 = content[2].strip(' ]')

        api_url = f"https://subhatde.id.vn/shopmaihuong?text1={text1}&text2={text2}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), "danhthiep_image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text="🌸🥱 Ảnh danh thiếp đã được tạo thành công! 💢😺")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_giangsinh_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")
        if len(content) < 2:
            error_message = Message(text="❌ Vui lòng nhập text để tạo ảnh Giáng Sinh.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        text = content[1].strip(' ]')

        api_url = f"https://subhatde.id.vn/giangsinh?text={text}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), "giangsinh_image.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text="🌸🥱 Ảnh Giáng Sinh đã được tạo thành công! 💢😺")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_fk_command(self, message, message_object, thread_id, thread_type):
      content = message.strip().split(" [")
      if len(content) < 6:
          error_message = Message(text="🌸❌😍 Vui lòng nhập đầy đủ text1, text2, text3, text4 và urlimg.")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
          return

      text1 = content[1].strip(' ]')
      text2 = content[2].strip(' ]')
      text3 = content[3].strip(' ]')
      text4 = content[4].strip(' ]')
      urlimg = content[5].strip(' ]')

      api_url = f"https://subhatde.id.vn/cccd?text1={text1}&text2={text2}&text3={text3}&text4={text4}&urlimg={urlimg}"

      try:
          response = requests.get(api_url)
          if response.status_code != 200:
              error_message = Message(text=f"🌸❌🚦 API trả về lỗi: {response.status_code}")
              self.replyMessage(error_message, message_object, thread_id, thread_type)
              return

          if response.headers['Content-Type'].startswith('image'):
              image_path = os.path.join(os.getcwd(), "fk_image.jpg")
              with open(image_path, 'wb') as f:
                  f.write(response.content)

              message_to_send = Message(
                  text=(
                      f"🌸😍 Ảnh đã được tạo thành công!\n"
                      f"🚦 Chi tiết ảnh:\n"
                      f"👉 Text1: {text1}\n"
                      f"👉 Text2: {text2}\n"
                      f"👉 Text3: {text3}\n"
                      f"👉 Text4: {text4}\n"
                      f"👉 URL ảnh: {urlimg}"
                  )
              )
              self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

              os.remove(image_path)
          else:
              error_message = Message(text="🌸❌🤫 API không trả về ảnh hợp lệ.")
              self.replyMessage(error_message, message_object, thread_id, thread_type)

      except requests.exceptions.RequestException as e:
          error_message = Message(text=f"🌸❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
      except Exception as e:
          error_message = Message(text=f"🌸⚠️🚦 Đã xảy ra lỗi không xác định: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_anhbia_command(self, message, message_object, thread_id, thread_type):
      content = message.strip().split(" [")
      if len(content) < 3:
          error_message = Message(text="🌸❌😍 Vui lòng nhập đầy đủ tên và tuổi.")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
          return

      name = content[1].strip(' ]')
      age = content[2].strip(' ]')

      api_url = f"https://subhatde.id.vn/anhbia?name={name}&age={age}"

      try:
          response = requests.get(api_url)
          if response.status_code != 200:
              error_message = Message(text=f"🌸❌🚦 API trả về lỗi: {response.status_code}")
              self.replyMessage(error_message, message_object, thread_id, thread_type)
              return

          if response.headers['Content-Type'].startswith('image'):
              image_path = os.path.join(os.getcwd(), f"{name}_anhbia.jpg")
              with open(image_path, 'wb') as f:
                  f.write(response.content)

              message_to_send = Message(
                  text=(
                      f"🌸🚦😍 Ảnh bìa của '{name}' đã được tạo thành công!\n"
                      f"🌸 Thông tin chi tiết:\n"
                      f"👉 Tên: {name}\n"
                      f"👉 Tuổi: {age}"
                  )
              )
              self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

              os.remove(image_path)
          else:
              error_message = Message(text="🌸❌🤫 API không trả về ảnh hợp lệ.")
              self.replyMessage(error_message, message_object, thread_id, thread_type)

      except requests.exceptions.RequestException as e:
          error_message = Message(text=f"🌸❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
      except Exception as e:
          error_message = Message(text=f"🌸⚠️🚦 Đã xảy ra lỗi không xác định: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)


    def handle_bnc1_command(self, message, message_object, thread_id, thread_type):
      content = message.strip().split(" [")
      if len(content) < 4:
          error_message = Message(text="🌸❌😍 Vui lòng nhập đầy đủ các tham số: kieu, age, name.")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
          return

      kieu = content[1].strip(' ]')
      age = content[2].strip(' ]')
      name = content[3].strip(' ]')

      api_url = f"https://subhatde.id.vn/bannertc?kieu={kieu}&age={age}&name={name}"

      try:
          response = requests.get(api_url)
          if response.status_code != 200:
              error_message = Message(text=f"🌸❌🚦 API trả về lỗi: {response.status_code}")
              self.replyMessage(error_message, message_object, thread_id, thread_type)
              return

          if response.headers['Content-Type'].startswith('image'):
              image_path = os.path.join(os.getcwd(), f"{name}_banner.jpg")
              with open(image_path, 'wb') as f:
                  f.write(response.content)

              message_to_send = Message(
                  text=(
                      f"🌸🚦😍 Banner của '{name}' đã được tạo thành công!\n"
                      f"🌸 Thông tin chi tiết:\n"
                      f"👉 Kiểu: {kieu}\n"
                      f"👉 Tuổi: {age}\n"
                      f"👉 Tên: {name}"
                  )
              )
              self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

              os.remove(image_path)
          else:
              error_message = Message(text="🌸❌🚦 API không trả về ảnh hợp lệ.")
              self.replyMessage(error_message, message_object, thread_id, thread_type)

      except requests.exceptions.RequestException as e:
          error_message = Message(text=f"🌸❌😍 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
      except Exception as e:
          error_message = Message(text=f"🌸⚠️🚦 Đã xảy ra lỗi không xác định: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_bnc2_command(self, message, message_object, thread_id, thread_type):
      content = message.strip().split(" [")
      if len(content) < 4:
          error_message = Message(text="🌸❌😍 Vui lòng nhập đầy đủ các tham số: age, name, text.")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
          return

      age = content[1].strip(' ]')
      name = content[2].strip(' ]')
      text = content[3].strip(' ]')

      api_url = f"https://subhatde.id.vn/bannertc2?age={age}&name={name}&text={text}"

      try:
          response = requests.get(api_url)
          if response.status_code != 200:
              error_message = Message(text=f"🌸❌😍 API trả về lỗi: {response.status_code}")
              self.replyMessage(error_message, message_object, thread_id, thread_type)
              return

          if response.headers['Content-Type'].startswith('image'):
              image_path = os.path.join(os.getcwd(), f"{name}_banner.jpg")
              with open(image_path, 'wb') as f:
                  f.write(response.content)

              message_to_send = Message(
                  text=(
                      f"🌸🚦😍 Banner của '{name}' với text '{text}' đã được tạo thành công!\n"
                      f"🌸 Thông tin chi tiết:\n"
                      f"👉 Tuổi: {age}\n"
                      f"👉 Tên: {name}\n"
                      f"👉 Nội dung: {text}"
                  )
              )
              self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

              os.remove(image_path)
          else:
              error_message = Message(text="🌸❌🚦 API không trả về ảnh hợp lệ.")
              self.replyMessage(error_message, message_object, thread_id, thread_type)

      except requests.exceptions.RequestException as e:
          error_message = Message(text=f"🌸❌😍 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
      except Exception as e:
          error_message = Message(text=f"🌸⚠️🚦 Đã xảy ra lỗi không xác định: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_cardif_command(self, message, message_object, thread_id, thread_type):
        content = message.strip().split(" [")
        if len(content) < 7:
            error_message = Message(text="❌ Vui lòng nhập đầy đủ các tham số: location, name, gender, vanity, uid, chuky.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        location = content[1].strip(' ]')
        name = content[2].strip(' ]')
        gender = content[3].strip(' ]')
        vanity = content[4].strip(' ]')
        uid = content[5].strip(' ]')
        chuky = content[6].strip(' ]')

        api_url = f"https://subhatde.id.vn/cardinfo?location={location}&name={name}&gender={gender}&vanity={vanity}&uid={uid}&chuky={chuky}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"🌸❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), f"{name}_cardinfo.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(
                    text=(
                        f"🌸🥱 Thẻ thông tin của '{name}' đã được tạo thành công!\n"
                        f"🌸 Thông tin chi tiết:\n"
                        f"😍 Vị trí: {location}\n"
                        f"🌸 Tên: {name}\n"
                        f"😍 Giới tính: {gender}\n"
                        f"🌸 Vanity: {vanity}\n"
                        f"😍 UID: {uid}\n"
                        f"🌸 Chữ ký: {chuky}"
                    )
                )
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

                os.remove(image_path)
            else:
                error_message = Message(text="❌🤫 API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌😒 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️🥱 Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_sophan_command(self, message, message_object, thread_id, thread_type, author_id):
        content = message.strip().split()
        if len(content) < 2:
            error_message = Message(text="❌ Vui lòng nhập tên để tra cứu số phận.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        name = " ".join(content[1:]).strip()
        api_url = f"https://subhatde.id.vn/ggsaid?name={name}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text=f"❌ API trả về lỗi: {response.status_code}")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            if response.headers['Content-Type'].startswith('image'):
                image_path = os.path.join(os.getcwd(), f"sophan_{name}.jpg")
                with open(image_path, 'wb') as f:
                    f.write(response.content)

                message_to_send = Message(text=f"💬 Đã tải ảnh số phận của '{name}'")
                self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type,width=3300, height=1180, ttl=30000)
                os.remove(image_path)
            else:
                error_message = Message(text="❌ API không trả về ảnh hợp lệ.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌ Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"⚠️ Đã xảy ra lỗi không xác định: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
    def handle_mrk_command(self, message, message_object, thread_id, thread_type):
      content = message.strip().split(" [")
      if len(content) < 8:
          error_message = Message(text="🌸❌😍 Vui lòng nhập đầy đủ các tham số: text1, text2, fb, ma, tl, lc, uid.")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
          return

      text1 = content[1].strip(' ]')
      text2 = content[2].strip(' ]')
      fb = content[3].strip(' ]')
      ma = content[4].strip(' ]')
      tl = content[5].strip(' ]')
      lc = content[6].strip(' ]')
      uid = content[7].strip(' ]')

      api_url = f"https://subhatde.id.vn/mkt?text1={text1}&text2={text2}&fb={fb}&ma={ma}&tl={tl}&lc={lc}&uid={uid}"

      try:
          response = requests.get(api_url)
          if response.status_code != 200:
              error_message = Message(text=f"🌸❌😍 API trả về lỗi: {response.status_code}")
              self.replyMessage(error_message, message_object, thread_id, thread_type)
              return

          if response.headers['Content-Type'].startswith('image'):
              image_path = os.path.join(os.getcwd(), f"{text1}_mrk.jpg")
              with open(image_path, 'wb') as f:
                  f.write(response.content)

              message_to_send = Message(
                  text=(
                      f"🌸🚦😍 Thẻ thông tin MRK của '{text1}' đã được tạo thành công!\n"
                      f"🌸 Thông tin chi tiết:\n"
                      f"👉 Text1: {text1}\n"
                      f"👉 Text2: {text2}\n"
                      f"👉 FB: {fb}\n"
                      f"👉 Mã: {ma}\n"
                      f"👉 TL: {tl}\n"
                      f"👉 Location: {lc}\n"
                      f"👉 UID: {uid}"
                  )
              )
              self.sendLocalImage(image_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=3300, height=1180, ttl=30000)

              os.remove(image_path)
          else:
              error_message = Message(text="🌸❌😍 API không trả về ảnh hợp lệ.")
              self.replyMessage(error_message, message_object, thread_id, thread_type)

      except requests.exceptions.RequestException as e:
          error_message = Message(text=f"🌸❌😍 Lỗi khi gọi API hoặc tải ảnh: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)
      except Exception as e:
          error_message = Message(text=f"🌸❌😍 Đã xảy ra lỗi không xác định: {str(e)}")
          self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_restart(self, message, message_object, thread_id, thread_type, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=300000
            )
            return

        self.replyMessage(
            Message(text="🔄 Bot đang khởi động lại..."),
            message_object,
            thread_id=thread_id,
            thread_type=thread_type,
            ttl=300000
        )

        self.restart_program()

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
    def handle_share_command(self, message, message_object, thread_id, thread_type):
        contents = {

            'voice': "https://link4m.com/kluGAKL",
            'icon': "https://link4m.com/RX77LOvD",
            'vdtet': "https://link4m.com/rzytC",
            'rename': "https://link4m.com/SrqbpS",

        }

        content_parts = message.strip().split(" ", 1)
        if len(content_parts) < 2:
            error_message = Message(text="💢 Vui lòng nhập tên nội dung cần chia sẻ sau lệnh #share.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        name = content_parts[1].strip()
        share_url = contents.get(name)

        if not share_url:
            error_message = Message(text=f"💢 Không tìm thấy nội dung share có tên '{name}'.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        author_name = "X"  

        share_message = Message(
            text=(
                f"🌸 Đây là nội dung share:\n"
                f"🚦 Tác giả: {author_name}\n"
                f"📅 Thời gian share: {current_time}\n"
                f"🤧 Nội dung share: {share_url}\n"
                f"🤭 Cảm ơn bạn đã sử dụng bot!"
            )
        )

        self.replyMessage(share_message, message_object, thread_id, thread_type,ttl=30000)

    def handle_sharemenu_command(self, message_object, thread_id, thread_type):
        menu_message = Message(
            text=(
                "🎉 Chào mừng đến với menu Share code 💌\n"
                "🚦 Tổng hợp code được share:\n"
                "       ➜ voice\n"
                "        ➜ icon\n"
                "        ➜ vdtet\n"
                "        ➜ rename\n"
                "🚦 Ví dụ: #share ask ✅\n"
                "🤖 Sẵn sàng phục 🌸"
            )
        )
        self.replyMessage(menu_message, message_object, thread_id, thread_type,ttl=30000)
    def convert_text_to_mp3(self, text, lang='vi'):
        try:
            tts = gTTS(text=text, lang=lang)
            mp3_file = 'temp.mp3'
            tts.save(mp3_file)
            return mp3_file
        except Exception as e:
            print(f"Lỗi {str(e)}")
            return None

    def upload_to_host(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                files = {'files[]': file}
                response = requests.post('https://uguu.se/upload', files=files).json()
                if response['success']:
                    return response['files'][0]['url']
                return False
        except Exception as e:
            print(f"Error in upload_to_host: {e}")
            return False

    def handle_voice_command(self, message, message_object, thread_id, thread_type):
        try:
            text = message[7:].strip()  
            if not text:
                error_message = Message(text="💢 Bạn chưa nhập nội dung để chuyển thành giọng nói!")
                self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
                return

            lang = 'vi'  
            if text.lower().startswith('en '):
                lang = 'en'
                text = text[3:].strip()
            elif text.lower().startswith('es '):
                lang = 'es'
                text = text[3:].strip()
            elif text.lower().startswith('fr '):
                lang = 'fr'
                text = text[3:].strip()
            elif text.lower().startswith('de '):
                lang = 'de'
                text = text[3:].strip()
            elif text.lower().startswith('it '):
                lang = 'it'
                text = text[3:].strip()
            elif text.lower().startswith('ko '):
                lang = 'ko'
                text = text[3:].strip()
            elif text.lower().startswith('ja '):
                lang = 'ja'
                text = text[3:].strip()
            elif text.lower().startswith('zh '):
                lang = 'zh'
                text = text[3:].strip()

            mp3_file = self.convert_text_to_mp3(text, lang)
            if not mp3_file:
                error_message = Message(text="💢 Đã xảy ra lỗi khi chuyển đổi văn bản thành giọng nói.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            voice_url = self.upload_to_host(mp3_file)
            if not voice_url:
                error_message = Message(text="💢 Đã xảy ra lỗi khi tải file âm thanh lên.")
                self.replyMessage(error_message, message_object, thread_id, thread_type)
                return

            file_size = os.path.getsize(mp3_file)
            self.sendRemoteVoice(voice_url, thread_id, thread_type, fileSize=file_size)

            os.remove(mp3_file)

            success_message = Message(text="🌸 Đã gửi âm thanh chuyển ngữ thành công!")
            self.replyMessage(success_message, message_object, thread_id, thread_type, ttl=30000)

        except Exception as e:
            error_message = Message(text=f"💢 Đã xảy ra lỗi: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type)

    def handle_languages_command(self, message_object, thread_id, thread_type):
        languages_message = Message(text="🌍 Các ngôn ngữ hỗ trợ:\n- Vi: Tiếng Việt\n- En: Tiếng Anh\n- Es: Tiếng Tây Ban Nha\n- Fr: Tiếng Pháp\n- De: Tiếng Đức\n- It: Tiếng Ý\n- Ko: Tiếng Hàn Quốc\n- Ja: Tiếng Nhật\n- Zh: Tiếng Trung Quốc")
        self.replyMessage(languages_message, message_object, thread_id, thread_type, ttl=30000)
    def handle_ura_command(self, message, message_object, thread_id, thread_type):
        file_path = "ura.txt"
        valid_extensions = (".jpg", ".jpeg", ".png")

        if not os.path.exists(file_path):
            error_message = Message(text="🚦 File 'ura.txt' không tồn tại.")
            self.sendMessage(error_message, thread_id, thread_type)
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                urls = [line.strip() for line in file.readlines() if line.strip() and line.strip().lower().endswith(valid_extensions)]

            if not urls:
                error_message = Message(text="🚦 File 'ura.txt' không chứa URL hợp lệ.")
                self.sendMessage(error_message, thread_id, thread_type)
                return

            random_url = random.choice(urls)

            response = requests.get(random_url, stream=True)
            if response.status_code != 200:
                error_message = Message(text=f"🚦 Không thể tải ảnh từ URL: {random_url}")
                self.sendMessage(error_message, thread_id, thread_type)
                return

            temp_image_path = "temp_ura_image.jpg"
            with open(temp_image_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            self.sendLocalImage(temp_image_path, thread_id=thread_id, thread_type=thread_type, ttl=30000)

            self.replyMessage(
                Message(text="🌸🤭 Đây là ảnh bạn yêu cầu!"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )

            os.remove(temp_image_path)

        except Exception as e:
            error_message = Message(text=f"🚦 Có lỗi xảy ra trong quá trình tải và gửi ảnh. Lỗi: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
    def handle_thinh_command(self, message_object, thread_id, thread_type):
        thinh_file_path = "thinh.json"
        url_file_path = "anhgai.txt"
        video_file_path = "vdgai.txt"

        if not os.path.exists(thinh_file_path) or not os.path.exists(url_file_path):
            self.replyMessage(Message(text="🚦 Tệp dữ liệu không tồn tại."), message_object, thread_id, thread_type)
            return

        try:

            with open(thinh_file_path, "r", encoding="utf-8") as thinh_file:
                data = json.load(thinh_file)
                if isinstance(data, list):
                    quote = random.choice(data)["data"]  
                else:
                    raise ValueError("Dữ liệu trong thinh.json không đúng định dạng.")

            with open(url_file_path, "r", encoding="utf-8") as url_file:
                urls = [line.strip() for line in url_file if line.strip()]

            if not urls:
                self.replyMessage(Message(text="🚦 Tệp URL không chứa dữ liệu."), message_object, thread_id, thread_type)
                return

            random_url = random.choice(urls)


            send_video = self.should_send_video()

            if send_video:
                if os.path.exists(video_file_path):
                    with open(video_file_path, "r", encoding="utf-8") as video_file:
                        video_urls = [line.strip() for line in video_file if line.strip()]

                    if video_urls:
                        random_video_url = random.choice(video_urls)
                        thumbnail_url = "https://files.catbox.moe/ksg81k.jpg"  
                        duration = 1000  
                        message_to_send = Message(text=f"🤭 {quote}")
                        self.sendRemoteVideo(
                            random_video_url,
                            thumbnail_url,
                            duration=duration,
                            message=message_to_send,
                            thread_id=thread_id,
                            thread_type=thread_type,
                            width=1080,
                            height=1920,
                            ttl=120000
                        )
                        self.last_sent = "video"  
                        return


            response = requests.get(random_url, stream=True)
            if response.status_code == 200:
                image_path = "temp_image.jpg"
                with open(image_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                self.sendLocalImage(
                    imagePath=image_path,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    message=Message(text=f"🤭 {quote}"),
                    ttl=30000
                )
                os.remove(image_path)
                self.last_sent = "image"  
            else:
                self.replyMessage(Message(text="🚦 Không thể tải ảnh từ URL."), message_object, thread_id, thread_type)

        except json.JSONDecodeError:
            self.replyMessage(Message(text="🚦 Lỗi định dạng JSON trong tệp thinh.json."), message_object, thread_id, thread_type)
        except Exception as e:
            self.replyMessage(Message(text=f"🚦 Có lỗi xảy ra: {str(e)}"), message_object, thread_id, thread_type)

    def should_send_video(self):

        if self.last_sent is None:
            return random.choice([True, False])

        return self.last_sent != "video"
    def handle_capcutvd_command(self, message, message_object, thread_id, thread_type, author_id):
        content = message.strip().split()
        if len(content) < 2:
            error_message = Message(text="❌ Vui lòng nhập từ khóa tìm kiếm video CapCut.")
            self.replyMessage(error_message, message_object, thread_id, thread_type)
            return

        keyword = " ".join(content[1:]).strip()

        try:
            encoded_keyword = urllib.parse.quote(keyword)
            api_url = f'https://subhatde.id.vn/capcut/search?keyword={encoded_keyword}'
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            if not data or len(data) == 0:
                raise KeyError("Không có video nào được tìm thấy cho từ khóa này.")

            gui = f"🤭 Tìm thấy {len(data)} video CapCut với từ khóa '{keyword}':\n\n"


            video = random.choice(data)

            title = video.get('title', 'Không có tiêu đề')
            short_title = video.get('short_title', 'Không có tên ngắn')
            views = video.get('play_amount', 0)
            likes = video.get('like_count', 0)
            comments = video.get('comment_count', 0)
            author = video.get('author', {})
            author_name = author.get('name', 'Không có tác giả')
            author_id = author.get('unique_id', 'Không có tác giả ID')
            video_url = video.get('video_url', 'Không có video URL')

            thumbnail_url = "https://files.catbox.moe/ksg81k.jpg"
            duration = 1000

            quote = f"{title} ({short_title})\n" \
                    f"   - Lượt xem: {views}\n" \
                    f"   - Lượt thích: {likes}\n" \
                    f"   - Lượt bình luận: {comments}\n" \
                    f"   - Tác giả: {author_name} (@{author_id})\n" \
                    f"   - Link video: {video_url}"

            message_to_send = Message(text=f"🤭 {quote}")
            self.sendRemoteVideo(
                video_url,
                thumbnail_url,
                duration=duration,
                message=message_to_send,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1080,
                height=1920,
                ttl=120000
            )

        except requests.exceptions.RequestException as e:
            error_message = Message(text=f"❌ Đã xảy ra lỗi khi gọi API: {str(e)}")
            self.sendMessage(error_message, thread_id, thread_type)
        except KeyError as e:
            error_message = Message(text=f"❌ Dữ liệu từ API không đúng cấu trúc: {str(e)}")
            self.sendMessage(error_message, thread_id, thread_type)
        except Exception as e:
            error_message = Message(text=f"❌ Đã xảy ra lỗi không xác định: {str(e)}")
            self.sendMessage(error_message, thread_id, thread_type)
    def handle_translate_command(self, message, message_object, thread_id, thread_type, author_id):
        message_text = message.strip()
        parts = message_text.split(maxsplit=2)

        if len(parts) < 3:
            language_menu = "🤭 Đây là danh sách các ngôn ngữ có thể dịch:\n" \
                            "1. Tiếng Anh (en)\n" \
                            "2. Tiếng Việt (vi)\n" \
                            "3. Tiếng Nhật (ja)\n" \
                            "4. Tiếng Pháp (fr)\n" \
                            "5. Tiếng Đức (de)\n" \
                            "6. Tiếng Hàn (ko)\n" \
                            "7. Tiếng Tây Ban Nha (es)\n" \
                            "8. Tiếng Trung (zh-CN)\n" \
                            "9. Tiếng Ý (it)\n" \
                            "10. Tiếng Bồ Đào Nha (pt)"\
                            "vd: #dich ko xin chào"
            self.replyMessage(Message(text=language_menu), message_object, thread_id, thread_type)

            return

        target_language = parts[1]
        text_to_translate = parts[2]

        try:
            translator = Translator()
            translated = translator.translate(text_to_translate, src='auto', dest=target_language)
            response = f"Dịch từ '{text_to_translate}' sang '{target_language}': {translated.text}"
            self.replyMessage(Message(text=response), message_object, thread_id, thread_type)
        except Exception as e:
            self.replyMessage(Message(text=f"❌ Lỗi khi dịch: {str(e)}"), message_object, thread_id, thread_type)

    ########################




    def handle_autodich_command(self, command, message_object, thread_id, thread_type, author_id):
        try:
            group_info = self.fetchGroupInfo(groupId=thread_id)  # Added self.
            admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
            creator_id = group_info.gridInfoMap[thread_id]['creatorId']

            if author_id in admin_ids and author_id != creator_id:
                self.replyMessage(  # Added self.
                    Message(text="🚦Lệnh bất khả thi với thí chủ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=300000
                )
                return

            if command == "on":
                self.auto_translate_enabled = True
                self.replyMessage(Message(text="🤭 Tự động dịch đã được bật."), message_object, thread_id, thread_type)
            elif command == "off":
                self.auto_translate_enabled = False
                self.replyMessage(Message(text="🤭 Tự động dịch đã được tắt."), message_object, thread_id, thread_type)
        except Exception as e:
            self.replyMessage(Message(text=f"❌ Lỗi: {str(e)}"), message_object, thread_id, thread_type)


    def handle_translate_message(self, message, message_object, thread_id, thread_type, author_id):
        if author_id == self.uid:  # Added self.
            return

        try:
            words = message.strip().split()
            translator = GoogleTranslator(source='auto', target='vi')  # Đảm bảo lớp được định nghĩa

            # Nếu là một từ đơn, dịch kèm theo thể loại
            if len(words) == 1:
                word = words[0]
                translated = translator.translate(word)

                # Lấy các thể loại của từ
                try:
                    from nltk.corpus import wordnet
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

                except LookupError:
                    import nltk
                    nltk.download('wordnet')
                    response = f"{word}: {translated}"

            # Nếu là câu, chỉ dịch nghĩa
            else:
                translated = translator.translate(message)
                if message != translated:
                    response = f"Dịch: {translated}"
                else:
                    return

            self.replyMessage(Message(text=response), message_object, thread_id, thread_type)  # Added self.

        except Exception as e:
            self.replyMessage(Message(text=f"🌸 Lỗi khi dịch: {str(e)}"), message_object, thread_id, thread_type)  # Added self.


    
    
    ##############################
    def handle_ifcc_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ")
        if len(parts) < 2:
            error_message = Message(text="🚦 Vui lòng cung cấp URL để lấy thông tin.")
            self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
            return

        url = parts[1]
        api_url = f"https://subhatde.id.vn/capcut/info?url={url}"

        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                error_message = Message(text="🚦 Không thể lấy thông tin từ URL.")
                self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
                return

            data = response.json()
            user = data.get("user", {})
            if not user:
                error_message = Message(text="🚦 Không tìm thấy thông tin người dùng.")
                self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
                return

            user_info = (
                f"👤 Tên: {user.get('name', 'N/A')}\n"
                f"🆔 UID:{user.get('uid', 'N/A')}\n"
                f"🎤 Mô tả: {user.get('description', 'Không có mô tả')}\n"
                f"👤 Giới tính: {'Nam' if user.get('gender') == 1 else 'Nữ'}\n"
                f"📹 Số video: {user.get('creator_info', {}).get('video_work_count', '0')}\n"
                f"🔗 Link Profile: https://www.tiktok.com/@{user.get('public_id')}"
            )

            avatar_url = user.get("avatar_url", "")
            if avatar_url:
                try:
                    img_response = requests.get(avatar_url, stream=True)
                    if img_response.status_code == 200:

                        img_path = "avatar.jpg"
                        with open(img_path, 'wb') as img_file:
                            for chunk in img_response.iter_content(1024):
                                img_file.write(chunk)
                        message_to_send = Message(text=f"🌸 Ảnh info đã được gửi!\n{user_info}")

                        self.sendLocalImage(img_path, message=message_to_send, thread_id=thread_id, thread_type=thread_type, width=1080, height=300, ttl=30000)
                    else:
                        self.sendLocalImage('default_avatar.jpg', message=message_object, thread_id=thread_id, thread_type=thread_type, width=300, height=300, ttl=30000)
                except requests.exceptions.RequestException:
                    self.sendLocalImage('default_avatar.jpg', message=message_object, thread_id=thread_id, thread_type=thread_type, width=300, height=300, ttl=30000)
        except Exception as e:
            error_message = Message(text=f"🚦 Có lỗi xảy ra khi lấy thông tin: {str(e)}")
            self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
    def process_add_command(self, author_id, message, message_object, thread_id, thread_type):
        parts = message.split(" ")
        if len(parts) < 3 or not parts[1].isdigit() or not hasattr(message_object, 'mentions'):
            self.replyMessage(
                Message(text="🚦 Cú pháp không hợp lệ. Sử dụng: #add số lần @mention"),
                message_object,
                thread_id,
                thread_type
            )
            return

        times = int(parts[1])
        mentions = message_object.mentions
        if not mentions:
            self.replyMessage(
                Message(text="🚦 Bạn cần mention một người dùng."),
                message_object,
                thread_id,
                thread_type
            )
            return

        mentioned_user_id = mentions[0]['uid']
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id,
                thread_type
            )
            return

        user_info = self.fetchUserInfo(mentioned_user_id)
        user_name = user_info.changed_profiles[mentioned_user_id].displayName

        self.replyMessage(
            Message(text=f"🤭 Đang tiến hành mời/kick {user_name} {times} lần."),
            message_object,
            thread_id,
            thread_type
        )

        threading.Thread(target=self.handle_add_and_kick_user, args=(mentioned_user_id, thread_id, thread_type, times)).start()

    def handle_add_and_kick_user(self, user_id, thread_id, thread_type, times):
        try:
            for _ in range(times):
                self.add_and_kick(user_id, thread_id)
            send_message = f"🤭 Đã hoàn thành {times} lần mời/kick cho người dùng ID {user_id}."
        except Exception as e:
            send_message = f"🚦 Lỗi khi thực hiện: {str(e)}"
        self.sendMessage(Message(text=send_message), thread_id, thread_type)

    def add_and_kick(self, user_id, thread_id):
        try:
            self.addUsersToGroup([user_id], thread_id)
            self.kickUsersFromGroup([user_id], thread_id)
        except Exception as e:
            print(f"🚦 Lỗi khi mời/kick: {str(e)}")
    def handle_sos(self, thread_id, thread_type, message_object, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        self.activate_sos_mode(thread_id, thread_type, message_object)

    def handle_unlock(self, thread_id, thread_type, message_object, author_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦 Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        self.deactivate_sos_mode(thread_id, thread_type, message_object)

    def activate_sos_mode(self, thread_id, thread_type, message_object):
        self.changeGroupSetting(groupId=thread_id, lockSendMsg=1)
        self.replyMessage(Message(text="🤖💦 Bot sos đã được bật."), message_object, thread_id=thread_id, thread_type=thread_type, ttl=300000)

    def deactivate_sos_mode(self, thread_id, thread_type, message_object):
        self.changeGroupSetting(groupId=thread_id, lockSendMsg=0)
        self.replyMessage(Message(text="🚦 Đã tắt sos."), message_object, thread_id=thread_id, thread_type=thread_type, ttl=300000)
    def handle_sr_command(self, message, message_object, thread_id, thread_type, author_id):
        parts = message.split(" ")
        if len(parts) <= 1:
            self.replyMessage(
                Message(text="🤭 Vui lòng cung cấp tên tìm kiếm sau lệnh #sr"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        search_name = " ".join(parts[1:]).strip()
        encoded_keyword = urllib.parse.quote(search_name)
        self.last_search_name = search_name
        api_url = f'https://subhatde.id.vn/tiktok/searchvideo?keywords={encoded_keyword}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            if data["code"] == 0:
                videos = data['data']['videos']
                if videos:
                    search_results = "🔍 Kết quả tìm kiếm:\n"
                    for idx, video in enumerate(videos[:20]):
                        title = video['title']
                        search_results += f"{idx+1}. {title}\n"
                    self.replyMessage(
                        Message(text=search_results),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                    self.replyMessage(
                        Message(text="• Reply số trên danh sách nhạc để chọn bài hát."),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                    self.next_step[author_id] = 'wait_select'
                    self.user_selection_status[author_id] = False

                    self.selection_timer[author_id] = time.time() + 30  # 30 seconds to choose

                else:
                    self.replyMessage(
                        Message(text="💢 Không tìm thấy video nào."),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
            else:
                self.replyMessage(
                    Message(text="💢 Đã xảy ra lỗi khi tìm kiếm."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )
        except requests.exceptions.RequestException as e:
            self.replyMessage(
                Message(text=f"🤭 Lỗi khi kết nối đến API: {e}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )

    def handle_selection(self, message, message_object, thread_id, thread_type, author_id):
        if time.time() > self.selection_timer.get(author_id, 0):
            pass
        try:
            selection = int(message.strip())
            if selection < 1 or selection > 20:
                self.replyMessage(
                    Message(text="😵‍💫 Số chọn không hợp lệ. Vui lòng chọn số từ 1 đến 20."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            api_url = f'https://subhatde.id.vn/tiktok/searchvideo?keywords={urllib.parse.quote(self.last_search_name)}'
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            if data["code"] == 0:
                video = data['data']['videos'][selection - 1]
                video_url = video['play']
                video_cover = video['cover']
                title = video['title']
                video_cover_filename = video_cover.split("/")[-1]
                video_cover_filename = hashlib.md5(video_cover_filename.encode()).hexdigest()[:10] + ".jpg"
                temp_image_path = os.path.join(os.getcwd(), video_cover_filename)
                self.download_image_to_path(video_cover, temp_image_path)
                self.sendLocalImage(temp_image_path, thread_id, thread_type)
                self.sendRemoteVideo(
                    video_url,
                    video_cover,
                    duration=100,
                    message=Message(text="Video bạn chọn: " + title),
                    thread_id=thread_id,
                    thread_type=thread_type,
                    width=1080,
                    height=1920
                )
                if os.path.exists(temp_image_path):
                    os.remove(temp_image_path)
                voice_url = video_url
                self.sendRemoteVoice(voice_url, thread_id, thread_type, fileSize=100000)

                self.user_selection_status[author_id] = True
        except Exception:
            pass

    def download_image_to_path(self, url, file_path):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except requests.exceptions.RequestException:
            pass

    def create_gif(self, image_list, gif_path, duration):
        directory = os.path.dirname(gif_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_list[0].save(gif_path, save_all=True, append_images=image_list[1:], duration=duration, loop=0)

    def download_images(self, image_urls):
        images = []
        for url in image_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    images.append(img)
            except:
                pass
        return images

    def handle_gif_command(self, message, message_object, thread_id, thread_type, author_id):
        if message_object.quote:
            attach = message_object.quote.attach
            if attach:
                try:
                    attach_data = json.loads(attach)
                    image_url = attach_data.get('hdUrl') or attach_data.get('href')
                    if image_url:
                        image_url = image_url.replace("\\/", "/")
                        self.reply_images.append(image_url)
                        self.replyMessage(
                            Message(text=f"Đã thêm ảnh: {len(self.reply_images)} ảnh được reply."),
                            message_object, thread_id, thread_type
                        )
                    else:
                        self.replyMessage(
                            Message(text="Không tìm thấy URL ảnh trong tin nhắn reply."),
                            message_object, thread_id, thread_type
                        )
                except json.JSONDecodeError:
                    self.replyMessage(
                        Message(text="Không thể đọc dữ liệu ảnh từ reply."),
                        message_object, thread_id, thread_type
                    )
            else:
                self.replyMessage(
                    Message(text="Hãy reply ít nhất 2 ảnh để tạo GIF."),
                    message_object, thread_id, thread_type
                )
        else:
            self.replyMessage(
                Message(text="Hãy reply ít nhất 2 ảnh để tạo GIF."),
                message_object, thread_id, thread_type
            )

    def handle_taogif_command(self, message, message_object, thread_id, thread_type):
        if len(self.reply_images) < 2:
            self.replyMessage(
                Message(text="Cần ít nhất 2 ảnh đã reply để tạo GIF."),
                message_object, thread_id, thread_type
            )
            return

        try:

            gif_path = "modules/cache/gif/taogif.gif"
            images = self.download_images(self.reply_images)
            resized_images = [img.resize((320, 240)) for img in images]  
            self.create_gif(resized_images, gif_path, 500)  
            self.sendLocalGif(
                gifPath=gif_path,
                thumbnailUrl=None,
                thread_id=thread_id,
                thread_type=thread_type,
                width=320,
                height=240,
                ttl=300000
            )
            self.reply_images = []
        except Exception as e:
            self.replyMessage(
                Message(text=f"Đã xảy ra lỗi khi tạo GIF: {e}"),
                message_object, thread_id, thread_type
            )



    def handle_stk_command(self, message, message_object, thread_id, thread_type):
        if message_object.quote:
            attach = message_object.quote.attach
            if attach:
                try:
                    attach_data = json.loads(attach)
                except json.JSONDecodeError:
                    self.replyMessage(
                        Message(text="Dữ liệu ảnh không hợp lệ."),
                        message_object, thread_id, thread_type
                    )
                    return

                image_url = attach_data.get('hdUrl') or attach_data.get('href')
                if not image_url:
                    self.replyMessage(
                        Message(text="Không tìm thấy URL ảnh."),
                        message_object, thread_id, thread_type
                    )
                    return

                image_url = image_url.replace("\\/", "/")
                image_url = urllib.parse.unquote(image_url)

                if self.is_valid_image_url(image_url):
                    self.create_sticker(image_url, message_object, thread_id, thread_type)
                else:
                    self.replyMessage(
                        Message(text="URL không phải là ảnh hợp lệ."),
                        message_object, thread_id, thread_type
                    )
            else:
                self.replyMessage(
                    Message(text="Không có ảnh nào được reply."),
                    message_object, thread_id, thread_type
                )
        else:
            self.replyMessage(
                Message(text="Hãy reply vào ảnh cần tạo sticker."),
                message_object, thread_id, thread_type
            )

    def create_sticker(self, image_url, message_object, thread_id, thread_type):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                image_path = 'temp_image.png'
                img.save(image_path)

                output_file_name = self.remove_background_from_url(image_url)
                if output_file_name:
                    webp_image_url = self.convert_image_to_webp(output_file_name)
                    if webp_image_url:
                        self.sendCustomSticker(
                            staticImgUrl=image_url,
                            animationImgUrl=webp_image_url,
                            thread_id=thread_id,
                            thread_type=thread_type
                        )
                        self.replyMessage(
                            Message(text="Sticker đã được tạo!"),
                            message_object, thread_id, thread_type
                        )
                    else:
                        self.replyMessage(
                            Message(text="Không thể chuyển đổi hình ảnh."),
                            message_object, thread_id, thread_type
                        )
                else:
                    self.replyMessage(
                        Message(text="Không thể xóa nền ảnh."),
                        message_object, thread_id, thread_type
                    )
            else:
                self.replyMessage(
                    Message(text="Không thể tải ảnh."),
                    message_object, thread_id, thread_type
                )
        except Exception as e:
            self.replyMessage(
                Message(text=f"Đã xảy ra lỗi: {str(e)}"),
                message_object, thread_id, thread_type
            )

    def is_valid_image_url(self, url):
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        return any(url.lower().endswith(ext) for ext in valid_extensions)

    def convert_image_to_webp(self, image_path):
        try:
            with Image.open(image_path) as image:
                buffered = io.BytesIO()
                image.save(buffered, format="WEBP")
                buffered.seek(0)
                webp_image_url = self.upload_to_catbox(buffered)
                return webp_image_url
        except Exception as e:
            print("Lỗi trong quá trình chuyển đổi:", e)
        return None

    def upload_to_catbox(self, buffered):
        url = "https://catbox.moe/user/api.php"
        files = {
            'fileToUpload': ('image.webp', buffered, 'image/webp')
        }
        data = {
            'reqtype': 'fileupload'
        }
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            if response.text.startswith("http"):
                return response.text
            else:
                print("Lỗi khi upload:", response.text)
        else:
            print("Lỗi kết nối:", response.status_code)
        return None

    def remove_background_from_url(self, img_url):
        try:
            output_file_name = 'no-bg.png'
            self.rmbg.remove_background_from_img_url(img_url, new_file_name=output_file_name)
            return output_file_name
        except Exception as e:
            print(f"Lỗi khi xóa nền từ URL: {e}")
            return None
    def handle_autodl_command(self, author_id, message, message_object, thread_id, thread_type):
        group_info = self.fetchGroupInfo(groupId=thread_id)


        if group_info is None:
            self.replyMessage(
                Message(text="💢 Không thể lấy thông tin nhóm."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return


        grid_info = group_info.get('gridInfoMap', {}).get(thread_id, {})
        if not grid_info:
            self.replyMessage(
                Message(text="💢 đòi bug à con chó."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        admin_ids = grid_info.get('adminIds', [])
        creator_id = grid_info.get('creatorId', None)

        if author_id in admin_ids and author_id != creator_id:
            self.replyMessage(
                Message(text="🚦Lệnh bất khả thi với thí chủ."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=300000
            )
            return

        parts = message.split(" ")
        if len(parts) < 2:
            error_message = Message(text="🚦 Vui lòng nhập 'on' hoặc 'off' để bật/tắt tự động tải video.")
            self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)
            return

        command = parts[1].lower()
        if command == "on":
            self.autodl_enabled = True
            success_message = Message(text="🤭 Tự động tải video TikTok đã được bật.")
            self.replyMessage(success_message, message_object, thread_id, thread_type, ttl=30000)
        elif command == "off":
            self.autodl_enabled = False
            success_message = Message(text="🤭 Tự động tải video TikTok đã được tắt.")
            self.replyMessage(success_message, message_object, thread_id, thread_type, ttl=30000)
        else:
            error_message = Message(text="🚦 Lệnh không hợp lệ. Vui lòng sử dụng 'on' hoặc 'off'.")
            self.replyMessage(error_message, message_object, thread_id, thread_type, ttl=30000)

    def is_tiktok_url(self, url):
        return url.startswith("https://vt.tiktok.com/")

    def handle_tiktok_download(self, url, message_object, thread_id, thread_type):
        api_url = f"https://subhatde.id.vn/tiktok/downloadvideo?url={url}"
        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            data = response.json()
            video_data = data.get('data', {})
            if not video_data:
                self.replyMessage(
                    Message(text="💢 Không tìm thấy dữ liệu video."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            video_title = video_data.get('title', 'Không có tiêu đề')
            video_play_url = video_data.get('play', '')
            video_cover = video_data.get('cover', '')
            if not video_play_url:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            send_title = f"📺 Tiêu đề Video: {video_title}\n💖 Số lượt thích: {video_data.get('digg_count', 0)}\n↪️ Số lượt chia sẻ: {video_data.get('share_count', 0)}\n💬 Số bình luận: {video_data.get('comment_count', 0)}\n📌 Link Video: {url}"
            messagesend = Message(text=send_title)
            thumbnail_url = video_cover if video_cover else 'https://files.catbox.moe/34xdgb.jpeg'
            duration = video_data.get('duration', 60)
            self.sendRemoteVideo(
                video_play_url,
                thumbnail_url,
                duration=duration,
                message=messagesend,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600,
                ttl=30000
            )

        except Exception as e:
            self.replyMessage(
                Message(text=f"💢 Có lỗi xảy ra khi tải video: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
    def handle_qr_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip():
            self.replyMessage(
                Message(text="💦 Vui lòng cung cấp nội dung sau lệnh #qr."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        content = parts[1].strip()
        qr_image_path = os.path.join(os.getcwd(), "qr_code.png")

        try:
            qr = qrcode.make(content)
            qr.save(qr_image_path)
            self.sendLocalImage(
                qr_image_path,
                message=Message(text=f"Mã QR của nội dung: {content}"),
                thread_id=thread_id,
                thread_type=thread_type,
                width=None,
                height=None,
                ttl=30000
            )
        except Exception as e:
            self.replyMessage(
                Message(text=f"💦 Đã xảy ra lỗi khi tạo mã QR: {e}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
        finally:
            if os.path.exists(qr_image_path):
                os.remove(qr_image_path)
    def handle_catbot_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip():
            self.replyMessage(
                Message(text="?? Vui lòng cung cấp URL để rút gọn sau lệnh #catbot."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        long_url = parts[1].strip()
        type_tiny = pyshorteners.Shortener()

        try:
            short_url = type_tiny.tinyurl.short(long_url)
            self.replyMessage(
                Message(text=f"🔗 Đây là link rút gọn của bạn: {short_url}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
        except Exception as e:
            self.replyMessage(
                Message(text=f"💦 Đã xảy ra lỗi khi rút gọn URL: {e}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
    def handle_link_command(self, message, message_object, thread_id, thread_type):
        parts = message.split(" ", 1)
        if len(parts) < 2 or not parts[1].strip():
            self.replyMessage(
                Message(text="💦 Vui lòng cung cấp URL để rút gọn sau lệnh #link."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        long_url = parts[1].strip()
        api_url = f'https://link4m.co/api-shorten/v2?api=66f43a0fb711e46de04d8c14&url={long_url}'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                if data["status"] == "success":
                    short_url = data["shortenedUrl"]
                    self.replyMessage(
                        Message(text=f"🤭 Đây là link rút gọn của bạn: {short_url}"),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                else:
                    self.replyMessage(
                        Message(text="💦 Lỗi khi rút gọn URL."),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
            else:
                self.replyMessage(
                    Message(text="💦 Lỗi kết nối API."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )
        except Exception as e:
            self.replyMessage(
                Message(text=f"💦 Đã xảy ra lỗi: {e}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
    def create_canvas(self, user_data):
        background_image = Image.open("anh/info.jpg")
        draw = ImageDraw.Draw(background_image)
        fonts_folder = "font"
        font_files = [f for f in os.listdir(fonts_folder) if f.endswith('.ttf')]
        fontc = os.path.join(fonts_folder, random.choice(font_files))
        font_title = ImageFont.truetype(fontc, 30)
        font_info = ImageFont.truetype(fontc, 30)
        rainbow_colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]
        info = [
            ("Tên:", user_data.get('displayName', 'N/A')),
            ("Id:", user_data.get('userId', 'N/A')),
            ("Username:", user_data.get('username', 'N/A')),
            ("Số điện thoại:", "N/A"),
            ("Giới tính:", {0: "Nam", 1: "Nữ"}.get(user_data.get('gender'), "Khác")),
            ("Sinh nhật:", datetime.fromtimestamp(user_data.get('dob')).strftime('%d/%m/%Y') if user_data.get('dob') else 'N/A'),
            ("Tiểu sử:", user_data.get('status', 'N/A'))
        ]
        image_width, image_height = background_image.size
        text_x = image_width // 4
        start_y = image_height // 4
        for index, (title, value) in enumerate(info):
            y_position = start_y + (index * 40)
            color = random.choice(rainbow_colors)
            draw.text((text_x, y_position), f"{title} {value}", font=font_info, fill=color)
        canvas_path = "anh/info_generated.jpg"
        background_image.save(canvas_path)
        return canvas_path
    def handle_sms_command(self, message, message_object, thread_id, thread_type, author_id):
        parts = message.split()
        if len(parts) == 1:
            self.replyMessage(Message(text='💢 Vui lòng nhập số điện thoại sau lệnh.'), message_object, thread_id=thread_id, thread_type=thread_type)
            return

        attack_phone_number = parts[1]

        if not attack_phone_number.isnumeric() or len(attack_phone_number) != 10:
            self.replyMessage(Message(text='🤭 Số điện thoại không hợp lệ! Vui lòng nhập đúng số.'), message_object, thread_id=thread_id, thread_type=thread_type)
            return

        if attack_phone_number in ['113', '911', '114', '115']:
            self.replyMessage(Message(text="🚦 Số này không thể spam."), message_object, thread_id=thread_id, thread_type=thread_type)
            return

        current_time = datetime.now()
        if author_id in self.last_sms_times:
            last_sent_time = self.last_sms_times[author_id]
            elapsed_time = (current_time - last_sent_time).total_seconds()
            if elapsed_time < 120:
                remaining_time = 120 - int(elapsed_time)
                self.replyMessage(Message(text=f"⏳ Bạn cần đợi {remaining_time}s nữa mới có thể thực hiện lệnh tiếp theo!"), message_object, thread_id=thread_id, thread_type=thread_type)
                return

        self.last_sms_times[author_id] = current_time

        file_path1 = os.path.join(os.getcwd(), "111.py")
        process = subprocess.Popen(["python", file_path1, attack_phone_number, "7"])

        now = datetime.now()
        time_str = now.strftime("%d/%m/%Y %H:%M:%S")
        masked_phone_number = f"{attack_phone_number[:3]}***{attack_phone_number[-3:]}"
        bot = "version 1.0.3"
        msg_content = f'''📢 Thông báo từ Bot Spam SMS 📢

🦸‍♂️ Bot {bot} đã thực hiện hành động spam SMS cho số điện thoại sau:

📞 Số điện thoại: 
   └─> `{masked_phone_number}`

🕰️ Thời gian thực hiện: 
   └─> `{time_str}`

⏳ Thời gian chờ (Cooldown): 
   └─> `120s` (Chờ trước khi có thể thử lại)

🔒 Thông tin bảo mật: 
   └─> Địa chỉ email và thông tin cá nhân của bạn sẽ không bị tiết lộ trong quá trình spam.

💻 Hệ thống: 
   └─> Bot đang chạy bằng Python và một số công cụ hỗ trợ.

👤 Quản trị viên: 
   └─> 很帅  (Tối ưu hóa công cụ spam SMS)

---------------------------------------
💦 **Lưu ý**: Hành động này chỉ có thể thực hiện một lần trong 120s. Sau khi thời gian chờ hết, bạn có thể gửi lại yêu cầu.
'''

        mention = Mention(author_id, length=len("@Member"), offset=0)
        color_green = MessageStyle(style="color", color="#4caf50", length=300, offset=0, auto_format=False)
        style = MultiMsgStyle([color_green])
        sms_img = "sms.png"

        self.replyMessage(Message(text=msg_content, style=style, mention=mention), message_object, thread_id=thread_id, thread_type=thread_type)

    def handle_mention_command(self, message, message_object, thread_id, thread_type):
        mentions = message_object.mentions if hasattr(message_object, 'mentions') else []
        if mentions:
            mentioned_user_id = mentions[0]['uid']
            if mentioned_user_id == '968896132353789689':  

                response = self.call_simsimi_api(message)

                if response:
                    self.replyMessage(
                        Message(text=response),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )
                else:
                    self.replyMessage(
                        Message(text="Có lỗi khi phản hồi."),
                        message_object,
                        thread_id=thread_id,
                        thread_type=thread_type
                    )

    def call_simsimi_api(self, message):
        url = f'https://www.hungdev.id.vn/others/simsimi?text={message}&apikey=iwHYQHJjTU'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", "Không có phản hồi từ SimSimi.")
                else:
                    return "Lỗi từ API SimSimi."
            else:
                return "Lỗi kết nối API."
        except Exception as e:
            return f"Lỗi khi kết nối với SimSimi: {str(e)}"
    def anti_all(self, message_object, thread_id, author_id):
        mentions = message_object.mentions if hasattr(message_object, 'mentions') else []

        if mentions:
            for mention in mentions:
                if mention.uid == '-1':
                    user_info = self.fetchUserInfo(author_id)
                    user_name = user_info.changed_profiles[author_id].displayName
                    self.blockUsersInGroup(members=[author_id], groupId=thread_id)

                    return
    def handle_dlfb_command(self, content, message_object, thread_id, thread_type):
        parts = content.split(" ")
        if len(parts) < 2:
            self.replyMessage(
                Message(text="🚦 Vui lòng cung cấp URL video Facebook."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )
            return

        url = parts[1]
        api_url = f"https://subhatde.id.vn/fb/download?url={url}"
        try:
            response = requests.get(api_url)
            if response.status_code != 200:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            data = response.json()
            video_data = data.get('medias', [{}])[0]
            video_play_url = video_data.get('url', '')
            video_cover = data.get('thumbnail', 'https://files.catbox.moe/34xdgb.jpeg')
            video_title = data.get('title', 'Không có tiêu đề')
            duration = data.get('duration', 60)

            if not video_play_url:
                self.replyMessage(
                    Message(text="💢 Không thể tải video, URL không hợp lệ."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    ttl=30000
                )
                return

            send_title = f"📺 Tiêu đề Video: {video_title}\n💬 Nguồn: Facebook\n⏱️ Thời lượng: {duration // 60}:{duration % 60:02d}"
            messagesend = Message(text=send_title)

            self.sendRemoteVideo(
                video_play_url,
                video_cover,
                duration=duration,
                message=messagesend,
                thread_id=thread_id,
                thread_type=thread_type,
                width=1200,
                height=1600,
                ttl=30000
            )

        except Exception as e:
            self.replyMessage(
                Message(text=f"💢 Có lỗi xảy ra khi tải video: {str(e)}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type,
                ttl=30000
            )




    def create_sticker(self, image_url, message_object, thread_id, thread_type):
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                image_path = 'temp_image.png'
                img.save(image_path)
                output_file_name = self.remove_background_from_url(image_url)
                if output_file_name:
                    webp_image_url = self.convert_image_to_webp(output_file_name)
                    message = "Sticker đã được tạo!" if webp_image_url else "Không thể chuyển đổi hình ảnh."
                    self.replyMessage(Message(text=message), message_object, thread_id, thread_type)
                    if webp_image_url:
                        self.sendCustomSticker(
                            staticImgUrl=image_url,
                            animationImgUrl=webp_image_url,
                            thread_id=thread_id,
                            thread_type=thread_type
                        )
                else:
                    self.replyMessage(Message(text="Không thể xóa nền ảnh."), message_object, thread_id, thread_type)
            else:
                self.replyMessage(Message(text="Không thể tải ảnh."), message_object, thread_id, thread_type)
        except Exception as e:
            self.replyMessage(Message(text=f"Đã xảy ra lỗi: {str(e)}"), message_object, thread_id, thread_type)

    def is_valid_image_url(self, url):
        return any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif'])

    def convert_image_to_webp(self, image_path):
        try:
            with Image.open(image_path) as image:
                buffered = io.BytesIO()
                image.save(buffered, format="WEBP")
                buffered.seek(0)
                return self.upload_to_catbox(buffered)
        except Exception as e:
            print("Lỗi trong quá trình chuyển đổi:", e)
        return None

    def upload_to_catbox(self, buffered):
        response = requests.post("https://catbox.moe/user/api.php", files={'fileToUpload': ('image.webp', buffered, 'image/webp')}, data={'reqtype': 'fileupload'})
        return response.text if response.status_code == 200 and response.text.startswith("http") else None

    def remove_background_from_url(self, img_url):
        try:
            output_file_name = 'no-bg.png'
            self.rmbg.remove_background_from_img_url(img_url, new_file_name=output_file_name)
            return output_file_name
        except Exception as e:
            print(f"Lỗi khi xóa nền từ URL: {e}")
        return None




    def changeGroupSetting(self, groupId, **kwargs):
      group_info = self.fetchGroupInfo(groupId)
      defSetting = group_info.gridInfoMap[str(groupId)]["setting"] if group_info and "gridInfoMap" in group_info else {}

      lockSendMsg = kwargs.get("lockSendMsg", defSetting.get("lockSendMsg", 0))

      params = {
          "params": self._encode({
              "lockSendMsg": lockSendMsg,
              "grid": str(groupId),
              "imei": self._imei
          }),
          "zpw_ver": 641,
          "zpw_type": 30
      }

      response = self._get("https://tt-group-wpa.chat.zalo.me/api/group/setting/update", params=params)
      data = response.json()
      results = data.get("data") if data.get("error_code") == 0 else None
      if results:

          return results

      error_code = data.get("error_code")
      error_message = data.get("error_message") or data.get("data")
      raise ZaloAPIException(f"Error #{error_code} when sending requests: {error_message}")
    def handle_getvoice_command(self, message, message_object, thread_id, thread_type, author_id):
        msg_obj = message_object
        if msg_obj.quote:
            attach = msg_obj.quote.attach
            if attach:
                try:
                    attach_data = json.loads(attach)
                except json.JSONDecodeError as e:
                    self.send_error_message(thread_id, thread_type, "Lỗi khi phân tích dữ liệu video.")
                    return

                video_url = attach_data.get('hdUrl') or attach_data.get('href')
                if video_url:
                    self.send_voice_from_video(video_url, thread_id, thread_type)
                else:
                    self.send_error_message(thread_id, thread_type, "Không tìm thấy URL video.")
            else:
                self.send_error_message(thread_id, thread_type, "Vui lòng reply tin nhắn chứa video.")
        else:
            self.send_error_message(thread_id, thread_type, "Vui lòng reply tin nhắn chứa video.")

    def send_voice_from_video(self, video_url, thread_id, thread_type):
        try:
            fake_file_size = 5 * 1024 * 1024
            self.sendRemoteVoice(video_url, thread_id, thread_type, fileSize=fake_file_size)
        except Exception as e:
            self.send_error_message(thread_id, thread_type, "Không thể gửi voice từ video này.")

    def send_error_message(self, thread_id, thread_type, error_message="Lỗi không xác định."):
        self.send(Message(text=error_message), thread_id=thread_id, thread_type=thread_type)
    def handle_scl_command(self, message, message_object, thread_id, thread_type):
        url = " ".join(message.split()[1:]).strip()
        if not url:
            self.replyMessage(
                Message(text="🤭 Vui lòng cung cấp URL SoundCloud sau lệnh /scl."),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )
            return

        try:
            response = requests.get(f"https://subhatde.id.vn/scl/download?url={url}")
            response.raise_for_status()
            data = response.json()

            if not data or "id" not in data:
                self.replyMessage(
                    Message(text="❌ Không thể tải thông tin từ URL này."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )
                return

            title = data.get("title", "Không có thông tin")
            author = data.get("author", "Không có thông tin")
            playback = data.get("playback", "Không có thông tin")
            likes = data.get("likes", "Không có thông tin")
            comment = data.get("comment", "Không có thông tin")
            share = data.get("share", "Không có thông tin")
            duration = data.get("duration", "Không có thông tin")
            create_at = data.get("create_at", "Không có thông tin")
            attachments = data.get("attachments", [])
            voice_url = attachments[0]["url"] if attachments else None

            msg = (
                f"🎶 **Thông tin bài hát:**\n"
                f"🆔 ID: {data['id']}\n"
                f"🎵 Tên: {title}\n"
                f"🎤 Tác giả: {author}\n"
                f"▶️ Lượt phát: {playback}\n"
                f"❤️ Lượt thích: {likes}\n"
                f"💬 Bình luận: {comment}\n"
                f"🔁 Chia sẻ: {share}\n"
                f"⏱ Thời lượng: {duration}\n"
                f"📅 Ngày tạo: {create_at}\n"
            )
            self.replyMessage(
                Message(text=msg),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )

            if voice_url:
                self.sendRemoteVoice(voice_url, thread_id, thread_type, fileSize=100000)
            else:
                self.replyMessage(
                    Message(text="❌ Không tìm thấy URL voice để gửi."),
                    message_object,
                    thread_id=thread_id,
                    thread_type=thread_type
                )

        except requests.RequestException as e:
            self.replyMessage(
                Message(text=f"❌ Đã xảy ra lỗi khi lấy dữ liệu: {e}"),
                message_object,
                thread_id=thread_id,
                thread_type=thread_type
            )





imei = "b03d7492-c38d-4fe6-b5d4-a9c1285fff11-7675d59b5e84e0a878ee6f0a97f9056f"
session_cookies ={"_ga":"GA1.2.1782749144.1735464586","zpsid":"INmX.421600670.6.kR0G7BeTvrSa0CPEjXtdLyzkbME8BD5dYYlGPn7w-6zNPJptkuVn9jqTvrS","zpw_sek":"udus.421600670.a0.XSDCViCEdbXT4xz1uWwUMBWi-pFXDBnXXt_fAfDUpnIKGF0vgcZDDezVsXs2CwDwlgLvH_lZveDZ3m9EiccUM0","__zi":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","__zi-legacy":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","ozi":"2000.UelfvS0R1PqpcVIltHyTt6UL_Rp0HqkNRP3zly55JDzabVhnmK97scAKz_ur.1","app.event.zalo.me":"2456638497330600094","_zlang":"vn","zoaw_sek":"vzo8.350505344.2.vAx6OtKZA6drQinzTICeQNKZA6br8oXfT2te6X8ZA6a","zoaw_type":"0"}
honhattruong = Honhattruong('TuW7DFuDstmHn1fRRkvSD3CK', 'secret_key', imei=imei, session_cookies=session_cookies)
honhattruong.listen()