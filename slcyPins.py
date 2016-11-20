import RPi.GPIO as GPIO

import slcypi.slcyGeneral as General

# GPIO.HIGH = 1
# GPIO.LOW = 0

class OutPin():
    """Sets up a pin for output
    pin <dict>, <list>, <int>, {'out':1}
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pins={},name='',verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing OutPin',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['out'],pins)
        self.__outpinsetup__()
        if self.__verbose__:
            print('Done')
    def __outpinsetup__(self) -> None:
        if self.__verbose__:
            print(self.__name__,'set to output')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pins__['out'], GPIO.OUT, initial=0)
        self.__on__ = False
    def on(self) -> bool:
        """Turns the pin on (sets to 3.3 V)"""
        if self.__verbose__:
            print(self.__name__,self.__pins__['out'],'on')
        GPIO.output(self.pin,1)
        self.__on__ = True
        return self.__on__
    def off(self) -> bool:
        """Turns the pin off (sets to 0 V)"""
        if self.__verbose__:
            print(self.__name__,self.__pins__['out'],'off')
        GPIO.output(self.pin,0)
        self.__on__ = False
        return self.__on__
    def toggle(self) -> bool:
        """Toggles the pin on/off"""
        if self.__verbose__:
            print(self.__name__,self.__pins__['out'],'toggled')
        self.__on__ = not self.__on__
        GPIO.output(self.pin,self.__on__)
        return self.__on__
    def get(self) -> bool:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.__verbose__:
            print(self.__name__,self.__pins__['out'],'getting value')
        return self.__on__

class InPin():
    """Sets up a pin for input
    pins <dict>, <list>, <int>, {'in':1}
    [pud] <str> 'OFF', 'DOWN', or 'UP', sets an internal pull-up or pull-down resistor
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pins,pud='OFF',name='',verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing InPin',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['in'],pins)
        self.__inpinsetup__(pud)
        if self.__verbose__:
            print('Done')
    def __inpinsetup__(self,pud) -> None:
        GPIO.setmode(GPIO.BOARD)
        if pud == 'OFF':
            if self.__verbose__:
                print(self.__name__,'set to input (no internal resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_OFF)
        elif pud == 'UP':
            if self.__verbose__:
                print(self.__name__,'set to input (pull-up resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_UP)
        elif pud == 'DOWN':
            if self.__verbose__:
                print(self.__name__,'set to input (pull-down resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_DOWN)
        else:
            print('Invalid PUD value:',pud)
    def get(self) -> bool:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.__verbose__:
            print(self.__name__,'getting value')
        return GPIO.input(self.__pins__['in'])

class EventPin():
    """Sets up a pin for input with a triggering function
    pins <dict>, <list>, <int>, {'in':1}
    function <func>
    [risefall] <str> 'RISING' or 'FALLING', detects signal edges up or down
    [pud] <str> 'OFF', 'DOWN', or 'UP', sets an internal pull-up or pull-down resistor
    [bouncetime] <int>, ms to ignore repeated triggers
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pins,function,risefall='RISING',pud='OFF',bouncetime=250,name='',verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing EventPin',self.__name__,'...',end=' ')
        self.__function__ = function
        self.__pins__ = General.LoadPins(['in'],pins)
        self.__eventpinsetup__(pud,risefall,bouncetime,function)
        if self.__verbose__:
            print('Done')
    def __eventpinsetup__(self,pud,risefall,bouncetime,function) -> None:
        GPIO.setmode(GPIO.BOARD)
        if pud == 'OFF':
            if self.__verbose__:
                print(self.__name__,'set to input (no internal resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_OFF)
        elif pud == 'UP': # GPIO <-> button <-> GND
            if self.__verbose__:
                print(self.__name__,'set to input (pull-up resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_UP)
        elif pud == 'DOWN': # GPIO <-> button <-> 3.3V
            if self.__verbose__:
                print(self.__name__,'set to input (pull-down resistor)')
            GPIO.setup(self.__pins__['in'],GPIO.IN,GPIO.PUD_DOWN)
        else:
            print('Invalid PUD value:',pud)
        if risefall == 'RISING':
            if self.__verbose__:
                print(self.__name__,'set to input (off)')
            #GPIO.add_event_detect(self.pin,GPIO.FALLING,function,bouncetime=self.bouncetime) #opposite due to wiring
            GPIO.add_event_detect(self.__pins__['in'],GPIO.FALLING,bouncetime=bouncetime)
        elif risefall == 'FALLING':
            if self.__verbose__:
                print(self.__name__,'set to input (up)')
            #GPIO.add_event_detect(self.pin,GPIO.RISING,function,bouncetime=self.bouncetime)
            GPIO.add_event_detect(self.__pins__['in'],GPIO.RISING,bouncetime=bouncetime)
        else:
            print('Invalid RISEFALL value:',risefall)
        GPIO.add_event_callback(self.pin,function)
    def setfunction(self,function) -> None:
        """Not implemented
        Need to figure out how to remove event detect triggers
        """
        pass
    def get(self) -> bool:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.__verbose__:
            print(self.__name__,'getting value')
        return GPIO.input(self.__pins__['in'])

class PWMPin():
    """Sets up a pin for pulse width modulated output
    pins <dict>, <list>, <int>, {'out':1}
    [freq] <int> frequency of cycle
    [dutycycle] <int>, percentage of time active (0-100)
    [on] <bool>, start on
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self, pins, freq=1023, dutycycle=100, on=False, name='', verbose=False):
        self.__name__ = name
        self.__verbose__ = verbose
        if self.__verbose__:
            print('Initializing PWMPin',self.__name__,'...',end=' ')
        self.__pins__ = General.LoadPins(['out'],pins)
        self.__pwmpinsetup__(on,freq,dutycycle)
        if self.__verbose__:
            print('Done')
    def __pwmpinsetup__(self,on,freq,dutycycle) -> None:
        if self.__verbose__:
            print(self.__name__,'set to output')
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.__pins__['out'], GPIO.OUT, initial=0)
        self.__on__ = on
        self.__freq__ = freq
        self.__dc__ = dutycycle
        self.__pwm__ = GPIO.PWM(self.__pins__['out'], self.__freq__)
        if self.__verbose__:
            print(self.__name__,'set to PWM (',self.__freq__,' Hz ,',self.__dc__,'%) ON:',on)
        if on:
            self.__pwm__.start(self.__dc__)
    def on(self) -> None:
        """Turns the PWM pin on"""
        if self.__verbose__:
            print(self.__name__,'on')
        self.__pwm__.start(self.dutycycle)
    def off(self) -> None:
        """Turns the PWM pin off"""
        if self.__verbose__:
            print(self.__name__,'off')
        self.__pwm__.stop()
    def setfreq(self, freq) -> None:
        """Sets the frequency of the PWM pin
        freq <int>
        """
        if self.__verbose__:
            print(self.__name__,'setting frequency to',freq)
        self.__freq__ = freq
        self.__pwm__.ChangeFrequency(self.__freq__)
    def setdutycycle(self, dutycycle) -> None:
        """Sets the duty cycle of the PWM pin
        dutycycle <int>, (1-100)
        """
        if self.__verbose__:
            print(self.__name__,'setting duty cycle to',dutycycle)
        self.__dc__ = dutycycle
        self.__pwm__.ChangeDutyCycle(self.__dc__)
