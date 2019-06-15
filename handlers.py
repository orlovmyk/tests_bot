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
MARK, CONTACT = range(2)


def start(bot, update):
    update.message.reply_text('Привет!\n'
                              'Я чат-бот, созданый для ...\n\n',
                              reply_markup=MAIN_MENU_MARKUP)


def test_start(bot, update):
    message = "Первый вопрос\n" \
              "1. выфвы\n" \
              "2. выфвы\n" \
              "3. выфвыфвыф\n"
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="1", callback_data="1.1")],
                                   [InlineKeyboardButton(text="2", callback_data="1.2")],
                                   [InlineKeyboardButton(text="3", callback_data="1.3")],
                                   ])
    update.message.reply_text(message,
                              reply_markup=markup)


def main_menu(bot, update):
    update.message.reply_text('Главное меню',
                              reply_markup=MAIN_MENU_MARKUP)


# CALLBACK HANDLER
def callback_handler(bot, update):
    print(123)


bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),
                RegexHandler('Начать тест', test_start),
                CallbackQueryHandler('', callback_handler)


                ]
