from slcyUltrasonic import *

if __name__ == "__main__":

    pins = {'trig':38,'echo':40} # replace 38 and 40 with your GPIO pins (BOARD setup)
    SEN = UltrasonicSensor(pins,'mySensor',True) # set verbose=False to make it shut up

    test = SEN.measure() # takes a single measurement

    dat = SEN.multimeasure(interval=0.1,totaltime=1) # takes a measurement every 0.1 s for 5 s

    print('Average measurement:', dat.avg())
    print('Measurement standard deviation:', dat.sd())

    file = 'testdata.txt' # write data to a file
    timestamp = str(datetime.datetime.utcnow())
    with open(file,'w') as f:
        f.write(timestamp)
        f.write(dat.tostring())
