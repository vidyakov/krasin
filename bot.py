import telebot
import logging
import conf

bot = telebot.TeleBot(conf.TOKEN)


def to_mailing(from_id):
    try:
        with open('ip.txt', 'r', encoding='utf8') as users_file:
            users_file = users_file.read().split()
            if not str(from_id) in users_file:
                with open('ip.txt', 'a', encoding='utf8') as add_user_to_file:
                    add_user_to_file.write(str(from_id) + '\n')
                    return
            else:
                return
    except:
        logging.exception('')


@bot.message_handler(commands=['mailing'])
def mailing_message(message):
    try:
        if message.chat.id == conf.admin:
            if message.text[9:] == '':
                bot.send_message(message.chat.id, '⚠ Отсутствует текст рассылки.')
            else:
                with open('ip.txt', 'r', encoding='utf8') as users_file:
                    users = users_file.read().split()
                    users_count = len(users)
                    for i in range(users_count):
                        try:
                            bot.send_message(users[i], message.text[9:])
                        except:
                            print('blocked')
                bot.send_message(message.chat.id, 'Успешно!')
    except:
        logging.exception('')


@bot.message_handler(commands=['start'])
def start(message):
    try:
        to_mailing(message.chat.id)
        bot.send_message(conf.admin, 'Новый пользователь!')
        bot.send_message(message.chat.id, conf.start)
    except:
        logging.exception('')


@bot.message_handler(commands=['today'])
def today_tap(message):
    try:
        with open('tap.txt', 'r', encoding='utf8') as file:
            bot.send_message(message.chat.id, file.read())
    except:
        logging.exception('')


@bot.message_handler(commands=['set_on_tap'])
def set_on_tap(message):
    try:
        if message.chat.id == conf.admin:
            if message.text[12:] == '':
                bot.send_message(message.chat.id, '⚠ Отсутствует текст')
            else:
                with open('tap.txt', 'w', encoding='utf8') as file:
                    file.write(message.text[12:])
                    bot.send_message(message.chat.id, 'Успешно!')
    except:
        logging.exception('')


@bot.message_handler(commands=['help_me_today'])
def game(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        keyboard.row(conf.button_stop)
        send = bot.send_message(message.chat.id, f'После какого бокала не наливать сегодня, {message.from_user.first_name}?\n\nДля отмены нажмите на крестик ⬇',
                                reply_markup=keyboard)
        bot.register_next_step_handler(send, send_user_count)
    except:
        logging.exception('')


def send_user_count(message):
    try:
        if not message.text == conf.button_stop:
            bot.send_message(message.chat.id, f'Ok!\nСегодня не наливаем вам после {int(message.text)} бокала!\nОбращайтесь снова!')
            bot.send_message(conf.admin, f'Не наливать {message.from_user.first_name} после {message.text}')
        else:
            bot.send_message(message.chat.id, 'Если что обращайтесь!')
    except:
        send = bot.send_message(message.chat.id, conf.button_stop)
        bot.register_next_step_handler(send, send_user_count)


while True:
    try:
        bot.infinity_polling(True)
    except:
        logging.exception('')
        bot.send_message(conf.admin, 'Я сломался')
