headers_table = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIZE 5.5; Windows NT)'
}
##    ----------------------------------------- splite line -----------------------------------------       ##
# test plantomJS
# from selenium import webdriver
# browser = webdriver.PhantomJS()
# browser.get("http://www.baidu.com")
# print(browser.current_url)


##    ----------------------------------------- splite line -----------------------------------------       ##
# test tesserocr
# import tesserocr
# from PIL import Image
# image = Image.open('image.png')
# print(tesserocr.image_to_text(image))



# URL urllib
##    ----------------------------------------- splite line -----------------------------------------       ##
# import urllib.request
# response = urllib.request.urlopen('https://www.zhihu.com')
# # print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader('Server'))

##    ----------------------------------------- splite line -----------------------------------------       ##
# import urllib.parse
# import urllib.request
# import socket
# import urllib.error

# data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
# try:
#     response = urllib.request.urlopen('http://httpbin.org/post', data=data, timeout=1)
#     print(response.read())
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print("TIME OUT")

##    ----------------------------------------- splite line -----------------------------------------       ##
# import urllib.request, urllib.parse

# url_info = 'http://httpbin.org/post'
# dict = {
#     'name':'Germey'
# }
# data_info = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
# request = urllib.request.Request(url = url_info, data = data_info, headers = headers_table)
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.4 POST请求
# import requests
# data = {'name' : 'germey', 'age':22}
# r = requests.post("http://httpbin.org/post", data=data)
# print(r.text)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 验证
## 这种方法不可以登录知乎
# from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
# from urllib.error import URLError

# username = ''
# password = ''
# url = 'https://www.zhihu.com/signin?next=%2Fhot'

# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None, url, username, password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)

# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)



##    ----------------------------------------- splite line -----------------------------------------       ##
## 代理
# from urllib.error import URLError
# from urllib.request import ProxyHandler, build_opener

# proxy_handler = ProxyHandler({
#     'http': 'http://127.0.0.1:9743',
#     'https': 'https://127.0.0.1:9743'
# })
# opener = build_opener(proxy_handler)
# try:
#     response = opener.open('https://www.baidu.com')
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

##    ----------------------------------------- splite line -----------------------------------------       ##
## Cookies
# import http.cookiejar, urllib.request

# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name+"="+item.value)

##    ----------------------------------------- splite line -----------------------------------------       ##
# URLERROR
# from urllib import request, error
# try:
#     response = request.urlopen('http://cuiqingcai.com/index.htm')
# except error.URLError as e:
#     print(e.reason)


##    ---------------------------------------- 3.1.3解析链接 -----------------------------------------       ##
# from urllib.parse import urlparse

# result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
# print(type(result), result)
# # 必须得带http才行
# # <class 'urllib.parse.ParseResult'> ParseResult(scheme='www.baidu.com', netloc='', path='8080/index.html;user', params='', query='id=5', fragment='comment')

# result = urlparse('www.baidu.com:8080/index.html;user?id=5#comment')
# print(type(result), result)
# result = urlparse('www.baidu.com/index.html;user?id=5#comment', scheme= 'https')
# print(type(result), result)
# result = urlparse('www.baidu.com/index.html;user?id=5#comment', allow_fragments=False)
# print(type(result), result)

#### urlunparse()
# from urllib.parse import urlunparse
# data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6', 'comment']
# print(urlunparse(data))


#### urlsplit
# from urllib.parse import urlsplit

# result = urlsplit('http://www.baidu.com/index.html;user?id=5#comment')
# print(result)
# print(result[1])
# print(result[8])

#### urlunsplit
# from urllib.parse import urlunsplit

# data = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
# print(urlunsplit(data))


#### urljoin()
# from urllib.parse import urljoin

# print(urljoin('http://www.baidu.com', 'FAQ.html'))
# print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
# print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
# print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
# print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
# print(urljoin('http://www.baidu.com', '?category=2#comment'))
# print(urljoin('www.baidu.com', '?category=2#comment'))
# print(urljoin('www.baidu.com#comment', '?category=2'))


#### urlencode
# from urllib.parse import urlencode

# params = {
#     'name': 'germey',
#     'age': 22
# }
# base_url = 'http://www.baidu.com?'
# url = base_url + urlencode(params)
# print(url)


#### 反序列化 
# from urllib.parse import parse_qs

# query = 'name=germey&age=22'
# print(parse_qs(query))

# from urllib.parse import parse_qsl

# query = 'name=germey&age=22'
# print(parse_qsl(query))


#### 中文搜索乱码，将中文字符转化为URL编码
# from urllib.parse import quote

# keyword = '壁纸'
# url = 'https://www.baidu.com/s?wd=' + quote(keyword)
# print(url)

#### 解码
# from urllib.parse import unquote

# url = 'https://www.baidu.com/s?wd=%E5%A3%81%E7%BA%B8'
# print(unquote(url))



##    ----------------------------------------- 3.2 使用requests -----------------------------------------       ##
# import requests

# r = requests.get('https://www.baidu.com/')
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text)
# print(r.cookies)

# r = requests.post('http://httpbin.org/post')
# r = requests.put('http://httpbin.org/put')
# r = requests.delete('http://httpbin.org/delete')
# r = requests.head('http://httpbin.org/get')
# r = requests.options('http://httpbin.org/get')

