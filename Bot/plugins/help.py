from pprint import pprint
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from Bot import TGBot


@TGBot.on_message(filters.private & filters.command("rmbtn"))
async def rmbtn_help_handler(bot: Client, message: Message):
    await message.reply_text(
"""`usage: /rmbtn [row] [column]`

Reply to Message from which you want to remove button

row: Count Button from Top to Button you want to remove the number you counted is row
column: Count Buttons from left to Button you want to remove in same line the number you counted is column

example: `/rmbtn 2 5`""")

@TGBot.on_message(filters.private & filters.command("create2"))
async def create_help_handler(bot: Client, message: Message):
    await message.reply_text(
"""`usage: /create2`

Reply to text or media message to create buttons""")


@TGBot.on_message(filters.private & filters.command("done"))
async def done_help_handler(bot: Client, message: Message):
    await message.reply_text(
"""`usage: /done`

Reply to Button you created using /create2 command
It will remove extra buttons Like Add Row and Add Column
""")

@TGBot.on_message(filters.private & filters.command("help"))
async def help_handler(bot: Client, message: Message):
    await message.reply_text(
"""<u>/create command</u>
It is a easy to use mode with Buttons to do everything

<u>/create2 command</u>
Here is How to use this bot with /create2 command
step 1: Send a Text or File here
step 2: Reply to the message you sent with /create2
step 3: Add Button by pressing on Add Column Button, You can add more rows by clicking on Add Row Button
step 4: After you complete creating buttons reply to message containg your buttons with /done command
step 5: Done you will receive message from bot will buttons you created
""")
