import json
import subprocess
import requests
import re
from io import BytesIO
from urllib.parse import parse_qs, urlparse

import asyncio
import math
import os
import shlex
from pyrogram.errors.exceptions import InviteHashExpired , ChannelPrivate ,GroupcallForbidden
from typing import Tuple
from pytgcalls import idle, PyTgCalls
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
from PIL import Image
from pymediainfo import MediaInfo
from pyrogram.types import Message
import time
from pytgcalls.exceptions import NotInCallError
from pytgcalls.types import ChatUpdate, StreamEnded



from pytgcalls.exceptions import (
    NoActiveGroupCall,
)
import os
from asyncio import sleep
import os
import sys
from re import sub
from fonts import *
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time
import asyncio
from config import *
from pyrogram import Client, filters
import gc
import time

from pyrogram.errors import (
    FloodWait,
    RPCError,
)

# Replace with your actual API ID and API hash from my.telegram.org                     
async def handle_disconnect(client, retries=5, delay=5):
    """Handles disconnects by attempting to reconnect with retries."""
    for attempt in range(retries):
        try:
            print(f"Attempting to reconnect (attempt {attempt + 1}/{retries})...")
            await client.connect()
            if client.is_connected:
                print("Successfully reconnected.")
                break  # Exit the loop if reconnected successfully
        except FloodWait as e:
            print(f"Floodwait encountered, waiting {e.value} seconds")
            await asyncio.sleep(e.value)
        except RPCError as e:
             print(f"RPC Error, not retrying: {e}")
             break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    else:
        print(f"Failed to reconnect after {retries} attempts.")


import os
import shutil

def clear_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return
    
    # Check if the path is actually a directory
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a directory.")
        return
    
    # List all files and directories in the given directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                # Remove file or symbolic link
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                # Remove directory and all its contents
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
    
    print(f"Directory {directory_path} has been cleared.")

import asyncio
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
import re

def extract_video_id(url):
    """
    Extract YouTube video ID from various forms of YouTube URLs.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Video ID or None if not found
    """
    try:
        # Patterns for different types of YouTube URLs
        patterns = [
            r'(?:v=|/v/|youtu\.be/|/embed/)([^&?/]+)',  # Standard, shortened and embed URLs
            r'(?:watch\?|/v/|youtu\.be/)([^&?/]+)',     # Watch URLs
            r'(?:youtube\.com/|youtu\.be/)([^&?/]+)'    # Channel URLs
        ]
        
        # Try each pattern
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        return None
        
    except Exception as e:
        return f"Error extracting video ID: {str(e)}"


def format_number(num):
    """Format number to international system (K, M, B)"""
    if num is None:
        return "N/A"
    
    if num < 1000:
        return str(num)
    
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    
    # Add precision based on magnitude
    if magnitude > 0:
        num = round(num, 1)
        if num.is_integer():
            num = int(num)
    
    return f"{num:g}{'KMB'[magnitude-1]}"

import yt_dlp
import datetime

def parse_and_format_date(date_str):
    """
    Parse and format date string
    
    Args:
        date_str (str): Date string to parse
    
    Returns:
        str: Formatted date or 'N/A'
    """
    if not date_str:
        return 'N/A'
    
    try:
        # Try different date formats
        date_formats = [
            '%Y%m%d',  # YouTube format
            '%Y-%m-%d',  # ISO format
            '%d/%m/%Y',  # DD/MM/YYYY
            '%m/%d/%Y',  # MM/DD/YYYY
        ]
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.datetime.strptime(date_str, date_format)
                return parsed_date.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        return 'N/A'
    except Exception:
        return 'N/A'

def get_video_details(video_id):
    """
    Get video details using yt_dlp
    
    Args:
        video_id (str): Video ID to fetch details for
    
    Returns:
        dict: Video details or error message
    """
    # Try YouTube first
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'cookiesfrombrowser': ('chrome',)
        }

        # Try YouTube URL first
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract initial info
            info = ydl.extract_info(youtube_url, download=False)

            # Process upload date
            upload_date = parse_and_format_date(info.get('upload_date'))

            # Process duration
            duration = 'N/A'
            if info.get('duration'):
                try:
                    duration = str(
                        datetime.datetime.fromtimestamp(
                            info.get('duration')
                        ).strftime('%H:%M:%S')
                    )
                except (ValueError, TypeError):
                    duration = 'N/A'

            # Prepare details dictionary
            details = {
                'title': info.get('title', 'N/A'),
                'thumbnail': info.get('thumbnail', 'N/A'),
                'duration': duration,
                'view_count': info.get('view_count', 'N/A'),
                'like_count': info.get('like_count', 'N/A'),
                'channel_name': info.get('uploader', 'N/A'),
                'subscriber_count': info.get('channel_follower_count', 'N/A'),
                'upload_date': upload_date,
                'video_url': youtube_url,
                'platform': 'YouTube'
            }

            return details

    except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError) as youtube_error:
        # If YouTube extraction fails, try Instagram
        try:
            # Construct Instagram Reel URL
            instagram_url = f"https://www.instagram.com/reel/{video_id}/"
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'cookiesfrombrowser': ('chrome',)
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract Instagram Reel info
                info = ydl.extract_info(instagram_url, download=False)

                # Process upload date
                upload_date = parse_and_format_date(info.get('upload_date'))

                # Process duration
                duration = 'N/A'
                if info.get('duration'):
                    try:
                        duration = str(
                            datetime.datetime.fromtimestamp(
                                info.get('duration')
                            ).strftime('%H:%M:%S')
                        )
                    except (ValueError, TypeError):
                        duration = 'N/A'

                # Prepare Instagram details
                details = {
                    'title': info.get('title', 'N/A'),
                    'thumbnail': info.get('thumbnail', 'N/A'),
                    'duration': duration,
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'channel_name': info.get('uploader', 'N/A'),
                    'subscriber_count': 0,
                    'upload_date': upload_date,
                    'video_url': instagram_url,
                    'platform': 'Instagram'
                }

                return details

        except Exception as instagram_error:
            # If both fail, return error details
            return {
                'error': f"Extraction failed for both YouTube and Instagram. Original error: {youtube_error}"
            }

