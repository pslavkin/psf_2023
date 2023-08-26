#include "sapi.h"
#include "arm_math.h"
#include "arm_const_structs.h"
//##include "fir_500.h" 
#include "fir_65_400_10000.h" 

#define INTERPOL_WIDTH 10 //ojo que no puede ser muy grande porque no se consideraron los bordes
#define FFT_LENGTH     512
#define OVERSAMPLE     10 //ojo que tiene que conincidir con el disenio del filtro

struct header_struct {
   char     pre[8];
   uint32_t id;
   uint16_t N;
   uint16_t fs ;
   q15_t maxValue ;
   uint32_t maxIndex ;
   char     pos[4];
} __attribute__ ((packed)); //importante para que no paddee

int16_t chord,tune;
float chordsF[]={329.63, 246.94, 196.00, 146.83, 110.00, 82.41};

struct header_struct header={"*header*",0,128,1000,0,0,"end*"};
void ledManagement      ( uint16_t chord            ,uint16_t tune                   );
void init_cfft_instance ( arm_cfft_instance_q15* CS ,int length                      );
void noAgc              ( int16_t* adc              ,uint16_t len                    );
void agc                ( int16_t* adc              ,uint16_t len                    );
void findChord          ( uint32_t index            ,uint16_t* chord ,uint16_t* tune );
void interpol           ( q15_t* magFft             ,uint32_t* maxIndex              );


int main ( void ) {
   int16_t  *adc = (int16_t*)0x10080000;//[ header.N*OVERSAMPLE+h_LENGTH-1] 
   int16_t  *fft = (int16_t*)0x20000000;//[ header.N*OVERSAMPLE+h_LENGTH-1]  
   arm_cfft_instance_q15 CS;
   q15_t fftAbs    [ FFT_LENGTH ];
   q15_t fftAbsProm[ FFT_LENGTH ];
   int16_t  x   [ header.N   ];
   int16_t  sample      = 0;
   int16_t  downSample  = 0;
   q15_t    maxAdc      = 0;
   uint32_t maxAdcIndex = 0;

   boardConfig       (                          );
   uartConfig        ( UART_USB ,460800         );
   adcConfig         ( ADC_ENABLE               );
   cyclesCounterInit ( EDU_CIAA_NXP_CLOCK_SPEED );

   while(1) {
      cyclesCounterReset();

//---------------sampleado y offset--------------------------
      adc[sample] = adcRead(CH1)-505; //ajusto el offset 
      
//---------------envio datos a rate de downsample--------------------------
      if(sample<header.N) {
         uartWriteByteArray ( UART_USB ,(uint8_t* )&x     [sample] ,sizeof(x[0]) );
         uartWriteByteArray ( UART_USB ,(uint8_t* )&fftAbs[sample] ,sizeof(fftAbs[0]) );
      }

//---------------sampleo a oversampling--------------------------
      sample++;
      if ( sample>=(header.N*OVERSAMPLE) ) {
//---------------escalado automatico--------------------------
//         noAgc(adc,header.N*OVERSAMPLE);
         agc(adc,header.N*OVERSAMPLE);

////---------------filtrado antialias en digitial--------------------------
         arm_conv_fast_q15  ( adc,header.N*OVERSAMPLE,h,h_LENGTH,fft); //se podria reutilizar el adc en vez de y como salida
//         arm_conv_q15  ( adc,header.N*OVERSAMPLE,h,h_LENGTH,fft); //se podria reutilizar el adc en vez de y como salida

////---------------escalado automatico a posteriori del filtrado--------------------------
         agc(fft,header.N*OVERSAMPLE+h_LENGTH-1);
//
////---------------downsampling--------------------------
         for(int i=0;i<header.N;i++){
            x[i]       = fft[i*OVERSAMPLE+(h_LENGTH-1)/2];//arranca desde la zona valida
         }
//---------------preparo vector para hacer fft--------------------------
         int i;
         for(i=0;i<header.N;i++){
            fft[2*i+0] = x[i]; //antes de calcular divido por dos para que no
                                  //salga de q15
            fft[2*i+1] = 0;
         }
////---------------zero padding--------------------------
         for(;i<FFT_LENGTH;i++){
            fft[2*i+0] = 0;
            fft[2*i+1] = 0;
         }

////------------TRANSFORMADA------------------
         init_cfft_instance ( &CS,FFT_LENGTH);
         arm_cfft_q15       ( &CS ,fft ,0 ,1 );

////------------MAGNITUD------------------
         arm_cmplx_mag_squared_q15 ( fft ,fftAbs ,FFT_LENGTH);
//
////------------Promedio de 2 espectros------------------
         for(int i=0;i<FFT_LENGTH;i++){
            fftAbsProm[i] = fftAbsProm[i]/2 + fftAbs[i]/2;
         }
////------------opcional SIN Promedio (queda mas fluido)------------------
//         for(int i=0;i<FFT_LENGTH;i++){
//            fftAbsProm[i] = fftAbs[i];
//         }
            
////------------BUSCO EL MAXIMO------------------
         arm_max_q15 ( fftAbsProm ,FFT_LENGTH ,&header.maxValue ,&header.maxIndex );
         header.maxValue*=8*FFT_LENGTH/header.N;//>>=2;//<<=3;
////------------Centro de masas------------------
//      header.maxIndex*=1000;
      interpol(fftAbsProm,&header.maxIndex); //TODO ojo! aca el max index sale x1000
//
//
////------------Downsample ABS (uso internamente FFT_LENGTH pero muestro solo N------------------
         int down=FFT_LENGTH/header.N;
         for(int i=0;i<header.N;i++) {
            int sum=0;
            for(int j=0;j<down;j++)
               sum+=fftAbsProm[i*down+j];
            fftAbs[i] = sum*8*FFT_LENGTH/(header.N*down);
         }


////------------BUSCO CUERDA------------------
         findChord(header.maxIndex,&chord,&tune);
//
////------------ENCIENDO LEDS------------------
         ledManagement(chord,tune );
//
         uartWriteByteArray ( UART_USB ,(uint8_t*)&header ,sizeof(struct header_struct ));
         header.id++;
         sample     = 0;
         downSample = 0;
         adcRead(CH1); //why?? hay algun efecto minimo en el 1er sample.. puede ser por el blinkeo de los leds o algo que me corre 10 puntos el primer sample. Con esto se resuelve.. habria que investigar el problema en detalle
      }
      //---------------over sampling--------------------------
      while(cyclesCounterRead()< (EDU_CIAA_NXP_CLOCK_SPEED/(header.fs*OVERSAMPLE))) // el clk de la CIAA es 204000000
         ;
   }
}

