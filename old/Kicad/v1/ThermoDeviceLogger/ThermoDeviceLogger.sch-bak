EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 2
Title "Thermo Device Logger"
Date "2021-05-27"
Rev "V0.1"
Comp "Making Devices"
Comment1 "https://makingdevices.com/"
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 1800 2300 1150 600 
U 60AFDA00
F0 "ThermoCouple Modules" 50
F1 "ThermoCouple.sch" 50
F2 "spi_CLK" I R 2950 2400 50 
F3 "spi_enable_tcm1" I R 2950 2600 50 
F4 "spi_MISO" O R 2950 2500 50 
F5 "3.3V" I L 1800 2400 50 
F6 "T-tcm1" I L 1800 2600 50 
F7 "T+tcm1" I L 1800 2500 50 
F8 "spi_enable_tcm2" I R 2950 2700 50 
F9 "T-tcm2" I L 1800 2800 50 
F10 "T+tcm2" I L 1800 2700 50 
F11 "gnd" I R 2950 2800 50 
$EndSheet
$Comp
L MCU_Microchip_PIC18:PIC18LF14K50-ESS U1
U 1 1 611D78C5
P 6650 2900
F 0 "U1" H 7044 3881 50  0000 C CNN
F 1 "PIC18F14K50" H 7044 3790 50  0000 C CNN
F 2 "Package_SO:SSOP-20_5.3x7.2mm_P0.65mm" H 6650 2900 50  0001 C CIN
F 3 "http://ww1.microchip.com/downloads/en/devicedoc/41350c.pdf" H 6650 3000 50  0001 C CNN
	1    6650 2900
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:CX2520DB12000D0GPSC1 Y1
U 1 1 611E8360
P 8600 1300
F 0 "Y1" H 9400 1565 50  0000 C CNN
F 1 "12Mhz" H 9400 1474 50  0000 C CNN
F 2 "CX2520DB12000D0GPSC1" H 10050 1400 50  0001 L CNN
F 3 "https://media.digikey.com/pdf/Data%20Sheets/AVX%20PDFs/CX2520DB_USY1M-H1-16428-00_Spec.pdf" H 10050 1300 50  0001 L CNN
F 4 "Crystals AEC-Q200 12MHz 8pF 2.5x2mm" H 10050 1200 50  0001 L CNN "Description"
F 5 "0.55" H 10050 1100 50  0001 L CNN "Height"
F 6 "" H 10050 1000 50  0001 L CNN "RS Part Number"
F 7 "" H 10050 900 50  0001 L CNN "RS Price/Stock"
F 8 "KYOCERA" H 10050 800 50  0001 L CNN "Manufacturer_Name"
F 9 "CX2520DB12000D0GPSC1" H 10050 700 50  0001 L CNN "Manufacturer_Part_Number"
	1    8600 1300
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 611EDA17
P 3100 2950
F 0 "#PWR04" H 3100 2700 50  0001 C CNN
F 1 "GND" H 3105 2777 50  0000 C CNN
F 2 "" H 3100 2950 50  0001 C CNN
F 3 "" H 3100 2950 50  0001 C CNN
	1    3100 2950
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C6
U 1 1 611EEAFC
P 10450 1800
F 0 "C6" V 10746 1672 50  0000 R CNN
F 1 "22pF" V 10655 1672 50  0000 R CNN
F 2 "CAPC2012X140N" H 10800 1850 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 10800 1750 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 10800 1650 50  0001 L CNN "Description"
F 5 "1.4" H 10800 1550 50  0001 L CNN "Height"
F 6 "" H 10800 1450 50  0001 L CNN "RS Part Number"
F 7 "" H 10800 1350 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 10800 1250 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 10800 1150 50  0001 L CNN "Manufacturer_Part_Number"
	1    10450 1800
	0    -1   -1   0   
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C5
U 1 1 611EFDE5
P 8350 1400
F 0 "C5" V 8554 1528 50  0000 L CNN
F 1 "22pF" V 8645 1528 50  0000 L CNN
F 2 "CAPC2012X140N" H 8700 1450 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 8700 1350 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 8700 1250 50  0001 L CNN "Description"
F 5 "1.4" H 8700 1150 50  0001 L CNN "Height"
F 6 "" H 8700 1050 50  0001 L CNN "RS Part Number"
F 7 "" H 8700 950 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 8700 850 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 8700 750 50  0001 L CNN "Manufacturer_Part_Number"
	1    8350 1400
	0    1    1    0   
