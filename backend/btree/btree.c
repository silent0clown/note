
#include <stdio.h>
#include "btree.h"

btree_node *btree_create_node(int order, int leaf) {
    btree_node *node = (btree_node *)calloc(1, sizeof(btree_node));
    if (node == NULL) {
        printf("calloc node fail\n");
        return NULL;
    }

    node->isleaf = leaf;
    node->keys = (KEY_TYPE *)calloc(1,  (2*order-1)* sizeof(KEY_TYPE));
    node->childrens = (btree_node **)calloc(1, (2*order) * sizeof(btree_node *));
    node->keynum = 0;

    return node;
}


void btree_create(btree *T, int order) {
    T->sub_order = order;

    btree_node *node = btree_create_node(order, BTREE_IS_LEAF);
    T->root = node;
}

void btree_split_child(btree *T, btree_node *node, int childPos) {
    int order = T->sub_order;
    btree_node *child_node = node->childrens[childPos];
    btree_node *brother_node = btree_create_node(order, child_node->isleaf);
    brother_node->keynum = order - 1;   // 平分

    int j = 0;
    for (j = 0; j < order - 1; j++) {
        brother_node->keys[j] = child_node->keys[j + order];
    }

    if (child_node->isleaf == BTREE_NO_LEAF) { // 内部节点需要拷贝子节点信息
        for (j = 0; j < order; j++) {
            brother_node->childrens[j] = child_node->childrens[j+order];
        }
    }
    child_node->keynum = order - 1;   // 分裂后只留一半的key

    for (j = node->keynum; j >= childPos+1; j--) {
        node->childrens[j+1] = node->childrens[j];
    }

    node->childrens[order+1] = brother_node;

    for (j = node->keynum-1; j >= order; j--) {
        node->keys[j+1] = node->keys[j];
    } 
    node->keys[order] = child_node->keys[order-1]; // 中位数移到父节点
    node->keynum += 1;

}

void btree_insert_nonfull(btree *T, btree_node *node, KEY_TYPE key) {
    if (T == NULL || node == NULL) return;

    int i = node->keynum - 1;

    if (node->isleaf == BTREE_IS_LEAF) {
        while (i >= 0 && node->keys[i] > key) { // 给插入值挪位置
            node->keys[i+1] = node->keys[i];
            i--;
        }
        node->keys[i+1] = key;
        node->keynum += 1;
    } else {
        while (i >= 0 && node->keys[i] > key) 
            i--;     // 找到待插入子节点的Pos
        
        if (node->childrens[i+1]->keynum == MAX_KEY_NUM(T->sub_order)) { // 子节点数量满了
            btree_split_child(T, node, i+1);
            if (key > node->keys[i+1])
                i++;
        }
        btree_insert_nonfull(T, node->childrens[i+1], key);
    }
}


void btree_insert(btree *T, KEY_TYPE key) {
    if (T == NULL || T->root == NULL) return;

    btree_node *root = T->root;
    if (root->keynum == MAX_KEY_NUM(T->sub_order)) { // need split
        btree_node *node = btree_create_node(T->sub_order, BTREE_IS_LEAF); // 创建一个父节点
        T->root = node;
        node->childrens[0] = root;

        btree_split_child(T, node, 0);

        int i = 0;
        if (node->keys[0] < key) 
            i++;
        btree_insert_nonfull(T, node->childrens[i], key);
    } else {
        btree_insert_nonfull(T, root, key);
    }
}




void btree_print(btree *T, btree_node *node, int layer) {
    btree_node *p = node;
    int i;
    if(p) {
        printf("\nlayer = %d, keynum = %d, is_leaf = %d\n",layer, p->keynum, p->isleaf);
        for(i = 0; i < p->keynum; i++) {
            printf("%c ", p->keys[i]);
        }
        printf("\n");

#if 0
        printf("%p\n", p);
        for(i = 0; i <= 2 * T->t; i++)
            printf("%p ", p->childrens[i]);
        printf("\n");
#endif
        layer++;
        for(i = 0; i <= p->keynum; i++)
            if(p->childrens[i])
                btree_print(T, p->childrens[i], layer);

    }
    else printf("the tree is empty\n");
}

// #define SUB_BTREE_BANDS    3

// typedef struct _btree_node {
// #if 0
//     int keys[2 * SUB_BTREE_BANDS -1];     // 5
//     struct _btree_node *childrens[2 * SUB_BTREE_BANDS]; // 6
// #else
//     int *keys;
//     struct _btree_node **childrens;
// #endif
//     int keynum; // 代表结点里存储的数量
//     int isleaf;

// } btree_node;

// typedef struct _btree {
//     struct _btree_node *root;
// } btree;

// b+ tree 所有的数据存储在叶子结点上


// btree *btree_init() {
//     btree *tree = (btree *)calloc(1, sizeof(btree));
//     if (tree == NULL) {
//         printf("malloc tree fail\n");
//         return NULL;
//     }
//     tree->isleaf = BTREE_IS_LEAF;
//     // tree->keynum = 0;
//     // tree->keys[MAX_KEY_NUM] = { 0 };
//     // tree->childrens[MAX_KEY_NUM + 1] = 
//     // btree_node *tree_node = btree_create_node(0);
//     // if (tree_node == NULL) {
//     //     printf("malloc tree_node fail\n");
//     //     free(tree);
//     //     return NULL;
//     // }
//     // tree->root = tree_node;

//     return tree;
// }

// static int binary_search(const int keynum, const KEY_TYPE *keylist,const KEY_TYPE findKey) {
//     if (keylist == NULL || keynum < 1) return -1;

//     int low_pos = 0;
//     int high_pos = keynum - 1;

