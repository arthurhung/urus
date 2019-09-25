from flask_restful import Resource, Api
from flask_restful import abort
from flasgger import swag_from
from flask import request
from flask import jsonify
from flask import Response
import datetime
import sqlalchemy

from urus_api import db
from urus_api.utility.utility_logger import logger
from urus_api.utility.db_utils.models import BcLineBroadcast, EcPfBotLineMember, EcPfMember, BcLineBroadcastItem, BcLineBroadcastCategory
from urus_api.utility.response_formmater import ResponseFormatter
from urus_api.utility.validation_error_handlers import validation_error_400
from urus_api.utility.decorator import validate_contentType


def check_sinopac_customer(line_id):
    is_customer = False
    mem_id_obj = EcPfBotLineMember.query.filter(EcPfBotLineMember.line_id == line_id).first()
    mem_id = mem_id_obj.mem_id if mem_id_obj else None
    if mem_id:
        uuidpk = EcPfMember.query.filter(EcPfMember.uuidpk == mem_id).first()
        if uuidpk:
            is_customer = True
    logger.info("line_id:[{}], mem_id:[{}], is_customer:[{}]".format(line_id, mem_id, is_customer))
    return is_customer


class Order(Resource):
    """
    提供碩網當User進入後，存入使用者推播設定
    """

    action = "broadcast_order"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from(
        './specs/broadcast_order.yml',
        validation=True,
        validation_error_handler=validation_error_400)
    def post(self, action=action):

        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        try:
            # 前面還要加一段判斷是否為證券客戶
            post_data = request.json
            line_id = post_data.get("line_id")

            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            source = "碩網"

            default_broadcasts_items = self.get_broadcast_items(line_id)
            logger.info("default_broadcasts_items:[{}]".format(default_broadcasts_items))
            for bc in default_broadcasts_items:
                user_info = BcLineBroadcast(
                    line_id=line_id,
                    broadcast=bc,
                    create_at=current_time,
                    update_at=current_time,
                    user_status="1",
                    source=source)
                db.session.add(user_info)
                try:
                    db.session.commit()
                except:
                    logger.warn("default_broadcasts_item duplicated, item number:[{}]".format(bc))

            result_msg = {"msg": "使用者推播設定已加入成功!"}
            response = ResponseFormatter(action, result_msg).success()
            return response

        except Exception as e:
            result_msg = {"msg": 'broadcast_order server error'}
            rep = ResponseFormatter(action, result_msg).error(error_type='ServerError')
            logger.error('action:[{}], error_msg:[{}]'.format(action, str(e)))
            abort(500, **rep)

    def get_broadcast_items(self, line_id):

        is_customer = check_sinopac_customer(line_id)
        items_info = BcLineBroadcastItem.query.all()
        default_broadcasts_items = []
        for i in items_info:
            flag = i.item_customer_default
            if is_customer:
                if flag == "1":
                    default_broadcasts_items.append(i.item_number)
            else:
                if flag == "0":
                    default_broadcasts_items.append(i.item_number)
        return default_broadcasts_items


class Cancel(Resource):
    """
    提供碩網Line封鎖後，關閉該使用者所有推播設定。
    """

    action = "broadcast_cancel"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from(
        './specs/broadcast_cancel.yml',
        validation=True,
        validation_error_handler=validation_error_400)
    def post(self, action=action):

        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        try:
            post_data = request.json
            line_id = post_data.get("line_id")
            source = post_data.get("source")
            user_infos = BcLineBroadcast.query.filter(BcLineBroadcast.line_id == line_id).all()
            logger.info("action:[{}], line_id:[{}], broadcast_len:[{}]".format(
                action, line_id, len(user_infos)))
            current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            for info in user_infos:
                if info.status != "0":
                    info.status = "0"
                    info.update_at = current_time
                info.source = source
            db.session.commit()
            result_msg = {"msg": "使用者已取消全部推播設定"}
            response = ResponseFormatter(action, result_msg).success()
            return response

        except Exception as e:
            result_msg = {"msg": 'broadcast_cancel server error'}
            rep = ResponseFormatter(action, result_msg).error(error_type='ServerError')
            logger.error('action:[{}], error_msg:[{}]'.format(action, str(e)))
            abort(500, **rep)


