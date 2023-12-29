# machine_learning/Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY modele.py .
COPY model.joblib .  # Copiez le fichier .joblib dans le conteneur
CMD ["python", "modele.py"]
