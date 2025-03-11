import telebot
import time
from datetime import datetime

# Токен берётся из переменной окружения (Heroku Config Vars)
import os
TOKEN = os.getenv("7643599912:AAFHQv96CzWOZotSd1sDufCuZseZNEwzWfo")
CHAT_START_TIME = {}
USER_MESSAGES = {}

bot = telebot.TeleBot(TOKEN)

def get_chat_time(chat_id):
    if chat_id not in CHAT_START_TIME:
        CHAT_START_TIME[chat_id] = datetime.now()
    return CHAT_START_TIME[chat_id]

def is_five_minutes_passed(chat_id):
    start_time = get_chat_time(chat_id)
    return (datetime.now() - start_time).total_seconds() > 300

def save_user_message(chat_id, message):
    if chat_id not in USER_MESSAGES:
        USER_MESSAGES[chat_id] = []
    USER_MESSAGES[chat_id].append(message.lower())

def get_potential_issues(chat_id):
    if chat_id not in USER_MESSAGES:
        return []
    messages = USER_MESSAGES[chat_id]
    issues = []
    for msg in messages:
        if any(keyword in msg for keyword in ["встретимся", "приеду", "созвонимся", "где шоп", "докажи", "где взять"]):
            issues.append(msg)
    return issues

def get_response_variants(issue):
    variants = {}
    if "встретимся" in issue or "приеду" in issue:
        variants[issue] = [
            "Ой, было бы круто, но давай сначала стафф закажешь, а то я стесняюсь. Потом точно тусим!",
            "Хочу встретиться, но давай сначала докажи, что в теме — закажешь стафф, и я твоя!",
            "Слушай, я за, но давай ты сначала замутить стафф, а потом уже реально зажжём вместе!",
            "Не, пока не могу, давай ты закажешь стафф, и я сразу к тебе рвану!"
        ]
    elif "созвонимся" in issue:
        variants[issue] = [
            "Ой, созвоны не мой вайб, я стесняюсь. Давай в чате решим, закажешь стафф?",
            "Не, по голосу не люблю, лучше пиши. Закажи стафф, и тусим!",
            "Слушай, я не фанат звонков, давай тут всё обсудим. Стафф закажешь?",
            "Да ну, давай без звонков, в чате веселее. Купи стафф, и вперёд!"
        ]
    elif "где шоп" in issue or "где взять" in issue or "докажи" in issue:
        variants[issue] = [
            "Я сама брала экс где-то через телегу, пушка была. Могу скинуть ссылку, закажешь сам!",
            "Не парься, я знаю, где брали, но не вникаю. Скину ссылку, закажешь?",
            "Ой, не знаю точно, подруга давала ссылку. Хочешь, кину, сам глянь?",
            "Доказывать не буду, сама брала и улёт был. Хочу тусить, скину ссылку!"
        ]
    return variants

@bot.message_handler(commands=['idea'])
def handle_idea(message):
    chat_id = message.chat.id
    issues = get_potential_issues(chat_id)
    if not issues:
        bot.reply_to(message, "Пока никаких замесных вопросов, бро! Пиши, и я подскажу.")
        return
    response = "Вот где можно замяться:\n"
    for issue in issues:
        response += f"- {issue}\n"
        variants = get_response_variants(issue)
        for var in variants[issue]:
            response += f"  - {var}\n"
    bot.reply_to(message, response)

@bot.message_handler(content_types=['text'])
def handle_message(message):
    chat_id = message.chat.id
    user_text = message.text.lower()
    save_user_message(chat_id, user_text)

bot.polling(none_stop=True)
​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​​
