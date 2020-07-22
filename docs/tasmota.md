# CasaEsperta - Tasmota

## Hardware

This is the hardware that I flashed with Tasmota:

* [Blitzwolf BW-SHP2](https://www.blitzwolf.com/3840W-EU-WIFI-Smart-Socket-p-244.html) - [How](https://tasmota.github.io/docs/devices/BlitzWolf-SHP2/)
* [Shelly 1](https://shelly.cloud/products/shelly-1-smart-home-automation-relay/) - [How](https://tasmota.github.io/docs/devices/Shelly-1/)
* Shelly 2 (discontinued) - [How](https://tasmota.github.io/docs/devices/Shelly-2/)
* [Magic Home Mini RGB RGBW Wifi Controller](https://pt.aliexpress.com/item/32791924935.html) - [How](https://tasmota.github.io/docs/devices/MagicHome-LED-strip-controller/)


## Flashing

We use [PlatformIO](https://platformio.org/) to flash the first version of Tasmota, built from source following [this guide](https://tasmota.github.io/docs/PlatformIO/).

Need to change some things to build and flash Tasmota with right settings:

Edit `platformio.ini` from the Tasmota source folder to set the right `upload_port`.

Edit `my_user_config.h` to configure your WiFi and timezone.


### Commands

* Set timezone and DSTs for Portugal
```
timezone 99
TimeDST 0,0,3,1,1,60
TimeSTD 0,0,10,1,2,0
```