import datetime
import os
import magic

def is_streamable(file_path):
    """
    Check if a file is potentially streamable.
    
    Args:
        file_path (str): Path to the file to be checked
    
    Returns:
        bool: True if file is potentially streamable, False otherwise
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False

    # Supported streamable file extensions
    STREAMABLE_EXTENSIONS = {
        'video': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                  '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'},
        'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', 
                  '.wma', '.m4a', '.opus'}
    }

    try:
        # Get file extension
        file_extension = os.path.splitext(file_path)[1].lower()

        # Use python-magic for MIME type detection
        mime = magic.Magic(mime=True)
        detected_mime_type = mime.from_file(file_path)
        
        # Check streamability based on MIME type and extension
        is_video_mime = detected_mime_type.startswith('video/')
        is_audio_mime = detected_mime_type.startswith('audio/')
        
        is_video_ext = file_extension in STREAMABLE_EXTENSIONS['video']
        is_audio_ext = file_extension in STREAMABLE_EXTENSIONS['audio']

        # Return True if any streaming condition is met
        return is_video_mime or is_audio_mime or is_video_ext or is_audio_ext

    except Exception:
        return False

# Example usage
import psutil
import os
async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
      return ""
    return " ".join(split[1:])



async def is_active_chat(chat_id):
    if chat_id not in active:
        return False
    else:
        return True

async def add_active_chat(chat_id):
    if chat_id not in active:
         active.append(chat_id)


async def remove_active_chat(chat_id):
    if chat_id in active:
        active.remove(chat_id)
    chat_dir = f"{ggg}/user_{clients["bot"].me.id}/{chat_id}"
    os.makedirs(chat_dir, exist_ok=True)
    clear_directory(chat_dir)


async def autoleave_vc(message, duration_str,chat):
    """
    Automatically leave voice chat when only the bot remains in the call for 5 seconds
    """
    
    while True:
        try:
            # Track if song duration changes
            if chat.id in playing and playing[chat.id]:
                current_song = playing[chat.id]
                if str(current_song['duration']) != str(duration_str):
                    break
        except Exception:
            pass

        try:
            # Get current call members
            members = []
            async for member in clients["session"].get_call_members(chat.id):
                members.append(member)

            # Check if only bot remains in call
            if len(members) == 1 and members[0].chat.id == clients["session"].me.id:
                # Confirm persistent presence check
                await asyncio.sleep(25)
                
                # Recheck after cooldown
                members = []
                async for member in clients["session"].get_call_members(chat.id):
                    members.append(member)

                # Final verification before leaving
                if len(members) == 1 and members[0].chat.id == clients["session"].me.id:
                    await clients["call_py"].leave_call(chat.id)
                    # Cleanup operations
                    try:
                        queues[chat.id].clear()
                        playing[chat.id].clear()
                    except KeyError:
                        pass
                    
                    await remove_active_chat(chat.id)
                    await clients["bot"].send_message(
                        message.chat.id,
                        "⚠️ Nᴏ ᴀᴄᴛɪᴠᴇ ʟɪsᴛᴇɴᴇʀs ᴅᴇᴛᴇᴄᴛᴇᴅ. Lᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ."
                    )
                    await remove_active_chat(chat.id)
                    break

        except Exception as e:
            print(f"Autoleave error: {e}")
            break

        # Reduced check interval
        await asyncio.sleep(8)

async def pautoleave_vc(message, duration_str):
    """
    Automatically leave voice chat when members count is <= 1 for 5 seconds
    
    :param user_client: User client to get call members and send messages
    :param call_py: PyTgCalls client for leaving call
    :param message: Message object containing chat information
    :param playing: Dictionary tracking currently playing songs
    :param duration_str: Current song duration
    """
    while True:
        try:
            # Check if current song duration changed
            if message.chat.id in playing and playing[message.chat.id]:
                current_song = playing[message.chat.id]
                if str(current_song['duration']) != str(duration_str):
                    break
        except Exception:
            pass

        # Get current call members
        members = []
        try:
          async for i in clients["session"].get_call_members(message.chat.id):
            members.append(i)
        except:
           break
        # Check if members count is <= 1
        if len(members) <= 1:
            # Wait 5 seconds to confirm
            await asyncio.sleep(5)
            
            # Recheck members count after 5 seconds
            members = []
            async for i in clients["session"].get_call_members(message.chat.id):
                members.append(i)
            
            # If still <= 1 member, leave the voice chat
            if len(members) <= 1:
                await clients["call_py"].leave_call(message.chat.id)
                # Send message about leaving
                try:
                    queues[message.chat.id].clear()
                except:
                   pass
                try:
                    playing[message.chat.id].clear()
                except:
                   pass
                await remove_active_chat(message.chat.id)
                await clients["bot"].send_message(
                    message.chat.id, 
                    f"ɴᴏ ᴏɴᴇ ɪꜱ ʟɪꜱᴛᴇɴɪɴɢ ᴛᴏ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ, ꜱᴏ ᴛʜᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ ʟᴇꜰᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ."
                )
                break
        
        # Wait before next check
        await asyncio.sleep(10)


async def update_progress_button(message, duration_str,chat):
    try:
        total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_str.split(":"))))

        while True:
            try:
                updated_msg = await clients["call_py"]._mtproto.get_messages(message.chat.id,message.id)
            except:
                break
            try:
                # Fetch elapsed seconds
                elapsed_seconds = int(await clients["call_py"].time(chat.id))
            except Exception as e:
                # If an exception occurs, the song has ended
                break
            try:
               if chat.id in playing and playing[chat.id]:
                   current_song = playing[chat.id]
                   if str(current_song['duration']) != str(duration_str):
                       break            # Format elapsed time
            except Exception as e:
                pass
            elapsed_str = time.strftime('%M:%S', time.gmtime(int(time.time() - played[chat.id])))
            elapsed_seconds = int(time.time() - played[chat.id])
            # Calculate progress bar (6 `─` with spaces)
            progress_length = 8
            position = min(int((elapsed_seconds / total_seconds) * progress_length), progress_length)
            progress_bar = "─ " * position + "▷" + "─ " * (progress_length - position - 1)
            progress_bar = progress_bar.strip()  # Remove trailing spaces

            progress_text = f"{elapsed_str} {progress_bar} {duration_str}"

            # Insert progress bar between the first and last rows
            keyboard = message.reply_markup.inline_keyboard
            progress_row = [InlineKeyboardButton(text=progress_text, callback_data="ignore")]
            updated_keyboard = keyboard[:1] + [progress_row] + keyboard[1:]

            await message.edit_reply_markup(InlineKeyboardMarkup(updated_keyboard))
            await asyncio.sleep(9)
    except Exception as e:
        print(f"Progress update error: {e}")


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

queue_styles = {
    1: """🌈 𝗤𝗨𝗘𝗨𝗘 𝗔𝗗𝗗𝗘𝗗 »✨
