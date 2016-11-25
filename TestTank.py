import sys
from time import sleep

sys.path.append("/home/pi/Documents/Robots/slcypi/MA") ### ADD PATH
sys.path.append("/home/pi/Documents/Robots/slcypi/HAT_Python3") ### ADD PATH


#from MA.Tank import Tank
from Tank import Tank

myRobot = Tank()

myRobot.drive(1,50)
sleep(1)
myRobot.stop()
