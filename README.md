# Angebotsverwaltungssystem

Ein Desktop-basiertes System zur Verwaltung von Kunden, Angeboten und Angebotsbausteinen.

## Projektstruktur

```
angebotsverwaltung/
├── backend/           # Django Backend
│   ├── api/          # REST API
│   ├── core/         # Hauptanwendung
│   └── requirements.txt
└── frontend/         # Vue.js Frontend
    ├── src/          # Quellcode
    ├── public/       # Statische Dateien
    └── package.json
```

## Technologie-Stack

- Backend: Django mit Django REST Framework
- Frontend: Vue.js
- Datenbank: SQLite (Entwicklung) / MySQL (Produktion)

## Setup-Anweisungen

### Backend Setup

1. Python 3.8+ installieren
2. Virtuelle Umgebung erstellen:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unter Windows: venv\Scripts\activate
   ```
3. Abhängigkeiten installieren:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Datenbank migrieren:
   ```bash
   python manage.py migrate
   ```
5. Entwicklungsserver starten:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. Node.js installieren
2. Abhängigkeiten installieren:
   ```bash
   cd frontend
   npm install
   ```
3. Entwicklungsserver starten:
   ```bash
   npm run serve
   ```

## Features

- Kundenverwaltung
- Angebotsverwaltung
- Angebotsbausteine-Verwaltung (Admin)
- PDF-Export
- E-Mail-Versand
