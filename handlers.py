"""
Handlers for all commands
"""
from telegram.ext import (CommandHandler,
                          MessageHandler,
                          Filters,
                          RegexHandler,
                          ConversationHandler,
                          CallbackQueryHandler,)

from telegram import (ReplyKeyboardMarkup,
                      KeyboardButton,
                      InlineKeyboardButton,
                      InlineKeyboardMarkup)

COUNTER = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['О кафедре'],
                                        ['О специальностях/специализациях'],
                                        ['Начать тест'],
                                        ['Контакты'],
                                        ['Адрес']],
                                       resize_keyboard=True)

SUB_KEYBOARD = ReplyKeyboardMarkup([['Бакалавриат'],
                                    ['Магистратура'],
                                    ['На главную']],
                                   resize_keyboard=True)

SUB_KEYBOARD_B = ReplyKeyboardMarkup([['1'],
                                      ['2'],
                                      ['3'],
                                      ['Вернуться назад']],
                                   resize_keyboard=True)

SUB_KEYBOARD_M = ReplyKeyboardMarkup([['1'],
                                      ['2'],
                                      ['3'],
                                      ['Вернуться назад']],
                                   resize_keyboard=True)

INITIAL_MESSAGE = "Привет!\n" \
                  "'Я чат-бот, созданый для ...\n\n"

TEXT = ["Сколько байт в 1 Кбайте?\n"
        "1 - 1000 байт\n"
        "2 - 1024 байт\n"
        "3 - 8 байт\n"
        "4 - 8000 байт",

        "Что из ниже перечисленного не является языком программирования?\n"
        "1 - C#\n"
        "2 - HTML\n"
        "3 - JavaScript\n"
        "4 - PHP\n",

        "Укажите компилируемый язык программирования:\n"
        "1 - JavaScript\n"
        "2 - Java\n"
        "3 - PHP\n"
        "4 - Ruby",

        "Конец\n"
        "Дальше ничего нет\n",
        ]


# USEFUL FUNCTIONS
def generate_inline(*step):
    # ARGUMENT FOR STEP KEYBOARD
    # NO ARGUMENT FOR EMPTY KEYBOARD
    if step:
        inline = InlineKeyboardMarkup(
                 [[InlineKeyboardButton(text="1", callback_data=str(step[0])+".0"),
                  InlineKeyboardButton(text="2", callback_data=str(step[0])+".1"),
                  InlineKeyboardButton(text="3", callback_data=str(step[0])+".0"),
                  InlineKeyboardButton(text="4", callback_data=str(step[0]) + ".0")]])

    else:
        inline = InlineKeyboardMarkup([[]])
    return inline


def add_kw(result, chat_id, message_id, **kwargs):
    if not kwargs:
        new_kw = {
            chat_id: {
                message_id: {
                    "result": int(result)
                }
            }
        }
        COUNTER.update(new_kw)
    else:
        new_chat_kw = {
            message_id: {
                "result": int(result)
            }
        }
        COUNTER[chat_id].update(new_chat_kw)


def count_result(message, result):
    # 'message': {'message_id': 436, 'date': 1560638474, 'chat': {'id': 239062390,
    print(message.chat.id)
    chat_id = message.chat.id
    message_id = message.message_id

    if chat_id not in COUNTER.keys():
        add_kw(result, chat_id, message_id)
    else:
        if message_id not in COUNTER[chat_id]:
            add_kw(result, chat_id, message_id, to_message=True)
        else:
            print(COUNTER[chat_id][message_id]["result"])
            COUNTER[chat_id][message_id]["result"] += int(result)


def delete_query(message):
    chat_id = message.chat.id
    message_id = message.message_id
    if chat_id in COUNTER.keys():
        if message_id in COUNTER[chat_id]:
            COUNTER[chat_id].pop(message_id)
        else:
            if not chat_id:
                COUNTER.pop(chat_id)


def get_result(message):
    # 'message': {'message_id': 436, 'date': 1560638474, 'chat': {'id': 239062390,
    chat_id = message.chat.id
    message_id = message.message_id

    if chat_id in COUNTER.keys():
        if message_id in COUNTER[chat_id].keys():
            return COUNTER[chat_id][message_id]["result"]


# MESSAGE HANDLER
def start(bot, update):
    update.message.reply_text(INITIAL_MESSAGE,
                              reply_markup=MAIN_MENU_MARKUP)


def test_start(bot, update):
    message = TEXT[0]
    markup = generate_inline(0)

    update.message.reply_text(message,
                              reply_markup=markup)


def main_menu(bot, update):
    update.message.reply_text('Главное меню',
                              reply_markup=MAIN_MENU_MARKUP)


# CALLBACK HANDLER
def callback_handler(bot, update):
    query = update.callback_query

    step, result = query.data.split(".")
    step = int(step) + 1

    if step >= len(TEXT) - 1:
        print(999)
        print(get_result(query.message))

        count_result(query.message, result)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=TEXT[step] + "\nВаш результат: " + str(get_result(query.message)),
                              reply_markup=generate_inline())
        bot.answer_callback_query(callback_query_id=query.id, text="На этом всё")
        delete_query(query.message)

    else:
        count_result(query.message, result)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=TEXT[step],
                              reply_markup=generate_inline(step))
        bot.answer_callback_query(callback_query_id=query.id, text="Ви выбрали вариант №" + str(result))


# Handlers for bot
bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Начать тест', test_start),
                CallbackQueryHandler(callback_handler)
                ]


