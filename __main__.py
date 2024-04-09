import logging
import os

from dotenv import load_dotenv

from . import bot, handler

load_dotenv()

bot.run(
    os.getenv("SECRET_TOKEN"),
    log_handler=handler,
    log_level=logging.DEBUG,
    root_logger=True,
)
