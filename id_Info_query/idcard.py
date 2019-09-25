from google.cloud import vision
from google.cloud.vision import types
from lxml import etree
from lxml import html
from model import img2txt
import requests
import time
import base64
import io
import os

url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
captchaBaseUrl = "https://www.ris.gov.tw/apply-idCard/captcha/image?"
queryAPI = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/query"


# CAPTCHA_KEY=c365ba2162f84498885bcff0873a91df&time=1542852591685
def getCaptchaKey():
    source = requests.get(url).content
    tree = html.fromstring(source)
    captchaKey = ''.join(
        tree.xpath('//*[@id="captchaKey_captcha-refresh"]/@value'))

    return captchaKey


def getCaptchaImages(captchaKey):
    currentTime = int(time.time())
    params = f"CAPTCHA_KEY={captchaKey}&time={currentTime}"
    getImageUrl = captchaBaseUrl + params

    return getImageUrl


# def useGoogleVisionAPIbyUrl(imageUrl):
#     os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project 83431-e48eeaa37a88.json'
#     client = vision.ImageAnnotatorClient()

#     image = vision.types.Image()
#     image.source.image_uri = imageUrl

#     response = client.text_detection(image=image)
#     texts = response.text_annotations

#     textList = []

#     for text in texts:
#         textList.append(text.description)

#     try:
#         code = textList[0].strip()
#         code = ''.join(code.split()).upper()

#     except:
#         code = 'None'
#     print(code)
#     return code


def detectImage(imageUrl):
    binary_img = requests.get(imageUrl).content
    ans = img2txt([binary_img])

    return ans[0]


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
    start_time = time.time()
    captchaKey = getCaptchaKey()
    roundTripTime = time.time() - start_time
    print(f'roundTripTime:{roundTripTime}')

    while True:
        imageUrl = getCaptchaImages(captchaKey)
        # captchaCode = useGoogleVisionAPIbyUrl(imageUrl)
        captchaCode = detectImage(imageUrl)

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
            tree = html.fromstring(result)

            successPath = '//*[@id="resultBlock"]/div/div[3]/div[1]/div[2]/div[2]/h4/strong/text()'
            failPath = '//*[@id="resultBlock"]/div/div[3]/div[1]/div[2]/div[1]/h4/strong/text()'
            lockPath = '//*[@id="resultBlock"]/div/div[3]/div[1]/div[2]/div/div/div'

            successResult = tree.xpath(successPath)
            failResult = tree.xpath(failPath)
            lockResult = tree.xpath(lockPath)

            if successResult:
                print(successResult)

            else:
                if failResult:
                    print(failResult)
                else:
                    print(lockResult)
            break