# import requests

# data = {
#     'name': 'germey',
#     'age': 22
# }
# r = requests.get("http://httpbin.org/get", params=data)
# print(r.text)


# import requests
# import re

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# }
# r = requests.get("https://www.zhihu.com/explore", headers=headers)
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, r.text)
# print(titles)



# 抓取图片音视频
# import requests
# import re
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }
# r = requests.get('https://www.zhihu.com/favicon.ico', headers=headers) 
# with open('zhihu.ico', 'wb') as f:
#     f.write(r.content)
# r = requests.get('https://www.baidu.com/favicon.ico', headers=headers) 
# with open('baidu.ico', 'wb') as f:
#     f.write(r.content)

# r = requests.get("https://www.zhihu.com/explore")
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, r.text)
# print(r.text)
# print(titles)


# import requests

# cookies = 'KLBRSID=46a537df17633233e0a02eea70ad140c|1700473799|1700473799'
# jar = requests.cookies.RequestsCookieJar()
# headers = {
#     'Host': 'www.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
# }
# for cookie in cookies.split(';'):
#     key, value = cookie.split('=', 1)
#     jar.set(key, value)
# r = requests.get('http://www.zhihu.com', cookies=jar, headers=headers)
# print(r.text)

# import requests

# requests.get('http://httpbin.org/cookies/set/number/123456789')
# r = requests.get('http://httpbin.org/cookies')
# print(r.text)

# import requests

# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/number/123456789')
# r = s.get('http://httpbin.org/cookies')
# print(r.text)

# import requests

# response = requests.get('https://www.12306.cn', verify=True)
# print(response.status_code)

# print("spilet------")
# response = requests.get('https://www.12306.cn', verify=False)
# print(response.status_code)


##    ----------------------------------------- 3.3 正则表达式 -----------------------------------------       ##
# import re

# content = 'Hello 123 4567 World_This is a Regex Demo'
# print(len(content))
# result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}', content)
# print(result)
# print(result.group())
# print(result.span())
##    ----------------------------------------- splite line -----------------------------------------       ##

# from urllib import request,error
# try:
#     response = request.urlopen('http://cuiqingcai.com/index.htm')
# except error.HTTPError as e:
#     print(e.reason, e.code, e.headers, sep='\n')


##    ----------------------------------------- splite line -----------------------------------------       ##
# 抓取图片音视频
# import requests
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }
# r = requests.get('https://www.baidu.com/favicon.ico', headers=headers) 
# with open('zhihu.ico', 'wb') as f:
#     f.write(r.content)












##    ----------------------------------------- splite line -----------------------------------------       ##
# GET请求
# import requests
# import re
# # data = {
# #     'name' : 'germey',
# #     'age' : 22
# # }
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }

# r= requests.get('https://www.zhihu.com/explore', headers=headers)
# print(r.text)
# # 这个正则有问题
# pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
# titles = re.findall(pattern, r.text)
# print(titles)








##    ----------------------------------------- splite line -----------------------------------------       ##
# import requests

# r= requests.get('http://www.baidu.com/')
# # r= requests.post('http://www.baidu.com/post')
# print(type(r))
# print(r.status_code)
# print(type(r.text))
# print(r.text)
# print(r.cookies)

##    ----------------------------------------- splite line -----------------------------------------       ##



# import socket
# from urllib import request, parse
# import urllib.error

# url = 'http://www.httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
#     'Host': 'www.httpbin.org'
# }

# dict = {
#     'name' : 'Germey'
# }

# data = bytes(parse.urlencode(dict), encoding='utf-8')

# req = request.Request(url = url, data = data, headers= headers, method= 'POST')

# try:
#     response = request.urlopen(req)
#     print(response.read().decode('utf-8'))
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print("TIME OUT")
    

# from urllib import request
# response = request.urlopen('https://www.python.org', timeout= 1)
# # read()得到网页内容
# # status()得到返回结果状态码
# # readinto() getheader(name) getheaders() fileno() msg version reason debuglevel closed等
# # print(response.read().decode('utf-8'))
# print(response.status)
# print(response.getheaders())

### test scrapyd-api
# from scrapyd_api import ScrapydAPI
# scrapyd = ScrapydAPI('http://127.0.0.1:6800')
# print(scrapyd.list_projects())

### end test scrapyd-api

### test tornado
# import tornado.ioloop
# import tornado.web

# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("hello world")

# def make_app():
#     return tornado.web.Application([
#         (r"/", MainHandler),
#         ])

# if __name__ =="__main__":
#     app = make_app()
#     app.listen(8888)
#     tornado.ioloop.IOLoop.current().start()

### end test tronado

### test flask
# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# if __name__ == "__main__":
#     app.run()
### end test flask

### test tesserocr

# import tesserocr
# from PIL import Image
# image = Image.open('image.png')

# print(tesserocr.image_to_text(image))
### end test tesserocr


#!/usr/bin/ python
# ## test phantomjs
# from selenium import webdriver
# browser = webdriver.PhantomJS()
# browser.get("https://www.baidu.com")
# print(browser.current_url)
# #  success if show:
# #  https://www.baidu.com/
# ## end test

### test bs4
# from bs4 import BeautifulSoup
# soup = BeautifulSoup('<p>Hello</p>', 'lxml')
# print(soup.p.string)
## success if show: Hello
### end test bs4

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.1.5 响应