class Update(Resource):
    """
    更新客戶推播設定狀態
    """
    action = "user_status_update"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from(
        './specs/user_status_update.yml',
        validation=True,
        validation_error_handler=validation_error_400)
    def post(self, action=action):

        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        try:
            post_data = request.json
            line_id = post_data.get("line_id").strip()
            broadcast = post_data.get("broadcast")
            user_status = post_data.get("user_status")

            user_infos = BcLineBroadcast.query.filter(BcLineBroadcast.line_id == line_id).all()
            logger.info("user_infos:[{}]".format(user_infos))
            if not user_infos:
                error_code = "ERR001"
                result_msg = {"msg": "無Line ID"}
                raise ValueError

            user_info = BcLineBroadcast.query.filter(
                BcLineBroadcast.line_id == line_id, BcLineBroadcast.broadcast == broadcast).first()
            logger.info("user_info:[{}]".format(user_info))
            if user_info:
                user_info.user_status = user_status
            else:
                is_customer = check_sinopac_customer(line_id)
                # 客人一開始無證券戶但有@Line，後來去辦證券戶的狀況處理
                if is_customer:
                    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    source = "永豐金"
                    user_info = BcLineBroadcast(
                        line_id=line_id,
                        broadcast=broadcast,
                        create_at=current_time,
                        update_at=current_time,
                        user_status="1",
                        source=source)
                    db.session.add(user_info)
                else:
                    error_code = "ERR002"
                    result_msg = {"msg": "無證券戶"}
                    raise ValueError

            db.session.commit()
            to_fe_data = {}
            to_fe_data["line_id"] = line_id
            to_fe_data["broadcast"] = broadcast
            to_fe_data["item_name"] = user_info.bc_line_broadcast_item.item_name
            to_fe_data["user_status"] = user_status

            response = ResponseFormatter(action, to_fe_data).success()
            return response

        except ValueError as e:
            rep = ResponseFormatter(action, result_msg).error(
                error_type='RequestError', error_code=error_code)
            abort(400, **rep)

        except Exception as e:
            result_msg = {"msg": 'user_status_update server error'}
            rep = ResponseFormatter(action, result_msg).error(error_type='ServerError')
            logger.error('action:[{}], error_msg:[{}]'.format(action, str(e)))
            abort(500, **rep)


class UserStatus(Resource):
    """
    查詢客戶推播設定狀態
    """
    action = "user_status_query"

    @validate_contentType(action=action, request=request, content_types=['application/json'])
    @swag_from(
        './specs/user_status_query.yml',
        validation=True,
        validation_error_handler=validation_error_400)
    def post(self, action=action):

        return self.main_process(request=request, action=action)

    def main_process(self, request, action):
        try:
            post_data = request.json
            line_id = post_data.get("line_id")

            user_infos = BcLineBroadcast.query.filter(BcLineBroadcast.line_id == line_id).all()
            logger.info("action:[{}], line_id:[{}], broadcast_len:[{}]".format(
                action, line_id, len(user_infos)))
            # user broadcast status
            user_broadcast_map = {}
            for info in user_infos:
                user_broadcast_map[info.broadcast] = info.user_status
            # get each category items list
            b_map = {}
            items_obj = BcLineBroadcastItem.query.all()
            for i in items_obj:
                category_number = i.bc_line_broadcast_category.category_number
                category_name = i.bc_line_broadcast_category.category_name
                key = str(category_number) + "_" + str(category_name)
                if key not in b_map:
                    b_map[key] = []
                d = i.to_dict(
                    filter_type="exclude", filter_columns=["item_status", "item_category"])
                d["user_status"] = user_broadcast_map.get(d["item_number"])
                b_map[key].append(d)

            result = []
            for k, v in b_map.items():
                category_number, category_name = k.split("_")
                d = {}
                d["category_number"] = int(category_number)
                d["category_name"] = category_name
                d["items"] = v
                result.append(d)

            response = ResponseFormatter(action, result).success()
            return response

        except Exception as e:
            result_msg = {"msg": 'user_status_query server error'}
            rep = ResponseFormatter(action, result_msg).error(error_type='ServerError')
            logger.error('action:[{}], error_msg:[{}]'.format(action, str(e)))
            abort(500, **rep)

    def get_user_status(self, user_infos):
        for info in user_infos:
            d = {}
            d["broadcast"] = info.broadcast
            d["user_status"] = info.user_status
            d["item_name"] = info.bc_line_broadcast_item.item_name
            yield d