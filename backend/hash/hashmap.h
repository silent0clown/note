#ifndef _HASH_MAP_H_
#define _HASH_MAP_H_



typedef struct{
	int key;  //键
	int val;  //值
}DataType; //对基本数据类型进行封装，类似泛型


typedef struct _HashNode{
	DataType data;
	struct _HashNode *next;  //key冲突时，通过next指针进行连接
} HashNode;


typedef struct{
	int size;
	HashNode *table;
}HashMap,*hashmap;





#endif