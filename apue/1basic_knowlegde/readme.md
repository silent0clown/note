# 1 UNIX基础知识
可将操作系统定义为一种软件，它可以控制计算机硬件资源，提供程序运行环境。这种软件被称为内核(kernel)，内核的接口被称为系统调用（system call）。

查看命令手册页：
```bash
man 1 ls
# or
man -s1 ls
```

进程ID是一个非负整数。getpid()获取进程ID

进程控制三个主要函数：
- fork
- exec
- waitpid

一个进程内的所有线程共享同一地址空间，文件描述符，栈以及与进程相关的属性。

# 出错处理
当UNIX系统函数出错时，通常会返回一个负值，而且整型变量errno通常被设置为具有特定信息的值。

Linux多线程的局部errno
```c
extern int* __errno_location(void);
#define errno (*__errno_location())
```