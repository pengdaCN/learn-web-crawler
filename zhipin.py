import requests
import execjs
import common


class Zhipin:
    js_zzzmh = execjs.compile(common.read_file("./zhipin-clear.js"))

    def __init__(self, t=""):
        self.__next_token = ""
        self.__token = t

    @classmethod
    def token(cls, seed: str, tz: int) -> str:
        return cls.js_zzzmh.call("token", seed, tz)

    def search_jobs(self, kw: str):
        requests.get(r'https://www.zhipin.com/wapi/zpgeek/search/joblist.json', params={
            "scene": 1,
            "query": kw,
            "city": 101270100,
            "page": 1,
            "pageSize": 30,
        }, cookies={

        })


if __name__ == '__main__':
    print(Zhipin.token("PohA+exl9uE+kVUN7aDWj9SgV3kxxiIs76ldBjmsvCo=", 1708234761914))
