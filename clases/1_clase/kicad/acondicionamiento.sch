EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L acondicionamiento-rescue:R R2
U 1 1 5E9F21B2
P 5900 2450
F 0 "R2" H 6050 2400 50  0000 C CNN
F 1 "100k" H 6050 2500 50  0000 C CNN
F 2 "" V 5830 2450 50  0000 C CNN
F 3 "" H 5900 2450 50  0000 C CNN
	1    5900 2450
	1    0    0    -1  
$EndComp
$Comp
L power:GNDA #PWR04
U 1 1 5E9F21FA
P 5900 2850
F 0 "#PWR04" H 5900 2600 50  0001 C CNN
F 1 "GNDA" H 5900 2700 50  0000 C CNN
F 2 "" H 5900 2850 50  0000 C CNN
F 3 "" H 5900 2850 50  0000 C CNN
	1    5900 2850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5900 2150 5900 2250
Connection ~ 5900 2250
$Comp
L acondicionamiento-rescue:C C2
U 1 1 5E9F228D
P 6650 2450
F 0 "C2" H 6675 2550 50  0000 L CNN
F 1 "33nF" H 6675 2350 50  0000 L CNN
F 2 "" H 6688 2300 50  0000 C CNN
F 3 "" H 6650 2450 50  0000 C CNN
	1    6650 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	6500 2250 6650 2250
Wire Wire Line
	6650 2250 6650 2300
$Comp
L power:GNDA #PWR05
U 1 1 5E9F22FD
P 6650 2850
F 0 "#PWR05" H 6650 2600 50  0001 C CNN
F 1 "GNDA" H 6650 2700 50  0000 C CNN
F 2 "" H 6650 2850 50  0000 C CNN
F 3 "" H 6650 2850 50  0000 C CNN
	1    6650 2850
	1    0    0    -1  
$EndComp
Connection ~ 6650 2250
Text HLabel 6950 2250 2    60   Input ~ 0
ADC1
Text HLabel 5000 2250 0    60   Input ~ 0
AudioL
Text Notes 4300 2150 0    60   ~ 0
+-1.65 Vac MAX
Text Notes 7050 2450 0    60   ~ 0
0-3.3Vdc\n
$Comp
L acondicionamiento-rescue:R R1
U 1 1 5E9F2549
P 5900 2000
F 0 "R1" H 6050 1950 50  0000 C CNN
F 1 "100k" H 6050 2050 50  0000 C CNN
F 2 "" V 5830 2000 50  0000 C CNN
F 3 "" H 5900 2000 50  0000 C CNN
	1    5900 2000
	1    0    0    -1  
$EndComp
$Comp
L acondicionamiento-rescue:R R3
U 1 1 5E9F2580
P 6350 2250
F 0 "R3" V 6250 2250 50  0000 C CNN
F 1 "1k" V 6450 2250 50  0000 C CNN
F 2 "" V 6280 2250 50  0000 C CNN
F 3 "" H 6350 2250 50  0000 C CNN
	1    6350 2250
	0    1    1    0   
$EndComp
Text Notes 4600 2050 0    60   ~ 0
0-20Khz\n
Text Notes 7050 2600 0    60   ~ 0
0-5Khz\n
$Comp
L acondicionamiento-rescue:C C1
U 1 1 5E9F278E
P 5550 2250
F 0 "C1" V 5700 2200 50  0000 L CNN
F 1 ">1uF" V 5350 2150 50  0000 L CNN
F 2 "" H 5588 2100 50  0000 C CNN
F 3 "" H 5550 2250 50  0000 C CNN
	1    5550 2250
	0    1    1    0   
$EndComp
Text Notes 6050 1850 0    60   ~ 0
fc=1/(2*pi*R*C)
Text Label 5900 2250 0    60   ~ 0
1.65v
Wire Wire Line
	5900 1850 5900 1650
Wire Wire Line
	5900 2600 5900 2850
Wire Wire Line
	6650 2600 6650 2850
Text Notes 5250 1950 0    60   ~ 0
Desacople
Wire Notes Line
	4300 1650 4300 2800
Wire Notes Line
	4300 2800 5100 2800
Wire Notes Line
	5100 2800 5100 1650
Wire Notes Line
	5100 1650 4300 1650
Text Notes 4350 1750 0    60   ~ 0
PC/Mobil/etc
Wire Notes Line
	6850 1650 6850 2800
Wire Notes Line
	6850 2800 7600 2800
Wire Notes Line
	7600 2800 7600 1650
Wire Notes Line
	7600 1650 6850 1650
Text Notes 7150 1750 0    60   ~ 0
CIAA
Wire Wire Line
	5900 2250 5900 2300
Wire Wire Line
	5900 2250 6200 2250
Wire Wire Line
	6650 2250 6950 2250
$Comp
L power:VDDA #PWR?
U 1 1 5EADD8C7
P 5900 1650
F 0 "#PWR?" H 5900 1500 50  0001 C CNN
F 1 "VDDA" H 5917 1823 50  0000 C CNN
F 2 "" H 5900 1650 50  0001 C CNN
F 3 "" H 5900 1650 50  0001 C CNN
	1    5900 1650
	1    0    0    -1  
