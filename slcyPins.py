import RPi.GPIO as GPIO

class OutPin():
    """Sets up a pin for output
    pin <int>
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pin,name='',verbose=False):
        self.pin = pin
        self.name = name
        self.verbose = verbose
        GPIO.setmode(GPIO.BOARD)
        if self.verbose:
            print(self.name,self.pin,'set to output')
        GPIO.setup(self.pin,GPIO.OUT)
    def on(self) -> None:
        """Turns the pin on (sets to 3.3 V)"""
        if self.verbose:
            print(self.name,self.pin,'on')
        GPIO.output(self.pin,GPIO.HIGH)
    def off(self) -> None:
        """Turns the pin off (sets to 0 V)"""
        if self.verbose:
            print(self.name,self.pin,'off')
        GPIO.output(self.pin,GPIO.LOW)
    def toggle(self) -> None:
        """Toggles the pin on/off"""
        if self.verbose:
            print(self.name,self.pin,'toggled')
        GPIO.output(self.pin,~self.get)
    def get(self) -> int:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.verbose:
            print(self.name,self.pin,'getting value')
        return GPIO.input(self.pin)

class InPin():
    """Sets up a pin for input
    pin <int>
    [pud] <str> 'OFF', 'DOWN', or 'UP', sets an internal pull-up or pull-down resistor
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pin,pud='OFF',name='',verbose=False):
        self.pin = pin
        self.name = name
        self.verbose = verbose
        GPIO.setmode(GPIO.BOARD)
        if ud == 'OFF':
            if self.verbose:
                print(self.name,self.pin,'set to input (off)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_OFF)
        elif ud == 'UP':
            if self.verbose:
                print(self.name,self.pin,'set to input (up)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_UP)
        elif ud == 'DOWN':
            if self.verbose:
                print(self.name,self.pin,'set to input (down)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_DOWN)
    def get(self) -> int:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.verbose:
            print(self.name,self.pin,'getting value')
        return GPIO.input(self.pin)

class EventPin():
    """Sets up a pin for input with a triggering function
    pin <int>
    function <func>
    [risefall] <str> 'RISING' or 'FALLING', detects signal edges up or down
    [pud] <str> 'OFF', 'DOWN', or 'UP', sets an internal pull-up or pull-down resistor
    [bouncetime] <int>, ms to ignore repeated triggers
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self,pin,function,risefall='RISING',pud=GPIO.PUD_UP,bouncetime=250,name='',verbose=False):
        self.pin = pin
        self.name = name
        self.function = function
        self.risefall = risefall
        self.pud = pud
        self.bouncetime = bouncetime
        self.verbose = verbose
        if self.verbose:
            print(name,'setting up',function,'on',pin)
        GPIO.setmode(GPIO.BOARD)
        if self.pud == GPIO.PUD_UP: # GPIO <-> button <-> GND
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_UP)
        elif self.pud == GPIO.PUD_DOWN: # GPIO <-> button <-> 3.3V
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_DOWN)
        if self.risefall == 'RISING':
            if self.verbose:
                print(self.name,self.pin,'set to input (off)')
            #GPIO.add_event_detect(self.pin,GPIO.FALLING,function,bouncetime=self.bouncetime) #opposite due to wiring
            GPIO.add_event_detect(self.pin,GPIO.FALLING,bouncetime=self.bouncetime)
        elif self.risefall == 'FALLING':
            if self.verbose:
                print(self.name,self.pin,'set to input (up)')
            #GPIO.add_event_detect(self.pin,GPIO.RISING,function,bouncetime=self.bouncetime)
            GPIO.add_event_detect(self.pin,GPIO.RISING,bouncetime=self.bouncetime)
        else:
            print('ERROR:',self.name,self.pin,'set to invalid risefall value')
        GPIO.add_event_callback(self.pin,function)
    def setfunction(self,function) -> None:
        """Not implemented
        Need to figure out how to remove event detect triggers
        """
        pass
    def get(self) -> int:
        """Returns the current status of the pin
        0 = OFF, 0 V
        1 = ON, 3.3 V
        """
        if self.verbose:
            print(self.pin,self.name,'getting value')
        return GPIO.input(self.pin)

class PWMPin():
    """Sets up a pin for pulse width modulated output
    pin <int>
    [freq] <int> frequency of cycle
    [dutycycle] <int>, percentage of time active (0-100)
    [on] <bool>, start on
    [name] <str>, identify this pin
    [verbose] <bool>, print every action
    """
    def __init__(self, pin, freq=1023, dutycycle=100, on=True, name='', verbose=False):
        self.pin = pin
        self.name = name
        self.freq = freq
        self.dutycycle = dutycycle
        self.verbose = verbose
        if self.verbose:
            print(self.name,self.pin,'set to PWM (',self.freq,'% ,',self.dutycycle,' Hz) ON:',on)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        if on:
            self.pwm.start(self.dutycycle)
    def on(self) -> None:
        """Turns the PWM pin on"""
        if self.verbose:
            print(self.name,self.pin,'on')
        self.pwm.start(self.dutycycle)
    def off(self) -> None:
        """Turns the PWM pin off"""
        if self.verbose:
            print(self.name,self.pin,'off')
        self.pwm.stop()
    def setfreq(self, freq) -> None:
        """Sets the frequency of the PWM pin
        freq <int>
        """
        if self.verbose:
            print(self.name,self.pin,'setting frequency to',freq)
        self.freq = freq
        self.pwm.ChangeFrequency(self.freq)
    def setdutycycle(self, dutycycle) -> None:
        """Sets the duty cycle of the PWM pin
        dutycycle <int>, (1-100)
        """
        if self.verbose:
            print(self.name,self.pin,'setting duty cycle to',dutycycle)
        self.dutycycle = dutycycle
        self.pwm.ChangeDutyCycle(self.dutycycle)
