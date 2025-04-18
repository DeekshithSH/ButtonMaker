from typing import Union
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from pyrogram.errors import ButtonUrlInvalid, MessageNotModified
from pyrogram.enums import ParseMode
from pyrogram.enums.message_media_type import MessageMediaType
from pyromod import Message
from pyromod.exceptions import ListenerTimeout
from Bot import TGBot
from Bot.utils import database as db
from Bot.vars import Var

supported_media=[MessageMediaType.ANIMATION, MessageMediaType.AUDIO, MessageMediaType.DOCUMENT, MessageMediaType.PHOTO, MessageMediaType.STICKER, MessageMediaType.VIDEO, MessageMediaType.VOICE]


@TGBot.on_message(filters.private & (filters.command("create") | filters.media))
async def control_handler(bot: Client, message: Message):
    msg=None
    if message.reply_to_message:
        if message.reply_to_message.text or message.reply_to_message.media in supported_media:
            msg = await message.reply_to_message.copy(message.chat.id)
    else:
        if message.media in supported_media:
            msg = await message.copy(message.chat.id)
        else:
            msg = await message.reply_text("Click On Edit Message Text to change this text\nIf you want buttons for media send/forward the media or reply to to the media with /create\nSupported media are\n```\nANIMATION\nAUDIO\nDOCUMENT\nPHOTO\nSTICKER\nVIDEO\nVOICE\n```")
    if not msg:
        return message.reply_text("Media Type does not support Inline Keyboard")
    await message.reply_text(
        "Controler\nButton Position will be showen here after adding buttons",
        quote=True,
        reply_to_message_id=msg.id,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("↑", "ctrl_up")],
            [InlineKeyboardButton("←", "ctrl_left"), InlineKeyboardButton("Button Name", "0_0"), InlineKeyboardButton("→", "ctrl_right")],
            [InlineKeyboardButton("↓", "ctrl_down")],
            [InlineKeyboardButton("Add Button Left", "ctrl_add_left"), InlineKeyboardButton("Add Button Right", "ctrl_add_right")],
            [InlineKeyboardButton("Add Button Above", "ctrl_add_above"), InlineKeyboardButton("Add Button Below", "ctrl_add_below")],
            [InlineKeyboardButton("Edit Button Text", "ctrl_edit_text"), InlineKeyboardButton("Edit Button URL", "ctrl_edit_url")],
            [InlineKeyboardButton("Edit Message Text", "ctrl_edit_message"), InlineKeyboardButton("save", "ctrl_save")],
            [InlineKeyboardButton("Remove Button", "ctrl_delete"), InlineKeyboardButton(" ", " ")]
        ]))


@TGBot.on_callback_query(filters.regex(pattern="ctrl_up"))
async def ctrl_up_handler(bot: Client, update: CallbackQuery):
    markup=(await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)).reply_markup
    if not markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)

    row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
    if row_no<1:
        return await update.answer(text="already selected top most button")

    if len(markup.inline_keyboard[row_no-1])<=col_no:
        col_no=len(markup.inline_keyboard[row_no-1])-1
    update.message.reply_markup.inline_keyboard[1][1].callback_data=f"{row_no-1}_{col_no}"
    update.message.reply_markup.inline_keyboard[1][1].text=markup.inline_keyboard[row_no-1][col_no].text
    await update.edit_message_text(gen_pos_text(row_no-1, col_no, len(markup.inline_keyboard)),
        reply_markup=InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))

@TGBot.on_callback_query(filters.regex(pattern="ctrl_left"))
async def ctrl_left_handler(bot: Client, update: CallbackQuery):
    markup=(await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)).reply_markup
    if not markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
    if col_no<1:
        return await update.answer(text="already selected left most button")
    update.message.reply_markup.inline_keyboard[1][1].callback_data=f"{row_no}_{col_no-1}"
    update.message.reply_markup.inline_keyboard[1][1].text=markup.inline_keyboard[row_no][col_no-1].text
    await update.edit_message_text(gen_pos_text(row_no, col_no-1, len(markup.inline_keyboard)),
        reply_markup=InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))

