from flask_restful import Resource, Api
from flasgger import swag_from
from flask import request
from flask import jsonify
from flask import Response
from flask_restful import abort
from lxml import etree
from lxml import html
import requests
import json
import time
import re

from urus_api.utility.utility_logger import logger
from urus_api.utility.validation_error_handlers import validation_error_400
from urus_api.utility.captcha.model import img2txt
from urus_api.utility.decorator import validate_contentType
from urus_api.utility.response_formmater import ResponseFormatter


class HelloWorld(Resource):

    def get(self):
        # binary_img = requests.get(
        #     'https://www.ris.gov.tw/apply-idCard/captcha/image?CAPTCHA_KEY=5d5a673fcc29480baf60240dd8cbebeb&time=1546828067149'
        # ).content
        # ans = img2txt([binary_img])
        ans = "hihihi"
        logger.info(ans)
        return {'hello': ans}


# {
#     "user_id": "S224845090",
#     "tw_year": "95",
#     "month": "4",
#     "day": "7",
#     "city_code": "63000",
#     "type": "3"
# }

# {
#     "user_id": "F127963584",
#     "tw_year": "99",
#     "month": "9",
#     "day": "20",
#     "city_code": "10001",
#     "type": "3"
# }


class IDcardValidator(Resource):
    """
    身分證查驗
    """
    action = "idcard_validator"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from('./specs/idcard_validator.yml', validation=True, validation_error_handler=validation_error_400)
    def post(self, action=action):
        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        base_url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
        captcha_url = "https://www.ris.gov.tw/apply-idCard/captcha/image?"
        idcard_validate_url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/query"
        idcard_query_changed_url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/idc/query"

        post_data = request.json
        captcha_key = self.get_captcha_key(base_url)
        logger.info('user_id[{}] captcha_key[{}]'.format(post_data.get('user_id'), captcha_key))

        for i in range(5):
            current_time = int(time.time())
            captcha_image_url = self.get_captcha_image_url(current_time, captcha_key, captcha_url)
            captcha_code = self.detect_captcha_image(captcha_image_url)
            request_data = {
                "idnum": post_data.get('user_id'),
                "applyTWY": post_data.get('tw_year'),
                "applyMM": post_data.get('month'),
                "applyDD": post_data.get('day'),
                "siteId": post_data.get('city_code'),
                "applyReason": post_data.get('type')
            }

            result = self.validate_idcard(idcard_validate_url, request_data, captcha_key,
                                          captcha_code).content.decode("utf-8")
            target_result = ""
            if "國民身分證領補換資料查詢結果" in result:
                tree = html.fromstring(result)
                result_msg_xpaths = [
                    # success_xpath
                    '//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div[2]/div/text()',
                    # '//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div[2]/h4/text()',
                    # fail_xpath
                    '//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div[2]/ol/li/text()',
                    # '//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div[1]/h4/strong/text()',
                    # lock_xpath
                    '//*[@id="resultBlock"]/div[2]/div[2]/div[1]/div[2]/div/div/div/text()'
                ]
                for x in result_msg_xpaths:
                    target_result = tree.xpath(x)
                    if target_result:
                        break

                if target_result:
                    result_msg = {"msg": target_result}
                    if "國民身分證資料與檔存資料相符。" in target_result:
                        birthday = post_data.get('birthday')
                        if birthday:
                            idc_rep = self.query_idcard_changed(result, birthday, idcard_query_changed_url)
                            result_msg['idc'] = json.loads(idc_rep)
                        response = ResponseFormatter(action, result_msg).success()
                    else:
                        response = ResponseFormatter(action, result_msg).error()

                break

        if not target_result:
            target_result = "查詢失敗，稍後再試。"
            result_msg = {"msg": target_result}
            response = ResponseFormatter(action, target_result).error()
        logger.info(f'嘗試次數[{i+1}]')
        logger.info(f"target_result[{target_result}]")
        return response

    def get_captcha_key(self, url):
        source = requests.get(url).content
        tree = html.fromstring(source)
        captcha_key = ''.join(tree.xpath('//*[@id="captchaKey_captcha-refresh"]/@value'))
        return captcha_key

    def get_captcha_image_url(self, current_time, captcha_key, captcha_url):
        params = f"CAPTCHA_KEY={captcha_key}&time={current_time}"
        captcha_image_url = captcha_url + params
        return captcha_image_url

    def detect_captcha_image(self, captcha_image_url):
        binary_img = requests.get(captcha_image_url).content
        ans = img2txt(binary_img)
        return ans[0]

    def validate_idcard(self, idcard_validate_url, request_data, captcha_key, captcha_code):
        request_data['captchaKey'] = captcha_key
        request_data['captchaInput'] = captcha_code
        rep = requests.post(idcard_validate_url, data=request_data)
        return rep

    def query_idcard_changed(self, result, birthday, url):
        rx = re.compile(r'{t:"(.*?)"', re.S)
        token = re.findall(rx, result)
        token = token[0] if token else 'None'
        birthday = birthday.zfill(7)
        request_data = {'d': birthday, 't': token}
        rep = requests.post(url, data=request_data).content.decode("utf-8")
        return rep


