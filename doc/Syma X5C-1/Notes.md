# Sniffing SDR

On va commencer par le plus simple: caractériser la liaison radio avec le drone éteint et la télécommande en mode recherche (avant l'appairage).


On va parcourir la bande de fréquence entre 2.400 GHz et 2.525 Ghz avec Gnuradio. Cela correspond à la plage de fréquences gérables par un nRF24l01 (la puce que l'on souhaite utiliser pour prendre le controle du drone).




Pour cela on crée une waterfall et on voit de l'activité autour **2.410 GHz**. Pour préciser notre observation, on fait une FFT avec Gnuradio autour de cette fréquence. Après avoir bien centré notre FFT, on voit une **bande passante autour de 800kHz** et une fréquence à 2.4701 GHz

Si on regarde un extrait de la spec du nRF24l01, on peut lire:

```
6.3 RF channel frequency
------------------------

The RF channel frequency determines the center of the channel used by the nRF24L01+. The channel occupies a bandwidth of less than 1MHz at 250kbps and 1Mbps and a bandwidth of less than 2MHz at 2Mbps. nRF24L01+ can operate on frequencies from 2.400GHz to 2.525GHz. The programming resolu-
tion of the RF channel frequency setting is 1MHz.

At 2Mbps the channel occupies a bandwidth wider than the resolution of the RF channel frequency setting. To ensure non-overlapping channels in 2Mbps mode, the channel spacing must be 2MHz or more. At 1Mbps and 250kbps the channel bandwidth is the same or lower than the resolution of the RF frequency.

The RF channel frequency is set by the RF_CH register according to the following formula:

F0 = 2400 + RF_CH [MHz]

You must program a transmitter and a receiver with the same RF channel frequency to communicate with each other.
```

A supposer que le chipset du drone soit similaire à un nRF25l01, on voit qu'avec 800kHz de bande passante, on doit avoir **soit du 250Kbps, soit du 1MBps** mais ce n'est certainement pas du 2Mbps.

On utilise la formule pour trouver le canal: 2410 - 2400 = canal 10.

En faisant la même chose sur les autres fréquences, on voit de l'activité sur les canaux: **10, 31, 42, 66**

# Capture SDR

On va utiliser Gnuradio pour enregistrer les bits correspondants à notre payload.

Avant cela, on enregistre le signal brut dans un fichier qu'on ouvre avec baudline: on voit que ça a l'air d'être de la modulation GFSK.

Dans Gnuradio, on rajoute donc la démodulation et on constate dans baudline que le signal modulé est assez propre. On peut y lire un préambule "01010101" suivi de ce qui est probablement une adresse.

# Interprétation du protocole

On utilise les fichiers python d'analyse qui existent déjà pour le RPI.

On voit:
- Puissance (Octet 1): 0x00 - 0xFF
- Tanguage (Octet 2):
  - Avant: 0x00 - 0x7F
  - Arrière: 0x80 - 0xFF
- Roulis (Octet 3):
  - Gauche: 0x00 - 0x7F
  - Droite: 0x80 - 0xFF
- Lacet (Octet 4):
  - Gauche: 0x00 - 0x7F
  - Droite: 0x80 - 0xFF
- Mode (Octet 6):
  - High: 0xA0
  - Low: 0x20
- Des bits indépendants sur les octets de la fin pour la gachette droite et les trims

# Autres

https://github.com/goebish/nrf24_multipro/blob/master/nRF24_multipro/SymaX.ino