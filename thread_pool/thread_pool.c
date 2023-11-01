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


ThreadPool_t* threadPoolCreate(int queueCapacity, int minNum, int maxNum){
    ThreadPool_t* pool = (ThreadPool_t*)malloc(sizeof(ThreadPool_t));
    // 替换goto的方法，一般使用do...while(0)
    if(pool == NULL){
        printf("malloc threadpool fail....\n");
        goto failure;
    }

    // 给工作线程数组申请内存
    pool->threadIDs = (pthread_t* )malloc(sizeof(pthread_t) * maxNum);
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
       pthread_cond_init(&pool->notEmpty, NULL) != 0 ||
       pthread_cond_init(&pool->notFull, NULL) != 0) 
    {
        printf("mutex or condition init fail...\n");
        
        goto failure;
    }

    // 任务队列
    pool->taskQ = malloc(sizeof(ThreadTask_t) * queueCapacity);
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

// 工作线程
void* ThreadPoolTaskThread(void* threadpool)
{
    ThreadPool_t* pool = (ThreadPool_t* )threadpool;
    ThreadTask_t  task;

    while(1)
    {
        pthread_mutex_lock(&pool->mutexPool);

        /* 无任务阻塞在“任务队列不为空”上，有任务则跳出 */
        while((pool->queueSize == 0) && !(pool->shutdown))
        {
            printf("thread 0x%x is waiting \n", (unsigned int)pthread_self());
            pthread_cond_wait(&(pool->notEmpty), &(pool->mutexPool));
        
            /* 判断是否需要清除线程，自杀功能 */
            if(pool->exitNum > 0)
            {
                pool->exitNum--;
            }

            /* 判断线程池中的线程数是否大于最小线程数，是则结束当前线程 */
            if(pool->liveNum > pool->minNum)
            {
                printf("thread 0x%x is exiting \n", (unsigned int)pthread_self());
                pool->liveNum--;
                pthread_mutex_unlock(&(pool->mutexPool));
                pthread_exit(NULL); // 结束线程
            }
        }


        /* 线程池开关状态 */
        if(pool->shutdown)    // 销毁线程池
        {
            pthread_mutex_unlock(&(pool->mutexPool));
            printf("thread 0x%x is exiting \n", (unsigned int)pthread_self());
            pthread_exit(NULL);       // 结束线程
        }

        /* 该线程可以拿出任务 */
        task.function = pool->taskQ[pool->queueFront].function;   // 队首出队操作
        task.arg      = pool->taskQ[pool->queueFront].arg;

        pool->queueFront = (pool->queueFront + 1) % pool->queueCapacity;   // 环形队列
        pool->queueSize--; 

        /* 通知可以添加新任务 */
        pthread_cond_broadcast(&(pool->notEmpty));

        /* 释放线程锁 */
        pthread_mutex_unlock(&(pool->mutexPool));

        /* 执行刚才取出的任务 */
        printf("thread 0x%x start working \n", (unsigned int)pthread_self());
        pthread_mutex_lock(pool->busyNum);
        pool->busyNum++;
        pthread_mutex_unlock(pool->busyNum);

        /* 执行任务 */
        (*(task.function))(task.arg);

        /* 任务结束处理 */           
        printf("thread 0x%x end working \n", (unsigned int)pthread_self());
        pthread_mutex_lock(pool->busyNum);
        pool->busyNum--;
        pthread_mutex_unlock(pool->busyNum);
    }

    pthread_exit(NULL);
}

/* 向线程池的任务队列中添加一个任务 */
int ThreadPoolAddTask(ThreadPool_t* pool, void *(*function)(void *arg), void *arg)
{
    pthread_mutex_lock(&(pool->mutexPool));

    /* 如果队列满了，调用wait阻塞 */
    while((pool->queueSize == pool->maxNum) && !(pool->shutdown))
    {
        pthread_cond_wait(&(pool->notFull), &(pool->mutexPool));
    }

    /* 如果线程池处于关闭状态 */
    if(pool->shutdown)
    {
        pthread_mutex_unlock(&(pool->mutexPool));
        
        return -1;
    }

    /* 清空工作线程的回调函数参数arg */
    if(pool->taskQ[pool->queueRear].arg != NULL)
    {
        free(pool->taskQ[pool->queueRear].arg);
        pool->taskQ[pool->queueRear].arg = NULL;
    }

    /* 添加任务到任务队列 */
    pool->taskQ[pool->queueRear].function = function;
    pool->taskQ[pool->queueRear].arg      = arg;
    pool->queueRear  = (pool->queueRear + 1) % pool->queueCapacity;  /* 逻辑环 */

}