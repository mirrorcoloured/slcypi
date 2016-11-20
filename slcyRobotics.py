import RPi.GPIO as GPIO
import time
#from slcypi.slcyMovement import *
#from slcypi.slcySensors import *
import slcypi.slcyMovement as Movement
import slcypi.slcyDataStructures as DataStructures
import slcypi.slcySensors as Sensors
import slcypi.slcyPins as Pins
import slcypi.slcyGeneral as General

class UltraServo(Movement.Servo, Sensors.UltrasonicSensor):
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
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing UltraServo',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['serv','trig','echo'],pins)
        self.__ultraservosetup__()
        if self.__verbose__:
            print('Done')
    def __ultraservosetup__(self) -> None:
        self.__servosetup__()
        self.__ultrasonicsensorsetup__()
    # COMBINED FUNCTIONS
    def sweep(self, a, b, step) -> DataStructures.Dataset:
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
            if self.__verbose__:
                print(self.__name__,'sweeping from',a,'to',b,'with step',step)
            rng = abs(b - a)
            dx = int((rng) / step) + 1
            x = []
            for i in range(dx):
                x.append(a + i * step)
            x.append(b)
            r = DataStructures.Dataset([])
            for i in x:
                self.move(i)
                r.append(self.measure())
            self.__lastresult__ = r
            return r

