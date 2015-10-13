#!/usr/bin/python
# coding=utf-8

import threading
import time
import math
import sys
from flask import Flask, render_template, jsonify

execfile("generators.py")

PWMAvailable = True

try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError, e:
    PWMAvailable = False

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2  # gamma correction

colors = [0] * STRIPCOUNT * 3

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
    for i in range(0, STRIPCOUNT):
        colors[i * 3 + 0] = 0
        colors[i * 3 + 1] = 0
        colors[i * 3 + 2] = 0

    currentTime = time.time()
    for generator in generators:
        generator(currentTime, frames, STRIPCOUNT)

class LightsThread(threading.Thread):
    def run(self):
        global fps, frames, fpstimer, r, g, b

        r = 0
        g = 0
        b = 0

        while True:
            global colors, r, g, b
            tick()

            for i in range(0, STRIPCOUNT):
                r = colors[i * 3] * amp
                g = colors[i * 3 + 1] * amp
                b = colors[i * 3 + 2] * amp

                setStripColor(i, r, g, b)

            fps += 1
            frames += 1
            if time.time() > fpstimer + 1.0:
                print "1,FPS: ", fps, ";"
                fps = 0
                fpstimer = time.time()

def updateGenerators():
    global generators
    global generatorsByName
    newGenerator = []
    for name, value in generatorsByName.iteritems():
        print name, value
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

    print newGenerator

    generators = newGenerator


class AppThread(threading.Thread):
    def run(self):
        app = Flask(__name__)

        @app.route("/")
        def hello():
            return render_template('index.html')

        @app.route("/generator/<string:name>/<int:value>")
        def generator(name, value):
            generatorsByName[name] = value
            updateGenerators()
            return jsonify(generatorsByName)

        if __name__ == '__main__':
            app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0')

appThread = AppThread()
try:
    appThread.setDaemon(True)
    appThread.start()

    lightsThread = LightsThread()
    lightsThread.run()
except KeyboardInterrupt:
    print "Ctrl-c pressed ..."
    appThread.join(0)
    sys.exit()

