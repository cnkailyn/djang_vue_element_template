from django.http import HttpResponse, JsonResponse


class ApiResponse(object):
    @staticmethod
    def success(data={}):
        return JsonResponse({
            "code": 0,
            "msg": "",
            "data": data
        })

    @staticmethod
    def fail(msg="", code=-1):
        return JsonResponse({
            "code": code,
            "msg": msg,
            "data": {}
        })
