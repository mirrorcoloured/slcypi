import RPi.GPIO as GPIO
import time
from slcyMovement import *
from slcySensors import *

class UltraServo():
    """Initialize with list of GPIO pins according to:
    [trig, echo, serv]
    pins <list> or <dict>
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action
    """
    # RED       VCC     5 V
    # BROWN     GND     0 V
    # ORANGE    CTRL    GPIO
    def __init__(self, pins, name='', verbose=False):
        self.name = name
        self.verbose = verbose
        if type(pins) is dict:
            self.pins = pins
        elif type(pins) is list:
            p = {}
            c = ['trig','echo','serv']
            i = 0
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        if self.verbose:
            print('Initializing UltraServo',self.name,'...',end=' ')
        self.__s__ = Servo(self.pins['serv'],name+'(servo)',self.verbose)
        self.__u__ = UltrasonicSensor([self.pins['trig'],self.pins['echo']],name+'(sensor)',self.verbose)
        if self.verbose:
            print('Done')
        # SENSOR FUNCTIONS
        def __measure__(self, digits=4) -> float:
            """---
            Returns a distance measurement
            Takes < 0.02 s to resolve
            ---
            [digits] <int>, how many digits to round to
            """
            return self.__u__.measure(digits)
        def __multimeasure__(self, interval=.1, totalmeasurements=None, totaltime=None, digits=4) -> Dataset:
            """Takes regular measurements, up to a max number or time, and returns a Dataset object
            interval <float>, time between each measurement
            totalmeasurements <int>, max number of measurements
            totaltime <float>, max time of series of measurements
            [digits] <int>, how many digits to round to
            """
            return self.__u__.multimeasure(interval, totalmeasurements, totaltime, digits)
        # SERVO FUNCTIONS
        def __posmap__(self, value) -> float:
            """Returns a mapping transformation
            [-1,1] -> [1,10]
            """
            return self.__s__.__posmap__(value)
        def __inrange__(self, value) -> bool:
            """Checks if a value is between -1 and 1"""
            return self.__s__.__inrange__(value)
        def __move__(self, position) -> None:
            """Moves to a specified position
            ---
            position <float>, [-1,1] left to right
            """
            self.__s__.move(position)
        def __left__(self, distance) -> None:
            """Moves the servo left (min -1)"""
            self.__s__.left(distance)
        def __right__(self, distance) -> None:
            """Moves the servo right (max 1)"""
            self.__s__.right(distance)
        def __center__(self) -> None:
            """Returns to center [0]"""
            self.__s__.center()
        # COMBINED FUNCTIONS
        def sweep(self, a, b, step) -> Dataset:
            """Takes a series of measurements across an angle range
            a <float>, a and b must be within [-1, 1]
            b <float>, 
            step <float>, must agree with a -> b direction
            """
            if b-a == 0 or step == 0:
                print('Error, distance or step 0')
            elif (b-a < 0 and step > 0) or (b-a > 0 and step < 0):
                print('Error, step and a -> b do not match')
            else:
                if self.verbose:
                    print(self.name,'sweeping from',a,'to',b,'with step',step)
                rng = abs(b - a)
                dx = int((rng) / step) + 1
                x = []
                for i in range(dx):
                    x.append(a + i * step)
                x.append(b)
                r = Dataset([])
                for i in x:
                    self.__s__.move(i)
                    r.add(self.__u__.measure())
                return r

