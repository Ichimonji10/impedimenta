/* prog9.c -- declare an int var, read a value from standard input, and write the value of var to standard output */

#include <stdio.h>

int main(void)
{
	int var = 10;

	printf("Please enter a number less than +-32767: ");
	scanf("%d", &var);
	printf("%d %d %d\n", var, 2 * var, var * var);

	return 0;
}
