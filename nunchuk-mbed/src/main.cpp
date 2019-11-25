#include "mbed.h"

DigitalIn mybutton(PC_0, PullDown);
DigitalOut myled(PA_5);


int main()
{
  while (1) {
    if (mybutton == 0) {
      printf("$BUTTON, 0\r\n");
    }
    else {
      printf("$BUTTON, 1\r\n");
    }
    myled = mybutton;
    wait_ms(500);
  }
}

