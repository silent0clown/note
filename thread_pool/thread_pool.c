#include "thread_pool.h"
#include <stdio.h>
#include <string.h>

/* 
 * 线程池的原理 ： 如果并发的线程数较多，每个线程执行一段时间就结束，频繁创建线程就会大大降低系统的效率
 *                线程池的原理就是线程复用，是一种多线程处理形式，处理过程中将任务添加到队列，然后再创建线程后
 *                自动启动这些任务。线程池都是后台线程。每个线程都使用默认的堆栈大小，已默认的优先级运行，并处于
 *                多线程单元中。如果某个线程在托管代码中空闲（如正在等待某个事件），则线程池将插入另一个辅助线程
 *                来使所有处理器保持繁忙。如果所有线程池线程都始终保持繁忙，但队列中包含挂起的工作，则线程池将在
 *                一段时间后创建另一个辅助线程，但线程的数目永远不会超过最大值。超过最大值的线程可以排队，但他们
 *                要等到其他线程活动完成后才启动。
 *
 * 实现原理：  组成分为3个部分，这三个部分配合工作就可以得到一个完整的线程池：
 *           1. 任务队列， 存储需要处理的任务，由工作的线程来处理这些任务
 *              - 通过线程池提供的API函数，将一个待处理的任务添加到任务队列，任务就是待执行的回调函数
 *              - 已处理的任务会被从任务队列中删除
 *              - 线程池的使用者，也就是调用线程池函数往任务队列中添加任务的线程就是生产者线程。
 *           2. 工作的线程（任务队列中任务的消费者） N个
 *              - 线程池中维护了一定数量的工作线程，他们的作用是不停的读任务队列，从里面取出任务并处理
 *              - 工作的线程相当于是任务队列的消费者角色。
 *              - 如果任务队列为空，工作的线程将会被阻塞（使用条件变量/信号量阻塞）
 *              - 如果阻塞之后有了新的任务，由生产者将阻塞解除，工作线程开始工作
 *           3. 管理者线程（不处理任务队列中的任务），1个
 *              - 他的任务是周期性的对任务队列中的任务数量以及处于忙状态的工作线程个数进行检测
 *              - 当任务过多的时候，可以适当地创建一些新的工作线程
 *              - 当任务过少的时候，可以适当地销毁一些工作的线程
 *  */ 


ThreadPool* threadPoolCreate(int queueCapacity, int minNum, int maxNum){
    ThreadPool* pool = (ThreadPool*)malloc(sizeof(ThreadPool));
    if(pool == NULL){
        printf("malloc threadpool fail....\n");
        goto failure;
    }

    pool->threadIDs = (pthread_t*)malloc(sizeof(pthread_t) * maxNum);
    if(pool->threadIDs == NULL){
        printf("malloc threadIDs fail...\n");
        goto failure;
    }
    memset(pool->threadIDs, 0, sizeof(pthread_t)*maxNum);
    pool->minNum = minNum;
    pool->maxNum = maxNum;
    pool->busyNum = 0;
    pool->liveNum = minNum;      // 和最小线程数相等
    pool->exitNum = 0;

    if(pthread_mutex_init(&pool->mutexPool, NULL) != 0 ||
       pthread_mutex_init(&pool->mutexBusy, NULL) != 0 ||
       pthread_mutex_init(&pool->notEmpty, NULL) != 0 ||
       pthread_mutex_init(&pool->notFull, NULL) != 0) 
    {
        printf("mutex or condition init fail...\n");
        
        return 0;
    }

    // 任务队列
    pool->taskQ = malloc(sizeof(thread_task) * queueCapacity);
    if(pool->taskQ == NULL)
    {
        printf("malloc task fail...\n");
        goto failure;
    }
    pool->queueCapacity = queueCapacity;
    pool->queueSize = 0;
    pool->queueFront = 0;
    pool->queueRear  = 0;

    pool->shutdown  = 0;

    // 创建线程
    pthread_create(&pool->managerID, NULL, manager, NULL);
    for(int i = 0; i < minNum; i++)
    {
        pthread_create(&pool->threadIDs[i], NULL, worker, NULL);
    }

    return pool;


failure:
if(pool->threadIDs) free(pool->threadIDs);
if(pool->taskQ) free(pool->taskQ);
if(pool) free(pool);
return NULL;
}