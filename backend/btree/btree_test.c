#include "btree.h"

int main() {
    btree *Tree = NULL;
    char list[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    
    btree_create(Tree, 3);

    for (unsigned long long i = 0; i < sizeof(list)/sizeof(char); i++) {
        btree_insert(Tree, list[i]);
    }
    
    btree_print(Tree, Tree->root, 0);
}