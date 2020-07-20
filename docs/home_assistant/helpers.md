# CasaEsperta - Home Assistant Helpers

This document will have tips and rules regarding how the configuration is structured.

## Includes
Explain the different methods to include files and folders in Home Assistant's configuration. This is adapted from [Frenck's Gist](https://gist.github.com/frenck/20a3236cf64bf5bbcb907ecc7cf665cd)

```yaml
# Single include on the spot, result is the content of the file as is
first: !include file.yaml

# Each file is an item in the list, result is a LIST!
second: !include_dir_list ./second

# All files merged into one big list (files MUST contain a list), result is a LIST!
third: !include_dir_merge_list ./third

# Merge all files into a directory using the filename as the key. Result is a DICTIONARY!
fourth: !include_dir_named ./fourth

# Merge contents of all files. Result is a DICTIONARY!
fifth: !include_dir_merge_named ./fifth
```

## MariaDB recorder
This is a script to create a user and a databse on a MariaDB instance, to be used with the Recorder.

```SQL
CREATE USER 'USER' IDENTIFIED by 'PASSWORD';
CREATE DATABASE IF NOT EXISTS homeassistant;
GRANT ALL PRIVILEGES ON `homeassistant%`.* TO 'USER';
FLUSH PRIVILEGES;
```

## Shelly2Led MQTT

To control the bulb with a simple on-off switch functionality, use:
```
shellies/shelly2led-<deviceid>/color/0/command
shellies/shelly2led-<deviceid>/color/1/command
```
accepts on and off payloads.

Device report its current on-off state: 
```
shellies/shelly2led-<deviceid>/color/0
shellies/shelly2led-<deviceid>/color/1 
```

For controlling other paramters of the LED channels publish to :
```
shellies/shelly2led-<deviceid>/color/0/set
shellies/shelly2led-<deviceid>/color/1/set
```
Device expects a JSON payload on this topic, with the following sample 
```json
contents:
{
    brightness:<value 0-100>,
    turn:"on"|"off",
}
```
An identical JSON payload will be published by Shelly2LED on :
```
shellies/shelly2led-<deviceid>/color/0/status
shellies/shelly2led-<deviceid>/color/1/status
```
