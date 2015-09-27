// run with 'node test.js simulate' to ignore pwm libraries so you can develop on a macbook
var _sim = false; if(process.argv.length > 2 && process.argv[2] == 'simulate') _sim = true;

// constants
var STRIPCOUNT = 10; // number of LED strips connected to the system (Q020 target: 10)
var TARGETFPS = 1000;  // target FPS -- assumption is 60fps
var PWMSCALE = 4096; // 0..4095

var fpsCounter = 0;

if(!_sim)
{
  try {
    var PwmFactory1 = require("adafruit-pca9685");
    var PwmFactory2 = require("adafruit-pca9685");
  }
  catch(e) {
    console.log(e);
    console.log("\nCan't include PWM controller module:")
    console.log("* If you're on a raspberry pi, followup setup instructions")
    console.log("* If you're on a macbook, run with '" + process.argv[0] + " " + process.argv[1] + " simulate'\n")
    process.exit(0);
  }
  var pwm1 = new PwmFactory1({
      "freq": "400",   // high is good but low enough to prevent brightness/pwr issues
      "correctionFactor": "1.0", // finetuning
      "address": "0x40", // i2c bus
      "device": '/dev/i2c-1'
    });
  var pwm2 = new PwmFactory2({
      "freq": "400",   // high is good but low enough to prevent brightness/pwr issues
      "correctionFactor": "1.0", // finetuning
      "address": "0x41", // i2c bus
      "device": '/dev/i2c-1'
    });
}

// RGB values are 0..1 floats
// stripID is 0..number of strips-1
function StripSetOne(stripID, R, G, B) {
  if(_sim)
    console.log("setting strip " + stripID + " to ("+R+","+G+","+B+")");
  else
  {
    if(stripID < 5) {
      //console.log("setting strip 1:" + stripID + " to ("+R+","+G+","+B+")");
      pwm1.setPwm(stripID * 3,     0, PWMScale(R));
      pwm1.setPwm(stripID * 3 + 1, 0, PWMScale(G));
      pwm1.setPwm(stripID * 3 + 2, 0, PWMScale(B));
    } else {
      //console.log("setting strip 2:" + (stripID-5) + " to ("+R+","+G+","+B+")");
      pwm2.setPwm((stripID-5) * 3,     0, PWMScale(R));
      pwm2.setPwm((stripID-5) * 3 + 1, 0, PWMScale(G));
      pwm2.setPwm((stripID-5) * 3 + 2, 0, PWMScale(B));
    }
  }
}

// scales to PWM (from 0..1 to eg 0..4095)
// TODO gamma correction
function PWMScale(val) {
  var p = val * PWMSCALE;
  if (p < 0) p = 0;
  if (p > PWMSCALE-1) p = PWMSCALE-1;
  return p;
}

// set all LED strips at once
function StripSetAll(R, G, B) {
  for(i = 0; i < STRIPCOUNT; i++) StripSetOne(i, R, G, B);
}

// turn off LEDS when we exit for safety purposes
function SafeShutDown() {
  console.log("-- Shutdown")
  StripSetAll(0,0,0);
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
  console.log("watchdog tick: " + fpsCounter + " fps");
  fpsCounter = 0;
}

// this is the basic setup of a plugin
// in:  dT = timer (milliseconds)
//      sC = strip count
// out: should be a (stripcount * 3) array of either floats or [0..99] ints depending on PWM needs
function Update(dT, sC) {
  colors = [];
  for(i = 0; i < sC; i++) {
    // sine wave 0..1 that moves across the strips
    var r = 0.5 + 0.5 * Math.sin(dT / 200 + i * 1.6);
    var g = 0.5 + 0.5 * Math.sin(dT / 200 + i * 1.6);
    var b = 0.5 + 0.5 * Math.sin(dT / 200 + i * 1.6);
    colors.push(r);
    colors.push(g);
    colors.push(b);
  }
  return colors;
}

console.log("Q42 / PARTYLED / start");
// aim for 60 fps, TODO create reliable framerate method
// watchdog every second
setInterval(MainLoop, 1000/TARGETFPS);
setInterval(WatchDogTimer, 1000);
