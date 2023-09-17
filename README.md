
## PokerHistorySplitter

---

### Présentation

PokerHistorySplitter est un projet conçu pour télécharger des fichiers d'historique de poker depuis un bucket S3, les diviser en fichiers individuels basés sur différentes mains de poker, puis uploader ces fichiers divisés vers le même bucket S3.

### Configuration

Pour utiliser ce projet, vous devez configurer certaines variables d'environnement. Créez un fichier `.env` à la racine du projet et ajoutez les éléments suivants :

```plaintext
DO_REGION=Votre_region_DigitalOcean
DO_ENDPOINT=Votre_endpoint_DigitalOcean
AWS_ACCESS_KEY_ID=Votre_access_key
AWS_SECRET_ACCESS_KEY=Votre_secret_access_key
```

N'oubliez pas de remplacer les valeurs par vos propres informations d'identification et de configuration.

### Dépendances

Installez les dépendances requises en exécutant :

```bash
pip install -r requirements.txt
```

### Exécution

Pour exécuter le projet, utilisez la commande suivante :

```bash
python app.py
```

### Structure du projet

- `app.py` : Point d'entrée principal de l'application.
- `downloader.py` : Contient la classe `S3Downloader` pour télécharger des fichiers depuis un bucket S3.
- `splitter.py` : Contient la classe `FileSplitter` pour diviser des fichiers d'historique brut et les uploader vers S3.
- `requirements.txt` : Liste des dépendances nécessaires à l'exécution du projet.


---

### License

MIT License (MIT).

Copyright (c) 2023 Alexandre MANGWA