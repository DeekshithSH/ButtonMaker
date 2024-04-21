from pyromod import Client
from Bot.vars import Var

TGBot=Client("Bot", Var.API_ID, Var.API_HASH, bot_token=Var.BOT_TOKEN,workers=Var.WORKER, workdir="Bot", plugins={"root": "Bot/plugins"})