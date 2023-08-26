#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "fir.h" 
//#include "fir_clase6.h"
//#include "fir_bandpass.h"
//#include "fir_band_pass_2.h"

#define BITS    10   // cantidad de bits usado para cuantizar

uint32_t tick   = 0   ;
uint16_t tone   = 100 ;
uint16_t B      = 2500;
uint16_t sweept = 5;
 int16_t offset = 512;
 int16_t zero = 0;

struct header_struct {
   char     pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint16_t hLength ;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

struct header_struct header={"*header*",0,128,10000,h_LENGTH,"end*"};

void trigger(int16_t threshold)/*{{{*/
{
   while((adcRead(CH1)-512)>threshold)
      ;
   while((adcRead(CH1)-512)<threshold)
      ;
   return;
}/*}}}*/

int main ( void ) {
   uint16_t sample = 0;
   int16_t adc   [ header.N            ];
   int16_t y     [ h_LENGTH+header.N-1 ]; //

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   //dacConfig       ( DAC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();

      adc[sample]       = (((int16_t )adcRead(CH1)-512)>>(10-BITS))<<(6+10-BITS);          // PISA el sample que se acaba de mandar con una nueva muestra
      //float t=((tick%(sweept*header.fs))/(float)header.fs);
      //tick++;
      //dacWrite( DAC, 512*arm_sin_f32 (t*B/2*(t/sweept)*2*PI)+512); // sweept
      //dacWrite( DAC, 512*arm_sin_f32 (t*tone*2*PI)+512);       // tono
      if ( ++sample==header.N ) {
         gpioToggle ( LEDR );                         // este led blinkea a fs/N
         sample = 0;

//------------CONVOLUCION------------------
         arm_conv_q15       ( adc,header.N,h,h_LENGTH,y);
//         arm_conv_fast_q15  ( adc,header.N,h,h_LENGTH,y); //126+74-1

//------------ENVIO DE TRAMA------------------
         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         for (int i=0;i<(header.N+h_LENGTH-1 );i++) {
            uartWriteByteArray ( UART_USB ,(uint8_t* )(i<header.N?&adc[i]:&offset ),sizeof(adc[0]));
            uartWriteByteArray ( UART_USB ,(uint8_t* )(i<h_LENGTH?&h  [i]:&zero   ),sizeof(h[0])  );
            uartWriteByteArray ( UART_USB ,(uint8_t* )(           &y  [i]         ),sizeof(y[0])  );
         }
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
