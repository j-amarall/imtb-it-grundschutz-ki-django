# IMTB IT-Grundschutz KI

Ein webbasiertes KI-Assistenzsystem zur fachlichen Unterstützung bei Fragestellungen rund um
**BSI IT-Grundschutz**, **C5**, **Cloud-Mindeststandards** und verwandte Sicherheitsstandards.

Das System richtet sich insbesondere an **Behörden, öffentliche IT-Dienstleister und Beratungsprojekte**
und ist auf **Datenschutz, Nachvollziehbarkeit und kontrollierten Betrieb** ausgelegt.

---

## 🎯 Zielsetzung

- Unterstützung bei der Einordnung von IT-Sicherheitsstandards (z. B. BSI IT-Grundschutz, C5)
- Keine Speicherung von Chat-Historien
- Klare Trennung von:
  - Antwort
  - Begründung (Reasoning)
  - Hinweis / Disclaimer
- Administrativ kontrollierter Nutzerzugang (Freigabe durch Admin)

---

## 🧱 Architektur

- **Backend:** Django 5
- **Frontend:** Django Templates + CSS
- **KI-Backend:** Langdock Assistants API
- **Authentifizierung:** Django Auth (E-Mail-basiert)
- **Betriebsmodus:** Stateless (keine Chat-Historie)

```text
Browser
  ↓
Django (Auth, Views, Templates)
  ↓
Langdock Assistants API
🔐 Sicherheits- & Datenschutzprinzipien
❌ Keine dauerhafte Speicherung von Nutzereingaben

❌ Keine Chat-Historie (auch nicht in Sessions)

✅ Zugriff nur für freigeschaltete Benutzer

✅ Trennung von Konfiguration und Secrets

✅ Geeignet für Pilot- und Beratungsprojekte im Behördenkontext

Hinweis: Die Anwendung ersetzt keine formale Sicherheits- oder Rechtsberatung.

👥 Benutzerverwaltung
Registrierung über Formular

Neue Benutzer sind standardmäßig deaktiviert

Aktivierung erfolgt durch einen Administrator im Django Admin

Login per E-Mail und Passwort

⚙️ Lokale Entwicklung
Voraussetzungen
Python ≥ 3.10

macOS / Linux

Git

Langdock Account

Installation
git clone git@github.com:j-amarall/imtb-it-grundschutz-ki-django.git
cd imtb-it-grundschutz-ki-django

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Umgebungsvariablen
Erstelle eine .env Datei:

DEBUG=True
SECRET_KEY=change-me

LANGDOCK_API_KEY=your-api-key
LANGDOCK_ASSISTANT_ID=your-assistant-id
LANGDOCK_ASSISTANT_URL=https://api.langdock.com/assistant/completions
Migration & Start
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
🧪 Funktionsumfang
Einzelanfrage-Modus (keine Historie)

Strukturierte Antwortdarstellung:

Antwort

Gedanken / Reasoning (einklappbar)

Hinweis

Ladeindikator bei KI-Antworten

Impressum & Datenschutzerklärung integriert

🚀 Deployment (Ausblick)
Geplant / empfohlen:

Gunicorn + Nginx

Docker / docker-compose

Betrieb hinter Reverse Proxy

HTTPS (TLS)

🛡️ Haftungsausschluss
Dieses Projekt dient der fachlichen Unterstützung.
Die bereitgestellten Informationen stellen keine rechtsverbindliche Auskunft
und keine Zertifizierungsentscheidung dar.

🤝 Unterstützung
Für Beratung, Anpassungen oder den produktiven Einsatz im Behördenumfeld:

IMTB Group GmbH
https://www.imtb.de
