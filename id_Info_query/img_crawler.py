from google.cloud import vision
from google.cloud.vision import types
from lxml import etree 
from lxml import html
import requests
import time
import os
import io


def getCaptchaKey(url):
    source = requests.get(url).content
    tree = html.fromstring(source)
    captchaKey = ''.join(tree.xpath('//*[@id="captchaKey_captcha-refresh"]/@value'))

    return captchaKey


def getCaptchaImages(captchaKey):
    currentTime = int(time.time()) 
    params = f"CAPTCHA_KEY={captchaKey}&time={currentTime}"
    getImageUrl = captchaBaseUrl + params

    return getImageUrl


def useGoogleVisionAPIbyUrl(url):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project 83431-e48eeaa37a88.json'
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image()
    image.source.image_uri = url

    response = client.text_detection(image=image)
    texts = response.text_annotations

    textList = []

    for text in texts:
        textList.append(text.description)

    try:
        code = textList[0].strip()
        code = ''.join(code.split()).upper()

    except:
        code = 'None'
    # print(code)
    return code


def useGoogleVisionAPI():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project 83431-e48eeaa37a88.json'
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__), 'image.jpg')

    # [START migration_text_detection]
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    textList = []

    for text in texts:
        textList.append(text.description)

    try:
        code = textList[0].strip()
        code = ''.join(code.split()).upper()

    except:
        code = 'None'

    return code


def queryIDcardRep(requestData, captchaKey, captchaCode):
    postData = {}
    postData['idnum'] = requestData.get('idnum')
    postData['applyTWY'] = requestData.get('applyTWY')
    postData['applyMM'] = requestData.get('applyMM')
    postData['applyDD'] = requestData.get('applyDD')
    postData['siteId'] = requestData.get('siteId')
    postData['applyReason'] = requestData.get('applyReason')
    postData['captchaInput'] = captchaCode
    postData['captchaKey'] = captchaKey

    response = requests.post(queryAPI, data=postData).content.decode("utf-8") 

    return response


if __name__ == '__main__':
    url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
    captchaBaseUrl = "https://www.ris.gov.tw/apply-idCard/captcha/image?"
    queryAPI = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/query"

    counter = 0

    for i in range(1, 1000):
        print(f"執行{i}次")
        captchaKey = getCaptchaKey(url)

        while True:
            counter += 1
            imageUrl = getCaptchaImages(captchaKey)

            imgData = requests.get(imageUrl).content

            with open('./image.jpg', 'wb') as handler:
                handler.write(imgData)

            captchaCode = useGoogleVisionAPI()

            requestData = {
                "idnum": "S224845090",
                "applyTWY": "95",
                "applyMM": "4",
                "applyDD": "7",
                "siteId": "63000",
                "applyReason": "3"
            }

            result = queryIDcardRep(requestData, captchaKey, captchaCode)

            if "國民身分證領補換資料查詢結果" in result:
                print("success")
                print(captchaCode)
                os.rename("./image.jpg", f"./img/{captchaCode}.jpg")
                time.sleep(0.5)
                break