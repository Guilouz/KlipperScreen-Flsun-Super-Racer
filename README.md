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

- Go to your Mainsail Web interface then select the `Machine` tab.
- Right-click on the `moonraker.conf` file then `Download` to make a backup of the original file. Keep this file carefully for possible backtracking.
- Now, still on Mainsail, open the `moonraker.conf` file and modify the `[update_manager KlipperScreen]` section  as follows:

```
[update_manager KlipperScreen]
type: git_repo
path: /home/pi/KlipperScreen
origin: https://github.com/Guilouz/KlipperScreen-Flsun-Super-Racer.git
env: /home/pi/.KlipperScreen-env/bin/python
requirements: scripts/KlipperScreen-requirements.txt
install_script: scripts/KlipperScreen-install.sh
```
- Once done, click on `SAVE & CLOSE` at the top right to save the file.
- You can now click the refresh button (still in the Machine tab) on the `Update Manager` tile.
- You will see a new KlipperScreen update appear, if you see a ⚠️DIRTY update, just select `Hard Recovery` to update.

![Update Manager](https://user-images.githubusercontent.com/12702322/183909392-24aab778-c8ed-4f81-be39-ac51612bf12c.jpg)

- Once installed you will have the new version of KlipperScreen and future updates will point directly to my repo like this:

![Update](https://user-images.githubusercontent.com/12702322/183990132-0a7673d1-2e51-484a-8113-e0bd54813995.jpg)

<br />

## Restoration

- If you want to go back to the official version, you can simply restore the previously downloaded `moonraker.conf` file or re-edit the `[update_manager KlipperScreen]` section and click the refresh button on the `Update Manager` tile:

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

Calibrations Menu use the following Macros:

- `Endstops Calibrate` function use `[gcode_macro ENDSTOPS_CALIBRATION]`
- `Calibrate` function use `[gcode_macro DELTA_CALIBRATION]`
- `Bed Mesh` function use `[gcode_macro BED_LEVELING]`
- `Move Z0` function in `Z Calibrate` menu use `[gcode_macro MOVE_TO_Z0]`

<br />

This version of KlipperScreen must be used with this Macros to save Z-Offset in real time:
```
[gcode_macro SET_GCODE_OFFSET]
description: Save Z-Offset value
rename_existing: _SET_GCODE_OFFSET
gcode:
  {% if printer.save_variables.variables.gcode_offsets %}
  {% set offsets = printer.save_variables.variables.gcode_offsets %}
  {% else %}
  {% set offsets = {'x': None,'y': None,'z': None} %}
  {% endif %}
  {% set ns = namespace(offsets={'x': offsets.x,'y': offsets.y,'z': offsets.z}) %}
  _SET_GCODE_OFFSET {% for p in params %}{'%s=%s '% (p, params[p])}{% endfor %}
  {%if 'X' in params %}{% set null = ns.offsets.update({'x': params.X}) %}{% endif %}
  {%if 'Y' in params %}{% set null = ns.offsets.update({'y': params.Y}) %}{% endif %}
  {%if 'Z' in params %}{% set null = ns.offsets.update({'z': params.Z}) %}{% endif %}
  {%if 'Z_ADJUST' in params %}
  {%if ns.offsets.z == None %}{% set null = ns.offsets.update({'z': 0}) %}{% endif %}
  {% set null = ns.offsets.update({'z': (ns.offsets.z | float) + (params.Z_ADJUST | float)}) %}
  {% endif %}
  SAVE_VARIABLE VARIABLE=gcode_offsets VALUE="{ns.offsets}"
```
```
[delayed_gcode LOAD_GCODE_OFFSETS]
initial_duration: 2
gcode:
  {% if printer.save_variables.variables.gcode_offsets %}
  {% set offsets = printer.save_variables.variables.gcode_offsets %}
  _SET_GCODE_OFFSET {% for axis, offset in offsets.items() if offsets[axis] %}{ "%s=%s " % (axis, offset) }{% endfor %}
  { action_respond_info("Loaded gcode offsets from saved variables [%s]" % (offsets)) }
  {% endif %}
```
<br />

## Changelog

- 11/09/2022 : Added settings to Show Heater Power
- 10/09/2022 : Some menus now use Macros
- 05/09/2022 : Updated to latest KlipperScreen v0.2.6
- 03/09/2022 : Improvements
- 29/08/2022 : First release
