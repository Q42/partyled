
# --------------- GENERATORS ------------------------------
# these actually drive the LEDs. TODO make these into actual plugins
# IN:  dT = time, use this as the sole driver for your output whenever possible
#      frames = framecounter, ONLY use this when you have strobe-like effects
#         that need precise frame-timings not to look odd. The reason is that
#         frame timings can change as hardware changes! right now, it's ~50fps.
#      sC = strip count, how many strips are connected.
# OUT: none, but the function is expected to mutate the values of colors[0..3*sC]
#      with 0..1 r/g/b/r/g/b/r/g/b etc values

# generator: fast/hard on/off walk
# example of when you might want to use the framecounter
def generator_Scatter(dT, fr, sC):
    global colors
    for i in range(0, sC):
        c = 0
        if fr % 10 == i: c = 1
        colors[i * 3 + 0] += c
        colors[i * 3 + 1] += c
        colors[i * 3 + 2] += c

def generator_Strobe(dT, fr, sC):
    if fr % 2:
        v = 1
    else:
        v = 0

    for i in range(0, sC):
        colors[i * 3 + 0] = v
        colors[i * 3 + 1] = v
        colors[i * 3 + 2] = v

# generator: smooth grayscale sinewave across strips
def generator_Wave(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.2 + i * 1.6)
        colors[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.6 + i * 1.6)


def generator_Wave_Green(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

def generator_Wave_Blue(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

def generator_Wave_Purple(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

def generator_Wave_Red(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

def generator_Wave_White(dT, fr, sC):
    global colors
    for i in range(0, sC):
        colors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

def generator_ON(dT, fr, sC):
    for i in range(0, sC * 3):
        colors[i] = 1

def generator_Green_Burst(dT, fr, sC):
    for i in range(0, sC * 3):
        colors[i] += 0

