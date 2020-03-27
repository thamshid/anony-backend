from rest_framework import status
from rest_framework.response import Response


class HttpSuccessResponse(Response):
    def __init__(self, data, message=None, count=None, extra_data=None, status_code=None, **kwargs):
        data = {"status": 'ok',
                "message": message if message else "",
                "data": data
                }
        if count is not None:
            data["count"] = count
        if extra_data:
            data['extra'] = extra_data
        if status_code:
            data['status_code'] = status_code
        super(HttpSuccessResponse, self).__init__(data, **kwargs)


class HttpErrorResponse(Response):
    def __init__(self, message, status_code=None, error_code=None, **kwargs):
        data = {"status": 'err',
                "message": message}
        if error_code:
            data['error_code'] = error_code
        self.status_code = status_code if status_code else status.HTTP_200_OK
        super(HttpErrorResponse, self).__init__(data, **kwargs)