# import requests

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }

# r= requests.get('http://www.jianshu.com',headers=headers)

# exit() if not r.status_code == requests.codes.ok else print('Request Success')
# print(type(r.status_code), r.status_code)
# print(type(r.headers), r.headers)
# print(type(r.cookies), r.cookies)
# print(type(r.url), r.url)
# print(type(r.history), r.history)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.1 文件上传
# import  requests

# files = {'file':open('favicon.ico', 'rb')}
# r = requests.post("http://httpbin.org/post", files = files)
# print(r.text)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.2 Cookies
# import requests

# headers = {
#     # 'Cookie' : '_zap=44e5be7e-9a60-4478-8830-c874692cc8e1',
#     'Host' :'wwww.zhihu.com',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36',
# }

# r = requests.get("https://www.zhihu.com", headers=headers)
# print(r.text)

# # for key, value in r.cookies.items():
# #     print(key + '=' + value)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.3 会话维持  
## 利用Session做到模拟同一个会话，通常用于模拟登陆成功之后再进行下一步的操作，在平常用的非常广泛。
# import requests
# requests.get('http://httpbin.org/cookies/set/number/1234567890')
# r = requests.get('http://httpbin.org/cookies')
# print("noraml request:")
# print(r.text)

# s = requests.Session()
# s.get('http://httpbin.org/cookies/set/number/1234567890')
# r = s.get('http://httpbin.org/cookies')
# print("Session Request:")
# print(r.text)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.4 SSL证书验证
## verify参数

# import requests

# response = requests.get('https://www.12306.cn')
# print("True SSL Verify")
# print(response.status_code)

# response = requests.get('https://www.12306.cn', verify=False)
# print("\nFalse SSL Verify")
# print(response.status_code)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.5 代理设置
# import requests

# proxies = {
#     # 需改为有效代理地址
#     "http" : "http://1.10.1.10:3128",
#     "https": "https://1.10.1.10:1080",
#     # 若代理需要使用HTTP BASIC AUTH
#     "http" : "http://user:password@1.10.1.10:3128/",
#     #SOCKS协议代理
#     'http' : 'socks5://user:password@host:port'
# }

# requests.get("https://www.taobao.com", proxies=proxies)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.6 超时设置
## timeout 如果超时，会抛出异常
# import requests
# import socket
# # try:
# #     response = request.urlopen(req)
# #     print(response.read().decode('utf-8'))
# # except urllib.error.URLError as e:
# #     if isinstance(e.reason, socket.timeout):
# #         print("TIME OUT")
# try:
#     r = requests.get("https://www.taobao.com", timeout=10)
# except requests.ConnectionError as e :
#     if isinstance(e.errno, socket.timeout):
#         print(TimeoutError)

# print(r.status_code)

# # timeout元祖值：连接、读取、连接+读取总时长
# r = requests.get("https://www.taobao.com", timeout=(5,11))
# print(r.status_code)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.7 身份认证
## auth

# import requests
# from requests.auth import HTTPBasicAuth

# # r = requests.get('http://localhost:5000')
# # print(r.status_code)

# r = requests.get('http://localhost:5000', auth=HTTPBasicAuth('admin', '123456'))
# # or
# # r = requests.get('http://localhost:5000', auth=('username', 'passwd'))

# print(r.status_code)



##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.2.2.8 Prepared Request
## 构造Request队列, 可以将请求当做独立的对象看待
# from requests import Request, Session

# url = 'http://httpbin.org/post'
# data = {
#     'name':'germey'
# }

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }

# s = Session()
# # 构造一个Request对象req
# req = Request('POST', url, data= data, headers=headers)
# # 将req转换为Prepared Request对象prepped
# prepped = s.prepare_request(req)
# # 发送prepped
# r=s.send(prepped)
# print(r.text)


##    ----------------------------------------- splite line -----------------------------------------       ##
##    ---------------------------------------- 3.3 正则表达式 ----------------------------------------       ##

## 3.3.1
## URL匹配正则  [a-zA-z]+://[^\s]*
## \s ：匹配任意的空白字符
######################## 正则匹配规则 #######################################################################
##  模 式                                                  描 述                                          ##
#    \w              匹配字母、数字和下划线                                                                  
#    \W              匹配不是字母、数字和下划线的字符                                                        
#    \s              匹配任意空白字符，等价于[\t\n\r\f]                                                      
#    \S              匹配任意非空字符                                                                        
#    \d              匹配任意数字，等价于[0-9]
#    \D              匹配任意非数字的字符
#    \A              匹配字符串开头
#    \Z              匹配字符串结尾，如果存在换行，只匹配到换行前的结束字符串
#    \z              匹配字符串结尾，如果存在换行，还会匹配换行符
#    \G              匹配最后匹配完成的位置
#    \n              匹配一个换行符
#    \t              匹配一个制表符
#    ^               匹配一行字符串的开头
#    $               匹配一行字符串的结尾
#    .               匹配任意除了换行符的任意字符
#    [...]           用来表示一组字符，单独列出，比如[amk]匹配a、m或k
#    [^...]          不在[]中的字符，比如[^abc]匹配除了a,b,c之外的字符
#    *               匹配0个或多个表达式
#    +               匹配1个或多个表达式
#    ?               匹配0个或1个前面的正则表达式定义的片段，非贪婪方式
#    {n}             精确匹配n个前面的表达式
#    {n, m}          匹配n到m次由前面正则表达式定义的片段，贪婪方式
#    a|b             匹配a或b
#    ( )             匹配括号内的表达式，也表示一个组
#############################################################################################################

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.3.2 match()
# import re
# content = 'Hello 123 4567 World_This is a regex demo'
# print(len(content))
# # \d{4} 对应 4567  \w{10} 对应World_This
# result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}',content)

