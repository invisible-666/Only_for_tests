from telebot import TeleBot
from confing import TOKEN

bot = TeleBot(TOKEN)

@bot.message_handler(commands=['rating'])
def handle_rating(message):
    rating_data = [
        ('user1', 5),
        ('user2x', 3),
    ]
    rating_data.sort(key=lambda x: x[1], reverse=True)
    res = [f'| @{x[0]:<11} | {x[1]:<11}|\n{"_"*26}' for x in rating_data]
    res = '\n'.join(res)
    res = f'|USER_NAME    |COUNT_PRIZE|\n{"_"*26}\n' + res
    bot.send_message(message.chat.id, res)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    prize_id = call.data
    user_id = call.message.chat.id

    winners = []

    if sum(winners) < 3:
        winners.append(user_id)
        img = 'This PC/downloads/m0r0k_t34m_news.jpg'
        with open(img, 'rb') as photo:
            bot.send_photo(user_id, photo)

    else:
        bot.send_message(user_id, "Сумма всех победителей достигла 3, вы не можете быть добавлены.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
