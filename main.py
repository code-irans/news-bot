from telebot import *
import requests
from bs4 import BeautifulSoup
import time
import json
import glob
import os


# ---------------------------------------------- #

AUTH_TOKEN = "1990105739:AAG5fSP_vdeRGlNnXTfzH9bOvm8kJe9ZygA"

Admin = 1743652832

bot = TeleBot(AUTH_TOKEN)

# ---------------------------------------------- #


# Start Functions # 

def Get_News():
    url = "https://www.tasnimnews.com/"
  
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')
    soup = soup.find_all("h4", class_ = "lead")

    return soup

def Save_User(id, user, name):
    A = open("users/" + str(id) + ".json", "w")
    B = open("users/" + str(id) + ".json", "r+")

    B.truncate(0)

    data = {
        "chat_id":id,
        "user_name":user,
        "full_name":name,
    }

    json.dump(data, A)

def Delete_User(id):
    os.remove("users/" + str(id) + ".json")

# End Functions # 


@bot.message_handler()
def MainBot(user):
    # Start from about user #
    text = user.text
    Chat_ID = user.chat.id
    username = user.chat.username
    first_name = user.chat.first_name
    last_name = user.chat.last_name
    full_name = first_name + " " + last_name
    # End from about user #

    def help_user():
        bot.send_message(Chat_ID, """
سلام اینم لیست کار هایی که ربات میکنه
✅ /news بدست اوردن اخبار روز از API معتبر
✅ /remove_user پاک کردن کاربر
✅ /register ثبت نام در ربات
✅ /support : پشتیبانی ربات
✅ /help : درباره ربات
        """)

    if text == "/start":
        bot.send_message(Chat_ID, "سلام {} به ربات خبر اول خوش امدی".format(full_name))
        Save_User(Chat_ID, username, full_name)
        time.sleep(2)
        bot.send_message(Chat_ID, "برای دیدن دستورات /help را وارد کنید")

    elif text == "/remove_user":
        Delete_User(Chat_ID)
        bot.reply_to(user, "کاربر گرامی شما از دیتابیس پاک شدی برا ثبت نام دوباره دستور /register بزنید")
        bot.send_message(Chat_ID, "برای دیدن دستورات /help را وارد کنید")

    elif text == "/register":
        Save_User(Chat_ID, username, full_name)
        bot.send_message(Chat_ID, "کاربر {} شما ثبت نام شدی".format(str(Chat_ID)))
        bot.send_message(Chat_ID, "برای دیدن دستورات /help را وارد کنید")

    elif text == "/help":
        help_user()
    
    elif text == "/support":
        KEY = json.load(open("about.json"))
        num = KEY['name'] + " " + KEY['family']

        bot.send_message(Chat_ID, """
سلام من {} هستم مدیر و برنامه نویس خبر اول
در صورت مشکل با پشتیبانی {} صحبت کنید
        """.format(num, KEY['username']))

        bot.send_message(Chat_ID, "برای دیدن دستورات /help را وارد کنید")

    elif text == "/panel":
        if Chat_ID == Admin:
            bot.send_message(Chat_ID, "سلام مدیر عزیز خوش امدی.")

            bot.send_message(Chat_ID, "برای گرفتن لیست کاربران لطفا صبر کنید...")
            time.sleep(5)

            list_file = glob.glob("users/*.json")

            for Me_File in list_file:
                open_file = json.load(open(Me_File, "r"))
                bot.send_message(Chat_ID, """
نام : {}
نام کاربری : {}
شناسه : {}
\n
با تشکر از برنامه نویس عزیز
                """.format(
                    open_file['full_name'],
                    open_file['user_name'],
                    open_file['chat_id']
                ))



        else:
            bot.reply_to(user, "سلام متسفانه شما مدیر نیستی. برای مدیر شدن با پشتیبانی {} صحبت کنید".format("/support"))


    elif text == "/news":
        news = Get_News()
     
        for body in news:
            bot.send_message(Chat_ID, body)

        bot.send_message(Chat_ID, "برای دیدن دستورات /help را وارد کنید")


    else:
        bot.reply_to(user, "دستور اشتباه میباشد!")
        time.sleep(2)
        help_user()

    

bot.polling(True)