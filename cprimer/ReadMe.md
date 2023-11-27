# 成员函数
类定义了如何表示和控制数据。成员函数归类所有，描述了操纵数据的方法。


# 面向行的输入
cin.getline(value, value_len)

# 类对象
要使用vector对象，必须包含头文件vector。vector包含在名称空间std中。

```c++
// 声明创建一个vt的vector对象，它可存储n_elem个类型为typeName的元素。
// 其中n_elem可以是整型常量/变量。
vector<typeName> vt(n_elem)

// 声明创建一个名为arr的array对象，它包含n_elem个类型为typename的元素
// n_elem不能为变量
array<typeName, n_elem> arr;
```

# 函数重载（函数多态）
函数重载的表现：
可以声明两个同名却有不同参数的函数，编译器会根据调用参数自动选择对应的函数声明。

# eof判断：
```c++
cin.fail() == false;  
// or
cin.eof() == true;
// or
while(cin)
```

```C++
// 在C++中，不指定参数列表时应使用省略号：
void say_bye(...);

// 括号为空与在括号中使用void等效

void test();   == void test(void para);


// 声明一个const array对象，该对象包含4个string对象，用于表示几个季节
const int Seasons = 4;
const std::array<std::string, Seasons> Snames = {"Spring", "Summer", "Fall", "Winter"};


// 函数指针，指向函数的指针
double (*pf)(int);

// 调用函数指针示例
double pam(int);
double (*pf)(int);
pf = pam;
double y = pf(4);
// or
double x = (*pf)(4);


// 指针函数，返回指针的函数
double* pf(int);
```

# 内联函数
编译器将内联函数代码替换为函数调用，程序无须调到另一个位置处执行代码再跳回来，因此运行速度比常规函数稍快，但内存占用更多。

使用场景：频繁调用，但执行时间很短的函数。

调用方式：
- 在函数声明前加上关键字inline
- 在函数定义前加上关键字inline

# 引用
```c++
// 引用必须初始化值
int rat = 1000;
// rodents和rat可以互换，他们指向相同的值和内存单元
int & rodents = rat;

引用的效率更高
```

# 对象、继承和引用
ofsteam对象可以使用ostream类的方法，使得能够将特性从一个类传递给另一个类的语言特性被称为继承。
ostream是基类，ofstream是派生类（ofstream是建立在ostream上的）。派生类继承了基类的方法。
基类引用可以指向派生类对象，无需进行强制类型转换。

# 默认参数
```c++
// 必须从右向左添加默认值
char* left(const char* str, int n = 1);
```

# 函数模板
```c++
template<class T>  // or typename T
void Swap(T & a, T & b) {
    T temp;
    temp = a;
    a = b;
    b = temp;
}
// 将模板放在头文件中，并在需要使用模板的文件中包含头文件

// 显式具体化
template <> void Swap(job &, job &);
// or
template <> void Swap<job>(job &, job &);

// 显式实例化
template void Swap<job>(job &, job &);

```

头文件常包含内容：
- 函数原型
- 使用#define、const或typedef定义的常量
- 结构声明
- 类声明
- 模板声明
- 内联函数

# 对象和类

```c++
// class定义类，Stock是这个新类的类型名
class Stock {
    // private标识只能通过公共成员访问的类成员
    // private可省略，默认为private
    private:
        std::string company;
        long shares;
        double share_val;
        double total_val;
        void set_tot(){total_val = shares * share_val;}
    // 公有成员函数是程序和对象的私有成员之间的桥梁
    publice:
        void acquire(const std::string & co, long n, double pr);
        void buy(long num, double price);
        void sell(long num, double price);
        void update(double price);
        void show();
}
```

# 友元
- 友元函数
    通过让函数成为类的友元，可以赋予该函数与类的成员相同的访问权限。友元机制允许非成员函数访问私有数据。
- 友元类
- 友元成员函数