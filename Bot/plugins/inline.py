from pyromod import Client
from pyrogram import filters, types
from pyrogram.enums.message_media_type import MessageMediaType
from Bot import TGBot
from Bot.vars import Var

@TGBot.on_inline_query(filters.regex("^[0-9]*$"))
async def answer(bot: Client, update: types.InlineQuery):
    msg=await bot.get_messages(Var.BIN_CHANNEL, int(update.query))
    if msg.media == MessageMediaType.ANIMATION:
        button=types.InlineQueryResultCachedAnimation(
            msg.animation.file_id,
            title=update.query,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.media == MessageMediaType.AUDIO:
        button=types.InlineQueryResultCachedAudio(
            msg.audio.file_id,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.media == MessageMediaType.DOCUMENT:
        button=types.InlineQueryResultCachedDocument(
            msg.document.file_id,
            title=update.query,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.media == MessageMediaType.PHOTO:
        button=types.InlineQueryResultCachedPhoto(
            msg.photo.file_id,
            title=update.query,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.media == MessageMediaType.STICKER:
        button=types.InlineQueryResultCachedSticker(
            msg.sticker.file_id,
            reply_markup=msg.reply_markup
        )        
    elif msg.media == MessageMediaType.VIDEO:
        button=types.InlineQueryResultCachedVideo(
            msg.video.file_id,
            title=update.query,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.media == MessageMediaType.VOICE:
        button=types.InlineQueryResultCachedVoice(
            msg.voice.file_id,
            title=update.query,
            caption=msg.caption,
            reply_markup=msg.reply_markup
        )
    elif msg.text:
        button=types.InlineQueryResultArticle(
            title=update.query,
            input_message_content=types.InputTextMessageContent(msg.text.markdown),
            reply_markup=msg.reply_markup
        )

    await update.answer(
        results=[button],
        cache_time=1
    )