$EndComp
Wire Wire Line
	10200 1300 10450 1300
Wire Wire Line
	8600 1300 8350 1300
Wire Wire Line
	8350 1300 8350 1400
$Comp
L power:GND #PWR015
U 1 1 611F22F9
P 9400 1900
F 0 "#PWR015" H 9400 1650 50  0001 C CNN
F 1 "GND" H 9405 1727 50  0000 C CNN
F 2 "" H 9400 1900 50  0001 C CNN
F 3 "" H 9400 1900 50  0001 C CNN
	1    9400 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	10450 1800 10450 1900
Wire Wire Line
	10450 1900 10200 1900
Wire Wire Line
	8350 1900 8600 1900
Connection ~ 9400 1900
Wire Wire Line
	10200 1400 10200 1900
Connection ~ 10200 1900
Wire Wire Line
	10200 1900 9400 1900
Wire Wire Line
	8600 1400 8600 1900
Connection ~ 8600 1900
Wire Wire Line
	8600 1900 9400 1900
Text Label 10400 1300 0    50   ~ 0
Crystal2
Text Label 8350 1300 0    50   ~ 0
Cyrstal1
$Comp
L Library_Loader:TC1108-3.3VDBTR IC1
U 1 1 611F931D
P 2100 3650
F 0 "IC1" H 2700 3915 50  0000 C CNN
F 1 "TC1108-3.3VDBTR" H 2700 3824 50  0000 C CNN
F 2 "SOT230P700X180-4N" H 3150 3750 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/8234309P" H 3150 3650 50  0001 L CNN
F 4 "Microchip TC1108-3.3VDBTR, LDO Voltage Regulator, 300mA, 3.3 V +/-0.5%, 2.7  6 Vin, 3-Pin SOT-223" H 3150 3550 50  0001 L CNN "Description"
F 5 "1.8" H 3150 3450 50  0001 L CNN "Height"
F 6 "8234309P" H 3150 3350 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/8234309P" H 3150 3250 50  0001 L CNN "RS Price/Stock"
F 8 "Microchip" H 3150 3150 50  0001 L CNN "Manufacturer_Name"
F 9 "TC1108-3.3VDBTR" H 3150 3050 50  0001 L CNN "Manufacturer_Part_Number"
F 10 "70451504" H 3150 2950 50  0001 L CNN "Allied_Number"
	1    2100 3650
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C2
U 1 1 611F9EEE
P 1800 3900
F 0 "C2" V 2004 4028 50  0000 L CNN
F 1 "1uF" V 2095 4028 50  0000 L CNN
F 2 "CAPC2012X140N" H 2150 3950 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 2150 3850 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 2150 3750 50  0001 L CNN "Description"
F 5 "1.4" H 2150 3650 50  0001 L CNN "Height"
F 6 "" H 2150 3550 50  0001 L CNN "RS Part Number"
F 7 "" H 2150 3450 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 2150 3350 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 2150 3250 50  0001 L CNN "Manufacturer_Part_Number"
	1    1800 3900
	0    1    1    0   
$EndComp
$Comp
L Library_Loader:C0805C475M8RACTU C1
U 1 1 611FB1BB
P 1450 3900
F 0 "C1" V 1654 4028 50  0000 L CNN
F 1 "1uF" V 1745 4028 50  0000 L CNN
F 2 "CAPC2012X140N" H 1800 3950 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 1800 3850 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 1800 3750 50  0001 L CNN "Description"
F 5 "1.4" H 1800 3650 50  0001 L CNN "Height"
F 6 "" H 1800 3550 50  0001 L CNN "RS Part Number"
F 7 "" H 1800 3450 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 1800 3350 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 1800 3250 50  0001 L CNN "Manufacturer_Part_Number"
	1    1450 3900
	0    1    1    0   
$EndComp
Wire Wire Line
	2100 3650 1450 3650
Wire Wire Line
	1450 3650 1450 3900
Wire Wire Line
	2100 3850 1800 3850
Wire Wire Line
	1800 3850 1800 3900
Wire Wire Line
	2100 3750 1250 3750
