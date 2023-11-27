# 7 进程环境

## 7.8 存储空间分配
- malloc 分配指定字节数的存储区。此存储区的初始值不确定。
- calloc 为指定数量指定长度的对象分配存储空间。该空间中的每一位都初始化为0.
- realloc 增加或减少以前分配区的长度。当长度增加时，可能需要将以前分配区的内容移到另一个足够大的区域，以便在尾端提供增加的存储区。新增区域内的初始值不确定。

```c
#include<stdlib.h>
void *malloc(size_t size);

void *calloc(size_t nobj, size_t size);

void *realloc(void *ptr, size_t newsize);

// 获取环境变量信息
char *getenv(const char *name);

// 取形式为name= value的字符串，将其放到环境表中。如果name已经存在，则删除其原先的定义
int putenv(char *str);

// 将name设置为value。如果在环境中name已经存在，那么(a)若rewrite非0，则首先删除其现有的定义；(b)若rewrite为0，则不删除其现有定义(name不设置为新的value，而且也不出错)
int setenv(const char *name, const char *value, int rewrite);

// 删除name定义，即使不存在也不算出错。
int unsetenv(const char *name);
```