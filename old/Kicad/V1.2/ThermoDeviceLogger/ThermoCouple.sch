EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 2
Title "Thermo Device Logger"
Date "2021-05-27"
Rev "V0.1"
Comp "Making Devices"
Comment1 "https://makingdevices.com/"
Comment2 "Thermo Couple Module"
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 7250 2350 2    50   Input ~ 0
spi_CLK
Text HLabel 7250 2250 2    50   Input ~ 0
spi_enable_tcm1
Text HLabel 7250 2150 2    50   Output ~ 0
spi_MISO
Text HLabel 5650 1200 2    50   Input ~ 0
3.3V
Text HLabel 1850 2150 0    50   Input ~ 0
T-tcm1
Text HLabel 1850 2250 0    50   Input ~ 0
T+tcm1
NoConn ~ 5050 2050
Wire Wire Line
	4050 2350 4000 2350
Wire Wire Line
	4000 2350 4000 1200
Wire Wire Line
	4000 2350 3950 2350
Connection ~ 4000 2350
Wire Wire Line
	3450 2050 3450 2350
Wire Wire Line
	3450 2050 4050 2050
Text HLabel 7250 3550 2    50   Input ~ 0
spi_enable_tcm2
Text HLabel 1850 3450 0    50   Input ~ 0
T-tcm2
Text HLabel 1850 3550 0    50   Input ~ 0
T+tcm2
NoConn ~ 5050 3350
Wire Wire Line
	4050 3650 4000 3650
Wire Wire Line
	4000 3650 3950 3650
Connection ~ 4000 3650
Wire Wire Line
	3450 3350 3450 3650
Wire Wire Line
	3450 3350 4050 3350
Wire Wire Line
	5050 3450 5100 3450
Wire Wire Line
	5050 3650 5400 3650
Wire Wire Line
	4000 1200 5400 1200
Wire Wire Line
	4000 2350 4000 3650
Wire Wire Line
	5400 3650 5400 2350
Wire Wire Line
	2700 2250 4050 2250
Wire Wire Line
	3400 2150 4050 2150
Wire Wire Line
	2700 3550 4050 3550
Wire Wire Line
	2600 3450 1850 3450
Wire Wire Line
	1900 3550 1850 3550
Wire Wire Line
	3400 3450 4050 3450
Wire Wire Line
	7250 2350 6850 2350
Wire Wire Line
	6250 2350 6100 2350
Connection ~ 5400 2350
Wire Wire Line
	5450 2250 5300 2250
Wire Wire Line
	6050 2250 7250 2250
Wire Wire Line
	6100 2100 6100 2350
Connection ~ 6100 2350
Wire Wire Line
	6100 2350 5400 2350
Wire Wire Line
	5300 2100 5300 2250
Connection ~ 5300 2250
Wire Wire Line
	5400 1400 5400 1200
Connection ~ 5400 1400
Wire Wire Line
	5400 1400 6100 1400
Connection ~ 5400 1200
Wire Wire Line
	5400 1200 5650 1200
Wire Wire Line
	7250 3550 6150 3550
Wire Wire Line
	5050 3550 5200 3550
Wire Wire Line
	5200 3400 5200 3550
Connection ~ 5200 3550
Wire Wire Line
	5200 3550 5550 3550
Wire Wire Line
	5200 2700 5200 1400
