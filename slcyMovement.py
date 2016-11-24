import RPi.GPIO as GPIO
import time

import slcypi.slcyPins as Pins
import slcypi.slcyGeneral as General

class Servo():
    """Initialize with control pin
    pins <dict>, <list>, <int>, {'serv':1}
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action"""
    # RED       VCC     5 V
    # BROWN     GND     0 V
    # ORANGE    CTRL    GPIO
    def __init__(self, pins, name='', verbose=False) -> None:
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing Servo',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['serv'],pins)
        self.__servosetup__()
        time.sleep(2)
        if self.__verbose__:
            print('Done')
    def __servosetup__(self) -> None:
        GPIO.setmode(GPIO.BOARD)
        self.__pwm__ = Pins.PWMPin(self.__pins__['serv'], freq=50, dutycycle=0, on=True)
        self.__position__ = 1 # ensures the first move has enough time
        self.center() # initializes to center
    def __linearsteps__(self, a, b, step, includeends=True) -> list:
        """Generates a list of linear steps from a to b
        a <float>
        b <float>
        step <float>
        [includeends] <bool>"""
        if (a < b and step > 0) or (a > b and step < 0):
            o = []
            rng = abs(b - a)
            steps = int(rng / step) + 1
            for i in range(steps):
                o.append(a + i * step)
            if includeends and o[len(o)-1] != b:
                o.append(b)
            return o
        else:
            print('Error, step and a -> b direction do not match')
    def __searchsteps__(self, c, r, step, bounds=[-1,1]) -> list:
        """Generates a list of steps centered at c going out r on either side
        c <float>
        r <float>
        step <float>
        [bounds] <list> of <float>"""
        if bounds[0] <= c <= bounds[1] and r > 0:
            o = []
            plus = True
            leftbound = max(bounds[0], c - r)
            rightbound = min(bounds[1], c + r)
            for i in range(1,int(r / step) + 1):
                p = c + i * step
                m = c - i * step
                if leftbound <= p <= rightbound:
                    o.append(p)
                if leftbound <= m <= rightbound:
                    o.append(m)
            return o
        else:
            print('Error, invalid searchstep configuration')
    def __posmap__(self, value) -> float:
        """Returns a mapping transformation
        [-1,1] -> [1,10]"""
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
        """Returns the servo position (Between -1 and 1)"""
        return self.__position__
    def move(self, target) -> None:
        """Moves to a specified position
        position <float>, [-1,1] left to right"""
        if self.__inrange__(target):
            if self.__verbose__:
                print(self.__name__,'moving to position',target,'...',end='')
            dt = abs(self.__position__ - target) * .3
            self.__pwm__.setdutycycle(self.__posmap__(target))
            time.sleep(dt)
            self.__pwm__.setdutycycle(0)
            self.__position__ = target
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
    """Initialize with control pin
    pins <dict>, <list>, <int>, {'IA':1,'IB':2}
    direction <int>, 1 forward, -1 backward
    speed <int>, [0:100]
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action"""
#   OA |-\/-| GND
#  VCC |    | IB
#  VCC |    | IA
#   OB |----| GND
# VCC accepts 2.5 - 12 V
    def __init__(self, pins, direction=1, speed=50, on=True, name = '', verbose=False) -> None:
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing DCMotor',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['IA','IB'],pins)
        self.__dcmotorsetup__(direction,speed,on)
        if self.__verbose__:
            print('Done')
    def __dcmotorsetup__(self,direction,speed,on) -> None:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pins__['IA'], GPIO.OUT, initial=0)
        GPIO.setup(self.__pins__['IB'], GPIO.OUT, initial=0)
        self.__pwm__ = PWMPin(self.__pins__['IA'],2000, self.__speed__)
        self.__direction__ = direction
        self.__speed__ = speed
        self.__running__ = on
    def on(self) -> None:
        """Turns the motor on"""
        if self.__verbose__:
            print(self.__name__,'starting up')
        self.__running__ = True
        if self.__direction__:
            self.forward()
        else:
            self.backward()
    def off(self) -> None:
        """Turns the motor off"""
        if self.__verbose__:
            print(self.__name__,'stopping')
        self.__running__ = False
        GPIO.output(self.__pins__['IA'], 0)
        GPIO.output(self.__pins__['IB'], 0)
        self.__pwm__.off()
    def power(self) -> bool:
        """Toggles the motor on/off
        Returns whether motor is now running"""
        if self.__verbose__:
            print(self.__name__,'toggling power')
        if self.__running__:
            self.off()
            return self.isrunning()
        else:
            self.on()
            return True
    def forward(self) -> None:
        """Runs motor forward"""
        if self.__verbose__:
            print(self.__name__,'going forward')
        self.__direction__ = 1
        GPIO.output(self.__pins__['IA'], 1)
        GPIO.output(self.__pins__['IB'], 0)
        self.__pwm__.on()
    def backward(self) -> None:
        """Runs motor backward"""
        if self.__verbose__:
            print(self.__name__,'going backward')
        self.__direction__ = 0
        GPIO.output(self.__pins__['IA'], 0)
        GPIO.output(self.__pins__['IB'], 1)
        self.__pwm__.on()
    def reverse(self) -> None:
        """Reverses the direction of the motor"""
        if self.__verbose__:
            print(self.__name__,'toggling direction')
        if self.__running__:
            if self.__direction__:
                self.forward()
            else:
                self.backward()
        else:
            if self.__direction__:
                self.__direction__ = 0
            else:
                self.__direction__ = 1
    def setspeed(self,speed=50) -> None:
        """Sets the speed of the motor
        speed <int>, [0:100]"""
        if self.__verbose__:
            print(self.__name__,'setting speed to',speed)
        self.__speed__ = speed
        if self.__direction__:
            self.__pwm__.setdutycycle(self.__speed__)
        else:
            self.__pwm__.setdutycycle(100 - self.__speed__)
    def getspeed(self) -> float:
        """Returns the current speed"""
        return self.__speed__
    def getdirection(self) -> int:
        """Returns the direction of rotation {backward:0, forward:1}"""
        return self.__direction__
    def isrunning(self) -> bool:
        """Returns whether the motor is running"""
        return self.__running__
