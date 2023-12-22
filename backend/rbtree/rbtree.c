#include <stdio.h>
#include <stdlib.h>
#include "rbtree.h"

#define rb_parent(r)   ((r)->parent)
#define rb_color(r) ((r)->color)
#define rb_is_red(r)   ((r)->color==RED)
#define rb_is_black(r)  ((r)->color==BLACK)
#define rb_set_black(r)  do { (r)->color = BLACK; } while (0)
#define rb_set_red(r)  do { (r)->color = RED; } while (0)
#define rb_set_parent(r,p)  do { (r)->parent = (p); } while (0)
#define rb_set_color(r,c)  do { (r)->color = (c); } while (0)


/*
 * 前序遍历"红黑树"
 */
static void preorder(rbtree_node *tree) {
    if(tree != NULL)
    {
        printf("%d ", tree->key);
        preorder(tree->left);
        preorder(tree->right);
    }
}
void preorder_rbtree(rbtree *root) {
    if (root)
        preorder(root->root);
}

/*
 * 中序遍历"红黑树"
 */
static void inorder(rbtree_node *tree) {
    if(tree != NULL)
    {
        inorder(tree->left);
        printf("%d ", tree->key);
        inorder(tree->right);
    }
}

void inorder_rbtree(rbtree *root) {
    if (root)
        inorder(root->root);
}

/*
 * 后序遍历"红黑树"
 */
static void postorder(rbtree_node *tree) {
    if(tree != NULL)
    {
        postorder(tree->left);
        postorder(tree->right);
        printf("%d ", tree->key);
    }
}

void postorder_rbtree(rbtree *root) {
    if (root)
        postorder(root->root);
}



static void rbtree_left_rotate(rbtree *T, rbtree_node *x) {
    if (x == T->nil) return;

    rbtree_node *y = x->right;
    x->right = y->left;
    if (y->left != T->nil) {
        y->left->parent = x;
    }

    y->parent = x->parent;
    // 需要考虑x是根节点的情况
    if (x->parent == T->nil) {
        T->root = y;
    }
    else {
        if (x == x->parent->left) {
            x->parent->left = y;
        } 
        else {
            x->parent->right = y;
        }
    }

    x->parent = y;
    y->left   = x;
}


static void rbtree_right_rotate(rbtree *T, rbtree_node *y) {
    if (y == T->nil) return;
    rbtree_node *x = y->left;
    
    y->left = x->right;
    if (x->right != T->nil) {
        x->right->parent = y;
    }

    x->parent = y->parent;
    // 需要考虑y是根节点的情况
    if (y->parent == T->nil) {
        T->root = x;
    }
    else {
        if (y == y->parent->left) {
            y->parent->left = x;
        } 
        else {
            y->parent->right = x;
        }
    }

    y->parent = x;
    x->right  = y;
}

// z->color == RED
// z->parent->color == RED (if not , return)
static void rbtree_insert_fixup(rbtree *T, rbtree_node *z) {
    // rbtree_node *x = z->parent;                // 父节点
    rbtree_node *y = T->nil;

    while (z->parent->color == RED) {
        if (z->parent == z->parent->parent->left) {
            y = z->parent->parent->right; // 叔节点

            // 叶子节点是黑的，所以不用单独考虑叔节点为叶子节点
            if (y->color == RED) {   // 情况3场景
                y->color = BLACK;
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                z = z->parent->parent;
            } else { // 叔节点为黑色
                if (z == z->parent->right) {  // 情况4.2
                    z = z->parent;
                    rbtree_left_rotate(T, z);
                }
                
                // 情况4.1
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                rbtree_right_rotate(T, z->parent->parent);
            }

        }
        else {
            y = z->parent->parent->left;
            
            // 叶子节点是黑的，所以不用单独考虑叔节点为叶子节点
            if (y->color == RED) {   // 情况3场景
                y->color = BLACK;
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                z = z->parent->parent;
            } else { // 叔节点为黑色
                if (z == z->parent->left) {  // 情况4.2
                    z = z->parent;
                    rbtree_right_rotate(T, z);
                }
                
                // 情况4.1
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                rbtree_left_rotate(T, z->parent->parent);
            }
        }

    }

    T->root->color = BLACK;
    return;
}

