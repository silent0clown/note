# UNIX环境高级编程
《unix环境高级编程》中有很多示例代码需要包含作者自定义的头文件，如"apue.h"。这些代码可以从以下网址下载

http://apuebook.com/code3e.html

1. 解压文件
tar -zxvf src.3e.tar.gz

2. 安装libbsd-dev，否则编译会报错不通过，会提示编译threads文件夹里面的内容时报错

3. cd apue.3e
4. make
5. 用 root 用户或者 sudo 执行以下命令：
```bash
cp ./include/apue.h /usr/include/         

cp ./lib/libapue.a /usr/local/lib/ 
cp ./lib/libapue.a /usr/lib/
cp apue_err.h /usr/include/
```