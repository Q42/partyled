
/*
var PwmFactory=require("adafruit-pca9685");

var pwm = PwmFactory( {
    "freq": "50",   // frequency of the device
    "correctionFactor": "1.0", // correction factor - fine tune the frequency
    "address": "0x40", // i2c bus address
    "device": '/dev/i2c-1' // device name
  });
*/

var fpsCounter = 0;

// TODO catch SIGINT etc to turn off light when we are forced to exit

function MainLoop() {
  var d = Date.now(); //returns millis since epoch
  fpsCounter++;
  var c = Update(d);
  //pwm.setPwm(0, c, 0);
}

function WatchDogTimer() {
  console.log("watchdog tick: " + fpsCounter + " fps");
  fpsCounter = 0;
}

// in:  timer (milliseconds)
// out: should be a (strips * 3) array of either floats or [0..99] ints depending on PWM needs
function Update(dT) {
  brightness = 0.75 + 0.25 * Math.sin(dT / 1000);
  return brightness;
}

// aim for 60 fps
// TODO fix to a steady framerate
setInterval(MainLoop, 1000/60);

// watchdog every second
setInterval(WatchDogTimer, 1000);
