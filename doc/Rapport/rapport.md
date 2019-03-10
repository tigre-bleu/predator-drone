---
title-first-page: |
                | Drone predator,
                | \textit{one drone tu rule them all}
title:          "Drone predator"
title-img:      "../../logo/logo.png"
author:         "Florent Fayollas et Antoine Vacher"
subject:        "Rapport de projet long TLS-SEC"
promotion:      "2018 -- 2019"
toc:            true
documentclass:  article
---


\pagebreak

# Introduction

## Introduction généraliste sur les drones

Les UAVs (*Unmanned Aerial Vehicles*), communément appelés drones, sont des aéronefs sans 
pilote humain à bord. Un drone est un composant d'un UAS (*Unmanned Aircraft System*), qui 
comprend un UAV, une station de contrôle au sol et un system de communication entre les 
deux.

Les UAVs étaient, à l'origine, développés par les militaires et utilisés pour des missions 
trop dangereuses pour les humains. Cependant, ces dernières années, leur utilisation s'est 
généralisée à beaucoup de secteurs, tels que l'industrie ou les loisirs. Des exemples 
concrets d'utilisations sont la surveillance de réseaux électriques EDF ou des voies 
ferrées ou la photographie aérienne.

Leur champ d'utilisation est en croissance continue. En effet, les drones pourraient nous 
aider lors de scénarios de secours, par exemple, en étant utilisés par les pompiers pour 
un suivi en temps réel par images thermiques d'un feu. En outre, certaines entreprises, 
telles qu'Amazon, envisagent d'effectuer des livraisons par drone.


## Motivations de ce travail

Bien que les précédents cas d'usage civils soient bénéfiques, d'autres usages peuvent 
exister... En effet, un cas concret concernant tout le monde est celui d'une personne qui 
utiliserait un drone pour vous espionner, en survolant votre maison et passant proche de 
vos fenêtres. Une autre utilisation, plus grave, est l'utilisation, par Daesh, de drones 
civils pour larguer des bombes sur le front en Syrie. Enfin, plus récemment, l'aéroport de 
Londres Gatwick a été fermé pour cause de survols répétés par un drone non identifié.

Ainsi, il devient nécessaire de pouvoir se protéger des drones. Du côté militaire, des 
solutions existent déjà, telles que le brouillage de la liaison de commandes, par exemple 
grâce à des sortes de fusils, comme le DroneGun développé par 
DroneShield^[<https://www.droneshield.com/>]. Cependant, très peu de solutions sont 
présentes côté civil.

On pourrait penser à importer les solutions militaires dans le civil. Or, celles-ci 
mettent souvent hors d'état de nuire le drone, peu importe l'état final (un *crash* par 
exemple). Ceci n'étant pas acceptable dans un cadre civil.


## Définition des objectifs

L'objectif de notre projet est donc de développer un outil capable de prendre le contrôle 
de plusieurs drones. Cette prise de contrôle ne doit pas impliquer une chute du drone 
piraté. Cet outil pourrait ensuite être utilisé, par exemple, pour sécuriser la 
médiatisation d'un match sportif : il sera en mesure de "capturer" les drones détectés et 
de les récupérer. Après capture, il sera aussi possible d'analyser le contenu des drones 
et éventuellement de remonter au propriétaire.

Pour réaliser cet outil, nous nous sommes focalisés sur la prise de contrôle de drones 
civils : le Parrot AR.Drone 2.0 et le Syma X5C-1. C'est ce que nous détaillons dans les 
deux premières parties de ce rapport. Lorsque ces prises de contrôle furent terminées, 
nous avons cherché à embarquer l'outil sur un autre drone. Ceci est discuté dans la 
troisième partie de ce rapport.




\pagebreak

# Prise de contrôle d'un drone Parrot AR.Drone 2.0

\itodo{présentation vulgarisée}


## Présentation technique de l'attaque

\itodo{TODO}


## Réalisation

\itodo{TODO}


### Utilisation d'une unique puce WiFi

\itodo{TODO}


### Problème de pilote de puce WiFi

\itodo{TODO}


## Détection et prévention de l'attaque

\itodo{TODO : capture ENAC}




\pagebreak

# Prise de contrôle d'un drone Syma X5C-1

\itodo{TODO}




\pagebreak

# Embarquement de l'outil de prise de contrôle sur un drone prédateur

## Installation de l'outil sur une Raspberry Pi Zero W

\itodo{présentation vulgarisée}


### Utilisation du cockpit `ardrone-webflight`

\itodo{déport par iptables}


### Compilation de la bibliothèque `pyRF24`

\itodo{compilation pyrf24}


### Utilisation distante d'une manette

\itodo{usbip}


### Contrôle distant de l'outil

\itodo{Bluetooth PAN}


## Tests finaux de l'outil embarqué

\itodo{volière ENAC avec paparazzi + utilisation moyens volière (vidéo, etc.) + portée 
bluetooth}




\pagebreak

# Conclusion

\itodo{TODO}


