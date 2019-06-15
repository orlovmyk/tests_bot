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

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Начать тест', 'Начать тест'],
                                        ['Начать тест']],
                                       resize_keyboard=True)

INITIAL_MESSAGE = "Привет!\n" \
                  "'Я чат-бот, созданый для ...\n\n"

TEXT = ["Тест на дебила\n"
        "Желаю удачи",

        "Вопрос №1 Вариатны такие:\n"
        "1. выфвыф\n"
        "2. выфвы\n" 
        "3. выф выфвыф\n",

        "Вопрос №2 Вариатны такие:\n"
        "1. выфвыф\n"
        "2. выфвы\n"
        "3. выф выфвыф\n",

        "Вопрос №3 такие:\n"
        "1. выфвыф\n"
        "2. выфвы\n"
        "3. выф выфвыф\n",

        "Конец\n"
        "Дальше ничего нет\n",
        ]


# USEFUL FUNCTIONS
def generate_inline(*step):
    # ARGUMENT FOR STEP KEYBOARD
    # NO ARGUMENT FOR EMPTY KEYBOARD
    if step:
        inline = InlineKeyboardMarkup(
                 [[InlineKeyboardButton(text="1", callback_data=str(step[0])+".1")],
                  [InlineKeyboardButton(text="2", callback_data=str(step[0])+".2")],
                  [InlineKeyboardButton(text="3", callback_data=str(step[0])+".3")]])

    else:
        inline = InlineKeyboardMarkup([[]])
    return inline


def add_kw(result, chat_id, message_id, **kwargs):
    if kwargs:
        new_kw = {
            chat_id: {
                message_id: {
                    "result": result
                }
            }
        }
        COUNTER.update(new_kw)
    else:
        new_chat_kw = {
            message_id: {
                "result": result
            }
        }
        COUNTER[chat_id].update(new_chat_kw)


def count_result(message, result):
    # 'message': {'message_id': 436, 'date': 1560638474, 'chat': {'id': 239062390,
    chat_id = message.chat.id
    message_id = message.id

    if chat_id not in COUNTER.keys():
        add_kw(result, chat_id, message_id)
    else:
        if message_id not in COUNTER[chat_id]:
            add_kw(result, chat_id, message_id, to_message=True)
        else:
            COUNTER[chat_id][message_id].result += result


def delete_query(message):
    chat_id = message.chat.id
    message_id = message.id
    if chat_id in COUNTER.keys():
        if message_id in COUNTER[chat_id]:
            COUNTER[chat_id].pop(message_id)
        else:
            if not chat_id:
                COUNTER.pop(chat_id)


def get_result(message):
    # 'message': {'message_id': 436, 'date': 1560638474, 'chat': {'id': 239062390,
    chat_id = message.chat.id
    message_id = message.id

    if chat_id in COUNTER.keys():
        if message_id in COUNTER[chat_id]:
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

    if step > len(TEXT):
        count_result(query.message, result)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=TEXT[step],
                              reply_markup=generate_inline())
        bot.answer_callback_query(callback_query_id=query.id, text="На этом всё\nВаш результат: " + str(get_result(query.message)))
        delete_query(query.message)

    else:
        count_result(query.message, result)
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=TEXT[step],
                              reply_markup=generate_inline(step))
        bot.answer_callback_query(callback_query_id=query.id, text="Ви выбрали вариант №" + str(result))


bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Начать тест', test_start),
                CallbackQueryHandler(callback_handler)
                ]
