# On part d'une base Python légère
FROM python:3.10-slim

# On définit le dossier de travail dans le conteneur
WORKDIR /app

# On installe les bibliothèques nécessaires
RUN pip install --no-cache-dir fastapi uvicorn httpx streamlit

# On copie ton dossier app vers le conteneur
COPY ./app /app

# On crée un script de lancement pour démarrer l'API et l'UI en même temps
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run /app/ui.py --server.port 8501 --server.address 0.0.0.0"]