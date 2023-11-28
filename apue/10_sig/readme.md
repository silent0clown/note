# 10 信号
信号是软件中断。提供了一种处理异步事件的方法。

在头文件<signal.h>中，信号名都被定义为正整数常量。

- SIGABRT  异常终止（abort）
- SIGALRM  定时器超时（alarm）
- SIGBUS   硬件故障
- SIGCANCEL  线程库内部使用
- SIGCHLD    子进程状态改变
- SIGCONT    使暂停进程继续
- SIGEMT     硬件故障
- SIGFPE     算术异常
- SIGFREEZE  检查点冻结
- SIGHUP     连接断开
- SIGILL     非法硬件指令
- SIGINFO    键盘状态请求
- SIGINT     终端中断符
- SIGIO      异步I/O
- SIGIOT     硬件故障
- SIGJVM1    Java虚拟机内部使用
- SIGJVM2    Java虚拟机内部使用
- SIGKILL    终止
- SIGLOST    资源丢失
- SIGLWP     线程库内部使用
- SIGPIPE    写至无读进程的管道
- SIGPOLL    可轮询事件
- SIGPROF    梗概时间超时
- SIGQUIT    终端退出符
- SIGSEGV    无效内存引用
- SIGSTKFLT  协处理器栈故障
- SIGSTOP    停止
- SIGTHAW    检查点解冻
- SIGTHR     线程库内部使用
- SIGTRAP    硬件故障
- SIGTSTP    终端停止符
- SIGTTIN    后台读控制tty
- SIGTTOU    后台写向控制tty
- SIGURG     紧急情况（套接字）
- SIGUSR1    用户自定义信号
- SIGUSR2    用户自定义信号
- SIGVTALRM  虚拟时间闹钟
- SIGWAITING 线程库内部使用
- SIGWINCH   终端窗口大小改变
- SIGXCPU    超过CPU限制
- SIGXFSZ    超过文件长度限制
- SIGXRES    超过资源控制 