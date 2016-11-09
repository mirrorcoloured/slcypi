# Simple library for Raspberry Pi use
# Sky Chrastina
# Python 3.4.2

import RPi.GPIO as GPIO
from twython import Twython
import time

OUT = 0 # GPIO.OUT
IN = 1 # GPIO.IN
LOW = 0 # GPIO.LOW
HIGH = 1 # GPIO.HIGH
UP = 22 # GPIO.PUD_UP
DOWN = 21 # GPIO.PUD_DOWN
OFF = 20 # GPIO.PUD_OFF

APP_KEY='zmmlyAJzMDIntLpDYmSH98gbw'
APP_SECRET='ksfSVa2hxvTQKYy4UR9tjpb57CAynMJDsygz9qOyzlH24NVwpW'
OAUTH_TOKEN='794094183841566720-BagrHW91yH8C3Mdh9SOlBfpL6wrSVRW'
OAUTH_TOKEN_SECRET='d0Uucq2dkSHrFHZGLM1X8Hw05d80ajKYGl1zTRxZQSKTm'

applepislcy = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# HARDWARE
#   LED (0.005-0.02 A, only flows 1 way)
#       0 -> off
#       1 -> on
#   BUZZER ()
#       0 -> off
#       1 -> on
#   BUTTON (pressing completes the the connections on each side (not across))
#       

### GENERAL ###

def Sleep(seconds):
    time.sleep(seconds)

### GPIO ###

class InPin():
    def __init__(self,pin,name='',ud='OFF',verbose=False):
        self.pin = pin
        self.name = name
        self.verbose = verbose
        GPIO.setmode(GPIO.BOARD)
        if ud == OFF:
            if self.verbose:
                print(self.pin,self.name,'set to input (off)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_OFF)
        elif ud == UP:
            if self.verbose:
                print(self.pin,self.name,'set to input (up)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_UP)
        elif ud == DOWN:
            if self.verbose:
                print(self.pin,self.name,'set to input (down)')
            GPIO.setup(self.pin,GPIO.IN,GPIO.PUD_DOWN)
    def get(self):
        if self.verbose:
            print(self.pin,self.name,'get')
        return GPIO.input(self.pin)

class EventPin():
    def __init__(self,pin,function,rising=True,bouncetime=250,pud=GPIO.PUD_UP,name='',verbose=False):
        self.pin = pin
        self.name = name
        self.function = function
        self.rising = rising
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
        if self.rising:
            if self.verbose:
                print(self.pin,self.name,'set to input (off)')
            #GPIO.add_event_detect(self.pin,GPIO.FALLING,function,bouncetime=self.bouncetime) #opposite due to wiring
            GPIO.add_event_detect(self.pin,GPIO.FALLING,bouncetime=self.bouncetime)
        else:
            if self.verbose:
                print(self.pin,self.name,'set to input (up)')
            #GPIO.add_event_detect(self.pin,GPIO.RISING,function,bouncetime=self.bouncetime)
            GPIO.add_event_detect(self.pin,GPIO.RISING,bouncetime=self.bouncetime)
        GPIO.add_event_callback(self.pin,function)
    def get(self):
        if self.verbose:
            print(self.pin,self.name,'get')
        return GPIO.input(self.pin)

##def alert(channel):
##    print('alert on channel',channel)

class PWMPin():
# frequency determines
    def __init__(self, pin, freq=1023, dutycycle=100, name='', verbose=False):
        self.pin = pin
        self.name = name
        self.freq = freq
        self.dutycycle = dutycycle
        self.verbose = verbose
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.freq)
        self.pwm.start(self.dutycycle)
    def on(self):
        if self.verbose:
            print(self.pin,self.name,'on')
        self.pwm.start(self.dutycycle)
    def off(self):
        if self.verbose:
            print(self.pin,self.name,'off')
        self.pwm.stop()
    def setfreq(self, freq):
        if self.verbose:
            print(self.name,'setting frequency to',freq)
        self.freq = freq
        self.pwm.ChangeFrequency(self.freq)
    def setdutycycle(self, dutycycle):
        if self.verbose:
            print(self.name,'setting frequency to',dutycycle)
        self.dutycycle = dutycycle
        self.pwm.ChangeDutyCycle(self.dutycycle)
        
class OutPin():
    def __init__(self,pin,name='',verbose=False):
        self.pin = pin
        self.name = name
        self.verbose = verbose
        GPIO.setmode(GPIO.BOARD)
        if self.verbose:
            print(self.pin,self.name,'set to output')
        GPIO.setup(self.pin,GPIO.OUT)
    def on(self):
        if self.verbose:
            print(self.pin,self.name,'on')
        GPIO.output(self.pin,GPIO.HIGH)
    def off(self):
        if self.verbose:
            print(self.pin,self.name,'off')
        GPIO.output(self.pin,GPIO.LOW)
    def toggle(self):
        if self.verbose:
            print(self.pin,self.name,'toggled')
        GPIO.output(self.pin,~self.get)
    def get(self):
        if self.verbose:
            print(self.pin,self.name,'get')
        return GPIO.input(self.pin)

class Dataset():
    def __init__(self, data):
        self.data = data
    def add(self,data):
        for d in data:
            self.data.append(d)
    def append(self,data):
        self.data.append(data)
    def __add__(self,data):
        self.data.append(data)
    def __len__(self):
        return len(self.data)
    def avg(self):
        return sum(self.data)/len(self.data)
    def sd(self):
        avg = self.avg()
        va = []
        for d in self.data:
            va.append((d - avg) ** 2)
        var = 0
        for v in va:
            var += v
        var = var / len(va)
        return var ** (1/2)
    def __max__(self):
        return max(self.data)
    def __min__(self):
        return min(self.data)
    def removeoutliers(self):
        avg = self.avg()
        sd = self.sd()
        new = []
        for d in self.data:
            if abs(d-avg) < sd:
                new.append(d)
        return Dataset(new)

class UltrasonicSensor():
# pins should be:
# [trig,echo]
    def __init__(self, name, pins):
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
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['trig'], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.pins['echo'], GPIO.IN)
        Sleep(2)
    def measure(self, digits=4): # takes < 0.02 s to resolve
        GPIO.output(self.pins['trig'], GPIO.HIGH)
        Sleep(0.000015)
        GPIO.output(self.pins['trig'], GPIO.LOW)
        while not GPIO.input(self.pins['echo']):
            pass
        t1 = time.time()
        while GPIO.input(18):
            pass
        t2 = time.time()
        return round((t2-t1) * 340 / 2, digits)
    def multimeasure(self, interval=.1, totalmeasurements=0, totaltime=0, digits=4):
        tm = totaltime / interval
        tx = min(tm, totalmeasurements)
        o = Dataset([])
        while len(o) < tx:
            o.append(self.measure(digits))
            Sleep(interval)
        return o

