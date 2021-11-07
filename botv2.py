import json
import logging
import logging.handlers as handlers
import os
import psycopg2
import time
from threading import Thread
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from psycopg2 import connect
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date, datetime

app = Client("bot", bot_token="1535754539:AAFSUHbk8Jg471SwOXO1AiFtr0sYnHsZ1e0", parse_mode="combined")
setWebhook = "https://api.telegram.org/bot1535754539:AAFSUHbk8Jg471SwOXO1AiFtr0sYnHsZ1e0/setWebhook?url=https://gvdhne9dy9.execute-api.us-east-2.amazonaws.com/default/BotFunction"
removeWebhook = "https://api.telegram.org/bot1535754539:AAFSUHbk8Jg471SwOXO1AiFtr0sYnHsZ1e0/setWebhook?url="
scheduleSeconds = 3300
channelID = '-1001667880134'
current_database_year = "2020"

formatter = logging.Formatter(
    '%(asctime)s * %(name)s * %(levelname)s * [%(filename)s:%(lineno)s  %(funcName)20s() ] %(message)s')
logger = logging.getLogger()
logHandler = handlers.TimedRotatingFileHandler('/home/ubuntu/intelb_bot/logs/logger.log', when='M', interval=53,
                                               backupCount=24)
logHandler.setLevel(logging.ERROR)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


async def sendTrigger(userId, userName, query):
    try:
        msg = "User: {} @{} \nQuery: <code>{}</code>".format(userId, userName, query)
        await app.send_message(channelID, msg)
        db = connect()
        cur = db.cursor()
        sql = f"UPDATE users SET search_count = search_count + 1 WHERE username = '{userName}'"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)
        print(e)


def getSupportText(key):
    try:
        f = open('supportText.json', "r")
        data = json.loads(f.read())
        f.close()
        return str(data[key])
    except Exception as e:
        logger.error(e)


def schedule(delayInSeconds):
    try:
        requests.get(url=removeWebhook)
        thread1 = Thread(target=shutdown, args=(delayInSeconds,))
        thread1.start()
        return True
    except Exception as e:
        logger.error(e)
        return False


def shutdown(delayInSeconds):
    try:
        time.sleep(delayInSeconds)  # Delay for 1 minute (60 seconds).
        requests.get(url=setWebhook)
        os.system("sudo shutdown now")
    except Exception as e:
        logger.error(e)
        return False


try:
    # schedule(scheduleSeconds)
    f = open(f'/home/ubuntu/intelb_bot/data/scheduler.txt', 'w')
    f.write(str(int(time.time())))
    f.close()
    logger.info("Scheduled to be stopped in {} seconds".format(scheduleSeconds))
except Exception as er:
    logger.error(er)


def connect():
    try:
        return psycopg2.connect(
            host="localhost",
            user="intelilb_bot",
            password="NamePros414255",
            database="intelilb_bot"
        )

    except Exception as e:
        logger.error("Database Error : {}".format(e))


def register_user(user_id, username):
    try:
        db = connect()
        cur = db.cursor()
        sql = f"INSERT INTO users (id, rank, username, search_count) VALUES ({user_id}, 0, '{username}', 0) ON CONFLICT (id) DO UPDATE SET username = '{username}';"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()

        update_user(user_id, username)

    except Exception as e:
        logger.error(e)


def add_user(username):
    try:
        db = connect()
        cur = db.cursor()
        if username.isdigit():
            sql = f"UPDATE users SET rank = 1 WHERE id = {int(username)}"
        else:
            sql = f"UPDATE users SET rank = 1 WHERE username = '{username}'"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)


def update_user(user_id, username):
    try:
        db = connect()
        cur = db.cursor()
        sql = f"UPDATE users SET username = '{username}' WHERE id = {user_id}"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)


def remove_user(username):
    try:
        db = connect()
        cur = db.cursor()
        if username.isdigit():
            sql = f"UPDATE users SET rank = 0 WHERE id = {int(username)}"
        else:
            sql = f"UPDATE users SET rank = 0 WHERE username = '{username}'"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)


def add_admin(username):
    try:
        db = connect()
        cur = db.cursor()
        if username.isdigit():
            sql = f"UPDATE users SET rank = 2 WHERE id = {int(username)}"
        else:
            sql = f"UPDATE users SET rank = 2 WHERE username = '{username}'"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)


def show_all_admins():
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT * FROM users WHERE rank = 2"
        cur.execute(sql)
        res = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        if res is not None:
            return res
        else:
            return None
    except Exception as e:
        logger.error(e)


def show_all_non_users():
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT * FROM users WHERE rank = 0"
        cur.execute(sql)
        res = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        if res is not None:
            return res
        else:
            return None
    except Exception as e:
        logger.error(e)


def show_all_users():
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT * FROM users WHERE rank = 1"
        cur.execute(sql)
        res = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        if res is not None:
            return res
        else:
            return None
    except Exception as e:
        logger.error(e)


def remove_admin(username):
    try:
        db = connect()
        cur = db.cursor()
        if username.isdigit():
            sql = f"UPDATE users SET rank = 1 WHERE id = {int(username)}"
        else:
            sql = f"UPDATE users SET rank = 1 WHERE username = '{username}'"
        cur.execute(sql)
        db.commit()
        cur.close()
        db.close()
    except Exception as e:
        logger.error(e)


def is_user(user_id):
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT * FROM users WHERE id = {user_id} AND rank > 0"
        cur.execute(sql)
        count = cur.rowcount
        db.commit()
        cur.close()
        db.close()
        if count > 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)