Wire Wire Line
	1250 3750 1250 4550
Wire Wire Line
	1250 4550 1450 4550
Wire Wire Line
	1800 4550 1800 4400
Wire Wire Line
	1450 4400 1450 4550
Connection ~ 1450 4550
Wire Wire Line
	1450 4550 1800 4550
Wire Wire Line
	1800 4550 2450 4550
Wire Wire Line
	3300 4550 3300 3650
Connection ~ 1800 4550
$Comp
L power:GND #PWR03
U 1 1 6120035B
P 2450 4600
F 0 "#PWR03" H 2450 4350 50  0001 C CNN
F 1 "GND" H 2455 4427 50  0000 C CNN
F 2 "" H 2450 4600 50  0001 C CNN
F 3 "" H 2450 4600 50  0001 C CNN
	1    2450 4600
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 4600 2450 4550
Connection ~ 2450 4550
Wire Wire Line
	2450 4550 3300 4550
Text Label 1850 3850 0    50   ~ 0
3.3V
Text Label 1450 2400 0    50   ~ 0
3.3V
Wire Wire Line
	1800 2400 1450 2400
$Comp
L power:GND #PWR012
U 1 1 6120FD6B
P 6650 3800
F 0 "#PWR012" H 6650 3550 50  0001 C CNN
F 1 "GND" H 6655 3627 50  0000 C CNN
F 2 "" H 6650 3800 50  0001 C CNN
F 3 "" H 6650 3800 50  0001 C CNN
	1    6650 3800
	1    0    0    -1  
$EndComp
Wire Wire Line
	6650 3800 6650 3700
Wire Wire Line
	5150 2800 4850 2800
Wire Wire Line
	5150 2700 4850 2700
Text Label 4850 2800 2    50   ~ 0
Crystal2
Text Label 4850 2700 2    50   ~ 0
Cyrstal1
$Comp
L Library_Loader:ERJP6WF1303V R1
U 1 1 6121478B
P 3950 2600
F 0 "R1" H 4300 2825 50  0000 C CNN
F 1 "10k" H 4300 2734 50  0000 C CNN
F 2 "RESC2012X75N" H 4500 2650 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 4500 2550 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 4500 2450 50  0001 L CNN "Description"
F 5 "0.75" H 4500 2350 50  0001 L CNN "Height"
F 6 "7708607P" H 4500 2250 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 4500 2150 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 4500 2050 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 4500 1950 50  0001 L CNN "Manufacturer_Part_Number"
	1    3950 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4650 2600 5150 2600
$Comp
L power:+5V #PWR07
U 1 1 61215597
P 3800 2600
F 0 "#PWR07" H 3800 2450 50  0001 C CNN
F 1 "+5V" H 3815 2773 50  0000 C CNN
F 2 "" H 3800 2600 50  0001 C CNN
F 3 "" H 3800 2600 50  0001 C CNN
	1    3800 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 2600 3800 2600
$Comp
L power:+5V #PWR011
U 1 1 612164F5
P 6650 1900
F 0 "#PWR011" H 6650 1750 50  0001 C CNN
F 1 "+5V" H 6665 2073 50  0000 C CNN
F 2 "" H 6650 1900 50  0001 C CNN
F 3 "" H 6650 1900 50  0001 C CNN
	1    6650 1900
	1    0    0    -1  
$EndComp
$Comp
L Library_Loader:TC2030-MCP-NL J2
U 1 1 61218202
P 5700 5250
F 0 "J2" H 6600 5515 50  0000 C CNN
F 1 "TC2030-MCP-NL" H 6600 5424 50  0000 C CNN
F 2 "TC2030-MCP-NL" H 7350 5350 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/8252561" H 7350 5250 50  0001 L CNN
F 4 "TC2030-MCP-NL PCB Footprint (no legs)" H 7350 5150 50  0001 L CNN "Description"
F 5 "" H 7350 5050 50  0001 L CNN "Height"
F 6 "8252561" H 7350 4950 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/8252561" H 7350 4850 50  0001 L CNN "RS Price/Stock"
F 8 "Microchip" H 7350 4750 50  0001 L CNN "Manufacturer_Name"
F 9 "TC2030-MCP-NL" H 7350 4650 50  0001 L CNN "Manufacturer_Part_Number"
	1    5700 5250
	1    0    0    -1  
