import os
import random
import time

import django
import requests as req
import arrow
from loguru import logger
import sys
from queue import SimpleQueue
import threading
from datetime import datetime


sys.path.append(os.path.dirname(os.getcwd()))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup()

from apps.main.models import Data, KeyWord


requests = None

keyword_queue = SimpleQueue()


def human_str_to_int(s: str):
    if isinstance(s, int):
        return s
    if s.isdigit():
        return int(s)
    if not s:
        return 0
    if s.endswith("千"):
        return int(round(float(s[:-1]), 2) * 1000)
    elif s.endswith("万"):
        return int(round(float(s[:-1]), 2) * 10000)
    logger.error(f"{s} can not trans to int")


def gen_data_item(batch, word, origin_data, index, tp):
    item = Data(
        batch_number=batch,
        word=word,
        tp=tp,
        user_id=origin_data['user']['id'],
        nickname=origin_data['user']['screen_name'],
        is_v=origin_data['user']['verified'],
        fans=human_str_to_int(origin_data['user']['followers_count']),
        forward_count=human_str_to_int(origin_data['reposts_count']),
        comment_count=human_str_to_int(origin_data['comments_count']),
        good_count=human_str_to_int(origin_data['attitudes_count']),
        order=index[0],
        publish_time=arrow.get(origin_data['created_at'], "ddd MMM DD hh:mm:ss Z YYYY").format("YYYY-MM-DD hh:mm:ss"),
        wei_bo_id=origin_data['id'],
        content=""
    )
    index[0] += 1
    return item


@logger.catch()
def get_jx(batch, word, proxy=None):
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type=1%26q={word}&page_type=searchall"
    try:
        response = requests.get(url, proxies=proxy)
        logger.debug(response.content[:100])
        data = response.json()['data']
    except (Exception,) as e:
        logger.error(str(e))
        return []
    try:
        card_group = data['cards'][1]['card_group']
    except (Exception,):
        return []
    result = []
    index = [1]
    if card_group[0].get('desc') == "精选":
        for group in card_group:
            if group['card_type'] == 89:
                result.append(gen_data_item(batch, word, group['mblog'], index, Data.Type.Curation))
            if group['card_type'] == 59:
                if group.get('left_element', {}).get('mblog'):
                    result.append(gen_data_item(batch, word, group['left_element']['mblog'], index, Data.Type.Curation))
                if group.get('right_element', {}).get('mblog'):
                    result.append(gen_data_item(batch, word, group['right_element']['mblog'], index, Data.Type.Curation))
    return result


@logger.catch()
def parse_cards(batch, word, index, cards, tp):
    result = []
    for card in cards:
        card_type = card['card_type']
        if card_type == 9:
            result.append(gen_data_item(batch, word, card['mblog'], index, tp))
        if card_type == 11:
            groups = card['card_group']
            for _card in groups:
                if _card['card_type'] != 9:
                    continue
                result.append(gen_data_item(batch, word, _card['mblog'], index, tp))
    return result


def parse_list(url, page, batch, word, index, tp, proxy=None):
    result = []
    if page > 0:
        url += f"&page={page + 1}"
    try:
        response = requests.get(url, proxies=proxy)
        logger.debug(response.content[:100])
        data = response.json()['data']
    except (Exception,) as e:
        logger.error(f"url: {url}, error: {e}")
        return []
    cards = data['cards']
    result.extend(parse_cards(batch, word, index, cards, tp))
    return result


def get_real_time(batch, word, proxy=None):
    result = []
    index = [1]
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type=61%26q={word}&t=&page_type=searchall"
    for page in range(6):
        page_result = parse_list(url, page, batch, word, index, Data.Type.Realtime, proxy)
        result.extend(page_result)
        if page < 6:
            time.sleep(random.randint(1, 3))
        if len(page_result) < 7:
            break

    return result[:50]


def get_hot(batch, word, proxy):
    result = []
    index = [1]
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type=60%26q={word}%26t=&title=热门-{word}&cardid=weibo_page&extparam=title=热门%26mid=%26q={word}&luicode=10000011&lfid=100103type=1%26q={word}%26t="
    for page in range(3):
        page_result = parse_list(url, page, batch, word, index, Data.Type.Hot, proxy)
        result.extend(page_result)
        if page < 6:
            time.sleep(random.randint(1, 3))
        if len(page_result) < 7:
            break
    return result[:20]


def handle_word(batch, proxy=None):
    global requests, keyword_queue

    while True:
        requests = req.Session()

        word = keyword_queue.get()

        results = []

        jx_result = get_jx(batch, word, proxy)
        results.extend(jx_result)
        time.sleep(random.randint(2, 4))

        hot_result = get_hot(batch, word, proxy)
        results.extend(hot_result)
        time.sleep(random.randint(2, 4))

        real_result = get_real_time(batch, word, proxy)
        results.extend(real_result)
        Data.objects.bulk_create(results)
        time.sleep(random.randint(2, 5))
        logger.info(f"[{word}]: jx: {len(jx_result)}, hot: {len(hot_result)}, realtime: {len(real_result)}, "
                    f"thread:{threading.currentThread().ident}")


def get_proxies(order_id):
    try:
        url = f"http://kps.kdlapi.com/api/getkps/?orderid={order_id}&num=1&signature=vfcnwmdy15a268ms3yt15giszx8l2q4s&pt=1&format=json&sep=1"
        res = req.get(url).json()
        logger.info(f"get proxies response:{res}")
        return res['data']['proxy_list']
    except (Exception,):
        return []


def main():
    while True:
        for i in KeyWord.objects.all():
            keyword_queue.put(i.word)

        logger.info(f"total {keyword_queue.qsize()} keyword")
        batch_no = str(datetime.now())[:19].replace("-", "").replace(":", "").replace(" ", "")
        logger.info(f"begin {batch_no}")

        thread_num = 4
        threads = []
        for i in range(thread_num):
            proxy = {
                "http": "47.100.38.213:16817",
                "https": "47.100.38.213:16817",
            }
            t = threading.Thread(target=handle_word, args=(batch_no, proxy))
            threads.append(t)
        # 创建5个线程
        for i in range(thread_num):
            threads[i].start()
        for i in range(thread_num):
            threads[i].join()

        time.sleep(random.randint(200, 500))


if __name__ == "__main__":
    main()
