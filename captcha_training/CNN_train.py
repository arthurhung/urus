from PIL import Image
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adam
import tensorflow as tf
import numpy as np
import glob


def code2onehot(code, num):
    arr = np.zeros((num,))
    arr[code] = 1

    return arr


if __name__ == '__main__':
    img_paths = glob.glob('img/*.jpg')

    # 一張五碼驗證碼切的position
    img_pos = [[5, 25], [20, 40], [32, 52], [45, 65], [60, 80]]

    # X(切割後每個captcha array), Y(正確答案one hot encoding)
    X, y = [], []
    for i, path in enumerate(img_paths):
        img = Image.open(path)
        imgArr = np.asarray(img)
        # print(imgArr.shape) # (28(高), 80(寬), 3)
        ans = path[4:9]  # img\237G3.jpg

        for idx, txt_pos in enumerate(img_pos):
            imgArrSingleTxt = imgArr[:, txt_pos[0]:txt_pos[1], :]
            X.append(imgArrSingleTxt)
            y.append(ans[idx])

    txt2code = {}
    code2txt = {}
    label = sorted(list(set(y)))
    [(txt2code.update({t: i}), code2txt.update({i: t})) for i, t in enumerate(label)]
    num_txt = len(label)

    Y = list(map(lambda x: code2onehot(txt2code[x], num_txt), y))

    split = int(len(X) * 0.75)
    X_train = np.array(X[:split])
    Y_train = np.array(Y[:split])
    X_test = np.array(X[split:])
    Y_test = np.array(Y[split:])

    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    # 建模
    img_channels = 3
    img_rows = 20
    img_cols = 28
    batch_size = 32
    nb_classes = num_txt
    nb_epoch = 200  # 訓練次數

    model = Sequential()

    model.add(Convolution2D(32, (3, 3), border_mode='same', input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(Convolution2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(64, (3, 3), border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, (3, 3)))
    model.add(Activation('relu'))
    #model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.summary()

    model.compile(loss='categorical_crossentropy', optimizer=Adam(), metrics=['accuracy'])

    model.fit(
        X_train,
        Y_train,
        batch_size=batch_size,
        nb_epoch=nb_epoch,
        validation_data=(X_test, Y_test),
        shuffle=True)

    # Test
    score = model.evaluate(X_test, Y_test, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])

    # Save model
    model.save('captcha_model.h5')