//     while (low_pos <= high_pos) {
//         KEY_TYPE mid_pos = (low_pos + high_pos)/2;
//         if (findKey < keylist[mid_pos]) {
//             high_pos = mid_pos - 1;
//         } else if (findKey > keylist[mid_pos]) {
//             low_pos = mid_pos + 1;    
//         } else {
//             return mid_pos + 1;
//         }
//     }
//     return 0;
// }


// btree *btree_recursive_match(const btree* tree, KEY_TYPE key, int *KeyPos) {
//     if (tree == NULL || tree->keynum == 0) return NULL;

//     int i = 0;  // 指向child
//     while((i < tree->keynum) && (tree->keys[i] < key)) { // 找到最接近key的child
//         i++;
//     }

//     if (i < tree->keynum && tree->keys[i] == key) {
//         *KeyPos = i;
//         return tree;
//     }

//     if (tree->isleaf == BTREE_IS_LEAF) {
//         return NULL;
//     }

//     tree = tree->childrens[i];        // 从磁盘读取第i个孩子的数据
    
//     return btree_recursive_match(tree, key, KeyPos);
// }

// btree *btree_match(const btree *tree, KEY_TYPE key) {
//     if (tree == NULL) {
//         printf("tree is NULL\n");
//         return NULL;
//     }

//     int KeyPos = -1;
//     return btree_recursive_match(tree, key, &KeyPos);
// }




// int btree_insert(btree *T, KEY_TYPE key) {
//     if (T == NULL) return -1;

//     // 根节点已满，插入前进行分裂调整
//     if (T->keynum == MAX_KEY_NUM) {
//         btree *node = (btree *)calloc(1, sizeof(btree));
//         if (!node) {
//             printf("malloc node fail\n");
//             return -1;
//         }
//         // *T = node;
//         node->isleaf = BTREE_NO_LEAF;
//         node->keynum = 0;
//         node->childrens[0] = T;


//     }




//     int i = 0;
//     while (i < T->keynum && T->keys[i] < key) {
//         i++;
//     }

//     if (T->keys[i] > key && T->keynum < MAX_KEY_NUM) {
//         for (int j = T->keynum; j > i; j--)
//         T->keys[j] = T->keys[j - 1];
//     }
//     T->keys[i] = key;


// }


// btree_node *btree_create_node(int isleaf) {
//     btree_node *node = (btree_node *)calloc(1, sizeof(btree_node));
//     if (node == NULL) {
//         return NULL;
//     }

//     node->isleaf = isleaf;
//     *node->keys = calloc(2 * SUB_BTREE_BANDS - 1, sizeof(btree_node));
//     *node->childrens = (btree_node *)calloc(2 * SUB_BTREE_BANDS, sizeof(btree_node));
//     node->keynum = 0;
//     return node;
// }

// void btree_destroy_node(btree_node *node) {

// }

// // x: 分裂结点的父节点
// // i：分裂第几个元素
// void btree_split_child(btree *T, btree_node *x, int idx) {
//     btree_node *y = x->childrens[idx];
//     btree_node *z = btree_create_node(y->isleaf);
//     z->keynum = SUB_BTREE_BANDS - 1;

//     int i = 0;
//     for (i = 0; i < SUB_BTREE_BANDS - 1; i++) {
//         z->keys[i] = y->keys[SUB_BTREE_BANDS + i];
//     }

//     if (y->isleaf == 0) { //inner
//         for (i = 0; i < SUB_BTREE_BANDS - 1; i++) {
//             z->childrens[i] = y->childrens[SUB_BTREE_BANDS + i];
//         }
//     }

//     y->keynum = SUB_BTREE_BANDS;

//     for (i = x->keynum; i >= idx + 1; i--) {
//         x->childrens[i+1] = x->childrens[i];
//     }
//     x->childrens[i+1] = z;

//     for(i = x->keynum-1; i >= idx; i--) {
//         x->keys[i+1] = x->keys[i];
//     }

//     x->keys[i] = y->keys[SUB_BTREE_BANDS];
//     x->keynum += 1;
// }

// void btree_insert(btree *T, KEY_TYPE key) {
//     btree_node *r = T->root;

//     if (r->keynum < MAX_KEY_NUM) {
//         if (r->childrens[r->keynum - 1]->keys < key) { // 大于当前节点最大值
//             r->keys[r->keynum] = key;
//         } else {
//             int i = 0;
//             for (i = 0; i < r->keynum; i++) {
//                 if (r->childrens[])
//             }
//         }

//         r->keynum++;
//     }

//     if(r->keynum == 2 * SUB_BTREE_BANDS - 1) { // 分裂
//         btree_node *node = btree_create_node(0);
//         T->root = node;

//         node->childrens[0] = r;
//         btree_split_child(T, node, 0);
//     }
// }

// void btree_merge(btree *T, btree_node *x, int i, int idx) {
//     btree_node *left = x->childrens[idx];
//     btree_node *right = x->childrens[idx+1];

//     left->keys[left->keynum] = x->keys[idx];
    
//     int i = 0;
//     for (i = 0; i < right->keynum; i++) {
//         left->keys[SUB_BTREE_BANDS+i] = right->keys[i];
//     }

//     if (!left->isleaf) {
//         for (i = 0; i < SUB_BTREE_BANDS; i++) {
//             left->childrens[SUB_BTREE_BANDS + i] = right->childrens[i];
//         }
//     }
//     left->keynum += SUB_BTREE_BANDS;

//     btree_destroy_node(right);

//     for (i = idx+1; i < x->keynum; i++) {
//         x->keys[i - 1] = x->keys[i];
//         x->childrens[i] = x->childrens[i+1]; // 为什么两个下标不一致？
//     }

// }