def is_visited(username):
    try:
        db = connect()
        cur = db.cursor()
        if username.isdigit():
            sql = f"SELECT * FROM users WHERE id = {int(username)}"
        else:
            sql = f"SELECT * FROM users WHERE username = '{username}'"
        cur.execute(sql)
        count = cur.rowcount
        db.commit()
        cur.close()
        db.close()
        if count > 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)


def is_admin(user_id):
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT * FROM users WHERE id = {user_id} AND rank > 1"
        cur.execute(sql)
        count = cur.rowcount
        db.commit()
        cur.close()
        db.close()
        if count > 0:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False


def search_in_db(query, current_database):
    try:
        db = connect()
        cur = db.cursor()
        if query is not None and len(query.strip()) > 0:
            sql = f"SELECT * FROM carmdi{current_database} WHERE {query} LIMIT 95"
            logger.error(sql)
            # val = (query,)
            cur.execute(sql)
            res = cur.fetchall()
            db.commit()
            cur.close()
            db.close()
            if res is not None:
                return res
            else:
                return None
        else:
            return None
    except Exception as e:
        logger.error(e)


def get_columns_names(table, current_database):
    try:
        db = connect()
        cur = db.cursor()
        sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}';"
        # val = (query,)
        cur.execute(sql)
        res = cur.fetchall()
        db.commit()
        cur.close()
        db.close()
        if res is not None:
            return res
        else:
            return None
    except Exception as e:
        logger.error(e)


def count_row_db(query, current_database):
    try:
        db = connect()
        cur = db.cursor()
        if query is not None and len(query.strip()) > 0:
            sql = f"SELECT COUNT(*) FROM carmdi{current_database} WHERE {query}"
            logger.error(sql)
            cur.execute(sql)
            count = cur.fetchone()[0]
            cur.close()
            db.close()
            return int(count)
        else:
            return 0
    except Exception as e:
        logger.error(e)


@app.on_message(filters.private)
async def check_msg(Client, message):
    try:
        dateS = message['message']['date']
        dateSent = datetime.fromtimestamp(dateS)
        minutes_diff = (datetime.now() - dateSent).total_seconds() / 60.0

        if message.from_user.id == 1535754539 or minutes_diff > 3:
            message.stop_propagation()
        elif message.from_user.username == 'None':
            await app.send_message(message.from_user.id, ''
                                                         'ðŸ¤– Oopz! Your telegram account does not have a username. Please check your profile and try again.')
            message.stop_propagation()

        elif not is_user(message.from_user.id) and message.from_user.id != 1535754539:
            register_user(message.from_user.id, message.from_user.username)
            await sendTrigger(message.from_user.id, message.from_user.username, f"UNAUTHORIZED ATTEMPT TO USE BOT")
            await app.send_message(message.from_user.id, ''
                                                         'ðŸ¤– You are not able to use this bot!')
            message.stop_propagation()

        else:
            register_user(message.from_user.id, message.from_user.username)

    except Exception as e:
        logger.error(e)
        pass


@app.on_message(filters.private & filters.command(['help'], ['/']), group=2)
async def helpMenuFunc(Client, message):
    if is_admin(message.from_user.id):
        helpMenu = f" <b> HELP TOPICS </b> " \
                   f"\n\n âœ” /admin : Admin Configurations." \
                   f"\n\n âœ” /start : Wake up the bot and start using it." \
                   f"\n\n âœ” /help : Help topics." \
                   f"\n\n âœ” /showusers : Show Users" \
                   f"\n\n âœ” /showadmins : Show Admins" \
                   f"\n\n âœ” /adduser username" \
                   f"\n\n âœ” /addadmin username" \
                   f"\n\n âœ” /removeuser username" \
                   f"\n\n âœ” /removeadmin username"
    else:
        helpMenu = f" <b> HELP TOPICS </b> " \
                   f"\n\n âœ” /start : Wake up the bot and start using it." \
                   f"\n\n âœ” /help : Help topics." \
                   f"\n\n <i>Please note that some of the admin functionalities are not listed here.</i>"
    await app.send_message(message.from_user.id, helpMenu)


@app.on_message(filters.private & filters.command(['adduser'], ['/']), group=2)
async def adduser(Client, message):
    if is_admin(message.from_user.id) and len(message.text.split(' ')) == 2:
        username = message.text.replace('/adduser ', '')
        if is_visited(username):
            add_user(username)
            await app.send_message(message.from_user.id, f'New user {username} added!')
            await sendTrigger(message.from_user.id, message.from_user.username, f'New user {username} added!')
        else:
            await app.send_message(message.from_user.id,
                                   f'User {username} has never used this bot. Ask them to say Hi @Intelb_bot')
    else:
        await app.send_message(message.from_user.id, f'Invalid request. /help')


@app.on_message(filters.private & filters.command(['errors'], ['/']), group=2)
async def errors(Client, message):
    if is_admin(message.from_user.id):
        errors = ""
        with open(f'/home/ubuntu/intelb_bot/logs/logger.log') as file:

            # loop to read iterate
            # last n lines and print it
            for line in (file.readlines()[-10:]):
                errors = errors + line

        await app.send_message(message.from_user.id, f'ERRORS: <pre> {errors} </pre>')
    else:
        await app.send_message(message.from_user.id, f'Unauthorised. /help')


