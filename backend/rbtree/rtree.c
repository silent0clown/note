#include "rbtree.h"


void rbtree_left_rotat(rbtree *T, rbtree_node *x) {
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


void rbtree_right_rotat(rbtree *T, rbtree_node *y) {
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
void rbtree_insert_fixup(rbtree *T, rbtree_node *z) {
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
                    rbtree_left_rotat(T, z);
                }
                
                // 情况4.1
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                rbtree_right_rotat(T, z->parent->parent);
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
                    rbtree_right_rotat(T, z->parent);
                }
                
                // 情况4.1
                z->parent->color = BLACK;
                z->parent->parent->color = RED;
                rbtree_left_rotat(T, z->parent->parent);
            }
        }

    }

    T->root->color = BLACK;
    return;
}

void rbtree_insert(rbtree* T, rbtree_node *z) {
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
rbtree_node *rbtree_mini(rbtree *T, rbtree_node *x) {
	while (x->left != T->nil) {
		x = x->left;
	}
	return x;
}

rbtree_node *rbtree_maxi(rbtree *T, rbtree_node *x) {
	while (x->right != T->nil) {
		x = x->right;
	}
	return x;
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

			rbtree_node *w = x->parent->right;
			if (w->color == RED) {
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
		y = rbtree_successor(T, z);  // 有左且有右
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

	if (y != z)
	{
		z->key = y->key;
		z->value = y->value;
	}
	// 调整
	if (y->color == BLACK) {
		rbtree_delete_fixup(T, x);
	}

	return y;
}

/**********************红黑树删除 end***************************/

/**********************红黑树查找 start***************************/
rbtree_node *rbtree_search(rbtree *T, KEY_TYPE key) {

	rbtree_node *node = T->root;
	while (node != T->nil) {
		if (key < node->key) {
			node = node->left;
		}
		else if (key > node->key) {
			node = node->right;
		}
		else {
			return node;
		}
	}
	return T->nil;
}
/**********************红黑树查找 end***************************/