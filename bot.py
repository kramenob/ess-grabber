
# bot.py
# Telegram bot "Sound Grabber Bot" code
# It's getting link message and make the post

#################################################
                                                #
import main         # Main Sound Grabber code   #
import config       # Configuration file        #
import logging      # Logging all code          #
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
                                                #
#################################################

from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)

def start():
    executor.start_polling(dp, skip_updates=True)

print("\n    Shalom, Mark!\n    Telegram bot in touch\n")

@dp.message_handler(content_types=["text"])
async def get_album_source(message: types.Message):

    link = message.text

    if link[0:35] == "https://www.epidemicsound.com/music":

        main.get_source_html(message.text)
        main.get_album_info(config.file_source)

        with open("./bin/info/info.md", "r", encoding="utf_8_sig") as file:

            album_info = "".join(file.readlines())
            cover = open(config.cover, "rb")

            await bot.send_photo(
                config.group_id,
                cover,
                caption = album_info,
                parse_mode = 'HTML'
            )
    else:
        pass

# p.s. Tutorial - https://youtu.be/I8K3iYcxPl0