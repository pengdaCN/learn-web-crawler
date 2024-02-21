import time

from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Route, Page, Request


def allow_continue(route: Route, _: Request):
    print('continue:', route.request.url)
    route.continue_()


def intercept_request(route: Route, _: Request):
    if not route.request.url.startswith(
            r'https://static.zhipin.com/fe-zhipin-geek/web/chat/v5126/static/js/app.896c12fe.js'):
        route.continue_()
        return

        # 拦截js
    resp = route.fetch()
    js_content = resp.text()
    hook_js = r'r=(new e).z(t,parseInt(n)+60*(480+(new Date).getTimezoneOffset())*1e3)'
    idx = js_content.find(hook_js)
    if idx < 0:
        print("hook 注入失败")
        route.continue_()
        return

    insert_idx = idx + len(hook_js)
    new_js_content_chars = list(js_content)
    new_js_content_chars.insert(insert_idx, r',(() => {console.log("hook ok in token calculate")})()')
    new_js_content = "".join(new_js_content_chars)
    route.fulfill(body=new_js_content)


def again_route(page: Page):
    print('nav changed')
    page.unroute_all(behavior='wait')
    time.sleep(1)
    page.route("**/*", intercept_request)
    print('again route ok')


if __name__ == '__main__':
    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            # executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            # args=[
            #     '--disable-features=ImprovedCookieControls,LazyFrameLoading,'
            #     'GlobalMediaControls,DestroyProfileOnBrowserClose,MediaRouter,AcceptCHFrame'],
            # ignore_default_args=True,
            devtools=True,
            headless=False,
        )
        # browser = pw.firefox.launch(headless=True)
        context = browser.new_context()
        # context.route("**/*", intercept_request)
        page = context.new_page()
        page.route("**/*", allow_continue)
        # page.on('domcontentloaded', lambda: again_route(page))
        # page.goto('https://www.zhipin.com/web/geek/job?query=%E5%AE%89%E5%8D%93&city=101270100')
        page.goto('https://www.baidu.com')
        time.sleep(5)
        page.goto('https://www.jd.com')

        time.sleep(1000)
