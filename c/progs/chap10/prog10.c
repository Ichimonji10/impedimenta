#include <stdio.h>
//#define 1 IN
//#define 0 OUT
int main (void) {
    //start w/ state = OUT
    char c = 0;
//    int state = OUT;
    int len = 0;
    int ctr[12];
    int i, j;
    i = j = 0;

    for (i = 0; i <12; i++)
        ctr[i] = 0;
    while ((c = getchar()) != EOF)
	{
       if (c != ' ' && c != '\t' && c != '\n') {
//            state = IN;
            len++;
            printf("%d", len);
            }
       else {
            ctr[len]++;
            len = 0;
            }
	}
    for (i = 0; i <12; i++) 
        printf("%d\n", ctr[i]);
    for (i = 0; i <12; i++) {
        printf("%d\n", i);   
        for (j = 0; j <= ctr[i]; j++)
            printf("-");
        printf("\n");
        }
    return 0;
}
