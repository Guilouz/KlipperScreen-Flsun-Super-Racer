# KlipperScreen for FLSUN Super Racer

![maxresdefault](https://user-images.githubusercontent.com/12702322/187098254-be0a0182-cc04-401a-9e95-97dda4bdb1b6.jpeg)

KlipperScreen is a touchscreen GUI that interfaces with [Klipper](https://github.com/kevinOConnor/klipper) via [Moonraker](https://github.com/arksine/moonraker). It can switch between multiple printers to access them from a single location, and it doesn't even need to run on the same host, you can install it on another device and configure the IP address to access the printer.

### Documentation [![Documentation Status](https://readthedocs.org/projects/klipperscreen/badge/?version=latest)](https://klipperscreen.readthedocs.io/en/latest/?badge=latest)

[Click here to access the documentation.](https://klipperscreen.readthedocs.io/en/latest/)

<br />

## About

This version of KlipperScreen is compatible with FLSUN Super Racer, it's optimized for Delta printers.

- Latest build of KlipperScreen
- Improved Z-Offset Calibration menu
- Added support for Endstops Phase Calibration
- Some fixes and adjustments

Klipper Configuration for Super Racer is also available here: [Klipper-Flsun-Super-Racer](https://github.com/Guilouz/Klipper-Flsun-Super-Racer)

<br />

If you like my work, don't hesitate to support me by paying me a 🍺 or a ☕. Thank you 🙂

[ ![Download](https://user-images.githubusercontent.com/12702322/115148445-e5a40100-a05f-11eb-8552-c1f5d4355987.png) ](https://www.paypal.me/CyrilGuislain)

<br />

## Installation

- Make sure previous installation of KlipperScreen is removed (with Kiauh).
- In SSH, enter the following commands (one at a time) to install KlipperScreen:
```
git clone https://github.com/Guilouz/KlipperScreen-Flsun-Super-Racer.git
sudo mv /home/pi/KlipperScreen-Flsun-Super-Racer /home/pi/KlipperScreen
cd ~/KlipperScreen
./scripts/KlipperScreen-install.sh
```
Note: Installation may take several minutes.

- Go to your Mainsail Web interface then select the `Machine` tab.
- Open the `moonraker.conf` file and modify the `[update_manager KlipperScreen]` section  as follows:

```
[update_manager KlipperScreen]
type: git_repo
path: /home/pi/KlipperScreen
origin: https://github.com/Guilouz/KlipperScreen-Flsun-Super-Racer.git
env: /home/pi/.KlipperScreen-env/bin/python
requirements: scripts/KlipperScreen-requirements.txt
install_script: scripts/KlipperScreen-install.sh
```
- Once done, click on `SAVE & RESTART` at the top right to save the file.
- You can now click the refresh button (still in the Machine tab) on the `Update Manager` tile.
- You will see a new KlipperScreen update appear, if you see a ⚠️DIRTY update, just select `Hard Recovery` to update.

![Update Manager](https://user-images.githubusercontent.com/12702322/183909392-24aab778-c8ed-4f81-be39-ac51612bf12c.jpg)

- Once installed you will have the new version of KlipperScreen and future updates will point directly to my repo like this:

![Update](https://user-images.githubusercontent.com/12702322/183990132-0a7673d1-2e51-484a-8113-e0bd54813995.jpg)

<br />

## Restoration

- Make sure previous installation of KlipperScreen is removed (with Kiauh).
- In SSH, enter the following commands (one at a time) to install KlipperScreen:
```
git clone https://github.com/jordanruthe/KlipperScreen.git
cd ~/KlipperScreen
./scripts/KlipperScreen-install.sh
```
Note: Installation may take several minutes.

- Go to your Mainsail Web interface then select the `Machine` tab.
- Open the `moonraker.conf` file and modify the `[update_manager KlipperScreen]` section  as follows:

```
[update_manager KlipperScreen]
type: git_repo
path: ~/KlipperScreen
origin: https://github.com/jordanruthe/KlipperScreen.git
env: ~/.KlipperScreen-env/bin/python
requirements: scripts/KlipperScreen-requirements.txt
install_script: scripts/KlipperScreen-install.sh
```

<br />

## Notes

My Macros for Super Racer can be found here : [macros.cfg](https://github.com/Guilouz/Klipper-Flsun-Super-Racer-Manta-M4P/blob/main/Configurations/macros.cfg)

- Calibrations Menu use the following Macros:

  - `Z Calibrate` function use `[gcode_macro Z_OFFSET_CALIBRATION]`
  - `Endstops Calibrate` function use `[gcode_macro ENDSTOPS_CALIBRATION]`
  - `Calibrate` function use `[gcode_macro DELTA_CALIBRATION]`
  - `Bed Mesh` function use `[gcode_macro BED_LEVELING]`

<br />

- To use `M600` Macro, you need to change `[filament_switch_sensor filament_sensor]` section in your `printer.cfg` file like this:
```
[filament_switch_sensor filament_sensor]
pause_on_runout: True
runout_gcode: M600
...
```

<br />

- To have screen notifications, add this in your `printer.cfg` file:
```
[respond]
```

<br />

- To use Endstops Calibrate function, it's needed to have this in your `printer.cfg` file:
```
[endstop_phase stepper_a]
endstop_align_zero: false

[endstop_phase stepper_b]
endstop_align_zero: false

[endstop_phase stepper_c]
endstop_align_zero: false
```

<br />

## Changelog

- 04/01/2023 : Use now official Z Calibrate
- 13/12/2022 : Latest KlipperScreen commits
- 06/12/2022 : Latest KlipperScreen commits
- 04/12/2022 : Latest KlipperScreen commits
- 03/12/2022 : Latest KlipperScreen commits
- 27/11/2022 : Latest KlipperScreen commits / Improvements
- 24/11/2022 : Latest KlipperScreen commits
- 23/11/2022 : Latest KlipperScreen commits / Fixed Reprint button when print is cancelling
- 21/11/2022 : Latest KlipperScreen commits
- 18/11/2022 : Latest KlipperScreen commits / Added possibility to reset Z-Offset on Z Calibration menu
- 09/11/2022 : Latest KlipperScreen commits
- 04/11/2022 : Latest KlipperScreen commits
- 29/10/2022 : Latest KlipperScreen commits
- 25/10/2022 : Added searching KlipperScreen.conf file in new directories
- 16/10/2022 : Latest KlipperScreen commits
- 08/10/2022 : Fixed heaters not showing their respective power percentages
- 04/10/2022 : Latest KlipperScreen commits
- 23/09/2022 : Added layers on Job Status Screen
- 18/09/2022 : Added support for bed mesh profiles and bed mesh visualization
- 11/09/2022 : Added settings to Show Heater Power
- 10/09/2022 : Some menus now use Macros
- 05/09/2022 : Updated to latest KlipperScreen v0.2.6
- 03/09/2022 : Improvements
- 29/08/2022 : First release
