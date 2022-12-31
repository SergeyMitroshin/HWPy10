import re
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import csv


commands = ['phonebook']
phonebookDB = {'Vasia': '+223322456', 'Petr': '+33245634', 'Daniil': '+7345345345'}

def handle_message(update, context):
    message = update.message
    text = message.text
    modified_text = remove_abc(text)
    context.bot.send_message(chat_id=message.chat_id, text=modified_text)

def start(update, context):
    update.message.reply_text('Привет! Я бот - телефонный справочник.\n'
                              'Поиск: /phonebook search [name]\n'
                              'Добавление: /phonebook add [name] [phone number]\n'
                              'Удаление: /phonebook remove [name]\n'
                              'Экспорт: /export [file name.csv]\n')


def phonebook(update, context):
    message = update.message.text
    words = message.split()
    if len(words) >= 2:
        subcommand = words[1]
        if subcommand == 'search':
            if len(words) == 3:
                name = words[2]
                if name in phonebookDB:
                    update.message.reply_text(f'{name}: {phonebookDB[name]}')
                else:
                    update.message.reply_text(f'Ошибка: {name} не найдено в телефонной книге')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook search [name]\n'
                                          'для поиска в справочнике')
        elif subcommand == 'add':
            if len(words) == 4:
                name = words[2]
                phone_number = words[3]
                phonebookDB[name] = phone_number
                update.message.reply_text(f'{name} добавлено в телефонную книгу')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook add [name] [phone number]\n'
                                          'для добавления контакта в телефонную книгу')
        elif subcommand == 'remove':
            if len(words) == 3:
                name = words[2]
                if name in phonebookDB:
                    del phonebookDB[name]
                    update.message.reply_text(f'{name} удалено из телефонной книги')
                else:
                    update.message.reply_text(f'Ошибка: {name} не найдено в телефонной книге')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook remove [name]\n'
                                          'для удаления контакта из телефонной книги')

def export_phonebook(update, context):
    message = update.message.text
    words = message.split()
    if len(words) == 2:
        file_name = words[1]
        
        with open(file_name, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Name', 'Phone Number'])
            
            for name, phone_number in phonebookDB.items():
                csv_writer.writerow([name, phone_number])
        

        context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_name, 'rb'))
    else:
        update.message.reply_text('Ошибка: неправильный формат\n'
                         'Используйте формат /export [file name]\n'
                         'для экспорта телефонной книги в CSV-файл')

def main():
    updater = Updater('jkhgkjhgkjhgk', use_context=True)

    dp = updater.dispatcher
  

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('phonebook', phonebook))
    dp.add_handler(CommandHandler('export', export_phonebook))
  

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
  main()