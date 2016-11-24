 
# Import statements
import sys
import time
import atexit
sys.path.append("/home/pi/Adafruit-Motor-HAT-Python-Library") ### ADD PATH
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

mh = Adafruit_MotorHAT(addr=0x60)

def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
 
atexit.register(turnOffMotors)

myMotor = mh.getMotor(1)

# set the speed to start, from 0 (off) to 255 (max speed)
myMotor.run(Adafruit_MotorHAT.FORWARD)
myMotor.setSpeed(50)
time.sleep(0.5)
myMotor.setSpeed(50)
myMotor.run(Adafruit_MotorHAT.RELEASE)
