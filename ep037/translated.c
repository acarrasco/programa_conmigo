#include <stdio.h>

int main(char *argv[], int argc) {
    int b, c, d, e, f, g, h;
    b = c = d = e = f = g = h = 0;

    b = 93;
    c = b;
    b *= 100;
    b += 100000;
    c = b;
    c += 17000;
    do { // block A
        f = 1;
        d = 2;
        do { // block B
            do { // block C
                e = 2;
                g = d;
                g *= e;
                g -= b;
                if (g == 0) {
                    f = 0;
                }
                e++;
                g = e;
                g -= b;
                printf("\t\tend of block C: b=%d\tc=%d\td=%d\te=%d\tf=%d\tg=%d\th=%d\n",
                    b, c, d, e, f, g, h);
            } while(g != 0);
            d++;
            g = d;
            g -= b;
            printf("\tend of block B: b=%d\tc=%d\td=%d\te=%d\tf=%d\tg=%d\th=%d\n",
                b, c, d, e, f, g, h);
        } while(g);
        if (!f) {
            h++;
        }
        g = b;
        g -= c;
        if (g) {
            b += 17;
        }
        printf("end of block A: b=%d\tc=%d\td=%d\te=%d\tf=%d\tg=%d\th=%d\n",
            b, c, d, e, f, g, h);
    } while (g);

    printf("%d\n", h);
}