
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

#smooth progressive
g_prog1C = [0] * STRIPCOUNT * 3
def generator_prog1(dT, fr, sC):
    global g_prog1C
    spd = 1.2
    for i in range(0, sC):
        g_prog1C[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * spd * 0.94 + i * 0.3)
        g_prog1C[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * spd * 0.69 + i * 0.26)
        g_prog1C[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * spd + i * 0.22)

    return g_prog1C

#variable progressive
g_prog2C = [0] * STRIPCOUNT * 3
def generator_prog2(dT, fr, sC):
    global g_prog2C
    spd = 1
    for i in range(0, sC):
        g_prog2C[i * 3 + 0] = 0.5 + 0.5 * math.sin(dT * spd * 0.94 + i * 0.200 + 1.0 * math.sin(0.91 * dT))
        g_prog2C[i * 3 + 1] = 0.5 + 0.5 * math.sin(dT * spd * 0.69 + i * 0.212 + 1.1 * math.sin(0.96 * dT))
        g_prog2C[i * 3 + 2] = 0.5 + 0.5 * math.sin(dT * spd * 1.01 + i * 0.193 + 0.4 * math.sin(0.33 * dT))

    return g_prog2C

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

g_ghost1Colors = [0] * STRIPCOUNT * 3
def generator_Ghost1(dT, fr, sC):
    global g_ghost1Colors
    sp = 0.006
    for i in range(0, sC):
        c = 1
        if(int(dT*10) % 50) == i:
            z = int(dT*50) % 4
            if z == 0:
                g_ghost1Colors[i*3 + 0] = random.random()
                g_ghost1Colors[i*3 + 1] = random.random()
                g_ghost1Colors[i*3 + 2] = random.random()
        else:
            g_ghost1Colors[i*3 + 0] -= sp
            g_ghost1Colors[i*3 + 1] -= sp
            g_ghost1Colors[i*3 + 2] -= sp
            if(g_ghost1Colors[i*3 + 0] < 0): g_ghost1Colors[i*3 + 0] = 0
            if(g_ghost1Colors[i*3 + 1] < 0): g_ghost1Colors[i*3 + 1] = 0
            if(g_ghost1Colors[i*3 + 2] < 0): g_ghost1Colors[i*3 + 2] = 0

    return g_ghost1Colors

g_ghost2Colors = [0] * STRIPCOUNT * 3
def generator_Ghost2(dT, fr, sC):
    global g_ghost2Colors

    fadeSpeed = 0.02 # higher = faster
    runSpeed = 20    # higher = faster

    for i in range(0, sC):
        if(int(dT*runSpeed) % sC) == i:
            z = int((int(dT*runSpeed) % (sC * 3)) / sC)
            g_ghost2Colors[i*3 + z] += 1
            if(g_ghost2Colors[i*3 + 0] > 1): g_ghost2Colors[i*3 + 0] = 1
            if(g_ghost2Colors[i*3 + 1] > 1): g_ghost2Colors[i*3 + 1] = 1
            if(g_ghost2Colors[i*3 + 2] > 1): g_ghost2Colors[i*3 + 2] = 1
        else:
            g_ghost2Colors[i*3 + 0] -= fadeSpeed
            g_ghost2Colors[i*3 + 1] -= fadeSpeed
            g_ghost2Colors[i*3 + 2] -= fadeSpeed
            if(g_ghost2Colors[i*3 + 0] < 0): g_ghost2Colors[i*3 + 0] = 0
            if(g_ghost2Colors[i*3 + 1] < 0): g_ghost2Colors[i*3 + 1] = 0
            if(g_ghost2Colors[i*3 + 2] < 0): g_ghost2Colors[i*3 + 2] = 0

    return g_ghost2Colors

g_ghost3Colors = [0] * STRIPCOUNT * 3
def generator_Ghost3(dT, fr, sC):
    global g_ghost3Colors

    fadeSpeed = 0.02 # higher = faster
    runSpeed = 10    # higher = faster

    for i in range(0, sC):
        if(int(dT*runSpeed) % (sC * 15)) == i:
            g_ghost3Colors[i*3 + 0] = 1
            g_ghost3Colors[i*3 + 1] = 1
            g_ghost3Colors[i*3 + 2] = 1
        else:
            g_ghost3Colors[i*3 + 0] -= fadeSpeed
            g_ghost3Colors[i*3 + 1] -= fadeSpeed
            g_ghost3Colors[i*3 + 2] -= fadeSpeed
            if(g_ghost3Colors[i*3 + 0] < 0): g_ghost3Colors[i*3 + 0] = 0
            if(g_ghost3Colors[i*3 + 1] < 0): g_ghost3Colors[i*3 + 1] = 0
            if(g_ghost3Colors[i*3 + 2] < 0): g_ghost3Colors[i*3 + 2] = 0

    return g_ghost3Colors
