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

# libcurl API
```c
// 初始化句柄
curl_easy_init()

// 设置参数，必须设置CURLOPT_URL参数项
curl_easy_setopt()

// 清空一个curl句柄的所有设置
curl_easy_reset()

// 克隆一个curl句柄及其所有设置
curl_easy_duphandle()

// 参数设置完毕后，开始执行操作，知道操作完成或失败才返回
curl_easy_perform()

// perform之后，获取传输的信息
curl_easy_getinfo()

// 完成传输后清除curl句柄
curl_easy_cleanup()
```

# [OPTION](https://curl.se/libcurl/c/curl_easy_setopt.html)
1. CURLOPT_VERBOSE
2. CURLOPT_HEADER
3. CURLOPT_NOPROGRESS
4. CURLOPT_NOSIGNAL
5. CURLOPT_WILDCARDMATCH    // 多模匹配传输文件，仅支持FTP下载
6. **[CURLOPT_WRITEFUNCTION](https://curl.se/libcurl/c/CURLOPT_WRITEFUNCTION.html)**，用于下载保存内容
7. CURLOPT_WRITEDATA
8. **[CURLOPT_READFUNCTION](https://curl.se/libcurl/c/CURLOPT_READFUNCTION.html)**，用于上传文件
9. **[CURLOPT_URL](https://curl.se/libcurl/c/CURLOPT_URL.html)**
10. CURLOPT_PROXY