@app.on_message(filters.private & filters.command(['removeuser'], ['/']), group=2)
async def removeuser(Client, message):
    if is_admin(message.from_user.id) and len(message.text.split(' ')) == 2:
        username = message.text.replace('/removeuser ', '')
        remove_user(username)
        await app.send_message(message.from_user.id, f'User {username} removed!')
        await sendTrigger(message.from_user.id, message.from_user.username, f'User {username} removed!')
    else:
        await app.send_message(message.from_user.id, f'Invalid request. /help')


@app.on_message(filters.private & filters.command(['addadmin'], ['/']), group=2)
async def addadmin(Client, message):
    if is_admin(message.from_user.id) and len(message.text.split(' ')) == 2:
        username = message.text.replace('/addadmin ', '')
        if is_visited(username):
            add_admin(username)
            await app.send_message(message.from_user.id, f'New admin {username} added!')
            await sendTrigger(message.from_user.id, message.from_user.username, f'New admin {username} added!')
        else:
            await app.send_message(message.from_user.id,
                                   f'User {username} has never used this bot. Ask them to say Hi @Intelb_bot')
    else:
        await app.send_message(message.from_user.id, f'Invalid request. /help')


@app.on_message(filters.private & filters.command(['removeadmin'], ['/']), group=2)
async def removeadmin(Client, message):
    if is_admin(message.from_user.id) and len(message.text.split(' ')) == 2:
        username = message.text.replace('/removeadmin ', '')
        remove_admin(username)
        await app.send_message(message.from_user.id, f'Admin {username} removed!')
        await sendTrigger(message.from_user.id, message.from_user.username, f'Admin {username} removed!')
    else:
        await app.send_message(message.from_user.id, f'Invalid request. /help')


@app.on_message(filters.private & filters.command(['showusers'], ['/']), group=2)
async def showusers(Client, message):
    try:
        if is_admin(message.from_user.id):
            await sendTrigger(message.from_user.id, message.from_user.username, "SHOW ALL USERS")
            users = show_all_users()
            logger.error("Show users {}".format(str(len(users))))
            if int(len(users)) <= 95:
                buttons = []

                for count_row, user in enumerate(users):
                    buttonRow = [
                        InlineKeyboardButton(text="{}".format(user[0]),
                                             callback_data="!showAdmin {}".format(user[3])),
                        InlineKeyboardButton(text="{}".format(user[3]),
                                             callback_data="!showUser {}".format(user[3])),
                        InlineKeyboardButton(text="ðŸ” {}".format(user[2]),
                                             callback_data="!showAdmin {}".format(user[3]))
                    ]
                    buttons.append(buttonRow)

                keyboard = InlineKeyboardMarkup(buttons)
                await app.send_message(message.from_user.id, f'<b> All Users </b>\n select an option',
                                       reply_markup=keyboard)
            elif int(len(users)) > 95:
                await app.send_message(message.from_user.id, f'<b> Too many users </b>\n Please add filters')
            else:
                await app.send_message(message.from_user.id, f'<b> No Users </b>\n Add new user via /addnewuser')

    except Exception as e:
        logger.error(e)


@app.on_message(filters.private & filters.command(['showadmins'], ['/']), group=2)
async def showadmins(Client, message):
    try:
        if is_admin(message.from_user.id):
            await sendTrigger(message.from_user.id, message.from_user.username, "SHOW ALL ADMINS")
            users = show_all_admins()
            logger.error("Show admins {}".format(str(len(users))))
            if int(len(users)) <= 95:
                buttons = []

                for count_row, user in enumerate(users):
                    buttonRow = [
                        InlineKeyboardButton(text="{}".format(user[0]),
                                             callback_data="!showAdmin {}".format(user[3])),
                        InlineKeyboardButton(text="{}".format(user[3]),
                                             callback_data="!showAdmin {}".format(user[3])),
                        InlineKeyboardButton(text="ðŸ” {}".format(user[2]),
                                             callback_data="!showAdmin {}".format(user[3]))
                    ]
                    buttons.append(buttonRow)

                keyboard = InlineKeyboardMarkup(buttons)
                await app.send_message(message.from_user.id, f'<b> All Admins </b>\n select an option',
                                       reply_markup=keyboard)
            elif int(len(users)) > 95:
                await app.send_message(message.from_user.id, f'<b> Too many admins </b>\n Please add filters')
            else:
                await app.send_message(message.from_user.id, f'<b> No Admins </b>\n Add new admin via /addnewadmin')

    except Exception as e:
        logger.error(e)


@app.on_message(filters.private & filters.command(['admin'], ['/']), group=2)
async def manageBot(Client, message):
    if is_admin(message.from_user.id):
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Show Users", callback_data=f"!showUsers")
                ],
                [
                    InlineKeyboardButton(text="Show Admins", callback_data=f"!showAdmins")
                ]
            ]
        )
        await app.send_message(message.from_user.id,
                               f'<b> Manage Bot </b> \n <i>Choose one of the option below.</i>',
                               reply_markup=keyboard)
    else:
        logger.error("Non admin {} tried to manage bot.".format(message.from_user.id))
        await app.send_message(message.from_user.id, 'ðŸ¤– You are not allowed to manage this bot!')
        message.stop_propagation()