class DCMotor():
#   OA |-\/-| GND
#  VCC |    | IB
#  VCC |    | IA
#   OB |----| GND
# VCC accepts 2.5 - 12 V
    def __init__(self, name, pins, on=True ,direction=1, speed=50, verbose=False):
        self.name = name
        self.verbose = verbose
        if self.verbose:
            print(self.name,'setting up')
        self.direction = direction
        self.speed = speed
        self.running = on
        if type(pins) is dict:
            self.pins = pins
        elif type(pins) is list:
            p = {}
            c = ['IA','IB']
            i = 0
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins['IA'], GPIO.OUT)
        GPIO.setup(self.pins['IB'], GPIO.OUT)
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm = PWMPin(self.pins['IA'],2000,self.speed)
    def start(self):
        if self.verbose:
            print(self.name,'starting up')
        self.running = True
        if self.direction:
            self.forward()
        else:
            self.backward()
    def stop(self):
        if self.verbose:
            print(self.name,'stopping')
        self.running = False
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.off()
    def power(self):
        if self.verbose:
            print(self.name,'toggling power')
        if self.running:
            self.stop()
        else:
            self.start()
    def forward(self):
        if self.verbose:
            print(self.name,'going forward')
        self.direction = 1
        GPIO.output(self.pins['IA'], GPIO.HIGH)
        GPIO.output(self.pins['IB'], GPIO.LOW)
        self.pwm.on()
    def backward(self):
        if self.verbose:
            print(self.name,'going backward')
        self.direction = 0
        GPIO.output(self.pins['IA'], GPIO.LOW)
        GPIO.output(self.pins['IB'], GPIO.HIGH)
        self.pwm.on()
    def reverse(self):
        if self.verbose:
            print(self.name,'toggling direction')
        if self.running:
            if self.direction:
                self.forward()
            else:
                self.backward()
        else:
            if self.direction:
                self.direction = 0
            else:
                self.direction = 1
    def setspeed(self,speed=50):
        if self.verbose:
            print(self.name,'setting speed to',speed)
        self.speed = speed
        if self.direction:
            self.pwm.setdutycycle(self.speed)
        else:
            self.pwm.setdutycycle(100 - self.speed)
        

