# CasaEsperta - Home Assistant - [Google Assistant](https://www.home-assistant.io/integrations/google_assistant/)

I followed the linked guide, although there's some changes in the UI of Google side of things.

## Exposed entities
I choose which entities are exposed individually, insead of being by domain.

* vacuum.xauxau - Main floor robot vacuum
* climate.temperatura_da_sala - Sala's temperature
* climate.temperatura_da_suite - Suite's temperature
* climate.temperatura_da_cozinha - Cozinha's temperature
* climate.temperatura_da_cave - Cave's temperature
* fan.ventoinha_da_cave - Cave's ventilation fan
* climate.temperatura_do_terraco - Terraço's temperature
* all light entities

## Xiaomi temperature sensors

To expose these sensors as a temperature sensor to Google Assistant, we need to make a fake Thermostat with its data like explained in [this thread](https://community.home-assistant.io/t/google-assistant-working-with-sensors/51688). 

My sensors are exposed through Zigbee2Mqtt so I had to adapt the yaml from [this one](https://community.home-assistant.io/t/google-assistant-working-with-sensors/51688/46). A full config example:
```yaml
climate:
    platform: mqtt
    unique_id: "UUID"
    name: temperatura da cave
    qos: 1
    initial: 20
    availability_topic: "zigbee2mqtt/bridge/state"
    payload_available: "online"
    payload_not_available: "offline"
    current_temperature_topic: "zigbee2mqtt/temp_cave"
    temperature_state_topic: "zigbee2mqtt/temp_cave"
    current_temperature_template: "{{ value_json.temperature | round(1) }}"
    temperature_state_template: "{{ value_json.temperature | round(1) }}"
    temperature_command_topic: "void/hvac/temperature/set"
    mode_state_topic: "void/hvac/mode/state"
    mode_command_topic: "void/hvac/mode/set"
    modes:
    - "off"
    - "cool"
    - "heat"
```
We also needed to create an [automation](automations.md) to make sure that these fake climate entities are on "Heat" mode so Google only reports the temperature without extra information.

An adapted version of this was used to expose an mqtt switch that controls a ventilator as a fan to Google Assistant.
