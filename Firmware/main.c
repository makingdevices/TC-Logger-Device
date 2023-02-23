/********************************************************************

Making Devices - 2023 CDC FOR PIC18F14K50
https://makingdevices.com/links/

*********************************************************************/

/********************************************************************
 FileName:      main.c
 Dependencies:  See INCLUDES section
 Processor:     PIC18F14K50 USB Microcontroller
 Hardware:      This demo is natively intended to be used on Microchip USB demo
                boards supported by the MCHPFSUSB stack.  See release notes for
                support matrix.  This demo can be modified for use on other 
                hardware platforms.
 Complier:      Microchip C18 (for PIC18)
 Company:       Microchip Technology, Inc.

 Software License Agreement:
 THIS SOFTWARE IS PROVIDED IN AN "AS IS" CONDITION. NO WARRANTIES,
 WHETHER EXPRESS, IMPLIED OR STATUTORY, INCLUDING, BUT NOT LIMITED
 TO, IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 PARTICULAR PURPOSE APPLY TO THIS SOFTWARE. THE COMPANY SHALL NOT,
 IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL OR
 CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.

/** INCLUDES *******************************************************/
#include "./USB/usb.h"
#include "./USB/usb_function_cdc.h"
#include "spi.h"

#include "HardwareProfile.h"

/** CONFIGURATION **************************************************/

#if defined(LOW_PIN_COUNT_USB_DEVELOPMENT_KIT)
        #pragma config CPUDIV = NOCLKDIV
        #pragma config USBDIV = OFF
        #pragma config FOSC   = HS
        #pragma config PLLEN  = ON
        #pragma config FCMEN  = OFF
        #pragma config IESO   = OFF
        #pragma config PWRTEN = OFF
        #pragma config BOREN  = ON
        #pragma config BORV   = 30
        #pragma config WDTEN  = OFF
        #pragma config WDTPS  = 32768
        #pragma config MCLRE  = OFF
        #pragma config HFOFST = OFF
        #pragma config STVREN = ON
        #pragma config LVP    = OFF
        #pragma config XINST  = OFF
        #pragma config BBSIZ  = OFF
        #pragma config CP0    = OFF
        #pragma config CP1    = OFF
        #pragma config CPB    = OFF
        #pragma config WRT0   = OFF
        #pragma config WRT1   = OFF
        #pragma config WRTB   = OFF
        #pragma config WRTC   = OFF
        #pragma config EBTR0  = OFF
        #pragma config EBTR1  = OFF
        #pragma config EBTRB  = OFF       
    #else
        #error No hardware board defined, see "HardwareProfile.h" and __FILE__
    #endif

/** I N C L U D E S **********************************************************/

#include "GenericTypeDefs.h"
#include "Compiler.h"
#include "usb_config.h"
#include "USB/usb_device.h"
#include "USB/usb.h"

/** V A R I A B L E S *******************************************************/
#if defined(__18CXX)
    #pragma udata				
#endif

char USB_In_Buffer[64];         //USB IN BUFFER
char USB_IDN_Buffer[] = {'C','D','C',' ','T','C',' ','L','O','G','G','E','R',' ','D','E','V','I','C','E',' ','B','Y',' ','M','A','K','I','N','G',' ','D','E','V','I','C','E','S',' ','H','W',':','1','.','2',' ','F','W',':','1','.','0','2',' ','\n'};
char USB_Out_Buffer[16];		//USB OUT BUFFER
char SPI_response[8];  
char SPI_lastmessage[8];
char spi_state = 0;
char length;
int LED1 = 0;
int LED2 = 0;
float convtemperature = 0;
char com_var = 0;

