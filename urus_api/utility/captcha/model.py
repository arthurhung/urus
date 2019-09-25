import os
import io
import numpy as np
import tensorflow as tf
from PIL import Image
from keras.models import load_model
from urus_api.config import Config

code2txt = {
    0: '2',
    1: '3',
    2: '4',
    3: '5',
    4: '6',
    5: '7',
    6: '8',
    7: '9',
    8: 'A',
    9: 'B',
    10: 'C',
    11: 'D',
    12: 'E',
    13: 'F',
    14: 'G',
    15: 'H',
    16: 'J',
    17: 'K',
    18: 'N',
    19: 'P',
    20: 'Q',
    21: 'R',
    22: 'S',
    23: 'T',
    24: 'U',
    25: 'V',
    26: 'X',
    27: 'Y',
    28: 'Z'
}
img_pos = [[5, 25], [20, 40], [32, 52], [45, 65], [60, 80]]

current_path = os.getcwd()
api_version = Config.API_VERSION
model_name = "captcha_model.h5"
model_path = f"{current_path}/urus_api/utility/captcha/{model_name}"

graph = None
model = None


def img2txt(binary_img_list):
    global graph
    global model
    graph = tf.get_default_graph() if not graph else graph
    model = load_model(model_path) if not model else model

    with graph.as_default():
        binary_img_list = [binary_img_list] if type(binary_img_list) != list else binary_img_list

        img_sep = []
        for binary_img in binary_img_list:
            img = Image.open(io.BytesIO(binary_img))
            img_arr = np.asarray(img)
            img_sep += [img_arr[:, pos[0]:pos[1], :] / 255 for pos in img_pos]

        img_prop = model.predict(np.array(img_sep))
        img_ans = [code2txt[code] for code in img_prop.argmax(axis=1)]

        return [('').join(img_ans[i * 5:(i + 1) * 5]) for i, _ in enumerate(binary_img_list)]
