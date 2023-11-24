# 文件IO
不带缓冲的IO：不带缓冲指的是每个read和write都调用内核中的一个系统调用。
- open
- read
- write
- lseek
- close

```c
#include <fcntl.h>

int open(const char* path, int oflag, .../* mode_t mode */);

// 可以使用相对路径打开目录中的文件，可以让同一进程的多个线程在同一时间工作在不同的目录中
// 避免time_of_check_to_time_of_use错误。
// TOCTTOU: 如果有两个基于文件的函数调用，其中第二个调用依赖于第一个调用的结果，那么程序是脆弱的。
openat();

//等价于 open(path, O_WRONLY|O_CREAT|O_TRUNC, mode);
int creat(const char* path, mode_t mode);

int close(int fd);

// 改变已经打开文件的属性
int fcntl(inf fd, int cmd, .../* int arg */);
```
```c
#include<unistd.h>

// 如read成功，则返回读取的字节数，如已到达文件尾端，则返回0。
ssize_t read(int fd, void* buf, size_t nbytes);

ssize_t write(int fd, const void* buf, size_t nbytes);

ssize_t pread(int fd, void* buf, size_t nbytes, off_t offset);

ssize_t pwrite(int fd, const void *buf, size_t nbytes, off_t offset);

int dup(int fd);

int dup2(int fd, int fd2);

int fsync(int fd);

int fdatasync(int fd);

void sync(void);

int ioctl(int fd, int request, ...);
// flush 冲洗
```

```c
#include<sys/stat.h>
// 更改现有文件的访问权限
int chmod(const char *pathname, mode_t mode);
int fchmode(int fd, mode_t mode);
int fchmodat(int fd, const char *pathname, mode_t mode, int flag);
```