/** P R I V A T E  P R O T O T Y P E S ***************************************/
static void InitializeSystem(void);
void ProcessIO(void);
void USBDeviceTasks(void);
void YourHighPriorityISRCode();
void YourLowPriorityISRCode();
void USBCBSendResume(void);
void UserInit(void);
/*
/** VECTOR REMAPPING ***********************************************/
#if defined(__18CXX)
	//On PIC18 devices, addresses 0x00, 0x08, and 0x18 are used for
	//the reset, high priority interrupt, and low priority interrupt
	//vectors.  However, the Microchip HID bootloader occupies the
	//0x00-0xFFF program memory region.  Therefore, the bootloader code remaps 
	//these vectors to new locations as indicated below.  This remapping is 
	//only necessary if you wish to be able to (optionally) program the hex file 
	//generated from this project with the USB bootloader.  

	#define REMAPPED_RESET_VECTOR_ADDRESS			0x0040
	#define REMAPPED_HIGH_INTERRUPT_VECTOR_ADDRESS	0x0048
	#define REMAPPED_LOW_INTERRUPT_VECTOR_ADDRESS	0x0050
	#define APP_VERSION_ADDRESS                     0x0056 //Fixed location, so the App FW image version can be read by the bootloader.
	#define APP_SIGNATURE_ADDRESS                   0x0046 //Signature location that must be kept at blaknk value (0xFFFF) in this project (has special purpose for bootloader).

    //--------------------------------------------------------------------------
    //Application firmware image version values, as reported to the bootloader
    //firmware.  These are useful so the bootloader can potentially know if the
    //user is trying to program an older firmware image onto a device that
    //has already been programmed with a with a newer firmware image.
    //Format is APP_FIRMWARE_VERSION_MAJOR.APP_FIRMWARE_VERSION_MINOR.
    //The valid minor version is from 00 to 99.  Example:
    //if APP_FIRMWARE_VERSION_MAJOR == 1, APP_FIRMWARE_VERSION_MINOR == 1,
    //then the version is "1.01"

    #define APP_FIRMWARE_VERSION_MAJOR  1   //valid values 0-255
    #define APP_FIRMWARE_VERSION_MINOR  2   //valid values 0-99
	#define APP_HARDWARE_VERSION_MAJOR  0x01   //valid values 0-255
    #define APP_HARDWARE_VERSION_MINOR  0x02   //valid values 0-99
    //--------------------------------------------------------------------------
	
	#pragma romdata AppVersionAndSignatureSection = APP_VERSION_ADDRESS
	ROM unsigned char AppVersion[2] = {APP_FIRMWARE_VERSION_MINOR, APP_FIRMWARE_VERSION_MAJOR};
	#pragma romdata AppSignatureSection = APP_SIGNATURE_ADDRESS
	ROM unsigned short int SignaturePlaceholder = 0xFFFF;
	
	#pragma code HIGH_INTERRUPT_VECTOR = 0x08
	void High_ISR (void)
	{
	     _asm goto REMAPPED_HIGH_INTERRUPT_VECTOR_ADDRESS _endasm
	}
	#pragma code LOW_INTERRUPT_VECTOR = 0x18
	void Low_ISR (void)
	{
	     _asm goto REMAPPED_LOW_INTERRUPT_VECTOR_ADDRESS _endasm
	}
	extern void _startup (void);        // See c018i.c in your C18 compiler dir
	#pragma code REMAPPED_RESET_VECTOR = REMAPPED_RESET_VECTOR_ADDRESS
	void _reset (void)
	{
	    _asm goto _startup _endasm
	}
	#pragma code REMAPPED_HIGH_INTERRUPT_VECTOR = REMAPPED_HIGH_INTERRUPT_VECTOR_ADDRESS
	void Remapped_High_ISR (void)
	{
	     _asm goto YourHighPriorityISRCode _endasm
	}
	#pragma code REMAPPED_LOW_INTERRUPT_VECTOR = REMAPPED_LOW_INTERRUPT_VECTOR_ADDRESS
	void Remapped_Low_ISR (void)
	{
	     _asm goto YourLowPriorityISRCode _endasm
	}
	#pragma code
	
	
	//These are your actual interrupt handling routines.
	#pragma interrupt YourHighPriorityISRCode
	void YourHighPriorityISRCode()
	{
		int i;
		//Check which interrupt flag caused the interrupt.
		//Service the interrupt
		//Clear the interrupt flag
		//Etc.
        #if defined(USB_INTERRUPT)
	        USBDeviceTasks();
        #endif
		
		if(INTCONbits.TMR0IF) //Timer0 interrupt
			{

				//We set the timer0 again
				TMR0H = 0x50;
				TMR0L = 0x38;
				INTCONbits.TMR0IF = 0; // reset overflow bit (for timer0).
				if(spi_state==0){  //If state == 0 we read first thermocouple
					LATCbits.LATC1=0;
					
					SPI_response[0] = ReadSPI();
					SPI_response[1] = ReadSPI();
					SPI_response[2] = ReadSPI();
					SPI_response[3] = ReadSPI();
	
					LATCbits.LATC1=1;
					spi_state = 1;
					
					for(i=0;i<4;i++){
						if(SPI_response[i]!=0x00){
							SPI_lastmessage[i] = SPI_response[i];
						}
					}
					
					if(LED1 < 2){
						if(((SPI_response[3]&0b00000111) > 0) || ((SPI_response[1]&0b00000001) > 0) ){ //LED brights if TC has an error
							LATCbits.LATC2=1;
							LED1 = 1;
						} else {
							LATCbits.LATC2=0;
							LED1 = 0;
						}
					} else if(LED1 == 2) {
						LATCbits.LATC2=1;
					} else LATCbits.LATC2=0;
					
				} else { //If state == 1 we read second thermocouple
	
					LATCbits.LATC0=0;
					SPI_response[4] = ReadSPI();
					SPI_response[5] = ReadSPI();
					SPI_response[6] = ReadSPI();
					SPI_response[7] = ReadSPI();
	
					LATCbits.LATC0=1;
					spi_state = 0;
					for(i=4;i<8;i++){
						if(SPI_response[i]!=0x00){
							SPI_lastmessage[i] = SPI_response[i];
						}
					}
					if(LED2 < 2){
						if(((SPI_response[7]&0b00000111) > 0) || ((SPI_response[5]&0b00000001) > 0) ){   //LED brights if TC has an error
							LATCbits.LATC3=1;
							LED2 = 1;
						} else {
							LATCbits.LATC3=0;
							LED2 = 0;
						}
					} else if(LED2 == 2) {
						LATCbits.LATC3=1;
					} else LATCbits.LATC3=0;
				}

			}	
	
	}	//This return will be a "retfie fast", since this is in a #pragma interrupt section 
	#pragma interruptlow YourLowPriorityISRCode
	void YourLowPriorityISRCode()
	{
		//Check which interrupt flag caused the interrupt.
		//Service the interrupt
		//Clear the interrupt flag
		//Etc.
	
	}	//This return will be a "retfie", since this is in a #pragma interruptlow section 

/** DECLARATIONS ***************************************************/
#if defined(__18CXX)
    #pragma code
#endif

/******************************************************************************
 * Function:        void main(void)
 *
 * Overview:        Main program entry point.
 *
 * Note:            None
 *****************************************************************************/
void Interrupts_enable(void) 
{    
  
	T0CONbits.T08BIT = 0; //60ms at 48Mhz. //TconvMAX31855 = 100ms
	T0CONbits.T0CS = 0;
	T0CONbits.PSA = 0;
	T0CONbits.T0PS2 = 0;
	T0CONbits.T0PS1 = 1;
	T0CONbits.T0PS0 = 1;
	TMR0H = 0x50;
	TMR0L = 0x38;
	T0CONbits.TMR0ON = 1;

	RCONbits.IPEN       = 1;    //Enable Interrupt Priorities
    INTCONbits.GIEL     = 1;    //Enable Low Priority Interrupt
    INTCONbits.GIEH     = 1;    //Enable high priority interrupts        
    INTCONbits.TMR0IE   = 1;    //Enable Timer0 Interrupt
	INTCONbits.T0IE     = 1;   
    INTCON2bits.TMR0IP  = 1;    //TMR0 set to low Priority Interrupt
    INTCONbits.TMR0IF = 0;  // T0 int flag bit cleared before starting
    T0CONbits.TMR0ON = 1;   // timer0 START
	INTCONbits.GIE = 1; 		   //Enable all unmasked interrupts   
} 

