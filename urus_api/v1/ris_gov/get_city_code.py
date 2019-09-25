from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')
path = "C://Users//011189//Desktop//Arthur//vesta7//chromedriver.exe"
driver = webdriver.Chrome(path, chrome_options=chrome_options)
url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
driver.get(url)
siteId = driver.find_elements_by_xpath('//*[@id="siteId"]/option')

print("[")
for i in siteId:
    print(f'* "{i.get_attribute("value")}": {i.text}')

print("]")

driver.quit()