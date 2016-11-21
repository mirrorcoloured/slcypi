import RPi.GPIO as GPIO

import slcypi.slcyDataStructures as DataStructures
import slcypi.slcyGeneral as General
import time

class UltrasonicSensor():
    """Initialize with list of GPIO pins according to:
    pins <list> or <dict>, {'trig':1, 'echo':2}
    [name] <str>, identify this sensor
    [verbose] <bool>, print every action
    """
# |-------------------|
# |     O       O     |
# |---|---|---|---|---|
#   VCC TRIG ECHO GND
    def __init__(self, pins, name='', verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing Ultrasonic Sensor',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['trig','echo'],pins)
        self.__ultrasonicsensorsetup__()
        time.sleep(2)
        if self.__verbose__:
            print('Done')
    def __ultrasonicsensorsetup__(self) -> None:
        self.__lastresult__ = 0
        self.__conversion__ = {'m':1, 'meter':1, 'meters':1,
                               'cm':10, 'centimeter':10, 'centimeters':10,
                               'in':39.3701, 'inch':39.3701, 'inches':39.3701,
                               'ft':3.28084, 'foot':3.28084, 'feet':3.28084}
        self.__unitname__ = 'meter'
        self.__unit__ = self.__conversion__[self.__unitname__]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pins__['trig'], GPIO.OUT, initial=0)
        GPIO.setup(self.__pins__['echo'], GPIO.IN)
    def getlastresult(self) -> DataStructures.Dataset:
        """Returns the last measured result
        """
        return self.__lastresult__
    def __printimage__(self,dist) -> None:
        dist = int(dist)
        o = '|O'
        for i in range(dist):
            o += ' '
        o += 'X'
        print(o)
    def setunit(self, unit='m') -> None:
        """Sets the measurement unit:
        unit <str>,  m  cm  in  ft
        """
        if self.__verbose__:
            print(self.__name__,'setting unit to',unit)
        if unit in self.__conversion__:
            self.__unit__ = self.__conversion__[unit]
        else:
            print('Invalid unit entered:',unit)
    def continuousmeasure(self, interval, digits=4) -> DataStructures.Dataset:
        d = DataStructures.Dataset()
        try:
            if self.__verbose__:
                print(self.__name__,'measuring every',interval,'...')
            while True:
                d.append(self.measure(digits, True))
                time.sleep(interval)
        except KeyboardInterrupt:
            self.__lastresult__ = d
            return d
    def measure(self, digits=4, printimage=False) -> float:
        """---
        Returns a distance measurement
        Takes < 0.02 s to resolve
        ---
        [digits] <int>, how many digits to round to
        """
        if self.__verbose__:
            print(self.__name__,'taking a measurement')
        GPIO.output(self.__pins__['trig'], GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(self.__pins__['trig'], GPIO.LOW)
        while not GPIO.input(self.__pins__['echo']):
            pass
        t1 = time.time()
        while GPIO.input(self.__pins__['echo']):
            pass
        t2 = time.time()
        r = round((t2-t1) * 340 / 2, digits) * self.__unit__
        if printimage:
            self.__printimage__(r / self.__unit__)
        if self.__verbose__:
            print(self.__name__,'measured',r,self.__unitname__)
        d = self.__constructresult__(r)
        self.__lastresult__ = d
        return d
    def __constructresult__(self,result) -> DataStructures.Dataset:
        d = DataStructures.Dataset()
        t = General.TimeString()
        d.add(dist=result, time=t)
        return d
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
        if self.__verbose__:
            print(self.__name__,'taking',tm,'measurements over',tm*interval,'seconds')
        o = DataStructures.Dataset() # initialize Dataset
        while len(o) < tm: # until I have enough data points
            o.append(self.measure(digits))
            time.sleep(interval)
        if self.__verbose__:
            print(self.__name__,'completed multimeasure')
        self.__lastresult__ = o
        return o
