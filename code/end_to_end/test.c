#include <stdlib.h>
#include <time.h>

#define TRUE  1
#define FALSE 0

static int randomized = FALSE;

//gcc -Wall -O3 -shared ~/test.c -o test.so

void randomize(void)
{
  srand(time(NULL));
  randomized = TRUE;
}

/* returns a random number between base and max, inclusive */
int get_random(int base, int max)
{
  if (randomized == FALSE){
    randomize();
  }
  return rand() % (max - base + 1) + base;
}