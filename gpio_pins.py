'''
Created on Oct 5, 2017

@author: root
'''

#https://learn.adafruit.com/adafruit-16-channel-servo-driver-with-raspberry-pi/using-the-adafruit-library
#https://github.com/adafruit/Adafruit_Python_PCA9685

##################################
#SERVO MOTOR SETTINGS  
# GPIO 2   SDA1 I2C
# GPIO 3   SCL1, I2C
##################################
#RELAY SETTINGS
# GPIO 4
# 
# GPIO 17
# GPIO 27
# GPIO 22
# GPIO 10
# GPIO 9
# GPIO 11
# GPIO 5
##################################

loaded = False
try:
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 3:
        pin_map = [0,0,0,2,0,3,0,4,14,0,15,17,18,27,0,22,23,0,24,10,0,9,25,11,8,0,7,0,0,5,0,6,12,13,0,19,16,26,20,0,21]
        loaded = True
except ImportError:
    pin_map = [i for i in range(27)] # assume 26 pins all mapped.  Maybe we should not assume anything, but...
    platform = ''  # if no platform, allows program to still run.
    print ('No GPIO module was loaded from GPIO Pins module')
        
try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
except NameError:
    pass

pin_relay1 = 4 #pin_map[2]
pin_relay2 = 17 
pin_relay3 = 27
pin_relay4 = 22
pin_relay5 = 10
pin_relay6 = 9
pin_relay7 = 11
pin_relay8 = 5

# init list with pin numbers  
  
pinList = [2, 3, 4, 17, 27, 22, 10, 9,]  

pinDict = {
    'relay1' : pinList[0],
    'relay2' : pinList[1],
    'relay3' : pinList[2],
    'relay4' : pinList[3],
    'relay5' : pinList[4],
    'relay6' : pinList[5],
    'relay7' : pinList[6],
    'relay8' : pinList[7],                            
    }

# loop through pins and set mode and state to 'low'  

def turn_reley_off(reley_pin):
    try:
        GPIO.setup(reley_pin, GPIO.OUT)
        GPIO.output(reley_pin, GPIO.LOW)
    except NameError:
        pass

def turn_reley_on(reley_pin):
    try:
        GPIO.setup(reley_pin, GPIO.OUT)
        GPIO.output(reley_pin, GPIO.HIGH)
    except NameError:
        pass
    
def turn_reley_on_by_name(relay):
    try:
        GPIO.setup(pinDict[relay], GPIO.OUT)
        GPIO.output(pinDict[relay], GPIO.HIGH)
    except NameError:
        pass
    
def turn_reley_off_by_name(relay):
    try:
        GPIO.setup(pinDict[relay], GPIO.OUT)
        GPIO.output(pinDict[relay], GPIO.LOW)
    except NameError:
        pass

def turn_gpio_off():
    try:
        GPIO.cleanup()
    except NameError:
        pass    