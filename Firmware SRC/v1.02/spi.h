#ifndef __SPI_H
#define __SPI_H
/******************************************************************************
 // *                   SPI PERIPHERAL LIBRARY HEADER FILE
 ******************************************************************************
 * FileName:        		spi.h
 * Dependencies:    	See include below
 * Processor:       		PIC18
 * Compiler:        		MCC18
 * Company:         		Microchip Technology, Inc.
 *
 * Software License Agreement
 * The software supplied herewith by Microchip Technology Incorporated
 * (the “Company”) for its PICmicro® Microcontroller is intended and
 * supplied to you, the Company’s customer, for use solely and
 * exclusively on Microchip PICmicro Microcontroller products. The
 * software is owned by the Company and/or its supplier, and is
 * protected under applicable copyright laws. All rights are reserved.
 * Any use in violation of the foregoing restrictions may subject the
 * user to criminal sanctions under applicable laws, as well as to
 * civil liability for the breach of the terms and conditions of this
 * license.
 *
 * THIS SOFTWARE IS PROVIDED IN AN “AS IS” CONDITION. NO WARRANTIES,
 * WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED
 * TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. THE COMPANY SHALL NOT,
 * IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR
 * CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 *****************************************************************************/
 
#include <pconfig.h>


/* PIC18 SPI peripheral library header */


/* SSPSTAT REGISTER */

// Master SPI mode only

#define   SMPEND        0b10000000           // Input data sample at end of data out             
#define   SMPMID        0b00000000           // Input data sample at middle of data out


#define   MODE_00       0b00000000              // Setting for SPI bus Mode 0,0
//CKE           0x40                   // SSPSTAT register 
//CKP           0x00                   // SSPCON1 register 

#define   MODE_01       0b00000001              // Setting for SPI bus Mode 0,1
//CKE           0x00                   // SSPSTAT register 
//CKP           0x00                   // SSPCON1 register

#define   MODE_10       0b00000010              // Setting for SPI bus Mode 1,0
//CKE           0x40                   // SSPSTAT register
//CKP           0x10                   // SSPCON1 register

#define   MODE_11       0b00000011              // Setting for SPI bus Mode 1,1
//CKE           0x00                   // SSPSTAT register
//CKP           0x10                   // SSPCON1 register

/* SSPCON1 REGISTER */
#define   SSPENB        0b00100000           // Enable serial port and configures SCK, SDO, SDI

#define   SPI_FOSC_4    0b00000000              // SPI Master mode, clock = Fosc/4
#define   SPI_FOSC_16   0b00000001              // SPI Master mode, clock = Fosc/16
#define   SPI_FOSC_64   0b00000010              // SPI Master mode, clock = Fosc/64
#define   SPI_FOSC_TMR2 0b00000011              // SPI Master mode, clock = TMR2 output/2
#define   SLV_SSON      0b00000100              // SPI Slave mode, /SS pin control enabled
#define   SLV_SSOFF     0b00000101              // SPI Slave mode, /SS pin control disabled
//************************************************************************************************//

/*  25Cxxx EEPROM instruction set */
#define   SPI_WREN          6              // write enable latch
#define   SPI_WRDI          4              // reset the write enable latch
#define   SPI_RDSR          5              // read status register
#define   SPI_WRSR          1              // write status register
#define   SPI_READ          3              // read data from memory
#define   SPI_WRITE         2              // write data to memory

/*  Bits within status register of 25Cxxx */
#define   WIP           0              // write in progress status
#define   WEL           1              // write enable latch status
#define   BP0           2              // block protection bit status
#define   BP1           3              // block protection bit status


/* FUNCTION PROTOTYPES */

/* These devices have two SPI modules */
#if defined (SPI_V2) || defined (SPI_V3) || defined (SPI_V5) || defined (SPI_V5_1) || defined (SPI_V5_2) || defined (SPI_V6)


/* ***** SPI1 ***** */

#define  CloseSPI 		CloseSPI1

#define  DataRdySPI 	DataRdySPI1

#define  ReadSPI        ReadSPI1

/**************************************************************************
Macro       : EnableIntSPI1
 
Description : Enables SPIx Interrupt
 
Arguments   : None
 
Remarks     : This macro sets SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define EnableIntSPI1                   (PIE1bits.SSP1IE = 1)

/**************************************************************************
Macro       : DisableIntSPI1

Description : This macro disables the SPI Interrupt
 
Arguments   : None
 
Remarks     : This macro clears SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define DisableIntSPI1                  (PIE1bits.SSP1IE = 0)

/**************************************************************************
Macro       : SetPriorityIntSPI1(priority)
 
Description : This macro sets the priority level for SPI interrupt
 
Arguments   : priority - This input parameter is the level of interrupt priority.
		* 0 -- Low priority (Default Value)
		* 1 -- High Priority
		
Remarks     : None 
***************************************************************************/
#define SetPriorityIntSPI1(priority)     (IPR1bits.SSP1IP = priority)