#if defined(__18CXX)
void main(void)
#else
int main(void)
#endif
{   
	InitializeSystem();
	Interrupts_enable();
	TRISC=0X00;
	LATCbits.LATC0=1;
	LATCbits.LATC1=1;
	TRISB=0b00111111;
	ANSELHbits.ANS10 = 0;
	OpenSPI(SPI_FOSC_16,MODE_00,SMPEND);

    while(1)
    {
        #if defined(USB_INTERRUPT)
            if(USB_BUS_SENSE && (USBGetDeviceState() == DETACHED_STATE))
            {
                USBDeviceAttach();
            }
        #endif

        #if defined(USB_POLLING)
		// Check bus status and service USB interrupts.
        USBDeviceTasks(); // Interrupt or polling method.  If using polling, must call
        				  // this function periodically.  This function will take care
        				  // of processing and responding to SETUP transactions 
        				  // (such as during the enumeration process when you first
        				  // plug in).  USB hosts require that USB devices should accept
        				  // and process SETUP packets in a timely fashion.  Therefore,
        				  // when using polling, this function should be called 
        				  // regularly (such as once every 1.8ms or faster** [see 
        				  // inline code comments in usb_device.c for explanation when
        				  // "or faster" applies])  In most cases, the USBDeviceTasks() 
        				  // function does not take very long to execute (ex: <100 
        				  // instruction cycles) before it returns.
        #endif
    				  

		// Application-specific tasks.
		// Application related code may be added here, or in the ProcessIO() function.
        ProcessIO();        
    }//end while
}//end main

/********************************************************************
 * Function:        float bin2tempint(unsigned char binary, unsigned char binary2)
 *					float bin2tempext(unsigned char binary, unsigned char binary2)
 *
 * Overview:        Converts the messages from the MAX31855 to float.
 *                  
 *                  
 *
 *                  
 *                                    
 *
 * Note:            None
 *******************************************************************/

float bin2temp(unsigned char binary,unsigned char binary2, int mode){
    float temperature = 0;
	if(mode == 1) {
	    if((binary&0b00000001) == 0b00000001){
	    //thermocouple is open circuit
	        temperature = -300;
	        return temperature;
		}
		if((binary&0b00000010) == 0b00000010){
	    //thermocouple is short-circuit to GND
	        temperature = -301;
	        return temperature;
		}
		if((binary&0b00000100) == 0b00000100){
	        //thermocouple is short-circuit to Vcc
	        temperature = -302;
	        return temperature;
		}
	} else {
	    if((binary&0b00000001) == 1){
	        temperature = -303;
	        return temperature;
		}

		mode = 16;
	    if((binary&0b00000100) == 0b100) temperature += 0.25;
	    if((binary&0b00001000) == 0b1000)temperature += 0.5;
	}   //MODE SHOULD BE 1 OR 2
	    if((binary&0b00010000) == 0b00010000)temperature += (0.0625*mode);
	    if((binary&0b00100000) == 0b00100000)temperature += (0.125*mode);
	    if((binary&0b01000000) == 0b01000000)temperature += (0.25*mode);
	    if((binary&0b10000000) == 0b10000000)temperature += (0.5*mode);
		if((binary2&0b00000001)  == 0b00000001) temperature += (1*mode);
	    if((binary2&0b00000010) == 0b00000010)temperature += (2*mode);
	    if((binary2&0b00000100) == 0b00000100)temperature += (4*mode);
	    if((binary2&0b00001000) == 0b00001000)temperature += (8*mode);
	    if((binary2&0b00010000) == 0b00010000)temperature += (16*mode);
	    if((binary2&0b00100000) == 0b00100000)temperature += (32*mode);
	    if((binary2&0b01000000) == 0b01000000)temperature += (64*mode);
	    if((binary2&0b10000000) == 0b10000000)temperature = temperature*(-1);
		return temperature;
}
/********************************************************************
 * Function:        ftoa(unsigned char *buf, float f)
 *
 * Overview:        Float to String
 *                  
 *                  
 *
 *                  
 *                                    
 *
 * Note:            None
 *******************************************************************/

char ftoa(unsigned char *buf, float f) {
        unsigned int rem;
        unsigned char *s,length=0;
        int i,j;
 
        i = (int)((float)f*100);
 
        s = buf;
        if (i == 0){            //print 0.0 with null termination here
                *s++ = '0';
                *s++ = '.';
                *s++ = '0';
				*s++ = '0';
                *s=0;                   //null terminate the string
        } else {       
                if (i < 0) {
                        *buf++ = '-';
                        s = buf;
                        i = -i;
                }
                //while-loop to "decode" the long integer to ASCII by append '0', string in reverse manner
                //If it is an integer of 124 -> string = {'4', '2', '1'}
                while (i) {
                        ++length;
                        rem = i % 10;
                        *s++ = rem + '0';
                        i /= 10;
                }
                //reverse the string in this for-loop, string became {'1', '2', '4'} after this for-loop
                for(rem=0; ((unsigned char)rem)<length/2; rem++) {
                        *(buf+length) = *(buf+((unsigned char)rem));
                        *(buf+((unsigned char)rem)) = *(buf+(length-((unsigned char)rem)-1));
                        *(buf+(length-((unsigned char)rem)-1)) = *(buf+length);
                }
 
                /* Take care of the special case of 0.x if length ==1*/
                if(length==1) {
                        *(buf+3) = *buf;
                        *buf = '0';
                        *(buf+1) = '.';
						*(buf+2) = '0';
                        *(s+3)=0;                       //null terminate
				} else {
                        *(buf+length) = *(buf+length-1);
						*(buf+length-1) = *(buf+length-2);
                        *(buf+length-2)='.';
                        *(s+2)=0;                       //null terminate
                }
        }
		return (length+1);
 }

/********************************************************************
 * Function:        static void InitializeSystem(void)
 *
 * Overview:        InitializeSystem is a centralize initialization
 *                  routine. All required USB initialization routines
 *                  are called from here.
 *
 *                  User application initialization routine should
 *                  also be called from here.                  
 *
 * Note:            None
 *******************************************************************/
