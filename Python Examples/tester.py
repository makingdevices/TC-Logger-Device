### Thermo Couple Logger Device
## MakingDevices - 2022/23
# TESTER APP - EXAMPLE OF CODE

#Import libraries:
import pyvisa, time

#We will use the resource manager from PYVISA
rm = pyvisa.ResourceManager()
print(rm)
devlist = rm.list_resources()
print(devlist)  # device list feedback is ('ASRL7::INSTR', 'ASRL8::INSTR', 'ASRL9::INSTR')
#We open the TC LOGGER in "COM9", feel free to change into the COM of your computer
TC_LOGGER = rm.open_resource('COM9') ## YOU MUST EDIT THE COM PORT
TC_LOGGER.timeout = 1 #1 sec of timeout
TC_LOGGER.write_termination = '\n' #termination of the communication
TC_LOGGER.read_termination = '\n' #termination of the communication


print(TC_LOGGER.query('*IDN?'))  #Device Info command

print("TC1 temperatures:")
print(TC_LOGGER.query(':MEAS:TC1:INT?'))
print(TC_LOGGER.query(':MEAS:TC1:EXT?'))

#You can mix different commands following the SCPI standard:
#print(TC_LOGGER.query(':MEAS:TC1:INT?;:MEAS:TC1:INT?'))
#print(TC_LOGGER.query(':MEAS:TC1:EXT?;EXT?'))
#print(TC_LOGGER.query(':MEAS:TC1:EXT?;:MEAS:TC1:INT?'))

print("Set ON LED TC1:")
print(TC_LOGGER.query(':SET:TC1:LED 1'))
time.sleep(1)
print("State of the LED 1:")
print(TC_LOGGER.query(':MEAS:TC1:LED?'))
print("Set OFF LED TC1:")
print(TC_LOGGER.query(':SET:TC1:LED 0'))
time.sleep(1)
print("State of the LED 1:")
print(TC_LOGGER.query(':MEAS:TC1:LED?'))
print("Mode of the LED:")
print(TC_LOGGER.query(':MODE:LED:TC1?'))
print("LED TC1 to auto:")
print(TC_LOGGER.query(':SET:TC1:LED AUTO'))
print("State of the LED 1:")
print(TC_LOGGER.query(':MODE:LED:TC1?'))

print("TC2 temperatures:")
print(TC_LOGGER.query(':MEAS:TC2:INT?'))
print(TC_LOGGER.query(':MEAS:TC2:EXT?'))
print("Set ON LED TC2:")
print(TC_LOGGER.query(':SET:TC2:LED 1'))
time.sleep(1)
print("State of the LED 2:")
print(TC_LOGGER.query(':MEAS:TC2:LED?'))
print("Set OFF LED TC2:")
print(TC_LOGGER.query(':SET:TC2:LED 0'))
time.sleep(1)
print("State of the LED 2:")
print(TC_LOGGER.query(':MEAS:TC2:LED?'))
print("Mode of the LED:")
print(TC_LOGGER.query(':MODE:LED:TC2?'))
print("LED TC2 to auto:")
print(TC_LOGGER.query(':SET:TC2:LED AUTO'))
print("State of the LED 2:")
print(TC_LOGGER.query(':MODE:LED:TC2?'))

print("App info:")
print(TC_LOGGER.query(':CONFIG:HW?'))
print(TC_LOGGER.query(':CONFIG:APP?'))

print("Random message:")
print(TC_LOGGER.query(':hello?'))
print(TC_LOGGER.query(':hey'))


## All the commands can be mixed following the SCPI Standards
## SCPI Commands

# - :MEAS  
#   - :TC1
#     - :INT?
#     - :EXT?
#     - :LED?
#   - :TC2 
#     - :INT?
#     - :EXT?
#     - :LED?

# - :SET  
#   - :TC1
#     - :LED [AUTO|0|1] 
#   - :TC2
#     - :LED [AUTO|0|1] 

# - :MODE   
#   - :LED
#     - :TC1?
#     - :TC2?

# - :CONF  
#     - :APP?
#     - :HW?

# - *IDN?  //DO NOT ACCEPT MIXING WITH OTHER COMMANDS

# - :hello? 

