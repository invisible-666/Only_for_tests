import cv2
import numpy as np
import os
from math import sqrt, ceil, floor
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

def get_winners_img(self, user_id):
    conn = sqlite3.connect(self.database)
    with conn:
        cur = conn.cursor()
        cur.execute(''' 
SELECT image FROM winners 
INNER JOIN prizes ON 
winners.prize_id = prizes.prize_id
WHERE user_id = ?''', (user_id, ))
        return cur.fetchall()

def create_collage(image_paths):
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        images.append(image)

    num_images = len(images)
    num_cols = floor(sqrt(num_images)) # Поиск количество картинок по горизонтали
    num_rows = ceil(num_images/num_cols)  # Поиск количество картинок по вертикали
    # Создание пустого коллажа
    collage = np.zeros((num_rows * images[0].shape[0], num_cols * images[0].shape[1], 3), dtype=np.uint8)
    # Размещение изображений на коллаже
    for i, image in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        collage[row*image.shape[0]:(row+1)*image.shape[0], col*image.shape[1]:(col+1)*image.shape[1], :] = image
    return collage


m = DatabaseManager(DATABASE)
info = m.get_winners_img("user_id")
prizes = [x[0] for x in info]
image_paths = os.listdir('img')
image_paths = [f'img/{x}' if x in prizes else f'hidden_img/{x}' for x in image_paths]
collage = create_collage(image_paths)

cv2.imshow('Collage', collage)
cv2.waitKey(0)
cv2.destroyAllWindows()

if __name__ == "__main__":
    bot.polling(none_stop=True)