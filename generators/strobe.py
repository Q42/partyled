import math

rgb = 0
sC = 0

def generator(dT, fr):
    global rgb
    if fr % 2:
        v = 1
    else:
        v = 0

    for i in range(0, sC):
        rgb[i * 3 + 0] = v
        rgb[i * 3 + 1] = v
        rgb[i * 3 + 2] = v
    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('strobe', generator)