# regroup = re.match('^Hello\s(\d+)\s\d',content)
# print("match result: ",result)
# print(result.group())
# # print(result.group(1))
# print(result.span())

# print("match result :", regroup)
# print("match content :",regroup.group())
# # 输出第一个被()包围的匹配结果, if no, raise error
# print(regroup.group(1))
# print(regroup.span)

# dotre = re.match('^Hello.*demo$', content)
# print("dot match :",dotre)
# print(dotre.group())
# print(dotre.span())

# # 贪婪匹配
# result = re.match('^H.*(\d+).*mo$',content)
# print('\ngreedy match result:\n',result) 
# print(result.group()) 
# print(result.group(1)) 

# # 非贪婪匹配, .*?不能在字符串结果，否则可能匹配不到任何内容
# result = re.match('^H.*?(\d+).*mo$',content)
# print('\nungreedy match result:\n',result) 
# print(result.group()) 
# print(result.group(1)) 

# # re.S修饰符，可以使*匹配换行符
# content = '''Hello  1234567 World_This
# is a Regex Demo
# '''
# result = re.match('^H.*?(\d+).*mo$',content, re.S)
# print(result.group(1)) 

# ########################################################
# ####################### 修饰符表 ########################
# # re.I           使匹配对大小写不敏感
# # re.L           做本地化识别匹配
# # re.M           多行匹配，影响^和$
# # re.S           使.匹配包括换行符在内的所有字符
# # re.U           根据Unicode字符集解析字符。这个标志影响\w,\W,\b,\B
# # re.X           更灵活的格式使正则表达式写的更容易理解

# # 转义匹配
# content  = '(百度)www.baidu.com'
# result   = re.match('\(百度\)www\.baidu\.com', content)
# print("\nzhuanyi match result:\n", result.group())

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.3.3 search()  匹配时扫描整个字符串，然后返回第一个成功匹配的结果
# import re 

# content = 'Extra strings Hello 123 4567 World_This is a regex demo'
# result = re.search('Hello.*?(\d+).*demo',content)
# print(result.group())

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.3.4 findall() 搜索整个字符串，返回所有匹配的内容

##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.3.5 sub() 替换匹配的字符
# import re

# content = '54ajska231djsd033djds'
# content = re.sub('\d+', 'M', content)     
# print(content)
# content = re.sub('\d+', '', content)     
# print(content)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.3.6 compile() 将正则字符串编译成正则表达式对象
# import re

# content1 = '2016-12-15 12:00'
# content2 = '2016-12-17 12:55'
# content3 = '2016-12-22 13:21'
# print(re.findall("\d{2}:\d{2}",content1))
# pattern = re.compile('\d{2}:\d{2}')
# print(pattern)
# result1 = re.sub(pattern, '', content1)
# result2 = re.sub(pattern, '', content2)
# result3 = re.sub(pattern, '', content3)
# print(result1, result2, result3)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 3.4 抓取猫眼电影排行TOP100
# import json
# import requests
# from requests.exceptions import RequestException
# import re
# import time

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }

# def get_one_page(url):
#     try:
#         response = requests.get(url,headers=headers)
#         if response.status_code == 200:
#             print(response.text)
#             return response.text

#         return None
#     except RequestException:
#         return None


# def parse_one_page(html):
#     pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
#                          + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
#                          + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
#     items = re.findall(pattern, html)
#     for item in items:
#         yield {
#             'index': item[0],
#             'image': item[1],
#             'title': item[2],
#             'actor': item[3].strip()[3:],
#             'time': item[4].strip()[5:],
#             'score': item[5] + item[6]
#         }


# def write_to_file(content):
#     with open('result.txt', 'a', encoding='utf-8') as f:
#         f.write(json.dumps(content, ensure_ascii=False) + '\n')


# def main(offset):
#     url = 'http://maoyan.com/board/4?offset=' + str(offset)
#     html = get_one_page(url)
#     for item in parse_one_page(html):
#         print(item)
#         write_to_file(item)


# if __name__ == '__main__':
#     for i in range(10):
#         main(offset=i * 10)
#         time.sleep(10)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 第4章  解析库的使用
## 4.1 使用XPatch XML路径语言，在XML文档中查找信息

###############  XPatch规则 ###################
##  表达式                  描述
#   nodename              选取此节点的所有子节点
#   /                     从当前节点选取直接子节点
#   //                    从当前节点选取子孙节点
#   .                     选取当前节点
#   ..                    选取当前节点的父节点
#   @                     选取属性
################################################

# 例 title[@lang='eng']
# from lxml import etree

# #etree可以自动修正HTML text
# html = etree.parse('./maoyan.html', etree.HTMLParser())
# # result = etree.tostring(html)
# # print(result.decode('utf-8'))

