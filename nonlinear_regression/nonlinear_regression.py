#!/usr/bin/python3

# Author: Kenta Ishii
# SPDX short identifier: BSD-3-Clause
# ./nonlinear_regression.py tokyo.csv

import sys
import math as math
import numpy as np
import matplotlib.pyplot as plt
import csv as csv

argv = sys.argv
csvfile = open(argv[1], 'r')
dataobject = csv.reader(csvfile, delimiter=',')

datalist = [] # Empty List

for row in dataobject:
    # data in dataobject is str type
    #if isinstance(row[1], str) == True:
    number = float(row[1])
    datalist.append(number)

#print(datalist)

datalength = len(datalist)
#print(datalength)

# Fourier Series
x_fft = np.linspace(0, datalength - 1, datalength)
y_fft = np.fft.fft(datalist)
#print(x_fft)
#print(y_fft)
#print(y_fft[6].real / datalength)
#print(y_fft[6].imag / datalength)
wavelist = [] # Empty List
for i in range(datalength, 0, -1): # Decremental Order
    sigma = 0
    for j in range(0, datalength >> 4, 1):
        sigma += (y_fft[j].real / datalength) * np.cos((2 * math.pi * i * j) / datalength)
        sigma += (y_fft[j].imag / datalength) * np.sin((2 * math.pi * i * j) / datalength)

    wavelist.append(sigma)

# Nonlinear Regression
a, b, c, d, e = np.polyfit(x_fft, wavelist, 4)
x_nonlinear = np.linspace(0, datalength + 90 - 1, datalength + 90)
y_nonlinear = a * x_nonlinear**4 + b * x_nonlinear**3 + c * x_nonlinear**2 + d * x_nonlinear + e

fig = plt.figure()

#Size of Rows, Size of Columns, Place
ax1 = fig.add_subplot(3,1,1)
ax1.plot(x_fft, datalist)
plt.title("Actual")
plt.xlabel("Days")
plt.ylabel("Temperature C")
#ax2 = fig.add_subplot(3,1,2)
#ax2.plot(x_fft, abs(y_fft * y_fft))
#plt.title("Power Spectrum")
ax3 = fig.add_subplot(3,1,2)
ax3.plot(x_fft, wavelist)
plt.title("Fourier Series")
ax4 = fig.add_subplot(3,1,3)
ax4.plot(x_nonlinear, y_nonlinear)
plt.title("Nonlinear Regression")
plt.subplots_adjust(wspace=0.2,hspace=1.0)
plt.show()
