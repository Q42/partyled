#!/usr/bin/python
# coding=utf-8

from threading import Timer
import time
import math
import sys
import platform
import os
import socket
import colorama
from colorama import Fore, Back, Style

# setup ANSI space

colorama.init()
pos = lambda x, y: '\x1b[%d;%dH' % (y, x)
def printPos(x, y, color, message):
    if not NodeParent:
        print color + pos(x, y) + message

PWMAvailable = True
if (len(sys.argv) > 1):
    NodeParent = sys.argv[1] == "node"
else:
    NodeParent = False

print NodeParent

try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError, e:
    print "entering stimulator mode..."
    PWMAvailable = False

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2      # gamma correction

def setupPWM():
    pwm1 = PWM(0x40) # PCA9685 board one
    pwm2 = PWM(0x41) # PCA9685 board two
    pwm1.setPWMFreq(100) # Not too low, to keep responsiveness to signals high
    pwm2.setPWMFreq(100) # Also not too high, to prevent voltage rise to cut off and reduce brightness
    return (pwm1, pwm2)

if (PWMAvailable):
    (pwm1, pwm2) = setupPWM()

# globals (to prevent reallocating/GC)fps = 0
frames = 0
fps = 0
fpstimer = 0
colors = [0] * STRIPCOUNT * 3

# set a single strip's color.
#   StripID is 0..STRIPCOUNT
#   r, g, b is 0..1

def charForValue(v):
    if (v == 0):
        return ' '
    if (v < 0.25):
        return '░'
    if (v >= 0.25 and v < 0.5):
        return '▒'
    if (v >= 0.5 and v < 0.75):
        return '▓'

    return '▉'

def setStripColorSim(stripID, r, g, b):
    printPos(stripID * 3 + 0, 0, Fore.RED, charForValue(r))
    printPos(stripID * 3 + 1, 0, Fore.GREEN, charForValue(g))
    printPos(stripID * 3 + 2, 0, Fore.BLUE, charForValue(b))

def printListener(m):
    print m

def setStripColor(stripID, r, g, b):
    if NodeParent:
        printListener(str(stripID)+","+str(r)+","+str(g)+","+str(b)+";")

    if (PWMAvailable):
        if stripID < 5:
            pwm1.setPWM(stripID * 3 + 0, 0, pwmscale(r))
            pwm1.setPWM(stripID * 3 + 1, 0, pwmscale(g))
            pwm1.setPWM(stripID * 3 + 2, 0, pwmscale(b))
        else:
            pwm2.setPWM((stripID - 5) * 3 + 0, 0, pwmscale(r))
            pwm2.setPWM((stripID - 5) * 3 + 1, 0, pwmscale(g))
            pwm2.setPWM((stripID - 5) * 3 + 2, 0, pwmscale(b))
    else:
        setStripColorSim(stripID, r, g, b)

# clip and scale a 0..1 input (inclusive) to 0..PWMSCALE
def pwmscale(val):
  p = (val ** GAMMA) * PWMSCALE;
  if p < 0: p = 0;
  if p > PWMSCALE-1: p = PWMSCALE-1
  return int(p)

# --------------- GENERATORS ------------------------------
# these actually drive the LEDs. TODO make these into actual plugins
# IN:  dT = time, use this as the sole driver for your output whenever possible
#      frames = framecounter, ONLY use this when you have strobe-like effects
#         that need precise frame-timings not to look odd. The reason is that
#         frame timings can change as hardware changes! right now, it's ~50fps.
#      sC = strip count, how many strips are connected.
# OUT: none, but the function is expected to mutate the values of colors[0..3*sC]
#      with 0..1 r/g/b/r/g/b/r/g/b etc values

# generator: fast/hard on/off walk
# example of when you might want to use the framecounter
def generator_Strobe(dT, fr, sC):
  for i in range(0, sC):
    c = 0
    if fr % 10 == i: c = 1
    colors[i*3 + 0] = c
    colors[i*3 + 1] = c
    colors[i*3 + 2] = c

# generator: smooth grayscale sinewave across strips
def generator_Wave(dT, fr, sC):
  for i in range(0, sC):
    colors[i*3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.2 + i * 1.6)
    colors[i*3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
    colors[i*3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.6 + i * 1.6)

def generator_Wave_Green(dT, fr, sC):
    for i in range(0, sC):
        colors[i*3 + 0] = 0
        colors[i*3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i*3 + 2] = 0


def generator_ON(dT, fr, sC):
  for i in range(0, sC * 3):
    colors[i] = 1

print "-----/ Q42 / partyLED /------"

amp = 1

while (True):
  generator_Wave_Green(time.time(), frames, STRIPCOUNT)
  # generator_Wave(time.time(), frames, STRIPCOUNT)
  # generator_Strobe(time.time(), frames, STRIPCOUNT)
  #generator_ON(0,0,STRIPCOUNT)
  for i in range(0, STRIPCOUNT):
    setStripColor(i, colors[i*3] * amp, colors[i*3 + 1] * amp, colors[i*3 + 2] * amp)
  fps += 1
  frames += 1
  if time.time() > fpstimer + 1.0:
    #print "FPS: ", fps
    fps = 0
    fpstimer = time.time()

