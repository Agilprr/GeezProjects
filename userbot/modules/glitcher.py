# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for filter commands """

import asyncio
import os
import time

from glitch_this import ImageGlitcher
from PIL import Image
from telethon import functions, types

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.utils import edit_or_reply, geez_cmd
from userbot.utils import check_media, progress

Glitched = TEMP_DOWNLOAD_DIRECTORY + "glitch.gif"


@geez_cmd(pattern="glitch$")
async def glitch(event):
    if not event.reply_to_msg_id:
        await edit_or_reply("`Aku Mau Glitch Sebuah Hantu!`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply("`Bales Ke Gambar/Sticker`")
        return
    await bot.download_file(reply_message.media)
    await edit_or_reply("`Sedang Mendownload Media....`")
    if event.is_reply:
        data = await check_media(reply_message)
        if isinstance(data, bool):
            await edit_or_reply("`File Tidak Di Dukung...`")
            return
    else:
        await edit_or_reply("`Balas Ke Media....`")
        return

    try:
        value = int(event.pattern_match.group(1))
        if value > 8:
            raise ValueError
    except ValueError:
        value = 2
    await edit_or_reply("```Melakukan Glitch Pada Media Ini```")
    await asyncio.sleep(2)
    file_name = "glitch.png"
    to_download_directory = TEMP_DOWNLOAD_DIRECTORY
    downloaded_file_name = os.path.join(to_download_directory, file_name)
    downloaded_file_name = await bot.download_media(
        reply_message,
        downloaded_file_name,
    )
    glitch_file = downloaded_file_name
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    glitch_img = glitcher.glitch_image(img, value, color_offset=True, gif=True)
    DURATION = 200
    LOOP = 0
    glitch_img[0].save(
        Glitched,
        format="GIF",
        append_images=glitch_img[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await edit_or_reply("`Sedang Mengunggah Media Yang Telah Di Glitch`")
    c_time = time.time()
    nosave = await event.client.send_file(
        event.chat_id,
        Glitched,
        force_document=False,
        reply_to=event.reply_to_msg_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UPLOAD]")
        ),
    )
    await event.delete()
    os.remove(Glitched)
    await bot(
        functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=nosave.media.document.id,
                access_hash=nosave.media.document.access_hash,
                file_reference=nosave.media.document.file_reference,
            ),
            unsave=True,
        )
    )
    os.remove(glitch_file)
    os.remove(Glitched)


CMD_HELP.update(
    {
        "glitch": "**Plugin : **`glitch`\
        \n\n  𝘾𝙤𝙢𝙢𝙖𝙣𝙙 :** `.glitch` <reply Ke Sticker/Gambar>\
        \n  ❍▸ : **Glitch Level 1-8 Jika Tidak Membuat Level Maka Otomatis Default Level 2.\
    "
    }
)
