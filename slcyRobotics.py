import RPi.GPIO as GPIO
import time
#from slcypi.slcyMovement import *
#from slcypi.slcySensors import *
import slcypi.slcyMovement as Movement
import slcypi.slcySensors as Sensors

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
        self.conversion = {'in':39.3701, 'inch':39.3701, 'inches':39.3701,
                           'ft':3.28084, 'foot':3.28084, 'feet':3.28084,
                           'cm':10, 'centimeters':10}
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['serv'], GPIO.OUT)
        self.__pwm__ = PWMPin(self.pin, freq=50, dutycycle=0, on=True)
        GPIO.setup(self.pins['trig'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pins['echo'], GPIO.IN)
        self.__u__ = UltrasonicSensor([self.pins['trig'],self.pins['echo']],name+'(sensor)',self.verbose)
        if self.verbose:
            print('Done')
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
                self.move(i)
                r.add(self.measure())
            return r

