#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "fir_65_400_10000.h" 

#define BITS    10   // cantidad de bits usado para cuantizar

struct header_struct {
   char     pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

struct header_struct header={"*header*",0,200,1000,"end*"};

int max(int a, int b)
{
   return a>b?a:b;
}

int main ( void ) {
   uint16_t sample     = 0;
   uint16_t overSample = 1;
   int garbageOffset = (h_LENGTH+header.N*overSample-1)/2-(header.N*overSample)/2;
   int16_t adc   [ header.N*overSample            ];
   int16_t y     [ header.N*overSample+h_LENGTH-1 ];

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();

      if(sample<header.N)
         uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample] ,sizeof(adc[0]) );
      adc[sample]          = (((int16_t )adcRead(CH1)-512)>>(10-BITS))<<(6+10-BITS); // PISA el sample que se acaba de mandar con una nueva muestra

      //---------------over sampling--------------------------
      if ( ++sample>=header.N*overSample ) {
         gpioToggle ( LEDR );                         // este led blinkea a fs/N

         //---------------filtrado antialias en digitial--------------------------
         //ojo que para fast creo que N debe ser potencia de 2
         //arm_conv_fast_q15  ( adc,header.N*overSample,h,h_LENGTH,y);
         arm_conv_q15  ( adc,header.N*overSample,h,h_LENGTH,y);

         //---------------downsampling--------------------------
         for(int i=0;i<header.N;i++){
            //adc[i]=y[i*overSample+garbageOffset];
            //notar que pasa si me quedo con la parte inicial de la conversion
            adc[i]=y[i*overSample+0];
         }

         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         header.id++;
         sample = 0;
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2

      //---------------over sampling--------------------------
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/(header.fs*overSample)) // el clk de la CIAA es 204000000
         ;
   }
}
