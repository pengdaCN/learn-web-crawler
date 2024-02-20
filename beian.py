import base64
import json
import random

import requests
import execjs
from dataclasses import dataclass
import time
import hashlib
import jmespath
from common import image_to_png, write_file


@dataclass
class CheckImage:
    big_image: bytes
    sk: str
    small_image: bytes
    uuid: str
    word_count: int


class Beian:
    _js = execjs.compile('./beian.js')
    auth = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
    check_image = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImagePoint'

    def __init__(self, account='test', secret='test'):
        self.account = account
        self.secret = secret
        self._token = ""
        self._token_expired = 0
        self._point_id = ""

    @property
    def point_id(self) -> str:
        if self._point_id == "":
            self._point_id = self.point()

        return self._point_id

    @staticmethod
    def point() -> str:
        a = "0123456789abcdef"
        g = [random.choice(a) for _ in range(36)]

        g[14] = "4"
        g[19] = a[3 & ord(g[19]) | 8]
        g[8] = g[13] = g[18] = g[23] = "-"

        return "point-" + ''.join(g)

    def get_check_image(self):
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "DNT": "1",
            "Origin": "https://beian.miit.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://beian.miit.gov.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "token": self.auth_token
        }
        data = {
            "clientUid": self.point_id
        }
        data = json.dumps(data, separators=(',', ':'))
        r = requests.post(self.check_image, headers=headers, data=data)
        obj = r.json()
        big_image = base64.b64decode(jmespath.search('params.bigImage', obj))
        small_image = base64.b64decode(jmespath.search('params.smallImage', obj))
        sk = jmespath.search('params.secretKey', obj)
        uuid = jmespath.search('params.uuid', obj)
        wc = jmespath.search('params.wordCount', obj)

        return CheckImage(
            big_image=image_to_png(big_image),
            small_image=image_to_png(small_image),
            sk=sk,
            uuid=uuid,
            word_count=wc
        )

    @property
    def auth_key(self) -> (str, int):
        now = int(round(time.time() * 1000))

        md5 = hashlib.md5()
        md5.update(f'{self.account}{self.secret}{now}'.encode(encoding='utf8'))

        return md5.hexdigest(), now

    @property
    def auth_token(self) -> str:
        if self._token_expired < time.time():
            token, expired = self._get_auth_token()
            self._token = token
            self._token_expired = expired

        return self._token

    def _get_auth_token(self) -> (str, int):
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "DNT": "1",
            "Origin": "https://beian.miit.gov.cn",
            "Pragma": "no-cache",
            "Referer": "https://beian.miit.gov.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Microsoft Edge\";v=\"121\", \"Chromium\";v=\"121\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\""
        }
        key, at = self.auth_key
        data = {
            "authKey": key,
            "timeStamp": at
        }
        r = requests.post(self.auth, headers=headers, data=data)

        obj = r.json()
        token = jmespath.search('params.bussiness', obj)
        token_expired = int(round(time.time())) + jmespath.search('params.expire', obj)

        return token, token_expired


if __name__ == '__main__':
    beian = Beian()

    for i in range(3, 10):
        check_img = beian.get_check_image()
        write_file(f'./ci_1_{i}.png', check_img.big_image)
        write_file(f'./ci_2_{i}.png', check_img.small_image)
