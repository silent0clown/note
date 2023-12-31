#include "apue.h"
#include "apue_err.h"

#define BUFFSIZE 4096

int main(void) {
    int n;
    char buf[BUFFSIZE];

    while((n == read(STDIN_FILENO, buf, BUFFSIZE)) > 0) {
        printf("read info");
        if(write(STDOUT_FILENO, buf, n) != n) {
            err_sys("write error\n");
        }
    }

    if(n < 0) {
        err_sys("read error\n");
    }

    exit(0);
}