class HouseholdCertRecord(Resource):
    """
    戶口名簿請領紀錄查詢
    """
    action = "household_cert_record"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from('./specs/household_cert_record.yml', validation=True, validation_error_handler=validation_error_400)
    def post(self, action=action):
        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        # 這支政府API captcha input是做假的 可以不用傳captchaInput&captchaKey
        idcard_validate_url = "https://www.ris.gov.tw/apply-registration/app/aw0720/doQuery"
        post_data = request.json

        request_data = {}
        request_data["applyYYYMMDD"] = post_data.get("apply_date")
        request_data["houseHoldId"] = post_data.get("houseHold_id")
        request_data["houseHoldHeadId"] = post_data.get("houseHoldHead_id")
        request_data["SeqNo"] = post_data.get("seq_no")
        request_data["siteId"] = post_data.get("site_code")
        request_data["varifyType"] = post_data.get("type")

        if request_data["varifyType"] == "apart":
            person_id = post_data.get("person_id") if post_data.get("person_id") else "None"
            request_data["personId"] = person_id
        # all
        else:
            request_data["personCount"] = post_data.get("person_count")

        logger.info(f"request_data[{request_data}]")
        result = requests.post(idcard_validate_url, data=request_data).content.decode("utf-8")
        target_result = ""
        if "戶口名簿請領記錄查詢結果" in result:
            tree = html.fromstring(result)
            result_msg_xpaths = ['//*[@id="print"]/div[2]/label[2]/text()']
            for x in result_msg_xpaths:
                target_result = tree.xpath(x)
                if target_result:
                    break

        if target_result:
            result_msg = {"msg": target_result}
            response = ResponseFormatter(action, result_msg).success()
        else:
            result_msg = {"msg": "查詢失敗，請再試一次。"}
            response = ResponseFormatter(action, result_msg).error()
        logger.info(f"result_msg[{result_msg}]")
        return response


class FamilyLitigation(Resource):
    """
    家事事件公告查詢
    """
    action = "family_litigation"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from('./specs/family_litigation.yml', validation=True, validation_error_handler=validation_error_400)
    def post(self, action=action):
        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        base_url = "http://domestic.judicial.gov.tw/abbs/wkw/WHD9HN02.jsp"
        post_data = request.json
        name = post_data.get("name", "")
        user_id = post_data.get("user_id", "")

        if user_id or name:
            request_data = {}
            request_data["form"] = "WHD9HN01.jsp"
            request_data["clnm"] = str(name.encode("big5"))[2:-1].replace("\\x", "%")
            request_data["idno"] = user_id
            url_params = '&'.join([f"{k}={v}" for k, v in request_data.items()])
            req_url = base_url + "?" + url_params
            logger.info(f"req_url[{req_url}]")
            source = requests.get(req_url).content.decode("big5")
            tree = html.fromstring(source)
            # 4 為該網站tr default長度
            default_tr = 4
            result_len = len(tree.xpath("//form/table[2]/tr[4]/td[2]/font/table/tr")) - default_tr
            logger.info(f"result_len[{result_len}]")
            if result_len > 0:
                result = []
                for i in range(1, result_len + 1):
                    tr_num = default_tr + i
                    tds = []
                    for j in range(1, 6 + 1):
                        td = tree.xpath(f"//table/tr[{tr_num}]/td[{j}]/div/text()")
                        td = td if td else ""
                        tds = tds + td
                    key = ["item", "court", "summary", "dispatch_date", "announce_date", "announcement"]
                    each_info = {k: tds[i] for i, k in enumerate(key)}
                    result.append(each_info)

                response = ResponseFormatter(action, result).success()
            else:
                if "查無資料" in source:
                    result_msg = {"msg": "查無資料"}
                    response = ResponseFormatter(action, result_msg).success()
                else:
                    result_msg = {"msg": "查詢條件異常"}
                    response = ResponseFormatter(action, result_msg).error()
            return response

        else:
            result_msg = {"msg": "查詢條件姓名及身分證號不能皆為全部。"}
            response = ResponseFormatter(action, result_msg).error()
            abort(400, **response)
