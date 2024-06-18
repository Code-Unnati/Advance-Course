from mq135_interface import *
import sys, time

#filename = "mq_sensors_log.csv"

# Create header row in new CSV file
#csv = open(filename, 'w')
#csv.write("Timestamp,Raw_value_MQ135, \n")
#csv.close

#mq135 = MQ135()
#now_time = time.time()
    
while True:

    mq135 = MQ135()
    now_time = time.time()
    
    perc135 = mq135.MQPercentage()

    print("MQ135 measurment")
    sys.stdout.write("\r")
    sys.stdout.write("\033[K")
    sys.stdout.write("Raw_value:   %g, \nACETON:      %g ppm, \nTOLUENO:     %g ppm, \nALCOHOL:     %g ppm, \nCO2:         %g ppm, \nNH4:         %g ppm, \nCO:          %g ppm" % (perc135["RAW_VALUE"], perc135["ACETON"], perc135["TOLUENO"], perc135["ALCOHOL"], perc135["CO2"], perc135["NH4"], perc135["CO"]))
    sys.stdout.flush()
    print("\n\n")
        
        # Write values to csv file
    entry = str(round((time.time() - now_time) / 60))
    entry = entry + "," + str(perc135["RAW_VALUE"]) + "\n"

    # Log (append) entry into file
#    csv = open(filename, 'a')
#    try:
#        csv.write(entry)
#    finally:
#        csv.close()
               
    time.sleep(2)
    
            