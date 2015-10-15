import math

rgb = 0
sC = 0

# a simple progression, layering color components at different frequencies and offsets
def generator1(dT, fr):
    global rgb
    spd = 1
    for i in range(0, sC):
        rgb[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * spd * 0.94 + i * 0.3)
        rgb[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * spd * 0.69 + i * 0.26)
        rgb[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * spd + i * 0.22)
    return rgb

# more complexity is added by varying the speed itself per component
def generator2(dT, fr):
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
    app.register_generator('progression1', generator1)
    app.register_generator('progression2', generator2)
