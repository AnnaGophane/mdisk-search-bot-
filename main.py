# (c) @Xxxxxxxxxxxxxxx_x_xxxxxxxxxx_x

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from TeamTeleRoid.forcesub import ForceSub

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):

    await event.reply_text(Config.START_MSG.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/Suryabali_4_Hindi_Movies"),
             InlineKeyboardButton("Our Group", url="https://t.me/Drishyam_2_Hindi_Movies")],
            [InlineKeyboardButton("Help", callback_data="Help_msg"),
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

@Bot.on_message(filters.private & filters.command("help"))
async def help_handler(_, event: Message):

    await event.reply_text(Config.ABOUT_HELP_TEXT.format(event.from_user.mention),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Our Channel", url="https://t.me/Suryabali_4_Hindi_Movies"),
             InlineKeyboardButton("Our Group", url="https://t.me/Drishyam_2_Hindi_Movies"), 
             InlineKeyboardButton("About", callback_data="About_msg")]
        ])
    )

@Bot.on_message(filters.incoming)
async def inline_handlers(_, event: Message):
    if event.text == '/start':
        return
    answers = f'**📂 Results For ➠ {event.text} \n\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n➠ Please Type Correct Spelling.✍️\n➠ Add Year For Better Result.🗓️\n▰▱▰▱▰▱▰▱▰▱▰▱▰▱\n\n**'
    async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.text):
        if message.text:
            thumb = None
            f_text = message.text
            msg_text = message.text.html
            if "|||" in message.text:
                f_text = message.text.split("|||", 1)[0]
                msg_text = message.text.html.split("|||", 1)[0]
            answers += f'**🍿 Title ➠ ' + '' + f_text.split("\n", 1)[0] + '' + '\n\n📜 About ➠ ' + '' + f_text.split("\n", 2)[-1] + ' \n\n**'
    try:
        await event.reply_text(
            answers
        )
        print(f"[{Config.BOT_SESSION_NAME}] - Answered Successfully - {event.from_user.first_name}")
        await asyncio.sleep(30)
        await msg.delete()
    except:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")


@Bot.on_callback_query()
async def button(bot, cmd: CallbackQuery):
        cb_data = cmd.data
        if "About_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_BOT_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("Our Channel", url="https://t.me/Suryabali_4_Hindi_Movies"),
						InlineKeyboardButton("Our Group", url="https://t.me/Drishyam_2_Hindi_Movies")
					],
					[
						InlineKeyboardButton("Developer", url="https://t.me/Xxxxxxxxxxxxxxx_x_xxxxxxxxxx_x"),
						InlineKeyboardButton("Home", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "Help_msg" in cb_data:
            await cmd.message.edit(
			text=Config.ABOUT_HELP_TEXT,
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
					[
						InlineKeyboardButton("About", callback_data="About_msg"),
						InlineKeyboardButton("Our Channel", url="https://t.me/Suryabali_4_Hindi_Movies")
					], 
                                        [
						InlineKeyboardButton("Owner", url="https://t.me/Xxxxxxxxxxxxxxx_x_xxxxxxxxxx_x"),
						InlineKeyboardButton("Home", callback_data="gohome")
					]
				]
			),
			parse_mode="html"
		)
        elif "gohome" in cb_data:
            await cmd.message.edit(
			text=Config.START_MSG.format(cmd.from_user.mention),
			disable_web_page_preview=True,
			reply_markup=InlineKeyboardMarkup(
				[
                                        [
						InlineKeyboardButton("Help", callback_data="Help_msg"),
						InlineKeyboardButton("About", callback_data="About_msg")
					],
					[
						InlineKeyboardButton("Support", url="https://t.me/Xxxxxxxxxxxxxxx_x_xxxxxxxxxx_x"),
						InlineKeyboardButton("Channel", url="https://t.me/Suryabali_4_Hindi_Movies")
					]
				]
			),
			parse_mode="html"
		)

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
