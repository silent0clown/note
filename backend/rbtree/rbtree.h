#ifndef _RBTREE_H_
#define _RBTREE_H_

#define RED   0
#define BLACK 1

typedef int KEY_TYPE;


typedef struct _rbtree_node {
    KEY_TYPE key;
    // value
    void     *value;
    
    // rbtree
    struct _rbtree_node *left;
    struct _rbtree_node *right;
    struct _rbtree_node *parent;
    unsigned char color;
    // end rbtree
} rbtree_node;

typedef struct _rbtree {
    rbtree_node *root;
    rbtree_node *nil;      // NULL
} rbtree;


#ifdef __cplusplus
extern "C" {
#endif
// 创建红黑树，返回"红黑树的根"！
rbtree* rbtree_create();

// 销毁红黑树
int rbtree_destroy(rbtree *root);

// 将结点插入到红黑树中。插入成功，返回0；失败返回-1。
int rbtree_insert_node(rbtree *root, KEY_TYPE key);

// 删除结点(key为节点的值)
int rbtree_delete_node(rbtree *T, KEY_TYPE key);


// 前序遍历"红黑树"
void preorder_rbtree(rbtree *root);
// 中序遍历"红黑树"
void inorder_rbtree(rbtree *root);
// 后序遍历"红黑树"
void postorder_rbtree(rbtree *root);

// (递归实现)查找"红黑树"中键值为key的节点。找到的话，返回0；否则，返回-1。
int rbtree_search(rbtree *root, KEY_TYPE key);
// (非递归实现)查找"红黑树"中键值为key的节点。找到的话，返回0；否则，返回-1。
int iterative_rbtree_search(rbtree *root, KEY_TYPE key, rbtree_node **tmp);

// 返回最小结点的值(将值保存到val中)。找到的话，返回0；否则返回-1。
int rbtree_minimum(rbtree *root, int *val);
// 返回最大结点的值(将值保存到val中)。找到的话，返回0；否则返回-1。
int rbtree_maximum(rbtree *root, int *val);

// 打印红黑树
void print_rbtree(rbtree *root, rbtree_node *node);

#ifdef __cplusplus
}
#endif



#endif