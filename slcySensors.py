import RPi.GPIO as GPIO

#from slcypi.slcyDataStructures import *
import slcypi.slcyDataStructures as DataStructures
import time

class UltrasonicSensor():
    """Initialize with list of GPIO pins according to:
    [trig, echo]
    pins <list> or <dict>
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action
    """
# |-------------------|
# |     O       O     |
# |---|---|---|---|---|
#   VCC TRIG ECHO GND

# appears to be reading in meters
# [ ] add conversion to different units
# [ ] add continuous read mode
# [ ] add visual distance output
#     |O       x
#     |O        x
    def __init__(self, pins, name='', verbose=False):
        self.name = name
        self.verbose = verbose
        if self.verbose:
            print('Initializing Ultrasonic Sensor',self.name,'...',end=' ')
        if type(pins) is dict:
            self.pins = pins
        elif type(pins) is list:
            p = {}
            c = ['trig','echo']
            i = 0
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        self.__lastresult__ = 0
        self.conversion = {'in':39.3701, 'inch':39.3701, 'inches':39.3701,
                           'ft':3.28084, 'foot':3.28084, 'feet':3.28084,
                           'cm':10, 'centimeters':10}
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['trig'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pins['echo'], GPIO.IN)
        time.sleep(2)
        if self.verbose:
            print('Done')
    def getlastresult(self):
        return self.__lastresult__
    def measure(self, digits=4) -> float:
        """---
        Returns a distance measurement
        Takes < 0.02 s to resolve
        ---
        [digits] <int>, how many digits to round to
        """
        if self.verbose:
            print(self.name,'taking a measurement')
        GPIO.output(self.pins['trig'], GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.pins['trig'], GPIO.LOW)
        while not GPIO.input(self.pins['echo']):
            pass
        t1 = time.time()
        while GPIO.input(self.pins['echo']):
            pass
        t2 = time.time()
        r = round((t2-t1) * 340 / 2, digits)
        if self.verbose:
            print(self.name,'measured',r)
        self.__lastresult__ = r
        return r
    def multimeasure(self, interval=.1, totalmeasurements=None, totaltime=None, digits=4) -> DataStructures.Dataset:
        """Takes regular measurements, up to a max number or time, and returns a Dataset object
        interval <float>, time between each measurement
        totalmeasurements <int>, max number of measurements
        totaltime <float>, max time of series of measurements
        [digits] <int>, how many digits to round to
        """
        if totalmeasurements == None and totaltime == None:
            print('Error, no max measurements or time provided.')
            return None    
        elif totaltime != None and totalmeasurements == None:
            tm = totaltime / interval
        elif totaltime == None and totalmeasurements != None:
            tm = totalmeasurements
        else:
            tm = min(totaltime / interval, totalmeasurements)
        if self.verbose:
            print(self.name,'taking',tm,'measurements over',tm*interval,'seconds')
        o = DataStructures.Dataset([]) # initialize Dataset
        while len(o) < tm: # until I have enough data points
            o.append(self.measure(digits))
            time.sleep(interval)
        if self.verbose:
            print(self.name,'completed multimeasure')
        self.__lastresult__ = o
        return o
