#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "fir.h" 
//#include "fir_500.h" 
//#include "fir_clase6.h" //126
//#include "fir_band_pass_2.h" //315
//#include "fir_bandpass.h" //199
//#include "stop_band_700.h"

//N? / 126+N-1=256 => 387
//

#define BITS    10   // cantidad de bits usado para cuantizar

#define CUTFREC 2000 // frec de corte para filtrar en frec

struct header_struct {
   char     pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint16_t cutFrec ;
   uint16_t M ;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

struct header_struct header={"*header*",0,1027,10000,CUTFREC,h_LENGTH,"end*"};

void trigger(int16_t threshold)/*{{{*/
{
   while((adcRead(CH1)-512)>threshold)
      ;
   while((adcRead(CH1)-512)<threshold)
      ;
   return;
}/*}}}*/
void init_cfft_instance(arm_cfft_instance_q15* CS,int length)/*{{{*/
{
   switch(length){
      case 16:
         *CS=arm_cfft_sR_q15_len16;
         break;
      case 32:
         *CS=arm_cfft_sR_q15_len32;
         break;
      case 64:
         *CS=arm_cfft_sR_q15_len64;
         break;
      case 128:
         *CS=arm_cfft_sR_q15_len128;
         break;
      case 256:
         *CS=arm_cfft_sR_q15_len256;
         break;
      case 512:
         *CS=arm_cfft_sR_q15_len512;
         break;
      case 1024:
         *CS=arm_cfft_sR_q15_len1024;
         break;
      case 2048:
         *CS=arm_cfft_sR_q15_len2048;
         break;
      case 4096:
         *CS=arm_cfft_sR_q15_len4096;
         break;
      default:
         *CS=arm_cfft_sR_q15_len128;
   }
   return;
}/*}}}*/

int main ( void ) {
   uint16_t sample = 0;
   arm_cfft_instance_q15 CS;
   q15_t fftInOut[ ( header.N+h_LENGTH-1 )*2 ];//
   q15_t fftAbs  [ ( header.N+h_LENGTH-1 )*1 ]; //
   int16_t adc   [ ( header.N+h_LENGTH-1 )*1 ];

   for(sample=header.N;sample<(header.N+h_LENGTH-1);sample++){ //relleno con ceros M-1 puntos
      adc[sample]          = 0; //como son automaticas no se inicializan en cero, podrian definirse globales para que arranquen en cero
      fftInOut[sample*2]   = 0;
      fftInOut[sample*2+1] = 0;                                                            // parte imaginaria cero
   }

//lo puedo calcular aqui o lo tomo desde pytho previamente cocinado
//   arm_cmplx_mag_squared_q15 ( H ,HAbs ,(header.N+h_LENGTH-1 ));

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   //dacConfig       ( DAC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();

      adc[sample]          = (((int16_t )adcRead(CH1)-512)>>(10-BITS))<<(6+10-BITS); // PISA el sample que se acaba de mandar con una nueva muestra
      fftInOut[sample*2]   = adc[sample];                                            // copia del adc porque la fft corrompe el arreglo de entrada
      fftInOut[sample*2+1] = 0;                                                      // parte imaginaria cero

      if ( ++sample>=header.N ) {
         gpioToggle ( LEDR );                         // este led blinkea a fs/N

//------------TRANSFORMADA------------------
         init_cfft_instance ( &CS,(header.N+h_LENGTH-1)); //512. 256 esto tienen que ser power of 2
         arm_cfft_q15       ( &CS ,fftInOut ,0 ,1      ) ;

//------------MAGNITUD------------------
         arm_cmplx_mag_squared_q15 ( fftInOut ,fftAbs ,(header.N+h_LENGTH-1 ));

//------------FILTRADO MULTIPLICANDO ESPECTROS------------------
         arm_mult_q15 ( fftAbs,HAbs ,fftAbs ,(header.N+h_LENGTH-1));

         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));

         for (sample=0; sample<(header.N+h_LENGTH-1);sample++ ) {
            uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]      ,sizeof(adc[0]) );     // envia el sample ANTERIOR
            uartWriteByteArray ( UART_USB ,(uint8_t* )&fftAbs[sample*1] ,sizeof(fftInOut[0])); // envia la fft del sample ANTERIO
         }
         sample = 0;
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
