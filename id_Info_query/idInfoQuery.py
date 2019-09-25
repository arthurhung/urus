from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64
import io
import os
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types


url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"

nID = 'S224845090'



getImageBase64Script = """$.getScript("https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.js", function() {
  var c = document.getElementById('captchaImage_captcha-refresh')
  domtoimage.toPng(c).then(function(dataUrl){
    
    var img = new Image();
    img.src = dataUrl;
    console.log(dataUrl)

    // ajax 


        document.body.appendChild(img);
  });
});"""




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

def useGoogleVisionAPIbyUrl():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './My Project 83431-e48eeaa37a88.json'
    client = vision.ImageAnnotatorClient()

    image = vision.types.Image()
    image.source.image_uri = "https://www.ris.gov.tw/apply-idCard/captcha/image?CAPTCHA_KEY=c365ba2162f84498885bcff0873a91df&time=1542852591685"

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
    print(code)
    return code



if __name__ == '__main__':
    start_time = time.time()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # path = "/home/apuser/Arthur/seleniumTest/chromedriver"
    path = "C://Users//011189//Desktop//Arthur//vesta7//chromedriver.exe"

    for i in range(1, 10):
        print(f"執行第{i}次")
        driver = webdriver.Chrome(path, chrome_options=chrome_options)

        driver.get(url)
        roundTripTime = time.time() - start_time
        print(f'roundTripTime:{roundTripTime}')

        while True:
            # start_time = time.time()
            # 統一編號
            driver.find_element_by_xpath('//*[@id="idnum"]').send_keys(nID)

            # 發照年月日
            driver.find_element_by_xpath('//*[@id="applyTWY"]/option[14]').click()
            driver.find_element_by_xpath('//*[@id="applyMM"]/option[5]').click()
            driver.find_element_by_xpath('//*[@id="applyDD"]/option[8]').click()

            # 發證地點
            driver.find_element_by_xpath('//*[@id="siteId"]/option[23]').click()

            # 補換類別
            driver.find_element_by_xpath('//*[@id="applyReason"]/option[4]').click()
         
            driver.execute_script(getImageBase64Script)

            # 取得image base64 
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/img"))
            )

            imageBase64 = element.get_attribute('src')
            # imageBase64 = driver.find_element_by_xpath('/html/body/img').get_attribute('src')

            imageBase64 = imageBase64.replace('data:image/png;base64,','')
            imageBase64Byte = str.encode(imageBase64)

            with open("image.jpg", "wb") as f:
                f.write(base64.decodebytes(imageBase64Byte))

            code = useGoogleVisionAPI()
            
            # 輸入驗證碼
            driver.find_element_by_xpath('//*[@id="captchaInput_captcha-refresh"]').clear()
            driver.find_element_by_xpath('//*[@id="captchaInput_captcha-refresh"]').send_keys(code) 
            
            driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/form/div[4]/button[1]').click()

            # 國民身分證資料與檔存資料相符。
            try:
                result = driver.find_element_by_xpath('//*[@id="resultBlock"]/div/div[3]/div[1]/div[2]/div[2]/h4/strong').text
                print('Success: ', result)
                print(code)
                os.rename("./image.jpg", f"./img/{code}.jpg")
                driver.quit()

                break

            except:
                print('Fail')