@TGBot.on_callback_query(filters.regex(pattern="ctrl_right"))
async def ctrl_right_handler(bot: Client, update: CallbackQuery):
    markup=(await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)).reply_markup
    if not markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    buttons=update.message.reply_markup.inline_keyboard
    row_no, col_no=[int(x) for x in buttons[1][1].callback_data.split("_")]

    if col_no>=len(markup.inline_keyboard[row_no])-1:
        return await update.answer(text="already selected right most button")
    update.message.reply_markup.inline_keyboard[1][1].callback_data=f"{row_no}_{col_no+1}"
    update.message.reply_markup.inline_keyboard[1][1].text=markup.inline_keyboard[row_no][col_no+1].text
    await update.edit_message_text(gen_pos_text(row_no, col_no+1, len(markup.inline_keyboard)),
        reply_markup=InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))

@TGBot.on_callback_query(filters.regex(pattern="ctrl_down"))
async def ctrl_down_handler(bot: Client, update: CallbackQuery):
    markup=(await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)).reply_markup
    if not markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    buttons=update.message.reply_markup.inline_keyboard
    row_no, col_no=[int(x) for x in buttons[1][1].callback_data.split("_")]

    if row_no>=len(markup.inline_keyboard)-1:
        return await update.answer(text="already selected bottom most button")
    if len(markup.inline_keyboard[row_no+1])<=col_no:
        col_no=len(markup.inline_keyboard[row_no+1])-1
    update.message.reply_markup.inline_keyboard[1][1].callback_data=f"{row_no+1}_{col_no}"
    update.message.reply_markup.inline_keyboard[1][1].text=markup.inline_keyboard[row_no+1][col_no].text
    await update.edit_message_text(gen_pos_text(row_no+1, col_no, len(markup.inline_keyboard)),
        reply_markup=InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))

@TGBot.on_callback_query(filters.regex(pattern="ctrl_add_left"))
async def ctrl_add_left_handler(bot: Client, update: CallbackQuery):
    try:
        reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        if not reply_msg.reply_markup:
            btn_name, btn_url=await ask_button_data(update.message)
            return await reply_msg.edit_reply_markup(InlineKeyboardMarkup(
                [[InlineKeyboardButton(btn_name, url=btn_url)]]
            ))
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        if len(buttons[row_no])>7:
            return await update.answer("Can't add more than 8 buttons in a row")
        btn_name, btn_url=await ask_button_data(update.message)
        buttons[row_no].insert(col_no, InlineKeyboardButton(btn_name, url=btn_url))
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        update.message.reply_markup.inline_keyboard[1][1].text=buttons[row_no][col_no].text
        await update.edit_message_reply_markup(InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))
        
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please add button again with valid URL")


@TGBot.on_callback_query(filters.regex(pattern="ctrl_add_right"))
async def ctrl_add_right_handler(bot: Client, update: CallbackQuery):
    try:
        reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        if not reply_msg.reply_markup:
            btn_name, btn_url=await ask_button_data(update.message)
            return await reply_msg.edit_reply_markup(InlineKeyboardMarkup(
                [[InlineKeyboardButton(btn_name, url=btn_url)]]
            ))
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        if len(buttons[row_no])>7:
            return await update.answer("Can't add more than 8 buttons in a row")
        btn_name, btn_url=await ask_button_data(update.message)
        buttons[row_no].insert(col_no+1, InlineKeyboardButton(btn_name, url=btn_url))
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please add button again with valid URL")

@TGBot.on_callback_query(filters.regex(pattern="ctrl_add_above"))
async def ctrl_add_above_handler(bot: Client, update: CallbackQuery):
    try:
        reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        if not reply_msg.reply_markup:
            btn_name, btn_url=await ask_button_data(update.message)
            return await reply_msg.edit_reply_markup(InlineKeyboardMarkup(
                [[InlineKeyboardButton(btn_name, url=btn_url)]]
            ))
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        if len(buttons)>99:
            return await update.answer("Can't add more than 100 buttons rows")
        btn_name, btn_url=await ask_button_data(update.message)
        buttons.insert(row_no, [InlineKeyboardButton(btn_name, url=btn_url)])
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        update.message.reply_markup.inline_keyboard[1][1].text=buttons[row_no][col_no].text
        await update.edit_message_reply_markup(InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))

    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please add button again with valid URL")

