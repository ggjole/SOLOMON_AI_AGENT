from UI.telegram import TelegramBot as tb
import rich
telegram_bot = tb()


def menu():
    print("-"*20)
    print("[1] LAUNCH WITH WEBSITE")
    print("[2] LAUNCH WITH TELEGRAM")
    print("[3] LAUNCH WITH CLI (BETA)")
    print("[x] EXIT")