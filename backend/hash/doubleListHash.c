/**
	采用双向循环链表实现HASH表
*/
#include <stdio.h>
#include <string.h>
#include  <stdlib.h>
#include <assert.h>
 
 
#define RS_OK 0
#define  RS_WRONG 1
#define MAX_LEN 128
 
#define FUNCTION_SHOW printf("this is %s, %d\n", __FUNCTION__, __LINE__);
 
/*双向循环链表结点*/
typedef struct list {
    struct list *next;
    struct list *prev;
    int key;
    int data;
}list;
 
/*hash表数据结构*/
typedef struct hash {
	/*hash桶的大小*/
    int bucket_size;
	/*初始化时共申请bucket_size块list结构
	  每一个list都是一个冲突链的头结点。
	*/
    struct list *buckets;
}hash;
 
void list_print(struct list *head)
{
    list *node;
    
    FUNCTION_SHOW
    if (!list_empty(head)) 
        return;
   node = head->next;
   while (node != head) {
        printf ("%d\n", node->key);
        node = node->next;
   }
   return;
}
 
/*初始化双向循环链表*/
void list_init(struct list *head)
{   
 
    FUNCTION_SHOW   
    if (head == NULL) 
        return;
    head->next = head;
    head->prev = head;
}
 
/*删除双向循环链表*/
int destroy_list(struct list *head)
{
    int i;
    struct list *node, *tmp;
    
    FUNCTION_SHOW
	
#ifdef RECURSION
    if (head->next = head)
        return RS_OK;
    node = head->next->next;
    free(head->next);
	head->next = NULL;
    destroy_list(node);
    return RS_OK;
#endif
    node = head->next;
    while (node != head) {
        tmp = node->next;
        free(node);
        node = NULL;
        node = tmp;
    }
    return RS_OK;
}
 
/*判断链表是否为空*/
int list_empty(struct list *head)
{
 
    FUNCTION_SHOW
    if (head == NULL) 
        return RS_WRONG;
    else if (head->next == head) 
        return RS_OK;
    else
        return RS_WRONG;
}
 
/*将数据插入链表尾*/
void list_insert_tail(struct list *head, struct list *node)
{
    FUNCTION_SHOW
    list *oldnode = NULL;
    if (node == NULL ||head == NULL ) {
        return;
    }
 
    oldnode = head->prev;
    oldnode ->next = node;
    node->prev = oldnode;
    head->prev = node;
    node->next = head;
 
    list_print(head);
    
   return ;
}
 
/*删除结点*/
void list_remove(struct list *node)
{
    list *oldnode;
	
    FUNCTION_SHOW
    if (node == NULL) {
        return ;
    }
    oldnode = node->prev;
    oldnode->next = node->next;
    node->next->prev = oldnode;
}
 
/*删除所有和KEY值相同的链表结点*/
void list_remove_data(struct list *head, int key)
{
    list *node, *tmp;
	
    FUNCTION_SHOW
    if ((node == NULL) || (head == NULL)
         ||(head->prev == head)) {
        return ;
    }
    
    node = head->next;
    while (node != head) {
            tmp = node->next;
            if (node->key == key) {
                list_remove(node);
                free(node);
           }
           node = tmp;
    }
}
 
/*创建hash表*/
struct hash *hash_create(int bucket_size)
{
    int i;
    hash *hashtable = NULL;
    
    FUNCTION_SHOW
    hashtable = malloc(sizeof(hash));
    if (hashtable == NULL) {
        hashtable = malloc(sizeof(hash));
        if (hashtable == NULL)
        return NULL;
     }
    hashtable->bucket_size = bucket_size;
    hashtable->buckets = malloc((sizeof(list) * bucket_size));
    if (hashtable->buckets == NULL) {
        hashtable->buckets = malloc((sizeof(list) * bucket_size));
        free(hashtable);
        return NULL;
    }
    for (i=0; i < bucket_size; i++) {
        list_init(&hashtable->buckets[i]);
    }
    
    return hashtable;
}
 
/*hash函数，采用除数留余法*/
int hash_hasher(struct hash *hash, int key)
{
    int addr;
	
    FUNCTION_SHOW
    addr = key%hash->bucket_size;
    
    return addr;
}
 
/*创建hash结点*/
list *create_hash_node(int key)
{
    list *hashnode;
	
    FUNCTION_SHOW
    hashnode = malloc(sizeof(list));
    if (hashnode == NULL) 
        return;
    hashnode->key = key;
    hashnode->prev = NULL;
    hashnode->next = NULL;
 
    return hashnode;
}
 
/*插入新的hash结点*/
int hash_insert(struct hash *hash, int key)
{
 
    list *hashnode;
	
    FUNCTION_SHOW
    hashnode = create_hash_node(key);
    list_insert_tail(&hash->buckets[ hash_hasher(hash, key)], hashnode);
   
    return RS_OK;
}
 
/*删除hash结点*/
int hash_remove(struct hash *hash, int key)
 
{
    FUNCTION_SHOW
    list_remove_data(&hash->buckets[ hash_hasher(hash, key)], key);
    return RS_OK;
}
 
/*hash 查找*/
int hash_lookup(struct hash *hash, int key)
 
{
    list *head, *node, *tmp;
 
    FUNCTION_SHOW
    head = &hash->buckets[hash_hasher(hash, key)];
    if (!list_empty(head))
        return;
    node = head->next;
   while (node != head) {
        tmp = node->next;
        if (node->key == key) {
            printf ("the node key is %d\n", node->key);
            return RS_OK;
        }
        node = tmp;
    }
    return RS_WRONG;
}
 
/*删除hash表*/
int destory_hash_table(hash *hash)
{
    int i;
 
    for (i=0; i < hash->bucket_size; i++) {
        FUNCTION_SHOW
        if (destroy_list(&hash->buckets[i])) {
            printf ("destroy list error\n");
        }
    }
    free(hash->buckets);
	hash->buckets = NULL;
    free(hash);
	hash = NULL;
}
 
/*测试用例*/
int main(int argc, char *argv[])
{
    int i;
    struct hash *hashtable;
 
   hashtable = hash_create(MAX_LEN);
    for (i=0; i < MAX_LEN; i++) {
        printf("insert %d\n", i);
        if(hash_insert(hashtable, i)) {
            printf ("insert error\n");
            return RS_WRONG;
        }
    }
 
    for (i=0; i < MAX_LEN; i++) {
        if (hash_lookup(hashtable, i)) {
            printf ("hash lookup error\n");
        }
    }
    destory_hash_table(hashtable);
	hashtable = NULL;
 
    return RS_OK;
}