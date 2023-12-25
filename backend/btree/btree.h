#ifndef _BTREE_H_
#define _BTREE_H_

#include <stdio.h>
#include <stdlib.h>

#define SUB_BTREE_BANDS   3  // 6阶
// #define MAX_KEY_NUM (2 * SUB_BTREE_BANDS - 1)
// #define MIN_KEY_NUM (SUB_BTREE_BANDS - 1)

#define MAX_KEY_NUM(x) (2*x-1)
// #define FIX_LENGTH        1
#define BTREE_NO_LEAF   0
#define BTREE_IS_LEAF   1

typedef char KEY_TYPE;

typedef struct _btree_node {
#ifdef FIX_LENGTH
    KEY_TYPE keys[2 * SUB_BTREE_BANDS - 1];       // 键数组
    btree *childrens[2 * SUB_BTREE_BANDS];  // 孩子指针数组
#else
    KEY_TYPE *keys;
    struct _btree_node **childrens; // unkown type name  'btree_node'
#endif
    int keynum;   // 键个数
    int isleaf;   // 是否是叶子节
} btree_node;

typedef struct _btree {
    btree_node *root;
    int sub_order;           // 阶数 == 2 * order
} btree;

// typedef struct _btree {
//     struct _btree_node *root;
// } btree;


#ifdef  __cplusplus
extern "C" {
#endif


// 创建一个B-树
void btree_create(btree *T, int order);


// btree_node *btree_create_node(int order, int leaf);

void btree_insert(btree *T, KEY_TYPE key);

void btree_print(btree *T, btree_node *node, int layer);
// // 创建一个btree
// btree *btree_init();

// // 向树中插入键
// int btree_insert(btree *T, KEY_TYPE key);

// // 树中查找键
// btree *btree_match(const btree *tree, KEY_TYPE key);
#ifdef __cplusplus
}
#endif


#endif