$Comp
L Library_Loader:MAX31855KASA+ IC2
U 1 1 611D796C
P 4050 2050
F 0 "IC2" H 4550 2315 50  0000 C CNN
F 1 "MAX31855KASA+" H 4550 2224 50  0000 C CNN
F 2 "SOIC127P600X175-8N" H 4900 2150 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/1901414P" H 4900 2050 50  0001 L CNN
F 4 "MAX31855KASA+, 14 bit Temperature Sensor +/-2 C SPI 3  3.6 V 8-Pin SOIC" H 4900 1950 50  0001 L CNN "Description"
F 5 "1.75" H 4900 1850 50  0001 L CNN "Height"
F 6 "1901414P" H 4900 1750 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/1901414P" H 4900 1650 50  0001 L CNN "RS Price/Stock"
F 8 "Maxim Integrated" H 4900 1550 50  0001 L CNN "Manufacturer_Name"
F 9 "MAX31855KASA+" H 4900 1450 50  0001 L CNN "Manufacturer_Part_Number"
	1    4050 2050
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:MAX31855KASA+ IC3
U 1 1 611D8506
P 4050 3350
F 0 "IC3" H 4550 3615 50  0000 C CNN
F 1 "MAX31855KASA+" H 4550 3524 50  0000 C CNN
F 2 "SOIC127P600X175-8N" H 4900 3450 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/1901414P" H 4900 3350 50  0001 L CNN
F 4 "MAX31855KASA+, 14 bit Temperature Sensor +/-2 C SPI 3  3.6 V 8-Pin SOIC" H 4900 3250 50  0001 L CNN "Description"
F 5 "1.75" H 4900 3150 50  0001 L CNN "Height"
F 6 "1901414P" H 4900 3050 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/1901414P" H 4900 2950 50  0001 L CNN "RS Price/Stock"
F 8 "Maxim Integrated" H 4900 2850 50  0001 L CNN "Manufacturer_Name"
F 9 "MAX31855KASA+" H 4900 2750 50  0001 L CNN "Manufacturer_Part_Number"
	1    4050 3350
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:742792005 LFB2
U 1 1 611DAC69
P 2600 2150
F 0 "LFB2" H 3000 2375 50  0000 C CNN
F 1 "Ferrite" H 3000 2284 50  0000 C CNN
F 2 "CAPC2012X90N" H 3250 2200 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7879929P" H 3250 2100 50  0001 L CNN
F 4 "SMD EMI Suppression Ferrite Beads WE-CBF" H 3250 2000 50  0001 L CNN "Description"
F 5 "0.9" H 3250 1900 50  0001 L CNN "Height"
F 6 "7879929P" H 3250 1800 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7879929P" H 3250 1700 50  0001 L CNN "RS Price/Stock"
F 8 "Wurth Elektronik" H 3250 1600 50  0001 L CNN "Manufacturer_Name"
F 9 "742792005" H 3250 1500 50  0001 L CNN "Manufacturer_Part_Number"
	1    2600 2150
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:742792005 LFB1
U 1 1 611DBCC7
P 1900 2250
F 0 "LFB1" H 2300 2475 50  0000 C CNN
F 1 "Ferrite" H 2300 2384 50  0000 C CNN
F 2 "CAPC2012X90N" H 2550 2300 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7879929P" H 2550 2200 50  0001 L CNN
F 4 "SMD EMI Suppression Ferrite Beads WE-CBF" H 2550 2100 50  0001 L CNN "Description"
F 5 "0.9" H 2550 2000 50  0001 L CNN "Height"
F 6 "7879929P" H 2550 1900 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7879929P" H 2550 1800 50  0001 L CNN "RS Price/Stock"
F 8 "Wurth Elektronik" H 2550 1700 50  0001 L CNN "Manufacturer_Name"
F 9 "742792005" H 2550 1600 50  0001 L CNN "Manufacturer_Part_Number"
	1    1900 2250
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:742792005 FB1
U 1 1 611DE3B5
P 1900 3550
F 0 "FB1" H 2300 3775 50  0000 C CNN
F 1 "742792005" H 2300 3684 50  0000 C CNN
F 2 "CAPC2012X90N" H 2550 3600 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7879929P" H 2550 3500 50  0001 L CNN
F 4 "SMD EMI Suppression Ferrite Beads WE-CBF" H 2550 3400 50  0001 L CNN "Description"
F 5 "0.9" H 2550 3300 50  0001 L CNN "Height"
F 6 "7879929P" H 2550 3200 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7879929P" H 2550 3100 50  0001 L CNN "RS Price/Stock"
F 8 "Wurth Elektronik" H 2550 3000 50  0001 L CNN "Manufacturer_Name"
F 9 "742792005" H 2550 2900 50  0001 L CNN "Manufacturer_Part_Number"
	1    1900 3550
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:742792005 FB2
U 1 1 611DF27E
P 2600 3450
F 0 "FB2" H 3000 3675 50  0000 C CNN
F 1 "742792005" H 3000 3584 50  0000 C CNN
F 2 "CAPC2012X90N" H 3250 3500 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7879929P" H 3250 3400 50  0001 L CNN
F 4 "SMD EMI Suppression Ferrite Beads WE-CBF" H 3250 3300 50  0001 L CNN "Description"
F 5 "0.9" H 3250 3200 50  0001 L CNN "Height"
F 6 "7879929P" H 3250 3100 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7879929P" H 3250 3000 50  0001 L CNN "RS Price/Stock"
F 8 "Wurth Elektronik" H 3250 2900 50  0001 L CNN "Manufacturer_Name"
F 9 "742792005" H 3250 2800 50  0001 L CNN "Manufacturer_Part_Number"
	1    2600 3450
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:ZLLS410TA D3
U 1 1 611E1D22
P 6850 2350
F 0 "D3" H 7150 2083 50  0000 C CNN
F 1 "ZLLS410TA" H 7150 2174 50  0000 C CNN
F 2 "SOD2513X120N" H 7300 2350 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7515203P" H 7300 2250 50  0001 L CNN
F 4 "Diodes Inc ZLLS410TA, SMT Schottky Diode, 10V 750mA, 3ns, 2-Pin SOD-323" H 7300 2150 50  0001 L CNN "Description"
F 5 "1.2" H 7300 2050 50  0001 L CNN "Height"
F 6 "7515203P" H 7300 1950 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7515203P" H 7300 1850 50  0001 L CNN "RS Price/Stock"
F 8 "Diodes Inc." H 7300 1750 50  0001 L CNN "Manufacturer_Name"
F 9 "ZLLS410TA" H 7300 1650 50  0001 L CNN "Manufacturer_Part_Number"
	1    6850 2350
	-1   0    0    1   
