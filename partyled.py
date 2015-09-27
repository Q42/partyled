#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
from threading import Timer
import time
import math

STRIPCOUNT = 10  # number of Q42 awesomeness 12V analog RGB LED strips
PWMSCALE = 4096  # fit in PWM bitdepth
GAMMA = 2.2      # gamma correction

# create globals for everything to prevent garbage collection from slowing down the show
pwm1 = PWM(0x40)
pwm2 = PWM(0x41)
fps = 0
fpstimer = 0
colors = [0] * STRIPCOUNT * 3

pwm1.setPWMFreq(400)

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

def generator_GrayscaleWave(dT, sC):
  for i in range(0, sC):
    colors[i*3 + 0] = 0.5 + 0.5 * math.sin(dT * 5000 + i * 1.6)
    colors[i*3 + 1] = 0.5 + 0.5 * math.sin(dT * 5000 + i * 1.6)
    colors[i*3 + 2] = 0.5 + 0.5 * math.sin(dT * 5000 + i * 1.6)

print "-----/ Q42 / partyLED /------"

while (True):
  generator_GrayscaleWave(time.time() / 1000, STRIPCOUNT)
  for i in range(0, STRIPCOUNT):
    setStripColor(i, colors[i*3], colors[i*3 + 1], colors[i*3 + 2])
  fps += 1
  if time.time() > fpstimer + 1.0:
    print "FPS: ", fps
    fps = 0
    fpstimer = time.time()

