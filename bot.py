# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at https://github.com/asirihewage/crew-vape-bot
# Telegram Bot
"""

# importing all dependencies
import logging
import os
from threading import Thread
import pymongo
import logging.handlers as handlers
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from fuzzywuzzy import fuzz

# Getting environment variables from Heroku configs if not overriden
BOT_MONGODB_CONECTION_URL = "mongodb+srv://sampleUsername:samplePassword@cluster0.lok9v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BOT_DATABASE_NAME = "TelegramBotCrewVape"
BOT_TOKEN = "2100863462:AAHK3vbFTjDPa5mIUhI8uY5HkbvufDKGi28"
schedule = 0
ANSWER_ACCURACY_PERCENTAGE = 75

app = Client("bot", bot_token=BOT_TOKEN, parse_mode="combined")

# Initialize logging for debugging purpose
formatter = logging.Formatter(
    '%(asctime)s * %(name)s * %(levelname)s * [%(filename)s:%(lineno)s  %(funcName)20s() ] %(message)s')
logger = logging.getLogger()
logHandler = handlers.TimedRotatingFileHandler('logs/logger.log', when='M', interval=53, backupCount=24)
logHandler.setLevel(logging.ERROR)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.error("Bot initialized")


# connect to the database
def connect():
    try:
        if BOT_MONGODB_CONECTION_URL:
            logger.error("Database Client initialized.")
            client = pymongo.MongoClient(BOT_MONGODB_CONECTION_URL)
            database = client[BOT_DATABASE_NAME]
            if database:
                logger.error("Database Connected.")
                return database
            else:
                logger.error("Database Connection failed.")
                return None
        else:
            logger.error("Database Client Connection failed.")
            return None
    except Exception as e:
        logger.error("Database Error : {}".format(e))
        return None


dbConnection = connect()


# save message object
def save_message(messageObj):
    try:
        if dbConnection:
            messagesCollection = dbConnection.get_collection("messages")
            if messagesCollection.insert_one(messageObj):
                logger.error("Message saved in Database")
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


def register_user(message):
    try:
        messageObj = {
            "id": message.from_user.id,
            "date": message.date,
            "type": message.chat.type,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "level": 1
        }
        updatedUser = {
            "date": message.date,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": message.from_user.id}):
                usersCollection.update_one({"id": message.from_user.id}, {"$set": updatedUser})
            else:
                if usersCollection.insert_one(messageObj):
                    logger.error("User saved in Database")
                    return True
                else:
                    logger.error("Failed to save user on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def checkUser(message):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": message.from_user.id, "level": 0}):
                return True
            else:
                return False
        return False
    except Exception as e:
        logger.error(e)


def isAdmin(message):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": message.from_user.id, "level": 1}):
                return True
            else:
                return False
        return False
    except Exception as e:
        logger.error(e)


def get_answer(question):
    try:
        if dbConnection:
            answersCollection = dbConnection.get_collection("answers")
            answer = None
            latestSimilarity = 0
            for x in answersCollection.find():
                similarity = fuzz.ratio(x['question'], question)
                if similarity >= ANSWER_ACCURACY_PERCENTAGE and similarity > latestSimilarity:
                    answer = x['answer']
                    latestSimilarity = similarity

            return answer
        else:
            return None
    except Exception as e:
        logger.error(e)


def save_answer(question, answer):
    try:
        messageObj = {
            "question": question,
            "answer": answer,
            "isKeyword": 0
        }
        if dbConnection:
            answersCollection = dbConnection.get_collection("answers")
            if answersCollection.find_one({"question": question}):
                answersCollection.update_one({"question": question, "isKeyword": 0}, {"$set": {"answer": answer}})
            else:
                if answersCollection.insert_one(messageObj):
                    logger.error("Question and answer saved in Database")
                    return True
                else:
                    logger.error("Failed to save Question and answer on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def save_keyword(keyword, response):
    try:
        messageObj = {
            "question": keyword,
            "answer": response,
            "isKeyword": 1
        }
        if dbConnection:
            answersCollection = dbConnection.get_collection("answers")
            if answersCollection.find_one({"question": keyword}):
                answersCollection.update_one({"question": keyword, "isKeyword": 1}, {"$set": {"answer": response}})
            else:
                if answersCollection.insert_one(messageObj):
                    logger.error("keyword and response saved in Database")
                    return True
                else:
                    logger.error("Failed to save keyword and response on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def get_all_schedules():
    try:
        if dbConnection:
            schedulesCollection = dbConnection.get_collection("schedules")
            if schedulesCollection.count_documents({}) > 100:
                logger.error("Too many schedules")
                return None
            else:
                logger.error("Retrieving schedules")
                return schedulesCollection.find()
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def promote_admin(admin):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"username": admin}):
                usersCollection.update_one({"username": admin}, {"$set": {"level": 1}})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def remove_admin(admin):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"username": admin}):
                usersCollection.update_one({"username": admin}, {"$set": {"level": 0}})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


@app.on_message(filters.text & filters.private)
async def check_msg(Client, message):
    try:
        dateS = message['date']
        dateSent = datetime.fromtimestamp(dateS)
        minutes_diff = (datetime.now() - dateSent).total_seconds() / 60.0

        if minutes_diff < 2:
            register_user(message)
            if message.text.startswith("learn "):
                if isAdmin(message):
                    txt = message.text.replace("learn ", "").split(",")
                    save_answer(txt[0], txt[1])
                    await app.send_message(message.from_user.id, f"Thank you! I will remember that.")
                    logger.error("Question: {} Answer: {}".format(txt[0], txt[1]))
                else:
                    await app.send_message(message.from_user.id,
                                           f"Oopz! You are not an admin. {message.from_user.mention}")

            elif message.text.startswith("keyword "):
                keywords = message.text.replace("keyword ", "").split(",")
                keyword = keywords[0]
                response = keywords[1]
                save_keyword(keyword, response)
                await app.send_message(message.from_user.id,
                                       "The keyword {} has been saved with the predefined response: {}".format(keyword,
                                                                                                               response))
            elif message.text.startswith("admin "):
                admin = message.text.replace("admin ", "")
                if promote_admin(admin):
                    await app.send_message(message.from_user.id,
                                           "The user @{} has been promoted as an admin.".format(admin))
                else:
                    await app.send_message(message.from_user.id,
                                           "Sorry! The user @{} has not been promoted as an admin. Please check whether the user is already using this bot.".format(
                                               admin))

            elif message.text.startswith("schedule "):
                minutes = message.text.replace("schedule ", "")
                f_search_query = open(f'data/schedule.txt', "w+")
                f_search_query.write(f"{''.join(minutes)}")
                f_search_query.close()
                logger.error("Scheduled message will be set in each {} minutes".format(minutes))
                await app.send_message(message.from_user.id,
                                       "Thank you! The scheduled message will be set in each {} minutes".format(
                                           minutes))

            else:
                getAnswer = get_answer(message.text)
                if getAnswer:
                    await app.send_message(message.from_user.id, f'{getAnswer}')
                else:
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
                    save_message(messageObj)

    except Exception as e:
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))
        logger.error(e)
        pass


@app.on_message(filters.private & filters.command(['start'], ['/']), group=2)
async def start(Client, message):
    if isAdmin(message):
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=f"Schedules", callback_data=f"!allshedules"),
                    InlineKeyboardButton(text=f"Keywords", callback_data=f"!allkeywords"),
                    InlineKeyboardButton(text=f"Users", callback_data=f"!allusers"),
                    InlineKeyboardButton(text=f"Admins", callback_data=f"!alladmins")
                ],
                [
                    InlineKeyboardButton(text=f"Add new scheduled message", callback_data=f"!newschedule")
                ],
                [
                    InlineKeyboardButton(text=f"Add new keyword", callback_data=f"!newkeyword")
                ],
                [
                    InlineKeyboardButton(text=f"Add new Admin", callback_data=f"!addNewAdmin")
                ],
                [
                    InlineKeyboardButton(text=f"Start training", callback_data=f"!train")
                ]
            ]
        )
        await app.send_message(message.from_user.id,
                               f'Hi {message.from_user.mention}\n\n<i>Choose one of the option below.</i>',
                               reply_markup=keyboard)
    else:
        await app.send_message(message.from_user.id,
                               f'You are not allowed to use admin functions {message.from_user.mention}')


def showAllUsers():
    rows = []
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.count_documents({"level": 0}) > 100:
                logger.error("Too many users")
                return InlineKeyboardMarkup(rows)
            if usersCollection.count_documents({"level": 0}) <= 0:
                logger.error("No users")

            else:
                logger.error("Retrieving users to fetch...")
                for user in usersCollection.find({"level": 0}):
                    row = [
                        InlineKeyboardButton(text=f"{user['username']}", callback_data=f"profile {user['username']}"),
                        InlineKeyboardButton(text=f"X Remove", callback_data=f"!remove {user['username']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def showAllAdmins():
    rows = []
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.count_documents({"level": 1}) > 100:
                logger.error("Too many admins")
                return InlineKeyboardMarkup(rows)
            if usersCollection.count_documents({"level": 1}) <= 0:
                logger.error("No admins")

            else:
                logger.error("Retrieving admins to fetch...")
                for user in usersCollection.find({"level": 1}):
                    row = [
                        InlineKeyboardButton(text=f"{user['username']}", callback_data=f"profile {user['username']}"),
                        InlineKeyboardButton(text=f"X Remove", callback_data=f"!remove {user['username']}")
                    ]
                    rows.append(row)
                print(rows)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def showAllKeywords():
    rows = []
    try:
        if dbConnection:
            keywordsCollection = dbConnection.get_collection("answers")
            if keywordsCollection.count_documents({"isKeyword": 1}) > 100:
                logger.error("Too many keywords")
                return InlineKeyboardMarkup(rows)
            if keywordsCollection.count_documents({"isKeyword": 1}) <= 0:
                logger.error("No keywords")

            else:
                logger.error("Retrieving keywords to fetch...")
                for keyword in keywordsCollection.find({"isKeyword": 1}):
                    row = [
                        InlineKeyboardButton(text=f"{keyword['question']}", callback_data=f""),
                        InlineKeyboardButton(text=f"X", callback_data=f"!removeKeyword {keyword['question']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return InlineKeyboardMarkup(rows)
    except Exception as er:
        logger.error(er)
        return InlineKeyboardMarkup(rows)


@app.on_callback_query(group=2)
async def callback_query(Client, Query):
    try:
        if isAdmin(Query):
            if Query.data == "!allkeywords":
                await Query.message.edit(f'All Keywords:', reply_markup=showAllKeywords())

            elif Query.data == "!allshedules":
                scheduled = open(f'data/schedule.txt', "r").read()
                await app.send_message(Query.from_user.id,
                                       f'The scheduled message will be sent in each {scheduled} minutes')

            elif Query.data == "!allusers":
                await Query.message.edit(f'All Users:', reply_markup=showAllUsers())

            elif Query.data == "!alladmins":
                await Query.message.edit(f'All Admins:', reply_markup=showAllAdmins())

            elif Query.data == "!addNewAdmin":
                await Query.message.edit(
                    f'Please add new admin like this: <b> admin username </b> \nExample: '
                    f'admin john.')

            elif Query.data.startswith("!remove "):
                user = Query.data.replace("!remove ", "")
                if remove_admin(user):
                    await Query.message.edit(
                        f"User @{user} removed from admin role.")
                else:
                    await Query.message.edit(
                        f"Sorry, failed to remove @{user} from admin role.")

            elif Query.data == "!train":
                await Query.message.edit(
                    f"Please teach me like this: <b> learn Question, Answer </b> \nExample: learn Hi, Hi how are you?")
            elif Query.data == "!newkeyword":
                await Query.message.edit(
                    f"Please add keywords like this: <b> keyword Keyword_name, Response </b> \nExample: keyword contact, Please contact +947123456 our hotline.")
            elif Query.data == "!newschedule":
                await Query.message.edit(
                    f"Please change the schedule like this: <b> schedule Minutes </b> \nExample: schedule 30 (The scheduled message will be sent in each 30 minutes)")

        else:
            await app.send_message(Query.from_user.id, f'You are not allowed to use the bot @{Query.from_user.mention}')

    except Exception as e:
        logger.error(e)
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))
        pass


async def scheduledJob():
    try:
        logger.info("Scheduled message")
        await app.send_message('1664758714', 'Scheduled Message')
        return True
    except Exception as e:
        logger.error(e)
        return False


# start polling to continuously listen for messages
if os.path.isfile(f'data/schedule.txt') and schedule > 0:
    schedule = open(f'data/schedule.txt', "r").read()
    scheduler = AsyncIOScheduler()
    scheduler.add_job(scheduledJob, "interval", minutes=int(schedule))
    scheduler.start()

logger.error("Poling started...")
app.run()