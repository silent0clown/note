
#include <stdio.h>


#define SUB_M    3

typedef struct _btree_node {
#if 0
    int keys[2 * SUB_M -1];     // 5
    struct _btree_node *childrens[2 * SUB_M]; // 6
#else
    int *keys;
    struct _btree_node **childrens;
#endif
    int num; // 代表结点里存储的数量
    int leaf;

} btree_node;

typedef struct _btree {
    struct _btree_node *root;
} btree;

// b+ tree 所有的数据存储在叶子结点上


btree_node *btree_create_node(int leaf) {
    btree_node *node = (btree_node *)calloc(1, sizeof(btree_node));
    if (node == NULL) {
        return NULL;
    }

    node->leaf = leaf;
    node->keys = calloc(2 * SUB_M - 1, sizeof(btree_node));
    node->childrens = (btree_node *)calloc(2 * SUB_M, sizeof(btree_node));
    node->num = 0;
    return node;
}

void btree_destroy_node(btree_node *node) {

}

// x: 分裂结点的父节点
// i：分裂第几个元素
void btree_split_child(btree *T, btree_node *x, int idx) {
    btree_node *y = x->childrens[idx];
    btree_node *z = btree_create_node(y->leaf);
    z->num = SUB_M - 1;

    int i = 0;
    for (i = 0; i < SUB_M - 1; i++) {
        z->keys[i] = y->keys[SUB_M + i];
    }

    if (y->leaf == 0) { //inner
        for (i = 0; i < SUB_M - 1; i++) {
            z->childrens[i] = y->childrens[SUB_M + i];
        }
    }

    y->num = SUB_M;

    for (i = x->num; i >= idx + 1; i--) {
        x->childrens[i+1] = x->childrens[i];
    }
    x->childrens[i+1] = z;

    for(i = x->num-1; i >= idx; i--) {
        x->keys[i+1] = x->keys[i];
    }

    x->keys[i] = y->keys[SUB_M];
    x->num += 1;
}

void btree_insert(btree *T, int key) {
    btree_node *r = T->root;

    if(r->num == 2 * SUB_M - 1) { // 分裂
        btree_node *node = btree_create_node(0);
        T->root = node;

        node->childrens[0] = r;
        btree_split_child(T, node, 0);
    }
}

void btree_merge(btree *T, btree_node *x, int i, int idx) {
    btree_node *left = x->childrens[idx];
    btree_node *right = x->childrens[idx+1];

    left->keys[left->num] = x->keys[idx];
    
    int i = 0;
    for (i = 0; i < right->num; i++) {
        left->keys[SUB_M+i] = right->keys[i];
    }

    if (!left->leaf) {
        for (i = 0; i < SUB_M; i++) {
            left->childrens[SUB_M + i] = right->childrens[i];
        }
    }
    left->num += SUB_M;

    btree_destroy_node(right);

    for (i = idx+1; i < x->num; i++) {
        x->keys[i - 1] = x->keys[i];
        x->childrens[i] = x->childrens[i+1]; // 为什么两个下标不一致？
    }

}