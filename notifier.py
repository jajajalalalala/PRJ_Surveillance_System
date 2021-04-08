######## A home Surveillance system - Telegram notification module #########
#
# Author: Bonian Hu
# Date: 2021/04/08
# Description: This class implements the telegram notifier via telegram Bot. The notifier can either
# send a frame or a text. It makes each notification as a thread.


import telegram
from threading import Thread

# Define the chat id and bot token
token = '1546815383:AAGf-drVoek0FmaGsOtFHkZT0-3li6ojHRc'
chat_id = '-556671391'


# Send normal text
def telegram_bot_send_text(message):
    bot = telegram.Bot(token)
    bot.send_message(chat_id=chat_id, text=message,
                     parse_mode=telegram.ParseMode.HTML)
# Define the sending text function
def telegram_bot_send_notify_text(message):
    bot = telegram.Bot(token)
    message += "\n Click <a href='http://192.168.0.143:5000'>here</a> to access the details"
    bot.send_message(chat_id=chat_id, text=message,
                     parse_mode=telegram.ParseMode.HTML)


# Define the sending photo function
def telegram_bot_send_image(image):
    bot = telegram.Bot(token)
    bot.send_photo(chat_id, photo=open(image, "rb"))


class RPI_Notifier:
    """
    A notifier class that can send either a text or a frame with text.
    """

    def __init__(self):
        self
    #Send the a text to the user
    def send_text(self, message):
        thr = Thread(target=telegram_bot_send_text, args=[message])
        thr.start()


    # Send notification to the phone telegram
    def send_message(self, message, image):
        thr = Thread(target=telegram_bot_send_notify_text, args=[message])
        thr.start()

        thr2 = Thread(target=telegram_bot_send_image, args=[image])
        thr2.start()
        return "OK"



