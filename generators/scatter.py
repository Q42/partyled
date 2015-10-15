import math

rgb = 0
sC = 0

def generator(dT, fr):
    global rgb
    for i in range(0, sC):
        c = 0
        if fr % 10 == i: c = 1
        rgb[i * 3 + 0] = c
        rgb[i * 3 + 1] = c
        rgb[i * 3 + 2] = c
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('scatter', generator)
