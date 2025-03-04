from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import os
from config import *

bot = Client(
    "TeraboxBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

START_MSG = """
💥 Hello {mention}  
Welcome to **Terabox Downloader Bot**  
Send any **Terabox Link** to download files 🚀

🔗 Example:
https://terabox.com/s/abcdef123456
"""

@bot.on_message(filters.command("start"))
async def start(client, message):
    buttons = [[InlineKeyboardButton("🔥 Join Channel", url=f"https://t.me/{FORCE_SUB}")]]
    await message.reply_text(
        START_MSG.format(mention=message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@bot.on_message(filters.regex("https://terabox.com/s/") & filters.private)
async def downloader(client, message):
    user = message.from_user.id

    # Force Subscribe Check
    try:
        member = await client.get_chat_member(f"@{FORCE_SUB}", user)
        if member.status not in ["member", "administrator", "creator"]:
            buttons = [[InlineKeyboardButton("🔥 Join Channel", url=f"https://t.me/{FORCE_SUB}")]]
            return await message.reply_text(
                "**🔒 First Join Our Channel To Use This Bot**",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    except:
        return await message.reply_text("Invalid Channel Username")

    link = message.text
    await message.reply_text("🔍 Processing your link... Please wait")

    url = f"{API_URL}{link}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            if "link" in data:
                file_name = data["file_name"]
                download_link = data["link"]
                thumb = data["thumb"]
                size = data["size"]

                await client.send_document(
                    message.chat.id,
                    document=download_link,
                    thumb=thumb,
                    caption=f"**📄 File Name:** `{file_name}`\n**📦 Size:** `{size}`\n\nPowered by @studybuddy",
                    progress=lambda current, total: message.edit_text(f"Uploading... {current * 100 / total:.1f}%")
                )

            else:
                await message.reply_text("❌ Invalid Terabox Link")
                
bot.run()