/*******************************************************************
Macro       : SPI1_Clear_Intr_Status_Bit

Description : Macro to Clear external Interrupt Status bit 

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI1_Clear_Intr_Status_Bit     (PIR1bits.SSP1IF = 0)

/*******************************************************************
Macro       : SPI1_Intr_Status

Description : Macro to Return SPI Interrupt Status  

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI1_Intr_Status     (PIR1bits.SSP1IF)

/**************************************************************************
Macro       : SPI1_Clear_Recv_OV

Description : macro clears Receive Overflow flag
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  SPI1_Clear_Recv_OV    SSP1CONbits.SSPOV = 0

/*********************************************************************
Macro  	:	CloseSPI1()

Include        : 	spi.h 

Description : 	This Macro turns off the SPI module 

Arguments   : 	None 

Return Value: 	None 

Remarks      : 	This Macro disables the SPI module.
*********************************************************************/
#define  CloseSPI1()    (SSP1CON1 &=0xDF)

/************************************************************************
Macro :  DataRdySPI1() 

Include            : spi.h 

Description        : This Macro provides status back to user if SSPxBUF
			register contain data. 
                     
Arguments          : None 

Remarks            : This Macro determines if there is any byte to read from
			SSPxBUF register.
*************************************************************************/
#define  DataRdySPI1()  (SSP1STATbits.BF)

/**************************************************************************
Macro       : getcSPI1

Description : macro is identical to ReadSPI1,#define to ReadSPI1 in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  getcSPI1  ReadSPI1
#define  getcSPI   getcSPI1

#define OpenSPI OpenSPI1

#define WriteSPI WriteSPI1

/**************************************************************************
Macro       : putcSPI1

Description : macro is identical to WriteSPI1,#define to WriteSPI1 in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  putcSPI1  WriteSPI1
#define  putcSPI putcSPI1

#define getsSPI getsSPI1

#define putsSPI putsSPI1



void OpenSPI1(  unsigned char sync_mode,
                unsigned char bus_mode,
                unsigned char smp_phase );

signed char WriteSPI1(  unsigned char data_out );

void getsSPI1(  unsigned char *rdptr,  unsigned char length );

void putsSPI1(  unsigned char *wrptr );

unsigned char ReadSPI1( void );

#endif
/* ***** SPI2 ***** */

#if defined (SPI_V3) || defined (SPI_V5) || defined (SPI_V5_1) || defined (SPI_V6)

#if defined (SPI_V3) || defined (SPI_V5) 
/**************************************************************************
Macro       : EnableIntSPI2
 
Description : Enables SPIx Interrupt
 
Arguments   : None
 
Remarks     : This macro sets SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define EnableIntSPI2                   (PIE3bits.SSP2IE = 1)

/**************************************************************************
Macro       : DisableIntSPI2

Description : This macro disables the SPI Interrupt
 
Arguments   : None
 
Remarks     : This macro clears SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define DisableIntSPI2                  (PIE3bits.SSP2IE = 0)

/**************************************************************************
Macro       : SetPriorityIntSPI2(priority)
 
Description : This macro sets the priority level for SPI interrupt
 
Arguments   : priority - This input parameter is the level of interrupt priority.
		* 0 -- Low priority (Default Value)
		* 1 -- High Priority
		
Remarks     : None 
***************************************************************************/
#define SetPriorityIntSPI2(priority)     (IPR3bits.SSP2IP = priority)

/*******************************************************************
Macro       : SPI2_Clear_Intr_Status_Bit

Description : Macro to Clear external Interrupt Status bit 

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI2_Clear_Intr_Status_Bit     (PIR3bits.SSP2IF = 0)

/*******************************************************************
Macro       : SPI2_Intr_Status

Description : Macro to Return SPI Interrupt Status  

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI2_Intr_Status     (PIR3bits.SSP2IF)

#elif defined (SPI_V5_1) || defined (SPI_V6)

/**************************************************************************
Macro       : EnableIntSPI2
 
Description : Enables SPIx Interrupt
 
Arguments   : None
 
Remarks     : This macro sets SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define EnableIntSPI2                   (PIE2bits.SSP2IE = 1)

/**************************************************************************
Macro       : DisableIntSPI2

Description : This macro disables the SPI Interrupt
 
Arguments   : None
 
Remarks     : This macro clears SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define DisableIntSPI2                  (PIE2bits.SSP2IE = 0)

/**************************************************************************
Macro       : SetPriorityIntSPI2(priority)
 
Description : This macro sets the priority level for SPI interrupt
 
Arguments   : priority - This input parameter is the level of interrupt priority.
		* 0 -- Low priority (Default Value)
		* 1 -- High Priority
		
Remarks     : None 
***************************************************************************/
#define SetPriorityIntSPI2(priority)     (IPR2bits.SSP2IP = priority)

