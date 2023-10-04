# -*- coding: utf-8 -*-
# @Author : 艾登Aiden
# @Email : aidencaptcha@gmail.com

import time

from loguru import logger

time_str = time.strftime("%Y-%m-%d_%H_%M_%S",time.localtime()) 
# logger.add(time_str + ".txt", level="DEBUG", enqueue=True, rotation="10 MB")
# logger.debug("msg msg msg!")

import json
import random
import time

from faker import Faker

from spiders.check import check
from spiders.login import login
from spiders.spider import Request, Response
from spiders.txcaptcha import txcaptcha
from spiders.x_login import x_login


def save_img(name, data):
    with open(name, "wb") as f:
        f.write(data)


def read_file(name):
    with open(name, "r") as f:
        text = f.read()
    return text


def save_file(name, data):
    with open(name, "w") as f:
        f.write(data)



def fake_useragent(nokey="Linux"):
    fak = Faker()
    while 1:
        ua = fak.user_agent()
        # print(ua)
        if nokey not in ua:
            break
    logger.debug(f"ua==>{ua}")
    return ua


logger.debug(r"""
    _     _      _                ____                _          _
   / \   (_)  __| |  ___  _ __   / ___|  __ _  _ __  | |_   ___ | |__    __ _ 
  / _ \  | | / _` | / _ \| '_ \ | |     / _` || '_ \ | __| / __|| '_ \  / _` |
 / ___ \ | || (_| ||  __/| | | || |___ | (_| || |_) || |_ | (__ | | | || (_| |
/_/   \_\|_| \__,_| \___||_| |_| \____| \__,_|| .__/  \__| \___||_| |_| \__,_|
                                              |_|
@Author : 艾登科技
@Email : aidencaptcha@gmail.com
@Address : https://github.com/aidencaptcha
@Description : API需求请在邮箱联系 aidencaptcha@gmail.com
""")

settings = {    
    "START_URL": "", # cap_union_prehandle url 在 txcaptcha 填入
    "PROXIES": {}, # 不使用代理
    # "PROXIES": {"all":"https://ip:port"}, # http 代理 无密码
    # "PROXIES": {"all":"https://user:pass@ip:port"}, # http 代理 有密码
    # "PROXIES": {"all":"socks5://user:pass@ip:port"}, # socks 代理 有密码
    "COOKIES": {},
    "DOWNLOAD_DELAY": 0,
    "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",      
    "DOWNLOAD_TIMEOUT": 30,
    "VERIFY": None,    
    "LOG": True
}
# print(settings)

proxies = {}
cookies = {}
downloads_delay = settings.get("DOWNLOAD_DELAY")
timeout = settings.get("DOWNLOAD_TIMEOUT")
allow_redirects = settings.get("ALLOW_REDIRECTS")
verify = settings.get("VERIFY")


response = Response()
response.meta = {}
response.meta["settings"] = settings


# qq空间登录 549000912
# qq邮箱登录 522005705
response.meta["aid"] = '549000912'
response.meta["qq"] = f'169{random.randint(100000, 999999)}'
response.meta["settings"]["COOKIES"] = cookies

logger.debug(f'aid==>{response.meta["aid"]}')
logger.debug(f'qq==>{response.meta["qq"]}')

response = x_login(
    response,
    timeout=timeout,
    proxies=proxies,
    verify=verify,
)
time.sleep(downloads_delay)


response = check(
    response,
    timeout=timeout,
    proxies=proxies,
    verify=verify,
)
time.sleep(downloads_delay)


response = txcaptcha(
    response,
    timeout=timeout,
    proxies=proxies,
    verify=verify,
)
logger.debug(f"txcaptcha response==>{response.text}")


assert str(response.json().get("errorCode")) == "0"


time.sleep(downloads_delay)

response = login(
    response,
    timeout=timeout,
    proxies=proxies,
    verify=verify,
)
logger.debug(f"login response==>{response.text}")