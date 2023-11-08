# 1、下载安装libcurl
```bash
git clone https://github.com/curl/curl.git
tar -zxvf curl.8.4
cd curl.8.4
./configure --prefix=/usr/local/curl --with-openssl
make
make install
```
# 2、编译test_libcurl.c
```bash
gcc test_libcurl.c -o proc_test -I /usr/local/curl/include/ -L /usr/local/curl/lib/ -lcurl
```

# libcurl是下载http的三方库

[HOW TO USE](https://curl.se/docs/manpage.html)

[HOW TO INSTALL CURL AND LIBCURL](https://curl.se/docs/install.html)