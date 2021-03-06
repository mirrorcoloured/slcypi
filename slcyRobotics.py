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
    [serv, trig, echo]
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
    def sweep(self, a, b, step) -> DataStructures.Dataset:
        """Takes a series of measurements across an angle range
        a <float>, a and b must be within [-1, 1]
        b <float>, 
        step <float>, must agree with a -> b direction
        """
        if b == a or step == 0:
            print('Error, distance or step 0')
        elif (b < a and step > 0) or (b > a and step < 0):
            print('Error, step and a -> b do not match')
        else:
            if self.__verbose__:
                print(self.__name__,'sweeping from',a,'to',b,'with step',step)
            x = self.__linearsteps__(a,b,step)
            r = DataStructures.Dataset([])
            for i in x:
                self.move(i)
                r.append(self.measure())
            self.__lastresult__ = r
            return r
    def __constructresult__(self,result) -> DataStructures.Dataset:
        d = DataStructures.Dataset([])
        t = General.TimeString()
        p = self.__position__
        d.add(dist=result, time=t, pos=p)
        return d
    def multisweep(self, a, b, step, passes, reverse=True) -> DataStructures.Dataset:
        """Takes repeated series of measurements across an angle range
        a <float>, a and b must be within [-1, 1]
        b <float>, 
        step <float>, must agree with a -> b direction
        passes <int>, how many times to repeat the sweep
        reverse <bool>, alternate left->right, right->left
        """
        if self.__verbose__:
            print(self.__name__,'sweeping from',a,'to',b,'with step',step,',',passes,'times')
        r = DataStructures.Dataset()
        goback = False
        count = 0
        while count < passes:
            if reverse and goback:
                r.append(self.measure(b,a,step))
                goback = False
            else:
                r.append(self.measure(a,b,step))
                goback = True
            count += 1
        self.__lastresult__ = r
        return r
    def followme(self) -> None:
        self.__following__ = True
        self.__scan__()
    def __scan__(self) -> None:
        try:
            if self.__following__:
                print(self.__name__,'starting following routine')
                scanstep = .05 # rotation resolution
                maxdist = 2 #
                scan = self.sweep(-1,1,scanstep) # initial scan of surroundings
                #scan.removeitems(dist='>'+str(maxdist)) # remove timeout values
                closest = scan.min('dist') # find closest measurement
                aim = closest['pos'] # get position of target
                rng = closest['dist'] # get distance to target
                self.move(aim) # move to position
                print(self.__name__,'following target at position',aim,'and distance',rng)
                self.__track__(aim, rng) # enter follow mode
        except KeyboardInterrupt:
            self.__stopfollowing__()
    def __track__(self, pos, dist) -> None:
        try:
            if self.__following__:
                trackstep = .05 # rotation resolution
                tracklimit = .5 # how far to look from last known position
                x = self.__searchsteps__(pos, tracklimit, trackstep) # generate local search positions
                for p in x:
                    self.move(p) # move to a nearby position
                    m = self.measure().list[0] # get a single measurement
                    if abs(m['dist']) > dist: # found it again
                        self.__track__(m['pos'], m['dist']) # go back to following
                print(self.__name__,'target not found nearby, restarting wide scan')
                self.__scan__() # target not found nearby, restart wide scan
        except KeyboardInterrupt:
            self.__stopfollowing__()
    def __stopfollowing__(self) -> None:
        print(self.__name__,'exiting follow routine')
        self.__following__ = False
