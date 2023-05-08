# -*- coding:utf-8 -*-
import os
import sys
import requests
import time
import copy
import logging
import random

from lxml.etree import HTML

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API_URL
LIKIE_URL = "https://tieba.baidu.com/f/like/mylike"
TBS_URL = "http://tieba.baidu.com/dc/common/tbs"
SIGN_URL = "https://tieba.baidu.com/sign/add"

ENV = os.environ


SIGN_DATA = {
    "ie": "utf-8",
    "kw": "",
    "tbs": ""
}

s = requests.Session()


def get_tbs():
    logger.info("获取tbs!")
    try:
        tbs = s.get(url=TBS_URL, timeout=5).json()["tbs"]
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    logger.info("获取tbs结束!")
    return tbs


def get_favorite():
    logger.info("获取关注的贴吧!")
    # 客户端关注的贴吧
    try:
        res = s.get(url=LIKIE_URL, timeout=5)
    except Exception as e:
        logger.error("获取关注的贴吧出错!")
        logger.error(e)
        sys.exit(1)
    html = HTML(res.text)
    names = html.cssselect("tr td:first-child a")

    ret = []
    for name in names:
        ret.append(name.get('title'))
    return ret


def client_sign(tbs, kw):
    # 客户端签到
    logger.info("开始签到贴吧：" + kw)
    data = copy.copy(SIGN_DATA)
    data.update({"kw": kw, "tbs": tbs})
    res_json = s.post(url=SIGN_URL, data=data).json()
    if res_json["no"] == 1101:
        logger.info(f"{kw}吧 已签到!")
    elif res_json["no"] != 0:
        logger.error(f"{kw}吧 签到出现错误!")


def main():
    # if 'COOKIE' not in ENV:
    #     logger.error("未配置COOKIE")
    #     return
    # cookies = ENV['COOKIE'].splitlines()
    cookies = ['RT="z=1&dm=baidu.com&si=8b89ca4f-c06a-40dd-851e-cf20240f77dc&ss=lhei3d46&sl=s&tt=1yhy&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=2cwtt&ul=2xm7l&hd=2xmj1"; tb_as_data=e716963261d370e48b9aa20657e03277131dbbbd245986b1ce52b6548df74b6d3800e3de4414c7c4d7fb6684a73fea29bd24c3383a12c603e0dd6599aa7fc1c70e83a58d18d0d04151f8ab312fe4e5dac5f82a33aa7a120382d4d64367ef53c47882a7ba3d1b0dec55d652f719b942d6; BAIDUID=A6E54307DDAF2AA317432E1ADB43E0AD:FG=1; XFI=3d556b20-ed78-11ed-9026-7db094b79bc7; XFCS=AF8760E2ADB8BF8D3AEEBDE029B317CC06A60A6B637C59D98BD4BC4820FEE65D; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1682640977,1682676822,1682867061,1683529665; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1683533620; BAIDU_WISE_UID=wapp_1683533551634_516; USER_JUMP=-1; XFT=ykXlLnbGDkUZ2Rt15RZOdeMjoAQZ4574w/+q6QeGUfw=; arialoadData=false; BDUSS=9pYnZmYjkwYm55bTBuTkE2c0NmN0dqYlFJekc2SVUzVVBBcGVjZzhBd3dQSUJrRVFBQUFBJCQAAAAAAQAAAAEAAABhV2sQa29uZ3llNTkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADCvWGQwr1hkSk; STOKEN=f27f458918fdbe9805081c654dfd960b4664b4016619c3ac2016b120b9f708f3']
    headers = {
        'Host': 'tieba.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
    }
    for i, cookie in enumerate(cookies):
        logger.info("开始签到第" + str(i+1) + "个用户!")
        headers.update({"Cookie": cookie})
        s.headers.update(headers)
        favorites = get_favorite()
        tbs = get_tbs()
        for name in favorites:
            time.sleep(random.randint(2, 3))
            client_sign(tbs, name)
        logger.info("完成第" + str(i+1) + "个用户签到!")
    logger.info("所有用户签到结束!")


if __name__ == '__main__':
    main()