# # * 匹配所有节点，返回一个列表
# result = html.xpath('//*')

# # 查找元素子节点,li节点的所有a子节点
# result = html.xpath('//li/a')
# # 查找ul节点下所有的孙子节点
# result = html.xpath('//ul//a')

# print(result)

# 父节点
# from lxml import etree

# html = etree.parse('./maoyan.html', etree.HTMLParser())

# # 查找a节点下元素为href="//www.maoyan.com"的父节点的class属性内容
# result = html.xpath('//a[@href="//www.maoyan.com"]/../@class')
# # or
# # result = html.xpath('//a[@href="//www.maoyan.com"]/parent::*/@class')
# print(result)

## html 文本说明
## 如： <span class="apptext">APP下载</span>
## span         : 节点
## apptext      ：节点属性
## APP下载      ： 节点内容

# 文本获取 text()
# from lxml import etree

# html = etree.parse('./maoyan.html', etree.HTMLParser())
# result = html.xpath('//li//text()')
# print(result)
# contain()
# 对于多属性节点，需要contains匹配
# 如 <span class="apptext appcontent">APP下载</span> 有apptext appcontent两个属性
# 解析为 html.xpath('//span[contains(@class, "apptext")]/text()')


# <span class="apptext appcontent" name="item">APP下载</span>
# 解析为 html.xpath('//span[contains(@class, "apptext") and @name="tiem"]/text()')

## 按序选择
# html.xpath('//span[contains(@class, "apptext")][1]/text()')       # 选择第一个
# html.xpath('//span[contains(@class, "apptext")][last()]/text()')       # 选择最后一个
# html.xpath('//span[contains(@class, "apptext")][postion() < 3]/text()')       # 选择前三个
# html.xpath('//span[contains(@class, "apptext")][last() - 2]/text()')       # 选择倒数第三个

## 节点轴选择
# result = html.xpath('//li[1]/ancestor::*')     # 获取li[1]节点的所有祖先节点
# result = html.xpath('//li[1]/ancestor::div')   # 获取li[1]节点的div祖先节点
# result = html.xpath('//li[1]/attribute::*')    # 获取节点的所有属性
# result = html.xpath('//li[1]/child::*')        # 获取所有子节点
# result = html.xpath('//li[1]/descendant::*')   # 获取所有子孙节点


##    ----------------------------------------- splite line -----------------------------------------       ##
## 4.2 使用 Beautiful Soup   HTML或XML的解析库。用于从网页中提取数据

# beauftiful soup支持的解析器:
# html.parser
# lxml           速度快，容错能力强
# xml
# html5lib
# 总结：
# 1. 推荐使用xml库，必要时使用html.parser
# 2. 节点选择筛选功能弱但是速度快
# 3. 尽量使用find()或find_all()查询匹配
# 4. 如果熟悉CSS，可以使用select()方法选择



##    ----------------------------------------- splite line -----------------------------------------       ##

# html = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
# <p class="story">...</p>
# """
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html, 'lxml')
# 以标准的缩进格式输出
# print(soup.prettify())
# 提取title节点的文本内容
# print(soup.title.string)
# print(soup.title)
# print(soup.head)
# print(soup.a.string)
# print(soup.a.name)
# print(soup.a.attrs)      # 获取属性，返回字典
# print(soup.a.attrs['herf'])      # 获取属性，返回字典
# print(soup.a['herf'])      # 与上一行等价
# print(soup.body.contents)      # 获取body节点下所有内容
# print(soup.p.children)      # 获取p下所有子节点
# for i,child in enumerate(soup.p.children):  #
#     print(i, child)

# print(soup.find_all(name='a'))    # 查询所有符合条件的元素，包括属性或文本
# print(soup.find_all(name='a')[1])    # 查询所有符合条件的元素，包括属性或文本
# print(soup.find_all(attrs={'id':"link1"}))    # 查询所有符合条件的元素，包括属性或文本
# print(soup.find_all(string=re.compile('their')))
# print(soup.find(string=re.compile("Lacie")))


# find()返回第一个匹配的元素，find_all返回所有匹配的元素组成的列表
# find_parents()  # 返回所有祖先节点
# find_parent()     # 返回直接父节点
# find_next_siblings()       # 返回后面的所有兄弟节点
# find_next_sibling()        # 返回后面第一个兄弟节点
# find_previous_siblings()   # 返回前面所有的兄弟节点
# find_previous_sibing()     # 返回前面的第一个节点

##这里 string 获取文本，name获取属性名称，attrs获取属性
##    ----------------------------------------- splite line -----------------------------------------       ##
## CSS选择器

# html= '''
# <div class= "panel">
# <div class="panel-heading">
# <h4>Hello</h4>
# </div>
# <div class="panel-body">
# <ul class="list" id="list-1">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# <li class="element">Jay</li>
# </ul>
# <ul class="list list-small" id="list-2">
# <li class="element">Foo</li>
# <li class="element">Bar</li>
# </ul>
# </div>
# </div>

# '''


# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html, 'lxml')
# print(soup.select('.panel .panel-heading'))   # select传入相应的CSS选择器
# # print(soup.select('ul li'))
# # print(soup.select('#list-2 .element'))
# # print(type(soup.select('ul')[0]))


