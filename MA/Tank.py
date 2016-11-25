
# Import statements
import sys
import time
import atexit
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

class Tank():
    """Initialize car and control functions"""

    def __init__(self) -> None:
        """Initialize method"""
        mh = Adafruit_MotorHAT(addr=0x60)
        self.leftMotor = mh.getMotor(1)
        self.rightMotor = mh.getMotor(2)
        #atexit.register(turnOffMotors)
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

        # Variables related to sync drive
        self.driveSpeed = 0
        self.rotateSpeed = 0
        self.leftSpeed = 0 
        self.rightSpeed = 0
        self.actualLeftSpeed = 0
        self.actualRightSpeed = 0

        # Variable for sets swaps
        self.leftRightSwap = False
        self.leftReverse = False
        self.rightReverse = False

    def correctDirections(self,leftRightSwap,leftReverse,rightReverse):
        """Method to correct for swapped motor or motors running backwards
        leftRightSwap <boolean>
        leftReverse <boolean>
        rightReverse <boolean>"""
        self.leftRightSwap = leftRightSwap
        self.leftReverse = leftReverse
        self.rightReverse = rightRevese
        
    def turnOffMotors(self):
        """Method to turn off all motors"""
        mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

    def stop(self) -> None:
        """Method to stop driving"""
        self.turnOffMotors()
        
    def drive(self,direction, speed=100) -> None:
        """Method control forward speed
        direction <integer> {-1,0,1}
        speed <integer> {0:255}"""
        if direction == 1:
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                self.leftMotor.setSpeed(speed)
                self.rightMotor.setSpeed(speed)
        if direction == -1:
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.leftMotor.setSpeed(speed)
                self.rightMotor.setSpeed(speed)
        if direction == 0:
                self.leftMotor.setSpeed(0)
                self.rightMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.RELEASE)
                self.rightMotor.run(Adafruit_MotorHAT.RELEASE)

    def rotate(self,direction, speed=50):
        """Method to control steering
        direction <integer> {-1,0,1}
        speed <integer>"""
        if direction == 1:
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.leftMotor.setSpeed(speed)
                self.rightMotor.setSpeed(speed)
        if direction == -1:
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                self.leftMotor.setSpeed(speed)
                self.rightMotor.setSpeed(speed)
        if direction == 0:
                self.leftMotor.setSpeed(0)
                self.rightMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.RELEASE)
                self.rightMotor.run(Adafruit_MotorHAT.RELEASE)

    def driveSync(self,direction, speed=100) -> None:
        """Method control forward speed
        direction <integer> {-1,0,1}
        speed <integer> {0:255}"""
        if direction == 1:
                self.driveSpeed = speed               
        if direction == -1:
                self.driveSpeed = -speed
        if direction == 0:
                self.diveSpeed = 0

    def rotateSync(self,direction, speed=50):
        """Method to control steering
        direction <integer> {-1,0,1}
        speed <integer>"""
        if direction == 1:
                self.rotateSpeed = speed
        if direction == -1:
                self.rotateSpeed = -speed
        if direction == 0:
                self.rotateSpeed = 0

    def setSpeeds(self):
        self.leftSpeed = self.driveSpeed + self.rotateSpeed
        self.rightSpeed = self.driveSpeed - self.rotateSpeed

        # Adjust for directions
        if self.leftRightSwap == False:
                self.actualLeftSpeed = self.leftSpeed
                self.actualRightSpeed = self.rightSpeed
        else:
                self.actualLeftSpeed = self.rightSpeed
                self.actualRightSpeed = self.leftSpeed

        if self.leftReverse == True:
                self.actualLeftSpeed = self.actualLeftSpeed * -1

        if self.rightReverse == TRUE: 
                self.actualRightSpeed = self.actualRightSpeed * -1

        # Left motor
        if self.actualLeftMotor == 0:
                self.leftMotor.setSpeed(0)
                self.leftMotor.run(Adafruit_MotorHAT.RELEASE)
        else: 
            if self.actualLeftMotor > 0:
                self.leftMotor.run(Adafruit_MotorHAT.FORWARD)
                self.leftMotor.setSpeed(self.actualLeftMotor)
            else:
                self.leftMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.leftMotor.setSpeed(abs(self.actualLeftMotor))        
                
        # Right motor
        if self.actualRightMotor == 0:
                self.rightMotor.setSpeed(0)
                self.rightMotor.run(Adafruit_MotorHAT.RELEASE)
        else: 
            if self.actualRightMotor > 0:
                self.rightMotor.run(Adafruit_MotorHAT.FORWARD)
                self.rightMotor.setSpeed(self.actualRightMotor)
            else:
                self.rightMotor.run(Adafruit_MotorHAT.BACKWARD)
                self.rightMotor.setSpeed(abs(self.actualRightMotor))        


