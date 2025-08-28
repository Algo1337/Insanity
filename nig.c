#include <stdio.h>

void printPoint(struct { int x, y; } p) {
    printf("Point(%d, %d)\n", p.x, p.y);
}

int main() {
    // Inline anonymous struct passed as argument
    printPoint((struct { int x, y; }){ 10, 20 });

    printf("Try programiz.pro");
    return 0;
}
