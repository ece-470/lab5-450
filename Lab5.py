import RPi.GPIO as  GPIO
import time

numSensors = 5

#Functions to carry out movement of the robot
# 0 = GPIO.LOW  1 = GPIO.HIGH
def moveForward():
    print("Moving Forward...")
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(20,GPIO.LOW)
    GPIO.output(21,GPIO.HIGH)

def stop():
    print("Stopping...")
    GPIO.output(12,GPIO.LOW)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(20,GPIO.LOW)
    GPIO.output(21,GPIO.LOW)

def moveBackward():
    print("Moving Backward...")
    GPIO.output(12,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(20,GPIO.HIGH)
    GPIO.output(21,GPIO.LOW)

def pivotRight():
    print("Right Pivot...")
    GPIO.output(12,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(20,GPIO.HIGH)
    GPIO.output(21,GPIO.LOW)

def pivotLeft():
    print("Left Pivot...")
    GPIO.output(12,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(20,GPIO.LOW)
    GPIO.output(21,GPIO.HIGH)

def initRake():
    calibratedMin = [0] * numSensors
    calibratedMax = [1023] * numSensors
    last_value = 0

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

# These are the pins we will be using.
# 6 and 26 are ena and enb
# 12, 13, 20, 21 are IN1 IN2 IN3 IN4
# CS-5, DataOut-23, Address-24, Clock-25
chan_list = [5,6,12,13,20,21,24,25,26]

# Sets all the pins stated above as outputs
GPIO.setup(chan_list,GPIO.OUT)
GPIO.setup(23,GPIO.IN,GPIO.PUD_UP)

# creates objects "p1" and "p2", sets ena and enb to 50 Hz, starts them at 20% duty cycle
p1 = GPIO.PWM(6,50)
p1.start(20)

p2 = GPIO.PWM(26,50)
p2.start(20)

# Stops both the PWM outputs
p1.stop()
p2.stop()

print("Number of sensors: " + str(numSensors))

# Cleans up the used resources
GPIO.cleanup()