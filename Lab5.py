import RPi.GPIO as  GPIO
import time

# These are the pins we will be using.
# ENA-6, ENB-26, IN1-12, IN2-13, IN3-20, IN4-21
# CS-5, DataOut-23, Address-24, Clock-25
ENA = 6
ENB = 26
IN1 = 12
IN2 = 13
IN3 = 20
IN4 = 21
CS = 5
DataOut = 23
Address = 24
Clock = 25


numSensors = 5

#Functions to carry out movement of the robot
# 0 = GPIO.LOW  1 = GPIO.HIGH
def moveForward():
    print("Moving Forward...")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

def stop():
    print("Stopping...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.LOW)

def moveBackward():
    print("Moving Backward...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def pivotRight():
    print("Right Pivot...")
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN2,GPIO.LOW)
    GPIO.output(IN3,GPIO.HIGH)
    GPIO.output(IN4,GPIO.LOW)

def pivotLeft():
    print("Left Pivot...")
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN2,GPIO.HIGH)
    GPIO.output(IN3,GPIO.LOW)
    GPIO.output(IN4,GPIO.HIGH)

def initRake():
    calibratedMin = [0] * numSensors
    calibratedMax = [1023] * numSensors
    last_value = 0

def readAnalog():
	value = [0,0,0,0,0,0] #array to hold values of the rake sensor
	for j in range(0,6):
		GPIO.output(CS, GPIO.LOW)
		for i in range(0,4):
			#sent 4-bit Address
			if(((j) >> (3 - i)) & 0x01):
				GPIO.output(Address,GPIO.HIGH)
			else:
				GPIO.output(Address,GPIO.LOW)
			#read MSB 4-bit data
			value[j] <<= 1
			if(GPIO.input(DataOut)):
				value[j] |= 0x01
			GPIO.output(Clock,GPIO.HIGH)
			GPIO.output(Clock,GPIO.LOW)
		for i in range(0,6):
			#read LSB 8-bit data
			value[j] <<= 1
			if(GPIO.input(DataOut)):
				value[j] |= 0x01
			GPIO.output(Clock,GPIO.HIGH)
			GPIO.output(Clock,GPIO.LOW)
		#no mean ,just delay
		for i in range(0,6):
			GPIO.output(Clock,GPIO.HIGH)
			GPIO.output(Clock,GPIO.LOW)
#		time.sleep(0.0001)
		GPIO.output(CS,GPIO.HIGH)
	return value[1:]

def readLine(white_line = 0):
    #sensor_values = readCalibrated()
    tmpSensors = numSensors
    avg = 0
    sum = 0
    on_line = 0
##    for i in range(0,tmpSensors):
##        value = sensor_values[i]
##        if(white_line):
##            lue = 1000-value
##        # keep track of whether we see the line at all
##        if(value > 200):
##            n_line = 1
##
##        # only average in values that are above a noise threshold
##        if(value > 50):
##            avg += value * (i * 1000);  # this is for the weighted total,
##            sum += value;                  #this is for the denominator

    if(on_line != 1):
        # If it last read to the left of center, return 0.
        if(last_value < (tmpSensors - 1)*1000/2):
            #print("left")
            return 0;

        # If it last read to the right of center, return the max.
        else:
            #print("right")
            return (tmpSensors - 1)*1000

    last_value = avg/sum
    return last_value

# Sets the desired pin numbering system to BCM
GPIO.setmode(GPIO.BCM)

# Disables warnings in case the RPI.GPIO detects that a pin has been configured
# to something other than the default (input)
GPIO.setwarnings(False)

# Sets all the pins stated above as outputs
chan_list = [ENA,ENB,IN1,IN2,IN3,IN4,Address,CS,Clock]
GPIO.setup(chan_list,GPIO.OUT)
GPIO.setup(DataOut,GPIO.IN,GPIO.PUD_UP)

# creates objects "p1" and "p2", sets ena and enb to 50 Hz, starts them at 20% duty cycle
p1 = GPIO.PWM(ENA,50)
p1.start(20)

p2 = GPIO.PWM(ENB,50)
p2.start(20)

# Stops both the PWM outputs
p1.stop()
p2.stop()





# Cleans up the used resources
GPIO.cleanup()
