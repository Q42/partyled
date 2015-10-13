
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

g_scatterColors = [0] * STRIPCOUNT * 3
def g_Scatter(dT, fr, sC):
    global g_scatterColors
    for i in range(0, sC):
        c = 0
        if fr % 10 == i: c = 1
        g_scatterColors[i * 3 + 0] = c
        g_scatterColors[i * 3 + 1] = c
        g_scatterColors[i * 3 + 2] = c

    return g_scatterColors

g_strobeColors = [0] * STRIPCOUNT * 3
def generator_Strobe(dT, fr, sC):
    global g_strobeColors
    if fr % 2:
        v = 1
    else:
        v = 0

    for i in range(0, sC):
        g_strobeColors[i * 3 + 0] = v
        g_strobeColors[i * 3 + 1] = v
        g_strobeColors[i * 3 + 2] = v

    return g_strobeColors

# generator: smooth grayscale sinewave across strips
g_waveColors = [0] * STRIPCOUNT * 3
def generator_Wave(dT, fr, sC):
    global g_waveColors
    for i in range(0, sC):
        g_waveColors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.2 + i * 1.6)
        g_waveColors[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_waveColors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.6 + i * 1.6)

    return g_waveColors

g_waveGreen = [0] * STRIPCOUNT * 3
def generator_Wave_Green(dT, fr, sC):
    global g_waveGreen
    for i in range(0, sC):
        g_waveGreen[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveGreen

g_waveBlue = [0] * STRIPCOUNT * 3
def generator_Wave_Blue(dT, fr, sC):
    global g_waveGreen
    for i in range(0, sC):
        g_waveGreen[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveGreen

g_wavePurple = [0] * STRIPCOUNT * 3
def generator_Wave_Purple(dT, fr, sC):
    global g_wavePurple
    for i in range(0, sC):
        g_wavePurple[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_wavePurple[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_wavePurple

g_waveRed = [0] * STRIPCOUNT * 3
def generator_Wave_Red(dT, fr, sC):
    global g_waveRed
    for i in range(0, sC):
        g_waveRed[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveRed

g_waveWhite = [0] * STRIPCOUNT * 3
def generator_Wave_White(dT, fr, sC):
    global g_waveWhite
    for i in range(0, sC):
        colors[i * 3 + 0] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 1] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        colors[i * 3 + 2] += 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveWhite

g_onColors = [0] * STRIPCOUNT * 3
def generator_ON(dT, fr, sC):
    global g_onColors
    for i in range(0, sC * 3):
        g_onColors[i] = 1

    return g_onColors

g_greenBurstColors = [0] * STRIPCOUNT * 3
def generator_Green_Burst(dT, fr, sC):
    global g_greenBurstColors
    for i in range(0, sC * 3):
        g_greenBurstColors[i] += 0

    return g_greenBurstColors

