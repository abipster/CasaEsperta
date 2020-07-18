# CasaEsperta - Home Assistant

I used the [Supervised Installation](https://community.home-assistant.io/t/installing-home-assistant-supervised-on-ubuntu-18-04-4/200020). As of now, this isn't an Official install method so we need to use the linked guide to install it this way.

This installs a series of containers related with Home Assistant but somewhat separated from your other containers. You'll be able to use the full former hass.io features like add-ons on your normal Ubuntu Server.

##  Install
```
aptupd
sudo -i
apt install -y software-properties-common apparmor-utils apt-transport-https avahi-daemon ca-certificates curl dbus jq network-manager socat
systemctl disable ModemManager
systemctl stop ModemManager
curl -sL "https://raw.githubusercontent.com/Kanga-Who/home-assistant/master/supervised-installer.sh" | bash -s
```

I add some errors in my first try, like having a notification that zeroconf and default_config failed when I first opened Home Assistant. I just removed all the related containers with Portainer (homeassistant, hassio_multicast, hassio_cli, hassio_audio, hassio_dns and hassio_supervisor) and deleted the hassio directory:
```
sudo rm -r /usr/share/hassio
```

I then tried the `curl -sL "https://raw.githubusercontent.com/Kanga-Who/home-assistant/master/supervised-installer.sh" | bash -s` command again and it went well the second time.

This might have been caused by a conflicting port reserved by Plex (5353) that I removed as it is not needed.

## Automatic updates
It is recommended to add the 6 containers to the ignore list of [Ouroboros](docker_containers.md#ouroboros) as they are managed by the supervisor and we don't want external updates that might break stuff. To do that, add the name of the six containers (homeassistant, hassio_multicast, hassio_cli, hassio_audio, hassio_dns and hassio_supervisor), each separated by a space, to the IGNORE tag of the ouroboros container in `~/docker/compose.yml` and run:
```
dcup
``` 

## Reverse Proxy
As we didn't set Home Assistant container's labels, we need to use the toml files to setup the reverse proxy, just like if it was an external app like [Sinobi](shinobi.md) or [Pi-hole](r-pi.md#pi-hole).

This time, we don't want Google authentication in front of Home Assistant nor any kind of external authentication, so I recommend to use strong passwords for your Home Assistant users.

To reverse-proxy it, edit the file [app-hass.toml](../main_server/docker/traefik/app-hass.toml) to replace example.pt with your domain and SERVER_IP with your lan IP. Then copy the file to `~/docker/traefik/rules/app-hass.toml` and navigate to https://hass.example.pt.

## Share folder
To facilitate the configuration process of Home Assistant, we'll setup a share to the folder where the config files are stored. 

That folder is located at `/usr/share/hassio` and we need to fis some permissions first.

Give ownership to the folder and files to the GROUP you created in the [Samba section](server.md#share-folders-with-samba) and give write permission to that group
```
cd /usr/share
sudo chown -R root:nasusers hassio
sudo chmod -R g+w hassio
```

I recommend creating a share only visible to your user, like the [Hass] config in the [example file](../main_server/smb_conf). 
Change the config:
```
sudo nano /etc/samba/smb.conf
sudo nano /etc/samba/USER.conf
sudo systemctl restart smbd
```

