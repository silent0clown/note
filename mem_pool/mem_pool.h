#ifndef MEM_POOL_H
#define MEM_POOL_H

#include <stdio.h>


#ifdef __linux__
    #define PAGE_SIZE (4096)
#else
    #define PAGE_SIZE (4096)
#endif

#define MP_ALIGNMENT   (16)



#define mp_align(n, alignment) (((n)+(alignment-1)) & ~(alignment-1))
#define mp_align_ptr(p, alignment) (void *)((((size_t)p)+(alignment-1)) & ~(alignment-1))

//每4k一block结点
struct mp_node_s {
    unsigned char *end;//块的结尾
    unsigned char *last;//使用到哪了
    struct mp_node_s *next;//链表
    int quote;//引用计数
    int failed;//失效次数
};

struct mp_large_s {
    struct mp_large_s *next;//链表
    int size;//alloc的大小
    void *alloc;//大块内存的起始地址
};

// 整个内存池的管理结构
struct mp_pool_s {
    struct mp_large_s *large;
    struct mp_node_s *head;
    struct mp_node_s *current;
};

#ifdef __cplusplus
extern "C" {
#endif

struct mp_pool_s *mp_create_pool(size_t size);

void mp_destroy_pool(struct mp_pool_s *pool);

// 内存申请API
void *mp_malloc(struct mp_pool_s *pool, size_t size);

// 内存申请API
void *mp_calloc(struct mp_pool_s *pool, size_t size);

// 释放内存API
void mp_free(struct mp_pool_s *pool, void *p);

void mp_reset_pool(struct mp_pool_s *pool);

void monitor_mp_poll(struct mp_pool_s *pool, char *tk);

#ifdef __cplusplus
}
#endif

#endif // end define MEM_POOL_H