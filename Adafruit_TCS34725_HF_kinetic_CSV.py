#!/usr/bin/python
import time
import csv
from Adafruit_TCS34725mod import TCS34725


# parameters adjusted for the HF colorimeter by HF
# in adafruit_IC2.py adress was fixed  for newer Pis
# Optimized for serial measurements 

# ===========================================================================
# Example Code
# ===========================================================================

# Initialize the TCS34725 and use default integration time and gain
# tcs34725 = TCS34725(debug=True)
# tcs = TCS34725(integrationTime=0xEB, gain=0x01) # original settings

tcs = TCS34725(integrationTime=0xC0, gain=0x00) # optimized settings: OxC0 = 64 cycles, 0x00 = no gain
tcs.setInterrupt(False)
time.sleep(1)

counter_m = 0
Meas_Circles = 1 # at least one measurement

ID_probe = raw_input("Please enter name of sample and CSV-file: ") #only standard signs allowed
Meas_Circles = input("Please enter number of measurements: ")
Meas_Length = input ("Please enter time between measurements in seconds: ")
print 
print "The measurement procedure will take about ", (Meas_Circles *Meas_Length), " seconds."
print
print
print 'Sample ID: ', ID_probe
file_name = '.'.join((str(ID_probe),'csv'))
print file_name
print "# red green blue wday month day time year" #header printed to shell

with open(file_name, 'wb') as csvfile:
    header = ['nr','red','green','blue','|time|']
    name_writer = csv.writer(csvfile, delimiter ='_')
    name_writer.writerow(file_name) # first row in file - indicates file name
    header_writer = csv.writer(csvfile, delimiter =' ')
    header_writer.writerow(header)          # second row in file - structures data, with a blank in between items
   
while (counter_m < Meas_Circles): 

        meas_time = time.asctime() # get timestamp
        rgb = tcs.getRawData()     # read data as dictionary
        rot = rgb["r"]             # extract individual values from dictionary: red, green, blue; not elegant but working
        gruen = rgb["g"]
        blau = rgb["b"]
        print counter_m, " ",rot," ",gruen," ",blau," ", meas_time # print data to shell

        data_set = [repr(counter_m),repr(rot),repr(gruen), repr(blau), str(meas_time)] # data to be writen to csv-file
        # print data_set

        with open(file_name, 'a') as csvfile: #a : append, not overwriting
         valuewriter = csv.writer(csvfile, delimiter =' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
         valuewriter.writerow(data_set)       # writes data to file
        
        tcs.setInterrupt(True)
        counter_m += 1
        time.sleep (Meas_Length)     # duration of measurement step: approx. n+1 seconds

print "End of measurement"
    

tcs.disable()
