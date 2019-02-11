# *Hacking* existants

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


# Notes diverses

- **Le protocole MAVLink est-il utilisé par le Parrot AR.Drone ?**\
  Oui, mais seulement avec le *Flight Recorder*, qui fait la traduction. Le module 
  introduit une gestion GPS et une interface avec *QGroundControl*.

