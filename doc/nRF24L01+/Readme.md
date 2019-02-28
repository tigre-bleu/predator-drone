# Documentation
Le module nRF24l01(+) utilise le bus SPI et 2 pins (CS+CE).

Voir la [Documentation](nRF24L01Pluss_Preliminary_Product_Specification_v1_0.pdf)

# Connexion à un Raspberry Pi

De nombreaux tutoriels existent sur le web. Le code de ce projet est basé sur le choix des pins CE = 22 et CS = 24 mais d'autres configurations peuvent marcher à condition de modifier le code.

![Image](./RPI_nRF24l01_conection.png?raw=true)

Les Headers des RPi 2, 3, Zero et Zero W sont identiques.

Le condensateur est recommandé car le module est sensible au bruit sur l'alimentation, mais il n'est pas indispensable.