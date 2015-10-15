
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
def generator_Scatter(dT, fr, sC):
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
        g_waveColors[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.2 + i * 1.6)
        g_waveColors[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_waveColors[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.6 + i * 1.6)

    return g_waveColors

g_waveGreen = [0] * STRIPCOUNT * 3
def generator_Wave_Green(dT, fr, sC):
    global g_waveGreen
    for i in range(0, sC):
        g_waveGreen[i * 3] = 0
        g_waveGreen[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_waveGreen[i * 3 + 2] = 0

    return g_waveGreen

g_waveBlue = [0] * STRIPCOUNT * 3
def generator_Wave_Blue(dT, fr, sC):
    global g_waveBlue
    for i in range(0, sC):
        g_waveGreen[i * 3 ] = 0
        g_waveGreen[i * 3 + 1] = 0
        g_waveGreen[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveGreen

g_wavePurple = [0] * STRIPCOUNT * 3
def generator_Wave_Purple(dT, fr, sC):
    global g_wavePurple
    for i in range(0, sC):
        g_wavePurple[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_wavePurple[i * 3 + 1] = 0
        g_wavePurple[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_wavePurple

g_waveRed = [0] * STRIPCOUNT * 3
def generator_Wave_Red(dT, fr, sC):
    global g_waveRed
    for i in range(0, sC):
        g_waveRed[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

    return g_waveRed

g_waveWhite = [0] * STRIPCOUNT * 3
def generator_Wave_White(dT, fr, sC):
    global g_waveWhite
    for i in range(0, sC):
        g_waveWhite[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_waveWhite[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)
        g_waveWhite[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * 5.4 + i * 1.6)

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

g_Random = [0] * STRIPCOUNT * 3
def generator_Random(dT, fr, sC):
    for i in range(0, sC):

        g_Random[i*3 + 0] -= 0.06
        g_Random[i*3 + 1] -= 0.06
        g_Random[i*3 + 2] -= 0.06

        if random.random() > 0.99:
            g_Random[i*3 + 0] = 1
            g_Random[i*3 + 1] = 1
            g_Random[i*3 + 2] = 1

        # if random.random() > 0.98:
        #     g_Random[i*3 + 0] = 0
        #     g_Random[i*3 + 1] = 0
        #     g_Random[i*3 + 2] = 0

        if(g_Random[i*3 + 0] < 0): g_Random[i*3 + 0] = 0
        if(g_Random[i*3 + 1] < 0): g_Random[i*3 + 1] = 0
        if(g_Random[i*3 + 2] < 0): g_Random[i*3 + 2] = 0

    return g_Random

g_ghostColors = [0] * STRIPCOUNT * 3
def generator_Ghost(dT, fr, sC):
    global g_ghostColors
    sp = 0.006
    for i in range(0, sC):
        c = 1
        if(int(dT*10) % 50) == i:
            z = int(dT*50) % 4
            if z == 0:
                g_ghostColors[i*3 + 0] = random.random()
                g_ghostColors[i*3 + 1] = random.random()
                g_ghostColors[i*3 + 2] = random.random()
        else:
            g_ghostColors[i*3 + 0] -= sp
            g_ghostColors[i*3 + 1] -= sp
            g_ghostColors[i*3 + 2] -= sp
            if(g_ghostColors[i*3 + 0] < 0): g_ghostColors[i*3 + 0] = 0
            if(g_ghostColors[i*3 + 1] < 0): g_ghostColors[i*3 + 1] = 0
            if(g_ghostColors[i*3 + 2] < 0): g_ghostColors[i*3 + 2] = 0

    return g_ghostColors

generator_waveGreenCueColors = [0] * STRIPCOUNT * 3
def cue_waveGreenCue(dT, startTime, fr, sC):
    global generator_waveGreenCueColors

    length = 1

    if startTime == 0 or (startTime + length) < time.time():
        generator_waveGreenCueColors = [0] * STRIPCOUNT * 3
    else:
        endTime = startTime + length
        progress = (dT - startTime) / (endTime - startTime)

        for i in range(0, sC):
            generator_waveGreenCueColors[i * 3] = 0
            generator_waveGreenCueColors[i * 3 + 1] = max(0, math.sin(2 * progress * math.pi - ((i - 1) * 0.1)))
            generator_waveGreenCueColors[i * 3 + 2] = 0

    return generator_waveGreenCueColors

generator_ghostGreenCueColors = [0] * STRIPCOUNT * 3
def cue_ghostGreenCue(dT, startTime, fr, sC):
    global generator_ghostGreenCueColors

    length = 1
    sp = 0.06

    if startTime == 0 or (startTime + length) < time.time():
        generator_ghostGreenCueColors = [0] * STRIPCOUNT * 3
    else:
        endTime = startTime + length
        progress = (dT - startTime) / (endTime - startTime)

        for i in range(0, sC):
            c = 1
            if progress < 0.1:
                generator_ghostGreenCueColors[i*3 + 0] = 0
                generator_ghostGreenCueColors[i*3 + 1] = 1
                generator_ghostGreenCueColors[i*3 + 2] = 0
            else:
                generator_ghostGreenCueColors[i*3 + 0] -= sp
                generator_ghostGreenCueColors[i*3 + 1] -= sp
                generator_ghostGreenCueColors[i*3 + 2] -= sp
                if(generator_ghostGreenCueColors[i*3 + 0] < 0): generator_ghostGreenCueColors[i*3 + 0] = 0
                if(generator_ghostGreenCueColors[i*3 + 1] < 0): generator_ghostGreenCueColors[i*3 + 1] = 0
                if(generator_ghostGreenCueColors[i*3 + 2] < 0): generator_ghostGreenCueColors[i*3 + 2] = 0

    return generator_ghostGreenCueColors

