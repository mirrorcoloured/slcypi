import sys
from time import sleep

sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH


#from MA.Tank import Tank
import Tank

myRobot = tank.Tank()

myRobot.drive(1,50)
time.sleep(1)
myRobot.stop()
