# CasaEsperta - Home Assistant - [InfluxDB](https://www.home-assistant.io/integrations/influxdb/)

InfluxDB is running on a docker container on the Main Server.

Only data from [whitelisted](../../home_assistant/influxdb/) sensors are sent to InfluxDB.

## Retention Policies

* ### autogen
It's the default one where all data that comes from Home Assistant is written. 

Changed from infinite to 60 days:
```
ALTER RETENTION POLICY "autogen" ON "homeassistant" DURATION 60d REPLICATION 1 DEFAULT
```

* ### forever
Policy that will hold calculated aggregates "forever".
```
CREATE RETENTION POLICY "forever" ON "homeassistant" DURATION INF REPLICATION 1
```

## Continuous Queries

* ### cq_lights_5m_W
Power usage of all lights - 5m.

This CQ will record the mean of the power usage of all Tasmota devices that represent lights, grouped by periods of 5 minutes. Its data will be stored in autogen RP.
```
CREATE CONTINUOUS QUERY cq_lights_5m_W ON homeassistant
BEGIN
	SELECT mean(value) AS "value" INTO homeassistant.autogen.lights_5m_W FROM homeassistant.autogen.W WHERE ("entity_id"='lightbedroom_0_energy_power' OR "entity_id"='lightbedroom_1_energy_power' OR "entity_id"='lightkitchen_energy_power' OR "entity_id"='lightpatio_energy_power' OR "entity_id"='lightsmallroom_1_energy_power' OR "entity_id"='lightswc_0_energy_power' OR "entity_id"='lightterrace_energy_power' OR "entity_id"='lightup_energy_power' OR "entity_id"='lightwc_1_energy_power') GROUP BY time(5m), entity_id fill(previous)
END
```

* ### cq_lights_10m_KWh
Energy consumption of all lights - 10m.

This CQ will record the last readings of "today" of all Tasmota devices that represent lights, grouped by periods of 10 minutes. This CQ will allow to correctly sum all the values into a single reading that represent consumption of lighting in the house. Its data will be stored in autogen RP.
```
CREATE CONTINUOUS QUERY cq_lights_10m_KWh ON homeassistant
BEGIN 
	SELECT last(value) AS "value" INTO homeassistant.autogen.lights_10m_KWh FROM homeassistant.autogen.kWh WHERE (entity_id = 'lightbedroom_0_energy_today' OR entity_id = 'lightbedroom_1_energy_today' OR entity_id = 'lightkitchen_energy_today' OR entity_id = 'lightpatio_energy_today' OR entity_id = 'lightsmallroom_1_energy_today' OR entity_id = 'lightswc_0_energy_today' OR entity_id = 'lightterrace_energy_today' OR entity_id = 'lightup_energy_today' OR entity_id = 'lightwc_1_energy_today') GROUP BY time(10m), entity_id fill(previous)
END
```

* ### cq_lights_6h_KWh
The same objective as above CQ, but this time grouped by periods of 6 hours and stored in forever RP.
```
CREATE CONTINUOUS QUERY cq_lights_6h_KWh ON homeassistant
BEGIN
	SELECT last(value) AS "value" INTO homeassistant.forever.lights_6h_KWh FROM homeassistant.autogen.kWh WHERE (entity_id = 'lightbedroom_0_energy_today' OR entity_id = 'lightbedroom_1_energy_today' OR entity_id = 'lightkitchen_energy_today' OR entity_id = 'lightpatio_energy_today' OR entity_id = 'lightsmallroom_1_energy_today' OR entity_id = 'lightswc_0_energy_today' OR entity_id = 'lightterrace_energy_today' OR entity_id = 'lightup_energy_today' OR entity_id = 'lightwc_1_energy_today') GROUP BY time(1h), entity_id fill(previous)
END
```

* ### cq_power_today_6h_KWh
Energy consumption of each energy meter plug - 6h.

CQ to store power consumption of each plug grouped by 6h in the forever RP.
```
CREATE CONTINUOUS QUERY cq_power_today_6h_KWh ON homeassistant
BEGIN
	SELECT mean(value) AS "value" INTO homeassistant.forever.power_today_6h_KWh FROM homeassistant.autogen.kWh WHERE (entity_id = 'atiplug_energy_today' OR entity_id = 'fridgeplug_energy_today' OR entity_id = 'mediacenterplug_energy_today' OR entity_id = 'pcplug_energy_today' OR entity_id = 'ritaofficeplug_energy_today' OR entity_id = 'serverplug_energy_today' OR entity_id = 'washingmachineplug_energy_today' OR entity_id = 'waterheaterplug_energy_today') GROUP BY time(6h), entity_id fill(previous)
END
```

* ### cq_temperature_6h_C
Temperatures - 6h.

CQ to store temperature readings grouped by 6h in the forever RP.
```
CREATE CONTINUOUS QUERY cq_temperature_6h_C ON homeassistant
BEGIN
	SELECT mean(value) AS "value" INTO homeassistant.forever.temperature_6h_C FROM homeassistant.autogen."°C" WHERE (entity_id = 'temp_cave_temperature' OR entity_id = 'temp_cozinha_temperature' OR entity_id = 'temp_exterior_temperature' OR entity_id = 'temp_sala_temperature' OR entity_id = 'temp_suite_temperature') GROUP BY time(6h), entity_id fill(previous)
END
```

* ### cq_humidity_6h_%
Humidity - 6h.

CQ to store humidity readings grouped by 6h in the forever RP.
```
CREATE CONTINUOUS QUERY "cq_humidity_6h_%" ON homeassistant 
BEGIN
	SELECT mean(value) AS "value" INTO homeassistant.forever."humidity_6h_%" FROM homeassistant.autogen."%" WHERE (entity_id = 'temp_cave_humidity' OR entity_id = 'temp_cozinha_humidity' OR entity_id = 'temp_exterior_humidity' OR entity_id = 'temp_sala_humidity' OR entity_id = 'temp_suite_humidity') GROUP BY time(6h), entity_id fill(previous)
END
```