class SegmentDisplay():
#
# g f X a b
# |-------|
# | aaa   |  X denotes ground
# |f   b  |  encoding:
# | ggg   |  00000000
# |e   c  |  hgfedcba
# | ddd h |  h = dc
# |-------|
# e d X c h
#
    def __init__(self,name,pins,verbose=False):
        self.name = name # name to refer to
        self.verbose = verbose # print each action
        if type(pins) is dict: # accepts dict, ex. {'a':11, 'b':15, ...}
            self.pins = pins
        elif type(pins) is list: # accepts ordered list, ex. [11, 15, ...}
            p = {}
            c = 'hgfedcba'
            i = 0
            for i in range(0,8):
                p[c[i]] = pins[i]
            self.pins = p
        GPIO.setmode(GPIO.BOARD) # refer to board by pin number
        for pin in self.pins.values(): # setup pins for output
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW) # initialize low = off
        #self.segs = {'a':0b00000001,'b':0b00000010,'c':0b00000100,
        #             'd':0b00001000,'e':0b00010000,'f':0b00100000,
        #             'g':0b01000000,'dc':0b10000000}
        self.trans = {'0':0b00011111,'1':0b00000110,'2':0b01011011,
                      '3':0b01001111,'4':0b01100110,'5':0b01101101,
                      '6':0b01111101,'7':0b00000111,'8':0b01111111,
                      '9':0b01100111,'a':0b01110111,'b':0b01111100,
                      'c':0b00111001,'d':0b01011110,'e':0b01111001,
                      'f':0b01110001,'.':0b10000000}
    def PATTERN(self,pat): # set outputs to bitstring pattern
        if self.verbose:
            print(self.name,'setting pattern',bin(pat))
        for i in range(len(pins)):
            GPIO.output(pins[i],pat & (1 << i))
    def WRITE(self,character): # display a character (valid characters in self.trans)
        if self.verbose:
            print(self.name,'writing',character)
        w = 0
        for c in character:
            w = w | self.trans(c)
        self.PATTERN(w)
    def SET(self,segment,signal=1): # set a specific segment to a specific signal
        if self.verbose:
            print(self.name,'setting segment',segment,'to',signal)
        GPIO.output(self.pins[segment],signal)
    def OFF(self): # set all segments to off
        if self.verbose:
            print(self.name,'turning all segments off')
        self.SET(0)

