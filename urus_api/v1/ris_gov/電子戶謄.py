import requests
import time
from lxml import etree
from lxml import html
from urus_api.v1.utility.captcha.model import img2txt

base_url = "https://www.ris.gov.tw/apply-householdRegistrationApply/app/aw0705/verifyCensus/main"
captcha_url = "https://www.ris.gov.tw/apply-householdRegistrationApply/captcha/image?"

source = requests.get(base_url).content
tree = html.fromstring(source)
captcha_key = ''.join(tree.xpath('//*[@id="captchaKey_captcha"]/@value'))

current_time = int(time.time())
params = f"CAPTCHA_KEY={captcha_key}&time={current_time}"
captcha_image_url = captcha_url + params

binary_img = requests.get(captcha_image_url).content

with open('./image.jpg', 'wb') as handler:
    handler.write(binary_img)
ans = img2txt([binary_img])[0]

post_data = {}
post_data["ccode"] = "TXF"
post_data["captchaInput"] = ans
post_data["captchaKey"] = captcha_key
# print(post_data)

v_url = "https://www.ris.gov.tw/apply-householdRegistrationApply/app/aw0705/verifyCensus/apply"
# headers = {
#         'Content-Type': 'multipart/form-data',
#     }

from requests_toolbelt.multipart.encoder import MultipartEncoder
multipart_data = MultipartEncoder(
    fields={
        # plain text fields
        # 'uploadFile': None,
        'ccode': 'TXF',
        'captchaInput': ans,
        'captchaKey': captcha_key
    })

# headers={
#     # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#     # 'Accept-Encoding':'gzip, deflate',
#     # 'Accept-Language':'zh-CN,zh;q=0.9',
#     'Content-Type':'multipart/form-data; boundary=----WebKitFormBoundary62t40g6x4lqfwwOS',
# }
# print(multipart_data)
rep = requests.post(
    v_url, data=multipart_data, headers={'Content-Type': multipart_data.content_type})
# rep = requests.post(v_url, data=multipart_data, headers=headers)

# rep = requests.post(v_url, files=dict(foo='bar'))

print(rep.request.headers)
print(rep.content.decode("utf-8"))