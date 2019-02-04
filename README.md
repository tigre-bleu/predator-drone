# predator-drone

Ce projet vise à construire un drone prédateur permettant de prendre le contrôle d'un autre drone.


## Notes de recherches

### [SkyJack](https://github.com/samyk/skyjack)

- Utilise la bibliothèque [`node-ar-drone`](https://github.com/felixge/node-ar-drone) (Node.JS) pour contrôler le drone. Cette 
  librairie ne fait que forger des paquets UDP et présenter une API ultra simple !
- Exploit fonctionnel, avec 2 cartes WiFi
- Tentative de fonctionnement avec 1 carte WiFi mais pas réussie


### [Thèse de *hack* de drone](https://github.com/markszabo/drone-hacking)

Services ouverts sur le Parrot AR drone :

- `telnet`
- FTP
- *stream* vidéo sur le port 5555
- écoute des commandes sur le port 5556

=> découverts grâce à un `nmap`


### Documentation ENSIMAG

<https://ensiwiki.ensimag.fr/index.php?title=Etude_de_la_s%C3%A9curit%C3%A9_d%27un_drone>

- Connexion `telnet` => `uid=0`
- Désauthentification
- Récupération du flux vidéo
- Envoi de commandes
- Déni de service par attaque MITM

=> beaucoup de références


### Utilisation du protocole MAVLink par le Parrot ?

Oui, mais seulement avec le *Flight Recorder*, qui fait la traduction. Le module introduit 
une gestion GPS et une interface avec *QGroundControl*.


## Achat éventuel de drone

- Eachine E61 ([Bang good, 
  26€](https://fr.banggood.com/Eachine-E61E61HW-Mini-WiFi-FPV-With-HD-Camera-High-Hold-Mode-Foldable-RC-Drone-Quadcopter-RTF-p-1384204.html))

- Eachine E58
  - [Cdiscount, 
    40€](https://www.cdiscount.com/juniors/drones/eachine-e58-wifi-rc-drone-2mp-camera-3-batteries/f-12099-eac6296623481690.html)
  - [AliExpress, 
    37€](https://fr.aliexpress.com/item/JY019-Quadrocopter-0-3MP-2MP-Cam-ra-Drone-Rc-Profissional-WiFi-FPV-Mini-Drones-Avions-Sans/32967487007.html)
  - [Bang good, 
    55€](https://fr.banggood.com/Eachine-E58-WIFI-FPV-With-2MP-Wide-Angle-Camera-High-Hold-Mode-Foldable-RC-Drone-Quadcopter-RTF-p-1212232.html)

- Eachine E511S, GPS ([Bang good, 
  100€](https://fr.banggood.com/Eachine-E511S-GPS-Dynamic-Follow-WIFI-FPV-With-1080P-Camera-16mins-Flight-Time-RC-Drone-Quadcopter-p-1373965.html))

- Eachine E511 ([Bang good, 
  80€](https://fr.banggood.com/Eachine-E511-WIFI-FPV-With-1080P-Camera-17mins-Flight-Time-High-Hold-Mode-Foldable-RC-Quadcopter-RTF-p-1361612.html))
