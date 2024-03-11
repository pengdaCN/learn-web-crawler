import asyncio
import logging
import threading
import time

from mitmproxy import http
from mitmproxy.script import concurrent
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
from playwright.sync_api import sync_playwright


class ZhipinAddons:
    @concurrent
    def response(self, flow: http.HTTPFlow):
        if not flow.request.url.startswith(
                r'https://static.zhipin.com/fe-zhipin-geek/web/chat/v5126/static/js/app.896c12fe.js'):
            return

        js_content = flow.response.text
        hook_js = r'r=(new e).z(t,parseInt(n)+60*(480+(new Date).getTimezoneOffset())*1e3)'
        idx = js_content.find(hook_js)
        if idx < 0:
            logging.warning('注入js代码失败')
            return

        insert_idx = idx + len(hook_js)
        new_js_content_chars = list(js_content)
        new_js_content_chars.insert(insert_idx, r',(() => {console.log("hook ok in token calculate")})()')
        new_js_content = "".join(new_js_content_chars)
        flow.response.text = new_js_content


def dump_server_run(addons):
    opts = Options(
        listen_host='127.0.0.1',
        listen_port=8080,
    )
    loop = asyncio.new_event_loop()
    m = DumpMaster(opts, loop=loop, with_dumper=False)
    m.addons.add(addons)
    loop.run_until_complete(m.run())


if __name__ == '__main__':
    dump = threading.Thread(target=dump_server_run, args=(ZhipinAddons(),))
    dump.daemon = True
    dump.start()

    time.sleep(5)
    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=r'C:\Users\admin\AppData\Local\Temp\1',
            headless=False,
            channel='msedge',
            proxy={
                "server": "127.0.0.1:8080",
            },
            args=['--ignore-certificate-errors']
        )

        page = browser.new_page()
        page.goto('https://www.zhipin.com/web/geek/job?query=%E5%AE%89%E5%8D%93&city=101270100')
        page.wait_for_timeout(1000 * 1000)