@app.on_message(filters.private & filters.command(['start'], ['/']), group=2)
async def start(Client, message):
    if not is_user(message.from_user.id) and message.from_user.username == 'None':
        message.stop_propagation()
        return

    f1 = open(f'/home/ubuntu/intelb_bot/data/{message.from_user.id}_search_query.txt', 'w+')
    f2 = open(f'/home/ubuntu/intelb_bot/data/{message.from_user.id}_database.txt', "w+")
    current_database = open(f'/home/ubuntu/intelb_bot/data/{message.from_user.id}_database.txt', "r").read().split(" ")[
        0]
    f2.write(current_database)
    f2.close()

    if not current_database or current_database.replace(" ", "") == "":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Select Default DB", callback_data=f"!changedb")
                ]
            ]
        )
    else:
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="ðŸ” SEARCH IN DB {} ðŸ”".format(str(current_database)),
                                         callback_data=f"!searchindb")
                ],
                [
                    InlineKeyboardButton(text="Change Default DB", callback_data=f"!changedb")
                ]
            ]
        )
    await app.send_message(message.from_user.id,
                           f'Hi {message.from_user.mention}\n\n<i>Choose one of the option below.</i>',
                           reply_markup=keyboard)


@app.on_message(filters.private, group=2)
async def insert_query(Client, message):
    try:
        f_status = open(f'/home/ubuntu/intelb_bot/data/{message.from_user.id}_status.txt', 'r+')
        if f_status.read() == 'SEARCH':
            f_status.write("START")
            f_status.close()

            f_column_name = open(f'/home/ubuntu/intelb_bot/data/{message.from_user.id}_column.txt', 'r+')

            column_name = f_column_name.read()

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Is",
                                             callback_data=f"!search translate({column_name}, '-', '') = '{message.text}'")
                    ],
                    [
                        InlineKeyboardButton(text="Contain",
                                             callback_data=f"!search translate({column_name}, '-', '') ILIKE '%{message.text}%'")
                    ],
                    [
                        InlineKeyboardButton(text="Starts With",
                                             callback_data=f"!search translate({column_name}, '-', '') ILIKE '{message.text}%'")
                    ],
                    [
                        InlineKeyboardButton(text="Ends With",
                                             callback_data=f"!search translate({column_name}, '-', '') ILIKE '%{message.text}'")
                    ],
                    [
                        InlineKeyboardButton(text="Does Not Contain",
                                             callback_data=f"!search translate({column_name}, '-', '') NOT ILIKE '%{message.text}%'")
                    ],
                ]
            )

            f_column_name.write('')
            f_column_name.close()

            await app.send_message(message.from_user.id,
                                   f'Ok {message.from_user.mention}, choose the search operator from the options below:',
                                   reply_markup=keyboard)
    except Exception as e:
        logger.error(e)
        await app.send_message(message.from_user.id, f'Something went wrong. Please try a different filter.')


