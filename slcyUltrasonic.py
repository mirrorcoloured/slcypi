import RPi.GPIO as GPIO
import time

def Sleep(seconds):
    time.sleep(seconds)

class Dataset():
    """---
    List container with some basic number analysis
    ---
    data <list>
    """
    def __init__(self, data):
        self.data = data
    def add(self,data): #create .add() function
        for d in data:
            self.data.append(d)
    def append(self,data): #extend .append() function
        self.data.append(data)
    def __add__(self,data): #overload + operator
        self.data.append(data)
    def __len__(self): #overload len() function
        return len(self.data)
    def __max__(self): #overload max() function
        return max(self.data)
    def __min__(self): #overload min() function
        return min(self.data)
    def avg(self) -> float:
        """Returns the average of the data contained"""
        return sum(self.data)/len(self.data)
    def sd(self) -> float:
        """Returns 1 SD of the data contained"""
        avg = self.avg()
        va = []
        for d in self.data:
            va.append((d - avg) ** 2)
        var = 0
        for v in va:
            var += v
        var = var / len(va)
        return var ** (1/2)
    def removeoutliers(self, c=1) -> Dataset:
        """Returns a new Dataset, excluding any data points +- c standard deviations
        [c] <int>
        """
        avg = self.avg()
        sd = self.sd()
        new = []
        for d in self.data:
            if abs(d-avg) < sd:
                new.append(d)
        return Dataset(new)

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
    def __init__(self, pins, name='', verbose=False):
        self.name = name
        if type(pins) is dict:
            self.pins = pins
        elif type(pins) is list:
            p = {}
            c = ['trig','echo']
            i = 0
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        if verbose:
            print('Initializing Ultrasonic Sensor',name)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['trig'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pins['echo'], GPIO.IN)
        Sleep(2)
    def measure(self, digits=4) -> float:
        """---
        Returns a distance measurement
        Takes < 0.02 s to resolve
        ---
        [digits] <int>, how many digits to round to
        """
        if verbose:
            print(name,'taking a measurement')
        GPIO.output(self.pins['trig'], GPIO.HIGH)
        Sleep(0.000015)
        GPIO.output(self.pins['trig'], GPIO.LOW)
        while not GPIO.input(self.pins['echo']):
            pass
        t1 = time.time()
        while GPIO.input(18):
            pass
        t2 = time.time()
        r = round((t2-t1) * 340 / 2, digits)
        if verbose:
            print(name,'measured',r)
        return r
    def multimeasure(self, interval=.1, totalmeasurements=None, totaltime=None, digits=4) -> Dataset:
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
        o = Dataset([]) # initialize Dataset
        while len(o) < tm: # until I have enough data points
            o.append(self.measure(digits))
            Sleep(interval)
        return o
