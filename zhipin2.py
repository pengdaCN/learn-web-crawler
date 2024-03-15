import json
import time
import urllib.parse

import requests
import urllib3.util


def job_list(token: str):
    headers = {
        "authority": "www.zhipin.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "referer": "https://www.zhipin.com/web/geek/job?query=Android&city=101190400",
        "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a": "1709101705,1710154656,1710154699,1710155135",
        "__g": "-",
        "wd_guid": "4a013a91-5279-403a-9ddb-ae39323b8311",
        "historyState": "state",
        "_bl_uid": "b5lz6teFpe1cO0lC7et5wadidI1U",
        "lastCity": "101270100",
        "__l": "l=%2Fwww.zhipin.com%2Fchengdu%2F&s=3&friend_source=0",
        "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a": "1710497725",
        "__c": "1710306942",
        "__a": "82979320.1710306942..1710306942.4.1.4.4",
        "__zp_stoken__": urllib.parse.quote(token)
    }
    url = "https://www.zhipin.com/wapi/zpgeek/search/joblist.json"
    params = {
        "scene": "1",
        "query": "Android",
        "city": "101190400",
        "experience": "",
        "payType": "",
        "partTime": "",
        "degree": "",
        "industry": "",
        "scale": "",
        "stage": "",
        "position": "",
        "jobType": "",
        "salary": "",
        "multiBusinessDistrict": "",
        "multiSubway": "",
        "page": "1",
        "pageSize": "30"
    }

    resp = requests.post(url, headers=headers, cookies=cookies, params=params)
    print(resp.text)


def gen_token(seed: str, t: int | None = None) -> str:
    if t is None:
        t = int(round(time.time() * 1000))

    url = "http://localhost:12080/go"
    data = {
        "group": "zhipin",
        "name": "token",
        "action": "token",
        "param": json.dumps({"seek": seed, "t": t})
    }

    resp = requests.post(url=url, data=data)
    return resp.json()['data']


if __name__ == '__main__':
    token = gen_token('FVMyb+vHAt5styKmqISiWGYpCiVRL4JZPLBI8hwnPFw=', 1710499829951)
    job_list(token)
