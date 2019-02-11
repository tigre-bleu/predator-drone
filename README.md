# `predator-drone`

L'objectif de ce projet est de développer un drone prédateur permettant de prendre le 
contrôle d'un autre drone. Nous nous focalisons dans un premier temps sur la prise de 
contrôle d'un drone Parrot AR.Drone.

L'attaque perpetrée est une variante de la preuve de concept 
[skyjack](https://github.com/samyk/skyjack). Le cockpit utilisé est 
[ardrone-webflight](https://github.com/eschnou/ardrone-webflight), avec le plugin 
[webflight-gamepad](https://github.com/wiseman/webflight-gamepad/) permettant de contrôler 
le drone grâce à un *gamepad*.

Le script `hack.py` est celui exécuté pour perpétrer l'attaque.


## TODO list

- [x] Configurer la Raspberry Pi Zero W
- [x] Faire fonctionner un cockpit
- [ ] Faire fonctionner l'attaque :
  - [x] Listing des réseaux WiFi
  - [x] Filtrage des réseaux Parrot
  - [x] Listing des clients connectés à un réseau Parrot
  - [x] Désauthentification d'un client
  - [ ] Connexion au réseau Parrot
  - [ ] Prise de contrôle
- [ ] Mettre au propre `hack.py`
  - [ ] Ordonner les fonctions
  - [ ] Spliter le script en une bibliothèque
- [ ] Étendre le concept à un autre drone, par exemple à l'Eachine E511

