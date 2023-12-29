FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY modele.py .
COPY data/ data/
EXPOSE 5000
CMD ["python", "modele.py"]