/*******************************************************************
Macro       : SPI2_Clear_Intr_Status_Bit

Description : Macro to Clear external Interrupt Status bit 

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI2_Clear_Intr_Status_Bit     (PIR2bits.SSP2IF = 0)

/*******************************************************************
Macro       : SPI2_Intr_Status

Description : Macro to Return SPI Interrupt Status  

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI2_Intr_Status     (PIR2bits.SSP2IF)

#endif


/**************************************************************************
Macro       : SPI2_Clear_Recv_OV

Description : macro clears Receive Overflow flag
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  SPI2_Clear_Recv_OV    SSP2CONbits.SSPOV = 0

/*********************************************************************
Macro  	:	CloseSPI2()

Include        : 	spi.h 

Description : 	This Macro turns off the SPI module 

Arguments   : 	None 

Return Value: 	None 

Remarks      : 	This Macro disables the SPI module.
*********************************************************************/
#define  CloseSPI2()      (SSP2CON1 &=0xDF)

/************************************************************************
Macro :  DataRdySPI2() 

Include            : spi.h 

Description        : This Macro provides status back to user if SSPxBUF
			register contain data. 
                     
Arguments          : None 

Remarks            : This Macro determines if there is any byte to read from
			SSPxBUF register.
*************************************************************************/
#define  DataRdySPI2()    (SSP2STATbits.BF)

/**************************************************************************
Macro       : getcSPI2

Description : macro is identical to ReadSPI2,#define to ReadSPI2 in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  getcSPI2  ReadSPI2

/**************************************************************************
Macro       : putcSPI2

Description : macro is identical to WriteSPI2,#define to WriteSPI2 in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  putcSPI2  WriteSPI2


void OpenSPI2(  unsigned char sync_mode,
                unsigned char bus_mode,
                unsigned char smp_phase );

signed char WriteSPI2(  unsigned char data_out );

void getsSPI2(  unsigned char *rdptr,  unsigned char length );

void putsSPI2(  unsigned char *wrptr );

unsigned char ReadSPI2( void );

#endif // v2 and v3

#if defined (SPI_V1) || defined (SPI_V4)

/* ***** SPI ***** */

/**************************************************************************
Macro       : EnableIntSPI
 
Description : Enables SPIx Interrupt
 
Arguments   : None
 
Remarks     : This macro sets SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define EnableIntSPI                   (PIE1bits.SSPIE = 1)

/**************************************************************************
Macro       : DisableIntSPI

Description : This macro disables the SPI Interrupt
 
Arguments   : None
 
Remarks     : This macro clears SPI Interrupt Enable bit of Interrupt Enable 
		Control register.
***************************************************************************/ 
#define DisableIntSPI                  (PIE1bits.SSPIE = 0)

/**************************************************************************
Macro       : SetPriorityIntSPI(priority)
 
Description : This macro sets the priority level for SPI interrupt
 
Arguments   : priority - This input parameter is the level of interrupt priority.
		* 0 -- Low priority (Default Value)
		* 1 -- High Priority
		
Remarks     : None 
***************************************************************************/
#define SetPriorityIntSPI(priority)     (IPR1bits.SSPIP = priority)

/*******************************************************************
Macro       : SPI_Clear_Intr_Status_Bit

Description : Macro to Clear external Interrupt Status bit 

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI_Clear_Intr_Status_Bit     (PIR1bits.SSPIF = 0)

/*******************************************************************
Macro       : SPI_Intr_Status

Description : Macro to Return SPI Interrupt Status  

Arguments   : None 

Remarks     : None 
*******************************************************************/
#define SPI_Intr_Status     (PIR1bits.SSPIF)

/**************************************************************************
Macro       : SPI_Clear_Recv_OV

Description : macro clears Receive Overflow flag
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  SPI_Clear_Recv_OV    SSPCONbits.SSPOV = 0



/*********************************************************************
Macro  	:	CloseSPI()

Include        : 	spi.h 

Description : 	This Macro turns off the SPI module 

Arguments   : 	None 

Return Value: 	None 

Remarks      : 	This Macro disables the SPI module.
*********************************************************************/
#define  CloseSPI()    (SSPCON1 &=0xDF)

/************************************************************************
Macro :  DataRdySPI() 

Include            : spi.h 

Description        : This Macro provides status back to user if SSPxBUF
			register contain data. 
                     
Arguments          : None 

Remarks            : This Macro determines if there is any byte to read from
			SSPxBUF register.
*************************************************************************/
#define  DataRdySPI()    (SSPSTATbits.BF)

/**************************************************************************
Macro       : getcSPI

Description : macro is identical to ReadSPI,#define to ReadSPI in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  getcSPI  ReadSPI

/**************************************************************************
Macro       : putcSPI

Description : macro is identical to WriteSPI,#define to WriteSPI in spi.h
 
Arguments   : None
 
Remarks     : None 
***************************************************************************/
#define  putcSPI  WriteSPI


void OpenSPI(  unsigned char sync_mode,
               unsigned char bus_mode,
               unsigned char smp_phase );

signed char WriteSPI(  unsigned char data_out );

void getsSPI(  unsigned char *rdptr,  unsigned char length );

void putsSPI(  unsigned char *wrptr );

unsigned char ReadSPI( void );

#endif 


#endif  /* __SPI_H */

