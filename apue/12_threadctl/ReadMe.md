# 12 线程控制
## 12.4 同步属性
1. 互斥量属性 pthread_mutexattr_t
   1. 进程共享属性， _SC_THREAD_PROCESS_SHARED查看
   2. 健壮属性
   3. 类型属性
   
```c
#include<pthread.h>
// 设置互斥量的属性
int pthread_mutexattr_init(pthread_mutexattr_t *attr);
// 反初始化互斥量属性
int pthread_mutexattr_destroy(pthread_mutexattr_t *attr);

// 查询attr的进程共享属性
int pthread_mutexattr_getpshared(const pthread_mutexattr_t *restrict attr, 
                                int *restrict pshared);
//修改attr的进程共享属性
int pthread_mutexattr_setpshared(const pthread_mutexattr_t *restrict attr, 

// 获取健壮的互斥量属性的值
int pthread_mutexattr_getrobust(const pthread_mutexattr_t *restrict attr, 
                                int *restrict robust);
// 设置健壮的互斥量属性的值
int pthread_mutexattr_setrobust(const pthread_mutexattr_t *restrict attr, 
                                int *restrict robust);


```