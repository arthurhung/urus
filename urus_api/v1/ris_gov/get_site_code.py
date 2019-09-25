from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
chrome_options = Options()
# chrome_options.add_argument('--headless')
path = "C://Users//011189//Desktop//Arthur//vesta7//chromedriver.exe"
driver = webdriver.Chrome(path, chrome_options=chrome_options)
url = "https://www.ris.gov.tw/apply-registration/app/aw0720/main"
driver.get(url)

driver.find_element_by_xpath('//*[@id="rdKBin"]').click()

time.sleep(2)
# driver.find_element_by_xpath('//*[@id="city_siteId"]/option[2]').click()



city_code = driver.find_elements_by_xpath('//*[@id="city_siteId"]/option')

print("[")
for code in city_code:
    # print(code.text, "****")
    if not code.get_attribute("value"):
        continue
    code.click()
    time.sleep(1)
    site_id = driver.find_elements_by_xpath('//*[@id="site_siteId"]/option')
    for site in site_id:
        # print(f'* "{site.get_attribute("value")}": {site.text}')
        print(f'"{site.get_attribute("value")}",')



# print(len(city_code))

# for i in range(1, len(city_code)+1):
#     driver.find_element_by_xpath(f'//*[@id="city_siteId"]/option[{i}]').click()
#     site_id = driver.find_elements_by_xpath('//*[@id="site_siteId"]/option')
#     for site in site_id:
#         print(f'* "{site.get_attribute("value")}": {site.text}')

print("]")

driver.quit()






