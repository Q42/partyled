import math

rgb = 0
sC = 0

def generator_green(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0
        rgb[i * 3 + 1] = 1
        rgb[i * 3 + 2] = 0
    return rgb

def generator_red(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 1
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 0
    return rgb

def generator_purple(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 1
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 1
    return rgb

def generator_blue(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] = 0
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 1
    return rgb

def generator_white(dT, fr):
    global rgb
    for i in range(0, sC):
        rgb[i * 3] =     1
        rgb[i * 3 + 1] = 1
        rgb[i * 3 + 2] = 1
    return rgb

def generator_rgb(dT, fr):
    global rgb
    z = int(dT) % 4
    for i in range(0, sC):
        rgb[i * 3] =     0
        rgb[i * 3 + 1] = 0
        rgb[i * 3 + 2] = 0
        if z < 3: rgb[i * 3 + z] = 1
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('allgreen', generator_green)
    app.register_generator('allred', generator_red)
    app.register_generator('allpurple', generator_purple)
    app.register_generator('allblue', generator_blue)
    app.register_generator('allwhite', generator_white)
    app.register_generator('rgb', generator_rgb)
