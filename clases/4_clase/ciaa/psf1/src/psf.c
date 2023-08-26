#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"

#define BITS    10   // cantidad de bits usado para cuantizar
#define CUTFREC 500 // frec de corte para filtrar en frec

uint32_t tick   = 0   ;
uint16_t tone   = 100 ;
uint16_t B      = 2500;
uint16_t sweept = 5;

struct header_struct {
   char     pre[4];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint16_t cutFrec ;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

struct header_struct header={"head",0,128,10000,CUTFREC,"tail"};

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
   q15_t fftInOut[ header.N *2 ];//
   int16_t adc   [ header.N    ];

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   //dacConfig       ( DAC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();

      uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]        ,sizeof(adc[0]) );     // envia el sample ANTERIOR
      uartWriteByteArray ( UART_USB ,(uint8_t* )&fftInOut[sample*2] ,sizeof(fftInOut[0])); // envia la fft del sample ANTERIO
      adc[sample]       = (((int16_t )adcRead(CH1)-512)>>(10-BITS))<<(6+10-BITS);          // PISA el sample que se acaba de mandar con una nueva muestra
      fftInOut[sample*2]   = adc[sample];                                                  // copia del adc porque la fft corrompe el arreglo de entrada
      fftInOut[sample*2+1] = 0;                                                            // parte imaginaria cero
      //float t=((tick%(sweept*header.fs))/(float)header.fs);
      //tick++;
      //dacWrite( DAC, 512*arm_sin_f32 (t*B/2*(t/sweept)*2*PI)+512); // sweept
      //dacWrite( DAC, 512*arm_sin_f32 (t*tone*2*PI)+512);       // tono
      if ( ++sample==header.N ) {
         gpioToggle ( LEDR );                         // este led blinkea a fs/N
         sample = 0;

//------------TRANSFORMADA------------------
         init_cfft_instance ( &CS,header.N        );
         arm_cfft_q15       ( &CS ,fftInOut ,0 ,1 ); //0 directa, 1 inversa

// FILTRADO BASICO RECORTANDO EN FREC
//       fftInOut[0]=0; //elimino la continua
//       fftInOut[1]=0;
//       int cutBin=CUTFREC/(header.fs/header.N); //defino el n donde comenzar a cortar
//       for(int i=0;i<=(header.N/2);i++) {        //solo recorro la mitad, porque la otra mitad es compleja conjugada asi que borro de los 2 lados
//          if(i>=cutBin ) {
//             fftInOut[i*2]                  = 0; //borro bin parte real
//             fftInOut[i*2+1]                = 0; //borro bin parte compleja
//             fftInOut[(header.N-1)*2-i*2]   = 0; //lo mismo pero de atras para adelante
//             fftInOut[(header.N-1)*2-i*2+1] = 0;
//          }
//       }
//---------ANTI transformada---------------------
         init_cfft_instance ( &CS,header.N        );
         arm_cfft_q15       ( &CS ,fftInOut ,1 ,1 );

         header.id++;
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));

         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      gpioToggle ( LED1 );                                           // este led blinkea a fs/2
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/header.fs) // el clk de la CIAA es 204000000
         ;
   }
}
