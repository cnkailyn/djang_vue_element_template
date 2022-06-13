import requests
import zipfile
import os
from loguru import logger


def notice_ding_ding(msg):
    msg = f"通知：{msg}"
    body = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }
    try:
        requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token="
            "8a7d4363ac334fed3c92e8d08756ded51916c89ee63c59175e101fd8c4c4464d",
            json=body)
    except (Exception,) as e:
        logger.exception(e)


def get_city(ip):
    if ip in ("127.0.0.1", "localhost"):
        return "本地"
    try:
        url = f"http://ip-api.com/json/{ip}?lang=zh-CN"
        res = requests.get(url).json()
        return f"{res['country']}->{res['regionName']}->{res['city']}"
    except (Exception,):
        logger.warning("get ip address fail")
        return "未知"


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def zip_files(file_path_list, target_file):
    f = zipfile.ZipFile(target_file, 'w', zipfile.ZIP_DEFLATED)
    for item in file_path_list:
        f.write(item, item.split(os.path.sep)[-1])
    f.close()
