# PROJECT LIBS
from Core.response_api import get_models,response
from Core.commands.telegram_commands import Basic_commands as bs
from Core.commands.telegram_commands import Advance_commands as ac
from Core.commands.telegram_commands import Dev_commands as dc

# BASIC LIBS
import os
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder,MessageHandler,CallbackQueryHandler,ContextTypes,CommandHandler,filters

load_dotenv(dotenv_path=f'{os.getcwd()}/Core/data/.env')

# INITIAL
user_com = bs()
advance_com = ac()
dev_com = dc()

class TelegramBot():
    def __init__(self):
        self.app = ApplicationBuilder().token(os.getenv('BOT_TELEGRAM_TOKEN')).build()
        
    def main(self):
        # COMMANDS
        self.app.add_handler(CommandHandler('start',user_com.welcome_txt))        
        # TESTING
        
        # RESPONSE
        self.app.add_handler(MessageHandler(filters.ALL,response))
        print("test")
        self.app.run_polling()


if __name__ == '__main__':
    tb = TelegramBot()