#include "mbed.h"

DigitalIn mybutton(PC_0, PullDown);
DigitalOut myled(PA_5);


int main()
{
  int change = -1;
  while (1) {
    if (change != mybutton) {
      change = mybutton;
      if (mybutton == 0) {
        printf("$BUTTON, 1\r\n");
      }
      else {
        printf("$BUTTON, 0\r\n");
      }
      myled = mybutton;
    }
  }
}
