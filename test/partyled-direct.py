#!/usr/bin/python

from threading import Timer
import time
import math
import sys
import platform
import random

if platform.system() == 'Darwin' or platform.system() == 'Windows':
    print "WARNING: this program needs an I2C bus and should be run on a Raspberry Pi."
    print "It is almost guaranteed not to work on your Mac or Windows box.\n"

try:
    from Adafruit_PWM_Servo_Driver import PWM
except ImportError, e:
    print "Cannot import PWM driver ('", e, "'), please check setup instructions in README.md\n"
    sys.exit()

STRIPCOUNT = 10  # number of Q42 awesome 12V analog RGB LED strips. 10 is the max for now.
PWMSCALE = 4096  # fit in PWM bitdepth. PCA9685 has a 12-bit PWM converter.
GAMMA = 2.2      # gamma correction

pwm1 = PWM(0x40) # PCA9685 board one
pwm2 = PWM(0x41) # PCA9685 board two
pwm1.setPWMFreq(100) # Not too low, to keep responsiveness to signals high
pwm2.setPWMFreq(100) # Also not too high, to prevent voltage rise to cut off and reduce brightness

# globals (to prevent reallocating/GC)fps = 0
frames = 0
fps = 0
fpstimer = 0
colors = [0] * STRIPCOUNT * 3

# set a single strip's color.
#   StripID is 0..STRIPCOUNT
#   r, g, b is 0..1
def setStripColor(stripID, r, g, b):
  if stripID < 5:
    pwm1.setPWM(stripID * 3 + 0, 0, pwmscale(r))
    pwm1.setPWM(stripID * 3 + 1, 0, pwmscale(g))
    pwm1.setPWM(stripID * 3 + 2, 0, pwmscale(b))
  else:
    pwm2.setPWM((stripID - 5) * 3 + 0, 0, pwmscale(r))
    pwm2.setPWM((stripID - 5) * 3 + 1, 0, pwmscale(g))
    pwm2.setPWM((stripID - 5) * 3 + 2, 0, pwmscale(b))

# clip and scale a 0..1 input (inclusive) to 0..PWMSCALE
def pwmscale(val):
  p = (val ** GAMMA) * PWMSCALE;
  if p < 0: p = 0;
  if p > PWMSCALE-1: p = PWMSCALE-1
  return int(p)

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
def generator_Strobe(dT, fr, sC):
  for i in range(0, sC):
    c = 0
    if(int(dT*8) % 10) == i: c = 1
    colors[i*3 + 0] = 0
    colors[i*3 + 1] = 0
    colors[i*3 + 2] = c

def generator_Ghost(dT, fr, sC):
  sp = 0.006
  for i in range(0, sC):
    c = 1
    if(int(dT*10) % 50) == i:
      z = int(dT*50) % 4
      if z == 0:
        colors[i*3 + 0] = random.random()
        colors[i*3 + 1] = random.random()
        colors[i*3 + 2] = random.random()
    else:
      colors[i*3 + 0] -= sp
      colors[i*3 + 1] -= sp
      colors[i*3 + 2] -= sp
      if(colors[i*3 + 0] < 0): colors[i*3 + 0] = 0
      if(colors[i*3 + 1] < 0): colors[i*3 + 1] = 0
      if(colors[i*3 + 2] < 0): colors[i*3 + 2] = 0


# generator: smooth grayscale sinewave across strips
def generator_Wave(dT, fr, sC):
  for i in range(0, sC):
    colors[i*3 + 0] = 0.7 + 0.3 * math.sin(dT * 4.2 + i * 1.6)
    colors[i*3 + 1] = 0.7 + 0.3 * math.sin(dT * 4.3 + i * 1.6)
    colors[i*3 + 2] = 0.7 + 0.3 * math.sin(dT * 4.4 + i * 1.6)

def generator_Red(dT, fr, sC):
  for i in range(0, sC):
    colors[i * 3] = 1

def generator_ON(dT, fr, sC):
  for i in range(0, sC * 3):
    colors[i] = 1

def generator_TEST(dT, fr, sC):
  for i in range(0,sC):
    z = int(dT*1) % 3
    colors[i*3]     = 0
    colors[i*3 + 1] = 0
    colors[i*3 + 2] = 0
    colors[i*3 + z] = 1

print "-----/ Q42 / partyLED /------"

amp = 1

while (True):
  generator_Ghost(time.time(), frames, STRIPCOUNT)
  for i in range(0, STRIPCOUNT):
    setStripColor(i, colors[i*3] * amp, colors[i*3 + 1] * amp, colors[i*3 + 2] * amp)
  fps += 1
  frames += 1
  if time.time() > fpstimer + 1.0:
    # print "FPS: ", fps
    fps = 0
    fpstimer = time.time()
