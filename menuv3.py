from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from zlapi import Message, ThreadType, Mention, MessageStyle, MultiMsgStyle
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import datetime
import threading
import time
import random 
import json
import requests
from Crypto.Cipher import AES
import base64
import logging
def ThanhNgocLoveThanhVy():
    try:
        with open('admin.json', 'r') as adminvip:
            adminzalo = json.load(adminvip)
            return set(adminzalo.get('idadmin', []))
    except FileNotFoundError:
        return set()
idadmin = ThanhNgocLoveThanhVy()
class ThanhNgocDzYeuThanhVy(ZaloAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spamming = False
        self.spam_thread = None
        self.spammingvip = False
        self.spam_threadvip = None
        self.reo_spamming = False
        self.reo_spam_thread = None
        self.idnguoidung = ['207754413506549669']
        self.excluded_user_ids = []
        self.call_running = False
        self.successful_call = 0
        self.todo_running = False
        self.successful_todos = 0
        self.thread_pool = ThreadPoolExecutor(max_workers=100000000)
        self.imei = kwargs.get('imei')
        self.session_cookies = kwargs.get('session_cookies')
        self.secret_key = self.getSecretKey()
        self.header = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; CPH2239 Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.105 Mobile Safari/537.36 GoogleApp/15.49.42.ve.arm64",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "origin": "https://chat.zalo.me",
            "sec-fetch-site": "same-site",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Accept-Encoding": "gzip",
            "referer": "https://chat.zalo.me/",
            "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        }


    def zalo_encode(self, params):
        try:
            key = base64.b64decode(self.secret_key)
            iv = bytes.fromhex("00000000000000000000000000000000")
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = json.dumps(params).encode()
            padded_plaintext = self._pad(plaintext, AES.block_size)
            ciphertext = cipher.encrypt(padded_plaintext)
            return base64.b64encode(ciphertext).decode()
        except Exception as e:
            logging.error(f'Encoding error: {e}')
            return None

    def _pad(self, data, block_size):
        padding_size = block_size - len(data) % block_size
        return data + bytes([padding_size] * padding_size)
    
    def StartCall(self, target_id, call_count):
        self.call_running = True
        futures = []
        
        for i in range(call_count):
            if not self.call_running:
                break
            callid_random = self.TaoIDCall()
            futures.append(
                self.thread_pool.submit(
                    self.call,
                    target_id,
                    callid_random
                )
            )
            time.sleep(0.5)

        for future in futures:
            future.result()

        completion_message = f"𝐒𝐩𝐚𝐦 𝐒𝐮𝐜𝐜𝐞𝐬𝐬 𝐅𝐮𝐥𝐥 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 {self.successful_call} </> {call_count}𝐂𝐚𝐥𝐥"
        print(completion_message)
        self.call_running = False
    def TaoIDCall(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(9)])
    def call(self, target_id, callid_random):
        payload = {
            "params": {
                "calleeId": target_id,
                "callId": callid_random,
                "codec": "[]\n",
                "typeRequest": 1,
                "imei": self.imei
            }
        }
        payload["params"] = self.zalo_encode(payload["params"])
        call_url1 = 'https://voicecall-wpa.chat.zalo.me/api/voicecall/requestcall?zpw_ver=646&zpw_type=24'
        response = requests.post(call_url1, params=payload["params"], data=payload, headers=self.header, cookies=self.session_cookies)
        json_data = json.loads(response.text)
        call_payload = {
                "params": {
                    'calleeId': target_id,
                    'rtcpAddress': "171.244.25.88:4601",
                    'rtpAddress': "171.244.25.88:4601",
                    'codec': '[{"dynamicFptime":0,"frmPtime":20,"name":"opus/16000/1","payload":112}]\n',
                    'session': callid_random,
                    'callId': callid_random,
                    'imei': self.imei,
                    'subCommand': 3
                }
        }
        call_payload["params"] = self.zalo_encode(call_payload["params"])
        call_url2 = 'https://voicecall-wpa.chat.zalo.me/api/voicecall/request?zpw_ver=646&zpw_type=24'
        response = requests.post(call_url2, params=call_payload["params"], data=call_payload, headers=self.header, cookies=self.session_cookies)
    def StartTodo1(self, group_id, target_id, todo_content, mid, author_id, todo_count):
        self.todo_running = True
        futures = []

        for i in range(todo_count):
            if not self.todo_running:
                break
            futures.append(
                self.thread_pool.submit(
                    self.todogr,
                    group_id,
                    target_id,
                    todo_content,
                    mid,
                    author_id
                )
            )
            time.sleep(0)

        for future in futures:
            future.result()

        completion_message = f"Successfully Spammed Todo -> {self.successful_todos}/{todo_count}"
        print(completion_message)
        self.todo_running = False

    def todogr(self, group_id, target_id, todo_content, mid, author_id):
        cli_msg_id = str(int(time.time() * 1000))       
        payload = {
            "assignees": json.dumps([target_id]), 
            "dueDate": -1,
            "content": todo_content,
            "description": todo_content,
            "extra": json.dumps({
                "msgId": str(mid),
                "toUid": group_id, 
                "isGroup": True,
                "cliMsgId": cli_msg_id, 
                "msgType": 1,
                "mention": [],
                "ownerMsgUId": str(author_id),
                "message": todo_content
            }),
            "dateDefaultType": 0,
            "status": -1,
            "watchers": "[]",
            "schedule": None,
            "src": 5,
            "imei": self.imei
        }
        encoded_payload = self.zalo_encode(payload)
        api_url = "https://board-wpa.chat.zalo.me/api/board/personal/todo/create?zpw_ver=645&zpw_type=30"
        try:
            response = requests.post(api_url, data={"params": encoded_payload}, headers=self.header, cookies=self.session_cookies)
            if response.status_code == 200:
                self.successful_todos += 1
            else:
                print(f"Lỗi khi gửi Todo đến {target_id}: {response.content}")
        except Exception as e:
            print(f"Lỗi không xác định khi gửi Todo: {e}")
    def StartTodo(self, target_id, todo_content, mid, author_id, todo_count):
        self.todo_running = True
        futures = []

        for i in range(todo_count):
            if not self.todo_running:
                break
            futures.append(
                self.thread_pool.submit(
                    self.todo,
                    target_id,
                    todo_content,
                    mid,
                    author_id
                )
            )
            time.sleep(0)

        for future in futures:
            future.result()

        completion_message = f"Successfully Spammed Todo -> {self.successful_todos}/{todo_count}"
        print(completion_message)
        self.todo_running = False

    def todo(self, target_id, todo_content, mid, author_id):
        payload = {
            "assignees": json.dumps([target_id]),
            "dueDate": -1,
            "content": todo_content,
            "description": "DuongNgocLoveThanhVy",
            "extra": json.dumps({
                "msgId": mid,
                "toUid": target_id,
                "isGroup": False,
                "cliMsgId": mid,
                "msgType": 1,
                "mention": [],
                "ownerMsgUId": author_id,
                "message": todo_content
            }),
            "dateDefaultType": 0,
            "status": -1,
            "watchers": "[]",
            "schedule": None,
            "src": 1,
            "imei": imei
        }
        encoded_payload = self.zalo_encode(payload)
        api_url = "https://board-wpa.chat.zalo.me/api/board/personal/todo/create?zpw_ver=645&zpw_type=30"
        try:
            response = requests.post(api_url, data={"params": encoded_payload}, headers=self.header, cookies=session_cookies)
            if response.status_code == 200:
                self.successful_todos += 1
            else:
                print(f"Lỗi khi gửi Todo đến {target_id}: {response.content}")
        except Exception as e:
            print(f"Lỗi không xác định khi gửi Todo: {e}")
    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type):
        print(f"\033[32m{message} \033[39m|\033[31m {author_id} \033[39m|\033[33m {thread_id}\033[0m\n")
        content = message_object.content if message_object and hasattr(message_object, 'content') else ""
        if not isinstance(message, str):
            print(f"{type(message)}")
            return
        if message.startswith("menuv2"):
           self.replyMessage(Message(text='''    
      🎉𝑀𝐸𝑁𝑈 𝑉3🎉  
_____________________________
> ┌────★𝐿𝐼𝐺𝐻𝑇★──────
> ├>🪂𝐵𝑂𝑇 𝑉𝐼𝑃         
> ├ 🦈𝑻𝒐𝒅𝒐                           
> ├ 🐙𝑻𝒐𝒅𝒐𝒈𝒓                          
> ├ 🐠𝑨𝒍𝒍          
> ├ 🥮𝑪𝒂𝒏𝒗𝒂                    
> ├ 🐟𝑰𝒏𝒇𝒐                             
> ├ 🐬𝑶𝒇𝒇                              
> ├ 🦑𝑹𝒆𝒐𝑺𝒑                           
> ├ 🐉𝑺𝒕𝒐𝒑𝑹                           
> ├> 𝑶𝒕𝒉𝒆𝒓 𝑭𝒖𝒏𝒄𝒕𝒊𝒐𝒏𝒔 𝑶𝒇 𝑩𝒐𝒕            
> ├ 🐬𝑺𝒑𝒂𝒎                           
> ├ 🐋𝑺𝒕𝒐𝒑𝑺𝒑𝒂𝒎                       
> ├ 🐚𝑺𝒑𝒂𝒎𝒗𝒊𝒑                        
> ├ 🐳𝑺𝒕𝒐𝒑𝑺𝒑𝒂𝒎𝒗𝒊𝒑                    
> ├> 𝑰𝒇 𝑩𝒐𝒕 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇                
   └──────────────────
            '''), message_object, thread_id=thread_id, thread_type=thread_type)
        elif message.startswith("Call"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split()
                if len(parts) < 3:
                    self.replyMessage(
                        Message(text="𝐂𝐚𝐥𝐥 𝐈𝐃 𝐂𝐨𝐮𝐧𝐭"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return
                    
                target_id = parts[1]
                call_count = int(parts[2])
                self.replyMessage(Message(text=f'𝐒𝐩𝐚𝐦 𝐒𝐞𝐧𝐭 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 {call_count} 𝐂𝐚𝐥𝐥𝐢𝐧𝐠'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                if self.call_running:
                    self.replyMessage(
                        Message(text=f"𝐂𝐚𝐥𝐥𝐢𝐧𝐠 𝐖𝐢𝐭𝐡 𝐓𝐚𝐠𝐞𝐭 𝐈𝐃 {target_id} 𝐓𝐨 {self.successful_call}"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return
                self.StartCall(target_id, call_count)
                self.replyMessage(Message(text=f'𝐒𝐩𝐚𝐦 𝐒𝐮𝐜𝐜𝐞𝐬𝐬 𝐅𝐮𝐥𝐥 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 {call_count} 𝐂𝐚𝐥𝐥'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            except Exception as e:
                print(f"Lỗi: {e}")
                self.replyMessage(Message(text=f'𝐒𝐩𝐚𝐦 𝐒𝐮𝐜𝐜𝐞𝐬𝐬 𝐅𝐮𝐥𝐥 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 {call_count} 𝐂𝐚𝐥𝐥'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Todogr"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split()
                if len(parts) < 5:
                    self.replyMessage(
                        Message(text="</> 𝐔𝐬𝐞 𝐓𝐨𝐝𝐨 𝐈𝐃 𝐆𝐫𝐨𝐮𝐩 𝐈𝐃 𝐔𝐬𝐞𝐫 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 𝐂𝐨𝐮𝐧𝐭"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return
                
                group_id = parts[1]
                target_id = parts[2]
                todo_content = parts[3]
                todo_count = int(parts[4])
                self.replyMessage(Message(text=f'</> 𝐓𝐨𝐝𝐨 𝐆𝐫𝐨𝐮𝐩 𝐒𝐩𝐚𝐦 𝐒𝐞𝐧𝐭 𝐓𝐨 𝐆𝐫𝐨𝐮𝐩 {group_id} 𝐖𝐢𝐭𝐡 𝐔𝐬𝐞𝐫 {target_id} </> 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐂𝐨𝐮𝐧𝐭'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                if self.todo_running:
                    self.replyMessage(
                        Message(text="</> 𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐅𝐨𝐫 𝐒𝐩𝐚𝐦 𝐓𝐨𝐝𝐨"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return

                self.StartTodo1(group_id, target_id, todo_content, mid, author_id, todo_count)
                self.replyMessage(Message(text=f'</> 𝐓𝐨𝐝𝐨 𝐆𝐫𝐨𝐮𝐩 𝐒𝐩𝐚𝐦 𝐄𝐧𝐝𝐞𝐝 𝐒𝐩𝐚𝐦 𝐓𝐨 𝐆𝐫𝐨𝐮𝐩 {group_id} 𝐖𝐢𝐭𝐡 𝐔𝐬𝐞𝐫 {target_id} </> 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐂𝐨𝐮𝐧𝐭 '), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)

            except Exception as e:
                print(f"Lỗi: {e}")
                self.replyMessage(Message(text=f'</> 𝐓𝐨𝐝𝐨 𝐆𝐫𝐨𝐮𝐩 𝐒𝐩𝐚𝐦 𝐄𝐧𝐝𝐞𝐝 𝐒𝐩𝐚𝐦 𝐓𝐨 𝐆𝐫𝐨𝐮𝐩 {group_id} 𝐖𝐢𝐭𝐡 𝐔𝐬𝐞𝐫 {target_id} </> 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐂𝐨𝐮𝐧𝐭 '), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Todo"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            try:
                parts = message.split()
                if len(parts) < 4:
                    self.replyMessage(
                        Message(text="</> 𝐓𝐨𝐝𝐨 𝐈𝐃 𝐔𝐬𝐞𝐫 𝐓𝐞𝐱𝐭 𝐂𝐨𝐮𝐧𝐭"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return

                target_id = parts[1]
                todo_content = parts[2]
                todo_count = int(parts[3])
                self.replyMessage(Message(text=f'</> 𝐒𝐩𝐚𝐦 𝐓𝐨𝐝𝐨 𝐒𝐞𝐧𝐭 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐓𝐨𝐝𝐨'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                if self.todo_running:
                    self.replyMessage(
                        Message(text="</> 𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐅𝐨𝐫 𝐒𝐩𝐚𝐦 𝐓𝐨𝐝𝐨"),
                        message_object, thread_id=thread_id, thread_type=thread_type,
                        ttl=30000
                    )
                    return

                self.StartTodo(target_id, todo_content, mid, author_id, todo_count)
                self.replyMessage(Message(text=f'</> 𝐒𝐩𝐚𝐦 𝐓𝐨𝐝𝐨 𝐄𝐧𝐝𝐞𝐝 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐓𝐨𝐝𝐨'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)

            except Exception as e:
                print(f"Lỗi: {e}")
                self.replyMessage(Message(text=f'</> 𝐒𝐩𝐚𝐦 𝐓𝐨𝐝𝐨 𝐄𝐧𝐝𝐞𝐝 𝐓𝐨 {target_id} 𝐖𝐢𝐭𝐡 𝐂𝐨𝐧𝐭𝐞𝐧𝐭 {todo_content} 𝐀𝐧𝐝 {todo_count} 𝐓𝐨𝐝𝐨'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Info"):
            user_id = None
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            elif content[5:].strip().isnumeric():
                user_id = content[5:].strip()
            else:
                user_id = author_id
            user_info = self.fetchUserInfo(user_id)
            infozalo = self.checkinfo(user_id, user_info)
            self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        elif message.startswith("ReoSp"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return

            if self.reo_spamming:
                  self.replyMessage(Message(text='𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡𝙮 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentions = message_object.mentions
            if not mentions:
                  self.replyMessage(Message(text='🚫 𝙐𝙨𝙚 𝙍𝙚𝙤 @𝙐𝙨𝙚𝙧.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return

            mentioned_user_id = mentions[0]['uid']

            self.reo_spamming = True
            self.reo_spam_thread = threading.Thread(target=self.reo_spam_message, args=(mentioned_user_id, thread_id, thread_type))
            self.reo_spam_thread.start()  
        elif message.startswith("StopR"):
          with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
          if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
          if not self.reo_spamming:
                  self.replyMessage(Message(text='🚫 𝙉𝙤𝙩 𝙎𝙥𝙖𝙢 𝙍𝙚𝙤 𝙍𝙪𝙣𝙣𝙞𝙣𝙜'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                  return
          self.reo_spamming = False
          if self.reo_spam_thread is not None:
            self.reo_spam_thread.join()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Info"):
            user_id = None
            if message_object.mentions:
                user_id = message_object.mentions[0]['uid']
            elif content[5:].strip().isnumeric():
                user_id = content[5:].strip()
            else:
                user_id = author_id
            user_info = self.fetchUserInfo(user_id)
            infozalo = self.checkinfo(user_id, user_info)
            self.replyMessage(Message(text=infozalo, parse_mode="HTML"), message_object, thread_id=thread_id, thread_type=thread_type)
            return
        elif message.startswith("Spamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return
                    self.chayspamvip(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙋𝙡𝙚𝙖𝙨𝙚 𝙄𝙣𝙥𝙪𝙩 𝘿𝙚𝙡𝙖𝙮'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            else:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢𝙫𝙞𝙥 𝙏𝙚𝙭𝙩 𝘿𝙚𝙡𝙖𝙮\n\n𝑺𝒑𝒂𝒎𝒗𝒊𝒑 𝑵𝒈𝒐𝒄 𝑳𝒐𝒗𝒆 𝑽𝒚 𝟓'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("StopSpamvip"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.dungspamvip()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙥𝙖𝙢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Spam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            args = content.split()
            if len(args) >= 3:
                message = " ".join(args[1:-1])
                try:
                    delay = float(args[-1])
                    if delay < 0:
                        self.replyMessage(Message(text='🚫 𝙃𝙤𝙬 𝙏𝙤 𝘿𝙚𝙡𝙖𝙮 ?'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                        return
                    self.chayspam(message, delay, thread_id, thread_type)
                except ValueError:
                    self.replyMessage(Message(text='🚫 𝙋𝙡𝙚𝙖𝙨𝙚 𝙄𝙣𝙥𝙪𝙩 𝘿𝙚𝙡𝙖𝙮'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            else:
                self.replyMessage(Message(text='🚫 𝙐𝙨𝙚:\n𝙎𝙥𝙖𝙢 𝙏𝙚𝙭𝙩 𝘿𝙚𝙡𝙖𝙮\n\n𝑺𝒑𝒂𝒎 𝑵𝒈𝒐𝒄 𝑳𝒐𝒗𝒆 𝑽𝒚 𝟓'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("StopSpam"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.dungspam()
            self.replyMessage(Message(text='𝙎𝙩𝙤𝙥 𝙎𝙥𝙖𝙢 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 !'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
        elif message.startswith("Off"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
                return
            self.replyMessage(Message(text='𝙊𝙛𝙛 ! - 𝙎𝙪𝙘𝙘𝙚𝙨𝙨 𝙁𝙪𝙡𝙡 '), message_object, thread_id=thread_id, thread_type=thread_type, ttl=30000)
            exit()
        elif message.startswith("All"):
            with open('admin.json', 'r') as adminvip:
                adminzalo = json.load(adminvip)
                idadmin = set(adminzalo['idadmin'])
            if author_id not in idadmin:
                self.replyMessage(
                Message(text='𝐵𝑂𝑇 𝑉𝐼𝑃 𝐶𝑂𝐷𝐸𝑅 𝐵𝑌 𝐿𝐼𝐺𝐻𝑇 🕊.'),
                message_object, thread_id=thread_id, thread_type=thread_type,
                ttl=30000
                )
                return
            message_content = message[4:].strip() 
            if not message_content:
                self.replyMessage(
                    Message(text="🚫 𝑷𝒍𝒆𝒂𝒔𝒆 𝑰𝒏𝒑𝒖𝒕 𝑻𝒆𝒙𝒕 𝑭𝒐𝒓 𝑨𝒍𝒍 !"),
                    message_object, thread_id=thread_id, thread_type=thread_type,
                    ttl=30000
                )
                return
            mention = Mention(uid='-1', offset=0, length=len(message_content))
            message_obj = Message(text=message_content, mention=mention)
            self.send(message_obj, thread_id=thread_id, thread_type=thread_type)
    def ThanhVy(self, thread_id, user_id):
        group_info = self.fetchGroupInfo(groupId=thread_id)
        admin_ids = group_info.gridInfoMap[thread_id]['adminIds']
        creator_id = group_info.gridInfoMap[thread_id]['creatorId']
        return user_id in admin_ids or user_id == creator_id
    def spam_message(self, spam_content, thread_id, thread_type):
        """Spam the content from content.txt file in the thread."""
        words = spam_content.split()
        while self.spamming:
            for word in words:
                if not self.spamming:
                    break
                mention = Mention(uid='-1', offset=0, length=len(word))
                spam_message = Message(text=word, mention=mention)
                self.send(spam_message, thread_id=thread_id, thread_type=thread_type)
                time.sleep(0.5)

    def reo_spam_message(self, mentioned_user_id, thread_id, thread_type):
        """Spam mentions of a specific user."""
        while self.reo_spamming:
            mention = Mention(uid=mentioned_user_id, offset=0, length=5)
            spam_message = Message(text="@user 𝑀𝐴𝑌 𝐷𝐴 𝐵𝐼 𝐿𝐼𝐺𝐻𝑇 𝑅𝐸𝑂 𝑁𝐴𝑀𝐸🦅", mention=mention)
            self.send(spam_message, thread_id=thread_id, thread_type=thread_type, ttl=10000)
            time.sleep(0)
    def chayspamvip(self, message, delay, thread_id, thread_type):
        if self.spammingvip:
            self.dungspamvip()
        self.spammingvip = True
        self.spam_threadvip = threading.Thread(target=self.spamtagallvip, args=(message, delay, thread_id, thread_type))
        self.spam_threadvip.start()
    def dungspamvip(self):
        if self.spammingvip:
            self.spammingvip = False
            if self.spam_threadvip is not None:
                self.spam_threadvip.join()
            self.spam_threadvip = None
    def spamtagallvip(self, message, delay, thread_id, thread_type):
        while self.spammingvip:
            try:
                mention = Mention(uid='-1', offset=0, length=0)  # Tạo đối tượng Mention hợp lệ
                message_obj = Message(text=message)
                message_obj.mention = mention
                self.send(message_obj, thread_id=thread_id, thread_type=thread_type, ttl=10000)
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error during spamtagallvip: {e}")
                break
    def chayspam(self, message, delay, thread_id, thread_type):
        if self.spamming:
            self.dungspam()
        self.spamming = True
        self.spam_thread = threading.Thread(target=self.spamtagall, args=(message, delay, thread_id, thread_type))
        self.spam_thread.start()
    def dungspam(self):
        if self.spamming:
            self.spamming = False
            if self.spam_thread is not None:
                self.spam_thread.join()
            self.spam_thread = None
    def spamtagall(self, message, delay, thread_id, thread_type):
        while self.spamming:
            try:
                logging.debug(f"Sending message: {message}, thread_id: {thread_id}, thread_type: {thread_type}")
                message_obj = Message(text=message)
                self.send(message_obj, thread_id=thread_id, thread_type=thread_type, ttl=10000)
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error during spamtagall: {e}")
                break
    def checkinfo(self, user_id, user_info):
        if 'changed_profiles' in user_info and user_id in user_info['changed_profiles']:
            profile = user_info['changed_profiles'][user_id]
            infozalo = f'''
> ┌────★ 𝐿𝐼𝐺𝐻𝑇 ★───────
> ├> <b>𝙉𝙖𝙢𝙚: </b> {profile.get('displayName', '')}
> ├> <b>𝙄𝘿: </b> {profile.get('userId', '')}
> └─────────────────────
            '''
            return infozalo
        else:
            return "Bruhh"             
client = ThanhNgocDzYeuThanhVy(
    '</>', '</>',
    imei="b03d7492-c38d-4fe6-b5d4-a9c1285fff11-7675d59b5e84e0a878ee6f0a97f9056f",
    user_agent="Mozilla/5.0 (Linux; Android 11; CPH2239 Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.105 Mobile Safari/537.36 GoogleApp/15.49.42.ve.arm64",
    session_cookies={"_ga":"GA1.2.1782749144.1735464586","zpsid":"INmX.421600670.6.kR0G7BeTvrSa0CPEjXtdLyzkbME8BD5dYYlGPn7w-6zNPJptkuVn9jqTvrS","zpw_sek":"udus.421600670.a0.XSDCViCEdbXT4xz1uWwUMBWi-pFXDBnXXt_fAfDUpnIKGF0vgcZDDezVsXs2CwDwlgLvH_lZveDZ3m9EiccUM0","__zi":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","__zi-legacy":"3000.SSZzejyD2DyiZwEqqGn1pJ75lh39JHN1E8Yy_zm36zbxrAxraayVspUUglULJX-NC9wfkPL9598sdwIsDG.1","ozi":"2000.UelfvS0R1PqpcVIltHyTt6UL_Rp0HqkNRP3zly55JDzabVhnmK97scAKz_ur.1","app.event.zalo.me":"2456638497330600094","_zlang":"vn","zoaw_sek":"vzo8.350505344.2.vAx6OtKZA6drQinzTICeQNKZA6br8oXfT2te6X8ZA6a","zoaw_type":"0"})
client.listen()