import time
import math
import busio
import digitalio
import board
#import adafruit_mcp3xxx.mcp3008 as MCP
#from adafruit_mcp3xxx.analog_in import AnalogIn

from dfadc import *

board_detect()    # If you forget address you had set, use this to detected them, must have class instance


while board.begin() != board.STA_OK:    # Board begin and check board status
    print_board_status()
    print("board begin faild")
    time.sleep(2)
print("board begin success")

board.set_adc_enable()


class MQ135():

    ######################### Hardware Related Macros #########################
    RL_VALUE                     = 10       # define the load resistance on the board, in kilo ohms
    RO_CLEAN_AIR_FACTOR          = 3.6      # RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                            # which is derived from the chart in datasheet
 
    ######################### Software Related Macros #########################
    CALIBRATION_SAMPLE_TIMES     = 50       # define how many samples you are going to take in the calibration phase
    CALIBRATION_SAMPLE_INTERVAL  = 50       # define the time interval(in milisecond) between each samples in the
                                            # cablibration phase
    READ_SAMPLE_INTERVAL         = 50       # define the time interval(in milisecond) between each samples in
    READ_SAMPLE_TIMES            = 5        # define how many samples you are going to take in normal operation 
                                            # normal operation
 
    ######################### Application Related Macros ######################
    GAS_ACETON                   = 0
    GAS_TOLUENO                  = 1
    GAS_ALCOHOL                  = 2
    GAS_CO2                      = 3
    GAS_NH4                      = 4
    GAS_CO                       = 5

    def __init__(self, Ro=10):
        self.Ro = Ro        
        # create the spi bus
        #spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

        # create the cs (chip select)
        #cs = digitalio.DigitalInOut(board.D8)

        # create the mcp object
        #mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 3 for MQ135
        #self.chan_MQ135 = AnalogIn(mcp, MCP.P3)
        self.chan_MQ135_value = board.get_adc_value(board.A0)#/4
        
        self.ACETONCurve = [1.0,0.18,-0.32] # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent"
                                            # to the original curve. 
                                            # data format:{ x, y, slope}; point1: (lg10, 0.18), point2: (lg200, -0.24) 
        self.TOLUENOCurve = [1.0,0.2,-0.30] # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg10, 0.2), point2: (lg200, -0.19)
        self.AlcoholCurve =[1.0,0.28,-0.32] # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg10, 0.28), point2: (lg200, -0.14)
        self.CO2Curve =[1.0,0.38,-0.37]       # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg10, 0.38), point2: (lg200, -0.10)
        self.NH4Curve =[1.0,0.42,-0.42]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg10, 0.42), point2: (lg200, -0.12)
        self.COCurve =[1.0,0.45,-0.26]     # two points are taken from the curve. 
                                            # with these two points, a line is formed which is "approximately equivalent" 
                                            # to the original curve.
                                            # data format:[ x, y, slope]; point1: (lg10, 0.45), point2: (lg200,  0.11)
                
        print("Calibrating MQ-135...")
        self.Ro = self.MQ135_Calibration()
        print("Calibration of MQ-135 is done...")
        print("MQ-135 Ro=%f kohm" % self.Ro)
        print("\n")
    
    ######################### MQCalibration ####################################
    # Input:   mq_pin - analog channel
    # Output:  Ro of the sensor
    # Remarks: This function assumes that the sensor is in clean air. It use  
    #          MQResistanceCalculation to calculates the sensor resistance in clean air 
    #          and then divides it with RO_CLEAN_AIR_FACTOR. RO_CLEAN_AIR_FACTOR is about 
    #          3.6, which differs slightly between different sensors.
    ############################################################################ 
    def MQ135_Calibration(self):
        val = 0.0
        for i in range(self.CALIBRATION_SAMPLE_TIMES):          # take multiple samples
            val += self.MQResistanceCalculation(self.chan_MQ135_value)
            time.sleep(self.CALIBRATION_SAMPLE_INTERVAL/1000.0)
            
        val = val/self.CALIBRATION_SAMPLE_TIMES                 # calculate the average value
        val = val/self.RO_CLEAN_AIR_FACTOR                      # divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                                # according to the chart in the datasheet 
        return val
        
    ######################### MQResistanceCalculation #########################
    # Input:   raw_adc - raw value read from adc, which represents the voltage
    # Output:  the calculated sensor resistance
    # Remarks: The sensor and the load resistor forms a voltage divider. Given the voltage
    #          across the load resistor and its resistance, the resistance of the sensor
    #          could be derived.
    ############################################################################ 
    def MQResistanceCalculation(self, raw_adc):
        #print(raw_adc)
        # 1023 for 3008()
        # https://github.com/tutRPi/Raspberry-Pi-Gas-Sensor-MQ
        
        # 65472 for circuit python
        # Even though the MCP3008 is a 10-bit ADC, the value returned is a 16-bit number to provide a consistent interface across ADCs in CircuitPython
        # https://github.com/adafruit/Adafruit_CircuitPython_MCP3xxx/blob/main/adafruit_mcp3xxx/analog_in.py#L50-L54
        
        if raw_adc == 0:
            raw_adc = 1
            
        return float(self.RL_VALUE * (65472.0-raw_adc) / float(raw_adc))    
      
    #########################  MQRead ##########################################
    # Input:   mq_pin - analog channel
    # Output:  Rs of the sensor
    # Remarks: This function use MQResistanceCalculation to caculate the sensor resistenc (Rs).
    #          The Rs changes as the sensor is in the different consentration of the target
    #          gas. The sample times and the time interval between samples could be configured
    #          by changing the definition of the macros.
    ############################################################################ 
    def MQRead(self):
        rs = 0.0
        raw_value = 0.0
        for i in range(self.READ_SAMPLE_TIMES):
            raw_value += self.chan_MQ135_value
            rs += self.MQResistanceCalculation(self.chan_MQ135_value)
            time.sleep(self.READ_SAMPLE_INTERVAL/1000.0)

        rs = rs / self.READ_SAMPLE_TIMES
        raw_value = raw_value / self.READ_SAMPLE_TIMES

        return rs, raw_value
    
    def MQPercentage(self):
        val = {}
        read, raw_value = self.MQRead()
        val["ACETON"]   = self.MQGetGasPercentage(read/self.Ro, self.GAS_ACETON)
        val["TOLUENO"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_TOLUENO)
        val["ALCOHOL"]  = self.MQGetGasPercentage(read/self.Ro, self.GAS_ALCOHOL)
        val["CO2"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO2)
        val["NH4"]      = self.MQGetGasPercentage(read/self.Ro, self.GAS_NH4)
        val["CO"]       = self.MQGetGasPercentage(read/self.Ro, self.GAS_CO)
        val["RAW_VALUE"]= raw_value
        return val
     
    #########################  MQGetGasPercentage ##############################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          gas_id      - target gas type
    # Output:  ppm of the target gas
    # Remarks: This function passes different curves to the MQGetPercentage function which 
    #          calculates the ppm (parts per million) of the target gas.
    ############################################################################ 
    def MQGetGasPercentage(self, rs_ro_ratio, gas_id):
        if ( gas_id == self.GAS_ACETON ):
            return self.MQGetPercentage(rs_ro_ratio, self.ACETONCurve)
        elif ( gas_id == self.GAS_TOLUENO ):
            return self.MQGetPercentage(rs_ro_ratio, self.TOLUENOCurve)
        elif ( gas_id == self.GAS_ALCOHOL ):
            return self.MQGetPercentage(rs_ro_ratio, self.AlcoholCurve)
        elif ( gas_id == self.GAS_CO2 ):
            return self.MQGetPercentage(rs_ro_ratio, self.CO2Curve)
        elif ( gas_id == self.GAS_NH4 ):
            return self.MQGetPercentage(rs_ro_ratio, self.NH4Curve)
        elif ( gas_id == self.GAS_CO ):
            return self.MQGetPercentage(rs_ro_ratio, self.COCurve)
        return 0
     
    #########################  MQGetPercentage #################################
    # Input:   rs_ro_ratio - Rs divided by Ro
    #          pcurve      - pointer to the curve of the target gas
    # Output:  ppm of the target gas
    # Remarks: By using the slope and a point of the line. The x(logarithmic value of ppm) 
    #          of the line could be derived if y(rs_ro_ratio) is provided. As it is a 
    #          logarithmic coordinate, power of 10 is used to convert the result to non-logarithmic 
    #          value.
    ############################################################################ 
    def MQGetPercentage(self, rs_ro_ratio, pcurve):
        #print(rs_ro_ratio)
        #print((math.log(rs_ro_ratio)-pcurve[1]))
        #print(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0]))
        
        # This is the natural natural logarithm -> log(rs_ro_ratio)
        return (math.pow(10,(((math.log(rs_ro_ratio)-pcurve[1])/ pcurve[2]) + pcurve[0])))
        
        
    