┏━━━━━━━━━━━━
┣ 𝗠𝗼𝗱𝗲 » {}
┣ 𝗧𝗶𝘁𝗹𝗲 » {}
┣ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 » {}
┗ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 » #{}""",

    2: """✧･ﾟ 𝓐𝓭𝓭𝓮𝓭 𝓣𝓸 𝓠𝓾𝓮𝓾𝓮 ･ﾟ✧
━━━━━━━━━━━━
♪ 𝓜𝓸𝓭𝓮 » {}
♪ 𝓣𝓲𝓽𝓵𝓮 » {}
♪ 𝓛𝓮𝓷𝓰𝓽𝓱 » {}
♪ 𝓟𝓸𝓼𝓲𝓽𝓲𝓸𝓷 » #{}""",

    3: """⋆｡°✩ 𝐒𝐨𝐧𝐠 𝐐𝐮𝐞𝐮𝐞𝐝 ✩°｡⋆
┏━━━━━━━━━━━
┣ 𝐌𝐨𝐝𝐞 » {}
┣ 𝐓𝐫𝐚𝐜𝐤 » {}
┣ 𝐓𝐢𝐦𝐞 » {}
┗ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 » #{}""",

    4: """⚡ 𝕋𝕣𝕒𝕔𝕜 𝔸𝕕𝕕𝕖𝕕 𝕥𝕠 ℚ𝕦𝕖𝕦𝕖 ⚡
╔═══════════
║ 𝕄𝕠𝕕𝕖: {}
║ 𝕋𝕚𝕥𝕝𝕖: {}
║ 𝔻𝕦𝕣𝕒𝕥𝕚𝕠𝕟: {}
╚ ℙ𝕠𝕤𝕚𝕥𝕚𝕠𝕟: #{}""",

    5: """• ғᴜᴛᴜʀᴇ ᴛʀᴀᴄᴋ •
────────────
⟡ ᴍᴏᴅᴇ: {}
⟡ ᴛɪᴛʟᴇ: {}
⟡ ʟᴇɴɢᴛʜ: {}
⟡ ᴘᴏꜱɪᴛɪᴏɴ: #{}""",

    6: """
