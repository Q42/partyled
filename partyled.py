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
    print(e)
    PWMAvailable = False

IsSimulated = False
argv = sys.argv

if len(argv) == 2 and argv[1] == "node":
    IsSimulated = True

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2  # gamma correction
MASTER = float(1)
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
    #print "Setting ", stripID, " to ", r, "/", g, "/", b
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

<<<<<<< HEAD
generators = [generator_Wave_White]

=======
generators = []
generatorsByName = {}
>>>>>>> webserver
currentTime = time.time()

def tick():
    global colors
    for i in range(0, STRIPCOUNT*3):
        colors[i] = 0

    currentTime = time.time()
    for generator in generators:
<<<<<<< HEAD
        generator(currentTime, frames, STRIPCOUNT)

    generator_Green_Burst(currentTime, frames, STRIPCOUNT)

def sleepFromFPS(currentFps):
        return
	# if fps < 60:
	# 	return

	# fw = (1.0 / 60)
	# fc = (1.0 / currentFps)

	# sleepTime = fw - fc

	# print "1,FPS sleep: ", fw, fc, currentFps, sleepTime, ";"

	# time.sleep(0.001)
=======
        newColors = generator(currentTime, frames, STRIPCOUNT)
        for i in range(0, STRIPCOUNT*3):
            colors[i] = min(colors[i] + newColors[i], 1)
>>>>>>> webserver

class LightsThread(threading.Thread):
    def run(self):
        global fps, frames, fpstimer

        r = 0
        g = 0
        b = 0

        while True:
            global colors, r, g, b
            tick()

<<<<<<< HEAD
            # string = ""
            for i in range(0, STRIPCOUNT):
                r = colors[i * 3] * amp
                g = colors[i * 3 + 1] * amp
                b = colors[i * 3 + 2] * amp

                setStripColor(i, r, g, b)
                # string = string + "0," + str(i) + "," + str(r) + "," + str(g) + "," + str(b) + ";"

            # print string for capture with node
            # print string
=======
            if IsSimulated:
                time.sleep(0.01)
                string = ""
>>>>>>> webserver

            for i in range(0, STRIPCOUNT):
                r = min(colors[i * 3] * amp * MASTER, 1)
                g = min(colors[i * 3 + 1] * amp * MASTER, 1)
                b = min(colors[i * 3 + 2] * amp * MASTER, 1)
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
        global MASTEr
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

        @app.route("/master/<string:value>")
        def master(value):
            MASTER = float(value)
            return MASTER

        @app.route("/generator/<string:name>/<int:value>")
        def generator(name, value):
            generatorsByName[name] = value
            updateGenerators()
            return jsonify(generatorsByName)

        if __name__ == '__main__':
            app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=4000)

class InputThread(threading.Thread):
    def run(self):
        global generators, generatorsByName, MASTER

        while True:
            string = raw_input()
            if string == "e":
<<<<<<< HEAD
            	process.exit()

            setGenerators = string.split("%")

            newGenerator = []

            for i in range(0, len(setGenerators)):
                if len(setGenerators[i]) > 1:
                    switch = setGenerators[i].split("$")
                    name = switch[0]
                    if name == "wavegreen" and switch[1] == '1':
                        newGenerator.append(generator_Wave_Green)
                    if name == "waveblue" and switch[1] == '1':
                        newGenerator.append(generator_Wave_Blue)
                    if name == "wavepurple" and switch[1] == '1':
                        newGenerator.append(generator_Wave_Purple)
                    if name == "wavered" and switch[1] == '1':
                        newGenerator.append(generator_Wave_Red)
                    if name == "wavewhite" and switch[1] == '1':
                        newGenerator.append(generator_Wave_White)
                    if name == "scatter" and switch[1] == '1':
                        newGenerator.append(generator_Scatter)
                    if name == "strobe" and switch[1] == '1':
                        newGenerator.append(generator_Strobe)
                    if name == "wavecolor" and switch[1] == '1':
                        newGenerator.append(generator_Wave)

            generators = newGenerator


def signal_handler(signal, frame):
        print('Breaking')
        lightsThread.stop()
        inputThread.stop()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


lightsThread = LightsThread()
#lightsThread.start()
inputThread = InputThread()
inputThread.start()

lightsThread.run()
=======
                appThread.join(0)
                sys.exit()

            command = string.split(";")

            if command[0] == "v":
                setGenerators = command[1].split("%")
                for i in range(0, len(setGenerators)):
                    if len(setGenerators[i]) > 1:
                        switch = setGenerators[i].split("$")
                        name = switch[0]
                        value = int(switch[1])
                        generatorsByName[name] = value
                updateGenerators()
            if command[0] == "m":
                MASTER = float(command[1])


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

>>>>>>> webserver
