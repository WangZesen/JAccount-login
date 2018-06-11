from urllib.parse import urlparse
from lxml import etree
import fateadm_api
import requests
import config
import os

class CanvasLogin():
    def __init__(self):
        self.session = requests.Session()
        self.cookies = {
            'UM_distinctid': '163cacffe326e-00aa6760e6b56a-737356c-144000-163cacffe359a6'
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Referer': 'https://www.umjicanvas.com/login/canvas'
        }
        self.session.headers.update(self.headers)
        self.login_status = self._recover()

    def _recover(self):
        #
        # TODO: Recover session after some time of disconnection
        #

        cookies_dir = config.cache_dir + 'CanvasLogin/cookies.txt'
        if os.path.exists(cookies_dir):
            with open(cookies_dir, 'r') as f:
                # self.cookies = eval(f.read())
                pass
            if 'JAAuthCookie' in self.cookies:
                #
                # TODO: Verify the cookies is not expired
                #
                return True
            else:
                return False

        pass

    def logout(self):
        #
        # TODO: Use 'https://www.umjicanvas.com/logout' to logout
        #
        self.__init__()

    def _get_courses_test(self):
        url = 'https://www.umjicanvas.com/'
        res = self.session.get(url, cookies = self.cookies, headers = self.headers)
        print (res.text)
        pass

    def get_captcha(self, login_res):
        selector = etree.HTML(login_res.text)
        captcha_xpath = '//*[@id="form-input"]/div[3]/img'
        captcha_src = selector.xpath('//*[@id="form-input"]/div[3]/img')[0].attrib['src']
        captcha_src = 'https://jaccount.sjtu.edu.cn/jaccount/' + captcha_src
        captcha_res = self.session.get(captcha_src, headers = self.headers)
        with open('test.jpg', 'wb') as f:
            f.write(captcha_res.content)
        captcha_value = input('Captcha: ')
        return captcha_value

    def login_jaccount_(self):
        login_url = 'https://www.umjicanvas.com/login/openid_connect'
        res = self.session.get(login_url)
        res_url = res.url


        url_raw = urlparse(res_url).query.split('&')
        url_parse = {}
        for item in url_raw:
            url_parse[item.split('=')[0]] = item.split('=')[1]

        login_data = {
        	'sid': url_parse['sid'],
            'returl': url_parse['returl'],
            'se': url_parse['se'],
            'v': '',
            'client': url_parse['client'],
            'user': 'UncleSam',
            'pass': 'wzshello123',
            'captcha': self.get_captcha(res)
        }
        # print (login_data)
        submit_url = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
        login_res = self.session.post(submit_url, allow_redirects = False, data = login_data)
        final_res = self.session.get('https://jaccount.sjtu.edu.cn' + login_res.headers['Location'])

        # print (self.session.cookies.get_dict())
        # print (final_res.text)
        print (login_res.url)
        print (login_res.status_code)

        #
        # TODO: Solve 400 Error for Final Response
        #

        print (final_res.status_code)


    def login_jaccount(self):
        login_url_0 = 'https://www.umjicanvas.com/login/openid_connect'
        login_res_0 = self.session.get(login_url_0, allow_redirects = False, headers = self.headers)
        # login_cookies_0 = requests.utils.dict_from_cookiejar(login_res_0.cookies)
        # self.cookies.update(login_cookies_0)
        print (self.session.cookies.get_dict())

        login_url_1 = login_res_0.headers['Location']
        login_res_1 = self.session.get(login_url_1, allow_redirects = False, headers = self.headers)
        # login_cookies_1 = requests.utils.dict_from_cookiejar(login_res_1.cookies)
        # self.cookies.update(login_cookies_1)

        login_url_2 = login_res_1.headers['Location']
        login_res_2 = self.session.get(login_url_2, allow_redirects = False, headers = self.headers)
        # login_cookies_2 = requests.utils.dict_from_cookiejar(login_res_2.cookies)
        # self.cookies.update(login_cookies_2)

        login_url_3 = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
        url_raw = urlparse(login_url_2).query.split('&')
        url_parse = {}
        for item in url_raw:
            url_parse[item.split('=')[0]] = item.split('=')[1]

        login_data = {
        	'sid': url_parse['sid'],
            'returl': url_parse['returl'],
            'se': url_parse['se'],
            'v': '',
            'client': url_parse['client'],
            'user': 'UncleSam',
            'pass': 'wzshello123',
            'captcha': self.get_captcha(login_res_2)
        }

        while True:
            login_res_3 = self.session.post(login_url_3, allow_redirects = False, data = login_data, cookies = self.cookies, headers = self.headers)
            login_cookies_3 = requests.utils.dict_from_cookiejar(login_res_3.cookies)
            with open('test.html', 'wb') as f:
                f.write(login_res_3.content)
            if login_res_3.headers['Location'].endswith('err=1'):
                login_url_2 = 'https://jaccount.sjtu.edu.cn/' + login_res_3.headers['Location']
                login_res_2 = self.session.get(login_url_2, allow_redirects = False, cookies = self.cookies, headers = self.headers)
                login_cookies_2 = requests.utils.dict_from_cookiejar(login_res_2.cookies)
                self.cookies.update(login_cookies_2)
                login_data['captcha'] = self.get_captcha(login_res_2)
            else:
                break

        self.cookies.update(login_cookies_3)
        cookies_dir = config.cache_dir + 'CanvasLogin/cookies.txt'
        with open(cookies_dir, 'w') as f:
            f.write(str(self.cookies))

        while login_res_3.status_code == '302':
            # login_url_3 =
            login_res_3 = self.session.get()
        print (login_res_3.status_code)

        print ('res cookie:', login_cookies_3)


if __name__ == '__main__':
    login_test = CanvasLogin()
    login_test.login_jaccount_()
    # login_test._get_courses_test()