void ledManagement(uint16_t chord,uint16_t tune)
{
   gpioWrite(LED1,tune&0x01?1:0);
   gpioWrite(LED2,tune&0x02?1:0);
   gpioWrite(LED3,tune&0x04?1:0);
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
      default:
         gpioWrite(LEDR,0);
         gpioWrite(LEDB,0);
         gpioToggle(LEDG);
         break;
   }
}

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

void noAgc(int16_t* adc,uint16_t len)
{
   for(int i=0;i<len;i++)
      adc[i]<<=6;
   return;
}
void agc(int16_t* adc,uint16_t len)
{
   int max=0;
   int i,gainFactor;
   for(i=0;i<len;i++) {
      int abs=adc[i]>0?adc[i]:-adc[i];
      if(abs>max)
         max=abs;
   }
   gainFactor=0x8000/max;
   for(i=0;i<len;i++) {
      adc[i]*=gainFactor;
   }
   return;
}

void findChord(uint32_t index,uint16_t* chord, uint16_t* tune)
{
#define MARGIN  10.00*1000
#define TUNE     0.25*1000
#define MID_TUNE 2.00*1000

   float frec = (header.fs*index)/FFT_LENGTH;
   *chord = 7;
   *tune  = 0;
   for(int i=0;i<6;i++){
      if(frec>(chordsF[i]*1000-MARGIN) && frec<(chordsF[i]*1000+MARGIN)) {
         *chord=i;
         if(frec>(chordsF[i]*1000+TUNE))
            *tune=0x04;
         else 
            if(frec<(chordsF[i]*1000-TUNE))
               *tune=0x01;

         if(frec>(chordsF[i]*1000-MID_TUNE) && frec<(chordsF[i]*1000+MID_TUNE))
            (*tune)|=0x02;
         break;
      }
   }
}

void interpol(q15_t* magFft,uint32_t* maxIndex)
{
   int32_t interpolF;
   int32_t f=0;
   int32_t sum=0;

   for (int i=0;i<(2*INTERPOL_WIDTH+1);i++) {
      interpolF=magFft[*maxIndex-INTERPOL_WIDTH+i];
      sum+=interpolF;
      f += interpolF*(*maxIndex-INTERPOL_WIDTH+i);
   }
   
   *maxIndex=(f*1000)/sum;
   if(*maxIndex>((FFT_LENGTH/2)*1000))
      *maxIndex=(FFT_LENGTH/2)*1000;
}