static void InitializeSystem(void)
{
    #if (defined(__18CXX) & !defined(PIC18F87J50_PIM) & !defined(PIC18F97J94_FAMILY))
        ADCON1 |= 0x0F;                 // Default all pins to digital

    #if defined(PIC18F45K50_FAMILY)
        //Configure oscillator settings for clock settings compatible with USB 
        //operation.  Note: Proper settings depends on USB speed (full or low).
        #if(USB_SPEED_OPTION == USB_FULL_SPEED)
            OSCTUNE = 0x80; //3X PLL ratio mode selected
            OSCCON = 0x70;  //Switch to 16MHz HFINTOSC
            OSCCON2 = 0x10; //Enable PLL, SOSC, PRI OSC drivers turned off
            while(OSCCON2bits.PLLRDY != 1);   //Wait for PLL lock
            *((unsigned char*)0xFB5) = 0x90;  //Enable active clock tuning for USB operation
        #endif
        //Configure all I/O pins for digital mode (except RA0/AN0 which has POT on demo board)
        ANSELA = 0x01;
        ANSELB = 0x00;
        ANSELC = 0x00;
        ANSELD = 0x00;
        ANSELE = 0x00;
    #endif
    
//	The USB specifications require that USB peripheral devices must never source
//	current onto the Vbus pin.  Additionally, USB peripherals should not source
//	current on D+ or D- when the host/hub is not actively powering the Vbus line.
//	When designing a self powered (as opposed to bus powered) USB peripheral
//	device, the firmware should make sure not to turn on the USB module and D+
//	or D- pull up resistor unless Vbus is actively powered.  Therefore, the
//	firmware needs some means to detect when Vbus is being powered by the host.
//	A 5V tolerant I/O pin can be connected to Vbus (through a resistor), and
// 	can be used to detect when Vbus is high (host actively powering), or low
//	(host is shut down or otherwise not supplying power).  The USB firmware
// 	can then periodically poll this I/O pin to know when it is okay to turn on
//	the USB module/D+/D- pull up resistor.  When designing a purely bus powered
//	peripheral device, it is not possible to source current on D+ or D- when the
//	host is not actively providing power on Vbus. Therefore, implementing this
//	bus sense feature is optional.  This firmware can be made to use this bus
//	sense feature by making sure "USE_USB_BUS_SENSE_IO" has been defined in the
//	HardwareProfile.h file.    

    #if defined(USE_USB_BUS_SENSE_IO)
    tris_usb_bus_sense = INPUT_PIN; // See HardwareProfile.h
    #endif
    
//	If the host PC sends a GetStatus (device) request, the firmware must respond
//	and let the host know if the USB peripheral device is currently bus powered
//	or self powered.  See chapter 9 in the official USB specifications for details
//	regarding this request.  If the peripheral device is capable of being both
//	self and bus powered, it should not return a hard coded value for this request.
//	Instead, firmware should check if it is currently self or bus powered, and
//	respond accordingly.  If the hardware has been configured like demonstrated
//	on the PICDEM FS USB Demo Board, an I/O pin can be polled to determine the
//	currently selected power source.  On the PICDEM FS USB Demo Board, "RA2" 
//	is used for	this purpose.  If using this feature, make sure "USE_SELF_POWER_SENSE_IO"
//	has been defined in HardwareProfile - (platform).h, and that an appropriate I/O pin 
//  has been mapped	to it.

    #if defined(USE_SELF_POWER_SENSE_IO)
    tris_self_power = INPUT_PIN;	// See HardwareProfile.h
    #endif
    
    UserInit();

    USBDeviceInit();	//usb_device.c.  Initializes USB module SFRs and firmware
    					//variables to known states.
}//end InitializeSystem


/******************************************************************************
 * Function:        void UserInit(void)
 *
 * Overview:        This routine should take care of all of the user
 *                  initialization that is required.
 *
 * Note:            
 *
 *****************************************************************************/
void UserInit(void)
{

}//end UserInit

/********************************************************************
 * Function:        void ProcessIO(void)
 *
 * Overview:        This function is a place holder for other user
 *                  routines. It is a mixture of both USB and
 *                  non-USB tasks.
 *
 * Note:            None
 *******************************************************************/