$EndComp
$Comp
L Library_Loader:ZLLS410TA D1
U 1 1 611E3073
P 6050 2250
F 0 "D1" H 6350 1983 50  0000 C CNN
F 1 "ZLLS410TA" H 6350 2074 50  0000 C CNN
F 2 "SOD2513X120N" H 6500 2250 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7515203P" H 6500 2150 50  0001 L CNN
F 4 "Diodes Inc ZLLS410TA, SMT Schottky Diode, 10V 750mA, 3ns, 2-Pin SOD-323" H 6500 2050 50  0001 L CNN "Description"
F 5 "1.2" H 6500 1950 50  0001 L CNN "Height"
F 6 "7515203P" H 6500 1850 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7515203P" H 6500 1750 50  0001 L CNN "RS Price/Stock"
F 8 "Diodes Inc." H 6500 1650 50  0001 L CNN "Manufacturer_Name"
F 9 "ZLLS410TA" H 6500 1550 50  0001 L CNN "Manufacturer_Part_Number"
	1    6050 2250
	-1   0    0    1   
$EndComp
$Comp
L Library_Loader:ZLLS410TA D2
U 1 1 611E3F22
P 6150 3550
F 0 "D2" H 6450 3283 50  0000 C CNN
F 1 "ZLLS410TA" H 6450 3374 50  0000 C CNN
F 2 "SOD2513X120N" H 6600 3550 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7515203P" H 6600 3450 50  0001 L CNN
F 4 "Diodes Inc ZLLS410TA, SMT Schottky Diode, 10V 750mA, 3ns, 2-Pin SOD-323" H 6600 3350 50  0001 L CNN "Description"
F 5 "1.2" H 6600 3250 50  0001 L CNN "Height"
F 6 "7515203P" H 6600 3150 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7515203P" H 6600 3050 50  0001 L CNN "RS Price/Stock"
F 8 "Diodes Inc." H 6600 2950 50  0001 L CNN "Manufacturer_Name"
F 9 "ZLLS410TA" H 6600 2850 50  0001 L CNN "Manufacturer_Part_Number"
	1    6150 3550
	-1   0    0    1   
$EndComp
Wire Wire Line
	5200 1400 5300 1400
Wire Wire Line
	5050 2350 5400 2350
