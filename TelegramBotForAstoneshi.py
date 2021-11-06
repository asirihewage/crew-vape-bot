# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at https://github.com/asirihewage/crew-vape-bot
# Telegram Bot
"""

# importing all dependencies
import logging
import os
import telebot
from telegram import ParseMode
from telegram.ext import CallbackContext, Updater, CommandHandler, JobQueue, Dispatcher
import pymongo
import json
import pandas as pd
import jsonpickle

# Getting environment variables from Heroku configs if not overriden
BOT_TELEGRAM_API_TOKEN = os.environ.get('botKey', "2041045930:AAGYTB6grvbbE_Fp6hYWGNKHkkQodscW05k")
BOT_MONGODB_CONECTION_URL = os.environ.get('mongodbConnectionURL',
                                           "mongodb+srv://sampleUsername:samplePassword@cluster0.jbgqq.mongodb.net/myFirstDatabase?authSource=admin&replicaSet=atlas-1r0k4s-shard-0&w=majority&readPreference=primary&appname=MongoDB%20Compass&retryWrites=true&ssl=true")
BOT_DATABASE_NAME = os.environ.get('databaseName', "TelegramBotCrewVape")

# Initialize logging for debugging purpose
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)


# Database Class
class Database:
    # constructor
    def __init__(self):
        self.connectionURL = BOT_MONGODB_CONECTION_URL
        self.databaseName = BOT_DATABASE_NAME
        self.dbClient = None

    # connect to the database
    def connect(self):
        try:
            if not self.dbClient:
                logger.info("Database Client initialized.")
                self.dbClient = pymongo.MongoClient(self.connectionURL)
                database = self.dbClient[str(self.databaseName)]
                if database:
                    logger.info("Database Connected.")
                    return database
                else:
                    logger.info("Database Connection failed.")
                    return None
            else:
                logger.info("Database Client Connection failed.")
                return None
        except Exception as er:
            logger.error(er)


# Message Class
class Message:

    # message constructor
    def __init__(self, dbCon):
        self.dbConnection = dbCon
        self.messagesCollection = self.dbConnection["messages"]

    # save message object
    def save_message(self, messageObj):
        try:
            if self.dbConnection:
                if self.messagesCollection.insert_one(messageObj):
                    logger.info("Message saved in Database")
                    return True
                else:
                    logger.error("Failed to save message on database")
                    return False
            else:
                logger.error("Database connection error")
                return False
        except Exception as er:
            logger.error(er)
            return False


# Initializing database
db = Database()
dbConnection = db.connect()

# Initializing a message object
messageContent = Message(dbConnection)

# initialize the bot
bot = telebot.TeleBot(BOT_TELEGRAM_API_TOKEN, parse_mode="markdown")


# Function to catch incoming command /about
@bot.message_handler(commands=['about'])
def about(message):
    try:
        bot.reply_to(message, "This is a sample Telegram bot. This bot will store incoming messages in a database")
    except Exception as e:
        logger.error(e)
    pass


# Function to catch incomming command /help
@bot.message_handler(commands=['help'])
def help(message):
    try:
        bot.reply_to(message, "Send a message. Then have a look https://github.com/asirihewage/crew-vape-bot")
    except Exception as e:
        logger.error(e)
    pass


# catch all messages and save in database
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        # bot.reply_to(message, message.text)
        messageObj = {
            "chat_id": message.chat.id,
            "message_id": message.message_id,
            "date": message.date,
            "type": message.chat.type,
            "text": message.text,
            "user": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        messageContent.save_message(messageObj)
    except Exception as e:
        logger.error(e)
    pass


# this function will send a message to a specific chat ID
def sendMessageViaChatId(chat_id, txt):
    bot.send_message(chat_id, txt)


sendMessageViaChatId(-1001545752396, "Hi")  # 1664758714 is the chat ID (For private messages, group ID = Chat ID)

# start polling to continuously listen for messages
bot.polling()
# gracefully stop the bot after ctrl + c 
bot.stop_polling()

"""

---


# View Data

View collected data from the Bot. (First stop the bot to view data)"""


def viewData():
    # getting database connection
    messagesCollection = dbConnection["messages"]

    # Make a query to the specific DB and Collection
    cursor = messagesCollection.find()

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))

    return df


viewData()
