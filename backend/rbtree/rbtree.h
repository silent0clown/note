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



#endif