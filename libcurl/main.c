#include <stdio.h>
#include <curl/curl.h>
#include <fcntl.h>

typedef struct _fileInfo
{
    char* fileptr;
    int   offset;
}fileInfo;


size_t writeFunc(void *ptr, size_t size, size_t memb, void *userdata) {
    printf("writeFunc...\n");
    fileInfo* info = (fileInfo *)userdata;

    memcpy(info->fileptr + info->offset, ptr, size * memb);
    info->offset += size * memb;

    return size * memb;
}

double getDownloadFileLength(const char* url) {
    double downloadFileLength = 0;
    CURL* curl = curl_easy_init();

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HEADER, 1);
    curl_easy_setopt(curl, CURLOPT_NOBODY, 1);

    CURLcode res = curl_easy_perform(curl);
    if(res == CURLE_OK) {
        printf("downloadFileLength Success\n");
        curl_get_info(curl, CURLINFO_CONTENT_LENGTH_DOWNLOAD, &downloadFileLength);
    }
    else {
        printf("downloadFileLength Fail\n");
        downloadFileLength = -1;
    }
    curl_easy_cleanup(curl);

    return downloadFileLength;
}

int download(const char* url, const char* filename) {
    long fileLength = getDownloadFileLength(url);
    printf("downloadFileLength: %ld\n", fileLength);

    // write
    int fd = open(filename, O_RDWR | O_CREAT, S_IRUER | S_IWUSER);
    if(fd == -1) {
        printf("open file fail\n");
        return -1;
    }

    if(-1 == lseek(fd, fileLength - 1, SEEK_SET)) {
        perror("lseek");
        close(fd);
        return -1;
    }

    fileInfo *info = (fileInfo* )malloc(sizeof(fileInfo));
    if(info == NULL) {
        printf("malloc fail\n");
        munmap(ptr, fileLength);
        close(fd);
        return -1;
    }
    info->fileptr = fileptr;
    info->offset  = 0;

    CURL* curl = curl_easy_init();

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeFunc);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, info);  

    CURLcode res = curl_easy_perform(curl);  
    if(res != CURLE_OK) {
        printf("res %d\n", res);
    }
    curl_easy_cleanup(curl);      // disconnect
    munmap(ptr, fileLength);
    close(fd);

    return 0;   
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
    // curl_download(url, filename);
    download(url, filename);
}