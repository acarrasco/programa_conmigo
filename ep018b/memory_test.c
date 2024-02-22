#include <stdio.h>

# define SIZE 10

int main(char** argv) {
    int a[SIZE];
    int b[SIZE];

    for (int i = 0; i < SIZE; i++) {
        a[i] = b[i] = i;
    }

    b[SIZE+2] = 42;
    
    printf("sizeof(int) = %d\n", sizeof(int));
    printf("a = 0x%x\n", a);
    printf("&a[SIZE] = 0x%x\n", a + SIZE);
    printf("b = 0x%x\n", b);

    for (int i = 0; i < SIZE; i++) {
        printf("a[%i] = %d\n", i, a[i]);
        printf("b[%i] = %d\n", i, b[i]);
    }
}