void ProcessIO(void)
{   
	int x, i,meas_1,meas_2,meas_3,g;
    BYTE numBytesRead;
    // User Application USB tasks
    if((USBDeviceState < CONFIGURED_STATE)||(USBSuspendControl==1)) return;

    if(USBUSARTIsTxTrfReady())
    {
		numBytesRead = getsUSBUSART(USB_Out_Buffer,32);
		if(numBytesRead != 0)
		{
			com_var=9;
			if(USB_Out_Buffer[0]==':' && USB_Out_Buffer[1]=='M' && USB_Out_Buffer[2]=='E' && USB_Out_Buffer[3]=='A'&& USB_Out_Buffer[4]=='S'){
				if(USB_Out_Buffer[5]==':' && USB_Out_Buffer[6]=='T' && USB_Out_Buffer[7]=='C' && USB_Out_Buffer[8]=='1'){
					if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='I' && USB_Out_Buffer[11]=='N' && USB_Out_Buffer[12]=='T' && USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						meas_1 = 3;
						meas_2 = 2;
						meas_3 = 1;
						com_var = 0;
					} else if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='E' && USB_Out_Buffer[11]=='X' && USB_Out_Buffer[12]=='T' && USB_Out_Buffer[13]=='?' && USB_Out_Buffer[14]=='\n'){
						meas_1 = 1;
						meas_2 = 0;
						meas_3 = 2;
						com_var = 0;
					} else if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='L' && USB_Out_Buffer[11]=='E' && USB_Out_Buffer[12]=='D' && USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						com_var = 1;
						if(LED1 == 1 || LED1 == 2){
							USB_In_Buffer[0] = '1';
						}else USB_In_Buffer[0] = '0';
					}
						
				} else if(USB_Out_Buffer[5]==':' && USB_Out_Buffer[6]=='T' && USB_Out_Buffer[7]=='C' && USB_Out_Buffer[8]=='2'){
					if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='I' && USB_Out_Buffer[11]=='N' && USB_Out_Buffer[12]=='T' && USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						meas_1 = 7;
						meas_2 = 6;
						meas_3 = 1;
						com_var = 0;
					} else if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='E' && USB_Out_Buffer[11]=='X' && USB_Out_Buffer[12]=='T' && USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						meas_1 = 5;
						meas_2 = 4;
						meas_3 = 2;
						com_var = 0;
					} else if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='L' && USB_Out_Buffer[11]=='E' && USB_Out_Buffer[12]=='D' && USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						com_var = 1;
						if(LED2 == 1 || LED2 == 2){
							USB_In_Buffer[0] = '1';
						}else USB_In_Buffer[0] = '0';
					}
				}
			}
			if(USB_Out_Buffer[0]==':' && USB_Out_Buffer[1]=='S' && USB_Out_Buffer[2]=='E' && USB_Out_Buffer[3]=='T'){
				if(USB_Out_Buffer[4]==':' && USB_Out_Buffer[5]=='T' && USB_Out_Buffer[6]=='C' && USB_Out_Buffer[7]=='1'){
					if(USB_Out_Buffer[8]==':' && USB_Out_Buffer[9]=='L' && USB_Out_Buffer[10]=='E' && USB_Out_Buffer[11]=='D'&& USB_Out_Buffer[12]==' '){
						if(USB_Out_Buffer[13]=='A' && USB_Out_Buffer[14]=='U' && USB_Out_Buffer[15]=='T' && USB_Out_Buffer[16]=='O'&& USB_Out_Buffer[17]=='\n'){
							LED1 = 0;
							USB_In_Buffer[0] = 'A';
							USB_In_Buffer[1] = 'U';
							USB_In_Buffer[2] = 'T';
							USB_In_Buffer[3] = 'O';
							com_var = 2;
						}else if(USB_Out_Buffer[13]=='1'&& USB_Out_Buffer[14]=='\n'){
							LED1 = 2;
							USB_In_Buffer[0] = '1';
							com_var = 1;
						}else if(USB_Out_Buffer[13]=='0'&& USB_Out_Buffer[14]=='\n'){
							LED1 = 3;
							USB_In_Buffer[0] = '0';
							com_var = 1;
						}	
					}
				}
				if(USB_Out_Buffer[4]==':' && USB_Out_Buffer[5]=='T' && USB_Out_Buffer[6]=='C' && USB_Out_Buffer[7]=='2'){
					if(USB_Out_Buffer[8]==':' && USB_Out_Buffer[9]=='L' && USB_Out_Buffer[10]=='E' && USB_Out_Buffer[11]=='D'&& USB_Out_Buffer[12]==' '){
						if(USB_Out_Buffer[13]=='A' && USB_Out_Buffer[14]=='U' && USB_Out_Buffer[15]=='T' && USB_Out_Buffer[16]=='O'&& USB_Out_Buffer[17]=='\n'){
							LED2 = 0;
							USB_In_Buffer[0] = 'A';
							USB_In_Buffer[1] = 'U';
							USB_In_Buffer[2] = 'T';
							USB_In_Buffer[3] = 'O';
							com_var = 2;
						}else if(USB_Out_Buffer[13]=='1'&& USB_Out_Buffer[14]=='\n'){
							LED2 = 2;
							USB_In_Buffer[0] = '1';
							com_var = 1;
						}else if(USB_Out_Buffer[13]=='0'&& USB_Out_Buffer[14]=='\n'){
							LED2 = 3;
							USB_In_Buffer[0] = '0';
							com_var = 1;
						}	
					}
				}
			}
			if(USB_Out_Buffer[0]==':' && USB_Out_Buffer[1]=='M' && USB_Out_Buffer[2]=='O' && USB_Out_Buffer[3]=='D' && USB_Out_Buffer[4]=='E'){
				if(USB_Out_Buffer[5]==':' && USB_Out_Buffer[6]=='T' && USB_Out_Buffer[7]=='C' && USB_Out_Buffer[8]=='1'){
					if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='L' && USB_Out_Buffer[11]=='E' && USB_Out_Buffer[12]=='D'&& USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						if(LED1<2){
							USB_In_Buffer[0] = 'A';
							USB_In_Buffer[1] = 'U';
							USB_In_Buffer[2] = 'T';
							USB_In_Buffer[3] = 'O';
							com_var = 2;
						} else {
							USB_In_Buffer[0] = 'M';
							USB_In_Buffer[1] = 'A';
							USB_In_Buffer[2] = 'N';
							USB_In_Buffer[3] = 'U';
							USB_In_Buffer[4] = 'A';
							USB_In_Buffer[5] = 'L';
							com_var = 3;
						}
					}	
				}else if(USB_Out_Buffer[5]==':' && USB_Out_Buffer[6]=='T' && USB_Out_Buffer[7]=='C' && USB_Out_Buffer[8]=='2'){
					if(USB_Out_Buffer[9]==':' && USB_Out_Buffer[10]=='L' && USB_Out_Buffer[11]=='E' && USB_Out_Buffer[12]=='D'&& USB_Out_Buffer[13]=='?'&& USB_Out_Buffer[14]=='\n'){
						if(LED2<2){
							USB_In_Buffer[0] = 'A';
							USB_In_Buffer[1] = 'U';
							USB_In_Buffer[2] = 'T';
							USB_In_Buffer[3] = 'O';
							com_var = 2;
						} else {
							USB_In_Buffer[0] = 'M';
							USB_In_Buffer[1] = 'A';
							USB_In_Buffer[2] = 'N';
							USB_In_Buffer[3] = 'U';
							USB_In_Buffer[4] = 'A';
							USB_In_Buffer[5] = 'L';
							com_var = 3;
						}
					}	
				}
			}
			if(USB_Out_Buffer[0]==':' && USB_Out_Buffer[1]=='C' && USB_Out_Buffer[2]=='O' && USB_Out_Buffer[3]=='N' && USB_Out_Buffer[4]=='F'&& USB_Out_Buffer[5]=='I'&& USB_Out_Buffer[6]=='G'){
				if(USB_Out_Buffer[7]==':' && USB_Out_Buffer[8]=='A' && USB_Out_Buffer[9]=='P' && USB_Out_Buffer[10]=='P'&& USB_Out_Buffer[11]=='?'&& USB_Out_Buffer[12]=='\n'){
						USB_In_Buffer[0] = '1';
						USB_In_Buffer[1] = '.';
						USB_In_Buffer[2] = '0';
						USB_In_Buffer[3] = '2';
						com_var = 2;
				}else if(USB_Out_Buffer[7]==':' && USB_Out_Buffer[8]=='H' && USB_Out_Buffer[9]=='W'&& USB_Out_Buffer[10]=='?'&& USB_Out_Buffer[11]=='\n'){
						USB_In_Buffer[0] = '1';
						USB_In_Buffer[1] = '.';
						USB_In_Buffer[2] = '2';
						com_var = 4;
				}
			}
			if(USB_Out_Buffer[0]==':' && USB_Out_Buffer[1]=='h' && USB_Out_Buffer[2]=='e' && USB_Out_Buffer[3]=='l' && USB_Out_Buffer[4]=='l'&& USB_Out_Buffer[5]=='o'&& USB_Out_Buffer[6]=='?'&& USB_Out_Buffer[7]=='\n'){
					USB_In_Buffer[0] = 'h';
					USB_In_Buffer[1] = 'e';
					USB_In_Buffer[2] = 'l';
					USB_In_Buffer[3] = 'l';
					USB_In_Buffer[4] = 'o';
					com_var = 6;
			}			
			if(USB_Out_Buffer[0]=='*' && USB_Out_Buffer[1]=='I' && USB_Out_Buffer[2]=='D' && USB_Out_Buffer[3]=='N' && USB_Out_Buffer[4]=='?' && USB_Out_Buffer[5]=='\n'){
				com_var = 5;
			}
			if(com_var == 0) {
				convtemperature = bin2temp(SPI_lastmessage[meas_1],SPI_lastmessage[meas_2],meas_3);
				for(g=0;g<10;g++){
					USB_In_Buffer[g] == ' ';
				}
				length = ftoa(USB_In_Buffer,convtemperature);
				USB_In_Buffer[length] = '\n';
				putUSBUSART(USB_In_Buffer,length+1);
			} else if(com_var==1) {
				USB_In_Buffer[1] = '\n';
				putUSBUSART(USB_In_Buffer,2);
			} else if(com_var==2) {
				USB_In_Buffer[4] = '\n';
				putUSBUSART(USB_In_Buffer,5);
			} else if(com_var==3){
				USB_In_Buffer[6] = '\n';
				putUSBUSART(USB_In_Buffer,7);
			} else if(com_var==4){
				USB_In_Buffer[3] = '\n';
				putUSBUSART(USB_In_Buffer,4);
			} else if(com_var==5){
				putUSBUSART(USB_IDN_Buffer,55);
			} else if(com_var==6){
				USB_In_Buffer[5] = '\n';
				putUSBUSART(USB_In_Buffer,6);
			} else if(com_var==9){
				USB_In_Buffer[0] = 'E';
				USB_In_Buffer[1] = 'r';
				USB_In_Buffer[2] = 'r';
				USB_In_Buffer[3] = '\n';
				putUSBUSART(USB_In_Buffer,4);
			}
		}
	}
    CDCTxService();
}		//end ProcessIO

