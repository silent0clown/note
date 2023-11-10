// 同时输出数据到终端和文件的程序
// 等同于linux的tee程序
#include <assert.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>


/* 
 * FUCNTION NAME: ssize_t tee(int fd_in, int fd_out, size_t len, unsigned int flags);
 * FUNCTION WORK: 在两个管道文件描述符之间复制数据，零拷贝操作
 * RETURN       : 成功时返回在两个描述符之间复制的字节数，失败时-1
 */

int main(int argc, int *argv) {
    if(argc != 2) {
        printf("usage: %s <file>\n", argv[0]);
        return 1;
    }

    int filefd = open(argv[1], O_CREAT|O_WRONLY|O_TRUNC, 0666);
    assert(filefd > 0);
    int pipefd_stdout[2];
    int ret = pipe(pipefd_stdout);
    assert(ret != -1);

    int pipefd_file[2];
    int ret = pipe(pipefd_file);
    assert(ret != -1);

    /* 将标准输入内容输入管道Pipefd_stdout */
    ret = splice(STDIN_FILENO, NULL, pipefd_stdout[1], NULL, 32768, SPLICE_F_MORE | SPLICE_F_MOVE);
    assert(ret != -1);
    /* 将管道pipefd_stdout的输出复制到pipefd_file的输入端 */
    ret = tee(pipefd_stdout[0], pipefd_file[1], 32768, SPLICE_F_NONBLOCK);
    assert(ret != -1);

    /* 将管道pipefd_file的输出定向到文件描述符filefd上，从而将标准输入的内容写入文件 */
    ret = splice(pipefd_file[0], NULL, filefd, NULL, 32768, SPLICE_F_MORE | SPLICE_F_MOVE);
    assert(ret != -1);

    close(filefd);
    close(pipefd_stdout[0]);
    close(pipefd_stdout[1]);
    close(pipefd_file[0]);
    close(pipefd_file[1]);

    return 0;

    
}