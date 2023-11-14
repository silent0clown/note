# 7、Linux服务器程序规范
- 服务器程序一般以后台形式运行，后台进程又称守护进程（daemon）
- Linux服务器程序通常有一套日志系统
- Linux服务器程序一般以某个专门的非root身份运行

---

# 8、高性能服务器程序框架
服务器结构为三个主要模块：
- I/O处理单元，4种I/O模型，两种高效时间处理模式
- 逻辑单元，两种高效并发模式，高效的逻辑处理模式——有限状态机
- 存储单元 

## 8.1 服务器模型
- C/S模型
- P2P模型

## 8.2 I/O模型
阻塞的概念：阻塞I/O执行的系统调用可能因为无法立即完成而被系统挂起，知道等待的事件发生为止。
4种模型：
- 阻塞I/O      程序阻塞于读写函数
- I/O复用      程序阻塞于I/O复用系统调用，但可同时监听多个I/O事件。对I/O本身的读写操作是非阻塞的。
- SIGIO信号    信号触发读写就绪事件，用户程序执行读写操作，程序没有阻塞阶段。
- 异步I/O      内核执行读写操作并触发读写完成事件。程序没有阻塞阶段。

## 8.3 两种高效的事件处理模式
- Reactor
    - 主线程只负责监听文件描述符上是否有事件发生，有的话就立即将该事件通知工作线程。除此之外主线程不做任何其他实质性的工作。
    - 使用同步I/O模型(epoll_wait)可以实现Reactor模式
- Proactor
    - 将所有I/O操作都交给主线程和内核来处理，工作线程仅仅负责业务逻辑。
    - 使用异步I/O模型(aio_read/aio_write)

## 8.4 两种高效的并发模式
如果程序是计算密集型的，并发编程并没有优势，反而由于任务的切换使效率降低。但如果程序是I/O密集型的，比如经常读写文件，访问数据库等，并发会极大提高性能。
- 半同步/半异步模式
    在I/O模型中，“同步”和“异步”区分的是内核向应用程序通知的是何种I/O事件以及该由谁来完成I/O读写（应用程序还是内核）。
    在并发模式中，“同步”指的是程序完全按照代码顺序执行，“异步”指程序的执行需要由系统事件来驱动。如中断、信号等。
    同步线程用于处理客户逻辑，异步线程用于处理I/O事件。

- 领导者/追随者模式
    多个工作线程轮流获得事件源集合，轮流监听、分发并处理事件。
    领导者/追随者模式包含如下几个组件
        - 句柄集， 表示I/O资源
        - 线程集， 所有工作线程的管理者
        - 事件处理器
        - 具体事务处理器

## 8.6 有限状态机

## 8.7 提高服务器性能的方式
- 池化，      内存池、进程池、线程池、连接池  
- 数据复制，   两个工作进程之间需要传递大量数据时，应该考虑使用共享内存而不是使用管道或者消息队列。
- 上下文切换， 线程的数量不大于CPU的数目
- 锁

# 9、I/O复用
I/O复用使得程序能同时监听多个文件描述符，本身是阻塞的。通常，网络程序在下列情况需要使用I/O复用：
- 客户端要同时处理多个socket，比如非阻塞connect；
- 客户端要同时处理用户输入和网络连接，比如聊天室程序；
- TCP服务器要同时处理监听socet和连接socket，这是I/O复用使用最多的场合；
- 服务器要同时处理TCP请求和UDP请求；
- 服务器要同时监听多个端口，或处理多种服务。
  
实现I/O复用的系统调用主要有poll, select, epoll

## 9.1
```c
// 用      途 ：在一段指定时间内，监听用户感兴趣的文件描述符上的可读、可写和异常等事件。
// 参      数 ：
/* 
 * nfds      : 指定被监听的文件描述符的总数
 * readfds   : 可读事件对应的文件描述符集合
 * writefds  : 可写事件
 * exceptfds : 异常事件
 * timeout   : 设置select函数的超时时间
*/
#include <sys/select.h>
int select(int nfds, fd_set* readfds, fd_set* writefds, fd_set* exceptfds, struct timeval* timeout);
```

