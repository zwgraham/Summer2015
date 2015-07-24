#! /usr/bin/env python2.7
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
from time import sleep
"""
normalizeData takes in analog readings of the  current(adc-4) and the volatage(adc-0).
It also takes in the sensorAddr(source_addr) simply to keep track where is the data comming from

@voltage:  a list of 19 analog readings [672, 801, 864, 860, 755, 607, 419, 242, 143, 108, 143, 253, 433, 623, 760, 848, 871, 811]
@current:  a list of 19 analog readings [492, 492, 510, 491, 492, 491, 491, 491, 492, 480, 492, 492, 492, 492, 492, 492, 497, 492]
"""
__authors__ = ["Miguel Flores Silverio (miguelflores6182@stuent.hartnell.edu)"]
__author__ = ', '.join(__authors__)
__copyright__ = """Copyright © 2015 The Regents of the University of California
All Rights Reserved"""
__credits__ = ["Zachary Graham", "Kapil Sinha", "Miguel Flores Silverio", "Andres Aranda"]
__status__ = "prototype"
__license__ = """Copyright © 2015, The Regents of the University of California
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
     * Neither the name of Center for Sustainable Energy and Power Systems nor
       the names of its contributors may be used to endorse or promote products
       derived from this software without specific prior written permission.
     THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
     AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
     IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
     DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
     FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
     DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
     SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
     CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
     OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
     OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."""
def graphit(voltage,current,sensorAddr):
    plt.ion()
    fig,ax1 = plt.subplots()
    ax2 = plt.twinx()
    print
    print "----Voltage----"
    print "min:",min(voltage)
    print "max:",max(voltage)
    print "----Current----"
    print "min:",min(current)
    print "max:",max(current)
    ax1.plot(voltage,'r')
    ax1.set_xlabel("Sample #")
    ax1.set_ylabel("Voltage")
    ax2.plot(current,'b')
    ax2.set_ylabel("Current")
    ax2.set_ylim(-1.2,1.2)
    plt.draw()

def getAnalogData(reading):
    reading = eval(reading)
    assert(type(reading) == dict)
    adc0 = []
    adc4 = []
    sensorAddr = reading['source_addr'].encode('hex')
    for sample in reading['samples']:
        adc0.append(sample['adc-0'])
        adc4.append(sample['adc-4'])

    return adc0,adc4,sensorAddr
def normalizeData(voltage,current):
    # Normalize the curve to zero
    # From and more at Adafruit design https://learn.adafruit.com/tweet-a-watt/design-listen
    MAINSVPP = 164 * 2 # +-164V
    VREF = 498         # Hardcoded 'DC bias' value its about 492
    CURRENTNORM = 16.0 # Normalizing constant that converts the analog reading to Amperes
    min_v = 1024       # XBee ADC is 10 bits, so max value is 1023
    max_v = 0
    # Find the smallest voltage and the biggest voltage in the list of samples taken
    for v in voltage:
        if(min_v > v):
            min_v = v
        if(max_v < v):
            max_v = v
    # Average of the biggest  and smallest voltage samples
    avg_voltage = (min_v + max_v) / 2
    # Calculate  the peak to peak measurement
    vpp = max_v - min_v
    for index in range(len(voltage)):
        # Remove 'dc-bias', which is the average reading
        voltage[index] -= avg_voltage
        voltage[index] = (voltage[index] * MAINSVPP) / vpp
    # Normalize current reading to amperes
    for index in range(len(current)):
        current[index] -= VREF
        current[index] /= CURRENTNORM
    return voltage,current
def main():
    #filepath = raw_input("Enter name of data file or path where it is located: ")
    data = open("/home/chronos/data_files/typicalLoadTest/typicalLoadTest.txt")
    for line in data:
        adc0, adc4, sensor = getAnalogData(line)
        volatage, current = normalizeData(adc0,adc4)
        sleep(5)
        graphit(volatage,current,sensor)
main()
