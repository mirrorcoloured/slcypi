#import RPi.GPIO as GPIO
from twython import Twython
import time
import sys
import os
import pygame

APP_KEY='zmmlyAJzMDIntLpDYmSH98gbw'
APP_SECRET='ksfSVa2hxvTQKYy4UR9tjpb57CAynMJDsygz9qOyzlH24NVwpW'
OAUTH_TOKEN='794094183841566720-BagrHW91yH8C3Mdh9SOlBfpL6wrSVRW'
OAUTH_TOKEN_SECRET='d0Uucq2dkSHrFHZGLM1X8Hw05d80ajKYGl1zTRxZQSKTm'
applepislcy = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### GENERAL ###

def Cleanup():
    GPIO.cleanup()

def Sleep(seconds) -> None:
    """Puts the program to sleep"""
    time.sleep(seconds)

def Alert(channel) -> None:
    """Simple alert function for testing event interrupts"""
    print('Alert on channel',channel)

def LoadPins(mapping,inp) -> dict:
    """Organizes an input into a pin mapping dict
    mapping <list>, ['IA','IB']
    inp <dict>, <list>, <int> {'IA':1,'IB':2}, [1,2]
    """
    if type(inp) is int and len(mapping) == 1:
        return {mapping[0]:inp}
    elif type(inp) is list and len(mapping) == len(inp):
        o = {}
        for i in range(inp):
            o[mapping[i]] = inp[i]
        return o
    elif type(inp) is dict:
        return inp
    else:
        print('Invalid input for pins:',inp,type(inp))
        print('Expected:',mapping)
        return {}

### PYGAME ###

def WindowSetup(size=(300,50),caption='',text='',background=(0,0,0),foreground=(255,255,255)):
    """Sets up a pygame window to take keyboard input
    size <tuple>, width by height
    caption <str>, window title bar
    text <str>, text to display in window, accepts \n
    background <tuple>, foreground <tuple>, (r,g,b) color
    """
    pygame.init()
    screen = pygame.display.set_mode(size,0,32)
    pygame.display.set_caption(caption)
    myfont = pygame.font.SysFont('Monospace',15)
    labels = []
    lines = text.split('\n')
    for line in lines:
        labels.append(myfont.render(line,1,foreground))
    screen.fill(background)
    y = 0
    for label in labels:
        screen.blit(label, (0,y))
        y += 15
    pygame.display.update()

def InputLoop(eventmap):
    """Begins a pygame loop, mapping key inputs to functions
    eventmap <dict>, {pygame.K_t:myfunction}
    """
    index = 0
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                #print("{0}: You pressed {1:c}".format ( index , event.key ))
                if event.key in eventmap:
                    eventmap[event.key]()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def InputLoopDemo():
    def dog():
        print('woof')
    def cat():
        print('meow')
    def fish():
        print('blub')
    WindowSetup(caption='pet simulator',text='d for dog\nc for cat\nf for fish')
    InputLoop({pygame.K_d:dog, pygame.K_c:cat, pygame.K_f:fish})

### TWITTER ###

def Tweet(twit,statustext) -> None:
    """Tweets a message
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    statustext <str>, must be <= 140 characters
    """
    if len(statustext) > 140:
        print('ERROR: Character limit 140 exceeded:',len(statustext))
    else:
        twit.update_status(status=statustext)

def TweetPicture(twit,file,statustext) -> None:
    """Tweets a message with a picture
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    file <str>, path and filename to picture
    statustext <str>, must be <= 140 characters
    """
    photo = open(file, 'rb')
    response = twitter.upload_media(media=photo)
    twit.update_status(status=statustext, media_ids=[response['media_id']])

def TweetVideo(twit,file,statustext) -> None:
    """Tweets a message with a video
    twit <Twython>, create with Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    file <str>, path and filename to video
    statustext <str>, must be <= 140 characters
    """
    video = open(file, 'rb')
    response = twitter.upload_video(media=video, media_type='video/mp4')
    twit.update_status(status=statustext, media_ids=[response['media_id']])
