#if !defined(THREAD_POOL_H)
#define THREAD_POOL_H

#ifdef __cplusplus
extern "C"{
#endif



// 任务队列结构体
typedef struct _thread_task
{
    void (*function)(void* arg);
    void* arg; 
}ThreadTask_t;


// 线程池结构体 
typedef struct _thread_pool
{
    ThreadTask_t* taskQ;         // 任务队列
    int queueCapacity;          // 队列能容纳最大任务数

    // 任务队列信息
    int queueSize;              // 当前任务个数
    int queueFront;             // 队头 -> 取数据
    int queueRear;              // 队尾 -> 放数据

    // 线程池管理
    pthread_t managerID;        // 管理者线程ID
    pthread_t *threadIDs;       // 工作的线程ID
    pthread_mutex_t mutexPool;  // 锁整个的线程池，任务队列
    pthread_mutex_t mutexBusy;  // 锁BusyNum
    pthread_cond_t  notFull;    // 任务队列是不是满了
    pthread_cond_t  notEmpty;   // 任务队列是不是空了

    // 线程池信息
    int minNum;                 // 最小工作线程个数
    int maxNum;                 // 最大工作线程个数
    int busyNum;                // 忙碌线程数
    int liveNum;                // 存活的线程数
    int exitNum;                // 要销毁的线程个数

    // 线程池状态
    int shutdown;               // 是否要销毁线程池，1销毁，0不销毁。
}ThreadPool_t;


// 创建线程池并初始化
ThreadPool_t* threadPoolCreate(int queueCapacity, int minNum, int maxNum);



// 销毁线程池

// 给线程池添加任务

// 获取线程池中工作的线程的个数

// 获取线程池中活着的线程的个数


// 创建工作线程






#ifdef __cplusplus 
}
#endif

#endif // THREAD_POOL_H

