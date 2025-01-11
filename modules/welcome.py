import time
import os
import json
import requests
from zlapi import ZaloAPI, ZaloAPIException
from zlapi.models import *
from threading import Thread
from datetime import datetime

# General description and version information
des = {
    'version': "1.0.3",
    'credits': "Thịnh",
    'description': "làm cc j"
}

# Function to handle welcome messages and member departure notifications
def welcome(self, event_data, event_type):
    def send():
        if event_type == GroupEventType.UNKNOWN:
            return

        print(event_data)
        current_time = datetime.now()
        formatted_time = current_time.strftime("%d/%m/%Y [%H:%M:%S]")

        thread_id = event_data.get('groupId')
        if not thread_id:
            print("Lỗi: Không tìm thấy 'groupId' trong event_data")
            return

        # Fetch group information to get the total number of members
        group_info = self.fetchGroupInfo(thread_id)
        total_members = group_info.get('gridInfoMap', {}).get(thread_id, {}).get('totalMember', 0)

        # Check if total_members is an integer
        if not isinstance(total_members, int):
            print("Lỗi: total_members không phải là số nguyên.")
            return

        # Handle the JOIN event
        if event_type == GroupEventType.JOIN:
            group_name = event_data.get('groupName', "nhóm")
            for member in event_data.get('updateMembers', []):
                member_id = member.get('id')
                member_name = member.get('dName')
                avatar_url = member.get('avatar')

                # Construct welcome message
                text_lines = [
                    '[ PROJECT NOTIFICATION GROUP ]',
                    f'> Chào mừng: @{member_name}',
                    f'> Bạn là thành viên thứ: {total_members}',
                    f'> Đã tham gia nhóm: {group_name}.'
                ]

                colors = ["#f00e0e", "#f8f700", "#09f926", "#233ee6", "#46d0e5", "#9b23e6", "#f91be4", "#fe1e1e", "#da2df2", "#fbfbfb"]
                color_styles = []
                start_idx = 0
                for j, line in enumerate(text_lines):
                    color = colors[j % len(colors)]
                    color_style = MessageStyle(
                        style="color",
                        color=color,
                        offset=start_idx,
                        length=len(line),
                        auto_format=False
                    )
                    color_styles.append(color_style)
                    start_idx += len(line) + 1

                # Font style
                font_style = MessageStyle(
                    style="font",
                    size="14",
                    offset=0,
                    length=len('\n'.join(text_lines)),
                    auto_format=False
                )

                # Send the welcome message
                msg = Message(text='\n'.join(text_lines), style=MultiMsgStyle(color_styles + [font_style]))
                try:
                    self.send(msg, thread_id, ThreadType.GROUP, ttl=3000000)
                except Exception as e:
                    print(f"Lỗi khi gửi tin nhắn: {e}")

                # Send a business card if member_id and avatar_url are available
                if member_id and avatar_url:
                    try:
                        self.sendBusinessCard(userId=member_id, qrCodeUrl=avatar_url, thread_id=thread_id, thread_type=ThreadType.GROUP, ttl=3000000)
                    except Exception as e:
                        print(f"Lỗi khi gửi thẻ doanh nghiệp: {e}")

        # Handle LEAVE and REMOVE_MEMBER events
        elif event_type in {GroupEventType.LEAVE, GroupEventType.REMOVE_MEMBER}:
            group_name = event_data.get('groupName', "nhóm")
            member_info = event_data.get('updateMembers', [{}])[0]
            member_name = member_info.get('dName', "thành viên")
            member_id = member_info.get('id')
            avatar_url = member_info.get('avatar')

            # Construct departure message
            text_lines = [
                '[ MITAI PROJECT NOTIFICATION GROUP ]',
                f'> {member_name} đã rời khỏi nhóm' if event_type == GroupEventType.LEAVE else f'> {member_name} bị xoá khỏi nhóm',
                f'> Nhóm: {group_name}',
                f'> Vào lúc: {formatted_time}',
                f'> Tổng thành viên còn lại: {total_members}'
            ]

            colors = ["#f00e0e", "#f8f700", "#ffffff", "#09f926", "#233ee6", "#9b23e6", "#f91be4", "#fe1e1e", "#da2df2", "#46d0e5"]
            color_styles = []
            start_idx = 0
            for j, line in enumerate(text_lines):
                color = colors[j % len(colors)]
                color_style = MessageStyle(
                    style="color",
                    color=color,
                    offset=start_idx,
                    length=len(line),
                    auto_format=False
                )
                color_styles.append(color_style)
                start_idx += len(line) + 1

            # Font style
            font_style = MessageStyle(
                style="font",
                size="14",
                offset=0,
                length=len('\n'.join(text_lines)),
                auto_format=False
            )

            # Send the departure message
            msg = Message(text='\n'.join(text_lines), style=MultiMsgStyle(color_styles + [font_style]))
            try:
                self.send(msg, thread_id, ThreadType.GROUP, ttl=3000000)
            except Exception as e:
                print(f"Lỗi khi gửi tin nhắn: {e}")

            # Send a business card if member_id and avatar_url are available
            if member_id and avatar_url:
                try:
                    self.sendBusinessCard(userId=member_id, qrCodeUrl=avatar_url, thread_id=thread_id, thread_type=ThreadType.GROUP, ttl=3000000)
                except Exception as e:
                    print(f"Lỗi khi gửi thẻ doanh nghiệp: {e}")

    # Start the send function in a new thread
    thread = Thread(target=send)
    thread.start()

# Function to get event handlers
def get_szl():
    return {
        'welcome': welcome  
    }