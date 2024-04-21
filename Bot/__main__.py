import asyncio
import logging
import sys
from pyrogram import idle
from Bot import TGBot

logging.basicConfig(
    level=logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

loop=asyncio.get_event_loop()  

async def main():
    await TGBot.start()
    me=await TGBot.get_me()
    TGBot.username=me.username
    TGBot.id=me.id
    logging.info("Started Bot: @{}".format(TGBot.username))
    await idle()

async def stop():
    await TGBot.stop()

if __name__ == "__main__":
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error(e)
    finally:
        loop.run_until_complete(stop())
        logging.info("Stoping Bot")