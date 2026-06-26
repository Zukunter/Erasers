#include <stdio.h>

int main() {
    printf("\033[H\033[2J\033[3J");
    fflush(stdout);
return 0 ; }
