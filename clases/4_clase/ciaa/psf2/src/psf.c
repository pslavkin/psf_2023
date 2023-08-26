#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"

#define BITS 10                     // cantidad de bits usado para cuantizar

struct header_struct {
   char     pre[4];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   char     pos[4];
} __attribute__ ((packed));

struct header_struct header={"head",0,128,4000,"tail"}; //atencion que enviando todo el tiempo 3 floatas, no me da para ir mas alla de 4k

void trigger(int16_t threshold)
{
   while((adcRead(CH1)-512)>threshold)
      ;
   while((adcRead(CH1)-512)<threshold)
      ;
   return;
}
void clearFloatBuf(float *b,uint16_t len)
{
   while(len--)
      b[len]=0.0;
}

int main ( void ) {
   uint16_t sample = 0;
   float coorIn [ header.N      ];// guarda copia de samples en Q15 como in para la fft.La fft corrompe los datos de la entrada!
   float corrOut[ header.N *2   ]; // salida de la fft
   float adc    [ header.N      ];
   float signal [ header.N      ];
  
   int i;
   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );
   clearFloatBuf(signal,header.N);
   for(i=0;i<10;i++) {
      signal[i]=-i/10.0;
   }
   for(;i<20;i++) {
      signal[i]=(i-10)/10.0;
   }

   while(1) {
      cyclesCounterReset();
      int16_t adcRaw;
      uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]      ,sizeof(adc[0]) );   // envia el sample ANTERIOR
      uartWriteByteArray ( UART_USB ,(uint8_t* )&corrOut[sample*2]   ,sizeof(corrOut[0])); // envia la fft del sample ANTERIO
      uartWriteByteArray ( UART_USB ,(uint8_t* )&corrOut[sample*2+1] ,sizeof(corrOut[0])); // envia la fft del sample ANTERIO
      adcRaw        = adcRead(CH1)-512;
      adc[sample]   = adcRaw/512.0;             // PISA el sample que se acaba de mandar con una nueva muestra
      coorIn[sample] = adcRaw;
      if ( ++sample==header.N ) {
         gpioToggle ( LEDR );                   // este led blinkea a fs/N

         clearFloatBuf ( corrOut,2*header.N );
         arm_correlate_f32 ( signal,header.N,adc ,header.N,corrOut  );
         // trigger(2);
         sample = 0;
         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