class MultiSegmentDisplay():
#
#        1  a  f  2  3  b
# |-----------------------------|
# |  aaa    aaa    aaa    aaa   |  
# | f   b  f   b  f   b  f   b  |  encoding:
# |  ggg    ggg    ggg    ggg   |  000000000000
# | e   c  e   c  e   c  e   c  |  hgfedcba4321
# |  ddd h  ddd h  ddd h  ddd h |  h = dc
# |-----------------------------|
#        e  d  h  c  g  4
#
# 220 Ohm resistor on 1, 2, 3, and 4
    def __init__(self,name,pins,digits=4,verbose=False):
        self.name = name # name to refer to
        self.verbose = verbose # print each action
        self.digits = digits
        self.cycle = 1
        self.cyclechars = ''
        if type(pins) is dict: # accepts dict, ex. {'a':11, 'b':15, ...}
            self.pins = pins
            # sort dict into list
            #self.pinsl = 
        elif type(pins) is list: # accepts ordered list, ex. [11, 15, ...}
            self.pinsl = pins
            p = {}
            c = 'hgfedcba4321'
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p
        GPIO.setmode(GPIO.BOARD) # refer to board by pin number
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH) # initialize high = off
        # nogood: k m v w x z
        self.trans = {'0':0b001111110000,'1':0b000001100000,'2':0b010110110000,
                      '3':0b010011110000,'4':0b011001100000,'5':0b011011010000,
                      '6':0b011111010000,'7':0b000001110000,'8':0b011111110000,
                      '9':0b011001110000,'a':0b011101110000,'b':0b011111000000,
                      'c':0b001110010000,'d':0b010111100000,'e':0b011110010000,
                      'f':0b011100010000,'g':0b011011110000,'h':0b011101000000,
                      'i':0b000100000000,'j':0b000011100000,'k':0b100010000000,
                      'l':0b001110000000,'m':0b100010000000,'n':0b010101000000,
                      'o':0b010111000000,'p':0b011100110000,'q':0b011001110000,
                      'r':0b010100000000,'s':0b011011010000,'t':0b011110000000,
                      'u':0b000111000000,'v':0b100010000000,'w':0b100010000000,
                      'x':0b100010000000,'y':0b011011100000,'z':0b100010000000,
                      '.':0b100000000000,'!':0b100001100000,'?':0b110100110000,
                      ' ':0b000000000000}
        self.digits = {1:0b1110,2:0b1101,3:0b1011,4:0b0111,
                       '1':0b1110,'2':0b1101,'3':0b1011,'4':0b0111}
    def PATTERN(self,pat): # set outputs to bitstring pattern
        if self.verbose:
            print(self.name,'setting pattern',bin(pat))
        for i in range(len(self.pins)):
            if self.verbose:
                print('','sending',pat & (1 << (11-i)),'to',self.pinsl[i])
            GPIO.output(self.pinsl[i],pat & (1 << (11-i)))
    def WRITE(self,character,digit): # display a character (valid characters in self.trans)
        if self.verbose:
            print(self.name,'writing',character,'to digit',digit)
        cw = 0
        for c in character:
            cw = cw | self.trans[c] # add up character bitstrings
        dw = 0
        #for d in digit:
        #    dw = dw | self.digits[d] # add up digit bitstrings
        dw = self.digits[digit]
        w = cw | dw # combine into single bitstring
        self.PATTERN(w)
    def SET(self,segment,digit,signal=1): # set a specific segment to a specific signal
        if self.verbose:
            print(self.name,'setting segment',segment,'on digit',digit,'to',signal)
        GPIO.output(self.pins[digit],signal)
        GPIO.output(self.pins[segment],signal)
    def OFF(self): # set all segments to off
        if self.verbose:
            print(self.name,'turning all segments off')
        self.PATTERN(0b111111111111)
    def DISPLAY(self,chars,duration=1,delay=.005):
        chars = chars.lower()
        elapsed = 0
        while elapsed < duration:
            self.WRITE(chars[0],4)
            Sleep(delay)
            self.WRITE(chars[1],3)
            Sleep(delay)
            self.WRITE(chars[2],2)
            Sleep(delay)
            self.WRITE(chars[3],1)
            Sleep(delay)
            elapsed += 4 * delay
        self.OFF()
    def SETCYCLE(self,chars): # sets the pattern for display cycling
        if self.verbose:
            print(self.name,'setting cycle pattern to',chars)
        self.cyclechars = chars.lower()
    def CYCLE(self): # for looping use while running other code
        # call 4 times in a loop with Sleep(.005) after each call
##        while True:
##            SEG.CYCLE()
##            Sleep(.005)
##            SEG.CYCLE()
##            Sleep(.005)
##            SEG.CYCLE()
##            Sleep(.005)
##            SEG.CYCLE()
##            Sleep(.005)
##            YourOtherFunctions()
##        # end while
        if self.verbose:
            print(self.name,'displaying',self.cyclechars,'on cycle',cycle)
        self.WRITE(self.cyclechars[self.cycle - 1],5 - self.cycle)
        if self.cycle < 4:
            self.cycle += 1
        else:
            self.cycle = 1
    def DEMO(self):
        d = '    0123456789.?!abcdefghijklmnopqrstuvwxyz    '
        for i in range(4,len(d)):
            self.DISPLAY(d[i-3]+d[i-2]+d[i-1]+d[i],.3)

