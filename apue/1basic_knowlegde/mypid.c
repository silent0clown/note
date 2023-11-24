#include "apue.h"
#include "apue_err.h"

int main(void) {
    printf("hello from process ID %ld", (long)getpid());
    exit(0);
}