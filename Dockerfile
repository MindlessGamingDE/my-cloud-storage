# Basisimage mit Python 3.9
FROM python:3.9-slim

# Setze Arbeitsverzeichnis
WORKDIR /app

# Kopiere requirements.txt und installiere Abhängigkeiten
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Anwendungs-Codes
COPY . .

# Setze Umgebungsvariablen für Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Exponiere Port 5000
EXPOSE 5000

# Startbefehl für die Anwendung
CMD ["flask", "run", "--host=0.0.0.0"]
