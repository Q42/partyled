#!/usr/bin/python
# coding=utf-8

import threading
import time
import math
import sys
import platform
import os
import socket
import fileinput

PWMAvailable = True

try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError, e:
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

# set a single strip's color.
#   StripID is 0..STRIPCOUNT
#   r, g, b is 0..1

def setStripColor(stripID, r, g, b):

    if (PWMAvailable):
        if stripID < 5:
            pwm1.setPWM(stripID * 3 + 0, 0, pwmscale(r))
            pwm1.setPWM(stripID * 3 + 1, 0, pwmscale(g))
            pwm1.setPWM(stripID * 3 + 2, 0, pwmscale(b))
        else:
            pwm2.setPWM((stripID - 5) * 3 + 0, 0, pwmscale(r))
            pwm2.setPWM((stripID - 5) * 3 + 1, 0, pwmscale(g))
            pwm2.setPWM((stripID - 5) * 3 + 2, 0, pwmscale(b))


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
    colors = [0] * STRIPCOUNT * 3
    for i in range(0, sC):
        c = 0
        if fr % 10 == i: c = 1
        colors[i*3 + 0] = c
        colors[i*3 + 1] = c
        colors[i*3 + 2] = c

    return colors

# generator: smooth grayscale sinewave across strips
def generator_Wave(dT, fr, sC):
    colors = [0] * STRIPCOUNT * 3
    for i in range(0, sC):
        colors[i*3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.2 + i * 1.6)
        colors[i*3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i*3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.6 + i * 1.6)

    return colors

def generator_Wave_Green(dT, fr, sC):
    colors = [0] * STRIPCOUNT * 3
    for i in range(0, sC):
        colors[i*3 + 0] = 0
        colors[i*3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i*3 + 2] = 0

    return colors

def generator_ON(dT, fr, sC):
  for i in range(0, sC * 3):
    colors[i] = 1

amp = 1

generators = []

def tick():
    colors = [0] * STRIPCOUNT * 3

    for generator in generators:
        newColors = generator(time.time(), frames, STRIPCOUNT)
        for i in range(0, len(colors)):
            colors[i] = colors[i] + newColors[i]

    return colors

class LightsThread(threading.Thread):
    def run(self):
        global fps
        global frames
        global fpstimer

        while (True):

            colors = tick()
            string = ""

            for i in range(0, STRIPCOUNT):
                r = colors[i*3] * amp
                g = colors[i*3 + 1] * amp
                b = colors[i*3 + 2] * amp

                setStripColor(i, r, g, b)
                string = string + "0,"+str(i)+","+str(r)+","+str(g)+","+str(b)+";"
            print string

            fps += 1
            frames += 1
            if time.time() > fpstimer + 1.0:
                print "1,FPS: ",fps,";"
                fps = 0
                fpstimer = time.time()


class InputThread(threading.Thread):
    def run(self):
        global generators
        while(True):
            string = raw_input()

            setGenerators = string.split("%")

            newGenerator = []

            for i in range(0, len(setGenerators)):
                if (len(setGenerators[i]) > 1):
                    switch = setGenerators[i].split("$")
                    name = switch[0]
                    if (name == "wave" and switch[1] == '1'):
                        newGenerator.append(generator_Wave_Green)
                    if (name == "strobe" and switch[1] == '1'):
                        newGenerator.append(generator_Strobe)
            generators = newGenerator

lightsThread = LightsThread()
lightsThread.start()
inputThread = InputThread()
inputThread.start()