@app.on_callback_query(group=2)
async def callback_query(Client, Query):
    try:
        current_database_year = \
            open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "r").read().split(" ")[0]
        if current_database_year is None:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="2016", callback_data=f"!changedb 2016"),
                        InlineKeyboardButton(text="2017", callback_data=f"!changedb 2017")
                    ],
                    [
                        InlineKeyboardButton(text="2018", callback_data=f"!changedb 2018"),
                        InlineKeyboardButton(text="2020", callback_data=f"!changedb 2020")
                    ]
                ]
            )
            await Query.message.edit(f'Select default DB:', reply_markup=keyboard)

        if Query.data.startswith("!search "):
            search_query = Query.data.replace('!search ', '').replace('â‰ƒ', ' ')
            if os.stat(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt').st_size != 0:
                column_name = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_column.txt', 'r+').read()
                f_search_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "a")
                f_search_query.write(f" AND {search_query}")
                f_search_query.close()
            else:
                column_name = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_column.txt', 'r+').read()
                f_search_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "w")
                f_search_query.write(search_query)
                f_search_query.close()
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ðŸ” Filter Again ðŸ”", callback_data=f"!searchindb"),
                        InlineKeyboardButton(text="ðŸ”™ Back ðŸ”™", callback_data=f"!removeLastQuery")
                    ],
                    [
                        InlineKeyboardButton(text="âŒ Cancel âŒ", callback_data=f"!cancel"),
                        InlineKeyboardButton(text="âœ… Show Results âœ…", callback_data=f"!showresults")
                    ],
                    [
                        InlineKeyboardButton(text="Extend Search to older DB's", callback_data=f"!extend")
                    ]
                ]
            )
            try:
                current_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r").read()
                modified_string = current_query.replace("translate(", "").replace(")", "").replace("-/@", "").replace(
                    "'",
                    "").replace(
                    ",", "")

                if current_database_year == "2019":
                    row_count = count_row_db(current_query, current_database_year)
                else:
                    row_count = count_row_db(current_query.replace('"', ''), current_database_year)

                logger.error(current_query)

                await Query.message.edit(
                    f'Ok {Query.from_user.mention}, what you want to do now?\n\nThe query: <code>{modified_string.replace("ILIKE", "LIKE")} from carmdi{str(current_database_year)}</code> returned {row_count} results\n\n<i>Choose one of the option below:</i>',
                    reply_markup=keyboard)
                await sendTrigger(Query.from_user.id, Query.from_user.username,
                                  f'<code>{modified_string.replace("ILIKE", "LIKE")} from carmdi{str(current_database_year)}</code> returned {row_count} results')
            except Exception as e:
                logger.error(e)
                pass

        if Query.data == "!searchindb":
            button = []
            # for column_name in get_columns_names("carmdi"):
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ”¢ ActualNB", callback_data=f"!select_column \"ActualNB\""),
                    InlineKeyboardButton(text="Letter ðŸ†Ž", callback_data=f"!select_column \"CodeDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ“… Year Produced", callback_data=f"!select_column \"PRODDATE\""),
                    InlineKeyboardButton(text="Chassis Number ðŸ” ðŸ”¢", callback_data=f"!select_column \"Chassis\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ”¢ðŸ”  Motor Number", callback_data=f"!select_column \"Moteur\""),
                    InlineKeyboardButton(text="Date Aqquired ðŸ“†", callback_data=f"!select_column \"dateaquisition\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸŒˆ Colour", callback_data=f"!select_column \"CouleurDesc\""),
                    InlineKeyboardButton(text="Brand ðŸš—", callback_data=f"!select_column \"MarqueDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸŽ Model", callback_data=f"!select_column \"TypeDesc\""),
                    InlineKeyboardButton(text="Utility Type ðŸš–", callback_data=f"!select_column \"UtilisDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ™‹â€â™‚ First Name", callback_data=f"!select_column \"Prenom\""),
                    InlineKeyboardButton(text="Last Name ðŸ‘¨â€ðŸ‘¨â€ðŸ‘§â€ðŸ‘§",
                                         callback_data=f"!select_column \"Nom\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ  Address", callback_data=f"!select_column \"Addresse\""),
                    InlineKeyboardButton(text="Mother's Name ðŸ¤°", callback_data=f"!select_column \"NomMere\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ“± Phone Number", callback_data=f"!select_column \"TelProp\""),
                    InlineKeyboardButton(text="Civil Number ðŸ“œ", callback_data=f"!select_column \"NoRegProp\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ‘¶ Birthplace ðŸ‘¶", callback_data=f"!select_column \"BirthPlace\"")
                ]
            )

            button.append([InlineKeyboardButton(text="âŒ Cancel âŒ", callback_data="!cancel")])

            file = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r")
            current_query = file.read()
            file.close()
            new_query = current_query.split("ILIKE")
            if len(new_query) > 1:
                button.append([InlineKeyboardButton(text="ðŸ”™ Back ðŸ”™", callback_data=f"!lookBack")])

            keyboard = InlineKeyboardMarkup(button)
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("START")
            f.close()
            await Query.message.edit("Select column name:", reply_markup=keyboard)

        if Query.data.startswith("!select_column "):
            column_name = Query.data.replace("!select_column ", "")
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_column.txt', 'w')
            f.write(column_name)
            f.close()

            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("SEARCH")
            f.close()

            await Query.message.edit("What would you like to search for?")

        if Query.data == "!showresults":
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("START")
            f.close()
            current_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r").read()
            current_databases = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt',
                                     "r").read().split(
                " ")
            search_in_db_r = []

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="BACK", callback_data=f"!cancel")
                    ]
                ]
            )

            # columns_name = get_columns_names("carmdi")
            current_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r").read()
            row_count = count_row_db(current_query.replace('"', ''), current_database_year)

            keyboard2 = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ðŸ” Filter Again ðŸ”", callback_data=f"!searchindb")
                    ]
                ]
            )

            keyboard3 = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ðŸ” Add New Filters ðŸ”", callback_data=f"!removeLastQuery")
                    ]
                ]
            )

            for db in current_databases:
                search_in_db_r = search_in_db(current_query.replace('"', ''), db)

                if search_in_db_r is not None:

                    modified_string = current_query.replace("translate(", "").replace(")", "").replace("-/@",
                                                                                                       "").replace(
                        "'",
                        "").replace(
                        ",", "")

                    if search_in_db_r != None and int(len(search_in_db_r)) == 95:
                        await Query.message.edit(f"Too many results! Please add more filters and try again.",
                                                 reply_markup=keyboard2)

                    elif search_in_db_r != None and int(len(search_in_db_r)) == 0:
                        await Query.message.edit(f"No results! Please change the filters and try again.",
                                                 reply_markup=keyboard3)

                    elif search_in_db_r != None and int(len(search_in_db_r)) < 95 and int(len(search_in_db_r)) != 0:

                        await Query.message.edit(
                            'Results for your query <code> {} FROM CARMDI {}</code> :'.format(
                                str(modified_string.replace("ILIKE", "LIKE")), str(" ".join(current_databases))))
                        for count_row, search_in_db_r_row in enumerate(search_in_db_r):
                            text = f"Plate Number ðŸ”¢: {search_in_db_r_row[0]}\nLetter ðŸ†Ž: {search_in_db_r_row[1]}\nYear Produced ðŸ“…: {search_in_db_r_row[2]}\nChassis Number ðŸ” ðŸ”¢: {search_in_db_r_row[3]}\nMotor Number ðŸ”¢ðŸ” : {search_in_db_r_row[4]}\nDate Aqquired ðŸ“†: {search_in_db_r_row[5]}\nColour ðŸŒˆ: {search_in_db_r_row[7]}\nBrand ðŸš—: {search_in_db_r_row[8]}\nModel ðŸŽ: {search_in_db_r_row[9]}\nUtility Type ðŸš–_: {search_in_db_r_row[10]}\nFirst Name ðŸ™‹â€â™‚: {search_in_db_r_row[11]}\nLast Name ðŸ‘¨â€ðŸ‘¨â€ðŸ‘§â€ðŸ‘§: {search_in_db_r_row[12]}\nAddress ðŸ : {search_in_db_r_row[13]}\nMother's Name ðŸ¤°: {search_in_db_r_row[14]}\nPhone Number ðŸ“±: {search_in_db_r_row[15]}\nCivil Number ðŸ“œ: {search_in_db_r_row[16]}\nBirthplace ðŸ‘¶: {search_in_db_r_row[17]}"

                            """
                            for count_column, search_in_db_r_row_column in enumerate(search_in_db_r_row):
                                if count_column == 0:
                                    text += str(columns_name[count_column][0]) + ": " + str(search_in_db_r_row_column)
                                else:
                                    text += '\n' + str(columns_name[count_column][0]) + ": " + str(search_in_db_r_row_column)
                            """
                            await app.send_message(Query.from_user.id, f"<code>{text}</code>")
                            time.sleep(1)

                        await app.send_message(Query.from_user.id, "<b> ðŸ‘†DONEðŸ‘† </b>", reply_markup=keyboard)

        if Query.data == "!cancel":
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_column.txt', 'w')

            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("START")
            f.close()

            current_database = \
                open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "r").read().split(" ")[0]
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "w")
            f.write(current_database)
            f.close()

            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', 'w')
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ðŸ” SEARCH IN DB {} ðŸ”".format(str(current_database_year)),
                                             callback_data=f"!searchindb")
                    ],
                    [
                        InlineKeyboardButton(text="Change Default DB", callback_data=f"!changedb")
                    ]
                ]
            )
            await Query.message.edit(f'Hi {Query.from_user.mention}\n\n<i>Choose one of the option below.</i>',
                                     reply_markup=keyboard)

        if Query.data == "!removeLastQuery":
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_column.txt', 'w')
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("START")
            f.close()

            file = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r")
            current_query = file.read()
            file.close()
            new_query = current_query.split("AND")
            if len(new_query) > 1:
                new_query = new_query[:-1]
                txt = ""
                file = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "w")
                file.write(f"{new_query.pop()}")
                file.close()
                for txt in new_query:
                    file = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "a")
                    file.write(f"AND {txt}")
                    file.close()
            else:
                f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "w")
                f.write("")
                f.close()

            button = []
            # for column_name in get_columns_names("carmdi"):
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ”¢ ActualNB", callback_data=f"!select_column \"ActualNB\""),
                    InlineKeyboardButton(text="Letter ðŸ†Ž", callback_data=f"!select_column \"CodeDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ“… Year Produced", callback_data=f"!select_column \"PRODDATE\""),
                    InlineKeyboardButton(text="Chassis Number ðŸ” ðŸ”¢", callback_data=f"!select_column \"Chassis\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ”¢ðŸ”  Motor Number", callback_data=f"!select_column \"Moteur\""),
                    InlineKeyboardButton(text="Date Aqquired ðŸ“†", callback_data=f"!select_column \"dateaquisition\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸŒˆ Colour", callback_data=f"!select_column \"CouleurDesc\""),
                    InlineKeyboardButton(text="Brand ðŸš—", callback_data=f"!select_column \"MarqueDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸŽ Model", callback_data=f"!select_column \"TypeDesc\""),
                    InlineKeyboardButton(text="Utility Type ðŸš–", callback_data=f"!select_column \"UtilisDesc\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ™‹â€â™‚ First Name", callback_data=f"!select_column \"Prenom\""),
                    InlineKeyboardButton(text="Last Name ðŸ‘¨â€ðŸ‘¨â€ðŸ‘§â€ðŸ‘§",
                                         callback_data=f"!select_column \"Nom\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ  Address", callback_data=f"!select_column \"Addresse\""),
                    InlineKeyboardButton(text="Mother's Name ðŸ¤°", callback_data=f"!select_column \"NomMere\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ“± Phone Number", callback_data=f"!select_column \"TelProp\""),
                    InlineKeyboardButton(text="Civil Number ðŸ“œ", callback_data=f"!select_column \"NoRegProp\"")
                ]
            )
            button.append(
                [
                    InlineKeyboardButton(text="ðŸ‘¶ Birthplace ðŸ‘¶", callback_data=f"!select_column \"BirthPlace\"")
                ]
            )

            button.append([InlineKeyboardButton(text="ðŸ”™ Back ðŸ”™", callback_data=f"!lookBack")])
            keyboard = InlineKeyboardMarkup(button)
            f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_status.txt', 'w')
            f.write("START")
            f.close()
            await Query.message.edit("Select column name:", reply_markup=keyboard)

        if Query.data == "!lookBack":
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ðŸ” Filter Again ðŸ”", callback_data=f"!searchindb"),
                        InlineKeyboardButton(text="ðŸ”™ Back ðŸ”™", callback_data=f"!removeLastQuery")
                    ],
                    [
                        InlineKeyboardButton(text="âŒ Cancel âŒ", callback_data=f"!cancel"),
                        InlineKeyboardButton(text="âœ… Show Results âœ…", callback_data=f"!showresults")
                    ],
                    [
                        InlineKeyboardButton(text="Extend Search to older DB's", callback_data=f"!extend")
                    ]
                ]
            )
            current_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r").read()
            modified_string = current_query.replace("translate(", "").replace(")", "").replace("-/@", "").replace("'",
                                                                                                                  "").replace(
                ",", "")
            if current_database_year == "2019":
                row_count = count_row_db(current_query, current_database_year)
            else:
                row_count = count_row_db(current_query.replace('"', ''), current_database_year)

            await Query.message.edit(
                f'Ok {Query.from_user.mention}, what you want to do now?\n\nThe query: <code>{modified_string.replace("ILIKE", "LIKE")}</code> returned {row_count} results\n\n<i>Choose one of the option below:</i>',
                reply_markup=keyboard)

        if Query.data.startswith("!changedb"):
            if len(Query.data.split(" ")) == 2:
                database_name = Query.data.replace("!changedb ", "")
                f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', 'w')
                f.write(database_name)
                f.close()

                current_database = \
                    open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "r").read().split(" ")[0]
                f = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "w")
                f.write(current_database)
                f.close()

                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="ðŸ” SEARCH IN DB {} ðŸ”".format(str(Query.data.split(" ")[1])),
                                                 callback_data=f"!searchindb")
                        ],
                        [
                            InlineKeyboardButton(text="Change Default DB", callback_data=f"!changedb")
                        ]
                    ]
                )
                await Query.message.edit(
                    "Default DB changed as {}. Select an option:".format(str(Query.data.split(" ")[1])),
                    reply_markup=keyboard)
            else:
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="2015", callback_data=f"!changedb 2015"),
                            InlineKeyboardButton(text="2016", callback_data=f"!changedb 2016"),
                            InlineKeyboardButton(text="2017", callback_data=f"!changedb 2017")
                        ],
                        [
                            InlineKeyboardButton(text="2018", callback_data=f"!changedb 2018"),
                            InlineKeyboardButton(text="2020", callback_data=f"!changedb 2020")
                        ]
                    ]
                )
                await Query.message.edit(f'Select default DB', reply_markup=keyboard)

        if Query.data.startswith("!extend"):
            if len(Query.data.split(" ")) >= 2:
                database_names = Query.data.replace("!extend ", "").split(" ")
                f_search_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "a")
                f_search_query.write(f" {' '.join(database_names)}")
                f_search_query.close()

                current_databases = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt',
                                         "r").read().split(" ")
                current_query = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_search_query.txt', "r").read()
                modified_string = current_query.replace("translate(", "").replace(")", "").replace("-/@", "").replace(
                    "'",
                    "").replace(
                    ",", "")
                row_count = 0
                for db in current_databases:
                    if current_database_year == "2019" or "2019" in database_names:
                        row_count = row_count + int(count_row_db(current_query, db))
                    else:
                        row_count = row_count + int(count_row_db(current_query.replace('"', ''), db))

                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="ðŸ” Filter Again ðŸ”", callback_data=f"!searchindb"),
                            InlineKeyboardButton(text="ðŸ”™ Back ðŸ”™", callback_data=f"!removeLastQuery")
                        ],
                        [
                            InlineKeyboardButton(text="âŒ Cancel âŒ", callback_data=f"!cancel"),
                            InlineKeyboardButton(text="âœ… Show Results âœ…", callback_data=f"!showresults")
                        ],
                        [
                            InlineKeyboardButton(text="Extend Search to older DB's", callback_data=f"!extend")
                        ]
                    ]
                )

                current_database_years = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt',
                                              "r").read()
                await Query.message.edit(
                    f'Ok {Query.from_user.mention}, what you want to do now?\n\n'
                    f'The query: <code>FROM carmdi {current_database_years} {modified_string.replace("ILIKE", "LIKE")}</code> '
                    f'returned {row_count} results\n\n<i>Choose one of the option below:</i>',
                    reply_markup=keyboard)

            else:
                dbs = ['2015', '2016', '2017', '2018', '2020']
                btns = []
                currentdbs = open(f'/home/ubuntu/intelb_bot/data/{Query.from_user.id}_database.txt', "r").read().split(
                    " ")
                for db in dbs:
                    if db not in currentdbs:
                        btns.append(InlineKeyboardButton(text=db, callback_data="!extend {}".format(db)))
                keyboard = InlineKeyboardMarkup(
                    [
                        btns
                    ]
                )

                keyboard2 = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="Back", callback_data=f"!lookBack")
                        ]
                    ]
                )

                if len(btns) > 0:
                    await Query.message.edit(f'Extend your search, select another DB: ', reply_markup=keyboard)
                else:
                    await Query.message.edit(f'You searched in all DBs', reply_markup=keyboard2)

        # if Query.data.startswith("!addUser "):
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!adduser ', '')
        #         if username:
        #             add_user(username)
        #             await sendTrigger(Query.from_user.id, Query.from_user.username, "ADD USER {}".format(username))
        #             await app.send_message(Query.from_user.id, f'New user @{username} added!')
        #
        # if Query.data.startswith("!removeUser "):
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!removeUser ', '')
        #         if username:
        #             remove_user(username)
        #             await sendTrigger(Query.from_user.id, Query.from_user.username, "REMOVE USER {}".format(username))
        #             await app.send_message(Query.from_user.id, f'User @{username} removed!')
        #
        # if Query.data == "!addAdmin ":
        #     print(Query.text)
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!addAdmin ', '')
        #         if username:
        #             add_admin(username)
        #             await sendTrigger(Query.from_user.id, Query.from_user.username, "ADD ADMIN {}".format(username))
        #             await app.send_message(Query.from_user.id, f'Admin permission granted for user @{username} !')
        #
        # if Query.data.startswith("!removeAdmin "):
        #     print(Query.text)
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!removeAdmin ', '')
        #         if username:
        #             remove_admin(username)
        #             await sendTrigger(Query.from_user.id, Query.from_user.username, "REMOVE ADMIN {}".format(username))
        #             await app.send_message(Query.from_user.id, f'Admin permission removed for user @{username} !')

        if Query.data.startswith("!showUsers"):
            try:
                if is_admin(Query.from_user.id):
                    await sendTrigger(Query.from_user.id, Query.from_user.username, "SHOW ALL USERS")
                    users = show_all_users()
                    logger.error("Show users {}".format(str(len(users))))
                    if int(len(users)) <= 95:
                        buttons = []
                        for count_row, user in enumerate(users):
                            buttonRow = [
                                InlineKeyboardButton(text="{}".format(user[0], user[3]),
                                                     callback_data="!showUser {}".format(user[3])),
                                InlineKeyboardButton(text="{}".format(user[3]),
                                                     callback_data="!showUser {}".format(user[3])),
                                InlineKeyboardButton(text="ðŸ” {}".format(user[2]),
                                                     callback_data="!showUser {}".format(user[3]))
                            ]
                            buttons.append(buttonRow)

                        keyboard = InlineKeyboardMarkup(buttons)
                        await Query.message.edit(f'<b> All Users </b>\n select an option', reply_markup=keyboard)
                    elif int(len(users)) > 95:
                        await app.send_message(Query.from_user.id, f'<b> Too many users </b>\n Please add filters')
                    else:
                        await app.send_message(Query.from_user.id, f'<b> No users </b>\n Add new users via /addnewuser')

            except Exception as e:
                logger.error(e)

        if Query.data.startswith("!showAdmins"):
            try:
                if is_admin(Query.from_user.id):
                    await sendTrigger(Query.from_user.id, Query.from_user.username, "SHOW ALL ADMINS")
                    users = show_all_admins()
                    logger.error("Show admins {}".format(str(len(users))))
                    if int(len(users)) <= 95:
                        buttons = []

                        for count_row, user in enumerate(users):
                            buttonRow = [
                                InlineKeyboardButton(text="{}".format(user[0]),
                                                     callback_data="!showAdmin {}".format(user[3])),
                                InlineKeyboardButton(text="{}".format(user[3]),
                                                     callback_data="!showAdmin {}".format(user[3])),
                                InlineKeyboardButton(text="ðŸ” {}".format(user[2]),
                                                     callback_data="!showAdmin {}".format(user[3]))
                            ]
                            buttons.append(buttonRow)

                        keyboard = InlineKeyboardMarkup(buttons)
                        await Query.message.edit(f'<b> All Admins </b>\n select an option', reply_markup=keyboard)
                    elif int(len(users)) > 95:
                        await app.send_message(Query.from_user.id, f'<b> Too many admins </b>\n Please add filters')
                    else:
                        await app.send_message(Query.from_user.id,
                                               f'<b> No Admins </b>\n Add new admin via /addnewadmin')

            except Exception as e:
                logger.error(e)

        if Query.data.startswith('!manageBot'):
            if is_admin(Query.from_user.id):
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="Show Users", callback_data=f"!showUsers")
                        ],
                        [
                            InlineKeyboardButton(text="Show Admins", callback_data=f"!showAdmins")
                        ]
                    ]
                )
                await Query.message.edit(Query.from_user.id,
                                         f'<b> Manage Bot </b> \n <i>Choose one of the option below.</i>',
                                         reply_markup=keyboard)
            else:
                logger.error("Non admin {} tried to manage bot.".format(Query.from_user.id))
                await app.send_message(Query.from_user.id, 'ðŸ¤– You are not allowed to manage this bot!')

        # if Query.data.startswith('!showAdmin '):
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!showAdmin ', '')
        #         keyboard = InlineKeyboardMarkup(
        #             [
        #                 [
        #                     InlineKeyboardButton(text="Remove Admin Permissions",
        #                                          callback_data="!removeAdmin {}".format(username)),
        #                     InlineKeyboardButton(text="Back", callback_data=f"!showAdmins")
        #                 ]
        #             ]
        #         )
        #         await sendTrigger(Query.from_user.username, "VIEW USER ACCOUNT")
        #         await Query.message.edit(Query.from_user.id, f"Choose one of the option below.", reply_markup=keyboard)
        #     else:
        #         logger.error("Non admin {} tried to manage bot.".format(Query.from_user.id))
        #         await app.send_message(Query.from_user.id, 'ðŸ¤– You are not allowed to manage this bot!')

        # if Query.data.startswith('!showUser '):
        #     await sendTrigger(Query.from_user.username, "VIEW USER ACCOUNT")
        #     if is_admin(Query.from_user.id):
        #         username = Query.data.replace('!showUser ', '')
        #         keyboard = InlineKeyboardMarkup(
        #             [
        #                 [
        #                     InlineKeyboardButton(text="Remove User Permissions",
        #                                          callback_data="!removeUser {}".format(username)),
        #                     InlineKeyboardButton(text="Back", callback_data=f"!showUsers")
        #                 ]
        #             ]
        #         )
        #         await Query.message.edit(Query.from_user.id,
        #                                  f'{username} \n Choose one of the option below.',
        #                                  reply_markup=keyboard)
        #     else:
        #         logger.error("Non admin {} tried to manage bot.".format(Query.from_user.id))
        #         await app.send_message(Query.from_user.id, f'ðŸ¤– You are not allowed to manage this bot!')

    except Exception as e:
        logger.error(e)
        print(e)
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))


async def shutdownReminder():
    try:
        timeStarted = int(open(f'/home/ubuntu/intelb_bot/data/scheduler.txt', "r").read())
        now = time.time()
        timeLeft = 55 * 60 - int(now - timeStarted)
        if 20 > timeLeft > 0:
            await app.send_message(channelID, "Bot turns off in {} seconds...".format(timeLeft))
    except Exception as e:
        logger.error(e)


scheduler = AsyncIOScheduler()
scheduler.add_job(shutdownReminder, "interval", seconds=int(15))
scheduler.start()

app.run()
