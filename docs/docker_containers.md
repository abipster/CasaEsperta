# CasaEsperta - Docker Containers

## What's included

Here are the containers included in the full compose file. There's specific guides for some of them, so check the list out!

Start at Traefik's guide [here](traefik.md).

---------------------------------------------------
|   | Service | Endpoint | Description | Required 
| - | ------- |--------- | ----------- | -------- 
| 1 | [Traefik](Traefik.md) | https://traefik.example.pt | Automatic reverse proxy with dashboard, automatic SSL certificate generation and Google OAuth | Yes
| 2 | [Google OAuth](Traefik.md#oauth-container) | N/A | Authenticate your services with a Google Account | Recommended
| 3 | [Docker CloudFlare DDNS](Traefik.md#ddns-companion-containers) | N/A | Updates your Cloudflare domain with your external IP when it changes | Recommended with Cloudflare and dynamic IP
| 4 | [Traefik Cloudflare Companion](Traefik.md#ddns-companion-containers) | N/A | Updates your Cloudflare CNames with each new Docker container | Recommended with Cloudflare until you settle your containers
| 5 | [DuckDNS](Traefik.md#ddns-companion-containers) | N/A | Updates your DuckDNS domain with your external IP when it changes | Recommended with DuckDNS and dynamic IP
| 6 | [Ouroboros](#ouroboros) | N/A | Automatically update your running Docker containers to the latest available image that matches its tag | No
| 7 | [Dozzle](https://github.com/amir20/dozzle) | https://logs.example.pt | Web interface to monitor Docker logs | No
| 8 | [Portainer](https://www.portainer.io/) | https://portainer.example.pt | Web interface to manage Docker containers | Recommended
| 9 | [Unifi Controller](https://www.ui.com/software/) | https://unifi.example.pt | Web interface to manage your Unifi network | Only if you have an Unifi network without a Cloud key
| 10 | [Netdata](https://github.com/netdata/netdata) | https://netadata.example.pt | Real-time performance monitoring | No
| 11 | [MariaDB](#mariadb) | N/A | Relational Database | Yes if you want to use Shinobi, Guacamole or Filerun
| 12 | [phpMyAdmin](https://www.phpmyadmin.net/) | https://pma.example.pt | MariaDB Database Management  | Recommended with MariaDB
| 13 | [InfluxDB](https://www.influxdata.com/products/influxdb-overview/) | N/A | Time series database  | No
| 14 | [Chronograf](https://www.influxdata.com/time-series-platform/chronograf/) | https://chrono.example.pt | Interface for InfluxDB  | Recommended with InfluxDB
| 15 | [Grafana](#grafana) | https://grafana.example.pt | Time series data visualization  | Recommended with InfluxDB
| 16 | [Organizr](organizr.md) | https://example.pt | Server Frontpage | Recommended
| 17 | [Guacamole](#guacamole) | https://guac.example.pt | HTML 5 clientless remote desktop gateway | No
| 18 | [Filerun](#filerun) | https://filerun.example.pt | Self-hosted file sharing and explorer | No
| 19 | [qBittorrent](#download-containers) | https://qbit.example.pt | Torrent downloader | Yes with Radarr or Sonarr
| 20 | [jackett](https://github.com/Jackett/Jackett) | https://jackett.example.pt | Torrent site indexer | Yes with Radarr or Sonarr
| 21 | [Radarr](#download-containers) | https://radarr.example.pt | Movie download and collection management | No
| 22 | [Sonarr](#download-containers) | https://sonarr.example.pt | TV Show download and collection management | No
| 23 | [Plex Media Server](#plex-media-server) | https://plex.example.pt | Client–server media player system | No
| 24 | [Kitana](#kitana) | https://kitana.example.pt | Frontend UI for Plex 's SubZero plugin | Recommended with Plex
| 25 | [Tautulli](https://tautulli.com/) | https://tautulli.example.pt | Plex Media Server monitoring | No
| 26 | [Mosquitto](#mosquitto) | N/A | MQTT Server | No


## Add containers

After having successfully deployed Traefik with oauth authentication, it's time to add more containers to your system.

If you're using Cloudflare, it's recommended for you to pause its features and turn on "Development mode" on Cloudflare. This way Cloudflare's cache will be disabled and won't affect what you see.

Replace `~/docker/compose.yml` with the content of [full_compose.yml](../main_server/docker/full_compose.yml).

I recommend to comment all the containers that weren't already installed (starts at ouroboros on the file) and uncommenting one or a few at the time, to separate new deploys from one another. For every container installed, you should check the above table or the below sections to see if it has any special instructions or configuration keys that you need to set.

Follow the table above starting at item number 6 (Ouroboros).

### [Ouroboros](https://github.com/pyouroboros/ouroboros)
Not much to say about this container apart from the `IGNORE` environment configuration. This represents the names of the containers you want to exclude from automatic updates. May it be because they are self-managed like Home Assistant Supervised instalation or because they will break or delete some configurations when they are recreated.

### [MariaDB](https://mariadb.org/)
This container should have a static IP in the range of the subnet we created.

Make sure that this key have a valid value on your `~/docker/.env` file:
- SERVER_PASSWORD - Password for the MySQL root user. If you're not comfortable having the same internal passwords for multiple services, you can create new keys and replace them in the `~/docker/compose.yml` file.

Optionally, you can instal a MySQL client on your host
```
sudo apt install mysql-client -y
```
Then, to connect with the database
```
mysql -h 192.168.50.250 -u root -p
```

### [Grafana](https://grafana.com/)
The default user/pass is admin/admin

### [Guacamole](https://guacamole.apache.org/)
Guacamole is in reality two separate containers and both are needed for the application to run.
It also depends on [MariaDB](#mariadb) to be installed.

Guacamole has a special middleware label for Traefik: `traefik.http.middlewares.add-guacamole.addPrefix.prefix=/guacamole`. This is because the default URL for the frontpage of Guacamole is https://guac.example.pt/guacamole and we don't want to have to write the /guacamole part. This middleware does that for us and we only have to got to https://guac.example.pt/ to open the main page.

Create the database and its user. If you installed phpMyAdmin, open it and execute the script [prep_guacamole.sql](../main_server/docker/guacamole/prep_guacamole.sql). Alternatively you can connect with the terminal client
```
mysql -h 192.168.50.250 -u root -p
```
And execute the commands that are in the script [prep_guacamole.sql](../main_server/docker/guacamole/prep_guacamole.sql) directly on the terminal.

After that, execute the script  [init_guacamoledb.sql](../main_server/docker/guacamole/init_guacamoledb.sql).

The default user/pass is guacadmin/guacadmin.

### [Filerun](https://www.filerun.com/)
This container also depends on [MariaDB](#mariadb) to be installed.

We need to create the database and its user. The steps are the same as explained in the [Guacamole](#guacamole) section. You need to execute the script [prep_filerun.sql](../main_server/docker/guacamole/prep_filerun.sql) 

Make sure that these keys have valid values on your `~/docker/.env` file:
- NAS_GROUP - Name of the linux group with access to the folders and files you'll want to expose
- NAS_GROUPID - ID of the linux group with access to the folders and files you'll want to expose
- DATA_DIR - The root folder that will be exposed by Filerun

The default user/pass is superuser/superuser.

### Download Containers
This section is related with the media download services: qBittorrent, Jackett, Sonarr and Radarr.

If you want to manage your downloads yourself, you don't need Jacket/Sonarr/Radarr.

For a guide on how to integrate these containers with one another, go watch a guide like [this one](https://www.youtube.com/watch?v=DQIGUmWxBX8).
As a quick reference: 
- Use http://contaner_name:container_port to reference other services
- Add torrent indexers to Jackett (choose all the public ones you know from the list)
- Add a tornzab indexer to Radarr and Sonarr and connect it to Jackett
- Add a downloader to Radarr and Sonarr and connect it to qBittorrent

You can use the following format to link containers: `http://container_name:container_port` becausr they all share the same network and their names can be resolved that way.

- #### [qBittorrent](https://www.qbittorrent.org/)
Make sure that these keys have valid values on your `~/docker/.env` file:
- DOWNLOADS_DIR - path to the folder where complete downloads will go
- TORRENTS_DIR - path to the black-hole folder 

- #### [Radarr](https://radarr.video/)
Make sure that this key have a valid value on your `~/docker/.env` file:
- MOVIES_DIR - path to the folder where the movies are

- #### [Sonarr](https://sonarr.tv/)
Make sure that this key have a valid value on your `~/docker/.env` file:
- SERIES_DIR - path to the folder where the tv shows are

As a reference, the categories to configure for the Jackett indexer are:
5000,5010,5040,5050,5070,5080

### [Plex Media Server](https://plex.tv)
You need to have an account with https://plex.tv. 

Then get a claim token here: https://plex.tv/claim. You'll have only 4 minutes from claiming the token until you spin up the container, so claim it only when ready.

Make sure that this key have a valid value on your `~/docker/.env` file:
- PLEX_CLAIM - The token you got from https://plex.tv/claim

### [Kitana](https://github.com/pannal/Kitana)
First you need to install and configure Sub-Zero plugin in your Plex media server. For those guides, you can read [here](https://github.com/pannal/Sub-Zero.bundle/wiki)

### [Mosquitto](https://mosquitto.org/)
This guide assumes there's already a pwfile generated before. If you don't have a pwfile nor a running instance of Mosquitto to generate one, you might need to deploy without authentication and follow a guide like [this one](http://www.steves-internet-guide.com/mqtt-username-password-example/) to setup the authentication after.

Copy [mosquitto.conf](../main_server/docker/mosquitto/mosquitto.conf) and the pwfile to `~/docker/mosquitto/config/` 
Run
```
touch ~/docker/mosquitto/log/mosquitto.log
```