$EndComp
NoConn ~ 7500 5450
Wire Wire Line
	7500 5250 7750 5250
Wire Wire Line
	7500 5350 7750 5350
Text Label 7750 5250 0    50   ~ 0
PGD
Text Label 7750 5350 0    50   ~ 0
PGC
Text Label 5150 2400 2    50   ~ 0
PGD
Text Label 5150 2500 2    50   ~ 0
PGC
$Comp
L power:GND #PWR09
U 1 1 6121ABC1
P 5500 5450
F 0 "#PWR09" H 5500 5200 50  0001 C CNN
F 1 "GND" H 5505 5277 50  0000 C CNN
F 2 "" H 5500 5450 50  0001 C CNN
F 3 "" H 5500 5450 50  0001 C CNN
	1    5500 5450
	1    0    0    -1  
$EndComp
$Comp
L power:+5V #PWR08
U 1 1 6121B7A5
P 5500 5350
F 0 "#PWR08" H 5500 5200 50  0001 C CNN
F 1 "+5V" H 5515 5523 50  0000 C CNN
F 2 "" H 5500 5350 50  0001 C CNN
F 3 "" H 5500 5350 50  0001 C CNN
	1    5500 5350
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5700 5450 5500 5450
Wire Wire Line
	5700 5350 5500 5350
Text Label 4800 2600 0    50   ~ 0
MCLR
Wire Wire Line
	5700 5250 5550 5250
Text Label 5550 5250 2    50   ~ 0
MCLR
Wire Wire Line
	5150 3300 4950 3300
Text Label 4950 3300 2    50   ~ 0
SCK
Text Label 4950 3100 2    50   ~ 0
MISO
Wire Wire Line
	5150 3100 4950 3100
Wire Wire Line
	2950 2400 3250 2400
Wire Wire Line
	2950 2500 3250 2500
Wire Wire Line
	2950 2600 3250 2600
Wire Wire Line
	2950 2700 3250 2700
Text Label 3250 2400 0    50   ~ 0
SCK
Text Label 3250 2500 0    50   ~ 0
MISO
Wire Wire Line
	8150 2400 8350 2400
Wire Wire Line
	8150 2500 8350 2500
Text Label 8350 2400 0    50   ~ 0
CS_1
Text Label 8350 2500 0    50   ~ 0
CS_2
Text Label 3250 2600 0    50   ~ 0
CS_1
Text Label 3250 2700 0    50   ~ 0
CS_2
$Comp
L Library_Loader:217183-0001 J1
U 1 1 611ECC22
P 1850 5250
F 0 "J1" H 2500 5515 50  0000 C CNN
F 1 "Type - C" H 2500 5424 50  0000 C CNN
F 2 "2171830001" H 3000 5350 50  0001 L CNN
F 3 "https://www.molex.com/pdm_docs/sd/2171830001_sd.pdf" H 3000 5250 50  0001 L CNN
F 4 "Connector USB Type C Hybrid Female 24Positions 0.5mm Right Angle Through Hole Embossed T/R" H 3000 5150 50  0001 L CNN "Description"
F 5 "3.36" H 3000 5050 50  0001 L CNN "Height"
F 6 "" H 3000 4950 50  0001 L CNN "RS Part Number"
F 7 "" H 3000 4850 50  0001 L CNN "RS Price/Stock"
F 8 "Molex" H 3000 4750 50  0001 L CNN "Manufacturer_Name"
F 9 "217183-0001" H 3000 4650 50  0001 L CNN "Manufacturer_Part_Number"
	1    1850 5250
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 61204234
P 3200 6850
F 0 "#PWR06" H 3200 6600 50  0001 C CNN
F 1 "GND" H 3205 6677 50  0000 C CNN
F 2 "" H 3200 6850 50  0001 C CNN
F 3 "" H 3200 6850 50  0001 C CNN
	1    3200 6850
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 6250 3150 6250
Wire Wire Line
	3200 6250 3200 6350
Wire Wire Line
	3150 6350 3200 6350
Connection ~ 3200 6350
Wire Wire Line
	3200 6350 3200 6450
Wire Wire Line
	3150 6450 3200 6450