// ******************************************************************************************************
// ************** USB Callback Functions ****************************************************************
// ******************************************************************************************************
// The USB firmware stack will call the callback functions USBCBxxx() in response to certain USB related
// events.  For example, if the host PC is powering down, it will stop sending out Start of Frame (SOF)
// packets to your device.  In response to this, all USB devices are supposed to decrease their power
// consumption from the USB Vbus to <2.5mA* each.  The USB module detects this condition (which according
// to the USB specifications is 3+ms of no bus activity/SOF packets) and then calls the USBCBSuspend()
// function.  You should modify these callback functions to take appropriate actions for each of these
// conditions.  For example, in the USBCBSuspend(), you may wish to add code that will decrease power
// consumption from Vbus to <2.5mA (such as by clock switching, turning off LEDs, putting the
// microcontroller to sleep, etc.).  Then, in the USBCBWakeFromSuspend() function, you may then wish to
// add code that undoes the power saving things done in the USBCBSuspend() function.

// The USBCBSendResume() function is special, in that the USB stack will not automatically call this
// function.  This function is meant to be called from the application firmware instead.  See the
// additional comments near the function.

// Note *: The "usb_20.pdf" specs indicate 500uA or 2.5mA, depending upon device classification. However,
// the USB-IF has officially issued an ECN (engineering change notice) changing this to 2.5mA for all 
// devices.  Make sure to re-download the latest specifications to get all of the newest ECNs.

/******************************************************************************
 * Function:        void USBCBSuspend(void)
 *
 * Overview:        Call back that is invoked when a USB suspend is detected
 *
 * Note:            None
 *****************************************************************************/
void USBCBSuspend(void)
{
	//Example power saving code.  Insert appropriate code here for the desired
	//application behavior.  If the microcontroller will be put to sleep, a
	//process similar to that shown below may be used:
	
	//ConfigureIOPinsForLowPower();
	//SaveStateOfAllInterruptEnableBits();
	//DisableAllInterruptEnableBits();
	//EnableOnlyTheInterruptsWhichWillBeUsedToWakeTheMicro();	//should enable at least USBActivityIF as a wake source
	//Sleep();
	//RestoreStateOfAllPreviouslySavedInterruptEnableBits();	//Preferrably, this should be done in the USBCBWakeFromSuspend() function instead.
	//RestoreIOPinsToNormal();									//Preferrably, this should be done in the USBCBWakeFromSuspend() function instead.

	//IMPORTANT NOTE: Do not clear the USBActivityIF (ACTVIF) bit here.  This bit is 
	//cleared inside the usb_device.c file.  Clearing USBActivityIF here will cause 
	//things to not work as intended.	
	

    #if defined(__C30__) || defined __XC16__
        USBSleepOnSuspend();
    #endif
}

/******************************************************************************
 * Function:        void USBCBWakeFromSuspend(void)
 *
 * Overview:        The host may put USB peripheral devices in low power
 *					suspend mode (by "sending" 3+ms of idle).  Once in suspend
 *					mode, the host may wake the device back up by sending non-
 *					idle state signalling.
 *					
 *					This call back is invoked when a wakeup from USB suspend 
 *					is detected.
 *
 * Note:            None
 *****************************************************************************/
