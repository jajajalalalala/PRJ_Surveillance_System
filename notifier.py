import requests
import threading
from io import BytesIO
import telegram


class RPI_Notifier:

    def __init__(self):
        self

    @staticmethod
    def telegram_bot_sendText(message):
        token = '1546815383:AAGf-drVoek0FmaGsOtFHkZT0-3li6ojHRc'
        chatID = '-556671391'
        send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chatID + '&parse_mode=Markdown&text=' + message

        response = requests.get(send_text)

        return response.json()

    @staticmethod
    def telegram_bot_sendImage(image):
        token = '1546815383:AAGf-drVoek0FmaGsOtFHkZT0-3li6ojHRc'
        chatID = '-556671391'

        bot = telegram.Bot(token)
        bot.send_photo(chatID, photo=open(image, "rb"))


if __name__ == '__main__':
    message = "test"
    notifier1 = RPI_Notifier("1")

