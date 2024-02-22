#include <stdio.h>

#define PROBLEM_SIZE 2000

int main(char** argv) {
    int jumps[PROBLEM_SIZE];
    FILE *fp = fopen("input.txt", "r");
    int size = 0;
    while (fscanf(fp, "%d\n", &jumps[size]) > 0) {
        if (size >= PROBLEM_SIZE) {
            return -1;
        }
        size++;
    }

    int pc = 0;
    int steps = 0;
    while (pc >= 0 && pc < size) {
        int j = jumps[pc];
        if (j >= 3) {
            jumps[pc]--;
        } else {
            jumps[pc]++;
        }
        pc += j;
        steps++;
    }
    printf("%d\n", steps);
}