在网络编程中，下列情况socket可读：
- sokcet内核接收缓存区中的字节数大于或等于其低水位标记SO_RCVLOWAT，此时可以无阻塞的读该socket
- sokcet通信的对方关闭连接
- 监听socket上有新的连接请求
- socket上有未处理的错误

下列情况socket可写：
- sokcet内核发送缓存区中的字节数大于或等于其低水位标记SO_SNDLOWAT，此时可以无阻塞的写该socket
- socket的写操作被关闭
- socket使用非阻塞connect连接成功或者失败（超时）之后
- socket上有未处理的错误
  

## 9.2 poll调用
poll和select类似，也是在指定时间内轮询一定数量的文件描述符，以测试其中是否有就绪者。
```c

#include <poll.h>
int poll(struct pollfd* fds, nfds_t nfds, int timeout);

struct pollfd {
    int fd;       // 文件描述符
    short events; // 注册的事件
    short revents; // 实际发生的事件，由内核填充
};
```
## 9.3 epoll系列系统调用

# 10 信号

# 13 多进程编程
Linux下创建新进程的系统调用是fork
```c
#include <sys/types.h>
#include <unistd.h>
pid_t fork(void);
```
该函数调用都返回两次，在父进程中返回的是子进程的PID，在子进程中则返回0。失败时返回-1。

如果在程序中分配了大量内存，使用fork时应当谨慎，尽量避免没必要的内存分配和数据复制。

僵尸状态：在子进程结束运行之后，父进程读取其退出状态之前，撑该子进程处于僵尸态。父进程结束或者异常终止，而子进程继续运行。也为僵尸态。

## 13.3 处理僵尸线程
```c
#include <sys/types.h>
#include <wait.h>

pid_t wait(int* stat_loc);   // 阻塞进程，直到进程的某个子进程结束运行为止。返回结束运行的子进程的PID

pid_t waitpid(pid_t pid, int* stat_loc, int options);   // 等待Pid参数指定的子进程
```

## 13.4 管道
socketpair

## 13.5 信号量
PV操作
Linux信号量的API都定义在sys/sem.h中，主要包含三个系统调用：
- semget  创建或者获取一个信号量集
- semop   改变信号量的值，即进行P,V操作 
- semctl  对信号量进行直接控制

## 13.6 共享内存
共享内存的API定义在sys/shm.h中，包括4个系统调用：
- shmget      创建一段新的共享内存，或者获取一段已经存在的共享内存
- shmat
- shmdt
- shmctl      系统调用控制共享内存

## 13.7 消息队列
消息队列是在两个进程之间传递二进制块数据的一种见到有效的方式。
Linux消息队列的API定义在sys/msg.h中，包括4个系统调用：
- msgget       创建或则获取一个消息队列
- msgsnd
- msgrcv
- msgctl
```c
#include <sys/msg.h>

/* 作    用 * 创建一个消息队列，或者获取一个已有的消息队列
 * key      * key参数是一个键值，用来标识一个全局唯一的消息队列
 * msgflg   * 
 * return   * 成功时返回一个正整数值，是消息队列的标识符。失败时返回-1并设置errno
 * 如果msgget用于创建消息队列，则与之关联的内核数据结构msqid_ds将被创建并初始化
*/
int msgget(key_t key, int msgflg);


/* 作     用 * 把一条消息添加到消息队列中
 * msqid     * 由msgget返回的消息队列标识符
 * msg_ptr   * 指向一个准备发送的消息
 * msgflg    * 控制msgsnd的行为，通常仅支持IPC_NOWAIT标志，即以非阻塞的方式发送消息，如果消息队列满了，则msgsnd将阻塞
*/
int msgsnd(int msqid, const void* msg_ptr, size_t msg_sz, int msgflg);

/* function  * 从消息队列中获取消息
 * msqid     * msgget调用返回的消息队列标识符
 * msg_ptr   * 存储接收的消息
 * msg_sz    * 消息数据部分的长度
 * msgtype   * 指定接收何种类型的消息     msgtype == 0 读取消息队列中第一个消息; > 0 读取消息队列中第一个类型为msgtype的消息;  <0 读取消息队列中第一个类型值比msgtype的绝对值小的消息
 * msgflg    * 控制msgrcv函数的行为 IPC_NOWAIT  MSG_EXCEPT  MSG_NOERROR
 * return    * success 0, fail -1; 成功时将msqid_ds字段num减一
*/
int msgrcv(int msqid, void* msg_ptr, size_t msg_sz, long int msgtype, int msgflg);

/* funciton  * 控制消息队列的某些属性
 * msqid     *
 * command   * 指定要执行的命令 IPC_STAT 将消息队列的内核数据结构复制到buf中；IPC_SET，IPC_RMID, IPC_INFO, MSG_INFO, MSG_STAT
*/
int msgctl(int msqid, int cmmand, struct msqid_ds* buf)
```
---

