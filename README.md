# Projet `predator-drone`

L'objectif de ce projet est de développer un drone prédateur permettant de prendre le 
contrôle d'un autre drone. Nous nous focalisons dans un premier temps sur la prise de 
contrôle d'un drone Parrot AR.Drone.

L'attaque perpetrée est une variante de la preuve de concept 
[`skyjack`](https://github.com/samyk/skyjack). Le cockpit utilisé pour piloter l'AR.Drone 
est [`ardrone-webflight`](https://github.com/eschnou/ardrone-webflight), avec le plugin 
[`webflight-gamepad`](https://github.com/wiseman/webflight-gamepad/) permettant un 
contrôle avec une manette de jeu.

Le script `main.py` est celui à exécuter pour perpétrer l'attaque. La majeure partie du 
code est dans la bibliothèque Python `predator_drone`. Cette bibliothèque contient :

- `disp.py` : multiples fonctions d'affichage (`debug`, `warn`, etc.)
- `ext_exec.py` : exécution de commande externe (fonction `do`)
- `menu.py` : affichage simple d'un menu
- `parrot_hack.py` : piratage d'un Parrot (en renseignant l'AP WiFi) et redirection de 
  tous les paquets reçus sur une adresse IP vers l'adresse de l'AP de l'AR.Drone (avec 
  `iptables`)
- `parrot_list.py` : listage de l'ensemble des AP WiFi Parrot
- `wifi.py` : gestion d'une carte WiFi
  + passage en mode *monitor*/*managed*
  + désauthentification d'un client sur un *Access Point* (avec `aireplay-ng`)
  + listage des *Access Points* aux alentours
  + listage des clients connectés à un AP
  + connexion à un AP et obtention d'une adresse IPv4 (avec `dhclient`)



### Intégration sur une RPi Zero W

Ce programme devait pouvoir être embarqué sur une Raspberry Pi Zero W, elle-même embarquée 
sur un drone. Le script `tools/install_on_rpi.sh` permet d'installer les dépendances 
nécessaires et de configurer le Bluetooth de la RPi en point d'accès réseau. C'est grâce à 
ce point d'accès que l'on garde le contrôle de la RPi, avec une connexion SSH par exemple.

La RPi Zero W dispose d'une carte WiFi intégrée qui est utilisée par le programme pour se 
connecter au point d'accès WiFi de l'AR.Drone piraté. Il est nécessaire d'ajouter un 
dongle WiFi pour pouvoir écouter les réseaux WiFi et envoyer les trames de 
désauthentification. Ce dongle WiFi doit supporter un mode *monitor*. Celui que nous avons 
utilisé est le TP-Link TL-WIN823N :

```
ID 0bda:8178 Realtek Semiconductor Corp. RTL8192CU 802.11n WLAN Adapter
```

Note : le pilote par défaut sur la RPi Zero pour ce dongle est le `8192cu`, mais celui-ci 
n'a pas fonctionné pour l'attaque. Il nous a été nécessaire d'enlever le pilote 
`rtl8192cu` de la *blacklist* noyau dans `/etc/modprobe.d/blacklist-rtl8192cu.conf`.



### Outils

Le dossier `tools` contient les scripts :

- `disconnect_link.sh` permet de déconnecter une interface WiFi de l'AP sur lequel elle 
  est enregistrée
- `share_net_with_rpi.sh` permet de partager Internet, disponible sur votre PC hôte, avec 
  la Raspberry Pi (il faut tout de même indiquer une route par défaut sur la RPi, ainsi 
  qu'un *nameserver* dans `/etc/resolv.conf`)
- `install_rpi.sh` permet d'installer le programme sur une Raspberry Pi



### Dépendances

Les dépendances de ce projet sont :

- [`ardrone-webflight`](https://github.com/eschnou/ardrone-webflight) avec le plugin 
  [`webflight-gamepad`](https://github.com/wiseman/webflight-gamepad/)
- `aireplay-ng`
- `dhclient`
- `iptables`
- Python 3 et `pip3`
  + [`Scapy`](https://scapy.net/) avec le correctif du bug 
    [#1872](https://github.com/secdev/scapy/issues/1872)
  + [`PyRIC`](https://github.com/wraith-wireless/pyric)



### Installation du cockpit `ardrone-webflight`

```bash
# Clone repository
git clone https://github.com/eschnou/ardrone-webflight.git
cd ardrone-webflight
npm install
bower install

# Edit configuration and select plugins
cp config.js.sample config.js
vim config.js

# Run application then point your browser to http://localhost:3000/
node app.js
```



### Notes sur l'installation de `pyRF24` sur la RPi

Instructions d'installation prises de <https://tmrh20.github.io/RF24/RPi.html>.

```bash
# =================
#    Extend SWAP
# =================

# Create a 4GB swap file
dd if=/dev/zero of=/tmp/swap bs=1024 count=4194304
chmod 600 /tmp/swap

# Register swap
mkswap /tmp/swap
swapon /tmp/swap


# =======================
#    Build and install
# =======================

# Enable SPI kernel module
sudo raspi-config

# Upgrade system
sudo apt update
sudo apt upgrade

# Make and install
git clone https://github.com/TMRh20/RF24
cd RF24
sudo make install -B

# Python requirements
sudo apt-get install python3-dev libboost-python-dev python3-setuptools
sudo ln -s /usr/lib/arm-linux-gnueabihf/libboost_python-py35.so \
  /usr/lib/arm-linux-gnueabihf/libboost_python3.so

# Build and install Python library
cd pyRF24
python3 setup.py build
sudo python3 setup.py install
```



### Notes sur l'installation d'`usbip`

***TODO***

