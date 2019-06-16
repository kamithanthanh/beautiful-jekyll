#include<stdio.h>
#include<stdlib.h>
#include<time.h>
// gcc -shared -Wl,-soname,rand -o rand.so -fPIC rand.c
int getrand()
{
        int t ;
        t = rand() ;
        return t ;
}
int setSrand(int t)
{
        srand(t) ;
        return t ;
}
int main()
{
        return  0 ;
}