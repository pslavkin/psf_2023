#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
#include "fir_65_400_10000.h" 

#define INTERPOL_WIDTH     10
#define MAX_FFT_LENGTH     512
#define CONVOLUTION_LENGTH 512
#define sizeN 256


struct header_struct {
   char     pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   uint16_t M;
   uint16_t convLength;
   q15_t maxValue;
   uint32_t maxIndex;
   uint16_t maxPromIndex;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

struct header_struct header={"*header*",0,sizeN,1024,h_LENGTH,CONVOLUTION_LENGTH,0,0,0,"end*"};

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


float chordsF[]={329.63, 246.94, 196.00, 146.83, 110.00, 82.41};
int16_t chord,tune;

arm_rfft_instance_q15 S;
uint32_t magIndex   = 0;
uint16_t sample     = 0;

int calcFftLength(int N,int M) {
   int convLength=N+M-1,i;
   for(i=MAX_FFT_LENGTH;i>=convLength;i>>=1)
      ;
   return i<<1;
}
int sendStr            ( char A[],int N                                                              );
int sendBlock          ( q15_t A[],int N                                                             );
void findFirstLocalMax ( q15_t* magFft,int length,q15_t threshold,q15_t* maxValue,uint32_t* maxIndex );
void interpol          ( q15_t* magFft,uint16_t* maxIndex                                            );
void promVector        ( q15_t* promMagFft,q15_t* magFft,uint16_t length                             );
void ledManagement     ( uint16_t chord,uint16_t tune                                                );
void findChord         ( uint32_t promIndex,uint16_t* chord, uint16_t* tune                          );

q15_t   fftMag    [ MAX_FFT_LENGTH+2        ];
q15_t   fftPromMag[ MAX_FFT_LENGTH          ]={0};
int16_t adc       [ sizeN*10+h_LENGTH-1     ];
q15_t   xOver     [ sizeN*10+2*(h_LENGTH-1) ];
q15_t   x         [ MAX_FFT_LENGTH          ]={0};

int main ( void ) {
   for(int i=0;i<sizeof(x)/sizeof(x[0]);i++) {
      x[i] = 0;
   }
   boardConfig        (                          );
   uartConfig         ( UART_USB, 460800         );
   uartWriteByteArray ( UART_USB ,"holahola" ,8);
   adcConfig          ( ADC_ENABLE               );
   cyclesCounterInit  ( EDU_CIAA_NXP_CLOCK_SPEED );

//   for(;sample<header.convLength;sample++)
//      adc[sample]=0;
   while(1) {
      cyclesCounterReset();
      if ( sample<header.N)  {                                                   // si es el ultimo
         uartWriteByteArray ( UART_USB ,(uint8_t* )&adc[sample]    ,sizeof(adc[0]) );// envia el sample ANTERIOR
         uartWriteByteArray ( UART_USB ,(uint8_t* )&fftPromMag[magIndex-header.N/2+sample] ,sizeof(fftMag[0])); // envia la fft del sample ANTERIO
      }
      adc[sample] = ((int16_t )adcRead(CH1)-512)<<6;
      if ( ++sample==(header.N*10+h_LENGTH-1) ) {                                                   // si es el ultimo
      //   arm_conv_fast_q15 ( adc,header.N*10+h_LENGTH-1,h,h_LENGTH,xOver );
      //   for(int i=0;i<header.N;i++){
      //      adc[i]=xOver[i*10+h_LENGTH-1];
      //      x[i]=adc[i];
      //   }

         //arm_rfft_init_q15 ( &S ,header.convLength ,0 ,1 );
         //arm_rfft_q15 ( &S ,x ,fftMag );

         //for(int i=0;i<(header.convLength+2);i++){
         //   fftMag[i]<<=6;
         //}
         //arm_cmplx_mag_squared_q15 ( fftMag ,fftMag ,header.convLength/2+1 );
         //promVector(fftPromMag,fftMag,header.convLength/2);
         //arm_max_q15               ( fftPromMag ,header.convLength/2+1 ,&header.maxValue ,&header.maxIndex );
         //findFirstLocalMax(fftPromMag,header.convLength/2,header.maxValue/2,&header.maxValue ,&header.maxIndex);
         //header.maxPromIndex=header.maxIndex;
         //interpol(fftPromMag,&header.maxPromIndex);
         //magIndex=header.maxIndex>=(header.N/2)?header.maxIndex:(header.N/2);
         //findChord( header.maxPromIndex,&chord,&tune);
         //ledManagement(chord,tune );
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         header.id++;
         sample = 0;                                                                 // arranca de nuevo
      }
      while(cyclesCounterRead()< EDU_CIAA_NXP_CLOCK_SPEED/(header.fs*10)) // el clk de la CIAA es 204000000
         ;
   }
}
int sendStr           ( char A[],int N )
{
   uartWriteByteArray ( UART_USB ,A ,N );
}
int sendBlock         ( q15_t A[],int N     )
{
   uartWriteByteArray ( UART_USB ,(uint8_t* )A ,2*N );
}
void findFirstLocalMax(q15_t* magFft,int length,q15_t threshold,q15_t* maxValue,uint32_t* maxIndex)
{
   int i=(header.convLength*60)/header.fs;
   *maxValue=0;
   *maxIndex=0;
   length-=INTERPOL_WIDTH; //para interpol
   if(threshold<5) threshold=5;
   for (;i<length;i++)
      if(magFft[i]>threshold) 
         break;
   if(i>=length) return;
   for (;i<length;i++)
      if(magFft[i]>=*maxValue) {
            *maxValue=magFft[i];
            *maxIndex=i;
      }
      else
         break;
}
void interpol(q15_t* magFft,uint16_t* maxIndex)
{
   q15_t interpolF [ 2*INTERPOL_WIDTH+1 ];
   uint32_t f=0;
   uint32_t sum=0;

   for (int i=0;i<(2*INTERPOL_WIDTH+1);i++) {
      interpolF[i]=magFft[*maxIndex-INTERPOL_WIDTH+i];
      sum+=interpolF[i];
      f += interpolF[i]*(*maxIndex-INTERPOL_WIDTH+i);
   }
   *maxIndex=(f*2*INTERPOL_WIDTH)/sum; //TODO ojo que segn parece no hay que multiplicar por 2
}
void promVector(q15_t* promMagFft,q15_t* magFft,uint16_t length)
{
   for (int i=0;i<length;i++)
      promMagFft[i]=(promMagFft[i]+magFft[i])/2;
}

void findChord(uint32_t promIndex,uint16_t* chord, uint16_t* tune)
{
#define MARGIN 20
#define TUNE 0.2
   float frec = (header.fs*(promIndex/20.0))/header.convLength;
   *chord = 7;
   *tune  = 3;
   for(int i=0;i<6;i++){
      if((chordsF[i]+MARGIN)>frec && (chordsF[i]-MARGIN)<frec) {
         *chord=i;
         if(frec>(chordsF[i]+TUNE))
            *tune=2;
         else if(frec<(chordsF[i]-TUNE))
            *tune=0;
         else 
            *tune=1;
         break;
      }
   }
}
void ledManagement(uint16_t chord,uint16_t tune)
{
   gpioWrite(LEDR,0);
   gpioWrite(LEDB,0);
   gpioWrite(LEDG,0);
   gpioWrite(LED1,0);
   gpioWrite(LED2,0);
   gpioWrite(LED3,0);
   return;
   switch (tune){
      case 0:
         gpioWrite(LED1,1);
         break;
      case 1:
         gpioWrite(LED2,1);
         break;
      case 2:
         gpioWrite(LED3,1);
         break;
   }
   switch (chord){
      case 0:
         gpioWrite(LEDR,1);
         break;
      case 1:
         gpioWrite(LEDG,1);
         break;
      case 2:
         gpioWrite(LEDB,1);
         break;
      case 3:
         gpioWrite(LEDR,1);
         gpioWrite(LEDG,1);
         break;
      case 4:
         gpioWrite(LEDR,1);
         gpioWrite(LEDB,1);
         break;
      case 5:
         gpioWrite(LEDB,1);
         gpioWrite(LEDG,1);
         break;
   }
}
