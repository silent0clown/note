#include <stdio.h>
#include <curl/curl.h>

size_t writeFunc(void *ptr, size_t size, size_t memb, void *userdata) {
    printf("writeFunc...\n");
}

/* * url      : download url
   # filename : download file to save path
*/
int curl_download(const char *url, const char *filename) {
    CURL *curl = curl_easy_init();    // init
    curl_easy_setopt(curl, CURLOPT_URL, url);  // connect
    curl_easy_setopt(curl,CURLOPT_HEADER, 1L);
    curl_easy_setopt(curl,CURLOPT_VERBOSE, 1L);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeFunc);   // downdload callback

    CURLcode res = curl_easy_perform(curl);         // process
    if(res != CURLM_OK) {
        printf("res %d\n", res);
    }
    curl_easy_cleanup(curl);      // disconnect

    return 0;
}

// int main(int argc, char *argv[]) {
//     curl_download(argv[1], argv[2]);
int main() {
    char *url = "www.baidu.com";
    char *filename = "./test.html";
    curl_download(url, filename);
}