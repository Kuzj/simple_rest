import logging
import os

from bot.bot import Bot

class ICQBotError(Exception):
    pass

bot_var_from_env = {i.split('_',1)[1]:os.environ[i] for i in list(os.environ.keys()) if i.startswith('icqbot_')}
if not bot_var_from_env:
    raise ICQBotError(f'Environment variable not found\nexport icqbot_[bot name]=[token]\nor delete {__name__} extension')

bot_dict = {name:Bot(token=token) for name, token in bot_var_from_env.items()}

async def send_message(bot_name, chat, message):
    try:
        bot = bot_dict[bot_name]
    except KeyError:
        raise ICQBotError('Bot with this name does not exist')
    bot.send_text(chat_id=chat, text=message)
    logging.info(f"bot_name: {bot_name} chat: {chat} message: {message}")
