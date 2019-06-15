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


USERS = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Начать тест', 'Начать тест'],
                                        ['Начать тест']],
                                       resize_keyboard=True)


TEXT = ["Вопрос №1 Вариатны такие:\n"
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
        ]


# USEFUL FUNCTIONS
def generate_inline(step):
    inline = [[InlineKeyboardButton(text="1", callback_data=str(step)+".1")],
              [InlineKeyboardButton(text="2", callback_data=str(step)+".2")],
              [InlineKeyboardButton(text="3", callback_data=str(step)+".3")]]
    return inline


# MESSAGE HANDLER
def start(bot, update):
    update.message.reply_text('Привет!\n'
                              'Я чат-бот, созданый для ...\n\n',
                              reply_markup=MAIN_MENU_MARKUP)


def test_start(bot, update):
    message = TEXT[0]
    markup = InlineKeyboardMarkup(generate_inline(0))

    update.message.reply_text(message,
                              reply_markup=markup)


def main_menu(bot, update):
    update.message.reply_text('Главное меню',
                              reply_markup=MAIN_MENU_MARKUP)


# CALLBACK HANDLER
def callback_handler(bot, update):
    query = update.callback_query
    print(query)

    step, result = query.strip(".")
    step += 1

    if step > len(TEXT):
        bot.edit_message_text(chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              text="Конец",
                              reply_markup=[[]])

    bot.edit_message_text(chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          text=TEXT[step],
                          reply_markup=generate_inline(step))


bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Начать тест', test_start),
                CallbackQueryHandler('', callback_handler)


                ]
