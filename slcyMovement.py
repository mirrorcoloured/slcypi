import RPi.GPIO as GPIO
import time
from slcyPins import *

class Servo():
    """Initialize with control pin
    pin <int>
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action
    """
    # RED       VCC     5 V
    # BROWN     GND     0 V
    # ORANGE    CTRL    GPIO
    def __init__(self, pin, name='', verbose=False):
        self.name = name
        self.verbose = verbose
        self.pin = pin
        self.__position__ = 3 # ensures the first move has enough time
        if self.verbose:
            print('Initializing Servo',self.name,'...',end=' ')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.__pwm__ = PWMPin(self.pin, freq=50, dutycycle=0, on=True)
        time.sleep(2)
        if self.verbose:
            print('Done')
    def __posmap__(self, value) -> float:
        """Returns a mapping transformation
        [-1,1] -> [1,10]
        """
        # dx = 2 # -1 to 1
        # dy = 9 # 1 to 10
        # ox = 1 # -1 -> 0
        # oy = 1 # 0 -> 1
        # (value + ox) * (dy / dx) + oy
        return ((value * -1) + 1) * (9 / 2) + 1
    def __inrange__(self, value) -> bool:
        """Checks if a value is between -1 and 1"""
        return value >= -1 and value <= 1
    def getpos(self) -> float:
        return self.__position__
    def move(self, position) -> None:
        """Moves to a specified position
        ---
        position <float>, [-1,1] left to right
        """
        if self.__inrange__(position):
            if self.verbose:
                print(self.name,'moving to position',position,'...',end='')
            dt = abs(self.__position__ - position) * .25
            self.__pwm__.setdutycycle(self.__posmap__(position))
            time.sleep(dt)
            self.__pwm__.setdutycycle(0)
            self.__position__ = position
            if self.verbose:
                print('Done')
        else:
            print('Error, position must be between -1 and 1')
    def left(self, distance) -> None:
        """Moves the servo left (min -1)"""
        if self.verbose:
            print(self.name,'moving left',distance)
        target = self.__position__ - distance
        if self.__inrange__(target):
            self.move(target)
        else:
            print('Position must be between -1 and 1, stopping at boundary')
            self.move(max(min(target,1),-1))
    def right(self, distance) -> None:
        """Moves the servo right (max 1)"""
        if self.verbose:
            print(self.name,'moving right',distance)
        target = self.__position__ + distance
        if self.__inrange__(target):
            self.move(target)
        else:
            print('Position must be between -1 and 1, stopping at boundary')
            self.move(max(min(target,1),-1))
    def center(self) -> None:
        """Returns to center [0]"""
        if self.verbose:
            print(self.name,'moving to center')
        self.move(0)

class DCMotor():
#   OA |-\/-| GND
#  VCC |    | IB
#  VCC |    | IA
#   OB |----| GND
# VCC accepts 2.5 - 12 V
    def __init__(self, name, pins, on=True ,direction=1, speed=50, verbose=False):
        self.name = name
        self.verbose = verbose
        if self.verbose:
            print(self.name,'setting up')
        self.direction = direction
        self.speed = speed
        self.running = on
        if type(pins) is dict:
            self.pins = pins
        elif type(pins) is list:
            p = {}
            c = ['IA','IB']
            i = 0
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['IA'], GPIO.OUT)
        GPIO.setup(self.pins['IB'], GPIO.OUT)
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm = PWMPin(self.pins['IA'],2000,self.speed)
    def start(self):
        if self.verbose:
            print(self.name,'starting up')
        self.running = True
        if self.direction:
            self.forward()
        else:
            self.backward()
    def stop(self):
        if self.verbose:
            print(self.name,'stopping')
        self.running = False
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.off()
    def power(self):
        if self.verbose:
            print(self.name,'toggling power')
        if self.running:
            self.stop()
        else:
            self.start()
    def forward(self):
        if self.verbose:
            print(self.name,'going forward')
        self.direction = 1
        GPIO.output(self.pins['IA'], GPIO.HIGH)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.on()
    def backward(self):
        if self.verbose:
            print(self.name,'going backward')
        self.direction = 0
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.HIGH)
        self.pwm.on()
    def reverse(self):
        if self.verbose:
            print(self.name,'toggling direction')
        if self.running:
            if self.direction:
                self.forward()
            else:
                self.backward()
        else:
            if self.direction:
                self.direction = 0
            else:
                self.direction = 1
    def setspeed(self,speed=50):
        if self.verbose:
            print(self.name,'setting speed to',speed)
        self.speed = speed
        if self.direction:
            self.pwm.setdutycycle(self.speed)
        else:
            self.pwm.setdutycycle(100 - self.speed)
