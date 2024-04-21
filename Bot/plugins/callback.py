import logging
from pyrogram import filters
from pyrogram.errors import ButtonUrlInvalid
from pyromod import Client, Message
from pyromod.exceptions import ListenerTimeout
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Bot import TGBot

@TGBot.on_callback_query(filters.regex(pattern="^add_r_\d+"))
async def add_row_handler(bot: Client, update: CallbackQuery):
    print(type(update.message))
    logging.info(update.data)
    data=update.data.split("_")
    row=int(data[2])
    button:list=update.message.reply_markup.inline_keyboard
    button.pop()
    button.append([InlineKeyboardButton("Add Column", f"add_c_{row}_0")])
    await update.edit_message_reply_markup(InlineKeyboardMarkup(button))

@TGBot.on_callback_query(filters.regex(pattern="^add_c_\d+_\d+"))
async def add_row_handler(bot: Client, update: CallbackQuery):
    logging.info(update.data)
    data=update.data.split("_")
    row_no=int(data[2])
    col_no=int(data[3])
    button:list=update.message.reply_markup.inline_keyboard
    row: list=button[row_no]
    row.pop()
    try:
        msg1=(await update.message.reply_text("Send the name that will appear on the button\nWait Time: 2 minute")).id
        btn_name = await update.message.chat.listen(filters=filters.text, timeout=120)
        msg2=(await update.message.reply_text("Send the url for the button\nWait Time: 2 minute")).id
        btn_url = await update.message.chat.listen(filters=filters.text, timeout=120)
        await bot.delete_messages(update.from_user.id, [msg1, btn_name.id, msg2, btn_url.id])
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')

    row.append(InlineKeyboardButton(btn_name.text, url=btn_url.text))
    if len(row) < 8:
        row.append(InlineKeyboardButton("Add Column", f"add_c_{row_no}_{col_no+1}"))
    button[row_no]=row
    if len(row)>1 and not button[-1][0].callback_data:
        button.append([InlineKeyboardButton("Add Row", f"add_r_{len(button)}")])
    try:
        await update.edit_message_reply_markup(InlineKeyboardMarkup(button))
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please add button again with valid URL")