void USBCBWakeFromSuspend(void)
{
	// If clock switching or other power savings measures were taken when
	// executing the USBCBSuspend() function, now would be a good time to
	// switch back to normal full power run mode conditions.  The host allows
	// 10+ milliseconds of wakeup time, after which the device must be 
	// fully back to normal, and capable of receiving and processing USB
	// packets.  In order to do this, the USB module must receive proper
	// clocking (IE: 48MHz clock must be available to SIE for full speed USB
	// operation).  
	// Make sure the selected oscillator settings are consistent with USB 
    // operation before returning from this function.
}

/********************************************************************
 * Function:        void USBCB_SOF_Handler(void)
 *
 * Overview:        The USB host sends out a SOF packet to full-speed
 *                  devices every 1 ms. This interrupt may be useful
 *                  for isochronous pipes. End designers should
 *                  implement callback routine as necessary.
 *
 * Note:            None
 *******************************************************************/
void USBCB_SOF_Handler(void)
{

}

/*******************************************************************
 * Function:        void USBCBErrorHandler(void)
 *
 * Overview:        The purpose of this callback is mainly for
 *                  debugging during development. Check UEIR to see
 *                  which error causes the interrupt.
 *
 * Note:            None
 *******************************************************************/
void USBCBErrorHandler(void)
{
    // No need to clear UEIR to 0 here.
    // Callback caller is already doing that.

	// Typically, user firmware does not need to do anything special
	// if a USB error occurs.  For example, if the host sends an OUT
	// packet to your device, but the packet gets corrupted (ex:
	// because of a bad connection, or the user unplugs the
	// USB cable during the transmission) this will typically set
	// one or more USB error interrupt flags.  Nothing specific
	// needs to be done however, since the SIE will automatically
	// send a "NAK" packet to the host.  In response to this, the
	// host will normally retry to send the packet again, and no
	// data loss occurs.  The system will typically recover
	// automatically, without the need for application firmware
	// intervention.
	
	// Nevertheless, this callback function is provided, such as
	// for debugging purposes.
}


/*******************************************************************
 * Function:        void USBCBCheckOtherReq(void)
 *
 * Overview:        When SETUP packets arrive from the host, some
 * 					firmware must process the request and respond
 *					appropriately to fulfill the request.  Some of
 *					the SETUP packets will be for standard
 *					USB "chapter 9" (as in, fulfilling chapter 9 of
 *					the official USB specifications) requests, while
 *					others may be specific to the USB device class
 *					that is being implemented.  For example, a HID
 *					class device needs to be able to respond to
 *					"GET REPORT" type of requests.  This
 *					is not a standard USB chapter 9 request, and 
 *					therefore not handled by usb_device.c.  Instead
 *					this request should be handled by class specific 
 *					firmware, such as that contained in usb_function_hid.c.
 *
 * Note:            None
 *******************************************************************/
void USBCBCheckOtherReq(void)
{
    USBCheckCDCRequest();
}//end


/*******************************************************************
 * Function:        void USBCBStdSetDscHandler(void)
 *
 * Overview:        The USBCBStdSetDscHandler() callback function is
 *					called when a SETUP, bRequest: SET_DESCRIPTOR request
 *					arrives.  Typically SET_DESCRIPTOR requests are
 *					not used in most applications, and it is
 *					optional to support this type of request.
 *
 * Note:            None
 *******************************************************************/
void USBCBStdSetDscHandler(void)
{
    // Must claim session ownership if supporting this request
}//end


/*******************************************************************
 * Function:        void USBCBInitEP(void)
 *
 * Overview:        This function is called when the device becomes
 *                  initialized, which occurs after the host sends a
 * 					SET_CONFIGURATION (wValue not = 0) request.  This 
 *					callback function should initialize the endpoints 
 *					for the device's usage according to the current 
 *					configuration.
 *
 * Note:            None
 *******************************************************************/
void USBCBInitEP(void)
{
    //Enable the CDC data endpoints
    CDCInitEP();
}

/********************************************************************
 * Function:        void USBCBSendResume(void)
 *
 * Overview:        The USB specifications allow some types of USB
 * 					peripheral devices to wake up a host PC (such
 *					as if it is in a low power suspend to RAM state).
 *					This can be a very useful feature in some
 *					USB applications, such as an Infrared remote
 *					control	receiver.  If a user presses the "power"
 *					button on a remote control, it is nice that the
 *					IR receiver can detect this signalling, and then
 *					send a USB "command" to the PC to wake up.
 *					
 *					The USBCBSendResume() "callback" function is used
 *					to send this special USB signalling which wakes 
 *					up the PC.  This function may be called by
 *					application firmware to wake up the PC.  This
 *					function will only be able to wake up the host if
 *                  all of the below are true:
 *					
 *					1.  The USB driver used on the host PC supports
 *						the remote wakeup capability.
 *					2.  The USB configuration descriptor indicates
 *						the device is remote wakeup capable in the
 *						bmAttributes field.
 *					3.  The USB host PC is currently sleeping,
 *						and has previously sent your device a SET 
 *						FEATURE setup packet which "armed" the
 *						remote wakeup capability.   
 *
 *                  If the host has not armed the device to perform remote wakeup,
 *                  then this function will return without actually performing a
 *                  remote wakeup sequence.  This is the required behavior, 
 *                  as a USB device that has not been armed to perform remote 
 *                  wakeup must not drive remote wakeup signalling onto the bus;
 *                  doing so will cause USB compliance testing failure.
 *                  
 *					This callback should send a RESUME signal that
 *                  has the period of 1-15ms.
 *
 * Note:            This function does nothing and returns quickly, if the USB
 *                  bus and host are not in a suspended condition, or are 
 *                  otherwise not in a remote wakeup ready state.  Therefore, it
 *                  is safe to optionally call this function regularly, ex: 
 *                  anytime application stimulus occurs, as the function will
 *                  have no effect, until the bus really is in a state ready
 *                  to accept remote wakeup. 
 *
 *                  When this function executes, it may perform clock switching,
 *                  depending upon the application specific code in 
 *                  USBCBWakeFromSuspend().  This is needed, since the USB
 *                  bus will no longer be suspended by the time this function
 *                  returns.  Therefore, the USB module will need to be ready
 *                  to receive traffic from the host.
 *
 *                  The modifiable section in this routine may be changed
 *                  to meet the application needs. Current implementation
 *                  temporary blocks other functions from executing for a
 *                  period of ~3-15 ms depending on the core frequency.
 *
 *                  According to USB 2.0 specification section 7.1.7.7,
 *                  "The remote wakeup device must hold the resume signaling
 *                  for at least 1 ms but for no more than 15 ms."
 *                  The idea here is to use a delay counter loop, using a
 *                  common value that would work over a wide range of core
 *                  frequencies.
 *                  That value selected is 1800. See table below:
 *                  ==========================================================
 *                  Core Freq(MHz)      MIP         RESUME Signal Period (ms)
 *                  ==========================================================
 *                      48              12          1.05
 *                       4              1           12.6
 *                  ==========================================================
 *                  * These timing could be incorrect when using code
 *                    optimization or extended instruction mode,
 *                    or when having other interrupts enabled.
 *                    Make sure to verify using the MPLAB SIM's Stopwatch
 *                    and verify the actual signal on an oscilloscope.
 *******************************************************************/
