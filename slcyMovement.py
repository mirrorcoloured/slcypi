import RPi.GPIO as GPIO
import time
#from slcypi.slcyPins import *
import slcypi.slcyPins as Pins

class Servo():
    """Initialize with control pin
    pins <dict>, <list>, <int>, {'serv':1}
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action
    """
    # RED       VCC     5 V
    # BROWN     GND     0 V
    # ORANGE    CTRL    GPIO
    def __init__(self, pins, name='', verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing Servo',self.__name__,'...',end=' ')
        self.__position__ = 0 # ensures the first move has enough time
        self.__pins__ = self.__loadpins__(pins)
        self.__setup__()
        time.sleep(2)
        if self.__verbose__:
            print('Done')
    def __loadpins__(self,inp) -> dict:
        if type(inp) is int:
            return {'serv':inp}
        elif type(inp) is list:
            return {'serv':inp[0]}
        elif type(inp) is dict:
            return inp
        else:
            print('Invalid input type for pins:',inp,type(inp))
            return {}
    def __setup__(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        self.__pwm__ = Pins.PWMPin(self.__pins__['serv'], freq=50, dutycycle=0, on=True)
        self.__on__ = False
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
        """Returns the servo position (Between -1 and 1)
        """
        return self.__position__
    def move(self, position) -> None:
        """Moves to a specified position
        ---
        position <float>, [-1,1] left to right
        """
        if self.__inrange__(position):
            if self.__verbose__:
                print(self.__name__,'moving to position',position,'...',end='')
            dt = abs(self.__position__ - position) * .25
            self.__pwm__.setdutycycle(self.__posmap__(position))
            time.sleep(dt)
            self.__pwm__.setdutycycle(0)
            self.__position__ = position
            if self.__verbose__:
                print('Done')
        else:
            print('Error, position must be between -1 and 1')
    def left(self, distance) -> None:
        """Moves the servo left (min -1)"""
        if self.__verbose__:
            print(self.__name__,'moving left',distance)
        target = self.__position__ - distance
        if self.__inrange__(target):
            self.move(target)
        else:
            print('Position must be between -1 and 1, stopping at boundary')
            self.move(max(min(target,1),-1))
    def right(self, distance) -> None:
        """Moves the servo right (max 1)"""
        if self.__verbose__:
            print(self.__name__,'moving right',distance)
        target = self.__position__ + distance
        if self.__inrange__(target):
            self.move(target)
        else:
            print('Position must be between -1 and 1, stopping at boundary')
            self.move(max(min(target,1),-1))
    def center(self) -> None:
        """Returns to center [0]"""
        if self.__verbose__:
            print(self.__name__,'moving to center')
        self.move(0)

class DCMotor():
#   OA |-\/-| GND
#  VCC |    | IB
#  VCC |    | IA
#   OB |----| GND
# VCC accepts 2.5 - 12 V
    def __init__(self, name, pins, on=True ,direction=1, speed=50, verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print(self.__name__,'setting up')
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
        if self.__verbose__:
            print(self.__name__,'starting up')
        self.running = True
        if self.direction:
            self.forward()
        else:
            self.backward()
    def stop(self):
        if self.__verbose__:
            print(self.__name__,'stopping')
        self.running = False
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.off()
    def power(self):
        if self.__verbose__:
            print(self.__name__,'toggling power')
        if self.running:
            self.stop()
        else:
            self.start()
    def forward(self):
        if self.__verbose__:
            print(self.__name__,'going forward')
        self.direction = 1
        GPIO.output(self.pins['IA'], GPIO.HIGH)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.on()
    def backward(self):
        if self.__verbose__:
            print(self.__name__,'going backward')
        self.direction = 0
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.HIGH)
        self.pwm.on()
    def reverse(self):
        if self.__verbose__:
            print(self.__name__,'toggling direction')
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
        if self.__verbose__:
            print(self.__name__,'setting speed to',speed)
        self.speed = speed
        if self.direction:
            self.pwm.setdutycycle(self.speed)
        else:
            self.pwm.setdutycycle(100 - self.speed)