class Adafruit_CharLCD:
# based on code from lrvick and LiquidCrystal
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
# modified by mirrorcoloured
# 16 characters, 2 lines
    # commands
    LCD_CLEARDISPLAY 		= 0x01
    LCD_RETURNHOME 		= 0x02
    LCD_ENTRYMODESET 		= 0x04
    LCD_DISPLAYCONTROL 		= 0x08
    LCD_CURSORSHIFT 		= 0x10
    LCD_FUNCTIONSET 		= 0x20
    LCD_SETCGRAMADDR 		= 0x40
    LCD_SETDDRAMADDR 		= 0x80
    # flags for display entry mode
    LCD_ENTRYRIGHT 		= 0x00
    LCD_ENTRYLEFT 		= 0x02
    LCD_ENTRYSHIFTINCREMENT 	= 0x01
    LCD_ENTRYSHIFTDECREMENT 	= 0x00
    # flags for display on/off control
    LCD_DISPLAYON 		= 0x04
    LCD_DISPLAYOFF 		= 0x00
    LCD_CURSORON 		= 0x02
    LCD_CURSOROFF 		= 0x00
    LCD_BLINKON 		= 0x01
    LCD_BLINKOFF 		= 0x00
    # flags for display/cursor shift
    LCD_DISPLAYMOVE 		= 0x08
    LCD_CURSORMOVE 		= 0x00
    # flags for display/cursor shift
    LCD_DISPLAYMOVE 		= 0x08
    LCD_CURSORMOVE 		= 0x00
    LCD_MOVERIGHT 		= 0x04
    LCD_MOVELEFT 		= 0x00
    # flags for function set
    LCD_8BITMODE 		= 0x10
    LCD_4BITMODE 		= 0x00
    LCD_2LINE 			= 0x08
    LCD_1LINE 			= 0x00
    LCD_5x10DOTS 		= 0x04
    LCD_5x8DOTS 		= 0x00
# board [VSS, VDD, V0, RS, RW, E, D0, D1, D2, D3, D4, D5, D6, D7, A, K]
# power [ 0V,  5V, Pot,  , 0V,  ,   ,   ,   ,   ,   ,   ,   ,   ,5V,0V]
# pins  [   ,    ,    ,rs,   , e, d0, d1, d2, d3, d4, d5, d6, d7,  ,  ]
    def __init__(self, pins, GPIO = None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.GPIO.setwarnings(False)
        self.GPIO.setmode(GPIO.BOARD)

        if type(pins) is dict: # accepts dict, ex. {'a':11, 'b':15, ...}
            self.pins = pins
        elif type(pins) is list: # accepts ordered list, ex. [11, 15, ...}
            p = {}
            c = ['rs','e','d0','d1','d2','d3','d4','d5','d6','d7']
            for i in range(0,len(c)):
                p[c[i]] = pins[i]
            self.pins = p

        for pin in list(self.pins.values()):
            if pin != 0:
                self.GPIO.setup(pin, GPIO.OUT)

        self.pin_rs = self.pins['rs']
        self.pin_e = self.pins['e']
        self.pins_db = [self.pins['d4'],
                        self.pins['d5'],
                        self.pins['d6'],
                        self.pins['d7'],]

        self.write4bits(0x33) # initialization
        self.write4bits(0x32) # initialization
        self.write4bits(0x28) # 2 line 5x7 matrix
        self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06) # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        #""" Initialize to default text direction (for romance languages) """
        self.displaymode =  self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode) #  set the entry mode

        self.begin(16,2)
        
        self.clear()
    def begin(self, cols, lines):
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE
            self.currline = 0
    def home(self):
        self.write4bits(self.LCD_RETURNHOME) # set cursor position to zero
        self.delayMicroseconds(3000) # this command takes a long time!
    def clear(self):
        self.write4bits(self.LCD_CLEARDISPLAY) # command to clear display
        self.delayMicroseconds(3000)	# 3000 microsecond sleep, clearing the display takes a long time
    def setCursor(self, col, row):
        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]
        row -= 1
        if ( row > self.numlines ): 
            row = self.numlines - 1 # we count rows starting w/0
        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))
    def displayOff(self): 
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def displayOn(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def display(self):
        """ Toggles the display (quickly) """
        self.displaycontrol ^= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def cursorOff(self):
        """ Turns the underline cursor off """
        print('off',self.displaycontrol)
        self.displaycontrol &= ~self.LCD_CURSORON
        print(self.displaycontrol)
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def cursorOn(self):
        """ Turns the underline cursor on """
        print('on',self.displaycontrol)
        self.displaycontrol |= self.LCD_CURSORON
        print(self.displaycontrol)
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def cursor(self):
        """ Toggles the underline cursor """
        self.displaycontrol ^= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def blinkOff(self): # not working? does alignment or something
        """ Turn on and off the blinking cursor """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def blinkOn(self): # not working? does alignment or something
        """ Turn on and off the blinking cursor """
        self.displaycontrol |= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)
    def scrollLeft(self,n=1):
        """ These commands scroll the display without changing the RAM """
        while n > 0:
            self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)
            n -= 1
    def scrollRight(self, n=1):
        """ These commands scroll the display without changing the RAM """
        while n > 0:
            self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT);
            n -= 1
    def leftToRight(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode);
    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)
    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)
    def noAutoscroll(self): 
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)
    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        self.delayMicroseconds(1000) # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)
        self.pulseEnable()
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4,8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)
        self.pulseEnable()
    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)	# divide microseconds by 1 million for seconds
        Sleep(seconds)
    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(1)		# 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(1)		# commands need > 37us to settle
    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0) # next line
            else:
                self.write4bits(ord(char),True)

