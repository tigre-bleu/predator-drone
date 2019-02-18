# `predator-drone`

L'objectif de ce projet est de développer un drone prédateur permettant de prendre le 
contrôle d'un autre drone. Nous nous focalisons dans un premier temps sur la prise de 
contrôle d'un drone Parrot AR.Drone.

L'attaque perpetrée est une variante de la preuve de concept 
[skyjack](https://github.com/samyk/skyjack). Le cockpit utilisé est 
[ardrone-webflight](https://github.com/eschnou/ardrone-webflight), avec le plugin 
[webflight-gamepad](https://github.com/wiseman/webflight-gamepad/) permettant de contrôler 
le drone grâce à un *gamepad*.

Le script `predator-drone.py` est celui exécuté pour perpétrer l'attaque.


## TODO list

- [x] Configurer la Raspberry Pi Zero W
- [x] Faire fonctionner un cockpit
- [x] Faire fonctionner l'attaque :
  - [x] Listing des réseaux WiFi
  - [x] Filtrage des réseaux Parrot
  - [x] Listing des clients connectés à un réseau Parrot
  - [x] Désauthentification d'un client
  - [x] Connexion au réseau Parrot
  - [x] Prise de contrôle
- [x] Mettre au propre `hack.py`
  - [x] Ordonner les fonctions
  - [x] Spliter le script en une bibliothèque
  - [x] Définir plusieurs niveaux de verbosité
- [x] Utiliser la bibliothèque [PyRIC](https://github.com/wraith-wireless/pyric)
- [ ] Mettre à jour le README avec des instructions d'installation
  - [ ] `npm`, `bower`
  - [ ] bug fix de scapy
- [ ] Changer la méthode de connexion à un AccessPoint
      => ne fonctionne actuellement pas toujours
- [ ] [Vérifier l'euid au démarrage du 
  script](https://stackoverflow.com/questions/2806897/)

