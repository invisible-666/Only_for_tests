import sqlite3
import cv2
import numpy as np
import os
from math import sqrt, ceil, floor

def create_collage(image_paths):
    images = []
    for path in image_paths:
        image = cv2.imread(path)
        images.append(image)

    num_images = len(images)
    num_cols = floor(sqrt(num_images))
    num_rows = ceil(num_images/num_cols)
    collage = np.zeros((num_rows * images[0].shape[0], num_cols * images[0].shape[1], 3), dtype=np.uint8)
    for i, image in enumerate(images):
        row = i // num_cols
        col = i % num_cols
        collage[row*image.shape[0]:(row+1)*image.shape[0], col*image.shape[1]:(col+1)*image.shape[1], :] = image
    return collage

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
    m = DatabaseManager(DATABASE)
    info = m.get_winners_img("user_id")
    prizes = [x[0] for x in info]
    image_paths = os.listdir('img')
    image_paths = [f'img/{x}' if x in prizes else f'hidden_img/{x}' for x in image_paths]
    collage = create_collage(image_paths)

    cv2.imshow('Collage', collage)
    cv2.waitKey(0)
    cv2.destroyAllWindows()