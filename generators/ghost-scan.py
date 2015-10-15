import math

rgb = 0
sC = 0
fadeSpeed = 0.02
runSpeed = 10

# NOTE time-based, but cheating with fading, which is inherently frame-based
def generator(dT, fr):
    global rgb
    for i in range(0, sC):
        if(int(dT*runSpeed) % (sC * 15)) == i:
            rgb[i*3 + 0] = 1
            rgb[i*3 + 1] = 1
            rgb[i*3 + 2] = 1
        else:
            rgb[i*3 + 0] -= fadeSpeed
            rgb[i*3 + 1] -= fadeSpeed
            rgb[i*3 + 2] -= fadeSpeed

    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('ghost-scan', generator)
