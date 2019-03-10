# Projet `predator-drone`

![Logo](logo/logo.png)
L'objectif de ce projet est de développer un drone prédateur permettant de prendre le
contrôle d'un autre drone. Deux types d'attaques ont été réalisées :

- RF2.4GHz (Syma X5C-1)
- WiFi (Parrot AR.Drone)

Un autre drone RF2.4GHz a été étudié, mais le reverse engineering du protocole n'est pas allé jusqu'au bout (PNJ Discovery)

## Détails des attaques

La description des attaques est détaillée dans le dossier de documentation:
- [Attaque Parrot AR.Drone](doc/Parrot_AR_Drone/Notes.md)
- [Attaque Syma X5C-1](doc/Syma\ X5C-1/Notes.md)

L'étude partielle du second drone RF est disponible dans le dossier [Etude PNJ Discovery](doc/PNJ\ Drone/Notes.md)

## Vidéos

2 vidéos ont été publiées démontrant les attaques sur le Parrot et le Syma:
- [Attaque Parrot AR.Drone](https://pe.ertu.be/videos/watch/54cb4bff-c321-4030-ad70-543e044f7b74)
- [Attaque Syma X5C-1](https://pe.ertu.be/videos/watch/14ae8a25-1c56-4ab7-91fe-47d0ec886a59)

## L'outil d'attaque multifonction `predator-drone`

Le script `main.py` est celui à exécuter pour perpétrer l'attaque. La majeure partie du
code est dans la bibliothèque Python `predator_drone`. Cette bibliothèque contient :

- `disp.py` : multiples fonctions d'affichage (`debug`, `warn`, etc.)
- `ext_exec.py` : exécution de commande externe (fonction `do`)
- `menu.py` : affichage simple d'un menu
- `parrot_hack.py` : piratage d'un Parrot (en renseignant l'AP WiFi) et redirection de
  tous les paquets reçus sur une adresse IP vers l'adresse de l'AP de l'AR.Drone (avec
  `iptables`)
- `parrot_list.py` : listage de l'ensemble des AP WiFi Parrot
- `syma_scan` : listage de l'ensemble des drones Syma X5C-1 détectés
- `syma_hack` : piratage d'un drone Syma X5C-1 (en renseignant l'adresse et les canaux utilisés). Le contrôle se fait grâce à un gamepad USB partagé via le réseau
- `wifi.py` : gestion d'une carte WiFi
  + passage en mode *monitor*/*managed*
  + désauthentification d'un client sur un *Access Point* (avec `aireplay-ng`)
  + listage des *Access Points* aux alentours
  + listage des clients connectés à un AP
  + connexion à un AP et obtention d'une adresse IPv4 (avec `dhclient`)

### Outils Annexes

Le dossier `tools` contient les scripts :

- `disconnect_link.sh` permet de déconnecter une interface WiFi de l'AP sur lequel elle
  est enregistrée
- `share_net_with_rpi.sh` permet de partager Internet, disponible sur votre PC hôte, avec
  la Raspberry Pi (il faut tout de même indiquer une route par défaut sur la RPi, ainsi
  qu'un *nameserver* dans `/etc/resolv.conf`)
- `install_rpi.sh` permet d'installer le programme sur une Raspberry Pi
- `nrf24_logger.py` permet de créer des fichiers CSV à partir des paquets capturés par un nRF24l01+
- `syma_protocol_analyser` permet d'afficher en temps réel les paquets capturés par le nRF24l01+ pour faciliter la compréhension du protocole


## Intégration sur une RPi Zero W

Ce programme devait pouvoir être embarqué sur une Raspberry Pi Zero W, elle-même embarquée
sur un drone. Le script `tools/install_rpi.sh` permet d'installer les dépendances
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

Il est nécessaire de connecter un module nRF24l01+ sur le bus SPI du RPi tel que spécifié [ici](doc/nRF24l01+/Readme.md).

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

USBIP permet d'utiliser sur le RPi une manette USB connectée sur le PC de l'attaquant. USBIP dépends d'une partie noyau et d'une partie utilisateur. En pratique, le périphérique est partagé via une connexion TCP.

*Attention: La version d'usbip dans Rasbian Stretch est trop vieille et n'est pas compatible avec un serveur plus récent. Il est nécessaire d'installer la version de Raspbian Buster (Version Testing). Les versions d'USBIP présente dans les dépots Debian armhf ne fonctionnent pas (Segmentation Fault)*

__Installation côté serveur__:
Le serveur est le PC qui a le périphérique USB physiquement connecté.

Lancer le démon:
```bash
sudo modprobe usbip_core
sudo modprobe usbip_host
sudo modprobe vhci-hcd
sudo usbipd -D
```

Lister les périphériques USB disponibles
```bash
sudo usbip list --local
```
La liste des périphériques USB est affiché. Il faut noter le Bus ID de celui à partager. Ensuite on le partage avec
```bash
sudo usbip bind -b <bus-id>
```

__Installation côté client__:
Le client est le RPi qui va utiliser le périphérique USB.

```bash
sudo modprobe usbip_core
sudo modprobe usbip_host
```
On liste les périphériques disponibles sur l'hôte distant:
```bash
sudo usbip list --remote=<IP_Serveur>
```
Enfin on attache le périphérique:
```bash
usbip attach --remote <IP_Serveur> --busid=<bus-id>
```