Connection ~ 3200 6450
Wire Wire Line
	3200 6450 3200 6550
Wire Wire Line
	3150 6550 3200 6550
Connection ~ 3200 6550
Wire Wire Line
	3200 6550 3200 6750
Wire Wire Line
	1450 6350 1450 6450
Wire Wire Line
	1450 5250 1450 6350
Connection ~ 1450 6350
Wire Wire Line
	1450 5250 1850 5250
Wire Wire Line
	1450 6450 1850 6450
Wire Wire Line
	1450 6350 1850 6350
Wire Wire Line
	3200 6750 1450 6750
Wire Wire Line
	1450 6750 1450 6450
Connection ~ 3200 6750
Wire Wire Line
	3200 6750 3200 6850
Connection ~ 1450 6450
NoConn ~ 1850 5950
NoConn ~ 1850 6050
NoConn ~ 1850 6150
NoConn ~ 1850 6250
NoConn ~ 1850 6550
NoConn ~ 1850 5650
NoConn ~ 1850 5450
NoConn ~ 1850 5350
NoConn ~ 3150 5250
NoConn ~ 3150 5350
NoConn ~ 3150 5450
NoConn ~ 3150 5750
NoConn ~ 3150 5950
NoConn ~ 3150 6050
NoConn ~ 3150 6150
Text Label 1850 5750 2    50   ~ 0
PGD
Text Label 3150 5550 0    50   ~ 0
PGD
Text Label 3150 5650 0    50   ~ 0
PGC
Text Label 1850 5850 2    50   ~ 0
PGC
$Comp
L Library_Loader:C0805C475M8RACTU C3
U 1 1 6122728D
P 5950 2000
F 0 "C3" V 6154 2128 50  0000 L CNN
F 1 "1uF" V 6245 2128 50  0000 L CNN
F 2 "CAPC2012X140N" H 6300 2050 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 6300 1950 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 6300 1850 50  0001 L CNN "Description"
F 5 "1.4" H 6300 1750 50  0001 L CNN "Height"
F 6 "" H 6300 1650 50  0001 L CNN "RS Part Number"
F 7 "" H 6300 1550 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 6300 1450 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 6300 1350 50  0001 L CNN "Manufacturer_Part_Number"
	1    5950 2000
	1    0    0    -1  
$EndComp
Wire Wire Line
	6650 1900 6650 2000
Wire Wire Line
	6450 2000 6650 2000
$Comp
L power:GND #PWR010
U 1 1 6122DF09
P 5850 2050
F 0 "#PWR010" H 5850 1800 50  0001 C CNN
F 1 "GND" H 5855 1877 50  0000 C CNN
F 2 "" H 5850 2050 50  0001 C CNN
F 3 "" H 5850 2050 50  0001 C CNN
	1    5850 2050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5950 2000 5850 2000
Wire Wire Line
	5850 2000 5850 2050
$Comp
L power:+5V #PWR01
U 1 1 61230989
P 1450 3450
F 0 "#PWR01" H 1450 3300 50  0001 C CNN
F 1 "+5V" H 1465 3623 50  0000 C CNN
F 2 "" H 1450 3450 50  0001 C CNN
F 3 "" H 1450 3450 50  0001 C CNN
	1    1450 3450
	1    0    0    -1  
$EndComp
Connection ~ 1450 3650
Wire Wire Line
	1450 3450 1450 3650
$Comp
L power:+5V #PWR05
U 1 1 61238588
P 3250 5850
F 0 "#PWR05" H 3250 5700 50  0001 C CNN
F 1 "+5V" H 3265 6023 50  0000 C CNN
F 2 "" H 3250 5850 50  0001 C CNN
F 3 "" H 3250 5850 50  0001 C CNN
	1    3250 5850
	0    1    1    0   
$EndComp
$Comp
L power:+5V #PWR02
U 1 1 61239D75
P 1750 5550
F 0 "#PWR02" H 1750 5400 50  0001 C CNN
F 1 "+5V" H 1765 5723 50  0000 C CNN
F 2 "" H 1750 5550 50  0001 C CNN
F 3 "" H 1750 5550 50  0001 C CNN
	1    1750 5550
	0    -1   -1   0   
