#!/usr/bin/python
# coding=utf-8

import threading, time, math, sys, os, random
from flask import Flask, render_template, jsonify
from functools import partial
from pluginbase import PluginBase

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)

PWMAvailable = False

try:
    sys.path.append(get_path('./drivers/'))
    from Adafruit_PWM_Servo_Driver import PWM
    PWMAvailable = True
except ImportError, e:
    print "Cannot initialize PWM, if you're on a Mac, try using the simulator"
    print "Exception: ", (e)

IsSimulated = False
argv = sys.argv

if len(argv) == 2 and argv[1] == "node":
    IsSimulated = True

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2  # gamma correction
MASTER = float(1)
colors = [0] * STRIPCOUNT * 3
r = 0
g = 0
b = 0
frames = 0
fps = 0
fpstimer = 0
amp = 1
generators = []
generatorsByName = {}
generatorList = {}
currentTime = time.time()

print "==== PARTYLED ====\nSimulation: ", IsSimulated

class wrapper_Application(object):
    def register_generator(self, name, generator):
        global generatorList
        generatorList[name] = generator

wrapperApp = wrapper_Application()

generatorBase = PluginBase(package='partyled.generatorplugins')
generatorSource = generatorBase.make_plugin_source(searchpath=[get_path('./generators/')])

for plugin_name in generatorSource.list_plugins():
    plugin = generatorSource.load_plugin(plugin_name)
    plugin.setup(wrapperApp, STRIPCOUNT)

print "! Generator plugins: ", generatorList.items()

def setupPWM():
    pwm1 = PWM(0x40)  # PCA9685 board one
    pwm2 = PWM(0x41)  # PCA9685 board two
    pwm1.setPWMFreq(100)  # Not too low, to keep responsiveness to signals high
    pwm2.setPWMFreq(100)  # Also not too high, to prevent voltage rise to cut off and reduce brightness
    return (pwm1, pwm2)


if (PWMAvailable):
    (pwm1, pwm2) = setupPWM()

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
    if val < 0: val = 0;
    p = (val ** GAMMA) * PWMSCALE;
    if p > PWMSCALE - 1: p = PWMSCALE - 1
    return int(p)

def tick():
    global colors
    for i in range(0, STRIPCOUNT*3):
        colors[i] = 0

    currentTime = time.time()
    for generator in generators:
        newColors = generator(currentTime, frames)
        for i in range(0, STRIPCOUNT*3):
            colors[i] = min(colors[i] + max(newColors[i],0), 1)

class LightsThread(threading.Thread):
    def run(self):
        global fps, frames, fpstimer, colors, r, g, b

        while True:
            tick()

            if IsSimulated:
                time.sleep(0.01)
                string = ""

            for i in range(0, STRIPCOUNT):
                r = min(colors[i * 3]     * amp * MASTER, 1)
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

    for name, oper in generatorList.items():
        if name in generatorsByName:
            if generatorsByName[name] > 0:
                newGenerator.append(oper)

    generators = newGenerator

class AppThread(threading.Thread):
    def run(self):
        global MASTER
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