void USBCBSendResume(void)
{
    static WORD delay_count;
    
    //First verify that the host has armed us to perform remote wakeup.
    //It does this by sending a SET_FEATURE request to enable remote wakeup,
    //usually just before the host goes to standby mode (note: it will only
    //send this SET_FEATURE request if the configuration descriptor declares
    //the device as remote wakeup capable, AND, if the feature is enabled
    //on the host (ex: on Windows based hosts, in the device manager 
    //properties page for the USB device, power management tab, the 
    //"Allow this device to bring the computer out of standby." checkbox 
    //should be checked).
    if(USBGetRemoteWakeupStatus() == TRUE) 
    {
        //Verify that the USB bus is in fact suspended, before we send
        //remote wakeup signalling.
        if(USBIsBusSuspended() == TRUE)
        {
            USBMaskInterrupts();
            
            //Clock switch to settings consistent with normal USB operation.
            USBCBWakeFromSuspend();
            USBSuspendControl = 0; 
            USBBusIsSuspended = FALSE;  //So we don't execute this code again, 
                                        //until a new suspend condition is detected.

            //Section 7.1.7.7 of the USB 2.0 specifications indicates a USB
            //device must continuously see 5ms+ of idle on the bus, before it sends
            //remote wakeup signalling.  One way to be certain that this parameter
            //gets met, is to add a 2ms+ blocking delay here (2ms plus at 
            //least 3ms from bus idle to USBIsBusSuspended() == TRUE, yeilds
            //5ms+ total delay since start of idle).
            delay_count = 3600U;        
            do
            {
                delay_count--;
            }while(delay_count);
            
            //Now drive the resume K-state signalling onto the USB bus.
            USBResumeControl = 1;       // Start RESUME signaling
            delay_count = 1800U;        // Set RESUME line for 1-13 ms
            do
            {
                delay_count--;
            }while(delay_count);
            USBResumeControl = 0;       //Finished driving resume signalling

            USBUnmaskInterrupts();
        }
    }
}


/*******************************************************************
 * Function:        void USBCBEP0DataReceived(void)
 *
 * PreCondition:    ENABLE_EP0_DATA_RECEIVED_CALLBACK must be
 *                  defined already (in usb_config.h)
 *
 * Overview:        This function is called whenever a EP0 data
 *                  packet is received.  This gives the user (and
 *                  thus the various class examples a way to get
 *                  data that is received via the control endpoint.
 *                  This function needs to be used in conjunction
 *                  with the USBCBCheckOtherReq() function since 
 *                  the USBCBCheckOtherReq() function is the apps
 *                  method for getting the initial control transfer
 *                  before the data arrives.
 *
 * Note:            None
 *******************************************************************/
#if defined(ENABLE_EP0_DATA_RECEIVED_CALLBACK)
void USBCBEP0DataReceived(void)
{
}
#endif

/*******************************************************************
 * Function:        BOOL USER_USB_CALLBACK_EVENT_HANDLER(
 *                        int event, void *pdata, WORD size)
 *
 * PreCondition:    None
 *
 * Input:           int event - the type of event
 *                  void *pdata - pointer to the event data
 *                  WORD size - size of the event data
 *
 * Output:          None
 *
 * Side Effects:    None
 *
 * Overview:        This function is called from the USB stack to
 *                  notify a user application that a USB event
 *                  occured.  This callback is in interrupt context
 *                  when the USB_INTERRUPT option is selected.
 *
 * Note:            None
 *******************************************************************/
BOOL USER_USB_CALLBACK_EVENT_HANDLER(int event, void *pdata, WORD size)
{
    switch( event )
    {
        case EVENT_TRANSFER:
            //Add application specific callback task or callback function here if desired.
            break;
        case EVENT_SOF:
            USBCB_SOF_Handler();
            break;
        case EVENT_SUSPEND:
            USBCBSuspend();
            break;
        case EVENT_RESUME:
            USBCBWakeFromSuspend();
            break;
        case EVENT_CONFIGURED: 
            USBCBInitEP();
            break;
        case EVENT_SET_DESCRIPTOR:
            USBCBStdSetDscHandler();
            break;
        case EVENT_EP0_REQUEST:
            USBCBCheckOtherReq();
            break;
        case EVENT_BUS_ERROR:
            USBCBErrorHandler();
            break;
        case EVENT_TRANSFER_TERMINATED:
            //Add application specific callback task or callback function here if desired.
            //The EVENT_TRANSFER_TERMINATED event occurs when the host performs a CLEAR
            //FEATURE (endpoint halt) request on an application endpoint which was 
            //previously armed (UOWN was = 1).  Here would be a good place to:
            //1.  Determine which endpoint the transaction that just got terminated was 
            //      on, by checking the handle value in the *pdata.
            //2.  Re-arm the endpoint if desired (typically would be the case for OUT 
            //      endpoints).
            break;
        default:
            break;
    }      
    return TRUE; 
}

 
/** EOF main.c *************************************************/

