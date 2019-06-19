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

from questions import QUIZ_QUESTIONS as Q

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


# USEFUL FUNCTIONS

# Генерирую клаву
def generate_inline(*step):
    # ARGUMENT FOR STEP KEYBOARD
    # NO ARGUMENT FOR EMPTY KEYBOARD
    if step:
        inline_arr = []

        for i in range(len(Q[0]["answers"])):
            inline_arr.append(InlineKeyboardButton(text=str(i + 1), callback_data=str(step[0])+"."+str(i + 1)))

        inline = InlineKeyboardMarkup([inline_arr])

    else:
        inline = InlineKeyboardMarkup([[]])

    return inline


# Генерирую текст ответа для теста
# если передаю на каком мы сейчас шаге - беру текст из вопросника, нет - можно дописать что угодно
def generate_text(*step):
    if step:
        text = Q[step[0]]["question"]+"\n"

        itr = 1
        for i in Q[step[0]]["answers"]:
            text += str(itr) + " - " + i["text"] + "\n"

            itr += 1
    else:
        text = "Дебаг??"

    return text


# Генерирую результат относительно того какой сейчас шаг и какая кнопка была нажата
def generate_result(*step, result):
    if step:
        result = int(result)-1
        return_result = Q[step[0]-1]["answers"][result]["value"]

    else:
        return_result = "Дебаг??"

    print("return_result: " + str(return_result))
    return return_result


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
    chat_id = message.chat.id
    message_id = message.message_id

    if chat_id not in COUNTER.keys():
        add_kw(result, chat_id, message_id)
    else:
        if message_id not in COUNTER[chat_id]:
            add_kw(result, chat_id, message_id, to_message=True)
        else:
            print("count_result: " + str(COUNTER[chat_id][message_id]["result"]))
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
    text = generate_text(0)
    markup = generate_inline(0)

    update.message.reply_text(text,
                              reply_markup=markup)


def main_menu(bot, update):
    update.message.reply_text('Главное меню',
                              reply_markup=MAIN_MENU_MARKUP)


# CALLBACK HANDLER
def callback_handler(bot, update):
    query = update.callback_query

    step, result = query.data.split(".")

    print("Current step: " + step)
    step = int(step) + 1

    if step >= len(Q):
        print("TOTAL RESULT: " + str(get_result(query.message)))

        count_result(query.message, int(generate_result(step, result=result)))
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text="\nВаш результат: " + str(get_result(query.message)),
                              reply_markup=generate_inline())
        bot.answer_callback_query(callback_query_id=query.id, text="На этом всё")
        delete_query(query.message)

    else:
        count_result(query.message, int(generate_result(step, result=result)))
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text=generate_text(step),
                              reply_markup=generate_inline(step))
        bot.answer_callback_query(callback_query_id=query.id, text="Вы выбрали вариант №" + str(result))


# Handlers for bot
bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Начать тест', test_start),
                CallbackQueryHandler(callback_handler)
                ]


