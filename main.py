import os
import telebot
from cfonts import render
import requests

bot_token = "7024639328:AAGQLb2VrBPK7sJ7rQVxM3zgBY3hZMMNyGM"

bot = telebot.TeleBot(bot_token)

apiurl = "https://api.classplusapp.com"
headers = {
    'Host': 'api.classplusapp.com',
    'x-access-token': '',
    'user-agent': 'Mobile-Android',
    'app-version': '1.4.65.3',
    'api-version': '29',
    'device-id': 'f84b35cfafd42686',
    'device-details': 'xiaomi_Mi 9T Pro_SDK-29',
    'region': 'IN',
    'x-chrome-version': '108.0.5359.128',
    'webengage-luid': '00000185-717d-b94d-b2a5-f576008be3cf',
    'accept-language': 'EN',
    'content-type': 'application/json',
    'build-number': '29',
    'accept-encoding': 'gzip'
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, render("ClassPlus Bot", colors=['cyan', 'white'], align='center'))

@bot.message_handler(func=lambda message: True)
def process_message(message):
    chat_id = message.chat.id
    raw_text = message.text.strip()

    if raw_text.startswith("**OrgID*Mobile**"):
        mob = raw_text.replace("**OrgID*Mobile**", "").strip()
        if len(mob) < 30:
            orgid = mob.split("*")[0]
            mobil = mob.split("*")[1]

            resp = requests.get(f'{apiurl}/v2/orgs/{orgid}').json()
            orgcode = resp["data"]["orgId"]
            orgname = resp["data"]["orgName"]

            head2 = {
                'authority': 'api.classplusapp.com',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json;charset=UTF-8',
                'device-id': '1672380179181',
                'origin': 'https://web.classplusapp.com',
                'pragma': 'no-cache',
                'referer': 'https://web.classplusapp.com/',
                'mobile-agent': 'Mobile-Android'
            }
            info = {
                'countryExt': '91', 'orgCode': orgname, 'viaSms': '1', 'viaEmail': '0', 'retry': 0, 'orgId': orgcode,
                'otpCount': 0, 'mobile': mobil
            }
            resp = requests.post(f'{apiurl}/v2/otp/generate', json=info, headers=head2)
            if "OTP code sent" in resp.text:
                sesid = resp.json()["data"]["sessionId"]
                bot.send_message(chat_id, "Enter OTP received on mobile:")
                # Now you need to implement a way to capture OTP from the user and proceed accordingly
            else:
                bot.send_message(chat_id, "OTP code generation failed. Please check your input.")
        else:
            bot.send_message(chat_id, "Invalid input format. Please follow the format: **OrgID*Mobile**")

    elif raw_text.startswith("**Now send the Batch ID to Download** :"):
        raw_text2 = raw_text.replace("**Now send the Batch ID to Download** :", "").strip()
        # Now you need to implement the logic to process the batch ID and perform necessary actions
        bot.send_message(chat_id, "Processing batch ID...")

    else:
        bot.send_message(chat_id, "Invalid command. Please enter a valid command.")

bot.polling()