from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from PIL import Image
import PaletteCreator
from io import BytesIO
import requests


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="I'm PyletteBot, you send me images, i send you palettes, a good deal isn't it?"
                          ""
                          "If you want to know how i'm made, please visit https://github.com/Tsadoq/Palette.Bot")


def startup(tkn):
    updater = Updater(token=tkn)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    print('startin up the bot')
    return updater, dispatcher


def replypalette(bot, update):
    print('image received')
    imgurl= bot.getFile(update.message.photo[-1]).file_path
    print(imgurl)
    chat_id = update.message.chat_id
    print(chat_id)
    adminchat=open('admin_chat.txt', 'r').readline()
    bot.send_message(chat_id=adminchat,text='image elaborated')
    bot.send_message(chat_id=update.message.chat_id,
                     text="I received the image, please, let me elaborate it, this could take up to 30 seconds")
    response = requests.get(imgurl)
    img = Image.open(BytesIO(response.content))
    outimg = PaletteCreator.image_creator(img)
    sendimage = BytesIO()
    sendimage.name = 'image.jpeg'
    outimg.save(sendimage, 'JPEG')
    sendimage.seek(0)
    bot.send_photo(chat_id, photo=sendimage)



def main():
    tkn = open('token.txt', 'r').readline()
    updater, dispatcher = startup(tkn)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(MessageHandler(Filters.photo, replypalette))
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
