from PIL import Image
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adam
import numpy as np
import glob
import requests
import io
from functools import partial

def code2onehot(code, num):
    arr = np.zeros((num,))
    arr[code] = 1

    return arr

code2txt = {0: '2',
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
 28: 'Z'}

txt2code = {'2': 0,
 '3': 1,
 '4': 2,
 '5': 3,
 '6': 4,
 '7': 5,
 '8': 6,
 '9': 7,
 'A': 8,
 'B': 9,
 'C': 10,
 'D': 11,
 'E': 12,
 'F': 13,
 'G': 14,
 'H': 15,
 'J': 16,
 'K': 17,
 'N': 18,
 'P': 19,
 'Q': 20,
 'R': 21,
 'S': 22,
 'T': 23,
 'U': 24,
 'V': 25,
 'X': 26,
 'Y': 27,
 'Z': 28}

def img2txt(binary_img, model, code2txt, img_pos):
    img = Image.open(io.BytesIO(binary_img))
    img_arr = np.asarray(img)
    img_sep = [img_arr[:,pos[0]:pos[1],:]/255 for pos in img_pos]
    img_prop = model.predict(np.array(img_sep))
    img_ans = [code2txt[code] for code in img_prop.argmax(axis=1)]   
    return img_ans


model = load_model('temp_model.h5')
img2txt = partial(img2txt, model=model, code2txt=code2txt, img_pos=img_pos)

if __name__ == '__main__':
    img_channels = 3
    img_rows = 20
    img_cols = 28
    img_pos = [[5,25], [20,40], [32,52], [45,65], [60,80]]

    model = load_model('temp_model.h5')
    # model.compile(loss='categorical_crossentropy',
    #               optimizer=Adam(),
    #               metrics=['accuracy'])


    res = requests.get('https://www.ris.gov.tw/apply-idCard/captcha/image?CAPTCHA_KEY=8dccfab505f14957876d92a1ded0ea5f&time=1545722979000')
    
    img = Image.open(io.BytesIO(res.content))
    img_arr = np.asarray(img)
    img_sep = [img_arr[:,pos[0]:pos[1],:]/255 for pos in img_pos]

    img_prop = model.predict(np.array(img_sep))
    img_ans = [code2txt[code] for code in img_prop.argmax(axis=1)]   

    print(('').join(img_ans))