static void rbtree_insert(rbtree* T, rbtree_node *z) {
    rbtree_node *x = T->root;
    rbtree_node *y = T->nil;

    while (x != T->nil) {   // 先找到插入节点的树底
        y = x;
        if (x->key > z->key) {
            x = x->left;
        }
        else if (x->key < z->key) {
            x = x->right;
        }
        else {
            // x->key == z->key
            // exit
        }
    }

    if (y == T->nil) { // 空树
        T->root = z;
    } else if (z->key < y->key) { // 插入
        y->left = z;
    } else {
        y->right = z;
    }

    z->color = RED;
    z->left = T->nil;
    z->right = T->nil;
    z->parent = y;

    rbtree_insert_fixup(T, z);  // 自平衡

    return;
}


/**********************红黑树删除 start***************************/

/*
 * 查找最小结点：返回tree为根结点的红黑树的最小结点。
 */

static rbtree_node *rbtree_mini(rbtree *T, rbtree_node *x) {
    while (x->left != T->nil) {
        x = x->left;
    }
    return x;
}

// 获取红黑树中的最小值
int rbtree_minimum(rbtree *root, int *val) {
    if (root == NULL || val == NULL) return -1;

    rbtree_node *node = root->root;
    node = rbtree_mini(root, root->root);

    if (node == root->nil) return -1; 
    *val = node->key;

    return 0;
}

rbtree_node *rbtree_maxi(rbtree *T, rbtree_node *x) {
	while (x->right != T->nil) {
		x = x->right;
	}
	return x;
}

// 获取红黑树中的最大值
int rbtree_maximum(rbtree *root, int *val) {
    if (root == NULL || val == NULL) return -1;

    rbtree_node *node = rbtree_maxi(root, root->root);

    if (node == root->nil) return -1;

    *val = node->key;
    return 0;
}

rbtree_node *rbtree_successor(rbtree *T, rbtree_node *x)
{
    rbtree_node *y = x->parent;
    if (x->right != T->nil)
    {
        return rbtree_mini(T, x->right);
    }


    while ((y != T->nil) && (x == y->right)) {
        x = y;
        y = y->parent;
    }
    return y;
}
//调整
void rbtree_delete_fixup(rbtree *T, rbtree_node *x) {

    while ((x != T->root) && (x->color == BLACK)) {
        if (x == x->parent->left) {

            rbtree_node *w = x->parent->right;   // 兄弟节点
            if (w->color == RED) {        // 情况2.3.2
                w->color = BLACK;
                x->parent->color = RED;  

                rbtree_left_rotate(T, x->parent);
                w = x->parent->right;
            }

            if ((w->left->color == BLACK) && (w->right->color == BLACK)) {
                w->color = RED;
                x = x->parent;
            }
            else {

                if (w->right->color == BLACK) {
                    w->left->color = BLACK;
                    w->color = RED;
                    rbtree_right_rotate(T, w);
                    w = x->parent->right;
                }

                w->color = x->parent->color;
                x->parent->color = BLACK;
                w->right->color = BLACK;
                rbtree_left_rotate(T, x->parent);

                x = T->root;
            }

        }
        else {

            rbtree_node *w = x->parent->left;
            if (w->color == RED) {
                w->color = BLACK;
                x->parent->color = RED;
                rbtree_right_rotate(T, x->parent);
                w = x->parent->left;
            }

            if ((w->left->color == BLACK) && (w->right->color == BLACK)) {
                w->color = RED;
                x = x->parent;
            }
            else {

                if (w->left->color == BLACK) {
                    w->right->color = BLACK;
                    w->color = RED;
                    rbtree_left_rotate(T, w);
                    w = x->parent->left;
                }

                w->color = x->parent->color;
                x->parent->color = BLACK;
                w->left->color = BLACK;
                rbtree_right_rotate(T, x->parent);

                x = T->root;
            }

        }
    }

    x->color = BLACK;
}


rbtree_node *rbtree_delete(rbtree *T, rbtree_node *z) 
{
    rbtree_node *y = T->nil;
    rbtree_node *x = T->nil;

    if ((z->left == T->nil) || (z->right == T->nil)) {
        y = z;
    } else {
        y = rbtree_successor(T, z);  // 有左且有右，要么找到左子树中的最大值，要么找到右子树的最小值，删除该值
    }

    if (y->left != T->nil)
        x = y->left;
    else if (y->right != T->nil)
        x = y->right;


    x->parent = y->parent;
    if (y->parent == T->nil)  // 删除根节点情况
        T->root = x;
    else if (y == y->parent->left)
        y->parent->left = x;
    else
        y->parent->right = x;

    if (y != z) { // 有左有右删除一个节点后的情况
        z->key = y->key;
        z->value = y->value;
    }
    // 调整
    if (y->color == BLACK) {   // 删除红色节点不需要调整
        rbtree_delete_fixup(T, x);
    }

    return y;
}

