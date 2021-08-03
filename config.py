import logging

BACKEND = "Telegram"

BOT_DATA_DIR = r"/home/member/code/chatops/data"
BOT_EXTRA_PLUGIN_DIR = r"/home/member/code/chatops/plugins"

BOT_LOG_FILE = r"/home/member/code/chatops/errbot.log"
BOT_LOG_LEVEL = logging.DEBUG

BOT_ALT_PREFIX = ("jimmy", "/")
BOT_ALT_PREFIX_SEPARATORS = (",", ";")

BOT_IDENTITY = {
    "token": "1923798395:AAGzKtQg6VJUcWUy84RSLGyv7X4nomXmHlQ"
}

BOT_ADMINS = ("139653633", )
