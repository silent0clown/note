# 10 线程
线程的好处：
- 通过Wie每种事件类型分配单独的处理线程，可以简化处理异步事件的代码。每个线程在进行事件处理时可以采用同步编程模式，同步编程模式要比异步编程模式简单。
- 多线程可以共享内存和文件描述符
- 有些问题分解为多线程处理可以提高整个程序吞吐量。
- 交互的程序同样可以通过使用多线程来改善响应时间。

POSIX线程的功能测试宏是`_POSIX_THREADS`，在编译时确定是否支持线程。

线程创建时并不能保证哪个线程会先运行。

## 11.6.1 互斥量（mutex）
可以使用互斥量保护数据，确保同一时间只有一个线程访问数据

如果线程试图对同一个互斥量加锁两次，那么他自身就会陷入死锁状态。

互锁也会造成死锁。

## 11.6.4 读写锁（rwlock）
一次只有一个线程可以占有写模式的读写锁，但是多个线程可以同时占用读模式的读写锁

## 11.6.6 条件变量
条件变量是线程可用的另一种同步机制。条件变量与互斥量一起使用时，允许线程以无竞争的方式等待特定的条件发生。

## 11.6.7 自旋锁
自旋锁与互斥量类似，但它不是通过休眠使进程阻塞，儿时在获取锁之前一直处于忙等阻塞状态。

应用场景：锁被持有的时间短，而且线程不希望在重新调度上花费太多的成本。
在内核中中断处理程序使用自旋锁，在用户层不是非常有用。

```c
#include <pthread.h>
/* 线程创建
 * tidp      : 新创建线程的线程ID
 * attr      : 线程属性
 * start_rtn : 新创建的线程运行的函数
 * arg       : 线程运行函数的入参，只有一个，若要传递多个参数，用结构体
*/
int pthread_create(pthread_t *restrict tidp, const pthread_attr_t *restrict attr,
                    void *(*start_rtn)(void *), void *restrict arg);

/* 终止单个线程 */
void pthread_exit(void *rval_ptr);

/* 阻塞调用线程，直接接收到指定thread线程的返回值 */
void pthread_join(pthread_t thread, void **rval_ptr);

/* 请求取消同一进程中的其他线程 */
int pthread_cancel(pthread_t tid);

/* 线程清理处理程序 */
void pthread_cleanup_push(void (*rtn)(void *), void *arg);

void pthread_cleanup_pop(int execute);

/* 互斥量使用前需要初始化 */
int pthread_mutex_init(pthread_mutex_t *restrict mutex,
                       const pthread_mutexatter_t *restrict attr);

/* 动态分配互斥量，在释放内存前需要调用destroy */
int pthread_mutex_destroy(pthread_mutex_t *mutex);       

/* 加锁 */
int pthread_mutex_lock(pthread_mutex_t *mutex);

/* 如果线程不希望阻塞，可以使用pthread_mutex_trylock尝试对互斥量进行加锁 */
/* 如果互斥量处于未锁住状态，trylock就会加锁，否则trylock就会失败，返回EBUSY */
int pthread_mutex_trylock(pthread_mutex_t *mutex);

int pthread_mutex_unlock(pthread_mutex_t *mutex);

/* 在tsptr时间内上锁，若失败，则返回错误编号 */
int pthread_mutex_timedlock(pthread_mutex_t *restrict mutex,
                            const struct timespce *restrict tsptr);

int pthread_rwlock_init(pthread_rwlock_t *restrict rwlock,          
                        const pthread_rwlockattr_t *attr);

int pthread_rwlock_destroy(pthread_rwlock_t *rwlock);


// 读锁
int pthread_rwlock_rdlock(pthread_rwlock_t *rwlock);

int pthread_rwlock_tryrdlock(pthread_rwlock_t *rwlock);

// 写锁
int pthread_rwlock_wrlock(pthread_rwlock_t *rwlock);

int pthread_rwlock_trywrlock(pthread_rwlock_t *rwlock);

// 解锁
int pthread_rwlock_unlock(pthread_rwlock_t *rwlock);

/* 初始化条件变量 */
int pthread_cond_init(pthread_cond_t *restrict cond,
                      const pthread_condattr_t *restrict attr);

int pthread_cond_destroy(pthread_cond_t *cond);     

/* 等待条件变量变为真 */
int pthread_cond_wait(pthread_cond_t *restrict cond,
                      pthread_mutex *restrict mutex);

int pthread_cond_timewait(pthread_cond_t *restrict cond,
                          pthread_mutex_t *restrict mutex,
                          const struct timespec *restrict tspter);

// 初始化自旋锁
int pthread_spin_init(pthread_spinlock_t *lock, int pshared);

int pthread_spin_destroy(pthread_spinlock_t *lock);

int pthread_spin_lock(pthread_spinlock_t *lock);

int pthread_spin_trylock(pthread_spinlock_t *lock);

int pthread_spin_unlock(pthread_spinlock_t *lock);
```
