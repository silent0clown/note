# 5 标准I/O函数

```c
#include <stdio.h>
#include <wchar.h>

int fwide(FILE *fp, int mode);

// 一次读一个字符
int getc(FILE *fp);
int fgetc(FILE *fp);
int getchar(void);

// output
int putc(int c, FILE *fp);
int fputc(int c, FILE *fp);
int putchar(int c);

// 每次一行I/O
char *fgets(char *restrict buf, int n, FILE *restrict fp);
char *gets(char *buf);     // 不推荐使用

int fputs(const char *restrict str, FILE *restrict fp);
int puts(const char *str);

```
标准I/O库提供缓冲的目的是尽可能减少使用read和write调用的次数。

flush: 将缓冲区中的内容写到磁盘上，或者丢弃已存储在缓冲区中的数据。

## 5.6读和写流
1. 每次一个字符的I/O，一次读写一个字符，如果流是带缓冲的，则标准I/O函数处理所有缓冲。
2. 每次一行的I/O，如果想要一次读或写一行，则使用fgets和fputs。每行都以一个换行符终止。
3. 直接I/O，fread和fwrite函数。常用于从二进制文件中每次读或写一个结构。

## 5.8
标准I/O库与直接调用read和write函数相比并不慢很多。

## 5.9 二进制I/O
```c
#include<stdio.h>
// fread and fwrite return 读写个数
size_t fread(void *restrict ptr, size_t size, size_t nobj, FILE *restrict fp);

/* ptr       : data pointer wait to write
 * size      : data length
 * nobj      ：write loop times
 * fp        : write to file
*/
size_t fwrite(const void *restrict ptr, size_t size, size_t nobj, FILE *restrict fp);
```

## 5.10 定位流

```c
#include<stdio.h>
long ftell(FILE *fp);

/* 
 * whence value : 1. SEEK_SET;   2. SEEK_CUR;   3. SEEK_END
*/
int fseek(FILE *fp, long offset, int whence);

void rewind(FILE *fp);
```
## 5.11 格式化I/O
```c
printf()

fprintf()

dprintf()

sprintf()

snprintf()

scanf()

fscanf()

sscanf()
```