##    ----------------------------------------- splite line -----------------------------------------       ##
## 4.3 使用pyquery  CSS选择器的功能比较强大
# 功能类似 bs4，先不研究了
# html = '''
# <div>
#     <ul>
#          <li class="item-0">first item</li>
#          <li class="item-1"><a href="link2.html">second item</a></li>
#          <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
#          <li class="item-1 active"><a href="link4.html">fourth item</a></li>
#          <li class="item-0"><a href="link5.html">fifth item</a></li>
#      </ul>
#  </div>
# '''
# from pyquery import PyQuery as pq
# doc = pq(html)
# print(doc('li'))

# from pyquery import PyQuery as pq
# # doc = pq(url='http://cuiqingcai.com')
# doc = pq(filename = 'index.html')
# print(doc('title'))


html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
# from pyquery import PyQuery as pq
# doc = pq(html)
# # 先选取id为container的节点，然后再选取内部的class为list的节点内部的所有li节点
# print(doc('#container .list li'))
# print(type(doc('#container .list li')))

# from pyquery import PyQuery as pq
# doc = pq(html)
# items = doc('.list')
# print(type(items))
# print(items)
# lis = items.find('li')
# print(type(lis))
# print(lis)

##    ----------------------------------------- splite line -----------------------------------------       ##
## 文件存储
## 方法有write txt json csv
# import requests 
# from pyquery import PyQuery as pq 
# url  =  'https://www.zhihu.com/explore'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2473.116 Safari/537.36'
# }
# html=  requests.get(url, headers=headers).text 
# doc =  pq(html) 
# items=  doc('.explore-tab  .feed-item').items() 
# for item in items: 
#     question =  item.find ('h2').text()
#     author  = item.find('.author-link-line').text() 
#     answer=  pq(item .find ('.content').html()).text() 
#     file  = open('explore.txt', 'a', encoding = 'utf-8')
#     file.write('\n'.join([question, author, answer])) 
#     file.write('\n'+ '='* 50 +'\n') 
#     file.close()

# import csv

# with open('data.csv', 'w')as f:
#     # writer =  csv.writer(f)
#     # writer.writerow(['id', 'name', 'age'])
#     # writer.writerow(['1', 'meke', 20])
#     # writer.writerow(['2', 'bob', 13])
#     # writer.writerow(['3', 'jab', 33])

#     # 字典写入
#     fieldnames= ['id', 'name', 'age']
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow({'id':1, 'name':'make', 'age':20})
#     writer.writerow({'id':2, 'name':'cade', 'age':30})
#     writer.writerow({'id':3, 'name':'csae', 'age':39})

# # 读取
# with open('data.csv', 'r', encoding='utf-8') as f:
#     reader=csv.reader(f)
#     for row in reader:
#         print(row)


##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.2 关系型数据库的存储MySQL


# # 创建一个数据库spiders，创建一次即可
# import pymysql

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306)
# cursor = db.cursor()
# cursor.execute('SELECT VERSION()')
# # fetchone()获得执行数据
# data = cursor.fetchone()
# print('Database version:', data)
# # 创建一个库spiders
# cursor.execute("CREATE DATABASE spiders DEFAULT CHARACTER SET utf8")
# db.close()

##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.2 创建数据表
################# 数据表 ######################
# 字段名           含义              类型
#  id              学号             varchar
#  name            姓名             varchar
#  age             年龄             int
##############################################

# import pymysql

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()
# sql = 'CREATE TABLE IF NOT EXISTS students(id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY(id))'
# cursor.execute(sql)
# db.close()


##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.2 向表中插入数据

# import pymysql

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# sql_cmd = 'INSERT INTO students(id, name, age) values(%s, %s, %s)'
# try:
#     cursor.execute(sql_cmd, ('001', 'mike', '17'))
#     # 执行这个才可实现数据插入， 插入、更新、删除都需要调用该方法
#     db.commit()
# except:
#     # 如果执行失败，通过rollback()执行数据回滚
#     db.rollback()
# db.close()

# ########################## 事务机制 #############################
# # 原子性：事务是一个不可分割的工作单位，要么都做，要么都不做
# # 一致性：事务必须使数据库从一个一致性状态到另一个一致性状态
# # 隔离性：一个事务的执行不能被其他事务干扰
# # 持久性：对数据库中的数据改变是永久性的，故障或其他操作不该对其有影响。
# #################################################################


##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.2 向表中插入的数据以字典形式，便于新增变量

# import pymysql

# data = {
#     'id' : '002',
#     'name' : 'Bob',
#     'age' : 18
# }

# table = 'students'

# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
# sql_cmd = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
# print(sql_cmd)
# # INSERT INTO students(id, name, age) VALUES (%s, %s, %s)

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# try:
#     if cursor.execute(sql_cmd, tuple(data.values())):
#         print("Success")
#         db.commit()
# except:
#     print("Fail")
#     db.rollback()
# db.close()

##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3 更新数据

# import pymysql

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# sql_cmd = 'UPDATE students SET age = %s WHERE name = %s'
# try:
#     cursor.execute(sql_cmd, (20, 'Bob')) 
#     db.commit()
# except:
#     db.rollback()
# db.close()   

##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3 对于重复数据进行更新，而不是重复插入

# import pymysql

# data = {
#     'id' : '002',
#     'name' : 'Bob',
#     'age' : 18
# }

# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))


# # ON DUPLICATE KEY UPDATE : 如果主键已经存在，就执行更新操作
# sql_cmd = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
# update = ','.join([" {key}=%s".format(key=key)for key in data])
# sql_cmd += update
# print(sql_cmd)
# # INSERT INTO students(id, name, age) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=%s, name=%s, age=%s

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# try:
#     # *2 得到UPDATE的参数
#     if cursor.execute(sql_cmd, tuple(data.values())*2):
#         print("Success")
#         db.commit()
# except:
#     print("Fail")
#     db.rollback()
# db.close()

##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3 删除数据

# import pymysql

# data = {
#     'id' : '002',
#     'name' : 'Bob',
#     'age' : 18
# }

# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
# conditon = 'age = 17'       # 'age == 18' 失败， 需要 'age = 18'

# sql_cmd = 'DELETE FROM {table} WHERE {conditon}'.format(table=table, conditon=conditon)
# print(sql_cmd)

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# try:
#     if cursor.execute(sql_cmd):
#         print("Success")
#         db.commit()
# except:
#     print("Fail")
#     db.rollback()
# db.close()

##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3 查询数据

# import pymysql

# data = {
#     'id' : '002',
#     'name' : 'Bob',
#     'age' : 18
# }

# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
# conditon = 'age = 17'       # 'age == 18' 失败， 需要 'age = 18'

# sql_cmd = 'SELECT * FROM {table} WHERE age >= 10'.format(table=table)
# print(sql_cmd)

# db = pymysql.connect(host='localhost',user='root',password='123456',port=3306, db='spiders')
# cursor = db.cursor()

# try:
#     cursor.execute(sql_cmd)
#     print(cursor.rowcount)
#     data = cursor.fetchone()
#     print(data)
#     result = cursor.fetchall()   # 如果数据量非常大，占用开小会很大，推荐用while 获取fetchone()
    # row = cursor.fetchone()
    # while row:
    # print("Row:", row)
    # row = cursor.fetchone()
#     print(result)
# except:
#     print("Fail")
# db.close()


##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3 非关系型数据库
## 对于爬虫的数据存储来说，一条数据可能存在某些字段提取失败而缺失的情况，而且数据可能随时调整，数据之间还存在嵌套关系
## 如果使用关系型数据库存储，意识需要提前建表，二是如果存在数据嵌套，需要进行序列化操作才可以存储，非常不方便
## 使用非关系型数据库可以避免这些麻烦，更简单高效


##    ----------------------------------------- splite line -----------------------------------------       ##
## 5.3.1 MongoDB
# import pymongo
# client = pymongo.MongoClient(host='localhost', port=27017)
# # 连接test数据库 == db = client['test]
# db = client.test

# # 指定集合
# collection = db.students
# # collection = db['students']

# # 插入数据
# student = {
#     'id':'001',
#     'name':'jay',
#     'age':20,
#     'gender':'male'
# }

# result = collection.insert_one(student)
# # insert_many([para1, para2,...])
# print(result)

# # 查询 find_one() or find()

# result = collection.find_one({'name':'jay'})
# print(type(result))
# print(result)

# # 根据ObjectId查询
# from bson.objectid import ObjectId
# result = collection.find_one({'_id': ObjectId('65266a7b4aefe493f6e72ce4')})
# print(result)

# # 范围查询

# # 查询年龄大于20的数据
# result = collection.find({'age':{'$gt':20}})
# ########################## 比较符号 ################################
# #  符号               含义                    示例
# #  $lt               小于            {'age' : {'$lt' : 20}}
# #  $lte              小于等于        {'age' : {'$lte' : 20}}
# #  $gt               大于            {'age' : {'$gt' : 20}}
# #  $gte              大于等于        {'age' : 20}
# #  $ne               不等于          {'age' : {'$ne' : 20}}
# #                    等于            {'age' : {'$ne' : 20}}
# #  $in               在范围内        {'age' : {'$in' : [20, 30]}}
# #  $nin              不在范围内       {'age' : {'$nin' : [20, 30]}}
# #####################################################################

# # count()
# count = collection.find().count()

# # 排序 sort
# result= collection.find().sort('name', pymongo.ASCENDING)     
# # pymongo.ASCENDING 指定升序
# # pymongo.DESCENDING 指定降序

# # 偏移 skip()
# result= collection.find().sort('name', pymongo.ASCENDING).skip(2)    # .limit(2)  # 限定取2个元素
# 偏移前两个元素，从第三个元素开始

# 更新 update()
# 更新Kevin年龄为25
# condition =  {'name':'Kevin'}
# student = collection.find_one(condition)
# student['age'] = 25
# result= collection.update_one(condition, {'$set' : student})

# 删除 remove()


### 5.3.2 Redis存储
# from redis import StrictRedis

# redis = StrictRedis(host='localhost',password='123456', port=6379)
# redis.set('name', 'Bob')

# print(redis.get('name'))
# print(redis.exists('name'))
# print(redis.type('name'))


