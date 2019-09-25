import requests
import time
from lxml import etree
from lxml import html

base_url = "http://domestic.judicial.gov.tw/abbs/wkw/WHD9HN02.jsp"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
# A223191329
# %B7%A8%A9y%BE%EC
post_data = {}
# post_data["kd_id"] = ""
# post_data["kd"] = ""
# post_data["idnoyn"] = ""
# post_data["crtid"] = ""
# post_data["Button"] = ""
# post_data["kdid"] = ""
post_data["clnm"] = str("楊宜樺".encode("big5"))[2:-1].replace("\\x", "%")
post_data["form"] = "WHD9HN01.jsp"
# post_data["idno"] = "A223191328"
# post_data["sddtStart"] = ""
# post_data["sddtEnd"] = ""
print(post_data)
print(post_data["clnm"])
s =  '&'.join([f"{k}={v}" for k, v in post_data.items()])
req_url = base_url +"?"+ s
# print(req_url)
source = requests.get(req_url).content.decode("big5")

# source = requests.post(base_url, data=post_data, headers=headers).content.decode("big5")
# print(source)
tree = html.fromstring(source)
# print(tree.xpath("/html/body/form/div/text()"))
tr = tree.xpath("/html/body/form/table[2]/tr[4]/td[2]/font/table/tr")
default_tr = 4
result_len = len(tree.xpath("//form/table[2]/tr[4]/td[2]/font/table/tr")) - default_tr
print(result_len)
if "查詢條件異常" in source:
    print("查詢條件異常")
if "查無資料" not in source:
    result = {}
    for i in range(1, result_len+1):
        tr_num = default_tr + i
        tds = []
        for j in range(1, 6+1):
            td = tree.xpath(f"//table/tr[{tr_num}]/td[{j}]/div/text()")
            td = td if td else ""
            tds = tds + td
        key = ["court", "summary", "dispatch_date", "announce_date", "announcement"]
        # each_info = {
        #     "court": tds[1],
        #     "summary": tds[2],
        #     "dispatch_date": tds[3],
        #     "announce_date": tds[4],
        #     "announcement": tds[5]
        # }
        each_info = {k: tds[i+1] for i, k in enumerate(key)}
        result[tds[0]] = each_info
        print(tds)
    print(result)

  