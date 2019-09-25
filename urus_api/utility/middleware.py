from werkzeug.wrappers import Request
import json
import copy


class ClientRequestDataRecordMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # req = Request(environ, shallow=True)
        # temp = copy.copy(req)
        # print(id(req.data))

        # print(environ["REMOTE_ADDR"])
        # a = req
        # req.temp_data = req.data

        # print(json.loads(temp.data))
        response = self.app(environ, start_response)
        # print(start_response)
        # print(dir(response))
        return response
