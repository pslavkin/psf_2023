#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"

#define BITS 10                     // cantidad de bits usado para cuantizar
uint32_t tick   = 0   ;
uint16_t tone   = 100 ;
uint16_t B      = 2500;

struct header_struct {
   char     pre[4];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint32_t maxIndex; // indexador de maxima energia por cada fft
   q15_t maxValue;    // maximo valor de energia del bin por cada fft
   char     pos[4];
} __attribute__ ((packed));

struct header_struct header={"head",0,128,10000,0,0,"tail"};

void trigger(int16_t threshold)
{
   while((adcRead(CH1)-512)>threshold)
      ;
   while((adcRead(CH1)-512)<threshold)
      ;
   return;
}

int main ( void ) {
   uint16_t sample = 0;

   arm_rfft_instance_f32 S;
   arm_cfft_radix4_instance_f32  cS;
   float fftIn [ header.N      ]; // guarda copia de samples en Q15 como in para la fft.La fft corrompe los datos de la entrada!
   float fftOut[ header.N *2   ]; // salida de la fft
   float adc [ header.N        ];

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();
      float aux=0;
      int16_t adcRaw;
      uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]        ,sizeof(adc[0]) );   // envia el sample ANTERIOR
      uartWriteByteArray ( UART_USB ,(uint8_t* )&fftOut[sample*2]   ,sizeof(fftOut[0])); // envia la fft del sample ANTERIO
      uartWriteByteArray ( UART_USB ,(uint8_t* )&fftOut[sample*2+1] ,sizeof(fftOut[0])); // envia la fft del sample ANTERIO
      adcRaw        = adcRead(CH1)-512;
      adc[sample]   = adcRaw/512.0;            // PISA el sample que se acaba de mandar con una nueva muestra
      fftIn[sample] = adcRaw;                                                      // copia del adc porque la fft corrompe el arreglo de entrada
      if ( ++sample==header.N ) {
         gpioToggle ( LEDR );                         // este led blinkea a fs/N
         sample = 0;
         arm_rfft_init_f32 ( &S ,&cS   ,header.N ,0 ,1 ); // inicializa una estructira que usa la funcion fft para procesar los datos. Notar el /2 para el largo
         arm_rfft_f32      ( &S ,fftIn ,fftOut         ); // por fin.. ejecuta la rfft REAL fft
         //      trigger(2);
         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
