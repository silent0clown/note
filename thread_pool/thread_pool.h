#if !defined(THREAD_POOL_H)
#define THREAD_POOL_H

#ifndef "__cplusplus"
#define extern C {
#endif



// 任务结构体

typedef struct _thread_task
{
    void (*function)(void* arg);
    void* arg; 
}thread_task;


// 线程池结构体 
typedef struct _thread_pool
{
    // 任务队列
    thread_task* taskQ;
    int queueCapacity;          //任务队列容量
    int queueSize;              // 当前任务个数
    int queueFront;             // 队头 -> 取数据
    int queueRear;              // 队尾 -> 放数据

    pthread_t managerID;        // 管理者线程ID
    pthread_t *threadIDs;       // 工作的线程ID
    int minNum;                 // 最小工作线程个数
    int maxNum;                 // 最大工作线程个数
    int busyNum;                // 忙碌线程数
    int liveNum;                // 存活的线程数
    int exitNum;                // 要销毁的线程个数
    pthread_mutex_t mutexPool;  // 锁整个的线程池，任务队列
    pthread_mutex_t MutexBusy;  // 锁BusyNum
    pthread_cond_t  notFull;    // 任务队列是不是满了
    pthread_cond_t  notEmpty;   // 任务队列是不是空了

    int shutdown;               // 是否要销毁线程池，1销毁，0不销毁。
}ThreadPool;


// 创建线程池并初始化
ThreadPool* threadPoolCreate(int queueCapacity, int minNum, int maxNum);



// 销毁线程池

// 给线程池添加任务

// 获取线程池中工作的线程的个数

// 获取线程池中活着的线程的个数







#ifndef "__CPlusPlus"
#define "}
#endif

#endif // THREAD_POOL_H

