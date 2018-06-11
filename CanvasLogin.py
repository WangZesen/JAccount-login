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
        self.login_status = self._recover()

    def _recover(self):
        #
        # TODO: Recover session after some time of disconnection
        #

        cookies_dir = config.cache_dir + 'CanvasLogin/cookies.txt'
        if os.path.exists(cookies_dir):
            with open(cookies_dir, 'r') as f:
                self.cookies = eval(f.read())
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

    def login_jaccount(self):
        login_url_0 = 'https://www.umjicanvas.com/login/openid_connect'
        login_res_0 = self.session.get(login_url_0, allow_redirects = False, cookies = self.cookies, headers = self.headers)
        login_cookies_0 = requests.utils.dict_from_cookiejar(login_res_0.cookies)
        self.cookies.update(login_cookies_0)

        login_url_1 = login_res_0.headers['Location']
        login_res_1 = self.session.get(login_url_1, allow_redirects = False, cookies = self.cookies, headers = self.headers)
        login_cookies_1 = requests.utils.dict_from_cookiejar(login_res_1.cookies)
        self.cookies.update(login_cookies_1)

        login_url_2 = login_res_1.headers['Location']
        login_res_2 = self.session.get(login_url_2, allow_redirects = False, cookies = self.cookies, headers = self.headers)
        login_cookies_2 = requests.utils.dict_from_cookiejar(login_res_2.cookies)
        self.cookies.update(login_cookies_2)

        selector = etree.HTML(login_res_2.text)
        captcha_xpath = '//*[@id="form-input"]/div[3]/img'
        captcha_src = selector.xpath('//*[@id="form-input"]/div[3]/img')[0].attrib['src']
        captcha_src = 'https://jaccount.sjtu.edu.cn/jaccount/' + captcha_src
        captcha_res = self.session.get(captcha_src, headers = self.headers)

        captcha_file = open('test.jpg', 'wb')
        captcha_file.write(captcha_res.content)
        captcha_file.close()

        captcha_value = None
        captcha_value = input('Captcha: ')

        login_url_3 = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'

        url_raw = urlparse(login_url_2).query.split('&')
        url_parse = {}
        for item in url_raw:
            url_parse[item.split('=')[0]] = item.split('=')[1]
            print (item.split('=')[0])
        print (url_parse)

        login_data = {
        	'sid': url_parse['sid'],
            'returl': url_parse['returl'],
            'se': url_parse['se'],
            'v': '',
            'client': url_parse['client'],
            'user': 'UncleSam',
            'pass': 'wzshello123',
            'captcha': captcha_value
        }

        while True:
            login_res_3 = self.session.post(login_url_3, allow_redirects = False, data = login_data, cookies = self.cookies, headers = self.headers)
            login_cookies_3 = requests.utils.dict_from_cookiejar(login_res_3.cookies)

            '''
            with open('test.html', 'wb') as f:
                f.write(login_res_3.content)
            '''

            #
            # TODO: Deal with login failure due to wrong captcha
            #

            if login_res_3.headers['Location'].endswith('err=1'):
                login_res_2 = login_res_3
                #
                # TODO: Get new captcha
                #
                print ('Wrong Captcha!')
                login_data['captcha'] = input('Captcha: ')
            else:
                break

        self.cookies.update(login_cookies_3)
        cookies_dir = config.cache_dir + 'CanvasLogin/cookies.txt'
        with open(cookies_dir, 'w') as f:
            f.write(str(self.cookies))

        print ('res cookie:', login_res_3)


if __name__ == '__main__':
    login_test = CanvasLogin()
    login_test.login_jaccount()
