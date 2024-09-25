# Utiliser l'image de base de Python 3.9
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /usr/src/app

# Copier le fichier requirements.txt (bibliothèques nécessaires)
COPY requirements.txt ./

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du bot dans le conteneur
COPY . .

# Commande pour exécuter le bot
CMD ["python", "main.py"]