$Comp
L Library_Loader:ERJP6WF1303V R6
U 1 1 611E8466
P 6100 1400
F 0 "R6" V 6404 1488 50  0000 L CNN
F 1 "10k" V 6495 1488 50  0000 L CNN
F 2 "RESC2012X75N" H 6650 1450 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 6650 1350 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 6650 1250 50  0001 L CNN "Description"
F 5 "0.75" H 6650 1150 50  0001 L CNN "Height"
F 6 "7708607P" H 6650 1050 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 6650 950 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 6650 850 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 6650 750 50  0001 L CNN "Manufacturer_Part_Number"
	1    6100 1400
	0    1    1    0   
$EndComp
$Comp
L Library_Loader:ERJP6WF1303V R5
U 1 1 611E940C
P 5300 1400
F 0 "R5" V 5604 1488 50  0000 L CNN
F 1 "10k" V 5695 1488 50  0000 L CNN
F 2 "RESC2012X75N" H 5850 1450 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 5850 1350 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 5850 1250 50  0001 L CNN "Description"
F 5 "0.75" H 5850 1150 50  0001 L CNN "Height"
F 6 "7708607P" H 5850 1050 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 5850 950 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 5850 850 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 5850 750 50  0001 L CNN "Manufacturer_Part_Number"
	1    5300 1400
	0    1    1    0   
$EndComp
Connection ~ 5300 1400
Wire Wire Line
	5300 1400 5400 1400
$Comp
L Library_Loader:ERJP6WF1303V R4
U 1 1 611EA2E3
P 5200 2700
F 0 "R4" V 5504 2788 50  0000 L CNN
F 1 "10k" V 5595 2788 50  0000 L CNN
F 2 "RESC2012X75N" H 5750 2750 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 5750 2650 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 5750 2550 50  0001 L CNN "Description"
F 5 "0.75" H 5750 2450 50  0001 L CNN "Height"
F 6 "7708607P" H 5750 2350 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 5750 2250 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 5750 2150 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 5750 2050 50  0001 L CNN "Manufacturer_Part_Number"
	1    5200 2700
	0    1    1    0   
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C7
U 1 1 611ED141
P 3450 2350
F 0 "C7" H 3700 2615 50  0000 C CNN
F 1 "100nF" H 3700 2524 50  0000 C CNN
F 2 "CAPC2012X140N" H 3800 2400 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 3800 2300 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 3800 2200 50  0001 L CNN "Description"
F 5 "1.4" H 3800 2100 50  0001 L CNN "Height"
F 6 "" H 3800 2000 50  0001 L CNN "RS Part Number"
F 7 "" H 3800 1900 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 3800 1800 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 3800 1700 50  0001 L CNN "Manufacturer_Part_Number"
	1    3450 2350
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C8
U 1 1 611EE2D4
P 3450 3650
F 0 "C8" H 3700 3915 50  0000 C CNN
F 1 "100nF" H 3700 3824 50  0000 C CNN
F 2 "CAPC2012X140N" H 3800 3700 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 3800 3600 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 3800 3500 50  0001 L CNN "Description"
F 5 "1.4" H 3800 3400 50  0001 L CNN "Height"
F 6 "" H 3800 3300 50  0001 L CNN "RS Part Number"
F 7 "" H 3800 3200 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 3800 3100 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 3800 3000 50  0001 L CNN "Manufacturer_Part_Number"
	1    3450 3650
	1    0    0    -1  
$EndComp
Text HLabel 3550 3950 2    50   Input ~ 0
gnd
Wire Wire Line
	3450 3650 3450 3950
Wire Wire Line
	3450 3950 3550 3950
Connection ~ 3450 3650
Wire Wire Line
	3450 3350 3450 2350
Connection ~ 3450 3350
Connection ~ 3450 2350
Wire Wire Line
	2600 2150 1850 2150
Wire Wire Line
	1900 2250 1850 2250
Wire Wire Line
	5050 2250 5300 2250
Wire Wire Line
	5050 2150 5100 2150
Wire Wire Line
	5100 3450 5100 2150
Connection ~ 5100 2150
Wire Wire Line
	5100 2150 7250 2150
$EndSCHEMATC
