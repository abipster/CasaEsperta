# CasaEsperta - Home Assistant - [Google Assistant](https://www.home-assistant.io/integrations/google_assistant/)

I followed the linked guide, although there's some changes in the UI of Google side of things.

## Exposed entities
I choose which entities are exposed individually, insead of being by domain.

* vacuum.xauxau - Main floor robot vacuum
* light.sala_sofa - Lights above the couch
* climate.temperatura_da_sala - Sala's temperature
* climate.temperatura_da_suite - Suite's temperature
* light.cozinha_led - Kitchen's led strip
* light.cozinha_mesa - Kitchen table's light
* light.cozinha_patio - Patio's light 
* light.cozinha_teto - Kitchen ceiling's light
* climate.temperatura_da_cozinha - Cozinha's temperature
* climate.temperatura_da_cave - Cave's temperature
* fan.ventoinha_da_cave - Cave's ventilation fan
* light.cave_detolf_led - Cave's vitrines's led strip
* light.cave_teto - Cave's ceiling light
* climate.temperatura_do_terraco - Terraço's temperature
* light.casa_banho_espelho - Bathrooms's mirror light
* light.casa_banho_teto - Bathrooms's ceiling light
* light.quarto_cama_direita - Right side of bedroom's bed
* light.quarto_teto - Bedroom's ceiling light


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
