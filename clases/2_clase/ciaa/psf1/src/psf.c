#include "sapi.h"
#include "arm_math.h"

#define DO  261.63
#define RE  293.66
#define MI  329.63
#define FA  349.23
#define SOL 392.00
#define LA  440.00
#define SI  493.88

uint32_t tick   = 0;
uint16_t tone   = 1000 ;
uint16_t B      = 4500;
uint16_t sweept = 10;

struct header_struct {
   char     pre[4];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   char     pos[4];
} header={"head",0,128,10000,"tail"};

void trigger(int16_t threshold)
{
   while((adcRead(CH1)-512)>threshold)
      ;
   while((adcRead(CH1)-512)<threshold)
      ;
   return;
}

uint16_t DOm(float t){
   return 512*0.4*arm_sin_f32 (2*PI*t*DO)+\
          512*0.2*arm_sin_f32 (2*PI*t*MI)+\
          512*0.3*arm_sin_f32 (2*PI*t*SOL)+512;
}

int main ( void ) {
   uint16_t sample = 0;
   int16_t adc [ header.N ];
   boardConfig (                  );
   uartConfig  ( UART_USB, 460800 );
   adcConfig   ( ADC_ENABLE       );
   dacConfig   ( DAC_ENABLE       );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );
   while(1) {
      cyclesCounterReset();
      adc[sample] = (int16_t )adcRead(CH1)-512;                     // va de -512 a 511
      uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample] ,sizeof(adc[0]) );
      //float t=((tick%(sweept*header.fs))/(float)header.fs);
      float t=tick/(float)header.fs;
      tick++;
     // dacWrite( DAC, DOm(t)); // acorde
      dacWrite( DAC, 512*arm_sin_f32 (t*B/2*(t/sweept)*2*PI)+512); // sweept
     // dacWrite( DAC, 512*arm_sin_f32 (t*tone*2*PI)+512);         // tono
      if ( ++sample==header.N ) {
         gpioToggle ( LEDR ); // este led blinkea a fs/N
         sample = 0;
//         trigger(2);
         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(header ));
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                             // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
