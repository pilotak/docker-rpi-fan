#!/usr/bin/env python3

# MIT License

# Copyright (c) 2020 Pavel Slama

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import time
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO


DESIRED_TEMP = float(os.getenv('DESIRED_TEMP', 40))

FAN_PIN = int(os.getenv('FAN_PIN', 13))
FAN_PWM_MIN = int(os.getenv('FAN_PWM_MIN', 20))
FAN_PWM_MAX = int(os.getenv('FAN_PWM_MAX', 100))
FAN_PWM_FREQ = int(os.getenv('FAN_PWM_FREQ', 17))

P_TEMP = float(os.getenv('P_TEMP', 18.0))
I_TEMP = float(os.getenv('I_TEMP', 0.3))

READ_INTERVAL = int(os.getenv('READ_INTERVAL', 2))

fanSpeed = FAN_PWM_MAX
sum = 0
pTemp = 18
iTemp = 0.3


def getCPUtemperature():
    temp = os.popen('cat /sys/class/thermal/thermal_zone*/temp').readline()
    temp = float(temp)
    temp /= 1000.0
    return temp


def fanOFF():
    myPWM.ChangeDutyCycle(0)
    return()


def handleFan():
    global fanSpeed, sum
    actualTemp = float(getCPUtemperature())
    diff = actualTemp - DESIRED_TEMP
    sum = sum + diff
    pDiff = diff * pTemp
    iDiff = sum * iTemp
    fanSpeed = pDiff + iDiff

    if fanSpeed > FAN_PWM_MAX:
        fanSpeed = FAN_PWM_MAX
    if fanSpeed < FAN_PWM_MIN:
        fanSpeed = 0
    if sum > 100:
        sum = 100
    if sum < -100:
        sum = -100
    # print("actualTemp %4.2f TempDiff %4.2f pDiff %4.2f iDiff %4.2f fanSpeed %5d" % (
    #     actualTemp, diff, pDiff, iDiff, fanSpeed))
    myPWM.ChangeDutyCycle(fanSpeed)
    return()


try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    myPWM = GPIO.PWM(FAN_PIN, FAN_PWM_FREQ)
    myPWM.start(50)
    GPIO.setwarnings(False)
    fanOFF()

    while True:
        handleFan()
        sleep(READ_INTERVAL)
except KeyboardInterrupt:
    fanOFF()
finally:
    GPIO.cleanup()
