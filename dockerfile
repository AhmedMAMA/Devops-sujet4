FROM python:3.10-slim

# Créer le dossier app
WORKDIR /app

# Copier ton script et éventuellement requirements.txt
COPY test.py .

# Installer pip et les dépendances
RUN pip install --upgrade pip
RUN pip install flask ultralytics tensorflow pillow numpy

# Exposer le port
EXPOSE 5000

# Commande pour lancer l'app
CMD ["python", "app.py"]
