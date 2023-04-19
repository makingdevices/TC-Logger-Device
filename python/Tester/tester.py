### Thermo Couple Logger Device
## MakingDevices - 2022/23
#
import pyvisa, time

rm = pyvisa.ResourceManager()
print(rm)
devlist = rm.list_resources()
print(devlist)  # device list feedback is ('ASRL7::INSTR', 'ASRL8::INSTR', 'ASRL9::INSTR')
TC_LOGGER = rm.open_resource('COM9')
TC_LOGGER.timeout = 1
TC_LOGGER.write_termination = '\n'
TC_LOGGER.read_termination = '\n'
# You may need to configure further the resource by setting explicitly the
# baud rate, parity, termination character, etc before being able to communicate
# Those depend on your instrument.

#TC_LOGGER.write("*IDN?")
#print(TC_LOGGER.read()

print(TC_LOGGER.query('*IDN?'))

print("TC1 temperatures:")
print(TC_LOGGER.query(':MEAS:TC1:INT?;:MEAS:TC1:INT?'))
print(TC_LOGGER.query(':MEAS:TC1:EXT?;EXT?'))

print("Set ON LED TC1:")
print(TC_LOGGER.query(':SET:TC1:LED 1'))
time.sleep(1)
print(TC_LOGGER.query(':MEAS:TC1:LED?'))
print("Set OFF LED TC1:")
print(TC_LOGGER.query(':SET:TC1:LED 0'))
time.sleep(1)
print(TC_LOGGER.query(':MEAS:TC1:LED?'))
print("Mode of the LED:")
print(TC_LOGGER.query(':MODE:LED:TC1?'))
print("LED TC1 to auto:")
print(TC_LOGGER.query(':SET:TC1:LED AUTO'))
print(TC_LOGGER.query(':MODE:LED:TC1?'))

print("TC2 temperatures:")
print(TC_LOGGER.query(':MEAS:TC2:INT?;:MEAS:TC2:INT?'))
print(TC_LOGGER.query(':MEAS:TC2:EXT?;EXT?'))
print("Set ON LED TC2:")
print(TC_LOGGER.query(':SET:TC2:LED 1'))
time.sleep(1)
print(TC_LOGGER.query(':MEAS:TC2:LED?'))
print("Set OFF LED TC2:")
print(TC_LOGGER.query(':SET:TC2:LED 0'))
time.sleep(1)
print(TC_LOGGER.query(':MEAS:TC2:LED?'))
print("Mode of the LED:")
print(TC_LOGGER.query(':MODE:LED:TC2?'))
print("LED TC2 to auto:")
print(TC_LOGGER.query(':SET:TC2:LED AUTO'))
print(TC_LOGGER.query(':MODE:LED:TC2?'))

print("App info:")
print(TC_LOGGER.query(':CONFIG:HW?'))
print(TC_LOGGER.query(':CONFIG:APP?'))

print("Random message:")
print(TC_LOGGER.query(':hello?'))
print(TC_LOGGER.query(':hey'))

print(" ")
print("***")
print("******")
print("TEST ENDED OK")
print("******")
print("***")

