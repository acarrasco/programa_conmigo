#include <stdio.h>

int main(char *argv[], int argc) {
    int b, c, d, e, f, g, h;
    b = c = d = e = f = g = h = 0;

    b = 109300;
    c = b + 17000;
    do { // block A
        f = 1;
        // for(d = 2; d < b; d++) { // block B   
        //     for (e = 2; e < b; e++) {
        //         if (d * e - b == 0) {
        //             f = 0;
        //         }
        //     }
        // }
        if (f == 0) {
            h++;
        }

        if (b != c) {
            b += 17;
        }
        printf("b=%d\n", b);
        // printf("end of block A: b=%d\tc=%d\td=%d\te=%d\tf=%d\tg=%d\th=%d\n",
        //     b, c, d, e, f, g, h);
    } while (b != c);

    printf("%d\n", h);
}