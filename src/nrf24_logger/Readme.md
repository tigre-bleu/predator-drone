# Configuration

Configurer dans le script nrf24_logger.py:
```
address = 0xAAA1CA201670
data_rate = RF24_250KBPS
payload_size = 10
channel = 10
aack = False
```

# Utilisation
Lancer le script et appuyer sur la touche q pour arrêter. Le script affiche le temps moyen entre 2 trames et enregistre 2 fichiers:
- 1 fichier raw avec tous les paquets reçus correspondants à l'adresse.
- 1 fichier filtré avec les paquets dont les octets correspondent à un drone Syma X5C-1 (CRC valide)

On peut utiliser Gnuplot pour tracer un courbe. Un exemple de fichier de configuration Gnuplot est donné qui trace les 2 courbes sur les mêmes axes.

Pour générer une image avec Gnuplot: `gnuplot <input_file.gnuplot> > <output_file>`

**Exemple de sortie:**
![Image](./example.png?raw=true)