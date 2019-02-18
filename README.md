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
- [ ] Utiliser la bibliothèque PyRIC
- [ ] Étendre le concept à un autre drone, par exemple à l'Eachine E511


## Gestion WiFi par Python

- [PyRIC](https://github.com/wraith-wireless/pyric)
  - Remplace les commandes `iw`, etc.
  - [Ne permet pas de gérer une connexion à un réseau 
    WiFi](https://github.com/wraith-wireless/PyRIC/issues/28)
  - [Semble abandonné](https://github.com/wraith-wireless/PyRIC/issues/42), mais repris 
    [ici](https://github.com/wifiphisher/WiPy)

- [pywificontrol](https://github.com/emlid/pywificontrol)
  - **À VOIR**

- [wireless](https://github.com/joshvillbrandt/wireless)
  - Ne semble pas fonctionner (après installation par `pip3`)
  - Version installée par `pip` différente de celle sur GitHub

- [wifi](https://pypi.org/project/wifi/)
  - [Très peu de documentation](http://pythonwifi.tuxfamily.org/)
  - [Exemple](https://gist.github.com/taylor224/516de7dd0b707bc0b1b3)

- [pythonwifi](https://github.com/pingflood/pythonwifi)
  - Très vieille bibliothèque (2009)
  - [Exemple d'utilisation](https://www.dropbox.com/s/tey8dusi9r18410/geo_envTLS.zip?dl=0)

- [pywifi](https://github.com/awkman/pywifi)
  - Semble mise à jour régulièrement

- [Recherche à 
  continuer](https://www.google.co.uk/search?q=windows+api+connect+to+wifi+python&oq=windows+api+connect+to+wifi+python&gs_l=psy-ab.3...9103.10269.0.10789.7.7.0.0.0.0.184.869.1j5.6.0....0...1.1.64.psy-ab..1.5.701...33i22i29i30k1.0.G4UA7PWgrWU)

