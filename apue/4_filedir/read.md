# 4 文件和目录
```c
#include <sys/stat.h>
int stat(const char *restrict pathname, struct stat *restrict buf);

int fstat(int fd, struct stat *buf);

int lstat(const char *restrict pathname, struct stat *restrict buf);

itn fstatat(int fd, const char *restrict pathname, struct stat *restrict buf, int flag);
```
## 文件类型
1. 普通文件
2. 目录文件
3. 块特殊文件，   提供对设别（如磁盘）带缓冲的访问，每次访问以固定长度为单位进行。
4. 字符特殊文件， 提供对设备不带缓冲的访问，每次访问长度可变。
5. FIFO,         进程间通信
6. 套接字
7. 符号链接

## 文件访问权限
- S_IRUSR   用户读
- S_IWUSR   用户写
- S_IXUSR   用户执行
- S_IRGRP   组读
- S_IWGRP   组写
- S_IXGRP   组执行
- S_IROTH   其他读
- S_IWOTH   其他写
- S_IXOTH   其他执行

```c
#include <unistd.h>
int access(const char *pathname, int mode);
int faccessat(int fd, const char *pathname, int mode, int flag);
```