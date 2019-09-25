from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from lxml import html
from model import img2txt
import requests
import time
import base64
import io
import os


url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"

nID = 'F127963584'



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


# CAPTCHA_KEY=c365ba2162f84498885bcff0873a91df&time=1542852591685
def get_captcha_key(source):
    tree = html.fromstring(source)
    captcha_key = ''.join(tree.xpath('//*[@id="captchaKey_captcha-refresh"]/@value'))

    return captcha_key


def getCaptchaImages(captcha_key):
    current_time = int(time.time())
    params = f"CAPTCHA_KEY={captcha_key}&time={current_time}"
    image_url = captcha_base_url + params

    return image_url


def detectImage(image_url):
    binary_img = requests.get(image_url).content
    ans = img2txt([binary_img])

    return ans[0]


if __name__ == '__main__':
    start_time = time.time()
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')

    # path = "/home/apuser/Arthur/seleniumTest/chromedriver"
    path = "C://Users//011189//Desktop//Arthur//vesta7//chromedriver.exe"
    
    url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
    captcha_base_url = "https://www.ris.gov.tw/apply-idCard/captcha/image?"

    for i in range(1, 10):
        print(f"執行第{i}次")
        driver = webdriver.Chrome(path, chrome_options=chrome_options)
        driver.get(url)
        captcha_key = get_captcha_key(driver.page_source)
        print(captcha_key)


        while True:
            # start_time = time.time()
            # 統一編號
            driver.find_element_by_xpath('//*[@id="idnum"]').send_keys(nID)

            # 發照年月日
            driver.find_element_by_xpath('//*[@id="applyTWY"]/option[11]').click()
            driver.find_element_by_xpath('//*[@id="applyMM"]/option[10]').click()
            driver.find_element_by_xpath('//*[@id="applyDD"]/option[21]').click()

            # 發證地點
            driver.find_element_by_xpath('//*[@id="siteId"]/option[2]').click()

            # 補換類別
            driver.find_element_by_xpath('//*[@id="applyReason"]/option[4]').click()

            # 辨識驗證碼
            image_url = getCaptchaImages(captcha_key)
            code = detectImage(image_url)
            print(code)
            # 輸入驗證碼
            driver.find_element_by_xpath('//*[@id="captchaInput_captcha-refresh"]').clear()
            driver.find_element_by_xpath('//*[@id="captchaInput_captcha-refresh"]').send_keys(code) 
            
            driver.find_element_by_xpath('/html/body/div/div[4]/div[1]/div/form/div[4]/button[1]').click()

            # 國民身分證資料與檔存資料相符。
            try:
                time.sleep(1.5)
                result = driver.find_element_by_xpath('//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div[2]/div').text
                print('Success: ', result)
                print(code)
                driver.quit()

                break

            except:
                print('Fail')
                

        roundTripTime = time.time() - start_time
        print(f'roundTripTime:{roundTripTime}')