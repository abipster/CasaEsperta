# CasaEsperta - Home Assistant - Integrations

* [Zigbee2Mqtt Assistant](https://github.com/yllibed/Zigbee2MqttAssistant) - GUI for Zigbee2Mqtt
Add the following repository url: `https://github.com/yllibed/hassio`

Configuration:
```yaml
settings:
  mqttserver: mqtt_ip
  mqttusername: mqtt_username
  mqttpassword: mqtt_password
```

* [TasmoAdmin](https://github.com/hassio-addons/addon-tasmoadmin) - Overview of Tasmota devices in the network
Configuration:
```yaml
ssl: false
certfile: fullchain.pem
keyfile: privkey.pem
```
Add the sidebar icon:
```yaml
panel_iframe:
  tasmoadmin:
    title: TasmoAdmin
    icon: mdi:lightbulb-on
    url: http://addres.to.your.hass.io:9541
```