$EndComp
$Comp
L Library_Loader:ERJP6WF1303V R2
U 1 1 6123CF68
P 8400 2700
F 0 "R2" V 8704 2788 50  0000 L CNN
F 1 "220" V 8795 2788 50  0000 L CNN
F 2 "RESC2012X75N" H 8950 2750 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 8950 2650 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 8950 2550 50  0001 L CNN "Description"
F 5 "0.75" H 8950 2450 50  0001 L CNN "Height"
F 6 "7708607P" H 8950 2350 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 8950 2250 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 8950 2150 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 8950 2050 50  0001 L CNN "Manufacturer_Part_Number"
	1    8400 2700
	0    1    1    0   
$EndComp
$Comp
L Library_Loader:ERJP6WF1303V R3
U 1 1 6123E138
P 8750 2600
F 0 "R3" V 9054 2688 50  0000 L CNN
F 1 "220" V 9145 2688 50  0000 L CNN
F 2 "RESC2012X75N" H 9300 2650 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/7708607P" H 9300 2550 50  0001 L CNN
F 4 "Panasonic ERJP6W Series Thick Film Surface Mount Fixed Resistor 0805 Case 130k +/-1% 0.5W +/-200ppm/C" H 9300 2450 50  0001 L CNN "Description"
F 5 "0.75" H 9300 2350 50  0001 L CNN "Height"
F 6 "7708607P" H 9300 2250 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/7708607P" H 9300 2150 50  0001 L CNN "RS Price/Stock"
F 8 "Panasonic" H 9300 2050 50  0001 L CNN "Manufacturer_Name"
F 9 "ERJP6WF1303V" H 9300 1950 50  0001 L CNN "Manufacturer_Part_Number"
	1    8750 2600
	0    1    1    0   
$EndComp
Wire Wire Line
	8750 2600 8150 2600
Wire Wire Line
	8150 2700 8400 2700
$Comp
L Library_Loader:SML-H12V8TT86 LED1
U 1 1 61243180
P 8400 4050
F 0 "LED1" V 8746 3920 50  0000 R CNN
F 1 "Green" V 8655 3920 50  0000 R CNN
F 2 "LEDC2012X90N" H 8900 4200 50  0001 L BNN
F 3 "http://uk.rs-online.com/web/p/products/1332888P" H 8900 4100 50  0001 L BNN
F 4 "EXCELED series chip LED: ROHM\\'s chip LED lineup consists of standard type,top-view type, side-view type and reverse-mount type." H 8900 4000 50  0001 L BNN "Description"
F 5 "0.9" H 8900 3900 50  0001 L BNN "Height"
F 6 "1332888P" H 8900 3800 50  0001 L BNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/1332888P" H 8900 3700 50  0001 L BNN "RS Price/Stock"
F 8 "ROHM Semiconductor" H 8900 3600 50  0001 L BNN "Manufacturer_Name"
F 9 "SML-H12V8TT86" H 8900 3500 50  0001 L BNN "Manufacturer_Part_Number"
	1    8400 4050
	0    -1   -1   0   
$EndComp
$Comp
L Library_Loader:SML-H12V8TT86 LED2
U 1 1 612482DC
P 8750 4250
F 0 "LED2" V 9096 4120 50  0000 R CNN
F 1 "Green" V 9005 4120 50  0000 R CNN
F 2 "LEDC2012X90N" H 9250 4400 50  0001 L BNN
F 3 "http://uk.rs-online.com/web/p/products/1332888P" H 9250 4300 50  0001 L BNN
F 4 "EXCELED series chip LED: ROHM\\'s chip LED lineup consists of standard type,top-view type, side-view type and reverse-mount type." H 9250 4200 50  0001 L BNN "Description"
F 5 "0.9" H 9250 4100 50  0001 L BNN "Height"
F 6 "1332888P" H 9250 4000 50  0001 L BNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/1332888P" H 9250 3900 50  0001 L BNN "RS Price/Stock"
F 8 "ROHM Semiconductor" H 9250 3800 50  0001 L BNN "Manufacturer_Name"
F 9 "SML-H12V8TT86" H 9250 3700 50  0001 L BNN "Manufacturer_Part_Number"
	1    8750 4250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8400 3400 8400 3450
Wire Wire Line
	8750 3300 8750 3650
Wire Wire Line
	8750 4250 8750 4350
Wire Wire Line
	8750 4350 8600 4350