@TGBot.on_callback_query(filters.regex(pattern="ctrl_add_below"))
async def ctrl_add_below_handler(bot: Client, update: CallbackQuery):
    try:
        reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
        if not reply_msg.reply_markup:
            btn_name, btn_url=await ask_button_data(update.message)
            return await reply_msg.edit_reply_markup(InlineKeyboardMarkup(
                [[InlineKeyboardButton(btn_name, url=btn_url)]]
            ))
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        if len(buttons)>99:
            return await update.answer("Can't add more than 100 buttons rows")
        btn_name, btn_url=await ask_button_data(update.message)
        buttons.insert(row_no+1,[InlineKeyboardButton(btn_name, url=btn_url)])
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please add button again with valid URL")

@TGBot.on_callback_query(filters.regex(pattern="ctrl_edit_text"))
async def ctrl_edit_text_handler(bot: Client, update: CallbackQuery):
    reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
    if not reply_msg.reply_markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    try:
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        msg=await update.message.reply_text("Send new Text for this button\nWait Time: 2 Minute")
        text=await update.message.chat.listen(filters=filters.text, timeout=120)
        buttons[row_no][col_no].text=text.text
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        await bot.delete_messages(update.message.chat.id, [msg.id, text.id])
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')

@TGBot.on_callback_query(filters.regex(pattern="ctrl_edit_url"))
async def ctrl_edit_url_handler(bot: Client, update: CallbackQuery):
    reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
    if not reply_msg.reply_markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    try:
        buttons=reply_msg.reply_markup.inline_keyboard
        row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
        msg=await update.message.reply_text("Send new URL for this button\nWait Time: 2 Minute")
        url=await update.message.chat.listen(filters=filters.text, timeout=120)
        buttons[row_no][col_no].url=url.text
        await reply_msg.edit_reply_markup(InlineKeyboardMarkup(buttons))
        await bot.delete_messages(update.message.chat.id, [msg.id, url.id])
    except ListenerTimeout:
        return await update.message.reply('You took too long to answer.')
    except ButtonUrlInvalid:
        await update.message.reply_text("Invalid URL please edit button url again with valid URL")

@TGBot.on_callback_query(filters.regex(pattern="ctrl_edit_message"))
async def ctrl_edit_message_handler(bot: Client, update: CallbackQuery):
    reply_msg=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
    try:
        msg=await update.message.reply_text("Send new text for the message\nWait Time: 2 Minute")
        text=await update.message.chat.listen(filters=filters.text, timeout=120)
    except ListenerTimeout:
        return await update.message.reply("You took too long to answer\nDown't worry you wan prepare your message now and click on `Edit Button Text` when your ready")
    try:
        msg2=await update.message.reply_text("Chose a parse mode\nMarkdown: Parse Text in Markdown Mode\nHTML: Parse Text in HTML Mode\nDefault: Parse Text in both HTML and Markdown Mode\nWait Time: 1 Minute\nIf not chosen by default text will be parsed in both Markdown and HTML Mode",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Default"), KeyboardButton("Markdown"), KeyboardButton("HTML")]
                ]
                )
            )
        parse_msg=await update.message.chat.listen(filters=filters.text,timeout=60)
        if parse_msg.text == "Markdown":
            parser=ParseMode.MARKDOWN
        elif parse_msg.text == "HTML":
            parser=ParseMode.HTML
        else:
            parser=ParseMode.DEFAULT
    except ListenerTimeout:
        parser=ParseMode.DEFAULT
    try:
        if reply_msg.text:
            await reply_msg.edit_text(text.text, parse_mode=parser, reply_markup=reply_msg.reply_markup)
        elif reply_msg.media:
            await reply_msg.edit_caption(text.text, reply_markup=reply_msg.reply_markup)
    except MessageNotModified:
        pass
    await bot.delete_messages(update.message.chat.id, [msg.id, text.id, msg2.id, parse_msg.id])

