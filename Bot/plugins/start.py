from pprint import pprint
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Bot import TGBot


@TGBot.on_message(filters.private & filters.command("start"))
async def start_handler(bot: Client, message: Message):
    await message.reply_text(f"""Hi {message.from_user.mention}
I am Button Maker Bot I can help you to create Button with URL
Join Our Channel @SpringsFern for News about our bot
Join Our Discussion Group @AWeirdString to ask commnon doubts you have or report any issue your facing
                             
send /help for more help
""")


@TGBot.on_message(filters.private & filters.command("create"))
async def create_handler(bot: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Please Reply to a Message or Media")
    await message.reply_to_message.copy(message.chat.id, reply_markup=InlineKeyboardMarkup(
        [[InlineKeyboardButton("Add Column", "add_c_0_0")]]
    ))

@TGBot.on_message(filters.private & filters.command("done") & filters.reply)
async def done_handler(bot: Client, message: Message):
    if not message.reply_to_message.reply_markup:
        return await message.reply_text("Couldn't find Inline Keyboard")

    buttons: list = []
    for row in message.reply_to_message.reply_markup.inline_keyboard:
        button_row=[]
        for col in row:
            if col.url:
                button_row.append(col)
        buttons.append(button_row)
    if buttons:
        await message.reply_to_message.copy(message.chat.id, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text("Couldn't find button with url in reply message")

@TGBot.on_message(filters.private & filters.command("rmbtn") & filters.reply)
async def rmbtn_handler(bot: Client, message: Message):
    if not message.reply_to_message.reply_markup:
        return await message.reply_text("Couldn't find Inline Keyboard")

    usr_cmd=message.text.split()
    if len(usr_cmd)<3 or (not usr_cmd[1].isdigit()) or (not usr_cmd[2].isdigit()):
        await message.reply_text("Invalid usage\nPlease send /rmbtn command and read the message to know hot to use this command")
    
    row_no=int(usr_cmd[1])
    col_no=int(usr_cmd[2])
    buttons:list=message.reply_to_message.reply_markup.inline_keyboard

    if len(buttons)>=row_no:
        if len(buttons[row_no-1])>=col_no:
            if buttons[row_no-1][col_no-1].callback_data:
                return await message.reply_text("Can't Removed Callback Button please select different button")
            buttons[row_no-1].pop(col_no-1)
        else:
            return await message.reply_text("Invalid Column Position")
    else:
        return await message.reply_text("Invalid Row Position")
    if buttons:
        if col_no==8:
            buttons[row_no-1].append(InlineKeyboardButton("Add Column", f"add_c_{row_no-1}_7"))
        else:
            buttons[row_no-1].pop()
            buttons[row_no-1].append(InlineKeyboardButton(f"Add Column", f"add_c_{row_no-1}_{len(buttons[row_no-1])}"))
        await message.reply_to_message.copy(message.chat.id, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text("Couldn't find button with url in reply message")