# not working properly, problem inheriting class
##class PWMPin(GPIO.PWM):
##    def __init__(self,pin,name='',freq=1023,spd=1,rising=True,verbose=False):
##        self.name = name
##        self.pin = pin
##        self.freq = freq
##        self.dc = 0
##        self.verbose = verbose
##        GPIO.setmode(GPIO.BOARD)
##        GPIO.setup(self.pin,GPIO.OUT)
##        self = GPIO.PWM(self.pin,self.freq)
##        self.start(0)
##        if self.verbose:
##            print(self.pin,self.name,'set to PWM output')
##    def ON(self):
##        if self.verbose:
##            print(self.pin,self.name,'on')
##        GPIO.output(self.pin,GPIO.HIGH)
##    def OFF(self):
##        if self.verbose:
##            print(self.pin,self.name,'off')
##        GPIO.output(self.pin,GPIO.LOW)
##    def GET(self):
##        if self.verbose:
##            print(self.pin,self.name,'get')
##        return GPIO.input(self.pin)
##    def CYCLE(self):
##        if self.verbose:
##            print(self.pin,self.name,'incrementing duty cycle from',self.dc,'by',self.spd)
##        if rising and self.dc + self.spd <= 100:
##            self.dc += self.spd
##            self.ChangeDutyCycle(self.dc)
##        elif rising and self.dc + self.spd > 100:
##            rising = False
##
##        elif not rising and self.dc - self.spd >= 0:
##            self.dc -= self.spd
##            self.ChangeDutyCycle(self.dc)
##        elif not rising and self.dc - self.spd < 0:
##            rising = True

def OnPin(PinNum,verbose=False):
    GPIO.output(PinNum, GPIO.HIGH)      # Set to high (+3.3 V)
    if verbose:
        print('Pin',PinNum,'set to 3.3 V')
    # GPIO.HIGH = True = 1

def OffPin(PinNum,verbose=False):
    GPIO.output(PinNum, GPIO.LOW)       # Set to low (0 V)
    if verbose:
        print('Pin',PinNum,'set to 0 V')
    # GPIO.Low = False = 0

def GetPin(PinNum,verbose=False):
    if verbose:
        print('Getting pin',PinNum)
    print(GPIO.input(PinNum))

def SetupPin(PinNum,PinType,verbose=False):
    GPIO.setmode(GPIO.BOARD)            # Identifies pin by physical location
    #GPIO.setmode(GPIO.BCM)             # Identifies pin by Broadcom channel
    if PinType == 'OUT':
        GPIO.setup(PinNum, GPIO.OUT)    # Set pin mode to output
        if verbose:
            print('Initialized',PinNum,'for output')
    elif PinType == 'IN':
        GPIO.setup(PinNum, GPIO.IN)     # Set pin mode to input
        if verbose:
            print('Initialized',PinNum,'for input')
    OnPin(PinNum,False)

def Cleanup():
    GPIO.cleanup()

def PinOut(PinNum,verbose=False):
    if verbose:
        print('Setting pin',PinNum,'to output')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinNum,GPIO.OUT)

def PinIn(PinNum,verbose=False):
    if verbose:
        print('Setting pin',PinNum,'to input (off)')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinNum,GPIO.IN,GPIO.PUD_OFF)

def PinInUp(PinNum,verbose=False):
    if verbose:
        print('Setting pin',PinNum,'to input (up)')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinNum,GPIO.IN,GPIO.PUD_UP)

def PinInDown(PinNum,verbose=False):
    if verbose:
        print('Setting pin',PinNum,'to input (down)')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PinNum,GPIO.IN,GPIO.PUD_DOWN)
    
### TWITTER ###

def Tweet(twit,statustext):
    twit.update_status(status=statustext)

def TweetPicture(twit,file,statustext):
    photo = open(file, 'rb')
    response = twitter.upload_media(media=photo)
    twit.update_status(status=statustext, media_ids=[response['media_id']])

def TweetVideo(twit,file,statustext):
    video = open(file, 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twit.update_status(status=statustext, media_ids=[response['media_id']])
