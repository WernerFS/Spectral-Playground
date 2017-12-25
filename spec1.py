import time
import csv
import RPi.GPIO as GPIO
from Adafruit_TCS34725mod import TCS34725



############## Led configuration Start #############################################
def setup(self):
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(11, GPIO.OUT)   # Set LedPin's mode is output

def destroy(self):
    GPIO.cleanup()                  # Release resource
############## Led configuration End ###############################################


tcs = TCS34725(integrationTime=0xC0, gain=0x00) # optimized settings: OxC0 = 64 cycles, 0x00 = no gain
tcs.setInterrupt(False)
time.sleep(1)
setup()

Meas_Circles = 1 # at least one measurement

ID_probe = raw_input("Please enter name of sample and CSV-file: ") #only standard signs allowed
Meas_Circles = input("Please enter number of measurements: ")

print 'Sample ID: ', ID_probe
file_name = '.'.join((str(ID_probe),'csv'))
print file_name
print "# clear red green blue  wday month day time year" #header printed to shell

with open(file_name, 'wb') as csvfile:
    header = ['nr','clear','red','green','blue','|time|']
    name_writer = csv.writer(csvfile, delimiter =' ')
    name_writer.writerow(file_name) # first row in file - indicates file name
    header_writer = csv.writer(csvfile, delimiter =',')
    header_writer.writerow(header)          # second row in file - structures data, with a blank in between items
    valuewriter = csv.writer(csvfile, delimiter =',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(Meas_Circles):
        op = raw_input("You ready to measure?  ")
        if op == 'y' or op == 'Y':
            print "Taking sample #", i
            meas_time = time.asctime() # get timestamp
            GPIO.output(LedPin, GPIO.HIGH)  # led on
            rgbc = tcs.getRawData()     # read data as dictionary
            for k,v in rgbc.iteritems():
                print k, v, " ",
                # print data_set
            print meas_time
            GPIO.output(LedPin, GPIO.LOW) # led off
            data_set = [repr(i), repr(rgbc["c"]), repr(rgbc["r"]), repr(rgbc["g"]), repr(rgbc["b"]), str(meas_time)]
            print "Writting to file"
            valuewriter.writerow(data_set)       # writes data to file

print "End of measurement"
destroy()
tcs.disable()
