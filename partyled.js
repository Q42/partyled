// run with 'node test.js simulate' to ignore pwm libraries so you can develop on a macbook
var _sim = false; if(process.argv.length > 2 && process.argv[2] == 'simulate') _sim = true;

// constants
var STRIPCOUNT = 2; // number of LED strips connected to the system (Q020 target: 10)
var TARGETFPS = 2;  // target FPS -- assumption is 60fps
var PWMSCALE = 4096; // 0..4095

var fpsCounter = 0;

if(!_sim)
{
  try {
    var PwmFactory = require("adafruit-pca9685");
  }
  catch(e) {
    console.log(e);
    console.log("\nCan't include PWM controller module:")
    console.log("* If you're on a raspberry pi, followup setup instructions")
    console.log("* If you're on a macbook, run with '" + process.argv[0] + " " + process.argv[1] + " simulate'\n")
    process.exit(0);
  }
  var pwm = PwmFactory( {
      "freq": "50",   // frequency of the device
      "correctionFactor": "1.0", // correction factor - fine tune the frequency
      "address": "0x40", // i2c bus address
      "device": '/dev/i2c-1' // device name
    });
}

// RGB are 0..1
// stripID is 0..number of strips
function StripSetOne(stripID, R, G, B) {
  if(_sim)
    console.log("setting strip " + stripID + " to ("+R+","+G+","+B+")");
  else
  {
    pwm.setPwm(stripID * 3,     R * PWMSCALE, 0);
    pwm.setPwm(stripID * 3 + 1, G * PWMSCALE, 0);
    pwm.setPwm(stripID * 3 + 2, B * PWMSCALE, 0);
  }
}

// set all LED strips at once
function StripSetAll(R, G, B) {
  for(i = 0; i < STRIPCOUNT; i++) StripSetOne(i, R, G, B);
}

// turn off LEDS when we exit for safety purposes
function SafeShutDown() {
  console.log("Initiate shutdown")
  PwmSetAll(0,0,0);
  process.exit(0);
}
process.on('SIGINT', SafeShutDown);
process.on('SIGTERM', SafeShutDown);

// the mainloop functions like a gameloop
function MainLoop() {
  var d = Date.now(); //millis since epoch
  fpsCounter++;
  var c = Update(d, STRIPCOUNT);
  for(i=0; i < STRIPCOUNT; i++)
    StripSetOne(i, c[i*3], c[i*3+1], c[i*3+2]);
}

// watchdog check fps etc
function WatchDogTimer() {
  if(_sim) {
    console.log("watchdog tick: " + fpsCounter + " fps");
    fpsCounter = 0;
  }
}

// this is the basic setup of a plugin
// in:  timer (milliseconds), strip count
// out: should be a (stripcount * 3) array of either floats or [0..99] ints depending on PWM needs
function Update(dT, sC) {
  brightness = 0.75 + 0.25 * Math.sin(dT / 1000);
  colors = [];
  for(i = 0; i < sC; i++) {
    colors.push(brightness);
    colors.push(brightness);
    colors.push(0);
  }
  return colors;
}

// aim for 60 fps, TODO create reliable framerate method
// watchdog every second
setInterval(MainLoop, 1000/TARGETFPS);
setInterval(WatchDogTimer, 1000);
