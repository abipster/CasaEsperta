# CasaEsperta - Raspberry Pi

## Hardware
I have two different Raspeberry Pis:

* [Raspberry Pi 3 Model B+](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) - It's main function is to run main Pi-hole instance and the Zigbee2Mqtt coordinator.

* [Raspberry Pi 3 Model A+](https://www.raspberrypi.org/products/raspberry-pi-3-model-a-plus/) - It's main function is to run backup Pi-hole instance and to act as a bluetooth connection upstairs.

## Setup
Put [Raspberry Pi OS Lite](https://www.raspberrypi.org/downloads/raspberry-pi-os/) with [Etcher](https://www.balena.io/etcher/) in a 16GB+ micro SD card.
This will prepare a headless OS for the Raspberry Pi.

Create an empty file called `ssh` in the root of the SD card. This way, Raspberry Pi will have SSH enabled so you won't need a keybord/monitor to do its initial configurations.

If you want to connect it to a WiFi network instead of a wired one, you'll have to create a `wpa_supplicant.conf` file in the root of the SD card. Copy the content of [wpa_supplicant.conf](../r_pis/wpa_supplicant.conf) and put your WiFi information.

Make sure you set a static IP in your router, so you can find it at the same address.

SSH to it with user `pi` and password `raspberry` and then do the initial configuration to set your hostname and timezone:
```
sudo raspi-config
```

### Change default username
To replace pi username with one of your choosing start by enabling root login
```
sudo passwd root
sudo nano /etc/ssh/sshd_config
```
To enable root SSH, change `PermitRootLogin` to `yes`
```
sudo /etc/init.d/ssh restart
```
Exit and login with root user and type, replacing username with your own
```
usermod -l username pi
usermod -m -d /home/username username
```
Exit and login with your newly created username. To setup your new password type
```
passwd
```
After that, we can disable the root user.
```
sudo passwd -l root
```

At your client machine, you can enable passwordless-SSH with the certificate you created when setting up the main server:
```
ssh-copy-id USERNAME@PI_IP
```

Some useful aliases for the Pi are [here](../r_pis/aliases) and you can append them to the end of your bashrc file:
```
nano ~/.bashrc
```
Save and update:
```
source .bashrc

aptupd
```

## Share folder
Setup a share in your main server. Then prepare your Pi to be able to connect to it and create a folder to mount the share:
```
sudo apt install samba samba-common-bin smbclient cifs-utils -y
sudo mkdir /mnt/shared
sudo chown ${USER}:pi /mnt/shared
```
Create a file with the credentials of the share:
```
nano ~/.smbcredentials
```
With this content:
```
username: USERNAME
password: PASSWORD
```
Change its permissions
```
chmod 600 ~/.credentials
```
Then edit the fstab to mount the share:
```
sudo nano /etc/fstab
```
Add this line to the file, editing SEVER_IP, SHARE_NAME and USERNAME with your values:
```
//SEVER_IP/SHARE_NAME /mnt/shared cifs rw,uid=USERNAME,gid=pi,file_mode=0774,dir_mode=0774,credentials=/home/USERNAME/.smbcredentials,x-systemd.automount 0 0
```
Save, exit and then run:
```
sudo mount -a
```

## [Netdata](https://github.com/netdata/netdata)

To install Netdata, just type
```
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

If you want to enable temperature charts:
```
sudo /etc/netdata/edit-config charts.d.conf
```
Append this line to the end:
```
sensors=force
```
Save and restart Netdata:
```
sudo systemctl restart netdata
```

To add a custom dashboard to Organizer, go read [that guide](organizr.md#homepage).

### Reverse-Proxy
To reverse-proxy it, edit the file [app-pi-data.toml](../main_server/docker/traefik/app-pi-data.toml) to reflect the Raspberry Pi's IP and replace example.pt with your domain. then copy the file to `~/docker/traefik/rules/app-pi-data.toml` and navigate to https://pi-data.example.pt.

## [Pi-Hole](https://pi-hole.net/)
I recommend you go read [this guide](https://www.smarthomebeginner.com/pi-hole-setup-guide/) before continuing.

```
wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```
Follow the steps of the installer.

Change the admin password:
```
pihole -a -p
```

To add more blocklists to Pi-hole, paste this [content](https://v.firebog.net/hosts/lists.php?type=tick) to Group Management -> AdLists -> Address field. Then update it with:
```
pihole -g
```

To configure your network to use it, go search a guide for your router model.
### For USG:
* In Pi-hole, under Settings -> DNS, turn on Conditional Forwarding with the IP of the router as USG's IP, and Local domain name your local domain name.
* Turn on DNSSEC
* In Unifi Controller, go to each of the networks and set the DHCP Name Server IP as the Pi's IP.
* In Unifi Controller, under Services -> DHCP -> DHCP Server, be sure Register client hostname from DHCP requests in USG DNS forwarder is On.

### Use the share
Pi-hole writes a log to the SD card every so often. To save the life span of the SD card, it's recommended to write this log elsewhere. We'll use the share to do just that.

Add pihole user to pi group so he can have write acces on the share
```
sudo usermod -aG pi pihole
```
Stop Pi-hole and edit the config:
```
phstop
sudo nano /etc/pihole/pihole-FTL.conf
```
Add the following line to the config file
```
LOGFILE=/mnt/shared/pihole1-FTL.log
```
Now copy the log file to the share and start Pi-hole
```
sudo cp /var/log/pihole-FTL.log /mnt/shared/pihole1-FTL.log
phstart
```

### Reverse-Proxy
To reverse-proxy it, edit the file [app-pihole.toml](../main_server/docker/traefik/app-pihole.toml) to reflect the Raspberry Pi's IP and replace example.pt with your domain. Then copy the file to `~/docker/traefik/rules/app-pihole.toml` and navigate to https://pihole.example.pt.

## [Zigbee2Mqtt](https://www.zigbee2mqtt.io/)
To learn how to flash Zigbee coordinators and routers, go read the linked documentation.

After pluggin the coordinator to a USB port of the Pi, check where it is found. Usually it's at `/dev/ttyACM0`. You can confirm with:
```
ls -l /dev/ttyACM0
```
that should give a result like:
```
crw-rw---- 1 root dialout 166, 0 May 16 19:15 /dev/ttyACM0
```

### Install
Install Noje.js
```
sudo curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt install nodejs git make g++ gcc -y
```

Get Zigbee2Mqtt from source and install dependencies
```
sudo git clone https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
sudo chown -R ${USER}:pi /opt/zigbee2mqtt/
cd /opt/zigbee2mqtt
npm ci
```
After that, configure it by following [this section](https://www.zigbee2mqtt.io/getting_started/running_zigbee2mqtt.html#3-configuring).
There's an example configuration file [here](../r_pis/zigbee2mqtt/configuration.yaml).


Start it:
```
npm start
```
If everything seems right, stop it and setup a autostart service:
```
sudo nano /etc/systemd/system/zigbee2mqtt.service
```
Edit the content of [zigbee2mqtt.service](../r_pis/zigbee2mqtt/zigbee2mqtt.service) to replace USERNAME with your username.

Then start it and check everything is running without errors:
```
zbstart
zblog
```
If everything is ok, enable autostart:
```
sudo systemctl enable zigbee2mqtt.service
```