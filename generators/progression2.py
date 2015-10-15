import math

rgb = 0
sC = 0

def generator(dT, fr):
    global rgb
    spd = 1
    for i in range(0, sC):
        rgb[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * spd * 0.94 + i * 0.200 + 1.0 * math.sin(0.91 * dT))
        rgb[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * spd * 0.69 + i * 0.212 + 1.1 * math.sin(0.96 * dT))
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * spd * 1.01 + i * 0.193 + 0.4 * math.sin(0.33 * dT))
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('progression2', generator)