int rbtree_delete_node(rbtree *T, KEY_TYPE key) {
    if (T == NULL) return -1;

    rbtree_node *search_node = T->nil;
    rbtree_node *tmp = T->nil;

    if (0 != iterative_rbtree_search(T, key, &search_node)) {
        printf("cant't find key %d in rbtree\n", key);
        return 1;     
    }

    tmp = rbtree_delete(T, search_node);

    if (tmp != NULL && tmp != T->nil) {
        // if (tmp == tmp->parent->left) {
        //     tmp->parent->left = T->nil;
        // } else {
        //     tmp->parent->right = T->nil;
        // }
        free(tmp);
        tmp = NULL;
    }
    return 0;
}

int rbtree_destroy(rbtree *T) {
    if(T == NULL ) return -1;

    rbtree_node *node = T->root;
    while (node != T->nil) {
        rbtree_delete_node(T, node->key);
        node = T->root;
    }
    free(T->nil);
    T->nil = NULL;
    free(T);
    T = NULL;

    return 0;
}

/**********************红黑树删除 end***************************/

/**********************红黑树查找 start***************************/
static rbtree_node *recursion_search(rbtree *root, rbtree_node *x, KEY_TYPE key) {
    if (x == root->nil || x->key==key)
        return x;

    if (key < x->key)
        return recursion_search(root, x->left, key);
    else
        return recursion_search(root, x->right, key);
}

int rbtree_search(rbtree *root, KEY_TYPE key) {
    if (root == NULL) return -1;
    
    rbtree_node *node = root->root;
    
    return recursion_search(root, node, key) ? 0 : -1;
}

int iterative_rbtree_search(rbtree *root, KEY_TYPE key, rbtree_node **tmp) {
    if (root == NULL || tmp == NULL) return -1;
        // return iterative_search(root->root, key) ? 0 : -1;
    rbtree_node *node = root->root;
    *tmp = root->nil;
    while (node != root->nil) {
        if (node->key < key) {
            node = node->right;
        } else if (node->key > key) {
            node = node->left;
        } else { // ==
            *tmp = node;
            return 0;
        }
    }

    return 1;
}
/**********************红黑树查找 end***************************/


rbtree *rbtree_create() {
    rbtree *node = (rbtree *)malloc(sizeof(rbtree));
    if (node == NULL) {
        return NULL;
    }

    node->nil = (rbtree_node *)malloc(sizeof(rbtree_node));
    if (node->nil == NULL) {
        free(node);
        node = NULL;

        return NULL;
    }

    node->nil->color = BLACK;
    node->nil->left = node->nil->right = NULL;
    node->nil->parent = NULL;

    node->root = node->nil;

    return node;
}


int rbtree_insert_node(rbtree *root, KEY_TYPE key) {
    if (root == NULL) return -2;

    // fix_it: need search 

    rbtree_node *node = (rbtree_node *)malloc(sizeof(rbtree_node));
    if (node == NULL) {
        printf("Malloc node fail\n");
        return -1;
    }

    node->key = key;

    rbtree_insert(root, node);

    return 0;
}

/*
 * 打印"红黑树"
 *
 * tree       -- 红黑树的节点
 * key        -- 节点的键值
 * direction  --  0，表示该节点是根节点;
 *               -1，表示该节点是它的父结点的左孩子;
 *                1，表示该节点是它的父结点的右孩子。
 */
// static void rbtree_print(rbtree_node *tree, KEY_TYPE key, int direction)
// {
//     if(tree != NULL)
//     {
//         if(direction==0)    // tree是根节点
//             printf("%2d(B) is root\n", tree->root->key);
//         else                // tree是分支节点
//             printf("%2d(%s) is %2d's %6s child\n", tree->root->key, rb_is_red(tree->root)?"R":"B", key, direction==1?"right" : "left");

//         rbtree_print(tree->root->left, tree->root->key, -1);
//         rbtree_print(tree->root->right,tree->root->key,  1);
//     }
// }

void print_rbtree(rbtree * root, rbtree_node *node) {
    if (node == NULL) return;

    // rbtree_node *node = root->root;
    if (node != root->nil) {

        printf("%2d(%s) has left child : %d(%s), right child :%d(%s)\n", node->key, rb_is_red(node)?"R":"B", 
                node->left->key,  rb_is_red(node->left)?"R":"B", node->right->key,  rb_is_red(node->right)?"R":"B");
        // node = node->left;
    }
    print_rbtree(root, node->left);
    print_rbtree(root, node->right);

        // rbtree_print(root, root->root->key, 0);
}