# 14 多线程编程
NPTL(Native POSIX Thread Library)
线程的实现模式：
- 完全在用户空间实现， 内核线程 = 1
- 完全由内核调度，     
- 双层调度， 核调度M个内核线程，线程库调度N个用户线程。这种方式不会消耗过多的内核资源，而且线程切换速度也较快。同时可以充分利用多核处理器的优势。

## 14.2 API接口
```c
#include <pthread.h>
/*
 * Function    * 创建一个线程
 * thread      * 新线程的标识符
 * attr        * 设置新线程的属性，默认使用NULL
 * start_routine * 指定新线程将运行的函数
 * arg           * 新线程运行函数的参数
 * Return        * success :0 ; fail : errorcode
 * 一个用户可以打开的线程数量不能超过RLIMIT_NPROC软资源限制
 * 系统上所有用户能创建的线程总数也不能超过/proc/sys/kernel/threads-max
 */
int pthread_create(pthread_t* thread, const pthread_attr_t* attr, void*(*start_routine)(void* ), void* arg);

/* 线程函数在结束时最好调用退出函数，以确保安全、干净的退出 */
void pthread_exit(void* retval);

/* 调用pthread_join可使线程等待其他线程结束 */
/* thread   * 目标线程标识符
 * retval   * 目标线程返回的退出信息
 * Return   * Success : 0; fail : error code;   EDEADLK 死锁， EINVAL 目标线程不可回收或已有其他线程在回收该目标线程；   ESRCH 目标线程不存在
*/
int pthread_join(pthread_t thread, void** retval);

/* 异常终止一个线程
 */
pthread_cancel(pthread_t thread);


```

## 14.3 线程属性
- detachstate   线程的脱离状态
- stackaddr和stacksize    线程堆栈的起始地址和大小
- guardsize 保护区域大小
- schedparam 线程调度参数
- scheedpolicy 线程调度策略
- inheritsched 是否继承调用线程的调度属性
- scpoe 线程间竞争CPU的范围

## 14.4 POSIX信号量
```c
#include<semaphore.h>

// 以下函数成功时返回0 ，失败时返回-1，并设置errno

/* 初始化一个未命名的信号量 */
/* pshared   * 指定信号量的类型，如果为0，则表示这个信号量是当前进程的局部信号量，否则就可以在多个进程之间共享 
 * value     * 指定信号量的初始值
*/
int sem_init(sem_t* sem, int pshared, unsigned int value);

/* 
 * 销毁信号量
 */
int sem_destroy(sem_t* sem);

/* 以原子操作方式将信号量的值减一 */
int sem_wait(sem_t* sem);

/* 与sem_wait相似，不过它始终立即返回 */
int sem_trywait(sem_t* sem);


/* 以原子操作方式将信号量的值加一 */
int sem_post(sem_t* sem);
```