@TGBot.on_callback_query(filters.regex(pattern="ctrl_save.*"))
async def ctrl_save_handler(bot: Client, update: CallbackQuery):
    markup=await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)
    if not markup.reply_markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)
    usr_cmd=update.data.split("_")
    if len(usr_cmd)<3:
        id=None
        msg_id=(await markup.copy(Var.BIN_CHANNEL)).id
    else:
        msg_id=(await db.get_button(usr_cmd[2])).get("msg_id")

    if len(usr_cmd)<3:
        id = await db.save_button(id, update.from_user.id, msg_id)
        update.message.reply_markup.inline_keyboard[7][1]=InlineKeyboardButton("Share", switch_inline_query=str(msg_id))
        update.message.reply_markup.inline_keyboard[6][1].callback_data=f"ctrl_save_{str(id)}"
        await update.edit_message_reply_markup(InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))
        await update.answer("Saved Buttons")
        await update.message.reply_text("You can share use Share Button to share this buttons with others")
    else:
        await bot.edit_message_reply_markup(Var.BIN_CHANNEL, msg_id, markup.reply_markup)
        await update.answer("Edited Button")

@TGBot.on_callback_query(filters.regex(pattern="ctrl_delete"))
async def ctrl_delete_handler(bot: Client, update: CallbackQuery):
    markup=(await bot.get_messages(update.message.chat.id, update.message.reply_to_message_id)).reply_markup
    if not markup:
        return await update.answer(text="First create a button by clicking on any Button stating with 'Add Button'", show_alert=True)

    row_no, col_no=[int(x) for x in update.message.reply_markup.inline_keyboard[1][1].callback_data.split("_")]
    markup.inline_keyboard[row_no].pop(col_no)
    if not markup.inline_keyboard[row_no]:
        markup.inline_keyboard.pop()
        10 <= 5
        if len(markup.inline_keyboard)<=row_no:
            row_no=len(markup.inline_keyboard)-1
    if len(markup.inline_keyboard[row_no])<=col_no:
        col_no=len(markup.inline_keyboard)-1
    update.message.reply_markup.inline_keyboard[1][1].callback_data=f"{row_no}_{col_no}"
    update.message.reply_markup.inline_keyboard[1][1].text=markup.inline_keyboard[row_no][col_no].text
    await update.message.reply_to_message.edit_reply_markup(InlineKeyboardMarkup(markup.inline_keyboard))
    try:
        await update.edit_message_text(gen_pos_text(row_no, col_no, len(markup.inline_keyboard)),
        reply_markup=InlineKeyboardMarkup(update.message.reply_markup.inline_keyboard))
    except MessageNotModified:
        pass

@TGBot.on_callback_query(filters.regex(pattern="\d+_\d+"))
async def info_message_handler(bot: Client, update: CallbackQuery):
    await update.answer(update.message.reply_markup.inline_keyboard[1][1].callback_data)

async def ask_button_data(message: Message) -> Union[str, str]:
    msg1=(await message.reply_text("Send the name that will appear on the button\nWait Time: 2 minute")).id
    btn_name = await message.chat.listen(filters=filters.text, timeout=120)
    msg2=(await message.reply_text("Send the url for the button\nWait Time: 2 minute")).id
    btn_url = await message.chat.listen(filters=filters.text, timeout=120)
    await message._client.delete_messages(message.from_user.id, [msg1, btn_name.id, msg2, btn_url.id])
    return btn_name.text, btn_url.text

def gen_pos_text(row: int, col: int, row_len: int):
    interface = []
    for i in range(row_len):
        row_text = ["🟦"] * 8
        if row==i:
            row_text[col]="🟥"
        interface.append(" ".join(row_text))
    return "\n".join(interface)


@TGBot.on_message(group=6)
async def check_user(bot, message):
    await db.add_user(message.from_user.id)