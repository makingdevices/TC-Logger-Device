/*	Making Devices 2021
	https://makingdevices.com
	Rubén García Segovia
	Thermo Device Logger
*/


#include <p18f14k50.h>
#include <delays.h>

 // setup config bits 
 #pragma config PCLKEN=OFF
 #pragma config FOSC = IRC
 #pragma config BOREN = OFF 
 #pragma config WDTEN = OFF 
 #pragma config LVP = OFF  

void InitOSC(void); 
void _low_isr (void);
void _high_isr (void);
void Interrupts_enable (void);

#pragma code low_vector=0x18 //Low interrupt priority starts at 0x18
void low_interrupt(void)
{
_asm goto _low_isr _endasm
}

#pragma code high_vector=0x08 //High interrupt priority starts at 0x08
void high_interrupt(void)
{
_asm goto _high_isr _endasm
}
#pragma code


#pragma interrupt _low_isr

void _low_isr (void){

}

char state = 0;
#pragma interrupt _high_isr
void _high_isr (void)   //High priority interrupt.
{
if(INTCONbits.TMR0IF) //Timer0 interrupt
	{

	//We set the timer0 again
	TMR0H = 0xAA;
	TMR0L = 0xFF;

		if (state == 0){
			LATC = 0b00001000;
			state++;
		} else {
			LATC = 0b00000100;
			state = 0;
		}
	INTCONbits.TMR0IF = 0; // reset overflow bit (for timer0).
	}
}

/* ****************** MAIN ****************** */
char init = 0;
void main(void)
{
	if(init == 0){
		InitOSC();     //Internal OSC 16MHz 
    	Interrupts_enable(); //Enable RA0 & RA1 interrupts
		TRISB =0; //Set port B as output
		TRISC =0; //Set port C as output
		
		init = 1; //We only run this loop once.
		OSCCONbits.IDLEN = 1; //We activate idle mode.
	}
	Sleep(); //Sleep either idle or deep mode!  
}

 void InitOSC(void) 
 {    
      OSCCON  = 0b10010110;   //Internal 250KHz    
 } 

 void Interrupts_enable(void) 
 {    
	TRISA = 0b11001111; //A port as input
	PORTA = 0;
    INTCON2bits.RABPU = 0; // Enable Pull-UP on port A-B
    INTCON2bits.RABIP = 1; // Change on port = High priority
	IOCA  = 0b00000011;        //Enable Interrupt on Change for Pin 4 of Port A 
    INTCONbits.RABIE = 1;      //Enable RA and RB Port Change Interrupt 

T0CONbits.T08BIT = 0;	//5ms at 250Khz timer 0 interrupt
T0CONbits.T0CS = 0;
T0CONbits.PSA = 1;
TMR0H = 0xFE;
TMR0L = 0xC7;
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
 
 


