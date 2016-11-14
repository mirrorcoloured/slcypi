from slcyRobotics import *

if __name__ == '__main__':
    try:
        t = UltraServo([33,35,37],'US',True)
        
        while False:
            pass
##            serv.move(-1)
##            print(sens.measure())
##            Sleep(1)
##            serv.move(1)
##            print(sens.measure())
##            Sleep(1)
##            serv.center()
##            print(sens.measure())
##            Sleep(1)
    except KeyboardInterrupt:
        print('Interrupt detected: exiting loop')
        Cleanup()
