# tst.py
# Andrew Ribeiro
# April 16, 2016
#
# Notes
# > I was going to have the system be able to read in presses from
#   the service selectors, but if the touch screen is being bypassed,
#   it is assumed that there is a critical error with the PI.
# > The spoofing of a signal should be outputted for 40 MS.
# > The code that deals with input is mainly for diagonstics. 

import RPi.GPIO as GPIO
import time



### Global Variables ##### 
ioMapping = {}

ioMapping["0011"] = 1 # 3
ioMapping["1011"] = 2 # 11
ioMapping["0111"] = 3 # 7
ioMapping["1111"] = 4 # 15
ioMapping["1100"] = 5 # 12 Guessed
ioMapping["1001"] = 6 # 9
ioMapping["0101"] = 7 # 5
ioMapping["1101"] = 8 # 13
ioMapping["0010"] = 9 # 2
ioMapping["1010"] = 10# 10
ioMapping["0110"] = 11# 6
ioMapping["1110"] = 12# 14
ioMapping["0000"] = 13# 0
ioMapping["1000"] = 14# 8
ioMapping["0100"] = 15# 4
ioMapping["0001"] = 16# 1 Guessed

oiMapping = {}

oiMapping[1]  = "0011"
oiMapping[2]  = "1011"
oiMapping[3]  = "0111"
oiMapping[4]  = "1111"
oiMapping[5]  = "1100"
oiMapping[6]  = "1001"
oiMapping[7]  = "0101"
oiMapping[8]  = "1101"
oiMapping[9]  = "0010"
oiMapping[10] = "1010"
oiMapping[11] = "0110"
oiMapping[12] = "1110"
oiMapping[13] = "0000"
oiMapping[14] = "1000"
oiMapping[15] = "0100"
oiMapping[16] = "0001"

# Data out 1,2,3,4 and IO ready flag 5. 
# firstGPIO: the GPIO pins handling the first service selector. 
firstGPIO  = [14,15,18,23,24]
# secondGPIO: the GPIO pins handling the second service selector. 
secondGPIO = [25,8,7,12,16]

# When we get a high reading on all inputs for a service selector
# we interpret that as the idleState. 
idleState = "11111"

##########################

#### UTIL FUNCTIONS #########
def prepForInput():
    #First service selector.
    for ioPin in firstGPIO:
        GPIO.setup( ioPin, GPIO.IN )
        
    #Second service selector. 
    for ioPin in secondGPIO:
        GPIO.setup( ioPin, GPIO.IN ) 

def prepForOutput():
    #First service selector.
    for ioPin in firstGPIO:
        GPIO.setup( ioPin, GPIO.OUT )
        
    #Second service selector. 
    for ioPin in secondGPIO:
        GPIO.setup( ioPin, GPIO.OUT )
    

def printPins():
    tmpSignal = ""

     #First service selector.
    for ioPin in firstGPIO:
        tmpSignal += str( GPIO.input( ioPin ) )

    if( tmpSignal != idleState):
        print( "First Selector: "+tmpSignal )
    else:
        #Second service selector. 
        for ioPin in secondGPIO:
            tmpSignal += str( GPIO.input( ioPin ) )
            
        if( tmpSignal != idleState):
            print( "Second Selector: "+tmpSignal )

    
def printIONums():
    global ioMapping

    for key,value in ioMapping.iteritems():
        base10 = 0
        baseValue = 3
        print( key + ": "),
        for char in key:
            base10 += pow(2,baseValue)*int(char)
            baseValue -= 1
        print(base10)


def pinListenPrinter():
    prepForInput()
    while True:
        printPins()
        # 5 MS
        time.sleep(5/1000)

##########################

# Sets up pins for output and sets the state of the pins
# to the idle state of all high signals.
# Call this once when the program/system is launched. 
def init():
    # Set to the default ordering of pins. 
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    prepForOutput()

    # Set all pins to the idle state. 
    for pin in firstGPIO:
        GPIO.output( pin , 1 )
    for pin in secondGPIO:
        GPIO.output( pin, 1 )

# Sends to corresponding signal for a button being pressed on either
# service selector. Signal spoofer.
# Prereq: must call init() before this function is called for the first time.
def buttonPressed( serviceSelector, button ):
    outCode = oiMapping[ button ]
    pins = None
    
    if serviceSelector == 1:
        pins = firstGPIO
        
    elif serviceSelector == 2:
        pins = secondGPIO

    if pins != None:
        pinIndex = 0

        # Activate signals. 
        for signal in outCode:
            sendNow = int(signal)
            GPIO.output( pins[pinIndex] , sendNow )
            pinIndex+=1
        #Turn on I/O flag. ( 0 is on, it's flipped for some reason. )
        GPIO.output( pins[pinIndex + 1 ], GPIO.LOW )
        
        # Send signals for 40 MS
        time.sleep(40/1000)

        #Turn off. Return pins to idle state. 
        pinIndex = 0
        for signal in idleState:
            GPIO.output( pins[ pinIndex ], int( signal ) )
            pinIndex+=1

# Call this function when a service is changed.        
def uploadServiceChange(serviceID, name, cost):
    pass
    

    
        
