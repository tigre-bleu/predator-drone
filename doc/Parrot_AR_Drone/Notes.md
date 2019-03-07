L'attaque perpetrée au final est une variante de la preuve de concept
[`skyjack`](https://github.com/samyk/skyjack). Le cockpit utilisé pour piloter l'AR.Drone
est [`ardrone-webflight`](https://github.com/eschnou/ardrone-webflight), avec le plugin
[`webflight-gamepad`](https://github.com/wiseman/webflight-gamepad/) permettant un
contrôle avec une manette de jeu.

# *Hacking* existants

Les notes ci-dessous retraçent les recherches menées sur le Parrot AR.Drone 2.0

## [SkyJack](https://github.com/samyk/skyjack)

- Utilise la bibliothèque [`node-ar-drone`](https://github.com/felixge/node-ar-drone)
  (NodeJS) pour contrôler le drone. Cette librairie ne fait que forger des paquets UDP et
  présenter une API ultra simple !
- Exploit fonctionnel, avec 2 cartes WiFi
- Tentative de fonctionnement avec 1 carte WiFi mais pas réussie


## [Thèse de *hack* de drone](https://github.com/markszabo/drone-hacking)

Services ouverts sur le Parrot AR drone :

- `telnet`
- FTP
- *stream* vidéo sur le port 5555
- écoute des commandes sur le port 5556

=> découverts grâce à un `nmap`


## Documentation ENSIMAG

<https://ensiwiki.ensimag.fr/index.php?title=Etude_de_la_s%C3%A9curit%C3%A9_d%27un_drone>

- Connexion `telnet` => `uid=0`
- Désauthentification
- Récupération du flux vidéo
- Envoi de commandes
- Déni de service par attaque MITM

=> beaucoup de références




# Contrôleur

- [AutoFlight (contrôle depuis PC)](http://electronics.kitchen/autoflight)
- Python :
  - [PS-Drone (Python lib)](http://www.playsheep.de/drone/)
  - [`python-ardrone` lib](https://github.com/venthur/python-ardrone)
- NodeJS
  - [NodeJS on AR.Drone](https://github.com/pubnub/pubnub-drone)
  - [Node Copter community](http://www.nodecopter.com/)
  - [AR.Drone webflight](http://eschnou.github.io/ardrone-webflight/)
    ([gamepad plugin](https://github.com/wiseman/webflight-gamepad/))


# Vidéo

Cette vidéo montre l'utilisation de `predator-drone` pour attaquer un Parrot AR 2.0.


<figure class="video_container">
  <iframe src="https://pe.ertu.be/videos/embed/54cb4bff-c321-4030-ad70-543e044f7b74" frameborder="0" allowfullscreen="true"> </iframe>
</figure>


# Notes diverses

- **Le protocole MAVLink est-il utilisé par le Parrot AR.Drone ?**\
  Oui, mais seulement avec le *Flight Recorder*, qui fait la traduction. Le module
  introduit une gestion GPS et une interface avec *QGroundControl*.


# Notes sur les dongles WiFi USB disponibles

- [TP-Link TL-WN823N (puce RTL8192CU)](https://doc.ubuntu-fr.org/hercules_hwnup-150)
- Ralink MT7601U (puce RTL8192SU) ([doc Debian](https://wiki.debian.org/fr/rtl819x))
- [Dlink DWA-131 (non compatible *nl80211*)](https://doc.ubuntu-fr.org/dwa-131), non
  affiché par `iw dev`.

# Recherches sur la désauthentification WiFi avec Scapy

- <https://github.com/0x90/wifi-scripts/blob/master/deauth/psdos.py>
- <https://github.com/catalyst256/MyJunk/blob/master/scapy-deauth.py>
-
<https://pen-testing.sans.org/blog/2011/10/13/special-request-wireless-client-sniffing-with-scapy/>
- <https://mrncciew.com/2014/10/11/802-11-mgmt-deauth-disassociation-frames/>
-
<https://security.stackexchange.com/questions/145484/deauthentication-attacks-from-or-to-client>

