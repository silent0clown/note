import requests   # requests模块需要使用 pip 命令安装
import json
from datetime import datetime
import logging
import time 
# 第一步：创建日志器对象，默认等级为warning
logger = logging.getLogger("[REMOTE MATCH]")
logging.basicConfig(level="INFO")

# 第二步：创建控制台日志处理器+文件日志处理器
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./log.txt",mode="a",encoding="utf-8")

# 第三步：设置控制台日志的输出级别,需要日志器也设置日志级别为info；----根据两个地方的等级进行对比，取日志器的级别
console_handler.setLevel(level="WARNING")

# 第四步：设置控制台日志和文件日志的输出格式
console_fmt = "%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s--->%(lineno)d"
file_fmt = "[%(levelname)s][%(asctime)s]:%(message)s"
# file_fmt = "%(lineno)d--->%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s"

fmt1 = logging.Formatter(fmt = console_fmt)
fmt2 = logging.Formatter(fmt = file_fmt)

console_handler.setFormatter(fmt = fmt1)
file_handler.setFormatter(fmt = fmt2)

# 第五步：将控制台日志器、文件日志器，添加进日志器对象中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

headers = {
    'Content-Type' : 'application/json; charset=utf-8',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoic29jX2FwaSIsInVzZXJuYW1lIjoiYWRtaW4iLCJhbGlhcyI6IkFJUyIsInRlbmFudF91dWlkIjoiMjhhNzFmYjI1MzU2NGZjZWI4Y2MyZjlkODk3NTc5ZmEiLCJtc3BfdXVpZCI6IjU0YTNmMjM4N2Y4ODQzNzJiZjc0ODZkYzVjMjhiNTVlIiwidXNlcl91dWlkIjoiNWI4YjIxMzQ3NWE2NGIyMWI4YThiMDEzMzYxNmE2MWQiLCJzdWIiOiJhZG1pbkB0cmFpbmluZy5hc2lhaW5mby1zZWMiLCJpYXQiOjEsImV4cCI6MTcwNDAxNjgwMH0.qbR9cgsDBu1eqr6UEg3xy6Fs9IMtE2KAE_VaGW6aCUugW0Sm3C74170E2HaUlL0MI34U34RIdAyIoXGhZH2kKw',
}
# data = '{\t"appId": appId,\t"appSecret": "appSecret"}'
http1 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=test.ceye.io&data_type=1'
http2 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=q10157.net&data_type=1'
http3 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=kozuwuwupoxofi.rf.gd&data_type=1'
http4 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=giwinilugo.epizy.com&data_type=1'
http5 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=yulistasupportservices.info&data_type=1'
http6 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=cavt894vahm5n2g00010617pd7gbomswo.oast.site&data_type=1'
http7 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=mgjrkwgietkqv.mp&data_type=1'
http8 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=bmrfdf.rusradio1.ru&data_type=1'
http9 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=finanzfaultier.com&data_type=1'
http10 = 'https://soc-test.edr-saas.asiainfo-sec.com/ioc/api/maldium/v1/lookup?data_value=nidc.aikapool.com&data_type=1'

def do_search():
    for i in [http1, http2, http3, http4, http5, http6, http7, http8, http9, http10]:
        # search_value = 'http' + str(i)
        # print(search_value)
        response = requests.get(i, headers=headers)
        # print(response)
        data = (json.loads(response.content))['data']
        rule_id = (json.loads(response.content))['data']['rule_uuid']
        if(rule_id == ''):
            # print("[error] no match", i)
            logger.warning("no match ioc: %s"% i)
        else:
            # print('match',i)
            logger.info("match ioc: %s"% i)

        # print((json.loads(response.content))['data'])
        # print((json.loads(response.content))['data']['rule_uuid'])

# # print(type(int(json.loads(response.content))))  

if __name__ == '__main__':

    logger.info(datetime.now())
    while(1):
        print('------- ', datetime.now(), ' ------')
        do_search()
        time.sleep(30)
