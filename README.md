# PARTYLED
Party LED system in 020

# SETUP
* Regel een bak 12V analoge LED strips, een hele zooi transistors (# LED strips x 3), draad, een Raspberry Pi, een of meer Adafruit PCA9685 boards, en een dikke vette 12V-voeding (reken 11.5W per meter LED-strip)
  * transistors: TO220 darlingtons, met heatsinks(!) anders worden ze te heet
  * soldeer alles met solid core wire, anders smelt de boel
  * gebruik een ouwe PC-voeding als relatief goedkope +12V-voeding voor 300+ W. Pak alle gele kabeltjes bij elkaar, die zijn allemaal +12V, en zwarte kabeltjes voor GND. Soldeer ze samen of verdeel ze over de outputs om te voorkomen dat er teveel stroom op één kabeltje komt te staan.
  * haal uit diezelfde voeding de +5V voor de Raspberry Pi, door een micro USB cable door te knippen en de +5V/GND kabeltjes te connecten (bij zowel ATX als USB is +5V een rode kabel, GND is zwart)
* download current raspbian https://www.raspberrypi.org/downloads/raspbian/
* stop een 8GB microSD via een adapter in je macbook
* `diskutil list`, zoek de identifier van de SD-kaart, bijv disk2 (verkeerde pakken is desastreus, check de size!)
* `diskutil unmountDisk diskX`
* `sudo dd if=yyyy-mm-dd-wheezy-raspbian.img of=/dev/diskX bs=2m`
* Voor wifi ipv LAN: edit `/etc/network/interfaces` *op de SD-kaart* door tijdelijk op LAN aan te sluiten en in te SSH-en.
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
* `sudo nmap -sP 192.168.1.0/24` om de pi te vinden.
* SSH in, and `sudo raspi-config`, expand filesystem en set timezone/local options
* update alles: `sudo apt-get update && sudo apt-get upgrade`
* sudo apt-get install git
* `curl -sLS https://apt.adafruit.com/add | sudo bash` om Adafruit's readymade Pi-stuff aan apt toe te voegen
* `sudo apt-get install node`, dan `node -v`
* I2C aanzetten:
  * `sudo apt-get install python-smbus`
  * `sudo apt-get install i2c-tools`
  * `sudo nano /etc/modules` en zorg ervoor dat `i2c-bcm2708` en `i2c-dev` erin staan
  * `sudo raspi-config`, Advanced options: zet I2C aan (en op boot) en zet Device Tree uit. Reboot.
  * checken: `sudo i2cdetect -y 1` moet geen error teruggeven
* I2C speedup: sneller maken baudrate van 100Kpbs naar 1.2Mbps
  * `sudo nano /boot/config.txt`:
```
    device_tree=bcm2708-rpi-b-plus.dtb
    device_tree_param=i2c_arm=on,i2c_arm_baudrate=1200000
    device_tree_param=i2c1=on,i2c1_baudrate=1200000
```
  * check dat het sneller is: `sudo reboot` en dan `dmesg|grep baudrate` moet 1200000 laten zien
* `git clone https://github.com/Q42/partyled && cd partyled`
* `nohup python partyled.py &`
