# CasaEsperta - [Shinobi](https://shinobi.video/)

Shinobi is a self-hosted CCTV solution. I had some problems with the Docker installation, so I installed it directly on the server.

Shinobi requires [MariaDB](docker_containers.md#mariadb) to be installed. My particular installation requires my External USB drive to be mounted as well.

Execute the script [init_shinobi.sql](../main_server/docker/shinobi/init_shinobi.sql) on your MariaDb instance.

After that, execute the install scriopt. As we already have an instance of MariaDB and want to configure some things before Shinobi starts, during the installation we choose to not install MariaDB nor start Shinobi at the end.
```
sudo su
bash <(curl -s https://gitlab.com/Shinobi-Systems/Shinobi-Installer/raw/master/shinobi-install.sh)     
```
After that:
```
cd /home/Shinobi
cp conf.json conf.json.bak
nano conf.json
```

Setup the file by changing the configurations you want. In my particular case, I want to add a secondary storage for the videos to be on my external usb drive, to change the running port, enable SMTP server on port 1025 and give my MariaDB server configurations.

There's an example file with only my changed configurations [here](../main_server/docker/shinobi/conf.json).

```
pm2 start camera.js && pm2 start cron.js
pm2 startup && pm2 save
```

If this doesn't work, set up a cron job to run 5 minutes after boot:
```
sudo su
crontab -e
```
Add this line:
```
@reboot /bin/sleep 300 && pm2 restart all
```

## Reverse Proxy
Although this is not a Docker container, we can instruct Traefik to reverse-proxy it.

Copy the content of [app-shinobi.toml](../main_server/docker/traefik/app-shinobi) to `~/docker/traefik/rules/app-shinobi.toml` and make sure to replace example.pt with your domain, SERVER_IP with your lan IP and SHINOBI_PORT with the running port of Shinobi. After saving the file, you only need to navigate to https://shinobi.example.pt/super.

## [MQTT](https://hub.shinobi.video/articles/view/xEMps3O4y4VEaYk)
You can enable MQTT triggers to alert other systems through MQTT if a motion is detected.

Edit `/home/Shinobi/conf.json` and add the following section:

```json
"mqtt": {
    "verbose": false,
    "url": "mqtt://localhost:1883",
    "mqtt_options": {
      "username": "USERNAME",
      "password": "PASSWORD" 
    },
    "topic": "shinobi",
    "filterplugs": ["body_terrace"],
    "toMqttMessage": {
      "key": "key",
      "name": "name",
      "details": "details",
      "currentTimestamp": "currentTimestamp",
      "plug": "plug",
      "name": "mon.name"
    },
    "triggerTopics": {
      "motionsensor/body_terrace/out": {
        "monitorid": "MONITOR_ID",
        "groupkey": "GROUPKEY"
      }
    }
}
```

Install the MQTT dependency:
```
sudo su
curl -o ./libs/customAutoLoad/mqtt.js https://gitlab.com/geerd/shinobi-mqtt/raw/master/mqtt.js
npm install mqtt
pm2 restart all
```



## How it works

TODO #2