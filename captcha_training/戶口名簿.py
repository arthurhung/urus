import requests
import time
from lxml import etree
from lxml import html
from model import img2txt

base_url = "https://www.ris.gov.tw/apply-registration/app/aw0720/main"
captcha_url = "https://www.ris.gov.tw/apply-registration/captcha/image?"

source = requests.get(base_url).content
tree = html.fromstring(source)
captcha_key = ''.join(tree.xpath('//*[@id="captchaKey_captcha-refresh"]/@value'))

current_time = int(time.time())
params = f"CAPTCHA_KEY={captcha_key}&time={current_time}"
captcha_image_url = captcha_url + params

binary_img = requests.get(captcha_image_url).content

with open('./image.jpg', 'wb') as handler:
    handler.write(binary_img)
ans = img2txt([binary_img])[0]

post_data = {}
post_data["result"] = True
post_data["dataIntputType"] = "KB"
post_data["scanIn"] = ""
post_data["applyYYYMMDD"] = "1060613"
post_data["houseHoldId"] = "C3605071"
post_data["houseHoldHeadId"] = "R123083931"
post_data["SeqNo"] = "00002"
post_data["siteId"] = "10017060"
post_data["varifyType"] = "apart"
post_data["personId"] = "R123083932"
# post_data["personId"] = "R123083931"
post_data["personCount"] = ""
post_data["captchaInput"] = "ABCDE"
post_data["captchaKey"] = captcha_key

v_url = "https://www.ris.gov.tw/apply-registration/app/aw0720/doQuery"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

result = requests.post(v_url, data=post_data, headers=headers).content.decode("utf-8")
print(result)

tree = html.fromstring(result)
# print(tree.xpath("/html/body/div/div[4]/div/div/div/h3/text()"))
