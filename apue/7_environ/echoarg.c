#include "apue.h"
#include "apue_err.h"

int main(int argc, char *argv[]) {
    int i;
    // for (i = 0; i < argc; i++)
    for (i = 0; argv[i] != NULL; i++)
        printf("argv[%d]: %s\n", i, argv[i]);
    exit(0);
}