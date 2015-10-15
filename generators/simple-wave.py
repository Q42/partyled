import math

rgb = 0
sC = 0

speed = 5.4
stripstep = 0.3

def generator_green(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0
        rgb[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
        rgb[i * 3 + 2] = 0
    return rgb

def generator_red(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 0
    return rgb

def generator_purple(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
    return rgb

def generator_blue(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
    return rgb

def generator_white(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] =     0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
        rgb[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * speed + i * stripstep)
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('wavegreen', generator_green)
    app.register_generator('wavered', generator_red)
    app.register_generator('wavepurple', generator_purple)
    app.register_generator('waveblue', generator_blue)
    app.register_generator('wavewhite', generator_white)