Wire Wire Line
	8400 4350 8400 4050
$Comp
L power:GND #PWR014
U 1 1 61251086
P 8600 4400
F 0 "#PWR014" H 8600 4150 50  0001 C CNN
F 1 "GND" H 8605 4227 50  0000 C CNN
F 2 "" H 8600 4400 50  0001 C CNN
F 3 "" H 8600 4400 50  0001 C CNN
	1    8600 4400
	1    0    0    -1  
$EndComp
Wire Wire Line
	8600 4400 8600 4350
Connection ~ 8600 4350
Wire Wire Line
	8600 4350 8400 4350
$Comp
L Library_Loader:C0805C475M8RACTU C4
U 1 1 6125711E
P 8050 4050
F 0 "C4" V 8254 4178 50  0000 L CNN
F 1 "1uF" V 8345 4178 50  0000 L CNN
F 2 "CAPC2012X140N" H 8400 4100 50  0001 L CNN
F 3 "https://datasheet.datasheetarchive.com/originals/distributors/Datasheets-DGA8/2444426.pdf" H 8400 4000 50  0001 L CNN
F 4 "Cap Ceramic 4.7uF 10V X7R 20% Pad SMD 0805 125C T/R" H 8400 3900 50  0001 L CNN "Description"
F 5 "1.4" H 8400 3800 50  0001 L CNN "Height"
F 6 "" H 8400 3700 50  0001 L CNN "RS Part Number"
F 7 "" H 8400 3600 50  0001 L CNN "RS Price/Stock"
F 8 "Kemet" H 8400 3500 50  0001 L CNN "Manufacturer_Name"
F 9 "C0805C475M8RACTU" H 8400 3400 50  0001 L CNN "Manufacturer_Part_Number"
	1    8050 4050
	0    -1   -1   0   
$EndComp
Wire Wire Line
	8150 3300 8150 3550
Wire Wire Line
	8150 3550 8050 3550
$Comp
L power:GND #PWR013
U 1 1 6125A633
P 8050 4050
F 0 "#PWR013" H 8050 3800 50  0001 C CNN
F 1 "GND" H 8055 3877 50  0000 C CNN
F 2 "" H 8050 4050 50  0001 C CNN
F 3 "" H 8050 4050 50  0001 C CNN
	1    8050 4050
	1    0    0    -1  
$EndComp
NoConn ~ 8150 3100
NoConn ~ 8150 3000
NoConn ~ 8150 2900
NoConn ~ 8150 2800
NoConn ~ 5150 3200
NoConn ~ 5150 3400
$Comp
L Library_Loader:1751264 J3
U 1 1 612913B9
P 1300 2500
F 0 "J3" H 1592 1935 50  0000 C CNN
F 1 "4-terminal" H 1592 2026 50  0000 C CNN
F 2 "1751264" H 1950 2600 50  0001 L CNN
F 3 "http://uk.rs-online.com/web/p/products/8024852" H 1950 2500 50  0001 L CNN
F 4 "Fixed Terminal Blocks 4P 3.5mm 90DEG" H 1950 2400 50  0001 L CNN "Description"
F 5 "8.5" H 1950 2300 50  0001 L CNN "Height"
F 6 "8024852" H 1950 2200 50  0001 L CNN "RS Part Number"
F 7 "http://uk.rs-online.com/web/p/products/8024852" H 1950 2100 50  0001 L CNN "RS Price/Stock"
F 8 "Phoenix Contact" H 1950 2000 50  0001 L CNN "Manufacturer_Name"
F 9 "1751264" H 1950 1900 50  0001 L CNN "Manufacturer_Part_Number"
	1    1300 2500
	-1   0    0    -1  
$EndComp
Wire Wire Line
	1800 2500 1300 2500
Wire Wire Line
	1300 2600 1800 2600
Wire Wire Line
	1800 2700 1300 2700
Wire Wire Line
	1300 2800 1800 2800
Wire Wire Line
	3100 2950 3100 2800
Wire Wire Line
	3100 2800 2950 2800
Wire Wire Line
	6650 2100 6650 2000
Connection ~ 6650 2000
Wire Wire Line
	1750 5550 1850 5550
Wire Wire Line
	3250 5850 3150 5850
$EndSCHEMATC
