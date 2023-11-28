# 8 进程控制
pid 0 调度进程（交换/系统进程），该进程是内核的一部分，不执行任何磁盘上的程序
pid 1 Init进程，属于用户进程，但是以超级用户特权运行。
pid 2 页守护进程，负责支持虚拟存储器系统的分页操作。

```c
#include<unistd.h>
pid_t getpid(void);
pid_t getppid(void);
pid_t getuid(void);
pid_t geteuid(void);
pid_t getgid(void);
pid_t getegid(void);

// 调用fork后，子进程返回0，父进程返回子进程的进程ID
// 子进程获得父进程数据、堆和栈的副本，并不共享这部分内容
pid_t fork(void);

```
## fork用法
- 父子进程同时执行不同的代码段。这在网络服务进程中是常见的。父进程等待客户端的服务请求，当请求到达时，父进程调用fork使子进程处理此请求，而父进程继续等待下一个服务请求。
- 父子进程执行不同的程序。这对shell是常见的情况。

```c
#include<sys/wait.h>


// 在一个子进程终止前，wait使其调用者阻塞，而waitpid可通过选项使调用者不阻塞。
// waitpid不等待在其调用后的第一个终止子进程，它通过选项控制所等待的进程。

// 如果子进程已经终止并且是个僵尸进程，则wait立即返回并取得该子进程的状态，否则wait使其调用者阻塞，知道一个子进程终止。
pid_t wait(int *statloc);

pid_t waitpid(pid_t pid, int *statloc, int options);
```

## 8.10 函数exec
当进程调用一致exec函数后，该进程执行的程序完全替换为新程序，而新程序则从其main函数开始执行。exec不改变线程ID，只是用磁盘上的一个新程序替换了当前进程的正文段、数据段、堆栈。

```c
#include<unistd.h>
int execl(const char *pathname, const char *arg0, ... /* (char *)0 */);
int execv(const char *pathname, char *const argv[]);
int execle(const char *pathname, const char *arg0, ... /* (char *)0, char *const envp[] */);


```