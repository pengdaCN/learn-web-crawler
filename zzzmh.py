import json
from collections.abc import Iterable

import execjs
import requests
import jmespath

from common import read_file

js_zzzmh = execjs.compile(read_file("./zzzmh-clear.sh.js"))


def decode(coding: str) -> str:
    return js_zzzmh.call("decode", coding)


def fetch_picture(p: int, size: int = 24) -> list[str] | None:
    resp = requests.post("https://api.zzzmh.cn/bz/v3/getData",
                         json={
                             "size": size,
                             "current": p,
                             "sort": 0,
                             "category": 0,
                             "resolution": 0,
                             "color": 0,
                             "categoryId": 0,
                             "ratio": 0
                         })
    data = resp.json()
    if jmespath.search('code', data) != 0:
        return

    raw_data: str = jmespath.search('result', data)
    decoding_data = decode(raw_data)

    return jmespath.search('list[].i', json.loads(decoding_data))


def write_lines(p: str, lines: Iterable[str]):
    with open(p, mode='a') as f:
        f.writelines(lines)


if __name__ == '__main__':
    for page in range(1, 20):
        write_lines('./pictures.txt', fetch_picture(page))

    print("写入成功")
