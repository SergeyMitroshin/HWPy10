import re
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import csv

# Set the command list for the bot
commands = ['phonebook']

# Set the phonebook database as a dictionary
phonebookDB = {'Vasia': '+223322456', 'Petr': '+33245634', 'Daniil': '+7345345345'}

def handle_message(update, context):
    # Get the message from the update
    message = update.message
    text = message.text

    # Remove "abc" from the message text
    modified_text = remove_abc(text)

    # Send the modified message back to the user
    context.bot.send_message(chat_id=message.chat_id, text=modified_text)

def start(update, context):
    #Send a message when the command /start is issued
    update.message.reply_text('Привет! Я бот - телефонный справочник.\n'
                              'Поиск: /phonebook search [name]\n'
                              'Добавление: /phonebook add [name] [phone number]\n'
                              'Удаление: /phonebook remove [name]\n'
                              'Экспорт: /export [file name.csv]\n')


def phonebook(update, context):
    #Search and manage the phonebook database.
    
    # Get the user's message
    message = update.message.text
    
    # Split the message into a list of words
    words = message.split()
    
    # Check that the message has the correct format (i.e., at least two words: the command and a subcommand)
    if len(words) >= 2:
        # Extract the subcommand from the message
        subcommand = words[1]
        # Check the subcommand
        if subcommand == 'search':
            # Check that the message has the correct format (i.e., three words: the command, the subcommand, and the name to search)
            if len(words) == 3:
                # Extract the name to search from the message
                name = words[2]
                # Check if the name is in the phonebook
                if name in phonebookDB:
                    # Send the phone number back to the user
                    update.message.reply_text(f'{name}: {phonebookDB[name]}')
                else:
                    update.message.reply_text(f'Ошибка: {name} не найдено в телефонной книге')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook search [name]\n'
                                          'для поиска в справочнике')
        elif subcommand == 'add':
            # Check that the message has the correct format (i.e., four words: the command, the subcommand, the name, and the phone number)
            if len(words) == 4:
                # Extract the name and phone number from the message
                name = words[2]
                phone_number = words[3]
                # Add the name and phone number to the phonebook
                phonebookDB[name] = phone_number
                update.message.reply_text(f'{name} добавлено в телефонную книгу')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook add [name] [phone number]\n'
                                          'для добавления контакта в телефонную книгу')
        elif subcommand == 'remove':
            # Check that the message has the correct format (i.e., three words: the command, the subcommand, and the name to remove)
            if len(words) == 3:
                # Extract the name to remove from the message
                name = words[2]
                # Check if the name is in the phonebook
                if name in phonebookDB:
                    # Remove the name and phone number from the phonebook
                    del phonebookDB[name]
                    update.message.reply_text(f'{name} удалено из телефонной книги')
                else:
                    update.message.reply_text(f'Ошибка: {name} не найдено в телефонной книге')
            else:
                update.message.reply_text('Ошибка: неправильный формат\n'
                                          'Используйте формат /phonebook remove [name]\n'
                                          'для удаления контакта из телефонной книги')

def export_phonebook(update, context):
    # Get the user's message
    message = update.message.text
    
    # Split the message into a list of words
    words = message.split()
    
    # Check that the message has the correct format (i.e., two words: the command and the file name)
    if len(words) == 2:
        # Extract the file name from the message
        file_name = words[1]
        
        # Open the CSV file in write mode
        with open(file_name, 'w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            
            # Write the header row to the CSV file
            csv_writer.writerow(['Name', 'Phone Number'])
            
            # Iterate through the phonebook database and write each name and phone number to the CSV file
            for name, phone_number in phonebookDB.items():
                csv_writer.writerow([name, phone_number])
        
        # Use the telegram API to send the CSV file to the user
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_name, 'rb'))
    else:
        update.message.reply_text('Ошибка: неправильный формат\n'
                         'Используйте формат /export [file name]\n'
                         'для экспорта телефонной книги в CSV-файл')

def main():
    # Create the Updater and pass it the bot's token
    updater = Updater('jkhgkjhgkjhgk', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
  
    # Add a message handler that will respond to messages containing "abc"
    dp.add_handler(MessageHandler(Filters.text & Filters.regex(r"abc"), handle_message))
    
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('phonebook', phonebook))
    dp.add_handler(CommandHandler('export', export_phonebook))
  
    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == "__main__":
  main()