##################################### 键操作 ########################################
# 方法                       作用                      示例             
# exists(name)           判断一个键是否存在         redis.exists('name')
# delete(name)           删除一个键                redis.delete('name')
# type(name)             判断键类型                redis.type('name')
# keys(pattern)          获取所有符合规则的键       redis.keys('n*')   获取n开头的键
# randomkey()            获取随机一个键             randomkey()
# rename(src, dst)       将src重命名为dst          redis.renmae('name', 'nickname')
# dbsize                 获取当前数据库中键的数目
# expire(name, time)     设定键的过期时间，单位为秒
# ttl(name)              获取键的过期时间，-1永不过期
# move(name, db)         将键移动到其他数据库
# flushdb()              删除当前选择数据库中的所有键
# flushall()             删除所有数据库中的所有键      
######################################################################################

################################### 字符串操作 #####################################
# set(name, value)
# get(name)
# getset(name, value)        给数据库中键为name的string赋值value并返回上一次的value
# mget(keys, *args)          返回多个键对应的value   例如：redis.mget(['name', 'nickname']) 返回name和nickname的value
# setnx(name, value)         如果不存在这个键对，则更新value，否则不变
# setex(name, time, value)   设置可以对应的值为string类型的value，并指定此键对应的有效期
# setrange(name, offset, value)  设置指定键的value值的子字符串
# mset(mapping)              批量赋值    redis.mset({'name1':'Mark', 'name2':'Job'})
# msetnx(mapping)            键均不存在时才批量赋值
# incr(name, amount=1)       键为name的value增值操作，默认为1,键不存在则被创建并设为1
# decr(name, amount=1)       减值操作
# append(key, value)         键为name的string的值附加value
# ...
#######################################################################################


########################################## 列表操作 ####################################
# rpush(name, *values)   在键为name的队列末尾添加值为value的元素        redis.rpush('list', 1, 2, 3)
# lpush(name, *values)   在队列头添加元素
# llen(name)             返回name列表的长度
# lrange(name, start, end)      返回列表name中start至end之间的元素
# lset(name, index, value)      给列表name中Index位置元素赋值value
# lrem(name, count, value)      删除count个键的列表中value元素
# lpop(name)                    返回并删除键为name的列表中的首元素
# rpop(name)                   
# ...
########################################################################################


################################### 集合操作 #####################################
# sadd(name, *values)                  向键为name的集合中添加元素     redis.sadd('tags', 'Book', 'Tea', 'Coffee')
# srem(name, *values)
# spop(name)
# smove(src, dst, value)
# scard(name)                         返回键为name的集合元素个数
# sismember(name, value)              测试value是否在集合name中
# sinter(key1, key2, ...)             返回键为key1和key2..的集合的交集元素
# ...
######################################################################################


##    ----------------------------------------- splite line -----------------------------------------       ##
## Ajax爬取
# from urllib.parse import urlencode
# import requests

# base_url = 'https://m.weibo.cn/api/container/getIndex?'

# headers = {
#     'Host':'m.weibo.cn',
#     'Referer':'https://m.weibo.cn/u/',
    
# }


# import pymongo
# from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
# from pyquery import PyQuery as pq
# from config import *
# from urllib.parse import quote

# # browser = webdriver.Chrome()
# browser = webdriver.PhantomJS()

# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument('--headless')
# # browser = webdriver.Chrome(chrome_options=chrome_options)

# wait = WebDriverWait(browser, 10)
# client = pymongo.MongoClient(MONGO_URL)
# db = client[MONGO_DB]


# def index_page(page):
#     """
#     抓取索引页
#     :param page: 页码
#     """
#     print('正在爬取第', page, '页')
#     try:
#         url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)
#         browser.get(url)
#         if page > 1:
#             input = wait.until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
#             submit = wait.until(
#                 EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_Submit')))
#             input.clear()
#             input.send_keys(page)
#             submit.click()
#         wait.until(
#             EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager li.item.active > span'), str(page)))
#         wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item')))
#         get_products()
#     except TimeoutException:
#         index_page(page)


# def get_products():
#     """
#     提取商品数据
#     """
#     html = browser.page_source
#     doc = pq(html)
#     items = doc('#mainsrp-itemlist .items .item').items()
#     for item in items:
#         product = {
#             'image': item.find('.pic .img').attr('data-src'),
#             'price': item.find('.price').text(),
#             'deal': item.find('.deal-cnt').text(),
#             'title': item.find('.title').text(),
#             'shop': item.find('.shop').text(),
#             'location': item.find('.location').text()
#         }
#         print(product)
#         save_to_mongo(product)


# def save_to_mongo(result):
#     """
#     保存至MongoDB
#     :param result: 结果
#     """
#     try:
#         if db[MONGO_COLLECTION].insert(result):
#             print('存储到MongoDB成功')
#     except Exception:
#         print('存储到MongoDB失败')


# def main():
#     """
#     遍历每一页
#     """
#     for i in range(1, MAX_PAGE + 1):
#         index_page(i)
#     browser.close()


# if __name__ == '__main__':
#     main()



import requests
from lxml import etree


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()
    
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div/input[2]/@value')
        return token
    
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            self.dynamics(response.text)
        
        response = self.session.get(self.logined_url, headers=self.headers)
        if response.status_code == 200:
            self.profile(response.text)
    
    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            print(dynamic)
    
    def profile(self, html):
        selector = etree.HTML(html)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')[0]
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print(name, email)


if __name__ == "__main__":
    login = Login()
    login.login(email='cqc@cuiqingcai.com', password='password')