"""
Handlers for all commands
"""
from telegram.ext import (CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler)
from telegram import ReplyKeyboardMarkup, KeyboardButton


USERS = {}

MAIN_MENU_MARKUP = ReplyKeyboardMarkup([['Начать тест', 'Начать тест'],
                                        ['Начать тест']],
                                       resize_keyboard=True)
MARK, CONTACT = range(2)


def start(bot, update):
    update.message.reply_text('Привет!\n'
                              'Я чат-бот, созданый для ...\n\n',
                              reply_markup=MAIN_MENU_MARKUP)


def main_menu(bot, update):
    update.message.reply_text('Главное меню',
                              reply_markup=MAIN_MENU_MARKUP)


bot_handlers = [CommandHandler('start', start),
                RegexHandler('Главное меню', main_menu),



                ]
