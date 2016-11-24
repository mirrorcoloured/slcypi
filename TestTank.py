from time import sleep

import MA.Tank as tank

myRobot = tank.Tank()

myRobot.drive(1,50)
time.sleep(1)
myRobot.stop()
