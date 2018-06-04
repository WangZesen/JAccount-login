import requests
from lxml import etree

cookies = {}
headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
	'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8'
}

login_url_0 = 'https://www.umjicanvas.com/login/openid_connect'
login_res_0 = requests.get(login_url_0, allow_redirects = False, cookies = cookies, headers = headers)
login_cookies_0 = requests.utils.dict_from_cookiejar(login_res_0.cookies)
cookies.update(login_cookies_0)

login_url_1 = login_res_0.headers['Location']
login_res_1 = requests.get(login_url_1, allow_redirects = False, cookies = cookies, headers = headers)
login_cookies_1 = requests.utils.dict_from_cookiejar(login_res_1.cookies)
cookies.update(login_cookies_1)

login_url_2 = login_res_1.headers['Location']
login_res_2 = requests.get(login_url_2, allow_redirects = False, cookies = cookies, headers = headers)
login_cookies_2 = requests.utils.dict_from_cookiejar(login_res_2.cookies)
cookies.update(login_cookies_2)

selector = etree.HTML(login_res_2.text)
capcha_xpath = '//*[@id="form-input"]/div[3]/img'
capcha_src = selector.xpath('//*[@id="form-input"]/div[3]/img')[0].attrib['src']
capcha_src = 'https://jaccount.sjtu.edu.cn/jaccount/' + capcha_src
print (capcha_src)
capcha_res = requests.get(capcha_src, headers = headers)
# print (type(capcha_res.content))

f = open('test.jpg', 'wb')
f.write(capcha_res.content)
f.close()

login_url_3 = 'https://jaccount.sjtu.edu.cn/jaccount/ulogin'
login_data = {
	'sid': 'sid'
}

print (cookies)