## 14.5 互斥锁
主要API
```c
#include<pthread.h>

// 初始化互斥锁， mutexattr为互斥锁的属性，默认为NULL
int pthread_mutex_init(pthread_mutex_t* mutex, const pthread_mutexattr_t* mutexattr);

// 销毁互斥锁，释放其占用的内核资源
int pthread_mutex_destroy(pthread_mutex_t* mutex);

// 以原子操作的方式给一个互斥锁加锁。如果目标互斥锁已经被加锁，调用Lock将导致阻塞，知道该互斥锁的占有者将其解锁
int pthread_mutex_lock(pthread_mutex_t* mutex);

// pthread_mutex_lock的非阻塞版
int pthread_mutex_trylock(pthread_mutex_t* mutex);

// 解锁
int pthread_mutex_unlock(pthread_mutex_t* mutex);
```
互斥锁有两种常用属性
- pshared，指定是欧服允许跨进程共享互斥锁，PTHREAD_PROCESS_SHARED可以被跨进程共享；PTHREAD_PROCESS_PRIVATE只能被和锁的初始化线程隶属于同一个进程的线程共享。
- type，指定互斥锁的类型，有4中类型
    - PTHREAD_MUTEX_NORMAL，普通锁，默认类型。一个线程如果对一个已经加锁的普通锁再次加锁，将引发死锁。对一个被其他线程加锁的普通锁解锁或对一个已经解锁的普通锁再次解锁，将导致不可预期的后果。
    - PTHREAD_MUTEX_ERRORCHECK，检错锁。一个线程如果对已经加锁的检错锁再次加锁，则加锁操作返回EDEADLK。对一个已经被其他线程加锁的检错锁解锁，或者对一个已经解锁的检错锁再次解锁，则解锁操作返回EPERM。
    - PTHREAD_MUTEX_RECURSIVE，嵌套锁。允许一个线程在释放锁之前多次对它加锁而不发生死锁。不过其他线程如果要获得这个锁，则当前锁的拥有者必须执行相应次数的解锁操作。对一个已经被其他线程加锁的嵌套锁加锁，或对一个已经解锁的嵌套锁再次解锁，则解锁操作返回EPERM。
    - PTHREAD_MUTEX_DEFAULT，默认锁。一个线程如果对一个已经加锁的默认锁再次加锁，或对一个已经被其他线程加锁的默认锁解锁，或对一个已经解锁的默认锁再次解锁，将导致不可预期的后果。

### 死锁
- 对一个已经加锁的普通锁再次加锁
- 两个线程按照不同的顺序来申请互斥锁。如主线程按照a，b顺序申请锁，子线程按照b,a顺序申请锁。则可能主线程拥有a,子线程拥有b。两个线程都在等另一个锁，造成死锁。

## 14.6 条件变量
互斥锁是用于同步线程对共享数据的访问，条件变量则是用于在线程之间同步共享数据的值。

条件变量提供了一种线程间的通知机制：当某个共享数据达到某个值的时候，唤醒等待这个共享数据的线程。

条件变量的API
```c

/* 初始化条件变量
 * cond       * 要操作的目标条件变量
 * cond_attr  * 指定条件变量的属性，默认使用NULL，属性和互斥锁相似
*/
int pthread_cond_init(pthread_cond_t* cond, const pthread_condattr_t* cond_attr);

/* 销毁 */
int pthread_cond_destroy(pthread_cond_t* cond);

/* 以广播方式唤醒所有等待目标条件变量的线程 */
int pthread_cond_broadcast(pthread_cond_t* cond);

/* 唤醒一个等待目标条件变量的线程 */
int pthread_cond_signal(pthread_cond_t* cond);

/* 等待目标条件变量，mutex是用于保护条件变量的互斥锁，在调用Pthread_cond_wait前，必须给Mutx加锁 */
int pthread_cond_wait(pthread_cond_t* cond, pthread_mutex_t* mutex);

```

# 15 进程池和线程池
线程池中的线程数应该和CPU数量差不多

# 16 调试
多线程调试 
- info threads， 显示所有线程
- thread ID， 调试目标ID指定的线程
- set scheduler-locking[off|on|step]

# 17 系统监测工具
tcpdump
- n ，使用IP地址表示主机，而不是主机名；使用数字表示端口号，而不是服务名称



