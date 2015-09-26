# PARTYLED
Party LED system in 020

# SETUP
* Regel een bak 12V analoge LED strips, een hele zooi transistors (# LED strips x 3), draad, een Raspberry Pi, een of meer Adafruit PCA9685 boards, en een dikke vette 12V-voeding (reken 11.5W per meter LED-strip)
* download current raspbian https://www.raspberrypi.org/downloads/raspbian/
* stop een 8GB microSD via een adapter in je macbook
* `diskutil list`
** zoek de identifier van de SD-kaart, bijv disk2 (verkeerde pakken is desastreus, check de size!)
* `diskutil unmountDisk diskX`
* `sudo dd if=yyyy-mm-dd-wheezy-raspbian.img of=/dev/diskX bs=2m`
* edit `/etc/network/interfaces` *on the SD card*, either via parallels, or by temporarily hooking the Pi up to LAN, `sudo nmap -sP 192.168.1.0/24` to find it, and ssh-ing in.
```
	auto lo
	iface lo inet loopback
	iface eth0 inet dhcp
	auto wlan0
	allow-hotplug wlan0
	iface wlan0 inet dhcp
	wpa-ssid "your-network-name"
	wpa-psk "password-here"
```
* `sudo nmap -sP 192.168.1.0/24` to find the pi.
* SSH in, and `sudo raspi-config`, expand filesystem and set timezone/local options
* update alles: `sudo apt-get update && sudo apt-get upgrade`
* `curl -sLS https://apt.adafruit.com/add | sudo bash` om Adafruit's readymade Pi-stuff aan apt toe te voegen
* `sudo apt-get install node`, dan `node -v` (moet minimaal 0.12 weergeven)
* I2C aanzetten: `sudo raspi-config`, Advanced options > I2C > Yes > Yes, quit raspi-config, `reboot`
  * evt: https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=97257
* `git clone https://github.com/Q42/partyled && cd partyled`
* `npm install adafruit-pca9685`
