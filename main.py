from telebot import types
import telebot
from auth_data import token
from dodo_parse import main
from dodo_parse import try_get_page


info = try_get_page()


def telegram_bot(token):
    bot = telebot.TeleBot(token)


    @bot.message_handler(commands=["start"])
    def start_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Пицца:Без мяса:pizzas')
        btn2 = types.KeyboardButton("Пицца:С мясом:pizzas")
        btn3 = types.KeyboardButton("Закуска:Без мяса:snacks")
        btn4 = types.KeyboardButton("Закуска:С мясом:snacks")
        btn5 = types.KeyboardButton("Напитки:Напитки:drinks")
        btn6 = types.KeyboardButton("Десерты:Десерты:desserts")


        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn5)
        markup.add(btn6)

        bot.send_message(message.chat.id, "Тест-бот готов работать для пирожка! "
                                          "В меню бота можно выбрать весь ассортимент "
                                          "До-До пиццерии", reply_markup=markup)


    @bot.message_handler(content_types=["text"])
    def message_handler(message):
        if message.text:
            bot.send_message(message.chat.id, info)
            menu = main(message.text.split(":")[2], message.text.split(":")[1])
            bot.send_message(message.chat.id, "Меню на текущий час\n")
            bot.send_message(message.chat.id, menu)
            bot.send_message(message.chat.id, "https://dodopizza.kz/")
        # elif message.text == "Напитки:drinks":
        #      bot.send_message(message.chat.id, info)
        #      menu = main(message.text.split(":")[1])
        #      bot.send_message(message.chat.id, "Меню напитков на сегодня\n")
        #      bot.send_message(message.chat.id, menu)

        else:
            bot.send_message(message.chat.id, "Упс! Неверная команда, попробуй еще раз")



    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)