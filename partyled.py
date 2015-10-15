#!/usr/bin/python
# coding=utf-8

import threading
import time
import math
import sys
from flask import Flask, render_template, jsonify
import random

PWMAvailable = True

try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError, e:
    PWMAvailable = False

IsSimulated = False
argv = sys.argv

if len(argv) == 2 and argv[1] == "node":
    IsSimulated = True

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2  # gamma correction

colors = [0] * STRIPCOUNT * 3

execfile("generators.py")

def setupPWM():
    pwm1 = PWM(0x40)  # PCA9685 board one
    pwm2 = PWM(0x41)  # PCA9685 board two
    pwm1.setPWMFreq(100)  # Not too low, to keep responsiveness to signals high
    pwm2.setPWMFreq(100)  # Also not too high, to prevent voltage rise to cut off and reduce brightness
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
    if p > PWMSCALE - 1: p = PWMSCALE - 1
    return int(p)

amp = 1

generators = []
generatorsByName = {}
currentTime = time.time()

def tick():
    global colors
    for i in range(0, STRIPCOUNT*3):
        colors[i] = 0

    currentTime = time.time()
    for generator in generators:
        newColors = generator(currentTime, frames, STRIPCOUNT)
        for i in range(0, STRIPCOUNT*3):
            colors[i] = min(colors[i] + newColors[i], 1)

class LightsThread(threading.Thread):
    def run(self):
        global fps, frames, fpstimer

        r = 0
        g = 0
        b = 0

        while True:
            global colors, r, g, b
            tick()

            if IsSimulated:
                time.sleep(0.01)
                string = ""

            for i in range(0, STRIPCOUNT):
                r = min(colors[i * 3] * amp, 1)
                g = min(colors[i * 3 + 1] * amp, 1)
                b = min(colors[i * 3 + 2] * amp, 1)
                if IsSimulated:
                    string = string + "0," + str(i) + "," + str(r) + "," + str(g) + "," + str(b) + ";"
                else:
                    setStripColor(i, r, g, b)

            if IsSimulated:
                print string
                sys.stdout.flush()

            fps += 1
            frames += 1
            if time.time() > fpstimer + 1.0:
                fps = 0
                fpstimer = time.time()

def updateGenerators():
    global generators
    global generatorsByName
    newGenerator = []
    for name, value in generatorsByName.iteritems():
        if name == "wavegreen" and value == 1:
            newGenerator.append(generator_Wave_Green)
        if name == "waveblue" and value == 1:
            newGenerator.append(generator_Wave_Blue)
        if name == "wavepurple" and value == 1:
            newGenerator.append(generator_Wave_Purple)
        if name == "wavered" and value == 1:
            newGenerator.append(generator_Wave_Red)
        if name == "wavewhite" and value == 1:
            newGenerator.append(generator_Wave_White)
        if name == "scatter" and value == 1:
            newGenerator.append(generator_Scatter)
        if name == "strobe" and value == 1:
            newGenerator.append(generator_Strobe)
        if name == "wavecolor" and value == 1:
            newGenerator.append(generator_Wave)
        if name == "ghost" and value == 1:
            newGenerator.append(generator_Ghost)

    generators = newGenerator

class AppThread(threading.Thread):
    def run(self):
        app = Flask(__name__)

        @app.route("/")
        def index():
            return render_template('index.html')

        @app.route("/settings")
        def settings():
            settingsObj = {
                "connection": "ajax"
            }
            return jsonify(settingsObj)

        @app.route("/generator/<string:name>/<int:value>")
        def generator(name, value):
            generatorsByName[name] = value
            updateGenerators()
            return jsonify(generatorsByName)

        if __name__ == '__main__':
            app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=4000)

class InputThread(threading.Thread):
    def run(self):
        global generators
        global generatorsByName
        while True:
            string = raw_input()
            if string == "e":
                appThread.join(0)
                sys.exit()

            setGenerators = string.split("%")
            for i in range(0, len(setGenerators)):
                if len(setGenerators[i]) > 1:
                    switch = setGenerators[i].split("$")
                    name = switch[0]
                    value = int(switch[1])
                    generatorsByName[name] = value
            updateGenerators()

appThread = AppThread()
inputThread = InputThread()
try:
    if IsSimulated:
        inputThread.start()
    else:
        appThread.setDaemon(True)
        appThread.start()

    lightsThread = LightsThread()
    lightsThread.run()
except KeyboardInterrupt:
    print "Ctrl-c pressed ..."
    appThread.join(0)
    sys.exit()

