# Sniffing SDR
## RC en mode Scanning (avant Binding)

On va commencer par le plus simple: caractériser la liaison radio avec le drone éteint et la télécommande en mode recherche (avant l'appairage).


On va parcourir la bande de fréquence entre 2.400 GHz et 2.525 Ghz avec Gnuradio. Cela correspond à la plage de fréquences gérables par un nRF24l01 (la puce que l'on souhaite utiliser pour prendre le controle du drone).

Pour cela on crée une waterfall et on voit de l'activité autour **2.472 GHz**. Pour préciser notre observation, on fait une FFT avec Gnuradio autour de cette fréquence. Après avoir bien centré notre FFT, on voit une **bande passante autour de 800kHz** et une fréquence à 2.4701 GHz

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

On utilise la formule pour trouver le canal: 2470 - 2400 = canal 70.

## En vol

Activité sur les canaux 54, 63, 65, 70, 73