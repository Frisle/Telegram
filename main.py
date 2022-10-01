import telebot
from auth_data import token
from link_analizator import ticker
from dodo_parse import print_request_menu
from dodo_parse import try_get_page

about = """
Прямо сейчас не много вещей
одна из основных задач тестировать код
для построения телеграмм-бота
"""




ticker = ticker()
emoji_money = "\U0001F911"
info = try_get_page()


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Тест-бот готов работать для пирожка! Напишите \"Без мяса\" чтобы получить"
                                          " веганские закуски. Напишите \" С мясом\" чтобы получить закуски с мясом из До-До."
                                          " Напишите \" Напитки \" чтобы получить меню напитков")

    @bot.message_handler(commands=["snacks"])
    def snacks_switch(message):
        bot.send_message(message.chat.id, "Выбраны закуски")
        file = open("product.txt", "w")
        file.write("snacks")
        file.close()

    @bot.message_handler(commands=["pizza"])
    def snacks_switch(message):
        bot.send_message(message.chat.id, "Выбраны пиццы")
        file = open("product.txt", "w")
        file.write("pizzas")
        file.close()

    @bot.message_handler(content_types=["text"])
    def message_handler(message):
        if message.text == "Без мяса":
            bot.send_message(message.chat.id, info)
            menu = print_request_menu("Без мяса")
            bot.send_message(message.chat.id, "Меню без мяса на сегодня\n")
            bot.send_message(message.chat.id, menu)
        elif message.text == "С мясом":
            bot.send_message(message.chat.id, info)
            menu = print_request_menu("С мясом")
            bot.send_message(message.chat.id, "Меню с мясом на сегодня\n")
            bot.send_message(message.chat.id, menu)
        elif message.text == "Напитки":
            bot.send_message(message.chat.id, info)
            menu = print_request_menu("Напитки")
            bot.send_message(message.chat.id, "Меню напитков на сегодня\n")
            bot.send_message(message.chat.id, menu)

        else:
            bot.send_message(message.chat.id, "Упс! Неверная комманда, попробуй еще раз")


        # elif message.text == "кот":
        #     bot.send_message(message.chat.id, "https://klike.net/uploads/posts/2021-05/1621412147_3.jpg")





    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)