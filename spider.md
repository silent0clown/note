# 环境配置
## 1、Windows环境
1. 安装python和谷歌浏览器
2. 安装python库pip install requests/Selenium/urllib3/aiohttp/cchardet/aiodns/lxml/beautifulsoup4(依赖lxml)/pyquery
    这里有个坑，urllib3 2.0.x版本与selenium3.141.x版本不兼容，后续运行时会报错，可以指定pip install urllib3==1.26.2规避
3. 安装chromedriver
    1. chromedirver版本需与浏览器版本保持一致
    2. 将chromedriver压缩包下chromedriver.exe文件放到Python的Scripts目录下
    3. 将chromedriver.exe放到浏览器安装路径Application目录下
    4. 将Application路径添加到系统变量
4. 测试验证,如果打开一个浏览器显示百度页面则成功
   ```python
   from selenium import webdriver
   
   browser = webdriver.Chrome()
   browser.get("http://www.baidu.com")
   ```
5. 安装tesseract，将图形验证码翻译成电子文本
   1. 下载安装包安装https://blog.csdn.net/weixin_42042397/article/details/88725822，需要勾选additional language，扩展支持的语言包
   2. 安装好之后pip install tesserocr pillow
        这里在win10上下载不成功，可以参考链接https://blog.csdn.net/coolcooljob/article/details/80385711尝试
        win10上安装Pillow失败，https://www.cnblogs.com/linyouyi/p/11427167.html
6. 验证安装
    1. 下载示例图片
    2. python 执行代码
    ```python
    import tesserocr
    from PIL import Image
    
    image = Image.open('image.png')
    print(tesserocr.image_to_text(image))
    ```
    如果成功，能够显示图片的txt文本。
    显示initAPI失败参考文档https://blog.csdn.net/Yuyh131/article/details/103880585

7. 安装数据库 mysql
    https://blog.csdn.net/qq_37984259/article/details/104517965
8. 安装mongoDB
9. 安装redis
10. Python与数据库的交互库安装pip install pymysql/pymongo/redis   gem install redis-dump
11. web库安装 pip install flask/tornado
12. 安装软件charles  [参考链接](https://blog.csdn.net/qq_35835118/article/details/94381177)
13. python库安装 pip install mitmproxy(mitmprxy证书跳过了)
14. appium安装(先跳过)
15. 安装爬虫框架pyspider和scrapy   pip install pyspider/Scrapy












## 2、Linux环境
1. 安装Python和谷歌浏览器
2. 安装Python库 pip install requesets/selenium
3. 下载对应版本的chromedriver,将可执行程序chromedriver移动到/usr/bin目录下
4. 安装chromedriver
    1. chromedirver版本需与浏览器版本保持一致
    2. 将chromedriver压缩包下chromedriver.exe文件放到Python的Scripts目录下
    3. 将chromedriver.exe放到浏览器安装路径Application目录下
    4. 将Application路径添加到系统变量
5. 测试验证,如果打开一个浏览器显示百度页面则成功
   ```python
   from selenium import webdriver
   
   browser = webdriver.Chrome()
   browser.get("http://www.baidu.com")
   ```
6. sudo apt-get install -y tesseractor-ocr libtesseract-dev libleptonica-dev
7. 安装数据库
   apt-get install -y mysql-server mysql-client



