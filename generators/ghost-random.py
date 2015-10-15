import math, random

rgb = 0
sC = 0
fadeSpeed = 0.02
runSpeed = 10

# NOTE time-based, but cheating with fading, which is inherently frame-based
def generator(dT, fr):
    global rgb
    sp = 0.006
    for i in range(0, sC):
        c = 1
        if(int(dT*10) % 50) == i:
            z = int(dT*50) % 4
            if z == 0:
                rgb[i*3 + 0] = random.random()
                rgb[i*3 + 1] = random.random()
                rgb[i*3 + 2] = random.random()
        else:
            rgb[i*3 + 0] -= sp
            rgb[i*3 + 1] -= sp
            rgb[i*3 + 2] -= sp

    return rgb

def setup(app, stripcount):
    global rgb, sC
    sC = stripcount
    rgb = [0] * sC * 3
    app.register_generator('ghost-random', generator)