$EndComp
Text Notes 6450 2550 2    60   ~ 0
FAA
Wire Wire Line
	5700 2250 5750 2250
$Comp
L acondicionamiento-rescue:R R?
U 1 1 5EB4A147
P 5600 4700
F 0 "R?" H 5750 4650 50  0000 C CNN
F 1 "100k" H 5750 4750 50  0000 C CNN
F 2 "" V 5530 4700 50  0000 C CNN
F 3 "" H 5600 4700 50  0000 C CNN
	1    5600 4700
	1    0    0    -1  
$EndComp
$Comp
L power:GNDA #PWR?
U 1 1 5EB4A14E
P 5600 5100
F 0 "#PWR?" H 5600 4850 50  0001 C CNN
F 1 "GNDA" H 5600 4950 50  0000 C CNN
F 2 "" H 5600 5100 50  0000 C CNN
F 3 "" H 5600 5100 50  0000 C CNN
	1    5600 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4400 5600 4500
Connection ~ 5600 4500
$Comp
L acondicionamiento-rescue:C C?
U 1 1 5EB4A156
P 6350 4700
F 0 "C?" H 6375 4800 50  0000 L CNN
F 1 "33nF" H 6375 4600 50  0000 L CNN
F 2 "" H 6388 4550 50  0000 C CNN
F 3 "" H 6350 4700 50  0000 C CNN
	1    6350 4700
	1    0    0    -1  
$EndComp
Wire Wire Line
	6200 4500 6350 4500
Wire Wire Line
	6350 4500 6350 4550
$Comp
L power:GNDA #PWR?
U 1 1 5EB4A15F
P 6350 5100
F 0 "#PWR?" H 6350 4850 50  0001 C CNN
F 1 "GNDA" H 6350 4950 50  0000 C CNN
F 2 "" H 6350 5100 50  0000 C CNN
F 3 "" H 6350 5100 50  0000 C CNN
	1    6350 5100
	1    0    0    -1  
$EndComp
Connection ~ 6350 4500
Text HLabel 6650 4500 2    60   Input ~ 0
ADC1
Text HLabel 4500 4500 0    60   Input ~ 0
Audio
Text Notes 4150 4400 0    60   ~ 0
+-1Vac
Text Notes 6750 4700 0    60   ~ 0
0-3.3Vdc\n
$Comp
L acondicionamiento-rescue:R R?
U 1 1 5EB4A16A
P 5600 4250
F 0 "R?" H 5750 4200 50  0000 C CNN
F 1 "100k" H 5750 4300 50  0000 C CNN
F 2 "" V 5530 4250 50  0000 C CNN
F 3 "" H 5600 4250 50  0000 C CNN
	1    5600 4250
	1    0    0    -1  
$EndComp
$Comp
L acondicionamiento-rescue:R R?
U 1 1 5EB4A171
P 6050 4500
F 0 "R?" V 5950 4500 50  0000 C CNN
F 1 "1k" V 6150 4500 50  0000 C CNN
F 2 "" V 5980 4500 50  0000 C CNN
F 3 "" H 6050 4500 50  0000 C CNN
	1    6050 4500
	0    1    1    0   
$EndComp
Text Notes 4100 4300 0    60   ~ 0
0-100Khz\n
Text Notes 6750 4850 0    60   ~ 0
0-5Khz\n
$Comp
L acondicionamiento-rescue:C C?
U 1 1 5EB4A17A
P 5250 4500
F 0 "C?" V 5400 4450 50  0000 L CNN
F 1 ">1uF" V 5050 4400 50  0000 L CNN
F 2 "" H 5288 4350 50  0000 C CNN
F 3 "" H 5250 4500 50  0000 C CNN
	1    5250 4500
	0    1    1    0   
$EndComp
Text Notes 5750 4100 0    60   ~ 0
fc=1/(2*pi*R*C)
Text Label 5600 4500 0    60   ~ 0
1.65v
$Comp
L acondicionamiento-rescue:D D?
U 1 1 5EB4A183
P 4900 4350
F 0 "D?" H 4900 4450 50  0000 C CNN
F 1 "D" H 4900 4250 50  0000 C CNN
F 2 "" H 4900 4350 50  0000 C CNN
F 3 "" H 4900 4350 50  0000 C CNN
	1    4900 4350
	0    1    1    0   
$EndComp
$Comp
L acondicionamiento-rescue:D D?
U 1 1 5EB4A18A
P 4900 4050
F 0 "D?" H 4900 4150 50  0000 C CNN
F 1 "D" H 4900 3950 50  0000 C CNN
F 2 "" H 4900 4050 50  0000 C CNN
F 3 "" H 4900 4050 50  0000 C CNN
	1    4900 4050
	0    1    1    0   
