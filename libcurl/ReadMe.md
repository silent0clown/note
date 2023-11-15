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
11. CURLINFO_CONTENT_LENGTH_DOWNLOAD 使用该选项时要求传递一个 double 型指针到函数中，该 double 型变量用来存放所要下载文件(或者是所要查询的文件)的 content-length (文档长度) 的信息。如果文件大小无法获取，那么函数返回值为 -1 

# 手把手实现多线程下载以及断点续传
1. download第三方库选择
2. curl与自实现http请求
3. mmap共享内存的使用
4. wmem/rmem的优化
5. 多线程下载httphdr的range使用
6. 断点续传实现
7. md5与sha256校验值


# 编译
需提前安装curl库

```bash
gcc main.c -o proc_main libcurl
```