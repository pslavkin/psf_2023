#include "sapi.h"
#include "arm_math.h"


uint16_t printQ31(q31_t n,char *buf)
{
   int i;
   float ans=(n&0x80000000)?-1:0;
   for(i=1;i<32;i++)
   {
      if(n&(0x80000000>>i)){
         ans+=1.0/(1U<<i);
      }
   }
   return sprintf(buf,"q31: %i float:%.20f\r\n",n,ans);
}
uint16_t printQ7(q15_t n,char *buf)
{
   int i;
   float ans=(n&0x80)?-1:0;
   for(i=1;i<8;i++)
   {
      if(n&(0x80>>i)){
         ans+=1.0/(1U<<i);
      }
   }
   return sprintf(buf,"q7: %i float:%.20f\r\n",n,ans);
}
uint16_t printQ15(q15_t n,char *buf)
{
   int i;
   float ans=(n&0x8000)?-1:0;
   for(i=1;i<16;i++)
   {
      if(n&(0x8000>>i)){
         ans+=1.0/(1U<<i);
      }
   }
   return sprintf(buf,"q15: %i float:%.20f\r\n",n,ans);
}
q15_t multiQ15(q15_t a,q15_t b)
{
   q31_t ans;
   ans=a*b;
   ans<<=1;
   return ans>>16;
}

q15_t printSqrtQ15(q15_t n,char *buf)
{
   q15_t b;
   arm_sqrt_q15(n,&b);
   return printQ15(b,buf);
}

int main ( void ) {
   uint16_t sample = 0;
   int16_t len;
   char buf [ 200 ];

   boardConfig (                  );
   uartConfig  ( UART_USB, 460800 );
   adcConfig   ( ADC_ENABLE       );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );
   q15_t n1=0x4000;

   q15_t a=0x4000;
   q15_t b=0x2300;

   q15_t m=0x0000;
   q31_t n2=0x40000000;
   while(1) {
      cyclesCounterReset();
      //q15 * q15 termina en q30
      //n2=n1*n1;
      //n2<<=1;
      //len=printQ31(n2,buf);
      //uartWriteByteArray ( UART_USB ,buf ,len);
      len=printQ15(a,buf);
      uartWriteByteArray ( UART_USB ,buf ,len);
      len=printQ15(b,buf);
      uartWriteByteArray ( UART_USB ,buf ,len);

      m=multiQ15(a,b);
      m>>=8;
      len=printQ7(m,buf);
      uartWriteByteArray ( UART_USB ,buf ,len);


      //n1=((q31_t)n1*(q31_t)n1)>>15;
      //len=printQ15(n1,buf);
      //uartWriteByteArray ( UART_USB ,buf ,len);
      //len=printSqrtQ15(0x4000,buf); //square root of 2
      //uartWriteByteArray ( UART_USB ,buf ,len);
      //n1++;
      sample++;
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2

      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/1)
         ;
   }
}