$EndComp
$Comp
L acondicionamiento-rescue:D D?
U 1 1 5EB4A191
P 4900 4650
F 0 "D?" H 4900 4750 50  0000 C CNN
F 1 "D" H 4900 4550 50  0000 C CNN
F 2 "" H 4900 4650 50  0000 C CNN
F 3 "" H 4900 4650 50  0000 C CNN
	1    4900 4650
	0    1    1    0   
$EndComp
$Comp
L acondicionamiento-rescue:D D?
U 1 1 5EB4A198
P 4900 4950
F 0 "D?" H 4900 5050 50  0000 C CNN
F 1 "D" H 4900 4850 50  0000 C CNN
F 2 "" H 4900 4950 50  0000 C CNN
F 3 "" H 4900 4950 50  0000 C CNN
	1    4900 4950
	0    1    1    0   
$EndComp
Connection ~ 4900 4500
Wire Wire Line
	5600 4100 5600 3900
$Comp
L power:GNDA #PWR?
U 1 1 5EB4A1A1
P 4900 5100
F 0 "#PWR?" H 4900 4850 50  0001 C CNN
F 1 "GNDA" H 4905 4927 50  0000 C CNN
F 2 "" H 4900 5100 50  0000 C CNN
F 3 "" H 4900 5100 50  0000 C CNN
	1    4900 5100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5600 4850 5600 5100
Wire Wire Line
	6350 4850 6350 5100
Text Notes 4750 5050 1    60   ~ 0
Proteccion\n
Text Notes 5100 4200 0    60   ~ 0
Desacple
Wire Notes Line
	3800 3900 3800 5050
Wire Notes Line
	3800 5050 4600 5050
Wire Notes Line
	4600 5050 4600 3900
Wire Notes Line
	4600 3900 3800 3900
Text Notes 3850 4000 0    60   ~ 0
PC/Mobil/etc
Wire Notes Line
	6550 3900 6550 5050
Wire Notes Line
	6550 5050 7300 5050
Wire Notes Line
	7300 5050 7300 3900
Wire Notes Line
	7300 3900 6550 3900
Text Notes 6850 4000 0    60   ~ 0
CIAA
Wire Wire Line
	5600 4500 5600 4550
Wire Wire Line
	5600 4500 5900 4500
Wire Wire Line
	6350 4500 6650 4500
Wire Wire Line
	4500 4500 4900 4500
Wire Wire Line
	4900 4500 5100 4500
$Comp
L power:VDDA #PWR?
U 1 1 5EB4A1BA
P 5600 3900
F 0 "#PWR?" H 5600 3750 50  0001 C CNN
F 1 "VDDA" H 5617 4073 50  0000 C CNN
F 2 "" H 5600 3900 50  0001 C CNN
F 3 "" H 5600 3900 50  0001 C CNN
	1    5600 3900
	1    0    0    -1  
$EndComp
$Comp
L power:VDDA #PWR?
U 1 1 5EB4A1C0
P 4900 3900
F 0 "#PWR?" H 4900 3750 50  0001 C CNN
F 1 "VDDA" H 4917 4073 50  0000 C CNN
F 2 "" H 4900 3900 50  0001 C CNN
F 3 "" H 4900 3900 50  0001 C CNN
	1    4900 3900
	1    0    0    -1  
$EndComp
Text Notes 4750 4400 1    60   ~ 0
Proteccion\n
Text Notes 6150 4800 2    60   ~ 0
FAA
Wire Wire Line
	5400 4500 5450 4500
Text HLabel 7300 4200 0    60   Input ~ 0
DAC
Wire Wire Line
	7300 4200 7450 4200
Wire Wire Line
	7450 4200 7450 3600
Wire Wire Line
	7450 3600 5450 3600
Wire Wire Line
	5450 3600 5450 4500
Connection ~ 5450 4500
Wire Wire Line
	5450 4500 5600 4500
Text HLabel 7600 1900 0    60   Input ~ 0
DAC
Wire Wire Line
	7600 1900 7750 1900
Wire Wire Line
	7750 1900 7750 1150
Wire Wire Line
	7750 1150 5750 1150
Wire Wire Line
	5750 1150 5750 2250
Connection ~ 5750 2250
Wire Wire Line
	5750 2250 5900 2250
Wire Wire Line
	5000 2250 5400 2250
$Comp
L power:GNDA #PWR?
U 1 1 60D0FAF6
P 5350 2850
F 0 "#PWR?" H 5350 2600 50  0001 C CNN
F 1 "GNDA" H 5350 2700 50  0000 C CNN
F 2 "" H 5350 2850 50  0000 C CNN
F 3 "" H 5350 2850 50  0000 C CNN
	1    5350 2850
	1    0    0    -1  
$EndComp
Text HLabel 5000 2450 0    60   Input ~ 0
AudioR
Text HLabel 5000 2700 0    60   Input ~ 0
AudioGND
Wire Wire Line
	5000 2700 5350 2700
Wire Wire Line
	5350 2700 5350 2850
$EndSCHEMATC
