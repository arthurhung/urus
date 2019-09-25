class ResponseFormatter(object):
    '''
    統一 response output格式。
    
    '''

    def __init__(self, action, data):
        self.action = action
        self.data = data if data else {"msg": "查無資料"}

    def success(self, result=None):
        result = result if result else self.data
        rep = {"success": True, "action": self.action, "result": result}
        return rep

    def error(self, error_type=None, error_code=None, error_msg=None):
        result = error_msg if error_msg else self.data
        error_type = error_type if error_type else str(self.action) + '_error'
        error_code = error_code if error_code else "None"
        rep = {
            "success": False,
            "error_type": error_type,
            "error_code": error_code,
            "result": result
        }
        return rep