# Time:2022 2022/3/1 17:20
# Author: Jasmay
# -*- coding: utf-8 -*-
import time
import logging

# 第一步：创建日志器对象，默认等级为warning
logger = logging.getLogger("这是我的一个小测试日志")
logging.basicConfig(level="INFO")

# 第二步：创建控制台日志处理器+文件日志处理器
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("./log.txt",mode="a",encoding="utf-8")

# 第三步：设置控制台日志的输出级别,需要日志器也设置日志级别为info；----根据两个地方的等级进行对比，取日志器的级别
console_handler.setLevel(level="WARNING")

# 第四步：设置控制台日志和文件日志的输出格式
console_fmt = "%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s--->%(lineno)d"
file_fmt = "%(lineno)d--->%(name)s--->%(levelname)s--->%(asctime)s--->%(message)s"

fmt1 = logging.Formatter(fmt = console_fmt)
fmt2 = logging.Formatter(fmt = file_fmt)

console_handler.setFormatter(fmt = fmt1)
file_handler.setFormatter(fmt = fmt2)

# 第五步：将控制台日志器、文件日志器，添加进日志器对象中
logger.addHandler(console_handler)
logger.addHandler(file_handler)


while(1):
    logger.debug("---debug")
    logger.info("---info")
    logger.warning("---warning")
    logger.error("---error")
    logger.critical("---critical")
    time.sleep(10)
