
# Import statements
import sys
import time
import atexit
sys.path.append("L:/test") ### ADD PATH
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

class Car():
    """Initialize car and control functions"""

    def __init__(self) -> None:
        """Initialize method"""
        mh = Adafruit_MotorHAT(addr=0x60)
        driveMotor = mh.getMotor(1)
        steerMotor = mh.getMotor(2)
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
                driveMotor.run(Adafruit_MotorHAT.FORWARD)
                driveMotor.setSpeed(speed)
        if direction == -1:
                driveMotor.run(Adafruit_MotorHAT.BACKWARD)
                driveMotor.setSpeed(speed)
        if direction == 0:
                driveMotor.setSpeed(0)
                driveMotor.run(Adafruit_MotorHAT.RELEASE)

    def steer(direction):
        """Method to control steering
        direction <integer> {-1,0,1}"""
        if direction == 1:
                steerMotor.run(Adafruit_MotorHAT.FORWARD)
                steerMotor.setSpeed(255)
        if direction == -1:
                steerMotor.run(Adafruit_MotorHAT.BACKWARD)
                steerMotor.setSpeed(255)
        if direction == 0:
                steerMotor.setSpeed(0)
                steerMotor.run(Adafruit_MotorHAT.RELEASE)
