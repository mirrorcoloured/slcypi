
# Import statements
import sys
import time
import atexit
sys.path.append("/home/pi/Adafruit-Motor-HAT-Python-Library") ### ADD PATH
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

class Tank():
    """Initialize car and control functions"""

    def __init__(self) -> None:
        """Initialize method"""
        mh = Adafruit_MotorHAT(addr=0x60)
        leftMotor = mh.getMotor(1)
        rightMotor = mh.getMotor(2)
        atexit.register(turnOffMotors)
    
    def turnOffMotors(self) -> None:
        """Method to turn off all motors"""
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def stop(self) -> None:
        """Method to stop driving"""
        turnOffMotors()
        
    def drive(self,direction, speed=100) -> None:
        """Method control forward speed
        direction <integer> {-1,0,1}
        speed <integer> {0:255}"""
        if direction == 1:
                leftMotor.run(Adafruit_MotorHAT.FORWARD)
                rightMotor.run(Adafruit_MotorHAT.FORWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == -1:
                leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == 0:
                leftMotor.setSpeed(0)
                rightMotor.setSpeed(0)
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)

    def rotate(self,direction, speed=30):
        """Method to control steering
        direction <integer> {-1,0,1}
        speed <integer>"""
        if direction == 1:
                leftMotor.run(Adafruit_MotorHAT.FORWARD)
                rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == -1:
                leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                rightMotor.run(Adafruit_MotorHAT.FORWARD)
                leftMotor.setSpeed(speed)
                rightMotor.setSpeed(speed)
        if direction == 0:
                leftMotor.setSpeed(0)
                rightMotor.setSpeed(0)
                leftMotor.run(Adafruit_MotorHAT.RELEASE)
                rightMotor.run(Adafruit_MotorHAT.RELEASE)



