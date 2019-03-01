#!/usr/bin/python3

# Author: Kenta Ishii
# SPDX short identifier: BSD-3-Clause
# ./nonlinear_regression.py tokyo2018.csv tokyo2019.csv

import sys
import math as math
import numpy as np
import matplotlib.pyplot as plt
import csv as csv

argv = sys.argv

## Actual Data for prediction
csvfile1 = open(argv[1], 'r')
dataobject1 = csv.reader(csvfile1, delimiter=',')
datalist1 = [] # Empty List

for row in dataobject1:
    # data in dataobject1 is str type
    #if isinstance(row[1], str) == True:
    number = float(row[1])
    datalist1.append(number)

#print(datalist1)

datalength1 = len(datalist1)
#print(datalength1)

## Actual Data to Be Predicted
csvfile2 = open(argv[2], 'r')
dataobject2 = csv.reader(csvfile2, delimiter=',')
datalist2 = [] # Empty List

for row in dataobject2:
    # data in dataobject2 is str type
    #if isinstance(row[1], str) == True:
    number = float(row[1])
    datalist2.append(number)

#print(datalist2)

datalength2 = len(datalist2)
#print(datalength2)

## Concatenation
datalist3 = datalist1 + datalist2

## Fourier Series
x_fft = np.linspace(0, datalength1 - 1, datalength1)
y_fft = np.fft.fft(datalist1)
#print(x_fft)
#print(y_fft)
#print(y_fft[6].real / datalength1)
#print(y_fft[6].imag / datalength1)
wavelist = [] # Empty List
for i in range(datalength1, 0, -1): # Decremental Order
    sigma = 0
    for j in range(0, 10, 1):
        sigma += (y_fft[j].real / datalength1) * np.cos((2 * math.pi * i * j) / datalength1)
        sigma += (y_fft[j].imag / datalength1) * np.sin((2 * math.pi * i * j) / datalength1)

    wavelist.append(sigma)

## Nonlinear Regression
a, b, c, d, e, f = np.polyfit(x_fft, wavelist, 5)
x_nonlinear = np.linspace(0, datalength1 + datalength2 - 1, datalength1 + datalength2)
y_nonlinear = a * x_nonlinear**5 + b * x_nonlinear**4 + c * x_nonlinear**3 + d * x_nonlinear**2 + e * x_nonlinear + f

fig = plt.figure()

#Size of Rows, Size of Columns, Place
ax1 = fig.add_subplot(2,1,1)
ax1.plot(x_fft, datalist1)
ax1.plot(x_fft, wavelist)
plt.title("Actual and Fourier Series")
plt.xlabel("Days")
plt.ylabel("Temperature Avg in Celsius")
#ax2 = fig.add_subplot(2,1,2)
#ax2.plot(x_fft, abs(y_fft * y_fft))
#plt.title("Power Spectrum")
ax3 = fig.add_subplot(2,1,2)
ax3.plot(x_nonlinear, y_nonlinear)
ax3.plot(x_nonlinear, datalist3)
plt.title("Prediction by Nonlinear Regression and Actual")
plt.subplots_adjust(wspace=0.2,hspace=1.0)
plt.show()
