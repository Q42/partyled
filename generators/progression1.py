import math

rgb = 0
sC = 0

def generator(dT, fr):
    global rgb
    spd = 1
    for i in range(0, sC):
        rgb[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * spd * 0.94 + i * 0.3)
        rgb[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * spd * 0.69 + i * 0.26)
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * spd + i * 0.22)
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('progression1', generator)
